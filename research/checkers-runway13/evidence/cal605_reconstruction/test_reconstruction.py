import csv,itertools,json,math,unittest
from pathlib import Path
import numpy as np
from reconstruct import axis_value,axis_range,stop_remaining,required_deceleration,segment_time,segment_position,G,KNOT,ROOT,sha

class ReconstructionTests(unittest.TestCase):
    def test_axes_and_inverse(self):
        self.assertEqual(axis_value(212,212,1331,-2800,0),-2800)
        self.assertEqual(axis_value(1331,212,1331,-2800,0),0)
        self.assertEqual(axis_value(245,995,245,0,200),200)
        self.assertEqual(axis_value(995,995,245,0,200),0)
    def test_interval_encloses_continuous_perturbations(self):
        rng=np.random.default_rng(20261013)
        for p in [215,500,1000,1330]:
            lo,hi=axis_range(p,212,1331,-2800,0,3,2)
            for _ in range(100):
                v=axis_value(p+rng.uniform(-3,3),212+rng.uniform(-2,2),1331+rng.uniform(-2,2),-2800,0)
                self.assertTrue(lo<=v<=hi)
        with self.assertRaises(ValueError):axis_range(1,0,3,0,1,1,2)
    def test_stopping_decomposition_and_units(self):
        a=json.loads((ROOT/'analysis.json').read_text());cases=a['fixed_formula']
        self.assertAlmostEqual(cases[0]['remaining_m']-cases[-1]['remaining_m'],sum(a['decomposition_m'].values()))
        self.assertAlmostEqual(KNOT*3600,1852)
        self.assertAlmostEqual(stop_remaining(2786,480,160*KNOT,2,.15*G),-161.5217894701882)
    def test_frontier(self):
        v=129*KNOT;R=880;t=R/v-v/(.6*G)
        self.assertAlmostEqual(required_deceleration(v,R,t),.3*G)
        self.assertGreater(required_deceleration(v,R,2)/G,.3)
        self.assertEqual(required_deceleration(10,10,2),math.inf)
    def test_invalid_inputs(self):
        for args in [(100,0,1,0,0),(100,0,-1,0,1),(100,0,1,-1,1),(100,0,float('nan'),0,1)]:
            with self.assertRaises(ValueError):stop_remaining(*args)
    def test_manifest_and_no_ci(self):
        manifest=json.loads((ROOT/'manifest.json').read_text())
        workspace=ROOT.parents[3]
        for name,digest in manifest['source_sha256'].items():self.assertEqual(sha(workspace/name),digest)
        a=json.loads((ROOT/'analysis.json').read_text())
        self.assertIsNone(a['uncertainty']['coverage_probability'])
        self.assertIsNone(a['uncertainty']['clock_offset_to_wind'])
    def test_trace_order_and_enclosure(self):
        with (ROOT/'rollout_trace.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),35)
        distances=[float(r['remaining_m']) for r in rows]
        self.assertTrue(all(a>b for a,b in zip(distances,distances[1:])))
        for r in rows:
            self.assertLessEqual(float(r['speed_reading_low_kt']),float(r['groundspeed_kt']))
            self.assertGreaterEqual(float(r['speed_reading_high_kt']),float(r['groundspeed_kt']))
    def test_piecewise_formula_against_quadrature(self):
        from scipy.integrate import quad
        for v0,v1,d in [(80,70,200),(70,70,200),(30,60,100),(50,50.000000001,90)]:
            duration=segment_time(d,v0,v1)
            numeric=quad(lambda x:1/(v0+(v1-v0)*x/d),0,d)[0]
            self.assertAlmostEqual(duration,numeric,places=10)
            self.assertAlmostEqual(segment_position(duration,-d,0,v0,v1),0,places=8)
            self.assertEqual(segment_position(0,-d,0,v0,v1),-d)
        with self.assertRaises(ValueError):segment_position(1,0,0,1,1)
        with self.assertRaises(ValueError):segment_time(1,0,1)
        with self.assertRaises(ValueError):required_deceleration(float('nan'),100)
    def test_unbounded_frontier_is_explicit(self):
        with (ROOT/'rollout_trace.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(rows[-1]['required_decel_reading_high_status'],'unbounded_as_remaining_approaches_zero')
    def test_source_discrepancy_preserved(self):
        with (ROOT/'flight_events.csv').open() as f: rows={r['event_id']:r for r in csv.DictReader(f)}
        self.assertEqual(rows['N03']['runway_remaining_m'],'2300')
        self.assertEqual(rows['A01']['runway_remaining_m'],'2250')
        self.assertEqual(rows['N08']['runway_remaining_m'],'880')
        self.assertEqual(rows['A04']['runway_remaining_m'],'900')

if __name__=='__main__':unittest.main()
