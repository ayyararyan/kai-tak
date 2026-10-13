"""Measured sparse stereo, nominal camera / locally planar ground assumptions.
No manufactured roof labels, HKPD elevations, confidence limits or clearance claims.
"""
from pathlib import Path
import sys,json,csv,hashlib
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'python_deps'))
import cv2,numpy as np
from PIL import Image
from stereo_guardrails import validate_manual_labels,point_validity,fit_ground_plane,intersect_rays_with_plane,similarity_alignment,gated_height
labels=validate_manual_labels(HERE/'stereo_tracks.npz',HERE/'manual_stereo_labels.json',HERE.parents[1]/'chronology/aerial/fullframes')
raw=np.load(HERE/'stereo_tracks.npz');sel=raw['fmask'];p1=raw['p1'][sel];p2=raw['p2'][sel];F=raw['F']
rows=list(csv.DictReader((HERE/'control_points.csv').open()));q=np.array([[float(r['photo_x']),float(r['photo_y'])] for r in rows]);EN=np.array([[float(r['easting']),float(r['northing'])] for r in rows]);origin=EN.mean(0);Y=np.c_[EN-origin,np.zeros(len(rows))];fit=np.array([r['role']=='fit' for r in rows]);ground_fit=[r['fundamental_inlier_row'] for r in labels['labels'] if r['role']=='ground_fit'];ground_check=[r['fundamental_inlier_row'] for r in labels['labels'] if r['role']=='ground_holdout'];roof=[r['fundamental_inlier_row'] for r in labels['labels'] if r['role']=='roof_observed']

def solve(fmult=1.,cx=1460.,cy=1440.):
 f=152.12*300/25.4*fmult;K=np.array([[f,0,cx],[0,f,cy],[0,0,1.]])
 _,R,t,positive=cv2.recoverPose(K.T@F@K,p1,p2,K)
 P1=K@np.hstack([np.eye(3),np.zeros((3,1))]);P2=K@np.hstack([R,t]);T=cv2.triangulatePoints(P1,P2,p1.T,p2.T);X=(T[:3]/T[3]).T
 valid,re=point_validity(X,R,t,P1,P2,p1,p2)
 plane_center,normal=fit_ground_plane(X,ground_fit,valid)
 C=(-R.T@t).ravel();rays=(R.T@np.linalg.inv(K)@np.c_[q,np.ones(len(q))].T).T
 G=intersect_rays_with_plane(C,rays,plane_center,normal)
 scale,A,b=similarity_alignment(G[fit],Y[fit]);world=scale*X@A+b+np.r_[origin,0]
 gcworld=scale*G@A+b+np.r_[origin,0];gcerr=gcworld-np.c_[EN,np.zeros(len(rows))]
 return dict(K=K,R=R,t=t,P1=P1,P2=P2,X=X,world=world,scale=scale,A=A,b=b,plane_center=plane_center,plane_normal=normal,gcerr=gcerr,reprojection=re,valid=valid,positive=(X[:,2]>0)&((R@X.T+t).T[:,2]>0),gcworld=gcworld,camera1_world=scale*np.zeros(3)@A+b+np.r_[origin,0],camera2_world=scale*C@A+b+np.r_[origin,0])
s=solve();world=s['world'];good=s['valid']&np.isfinite(world).all(1)
# Original GCP reference bounds indicate local support only, not a guarantee for all points therein.
reg=json.loads((HERE/'registration.json').read_text());hull=np.array(reg['support_polygon_hk1980']['coordinates'][0][:-1]);local=np.array([cv2.pointPolygonTest(hull.astype(np.float32),(float(x),float(y)),False)>=0 for x,y in world[:,:2]])
# Standard GeoJSON supplies horizontal EPSG4326 only; height is a separate relative-plane field.
from pyproj import Transformer
tr=Transformer.from_crs(2326,4326,always_xy=True)
photo=np.array(Image.open(HERE.parents[1]/'chronology/aerial/fullframes/A36143.jpg').convert('RGB'))
fields=['track_id','frame42_x','frame42_y','frame43_x','frame43_y','easting_hk1980_m','northing_hk1980_m','z_above_fitted_local_park_road_plane_m','reprojection_rms_px','positive_depth_both_views','passes_diagnostic_5px_filter','within_map_control_hull','surface_class','manual_surface_note','r','g','b']
notes={r['fundamental_inlier_row']:(r['role'],r['observed_surface']) for r in labels['labels']}
records=[]
for i in range(len(world)):
 x,y=np.round(p2[i]).astype(int);rgb=photo[np.clip(y,0,2999),np.clip(x,0,2999)].tolist();kind,note=notes.get(i,('unclassified','no automatic building/ground assignment'))
 records.append(dict(zip(fields,[i,*p1[i],*p2[i],*world[i],s['reprojection'][i],bool(s['positive'][i]),bool(good[i]),bool(local[i]),kind,note,*rgb])))
with (HERE/'sparse_stereo_points.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
with (HERE/'sparse_stereo_points.ply').open('w') as f:
 f.write('ply\nformat ascii 1.0\ncomment x y are EPSG2326 metres; z relative fitted local park-road plane NOT HKPD\ncomment nominal camera calibration; unclassified sparse tiepoints NOT solid buildings\n'+f'element vertex {int(good.sum())}\nproperty double x\nproperty double y\nproperty double z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nproperty int track_id\nproperty float reprojection_px\nend_header\n')
 for r in records:
  if r['passes_diagnostic_5px_filter']:f.write(' '.join(str(r[k]) for k in ['easting_hk1980_m','northing_hk1980_m','z_above_fitted_local_park_road_plane_m','r','g','b','track_id','reprojection_rms_px'])+'\n')
# Finite perturbation experiment only. These offsets are declared sensitivity choices, NOT uncertainty bounds.
variants=[]
for fm,cx,cy in [(1.,1460.,1440.),(.95,1460.,1440.),(1.05,1460.,1440.),(1.,1440.,1440.),(1.,1480.,1440.),(1.,1460.,1420.),(1.,1460.,1460.)]:
 v=solve(fm,cx,cy);variants.append({'focal_multiplier':fm,'principal_x':cx,'principal_y':cy,'metric_baseline_m':v['scale'],'roof_point_26_height_m':gated_height(v['world'],v['valid'],26),'roof_point_1135_height_m':gated_height(v['world'],v['valid'],1135),'heldout_ground708_z_m':gated_height(v['world'],v['valid'],708),'named_point_validity':{str(i):bool(v['valid'][i]) for i in roof+ground_check},'map_holdout_horizontal_rmse_m':float(np.sqrt(np.mean(np.sum(v['gcerr'][~fit,:2]**2,axis=1))))})
sourcefiles=[HERE.parents[1]/'chronology/aerial/fullframes/A36142.jpg',HERE.parents[1]/'chronology/aerial/fullframes/A36143.jpg',HERE.parents[1]/'chronology/sheets/maps/1980_1990_678_11-NE-11A_1989-10-01.zip']
report={'generated_utc':datetime.now(timezone.utc).isoformat(),'status':'measured_sparse_stereo_reconstruction_conditional_nominal_calibration','actual_same_epoch_content_overlap_verified':True,'source_date':'1993-11-02','source_frames':['A36142','A36143'],'same_camera_label':'WILD15/UAGIA Nr6098 152.12','crs_horizontal':'EPSG:2326 via original 1989 survey worldfile and 6 map road GCPs','vertical_reference':'relative to four observed park/paved-path stereo points fitted as common local plane; NOT HKPD or absolute elevation','assumptions':['nominal152.12mm focal number interpreted as focal length;300dpi taken as metric film scan scale','shared principal point approximated from corner fiducial layout at1460,1440 original pixels','no calibrated lens distortion or scan deformation correction','four selected park/path ground correspondences approximated by one locally planar reference; source ground elevations not equated to sea level','map road junctions unchanged between1989 and1993; six fitted and four held-out ground coordinates','all triangulated points remain unclassified except explicitly inspected surface IDs; vegetation/terrain/roof outliers not silently buildings'],'counts':{'ratio_matches':int(len(raw['p1'])),'fundamental_inliers':len(world),'positive_depth':int(s['positive'].sum()),'exported_ply_reprojection_under5px':int(good.sum()),'exported_points_within_map_control_hull':int((good&local).sum()),'map_control_fit':int(fit.sum()),'map_control_holdout':int((~fit).sum()),'stereo_ground_plane_fit':len(ground_fit),'stereo_ground_plane_holdout':len(ground_check),'observed_roof_points':len(roof)},'nominal_K':s['K'].tolist(),'nominal_relative_R':s['R'].tolist(),'nominal_relative_t_unit':s['t'].ravel().tolist(),'metric_baseline_m_from_map_scale':s['scale'],'index_center_baseline_m_comparison_only':float(np.hypot(838068-837543,820693-820672)),'ground_plane_fit_track_ids':ground_fit,'ground_plane_holdout_track_ids':ground_check,'ground_plane_fit_z_residuals_m':world[ground_fit,2].tolist(),'ground_plane_holdout_z_residuals_m':[gated_height(world,s['valid'],i) for i in ground_check],'map_fit_horizontal_rmse_m':float(np.sqrt(np.mean(np.sum(s['gcerr'][fit,:2]**2,axis=1)))),'map_holdout_horizontal_rmse_m':float(np.sqrt(np.mean(np.sum(s['gcerr'][~fit,:2]**2,axis=1)))),'map_holdout_horizontal_max_m':float(np.linalg.norm(s['gcerr'][~fit,:2],axis=1).max()),'map_control_residuals_ENZ_m':s['gcerr'].tolist(),'reprojection_rms_px_quantiles':np.percentile(s['reprojection'],[0,25,50,75,95,100]).tolist(),'camera1_relative_plane_height_m':s['camera1_world'][2],'camera2_relative_plane_height_m':s['camera2_world'][2],'roof_point_estimates':[{'track_id':i,'observed_object':notes[i][1],'height_above_reference_plane_m':gated_height(world,s['valid'],i),'status':'accepted_conditional' if bool(s['valid'][i]) else 'rejected_null_height','reprojection_rms_px':s['reprojection'][i],'ground_base_elevation_at_building_identified':False,'statistical_or_hard_error_bounds':None} for i in roof],'nominal_intrinsic_sensitivity_experiment':variants,'sensitivity_is_calibrated_uncertainty':False,'height_acceptance':'exploratory visualization point heights only; full building heights/roof meshes need more observations; one ground holdout is not vertical accuracy validation','source_sha256':{str(p.relative_to(HERE.parents[1])):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcefiles}}
report['manual_labels_sha256']=hashlib.sha256((HERE/'manual_stereo_labels.json').read_bytes()).hexdigest()
report['tracks_sha256']=labels['stereo_tracks_npz_sha256']
report['accepted_ground_checks']={str(i):bool(s['valid'][i]) for i in ground_fit+ground_check}
(HERE/'sparse_stereo_report.json').write_text(json.dumps(report,indent=2)+'\n')
np.savez(HERE/'sparse_stereo_transform.npz',**{k:v for k,v in s.items() if isinstance(v,np.ndarray)},scale=s['scale'],origin_EN=origin)
report['transform_sha256']=hashlib.sha256((HERE/'sparse_stereo_transform.npz').read_bytes()).hexdigest()
(HERE/'sparse_stereo_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
