import unittest,sys,json,math,hashlib
from pathlib import Path
import numpy as np
from fractions import Fraction as F
from itertools import product
sys.path.insert(0,str(Path(__file__).resolve().parent))
from clearance import *
ROOT=Path(__file__).resolve().parents[1]
class EnclosureTests(unittest.TestCase):
 def test_polynomial_exact_known_extrema(self):
  self.assertEqual(polynomial_range([0,1]),(F(0),F(1)))
  lo,hi=polynomial_range([0,4,-4]);self.assertLessEqual(lo,0);self.assertGreaterEqual(hi,1)
  lo,hi=polynomial_range([0,4,-4],.4,.6);self.assertLessEqual(lo,F('0.96'));self.assertGreaterEqual(hi,1)
 def test_random_bernstein_encloses_rational_evaluations(self):
  rng=np.random.default_rng(7)
  for _ in range(60):
   c=rng.integers(-50,50,8).tolist();lo,hi=polynomial_range(c,.2,.8)
   for k in range(101):
    x=F(1,5)+F(3*k,500);v=sum(F(a)*x**i for i,a in enumerate(c));self.assertLessEqual(lo,v);self.assertGreaterEqual(hi,v)
 def test_phase_domain_refusal(self):
  for a,b in [(-.1,1),(0,1.1),(.5,.4)]:
   with self.assertRaises(ValueError):polynomial_range([1,2],a,b)
 def test_empty_nonfinite(self):
  for c in [[],[float('nan')],[float('inf')]]:
   with self.assertRaises(ValueError):polynomial_range(c)
 def test_rotations(self):
  for yaw,pitch,bank in [(0,0,.3),(.2,.4,.5),(-.5,.2,-.7)]:
   R=rotation(yaw,pitch,bank);np.testing.assert_allclose(R.T@R,np.eye(3),atol=1e-15);self.assertAlmostEqual(np.linalg.det(R),1)
  self.assertLess((rotation(0,0,.3)@np.array([0,1,0]))[2],0)
  self.assertGreater((rotation(0,.3,0)@np.array([1,0,0]))[2],0)
  self.assertGreater((rotation(.3,0,0)@np.array([1,0,0]))[1],0)
 def test_box_contains_all_corner_poses(self):
  vs=np.array(list(product([-35,35],[-32,32],[-5,15])),float);angles=[[-.2,.3],[-.1,.2],[-.4,.4]];pr=[[-20,20],[0,10],[50,60]];ref=[-3,2,1]
  B=enclose_body(vs,ref,pr,angles,[2,3,1])
  rng=np.random.default_rng(5)
  for _ in range(400):
   aa=[rng.uniform(*v) for v in angles];pos=np.array([rng.uniform(*v) for v in pr]);track=rng.uniform(-1,1,3)*[2,3,1];p=pos+(vs-ref)@rotation(*aa).T+track
   self.assertTrue(np.all(p>=B[0]));self.assertTrue(np.all(p<=B[1]))
 def test_wing_collision_missed_by_reference_point(self):
  vs=np.array(list(product([-1,1],[-32,32],[-1,1])),float);B=enclose_body(vs,[0,0,0],[[0,0],[0,0],[10,10]],[[0,0]]*3)
  obstacle=[[-.5,30,0],[.5,31,20]]
  self.assertTrue(box_clearance([[0,0,10],[0,0,10]],obstacle)['separated'])
  self.assertFalse(box_clearance(B,obstacle)['separated'])
 def test_tail_clearance_depends_on_pitch(self):
  vs=np.array([[-40,0,5],[0,0,0]])
  flat=enclose_body(vs,[0,0,0],[[0,0],[0,0],[5,5]],[[0,0]]*3)
  pitch=enclose_body(vs,[0,0,0],[[0,0],[0,0],[5,5]],[[0,0],[.3,.3],[0,0]])
  self.assertGreater(flat[0,2],4.9);self.assertLess(pitch[0,2],0)
 def test_unknown_top_refuses(self):
  b=[[-1,-1,100],[1,1,101]];f=[{'id':'roof','xy_bounds':[[-2,-2],[2,2]],'top_upper_m':None,'same_frame_and_epoch_verified':True}]
  self.assertEqual(screen_scene(b,f,True)['status'],'unknown')
 def test_wrong_epoch_refuses(self):
  f=[{'id':'modernroof','xy_bounds':[[-2,-2],[2,2]],'top_upper_m':10,'same_frame_and_epoch_verified':False}]
  self.assertEqual(screen_scene([[-1,-1,100],[1,1,101]],f,True)['status'],'unknown')
 def test_missing_coverage_refuses_empty_obstacles(self):
  self.assertEqual(screen_scene([[0,0,10],[1,1,11]],[],False)['status'],'unknown')
 def test_unknown_outside_swept_footprint_does_not_block_fixture(self):
  f=[{'id':'outside','xy_bounds':[[30,30],[40,40]],'top_upper_m':None}]
  r=screen_scene([[0,0,10],[1,1,11]],f,True);self.assertEqual(r['status'],'clear_for_supplied_enclosures');self.assertFalse(r['historical_certified'])
 def test_narrow_obstacle_between_endpoints(self):
  pos=polynomial_position_box([[0,100],[0],[10]])
  b=enclose_body([[0,0,0]],[0,0,0],pos,[[0,0]]*3)
  obstacle=[[49.999,-.01,0],[50.001,.01,20]]
  self.assertFalse(box_clearance(b,obstacle)['separated'])
  for x in [0,100]:self.assertTrue(box_clearance([[x,0,10],[x,0,10]],obstacle)['separated'])
 def test_reference_translation_velocity_acceleration(self):
  t=.4;w=.3;R=rotation(w*t,0,0);omega=[0,0,w];alpha=[0,0,0];bc=np.array([3,4,5.]);br=np.zeros(3)
  r,v,a=reference_kinematics(np.zeros(3),np.zeros(3),np.zeros(3),R,omega,alpha,bc,br)
  h=1e-4;f=lambda t:rotation(w*t,0,0)@bc
  np.testing.assert_allclose(v,(f(t+h)-f(t-h))/(2*h),atol=1e-8)
  np.testing.assert_allclose(a,(f(t+h)-2*f(t)+f(t-h))/h**2,atol=2e-7)
 def test_invalid_reference_and_tracking(self):
  with self.assertRaises(ValueError):enclose_body([[0,0,0]],[0,0],[[0,0]]*3,[[0,0]]*3)
  with self.assertRaises(ValueError):enclose_body([[0,0,0]],[0,0,0],[[0,0]]*3,[[0,0]]*3,[-1,0,0])
  with self.assertRaises(ValueError):enclose_body([[0,0,0]],[0,0,0],[[0,0]]*3,[[0,float('inf')]]*3)
 def test_touching_not_clear(self):
  self.assertFalse(box_clearance([[0,0,0],[1,1,1]],[[1,0,0],[2,1,1]])['separated'])
 def test_clearance_domain_validation(self):
  with self.assertRaises(ValueError):box_clearance([[2,0,0],[1,1,1]],[[0,0,0],[1,1,1]])
 def test_aircraft_geometry_extent(self):
  r=json.loads((ROOT/'integrated/geometry/airframe_envelope.json').read_text());lo,hi=np.array(r['bounds_m']);self.assertGreaterEqual(hi[2],19.51);self.assertGreaterEqual(hi[0]-lo[0],70.67);self.assertGreaterEqual(hi[1]-lo[1],64.92);self.assertFalse(r['clearance_eligible_historical'])
 def test_frozen_baselines_unchanged(self):
  r=json.loads((ROOT/'integrated/source_manifest.json').read_text())
  for p,h in r['files'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h,p)
 def test_prior_counterfactual_polynomial_ranges(self):
  r=json.loads((ROOT/'counterfactual/formula.json').read_text())
  for phase in r['phases']:
   for k in range(20):
    a=k/20;b=(k+1)/20;box=np.array(polynomial_position_box(phase['coefficients_xyz_m'],a,b))
    for s in np.linspace(a,b,20):
     p=np.array([np.polynomial.polynomial.polyval(s,c) for c in phase['coefficients_xyz_m']]);self.assertTrue(np.all(p>=box[:,0]-1e-8));self.assertTrue(np.all(p<=box[:,1]+1e-8))
if __name__=='__main__':unittest.main(verbosity=2)
