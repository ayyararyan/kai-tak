"""Affine semantics, official source integrity, and delivered raster acceptance."""
import json, math, unittest
from pathlib import Path
import numpy as np
import rasterio
from PIL import Image
from register_sheets import tfw_affine,core_bounds,sha,ROOT,OUT

class WorldFileTests(unittest.TestCase):
 def test_center_to_edge(self):
  t=tfw_affine('2\n0\n0\n-3\n100\n200')
  self.assertEqual(t*(.5,.5),(100,200))
  self.assertEqual(t*(0,0),(99,201.5))
 def test_rotated_center_and_inverse(self):
  t=tfw_affine('2\n0.3\n0.4\n-3\n100\n200')
  self.assertEqual(t*(.5,.5),(100,200))
  for p in [(0,0),(123,456),(-17.2,800.3)]:np.testing.assert_allclose((~t)*(t*p),p,atol=1e-10)
 def test_bad_tfw_refused(self):
  for s in ['0 0 0 0 1 2','nan 0 0 -1 1 2','1 0 0 -1 1']:
   with self.assertRaises(ValueError):tfw_affine(s)

class DeliveredRegistrationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.inv=json.loads((OUT/'sheet_registration_inventory.json').read_text())
 def test_all_original_archives_verified(self):
  self.assertEqual(self.inv['total'],227)
  self.assertEqual(len(self.inv['records']),227)
  self.assertEqual(len({r['source_id'] for r in self.inv['records']}),227)
  for r in self.inv['records']:
   with self.subTest(source=r['source_id']):
    self.assertTrue(r['metadata_checks_pass']);self.assertTrue(r['source_sha256_matches'])
    self.assertEqual(sha(ROOT.parent.parent/r['source_archive']),r['source_sha256'])
    self.assertIsNone(r['cartographic_ground_accuracy_m'])
 def test_three_rgb_outputs_have_exact_core_and_hashes(self):
  for d in self.inv['rendered']:
   stem='11-NE-11A_'+d['source_date']+'_core'
   self.assertEqual(d['bounds'],[837500,821000,838250,821600])
   for ext,key in [('tif','tif_sha256'),('png','png_sha256')]:self.assertEqual(sha(OUT/(stem+'.'+ext)),d[key])
   with rasterio.open(OUT/(stem+'.tif')) as ds:
    self.assertEqual(ds.crs.to_epsg(),2326);self.assertEqual(ds.count,3)
    self.assertEqual(list(ds.bounds),d['bounds']);self.assertEqual(ds.width,3000);self.assertEqual(ds.height,2400)
    np.testing.assert_array_equal(np.moveaxis(ds.read(),0,2),np.array(Image.open(OUT/(stem+'.png'))))
 def test_independent_grid_evidence_exists_and_residuals_recompute(self):
  checks=self.inv['printed_grid_checks'];self.assertEqual(len(checks),3)
  for c in checks:
   self.assertEqual(len(c['points']),4);self.assertIsNone(c['cartographic_ground_accuracy_m'])
   for p in c['points']:
    self.assertAlmostEqual(p['residual_distance_m'],math.hypot(p['observed_e']-p['grid_e'],p['observed_n']-p['grid_n']))
   self.assertAlmostEqual(c['rms_2d_m'],math.sqrt(sum(p['residual_distance_m']**2 for p in c['points'])/4))
   self.assertTrue((OUT/c['image']).exists())
 def test_uninspected_sheets_not_promoted(self):
  unchecked=[r for r in self.inv['records'] if r['printed_grid_status']=='not_independently_checked']
  self.assertEqual(len(unchecked),224)
  for r in unchecked:self.assertNotIn('printed_grid_rms_m',r)

class FailClosedTests(unittest.TestCase):
 def test_bad_record_cannot_render(self):
  from register_sheets import render
  for r in [{'metadata_checks_pass':True,'source_sha256_matches':False},{'metadata_checks_pass':False,'source_sha256_matches':True}]:
   with self.assertRaisesRegex(ValueError,'Refusing'):render(r)
 def test_tampered_zip_preserves_audit_without_rendering(self):
  import tempfile,zipfile
  from unittest.mock import patch
  from pyproj import Transformer
  from rasterio.transform import from_origin
  import register_sheets as rs
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'maps').mkdir();out=p/'out';out.mkdir()
   tf=from_origin(837500,821010,1,1)
   with rasterio.open(p/'test.tif','w',driver='GTiff',width=10,height=10,count=1,dtype='uint8',transform=tf) as ds:ds.write(np.zeros((1,10,10),dtype='uint8'))
   z=p/'maps/test.zip'
   with zipfile.ZipFile(z,'w') as f:
    f.write(p/'test.tif','test.tif');f.writestr('test.tfw','1\n0\n0\n-1\n837500.5\n821009.5\n')
   before=sha(z)
   with z.open('ab') as f:f.write(b'TAMPER_TRAILING_BYTES')
   r={'source_id':'1980_1990:678','sheet':'test','edition_date':'1989-10-01','file':'maps/test.zip','status':'validated_zip','sha256':before}
   (p/'maps/test.json').write_text(json.dumps(r))
   proj=Transformer.from_crs(2326,4326,always_xy=True)
   ring=[proj.transform(*q) for q in [(837500,821000),(837510,821000),(837510,821010),(837500,821010),(837500,821000)]]
   f={'type':'Feature','properties':{'source_id':r['source_id']},'geometry':{'type':'Polygon','coordinates':[ring]}}
   (p/'aoi_sheet_index.geojson').write_text(json.dumps({'features':[f]}))
   with patch.object(rs,'SHEETS',p),patch.object(rs,'OUT',out),patch.object(rs,'ROOT',p/'placeholder/root'),patch.object(rs,'render') as render_mock:
    with self.assertRaisesRegex(ValueError,'audit failed'):rs.main()
    render_mock.assert_not_called()
   inv=json.loads((out/'sheet_registration_inventory.json').read_text())
   self.assertEqual(inv['metadata_pass'],0);self.assertFalse(inv['records'][0]['source_sha256_matches']);self.assertEqual(inv['rendered'],[])

if __name__=='__main__':unittest.main()
