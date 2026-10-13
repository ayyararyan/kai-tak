"""Acceptance gates for manually labelled stereo evidence and conditional geometry."""
from pathlib import Path
import hashlib,json
import numpy as np

def validate_manual_labels(track_path,label_path,source_dir):
 track_path=Path(track_path);book=json.loads(Path(label_path).read_text())
 if hashlib.sha256(track_path.read_bytes()).hexdigest()!=book['stereo_tracks_npz_sha256']:
  raise ValueError('Manual stereo labels invalidated: stereo_tracks.npz hash changed; re-inspect correspondences, do not relabel by row index.')
 for frame,h in book['frame_sha256'].items():
  if hashlib.sha256((Path(source_dir)/(frame+'.jpg')).read_bytes()).hexdigest()!=h:raise ValueError('Manual stereo labels invalidated: source frame changed')
 raw=np.load(track_path);sel=raw['fmask'];p1=raw['p1'][sel];p2=raw['p2'][sel]
 seen=set()
 for r in book['labels']:
  i=r['fundamental_inlier_row']
  if i in seen or i<0 or i>=len(p1):raise ValueError('Invalid or duplicate pinned stereo correspondence ID')
  seen.add(i)
  if not np.array_equal(p1[i],np.array(r['frame42_xy'])) or not np.array_equal(p2[i],np.array(r['frame43_xy'])):raise ValueError('Pinned manual stereo coordinates disagree')
 return book

def point_validity(X,R,t,P1,P2,p1,p2,max_reprojection=5.):
 X=np.asarray(X);z2=(R@X.T+t).T[:,2]
 finite=np.isfinite(X).all(1);err=[]
 with np.errstate(divide='ignore',invalid='ignore'):
  for P,obs in [(P1,p1),(P2,p2)]:
   z=(P@np.c_[X,np.ones(len(X))].T).T;pred=z[:,:2]/z[:,2,None];err.append(np.sum((pred-obs)**2,axis=1))
  re=np.sqrt((err[0]+err[1])/2)
 valid=finite&np.isfinite(re)&(X[:,2]>0)&(z2>0)&(re<=max_reprojection)
 return valid,re

def fit_ground_plane(X,ids,valid):
 if len(set(ids))<3 or not np.asarray(valid)[ids].all():raise ValueError('Ground-plane controls fail finite/positive-depth/reprojection gate')
 pts=np.asarray(X)[ids]
 if not np.isfinite(pts).all():raise ValueError('Ground-plane controls nonfinite')
 c=pts.mean(0);_,s,v=np.linalg.svd(pts-c)
 if len(s)<2 or s[0]<=1e-12 or s[1]<=1e-5*s[0]:raise ValueError('Ground-plane controls collinear or rank deficient')
 return c,v[-1]

def intersect_rays_with_plane(C,rays,center,normal):
 rays=np.asarray(rays);den=rays@normal
 if not np.isfinite(rays).all() or not np.isfinite(den).all() or np.any(np.abs(den)<=1e-8*np.linalg.norm(rays,axis=1)):
  raise ValueError('Camera ray parallel to or invalid for reference plane')
 lam=((center-C)@normal)/den
 if not np.isfinite(lam).all() or np.any(lam<=0):raise ValueError('Reference plane intersection behind camera or nonfinite')
 return C+lam[:,None]*rays

def similarity_alignment(X,Y):
 X=np.asarray(X);Y=np.asarray(Y)
 if X.shape!=Y.shape or X.ndim!=2 or X.shape[1]!=3 or len(X)<3 or not np.isfinite(X).all() or not np.isfinite(Y).all():raise ValueError('Invalid similarity controls')
 mx=X.mean(0);my=Y.mean(0);xc=X-mx;yc=Y-my
 for a in [xc,yc]:
  sv=np.linalg.svd(a,compute_uv=False)
  if sv[0]<=1e-12 or sv[1]<=1e-5*sv[0]:raise ValueError('Similarity controls collinear or rank deficient')
 U,S,V=np.linalg.svd(xc.T@yc);D=np.eye(3);D[-1,-1]=np.linalg.det(U@V);A=U@D@V;scale=np.trace(np.diag(S)@D)/np.sum(xc**2);b=my-scale*mx@A
 if not np.isfinite(scale) or scale<=0 or not np.isfinite(A).all() or not np.isfinite(b).all():raise ValueError('Nonpositive or invalid metric scale')
 return scale,A,b

def gated_height(world,valid,index):
 return float(world[index,2]) if bool(valid[index]) and np.isfinite(world[index]).all() else None

def all_nonzero_bilinear_contributors_valid(source_valid,x,y):
 """Reject an interpolated sample if any positive-weight source is invalid/outside.

 Integer-coordinate zero-weight neighbors need not exist/be valid. This gate must
 run on the original validity mask, never on already interpolated disparities.
 """
 source_valid=np.asarray(source_valid,dtype=bool);x=np.asarray(x);y=np.asarray(y)
 if x.shape!=y.shape:raise ValueError('Remap coordinate shapes differ')
 finite=np.isfinite(x)&np.isfinite(y);safe_x=np.where(finite,x,0.);safe_y=np.where(finite,y,0.);x0=np.floor(safe_x).astype(np.int64);y0=np.floor(safe_y).astype(np.int64);fx=safe_x-x0;fy=safe_y-y0;h,w=source_valid.shape;ok=finite.copy()
 for dx,dy,weight in [(0,0,(1-fx)*(1-fy)),(1,0,fx*(1-fy)),(0,1,(1-fx)*fy),(1,1,fx*fy)]:
  xx=x0+dx;yy=y0+dy;inside=(xx>=0)&(xx<w)&(yy>=0)&(yy<h)
  supported=inside&source_valid[np.clip(yy,0,h-1),np.clip(xx,0,w-1)]
  ok&=(weight==0)|supported
 return ok
