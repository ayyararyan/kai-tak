from pathlib import Path
import sys,json,csv
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'python_deps'))
import cv2,numpy as np
ROOT=HERE.parents[1];src=ROOT/'chronology/aerial/fullframes'
a=cv2.imread(str(src/'A36142.jpg'),0);b=cv2.imread(str(src/'A36143.jpg'),0)
sift=cv2.SIFT_create(nfeatures=25000)
mask=np.zeros(a.shape,np.uint8);mask[120:2800,120:2800]=255
ka,da=sift.detectAndCompute(a,mask);kb,db=sift.detectAndCompute(b,mask)
matches=cv2.BFMatcher().knnMatch(da,db,k=2);good=[m for m,n in matches if m.distance<.7*n.distance]
p1=np.float64([ka[m.queryIdx].pt for m in good]);p2=np.float64([kb[m.trainIdx].pt for m in good])
F,fmask=cv2.findFundamentalMat(p1,p2,cv2.USAC_MAGSAC,1.0,.999,10000)
sel=fmask.ravel()>0;np.savez(HERE/'stereo_tracks.npz',p1=p1,p2=p2,fmask=sel,F=F)
f=152.12*300/25.4;K=np.array([[f,0,1460.],[0,f,1440.],[0,0,1.]])
E=K.T@F@K
n,R,t,posemask=cv2.recoverPose(E,p1[sel],p2[sel],K)
P1=K@np.hstack([np.eye(3),np.zeros((3,1))]);P2=K@np.hstack([R,t]);X=cv2.triangulatePoints(P1,P2,p1[sel].T,p2[sel].T);X=(X[:3]/X[3]).T
np.savez(HERE/'stereo_nominal_camera.npz',K=K,R=R,t=t,P1=P1,P2=P2,X=X,p1=p1[sel],p2=p2[sel])
# Homography is only a search seed, not final pair correspondence/ground registration.
H,hmask=cv2.findHomography(p2[sel],p1[sel],cv2.USAC_MAGSAC,3.)
rows=list(csv.DictReader((HERE/'control_points.csv').open()))
# Patch normalized cross correlation around ground-control coordinates.
# Search seed: nearest SIFT track displacement; retain score/second peak separation and visualize.
controls=[]
for r in rows:
 q=np.array([float(r['photo_x']),float(r['photo_y'])]);near=np.argsort(np.linalg.norm(p2[sel]-q,axis=1))[:20]
 pred=q+np.median((p1[sel]-p2[sel])[near],axis=0)
 half=12;radius=35
 qx,qy=np.round(q).astype(int);px,py=np.round(pred).astype(int)
 patch=b[qy-half:qy+half+1,qx-half:qx+half+1]
 region=a[py-radius-half:py+radius+half+1,px-radius-half:px+radius+half+1]
 corr=cv2.matchTemplate(region,patch,cv2.TM_CCOEFF_NORMED);_,score,_,loc=cv2.minMaxLoc(corr)
 match=np.array([px-radius+loc[0],py-radius+loc[1]],float)
 # LK subpixel refinement initialized to actual NCC result.
 dest,status,err=cv2.calcOpticalFlowPyrLK(b,a,q.astype(np.float32).reshape(1,1,2),match.astype(np.float32).reshape(1,1,2),winSize=(25,25),maxLevel=2,flags=cv2.OPTFLOW_USE_INITIAL_FLOW)
 if status[0,0]:match=dest[0,0].astype(float)
 v=cv2.triangulatePoints(P1,P2,match.reshape(2,1),q.reshape(2,1));v=(v[:3]/v[3]).ravel()
 reproj1=P1@np.r_[v,1];reproj1=reproj1[:2]/reproj1[2];reproj2=P2@np.r_[v,1];reproj2=reproj2[:2]/reproj2[2]
 controls.append({**r,'frame42_x':float(match[0]),'frame42_y':float(match[1]),'ncc':score,'triangulated_xyz_baseline_units':v.tolist(),'stereo_reprojection_error_px':float(np.sqrt((np.sum((reproj1-match)**2)+np.sum((reproj2-q)**2))/2))})
(HERE/'stereo_ground_controls.json').write_text(json.dumps(controls,indent=2)+'\n')
report={'keypoints42':len(ka),'keypoints43':len(kb),'ratio_matches':len(good),'fundamental_inliers':int(sel.sum()),'cheirality_positive':n,'K_nominal':K.tolist(),'R':R.tolist(),'t_unit':t.ravel().tolist(),'controls_ncc':[c['ncc'] for c in controls],'controls_stereo_reprojection_error_px':[c['stereo_reprojection_error_px'] for c in controls]}
(HERE/'stereo_probe.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
# Actual matched feature overview
vis=cv2.drawMatches(a,ka,b,kb,[good[i] for i in np.flatnonzero(sel)[::max(1,int(sel.sum())//80)]],None,flags=2);vis=cv2.resize(vis,(1800,900));cv2.imwrite(str(HERE/'stereo_actual_matches.jpg'),vis)
# Patches of manually selected controls with tracked pair marked.
from PIL import Image,ImageDraw
canvas=Image.new('RGB',(1200,600),'white')
for i,c in enumerate(controls):
 for j,(im,x,y) in enumerate([(a,c['frame42_x'],c['frame42_y']),(b,float(c['photo_x']),float(c['photo_y']))]):
  x,y=int(round(x)),int(round(y));patch=Image.fromarray(im[y-35:y+35,x-35:x+35]).convert('RGB').resize((110,110));d=ImageDraw.Draw(patch);d.line((50,55,60,55),fill='red');d.line((55,50,55,60),fill='red');d.text((2,2),f'{i+1}:{42+j}',fill='yellow');canvas.paste(patch,((i%5)*240+j*120,(i//5)*150))
canvas.crop((0,0,1200,300)).save(HERE/'stereo_ground_control_patches.jpg')
