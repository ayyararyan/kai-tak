import unittest,json,math,copy
from pathlib import Path
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer
R=Path(__file__).resolve().parent
class GeometrySemantics(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.projected=json.loads((R/'historical_faces_hk1980.geojson').read_text())['features']
  cls.wgs=json.loads((R/'historical_faces.geojson').read_text())['features']
 def test_complete_reviewed_rows(self):
  self.assertEqual(len(self.projected),45)
  self.assertEqual(len({f['properties']['id'] for f in self.projected}),15)
  self.assertEqual({f['properties']['source_epoch'] for f in self.projected},{'1989-10','1994-07','1997-04'})
 def test_no_unknown_height_extrusion(self):
  for f in self.projected:
   self.assertIsNone(f['properties']['historical_top_hkpd_m']);self.assertIsNone(f['properties']['historical_base_hkpd_m'])
   self.assertFalse(f['properties']['full_structure_mesh'])
 def test_geometries_valid_and_nontrivial(self):
  for f in self.projected:
   g=shape(f['geometry']);self.assertTrue(g.is_valid);self.assertGreater(g.area,100);self.assertLess(g.area,5000)
 def test_round_trip(self):
  t=Transformer.from_crs(4326,2326,always_xy=True).transform
  for p,w in zip(self.projected,self.wgs):self.assertLess(shape(p['geometry']).hausdorff_distance(transform(t,shape(w['geometry']))),.001)
 def test_output_crs_matches_coordinates(self):
  self.assertTrue(all(f['properties']['crs']=='EPSG:4326' for f in self.wgs))
  self.assertTrue(all(f['properties']['crs']=='EPSG:2326' for f in self.projected))
 def test_review_does_not_transfer_to_changed_input(self):
  from accept_geometry import reviewed_candidate_matches
  f=json.loads((R/'digitization_candidates_hk1980.geojson').read_text())['features'][0]
  records=json.loads((R/'reviewed_geometry_manifest.json').read_text())['rows']
  r=next(r for r in records if r['id']==f['properties']['id'] and r['source_id']==f['properties']['source_id'])
  self.assertTrue(reviewed_candidate_matches(f,r))
  for field,value in [('source_epoch','1993-11'),('historical_top_hkpd_m',40),('name','Different identity')]:
   changed=copy.deepcopy(f);changed['properties'][field]=value
   self.assertFalse(reviewed_candidate_matches(changed,r))
  changed=copy.deepcopy(f);changed['geometry']['coordinates'][0][0][0]+=1
  self.assertFalse(reviewed_candidate_matches(changed,r));self.assertFalse(reviewed_candidate_matches(f,None))
 def test_containing_pixel_floor(self):
  import numpy as np
  from affine import Affine
  from digitize import extract
  # Narrow one-cell region contains x=10.75; rounding would choose the black wall.
  a=np.zeros((20,20),dtype=np.uint8);a[1:19,10]=255
  g,meta=extract(a,Affine.identity(),10.75,5.1)
  self.assertIsNotNone(g);self.assertAlmostEqual(g.area,18)
 def test_rejected_wrong_region_absent(self):
  self.assertNotIn('clinic',{f['properties']['id'] for f in self.projected})
 def test_modern_heights_not_transferred(self):
  for f in self.projected:
   for m in f['properties']['modern_correspondences']:
    self.assertFalse(m['height_transfer_to_historical']);self.assertEqual(m['height_epoch'],'2026-09-21')
 def test_temporal_interpolation_not_certified(self):
  for r in json.loads((R/'structure_matches.json').read_text()):
   self.assertFalse(r['continued_presence_every_day_verified']);self.assertFalse(r['historical_height_verified'])
 def test_full_unknown_mask_preserved(self):
  d=json.loads((R/'historical_3d_unknown_mask.geojson').read_text())
  for f in d['features']:
   self.assertFalse(f['properties']['complete_historical_3d']);self.assertIsNone(f['properties']['physical_occupancy'])
 def test_changed_symbol_remains_ambiguous(self):
  rows=[r for r in json.loads((R/'structure_matches.json').read_text()) if r['historical_id']=='lok_sin_school']
  self.assertTrue(rows);self.assertTrue(all(not r['same_depicted_form'] for r in rows))
if __name__=='__main__':unittest.main(verbosity=2)
