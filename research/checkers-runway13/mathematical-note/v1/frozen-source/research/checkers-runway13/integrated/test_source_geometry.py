import unittest,json,hashlib,sys
from pathlib import Path
import numpy as np
from shapely.geometry import shape
from pyproj import Transformer
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
class SourceGeometryTests(unittest.TestCase):
 def test_all_scene_geometries_and_bound_sources(self):
  features=load('integrated/geometry/integrated_evidence.geojson')['features']
  for f in features:
   self.assertTrue(shape(f['geometry']).is_valid);self.assertFalse(shape(f['geometry']).is_empty)
   p=f['properties'];self.assertFalse(p['integrated_historical_clearance_eligible']);self.assertEqual(hashlib.sha256((R/p['integrated_source_path']).read_bytes()).hexdigest(),p['integrated_source_sha256'])
 def test_hill_readings_and_nonpromotion(self):
  f=load('integrated/geometry/historical_hill_terrain.geojson')['features'];lines=[x for x in f if x['geometry']['type']=='LineString'];pts=[x for x in f if x['geometry']['type']=='Point']
  self.assertEqual(sorted(x['properties']['elevation_HKPD_m'] for x in lines),[60,80]);self.assertEqual(len(pts),9);self.assertEqual(sum(x['properties']['elevation_HKPD_m'] is None for x in pts),1)
  for v in f:
   p=v['properties'];self.assertIsNone(p['physical_upper_bound_m']);self.assertFalse(p['query_date_presence_certified']);self.assertFalse(p['is_full_structure_top'])
   if 'source_crop' in p:self.assertEqual(hashlib.sha256((R/p['source_crop']).read_bytes()).hexdigest(),p['source_crop_sha256'])
 def test_new_geometry_coordinate_roundtrip(self):
  t=Transformer.from_crs(4326,2326,always_xy=True)
  for filename in ['historical_hill_terrain.geojson','mapped_runway_edges.geojson','historical_seawall.geojson','historical_approach_lights.geojson']:
   for f in load('integrated/geometry/'+filename)['features']:
    c=np.array(f['geometry']['coordinates']);c=c[None,:] if c.ndim==1 else c;actual=np.array(t.transform(c[:,0],c[:,1])).T;target=np.array(f['properties']['EN_m']);target=target[None,:] if target.ndim==1 else target;self.assertLess(float(np.linalg.norm(actual-target,axis=1).max()),.002)
 def test_runway_identity_diagnostic_is_not_registration(self):
  r=load('integrated/geometry/mapped_runway_axis_check.json');self.assertLess(abs(r['normal_width_at_mosaic_x400_m']-61),.2);self.assertGreater(r['threshold_crosscheck_with_mapped_axis']['disagreement_m'],70);self.assertFalse(r['threshold_crosscheck_with_mapped_axis']['accepted']);self.assertIsNone(r['source_error_hard_bound_m'])
 def test_source_observations_hashes_and_unknown_fixdatum(self):
  rows=load('integrated/source_observations.json')['observations'];self.assertEqual(len(rows),28)
  for r in rows:self.assertEqual(hashlib.sha256((R/r['source_path']).read_bytes()).hexdigest(),r['source_sha256'])
  fix=next(r for r in rows if r['id']=='IGS-GPINOP-FIX');self.assertIsNone(fix['value']['horizontal_datum'])
 def test_requirement_coverage_every_id_once(self):
  spec=(R/'integrated/SPEC.md').read_text();tr=(R/'integrated/TRACEABILITY.md').read_text();ids=[line.split('|')[1].strip() for line in spec.splitlines() if line.startswith('| ') and '-' in line.split('|')[1] and line.split('|')[1].strip()!='ID'];self.assertEqual(len(ids),16)
  for id in ids:self.assertEqual(sum(line.startswith('| '+id+' |') for line in tr.splitlines()),1,id)
if __name__=='__main__':unittest.main(verbosity=2)
