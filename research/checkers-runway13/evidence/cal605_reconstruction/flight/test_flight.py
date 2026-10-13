import json
import unittest
import csv
import numpy as np
from build_flight import HERE,limits,axis

class TestFlight(unittest.TestCase):
 def test_axis(self):
  self.assertAlmostEqual(axis(566,566,0,1573,70),0)
  self.assertAlmostEqual(axis(1573,566,0,1573,70),70)
  self.assertAlmostEqual(axis(647,1156,0,647,250),250)
 def test_corner_bounds(self):
  rng=np.random.default_rng(17)
  lo,hi=limits(1012,3,566,0,1573,70,3)
  for _ in range(1000):
   x,x0,x1=np.array([1012,566,1573])+rng.uniform(-3,3,3)
   self.assertTrue(lo<=axis(x,x0,0,x1,70)<=hi)
 def test_anchor_semantics(self):
  m=json.loads((HERE/'trace_anchors.json').read_text());self.assertEqual(len(m['anchors']),123)
  for a in m['anchors']:
   self.assertLessEqual(a['reading_lo'],a['value']);self.assertGreaterEqual(a['reading_hi'],a['value'])
   self.assertLessEqual(a['time_lo_s'],a['time_datum_B_s']);self.assertGreaterEqual(a['time_hi_s'],a['time_datum_B_s'])
  self.assertIn('no coverage probability',m['uncertainty'])
 def test_random_independent_anchor_box_interpolation(self):
  a=json.loads((HERE/'trace_anchors.json').read_text())['anchors']
  with (HERE/'flight_traces.csv').open() as f:r=list(csv.DictReader(f))
  rng=np.random.default_rng(502)
  for name in sorted({q['variable'] for q in a}):
   aa=[q for q in a if q['variable']==name];rr=[q for q in r if q['variable']==name]
   t=np.array([float(q['time_datum_B_s']) for q in rr]);outlo=np.array([float(q['reading_lo']) for q in rr]);outhi=np.array([float(q['reading_hi']) for q in rr])
   for _ in range(500):
    ta=np.array([rng.uniform(q['time_lo_s'],q['time_hi_s']) for q in aa]);va=np.array([rng.uniform(q['reading_lo'],q['reading_hi']) for q in aa]);v=np.interp(t,ta,va)
    self.assertTrue(np.all(v>=outlo-.002));self.assertTrue(np.all(v<=outhi+.002))
 def test_approach_and_wind(self):
  m=json.loads((HERE/'approach_anchors.json').read_text());self.assertEqual(len(m['anchors']),67)
  self.assertEqual(len({a['variable'] for a in m['anchors']}),8)
  self.assertTrue(all(78<=a['time_datum_A_s']<=147 for a in m['anchors']))
  self.assertTrue(all(a['reading_lo']<=a['value']<=a['reading_hi'] for a in m['anchors']))
 def test_no_runway_exit_or_utc_claim(self):
  s=json.loads((HERE/'flight_summary.json').read_text());self.assertFalse(s['last_anchor_is_runway_end']);self.assertIn('No precise UTC sync',s['omissions'])
  self.assertTrue(s['distance_sensitivity_range_m'][0]<s['distance_integral_flag_to_last_anchor_m']<s['distance_sensitivity_range_m'][1])
if __name__=='__main__':unittest.main()
