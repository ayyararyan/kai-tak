import unittest,json,sys,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from frames import *
from evaluate import *
class FrameGateTests(unittest.TestCase):
 def test_official_numeric_checkpoint(self):
  result=official_itrf96_to_hk1980(114+1.079932/3600,22+29/60+8.777176/3600)
  np.testing.assert_allclose(result,[818097.267,838477.970],atol=.004,rtol=0)
 def test_frame_inverse_and_orientation(self):
  p=np.array([[1,2,3],[-3000,1000,140],[2786,0,0]])
  for angle in [0,90,133.2,270]:
   q=runway_to_grid(p,[838000,821000],angle,6);np.testing.assert_allclose(grid_to_runway(q,[838000,821000],angle,6),p,atol=1e-9)
  np.testing.assert_allclose(runway_to_grid([[100,0,0],[0,100,0]],[0,0],0,0),[[0,100,0],[100,0,0]],atol=1e-10)
 def test_unknown_registration_refused(self):
  for f in [runway_to_grid,grid_to_runway]:
   for o,a,z in [(None,130,6),([1,2],None,6),([1,2],130,None)]:
    with self.assertRaises(ValueError):f([[0,0,0]],o,a,z)
 def test_domain_boundaries_and_units(self):
  for c,L in [('dry',25),('wet_no_standing_water',22),('standing_water_or_slush',10)]:
   self.assertTrue(steady_wind_domain(90,L,0,c)['source_condition_passes'])
   self.assertFalse(steady_wind_domain(90,L+.0001,0,c)['source_condition_passes'])
   self.assertIsNone(steady_wind_domain(90,L,0,c)['full_landing_feasible'])
  with self.assertRaises(ValueError):steady_wind_domain(90,-1,0,'dry')
  with self.assertRaises(ValueError):steady_wind_domain(90,1,0,'ice_unknown')
 def test_source_scenario_condition_not_optimality(self):
  self.assertTrue(steady_wind_domain(70,21,799/6,'wet_no_standing_water')['source_condition_passes'])
  self.assertFalse(steady_wind_domain(70,21,799/6,'standing_water_or_slush')['source_condition_passes'])
 def test_continuous_feature_and_time_reporting(self):
  seg=[{'name':'air','duration_s':10,'start_s':0,'coefficients_xyz_m':[[0,100],[0],[30,-10]],'angle_ranges_rad':[[0,0]]*3,'cells':10}]
  f=[{'id':'dated_test_roof','xy_bounds':[[60,-1],[80,1]],'top_upper_m':5,'same_frame_and_epoch_verified':True}]
  r=check_segments(seg,[[0,0,0]],[0,0,0],f,[0,0,0],True)
  self.assertEqual(r['status'],'clear_for_supplied_enclosures');self.assertFalse(r['historical_certified']);self.assertEqual(r['limiting_cleared_feature']['id'],'dated_test_roof');self.assertGreaterEqual(r['limiting_cleared_feature']['time_interval_s'][0],6)
  f[0]['top_upper_m']=None;r=check_segments(seg,[[0,0,0]],[0,0,0],f,[0,0,0],True);self.assertEqual(r['status'],'unknown')
 def test_join_gap_refused(self):
  s={'name':'a','duration_s':1,'start_s':0,'coefficients_xyz_m':[[0,1],[0],[20]],'angle_ranges_rad':[[0,0]]*3,'cells':1}
  with self.assertRaises(ValueError):check_segments([s,dict(s,start_s=1)],[[0,0,0]],[0,0,0],[],[0,0,0],True)
 def test_empty_scene_not_historical(self):
  s={'name':'a','duration_s':1,'start_s':0,'coefficients_xyz_m':[[0,1],[0],[20]],'angle_ranges_rad':[[0,0]]*3,'cells':1}
  r=check_segments([s],[[0,0,0]],[0,0,0],[],[0,0,0]);self.assertEqual(r['status'],'unknown')
 def test_gate_cannot_upgrade_old_certificate(self):
  r=evidence_gate();self.assertEqual(r['frozen_files_changed'],[]);self.assertEqual(r['historical_condition_cells_certified'],0);self.assertIsNone(r['closed_form_optimum']);self.assertIsNone(r['candidate_historical_clearance'])
 def test_inherited_unknowns_preserved(self):
  root=Path(__file__).resolve().parents[1];f=json.loads((root/'integrated/geometry/integrated_evidence.geojson').read_text())['features']
  self.assertEqual(len(f),88)
  self.assertTrue(all(v['properties']['integrated_historical_clearance_eligible'] is False for v in f))
  self.assertEqual(sum(v['properties']['integrated_role']=='unresolved_mapped_form_or_mask' for v in f),46)
if __name__=='__main__':unittest.main(verbosity=2)
