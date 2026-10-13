"""Dense actual-image correspondences, conservative masks; unclassified points."""
from pathlib import Path
import sys,json,time,csv,hashlib
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'python_deps'))
import cv2,numpy as np
from PIL import Image
from stereo_guardrails import validate_manual_labels,point_validity,fit_ground_plane,gated_height,all_nonzero_bilinear_contributors_valid
labels=validate_manual_labels(HERE/'stereo_tracks.npz',HERE/'manual_stereo_labels.json',HERE.parents[1]/'chronology/aerial/fullframes')
sparse_report=json.loads((HERE/'sparse_stereo_report.json').read_text())
if hashlib.sha256((HERE/'sparse_stereo_transform.npz').read_bytes()).hexdigest()!=sparse_report['transform_sha256']:raise ValueError('Sparse transform hash mismatch')
if hashlib.sha256((HERE/'manual_stereo_labels.json').read_bytes()).hexdigest()!=sparse_report['manual_labels_sha256']:raise ValueError('Manual labels differ from accepted sparse solution')
started=time.time();src=HERE.parents[1]/'chronology/aerial/fullframes';a=cv2.imread(str(src/'A36142.jpg'),0);b=cv2.imread(str(src/'A36143.jpg'),0)
s=np.load(HERE/'sparse_stereo_transform.npz');tracks=np.load(HERE/'stereo_tracks.npz');sel=tracks['fmask'];p1=tracks['p1'][sel];p2=tracks['p2'][sel]
ground_ids=[r['fundamental_inlier_row'] for r in labels['labels'] if r['role']=='ground_fit']
accepted,_=point_validity(s['X'],s['R'],s['t'],s['P1'],s['P2'],p1,p2)
fit_ground_plane(s['X'],ground_ids,accepted)
ok,H1,H2=cv2.stereoRectifyUncalibrated(p1,p2,tracks['F'],(3000,3000),threshold=2)
if not ok:raise RuntimeError('Actual fundamental rectification failed')
N=2000;S=np.diag([N/3000,N/3000,1.]);H1=S@H1;H2=S@H2
r1=cv2.warpPerspective(a,H1,(N,N));r2=cv2.warpPerspective(b,H2,(N,N));m=np.zeros(a.shape,np.uint8);m[140:2780,140:2800]=255;m1=cv2.warpPerspective(m,H1,(N,N));m2=cv2.warpPerspective(m,H2,(N,N))
def project(H,p):
 q=(H@np.c_[p,np.ones(len(p))].T).T;return q[:,:2]/q[:,2,None]
rp1=project(H1,p1);rp2=project(H2,p2);ds=rp1[:,0]-rp2[:,0];v_err=rp1[:,1]-rp2[:,1]
mind=int(np.floor(np.percentile(ds,0)/16)*16)-16;maxd=int(np.ceil(np.percentile(ds,100)/16)*16)+16;num=int(np.ceil((maxd-mind)/16)*16)
print('Rectified sparse disparity range',np.percentile(ds,[0,1,50,99,100]).tolist(),'verticalRMSE',np.sqrt(np.mean(v_err**2)),'SGBM',mind,num,flush=True)
# Actual-image rectification illustration.
cv2.imwrite(str(HERE/'dense_rectified_pair.jpg'),cv2.resize(np.hstack([r1,r2]),(1600,800)))
params=dict(numDisparities=num,blockSize=5,P1=8*25,P2=32*25,disp12MaxDiff=1,preFilterCap=31,uniquenessRatio=12,speckleWindowSize=100,speckleRange=2,mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
left=cv2.StereoSGBM_create(minDisparity=mind,**params);right=cv2.StereoSGBM_create(minDisparity=-mind-num+1,**params)
d1=left.compute(r1,r2).astype(np.float32)/16;d2=right.compute(r2,r1).astype(np.float32)/16
print('SGBM done',time.time()-started,flush=True)
y,x=np.indices((N,N));xr=x-d1;yr=y.astype(np.float32);sampled=cv2.remap(d2,xr.astype(np.float32),yr,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=-1e4);valid2=cv2.remap(m2,xr.astype(np.float32),yr,cv2.INTER_NEAREST)>250
lr=np.abs(d1+sampled);mean=cv2.boxFilter(r1.astype(np.float32),-1,(7,7));var=cv2.boxFilter(r1.astype(np.float32)**2,-1,(7,7))-mean**2
right_source_valid=np.isfinite(d2)&(d2>(-mind-num+1)-.1)
right_disparity_support=all_nonzero_bilinear_contributors_valid(right_source_valid,xr,yr)
right_all_support=all_nonzero_bilinear_contributors_valid(right_source_valid&(m2>250),xr,yr)
valid=(m1>250)&valid2&(d1>mind-.1)&right_all_support&(lr<=.75)&(var>=36)
# Pixel-level QC bit mask, no scene meaning inferred from failure.
qc=np.zeros((N,N),np.uint8);qc|=(m1>250).astype('uint8');qc|=valid2.astype('uint8')*2;qc|=(d1>mind-.1).astype('uint8')*4;qc|=(lr<=.75).astype('uint8')*8;qc|=(var>=36).astype('uint8')*16;qc|=right_all_support.astype('uint8')*32
np.savez_compressed(HERE/'dense_pixel_qc.npz',disparity=d1,left_right_error=lr,texture_variance=var,qc_bits=qc,valid_correspondence=valid,right_disparity_support_valid=right_disparity_support,right_all_support_valid=right_all_support,H1=H1,H2=H2)
# Every third rectified pixel each axis caps output without altering accepted correspondence mask.
export_mask=valid&(x%3==0)&(y%3==0);iy,ix=np.where(export_mask);L=np.c_[ix,iy].astype(float);R=np.c_[ix-d1[iy,ix],iy].astype(float);op1=project(np.linalg.inv(H1),L);op2=project(np.linalg.inv(H2),R)
T=cv2.triangulatePoints(s['P1'],s['P2'],op1.T,op2.T);X=(T[:3]/T[3]).T;w=float(s['scale'])*X@s['A']+s['b']+np.r_[s['origin_EN'],0]
uv1=project(s['P1'],X) if False else None
rr=[]
for P,obs in [(s['P1'],op1),(s['P2'],op2)]:
 z=(P@np.c_[X,np.ones(len(X))].T).T;rr.append(np.sum((z[:,:2]/z[:,2,None]-obs)**2,axis=1))
re=np.sqrt((rr[0]+rr[1])/2);depth2=(s['R']@X.T+s['t']).T[:,2]
keep=np.isfinite(w).all(1)&(X[:,2]>0)&(depth2>0)&(re<=5)
# No height clipping: below-plane points could be ground/terrain or errors, not silently deleted.
photo=np.array(Image.open(src/'A36143.jpg').convert('RGB'));p=np.rint(op2).astype(int);rgb=photo[np.clip(p[:,1],0,2999),np.clip(p[:,0],0,2999)]
reg=json.loads((HERE/'registration.json').read_text());hull=np.array(reg['support_polygon_hk1980']['coordinates'][0][:-1],np.float32);inside=np.array([cv2.pointPolygonTest(hull,(float(e),float(n)),False)>=0 for e,n in w[:,:2]])
fields=['dense_id','rectified42_x','rectified42_y','frame42_x','frame42_y','frame43_x','frame43_y','easting_hk1980_m','northing_hk1980_m','z_above_fitted_local_park_road_plane_m','reprojection_rms_px','left_right_error_rectified_px','texture_variance','within_map_control_hull','r','g','b']
with (HERE/'dense_stereo_points.csv').open('w') as f:
 wr=csv.writer(f);wr.writerow(fields)
 for i in np.flatnonzero(keep):wr.writerow([i,int(ix[i]),int(iy[i]),*op1[i],*op2[i],*w[i],re[i],lr[iy[i],ix[i]],var[iy[i],ix[i]],bool(inside[i]),*rgb[i]])
with (HERE/'dense_stereo_points.ply').open('w') as f:
 f.write('ply\nformat ascii 1.0\ncomment nominal-calibration dense image correspondence; unclassified surfaces; no certified bounds\ncomment x y EPSG2326; z relative park-road plane NOT HKPD\n'+f'element vertex {int(keep.sum())}\nproperty double x\nproperty double y\nproperty double z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nproperty int point_id\nproperty float reprojection_px\nend_header\n')
 for i in np.flatnonzero(keep):f.write(' '.join(map(str,[*w[i],*rgb[i],i,re[i]]))+'\n')
# Held-out sparse image correspondences are not SGBM supervision. Compare nearby source-pixel points.
checks=[]
for tid in [708,26,1135]:
 if not bool(accepted[tid]):
  checks.append({'sparse_track_id':tid,'status':'rejected_reference_point','sparse_z_m':None,'dense_z_m_quantiles':None});continue
 dist=np.linalg.norm(op2-p2[tid],axis=1);near=keep&(dist<=8)
 checks.append({'sparse_track_id':tid,'dense_source43_radius_px':8,'dense_count':int(near.sum()),'sparse_z_m':float(s['world'][tid,2]),'dense_z_m_quantiles':np.percentile(w[near,2],[10,50,90]).tolist() if near.any() else None,'median_dense_minus_sparse_z_m':float(np.median(w[near,2])-s['world'][tid,2]) if near.any() else None,'caveat':'same image pair/calibration; local neighborhood may contain distinct edges/levels, not independent height truth'})
report={'status':'dense_conditional_image_based_pointcloud_not_mesh','runtime_s':time.time()-started,'source_frames':['A36142','A36143'],'source_epoch':'1993-11-02','same_reference_as':'sparse_stereo_report.json','output_resolution_rectified_px':N,'rectification':'uncalibrated fundamental-matrix homographies from measured sparse matches; triangulation in original nominal cameras','rectified_sparse_vertical_rmse_px':float(np.sqrt(np.mean(v_err**2))),'min_disparity':mind,'num_disparities':num,'counts':{'rectified_pixels':N*N,'valid_image_overlap':int(((m1>250)&valid2).sum()),'lr_texture_valid_correspondences':int(valid.sum()),'subsampled_for_triangulation':len(X),'positive_finite_reprojection_accepted':int(keep.sum()),'exported_within_map_control_hull':int((keep&inside).sum())},'filters':{'left_right_max_rectified_px':.75,'local_7x7_grayscale_variance_min':36,'original_camera_reprojection_rms_max_px':5,'export_subsample_stride_each_axis':3,'automatic_surface_labels':False,'height_clipping':False},'dense_vs_sparse_surface_checks':checks,'pointcloud_scope':'unclassified observed image surfaces incl.roofs,ground,trees and possible correspondence errors; no solid buildings or all-obstacle completeness','crs_horizontal':'EPSG:2326 diagnostic via local control transform','vertical_reference':'relative fitted park-road plane, no HKPD datum','source_calibration_report':'sparse_stereo_report.json','qc_bits':{'1':'inside usable frame42','2':'matched coordinate inside usable frame43','4':'left disparity valid','8':'left-right consistency<=.75px','16':'local texture variance>=36','32':'every nonzero-weight right interpolation contributor in bounds, valid disparity, usable source image'},'rejected_pixels_are':'failed_correspondence_or_unknown_not_absence','requires_more_work':['independent height calibration','ground/roof interpretation','occlusion/mismatch correction','additional views','dense parameter and rectification sensitivity']}
old_path=HERE/'invalidated_dense_lr_blend/dense_pixel_qc.npz'
if old_path.exists():
 old=np.load(old_path)['valid_correspondence'];old_sub=old&(x%3==0)&(y%3==0);report['sentinel_interpolation_repair']={'previous_accepted_pixels_with_invalid_disparity_support':int((old&~right_disparity_support).sum()),'previous_export_samples_with_invalid_disparity_support':int((old_sub&~right_disparity_support).sum()),'previous_accepted_pixels_with_invalid_any_right_support':int((old&~right_all_support).sum()),'old_outputs_preserved':'invalidated_dense_lr_blend/','sparse_unchanged':True}
report['accepted_sparse_transform_sha256']=sparse_report['transform_sha256']
report['accepted_manual_labels_sha256']=sparse_report['manual_labels_sha256']
report['source_sha256']=sparse_report['source_sha256']
(HERE/'dense_stereo_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
