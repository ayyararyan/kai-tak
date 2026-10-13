import unittest,tempfile,json,hashlib
from pathlib import Path
import numpy as np
from stereo_guardrails import validate_manual_labels,point_validity,fit_ground_plane,intersect_rays_with_plane,similarity_alignment,gated_height,all_nonzero_bilinear_contributors_valid
class StereoGuardrailTests(unittest.TestCase):
 def setUp(self):
  self.X=np.array([[0.,0.,10.],[1.,0.,10.],[0.,1.,10.],[1.,1.,10.]])
  self.R=np.eye(3);self.t=np.array([[-1.],[0.],[0.]]);self.P1=np.c_[np.eye(3),np.zeros(3)];self.P2=np.c_[self.R,self.t]
  self.p1=self.X[:,:2]/self.X[:,2,None];Y=self.X+self.t.ravel();self.p2=Y[:,:2]/Y[:,2,None]
 def test_valid_geometry(self):
  valid,e=point_validity(self.X,self.R,self.t,self.P1,self.P2,self.p1,self.p2);self.assertTrue(valid.all());self.assertLess(e.max(),1e-12)
 def test_negative_depth_rejected(self):
  X=self.X.copy();X[0,2]=-10
  valid,_=point_validity(X,self.R,self.t,self.P1,self.P2,self.p1,self.p2);self.assertFalse(valid[0])
 def test_nonfinite_point_rejected(self):
  X=self.X.copy();X[0,0]=np.nan
  valid,_=point_validity(X,self.R,self.t,self.P1,self.P2,self.p1,self.p2);self.assertFalse(valid[0])
 def test_high_reprojection_rejected(self):
  q=self.p1.copy();q[0,0]+=20
  valid,_=point_validity(self.X,self.R,self.t,self.P1,self.P2,q,self.p2);self.assertFalse(valid[0])
 def test_rejected_ground_cannot_define_plane(self):
  with self.assertRaises(ValueError):fit_ground_plane(self.X,[0,1,2],[False,True,True,True])
 def test_collinear_plane_rejected(self):
  with self.assertRaises(ValueError):fit_ground_plane(np.array([[0,0,1],[1,0,1],[2,0,1.]]),[0,1,2],[True]*3)
 def test_valid_plane_and_holdout_not_fitted(self):
  X=self.X.copy();X[3,2]=15;c,n=fit_ground_plane(X,[0,1,2],[True]*4);self.assertAlmostEqual(abs((X[3]-c)@n),5.)
 def test_parallel_ray_rejected(self):
  with self.assertRaises(ValueError):intersect_rays_with_plane(np.zeros(3),np.array([[1.,0,0]]),np.array([0.,0,10]),np.array([0.,0,1]))
 def test_behind_camera_plane_rejected(self):
  with self.assertRaises(ValueError):intersect_rays_with_plane(np.zeros(3),np.array([[0.,0,1]]),np.array([0.,0,-10]),np.array([0.,0,1]))
 def test_plane_intersection_valid(self):
  X=intersect_rays_with_plane(np.zeros(3),np.array([[1.,0,1]]),np.array([0.,0,10]),np.array([0.,0,1]));np.testing.assert_allclose(X,[[10,0,10]])
 def test_similarity_collinear_rejected(self):
  X=np.array([[0.,0,0],[1,0,0],[2,0,0]])
  with self.assertRaises(ValueError):similarity_alignment(X,X)
 def test_similarity_scale_recovered(self):
  Y=3*self.X+np.array([5,7,-30]);s,A,b=similarity_alignment(self.X,Y);self.assertAlmostEqual(s,3.);np.testing.assert_allclose(s*self.X@A+b,Y,atol=1e-10)
 def test_invalid_roof_never_reports_height(self):
  self.assertIsNone(gated_height(self.X,[False]*4,0));X=self.X.copy();X[0,2]=np.nan;self.assertIsNone(gated_height(X,[True]*4,0))
 def test_accepted_roof_is_not_zeroed(self):self.assertEqual(gated_height(self.X,[True]*4,0),10.)
 def fixture(self,p):
  a=np.array([[1.,2.],[3.,4.],[5.,6.]]);b=a+1;np.savez(p/'tracks.npz',p1=a,p2=b,fmask=np.ones(3,dtype=bool),F=np.eye(3))
  for fr in ['A36142','A36143']:(p/(fr+'.jpg')).write_bytes(fr.encode())
  book={'stereo_tracks_npz_sha256':hashlib.sha256((p/'tracks.npz').read_bytes()).hexdigest(),'frame_sha256':{fr:hashlib.sha256((p/(fr+'.jpg')).read_bytes()).hexdigest() for fr in ['A36142','A36143']},'labels':[{'fundamental_inlier_row':0,'frame42_xy':a[0].tolist(),'frame43_xy':b[0].tolist()}]};(p/'labels.json').write_text(json.dumps(book));return book
 def test_pinned_labels_validate(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);self.fixture(p);validate_manual_labels(p/'tracks.npz',p/'labels.json',p)
 def test_changed_track_archive_refused(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);self.fixture(p);q=p/'tracks.npz';q.write_bytes(q.read_bytes()+b'changed')
   with self.assertRaisesRegex(ValueError,'hash changed'):validate_manual_labels(q,p/'labels.json',p)
 def test_row_reassignment_refused(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);book=self.fixture(p);book['labels'][0]['fundamental_inlier_row']=1;(p/'labels.json').write_text(json.dumps(book))
   with self.assertRaisesRegex(ValueError,'coordinates disagree'):validate_manual_labels(p/'tracks.npz',p/'labels.json',p)
 def test_changed_frame_refused(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);self.fixture(p);(p/'A36142.jpg').write_bytes(b'changed')
   with self.assertRaisesRegex(ValueError,'source frame changed'):validate_manual_labels(p/'tracks.npz',p/'labels.json',p)
 def test_duplicate_correspondence_refused(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);book=self.fixture(p);book['labels'].append(book['labels'][0]);(p/'labels.json').write_text(json.dumps(book))
   with self.assertRaisesRegex(ValueError,'duplicate'):validate_manual_labels(p/'tracks.npz',p/'labels.json',p)
 def test_invalid_sentinel_blend_cannot_pass_lr_gate(self):
  # Actual reviewed failure: valid5.0625 blended with sentinel−32 at x=.25.
  interpolated=.75*5.0625+.25*(-32.);self.assertLess(abs(3.75+interpolated),.75)
  ok=all_nonzero_bilinear_contributors_valid(np.array([[True,False]]),np.array([.25]),np.array([0.]));self.assertFalse(ok[0])
 def test_integer_sample_ignores_zero_weight_invalid_neighbor(self):
  ok=all_nonzero_bilinear_contributors_valid(np.array([[True,False]]),np.array([0.]),np.array([0.]));self.assertTrue(ok[0])
 def test_fractional_out_of_bounds_contributor_rejected(self):
  ok=all_nonzero_bilinear_contributors_valid(np.ones((2,2),bool),np.array([1.25]),np.array([0.]));self.assertFalse(ok[0])
 def test_exact_last_pixel_has_no_outside_contributors(self):
  ok=all_nonzero_bilinear_contributors_valid(np.ones((2,2),bool),np.array([1.]),np.array([1.]));self.assertTrue(ok[0])
 def test_nonfinite_remap_rejected(self):
  ok=all_nonzero_bilinear_contributors_valid(np.ones((2,2),bool),np.array([np.nan]),np.array([0.]));self.assertFalse(ok[0])
 def test_both_axes_nonzero_weight_contributors_required(self):
  mask=np.ones((2,2),bool);mask[1,1]=False
  ok=all_nonzero_bilinear_contributors_valid(mask,np.array([.25]),np.array([.25]));self.assertFalse(ok[0])
if __name__=='__main__':unittest.main(verbosity=2)
