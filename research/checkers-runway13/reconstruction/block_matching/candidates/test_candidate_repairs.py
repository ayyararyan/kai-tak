import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import cv2
import numpy as np
from affine import Affine
from rasterio.io import MemoryFile
from shapely.geometry import Point
from extract_candidates import read_gray,coverage_edge_labels,candidate_status,polygonize_cells,source_coverage
import extract_candidates

class CandidateRegressions(unittest.TestCase):
    def test_tampered_archive_rejected_before_zip_decoding(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'map.zip';path.write_bytes(b'changed archive bytes')
            with patch.object(extract_candidates,'MAPS',Path(td)):
                with self.assertRaisesRegex(ValueError,'SHA256'):
                    extract_candidates.read_map({'file':'map.zip','sha256':'0'*64})

    def test_palette_is_rejected_before_averaging_indices(self):
        for colors in [{0:(0,0,0,255),1:(255,255,255,255)},{0:(255,255,255,255),1:(0,0,0,255)}]:
            with MemoryFile() as mem:
                with mem.open(driver='GTiff',width=2,height=2,count=1,dtype='uint8',transform=Affine(1,0,100,0,-1,200)) as ds:
                    ds.write(np.array([[0,1],[1,0]],dtype='uint8'),1);ds.write_colormap(1,colors)
                with mem.open() as ds:
                    with self.assertRaisesRegex(ValueError,'grayscale'):read_gray(ds,(1,1))

    def test_nodata_is_rejected_not_treated_as_clear_or_ink(self):
        with MemoryFile() as mem:
            with mem.open(driver='GTiff',width=2,height=2,count=1,dtype='uint8',nodata=0,transform=Affine(1,0,100,0,-1,200)) as ds:ds.write(np.zeros((2,2),dtype='uint8'),1)
            with mem.open() as ds:
                with self.assertRaisesRegex(ValueError,'Nodata'):read_gray(ds,(1,1))

    def test_grayscale_averages_brightness(self):
        with MemoryFile() as mem:
            with mem.open(driver='GTiff',width=2,height=2,count=1,dtype='uint8',transform=Affine(1,0,100,0,-1,200)) as ds:ds.write(np.array([[0,255],[255,0]],dtype='uint8'),1)
            with mem.open() as ds:self.assertAlmostEqual(int(read_gray(ds,(1,1))[0,0]),128,delta=1)

    def test_coverage_cut_cannot_be_strong_even_if_template_inside(self):
        valid=np.zeros((10,10),bool);valid[2:8,2:8]=True
        # An entirely open white plane becomes finite only because of coverage clipping.
        _,labels,_,_=cv2.connectedComponentsWithStats(valid.astype('uint8'),connectivity=8)
        label=int(labels[4,4]);truncated=label in coverage_edge_labels(labels,valid)
        self.assertTrue(truncated)
        self.assertEqual(candidate_status(False,1.,.9,truncated),'ambiguous_region_truncated')

    def test_genuinely_enclosed_component_remains_strong_candidate(self):
        valid=np.ones((10,10),bool);white=np.zeros((10,10),'uint8');white[3:7,3:7]=1
        _,labels,_,_=cv2.connectedComponentsWithStats(white,connectivity=8)
        truncated=int(labels[4,4]) in coverage_edge_labels(labels,valid)
        self.assertFalse(truncated)
        self.assertEqual(candidate_status(False,1.,.9,truncated),'strong_content_candidate_unverified')

    def test_pixel_cell_area_and_bounds_no_half_pixel_erosion(self):
        mask=np.ones((4,7),'uint8');tf=Affine(.25,0,837500,0,-.25,821600)
        p=polygonize_cells(mask,tf)
        self.assertEqual(p.area,28*.25**2)
        self.assertEqual(p.bounds,(837500,821599,837501.75,821600))

    def test_single_pixel_wide_component_is_not_dropped(self):
        mask=np.ones((1,200),'uint8');p=polygonize_cells(mask,Affine(.25,0,0,0,-.25,0))
        self.assertEqual(p.area,12.5)

    def test_holes_and_diagonal_components_preserve_pixel_area(self):
        mask=np.ones((10,10),'uint8');mask[2:8,2:8]=0
        p=polygonize_cells(mask,Affine(.25,0,0,0,-.25,0))
        self.assertEqual(len(p.interiors),1);self.assertEqual(p.area,mask.sum()*.25**2)
        p=polygonize_cells(np.eye(4,dtype='uint8'),Affine.identity())
        self.assertTrue(p.is_valid);self.assertEqual(p.area,4)

    def test_actual_index_core_edges(self):
        p=source_coverage({'source_id':'1980_1990:678'})
        left,bottom,right,top=p.bounds
        self.assertLess(max(abs(v-round(v)) for v in p.bounds),.01)
        for inside,outside in [((left+.02,(bottom+top)/2),(left-.02,(bottom+top)/2)),((right-.02,(bottom+top)/2),(right+.02,(bottom+top)/2)),(((left+right)/2,bottom+.02),((left+right)/2,bottom-.02)),(((left+right)/2,top-.02),((left+right)/2,top+.02))]:
            self.assertTrue(p.covers(Point(inside)));self.assertFalse(p.covers(Point(outside)))

if __name__=='__main__':unittest.main()
