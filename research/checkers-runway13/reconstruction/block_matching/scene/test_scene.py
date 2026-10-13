"""Delivered scene semantics: no false historical volumes or mixed vertical datums."""
import csv,json,unittest,hashlib
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
class SceneTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=json.loads((R/'scene.json').read_text())
 def test_historical_null_heights_and_exact_source_geometry(self):
  source=json.loads((R.parent/'historical_faces_hk1980.geojson').read_text())['features']
  self.assertEqual(len(source),45);self.assertEqual(len(self.s['historical_faces']),45)
  for f,s in zip(self.s['historical_faces'],source):
   self.assertEqual(f['geometry'],s['geometry'])
   for k in ('height_m','base_hkpd_m','top_hkpd_m','physical_volume'):self.assertIsNone(f[k])
   self.assertFalse(f['display_plane_is_physical_surface'])
 def test_modern_is_separate_epoch_datum_and_valid_component(self):
  m=self.s['modern'];self.assertEqual(m['epoch'],'2026-09-21');self.assertEqual(m['vertical_datum'],'HKPD')
  self.assertGreater(len(m['features']),0)
  for f in m['features']:
   self.assertFalse(f['height_transfer_to_historical']);self.assertGreaterEqual(f['top_hkpd_m'],f['base_hkpd_m']);self.assertEqual(f['category'],'modern_2026_comparison_only')
 def test_sparse_relative_heights_not_hkpd(self):
  s=self.s['stereo'];self.assertEqual(s['vertical_datum'],'relative_ground_plane');self.assertEqual(len(s['points']),1318)
  for p in s['points']:self.assertIsNone(p['hkpd_elevation_m'])
  self.assertFalse(s['physical_surface_mesh']);self.assertIsNone(s['calibrated_error_bounds'])
 def test_dense_display_subsample_exact_source_coordinates(self):
  d=self.s['dense']
  with (R.parent/'aerial_registration/dense_stereo_points.csv').open() as f:source=list(csv.DictReader(f))
  self.assertEqual(d['total_source_points'],len(source));self.assertEqual(len(d['points']),len(source[::d['display_stride']]))
  for p,r in zip(d['points'],source[::d['display_stride']]):
   self.assertEqual(p[0],int(r['dense_id']))
   np.testing.assert_allclose([p[1]+837500,p[2]+821000,p[3]],[float(r['easting_hk1980_m']),float(r['northing_hk1980_m']),float(r['z_above_fitted_local_park_road_plane_m'])],atol=1e-8,rtol=0)
  self.assertIsNone(d['absolute_vertical_datum']);self.assertFalse(d['physical_mesh'])
 def test_unchanged_input_hashes(self):
  for name,h in self.s['source_files'].items():self.assertEqual(hashlib.sha256((R.parent/name).read_bytes()).hexdigest(),h)
  for lane in ('sparse','dense'):
   d=self.s['stereo' if lane=='sparse' else 'dense']
   for ext in ('csv','ply'):self.assertEqual(hashlib.sha256((R.parent/f'aerial_registration/{lane}_stereo_points.{ext}').read_bytes()).hexdigest(),d[ext+'_sha256'])
 def test_offline_bundle_and_separate_view_controls(self):
  html=(R/'index.html').read_text();self.assertIn('plotly.js',html.lower());self.assertNotIn('<script src=',html)
  for v in ('stereo','sources','modern'):self.assertIn('data-view="'+v+'"',html)
  self.assertNotIn('/*SCENE_DATA*/',html);self.assertNotIn('/*PLOTLY_BUNDLE*/',html)

class RegenerationGuards(unittest.TestCase):
 def test_sparse_rejected_regenerated_rows_cannot_reenter(self):
  import tempfile
  from unittest.mock import patch
  import build_scene
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);d=root/'aerial_registration';d.mkdir()
   report={'vertical_reference':'relative plane NOT HKPD','source_date':'1993-11-02','source_frames':['A36142','A36143']}
   (d/'sparse_stereo_report.json').write_text(json.dumps(report));(d/'sparse_stereo_points.ply').write_text('fixture only')
   base=dict(track_id='1',easting_hk1980_m='837600',northing_hk1980_m='821200',z_above_fitted_local_park_road_plane_m='12',r='100',g='100',b='100',reprojection_rms_px='1',within_map_control_hull='True',surface_class='roof',manual_surface_note='fixture',passes_diagnostic_5px_filter='True',positive_depth_both_views='True')
   rows=[base,{**base,'track_id':'2','passes_diagnostic_5px_filter':'False'},{**base,'track_id':'3','positive_depth_both_views':'False'},{**base,'track_id':'4','positive_depth_both_views':''}]
   with (d/'sparse_stereo_points.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(base));w.writeheader();w.writerows(rows)
   with patch.object(build_scene,'ROOT',root):result=build_scene.stereo_adapter()
   self.assertEqual(result['source_row_count'],4);self.assertEqual(result['accepted_row_count'],1);self.assertEqual(result['omitted_row_count'],3);self.assertEqual([p['id'] for p in result['points']],[1])

 def test_mesh_with_changed_producer_inputs_is_refused(self):
  import tempfile
  from unittest.mock import patch
  import build_scene
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);d=root/'aerial_registration';d.mkdir()
   (d/'observed_surface_mesh.ply').write_text('not reached because source integrity must be checked first')
   (d/'dense_stereo_points.csv').write_text('changed data')
   report={'watertight':False,'vertical_reference':'relative plane NOT HKPD','input_sha256':{'dense_stereo_points.csv':'0'*64}}
   (d/'observed_surface_mesh_report.json').write_text(json.dumps(report))
   with patch.object(build_scene,'ROOT',root):
    with self.assertRaisesRegex(ValueError,'Mesh input changed'):build_scene.mesh_adapter()

class FinalSurfaceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=json.loads((R/'scene.json').read_text())
 def test_courtyard_boundaries_preserved(self):
  component=next(f for f in self.s['modern']['features'] if f['id']=='3810921432T20050430:0')
  self.assertEqual(len(component['rings_local']),2)
  self.assertEqual(len(component['geometry']['coordinates']),2)
  for a,b in zip(component['rings_local'],component['geometry']['coordinates']):
   np.testing.assert_allclose(np.array(a)+[837500,821000],b,atol=0.000051,rtol=0)
  js=(R/'template.html').read_text();self.assertIn('for(const ring of f.rings_local)',js)
 def test_mesh_source_datum_counts_and_hashes(self):
  m=self.s['observed_mesh'];self.assertTrue(m['available']);self.assertFalse(m['watertight']);self.assertFalse(m['complete_buildings']);self.assertEqual(m['vertical_datum'],'relative_ground_plane')
  self.assertEqual(len(m['vertices']),m['report']['counts']['retained_mesh_vertices']);self.assertEqual(len(m['faces']),m['report']['counts']['accepted_faces'])
  for ext in ('ply','glb'):self.assertEqual(hashlib.sha256((R.parent/f'aerial_registration/observed_surface_mesh.{ext}').read_bytes()).hexdigest(),m[ext+'_sha256'])
  for name,h in m['report']['input_sha256'].items():self.assertEqual(hashlib.sha256((R.parent/'aerial_registration'/name).read_bytes()).hexdigest(),h)
  self.assertTrue(all(min(f[:3])>=0 and max(f[:3])<len(m['vertices']) for f in m['faces']))
 def test_browser_verification_not_claimed(self):
  v=json.loads((R/'validation.json').read_text());self.assertFalse(v['browser_interaction_verified']);self.assertIn('navigation policy blocked',v['browser_verification_blocker'])

if __name__=='__main__':unittest.main()
