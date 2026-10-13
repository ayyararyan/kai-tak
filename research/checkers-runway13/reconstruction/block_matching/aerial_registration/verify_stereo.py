from pathlib import Path
import json,csv,hashlib,sys,unittest
from datetime import datetime,timezone
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'python_deps'))
import cv2
from stereo_guardrails import validate_manual_labels,point_validity,fit_ground_plane
labels=validate_manual_labels(HERE/'stereo_tracks.npz',HERE/'manual_stereo_labels.json',HERE.parents[1]/'chronology/aerial/fullframes')
s=json.loads((HERE/'sparse_stereo_report.json').read_text());d=json.loads((HERE/'dense_stereo_report.json').read_text());before=json.loads((HERE/'pre_guard_repair_evidence.json').read_text());checks={};detail={}
checks['source_hashes_match']=all(hashlib.sha256((HERE.parents[1]/p).read_bytes()).hexdigest()==h for p,h in s['source_sha256'].items())
checks['pinned_labels_validate']=True
checks['sparse_transform_hash_match']=hashlib.sha256((HERE/'sparse_stereo_transform.npz').read_bytes()).hexdigest()==s['transform_sha256']
checks['dense_inherits_accepted_transform']=d['accepted_sparse_transform_sha256']==s['transform_sha256']
checks['dense_inherits_pinned_labels']=d['accepted_manual_labels_sha256']==s['manual_labels_sha256']
z=np.load(HERE/'sparse_stereo_transform.npz');raw=np.load(HERE/'stereo_tracks.npz');sel=raw['fmask'];p1=raw['p1'][sel];p2=raw['p2'][sel]
valid,rep=point_validity(z['X'],z['R'],z['t'],z['P1'],z['P2'],p1,p2);gids=[r['fundamental_inlier_row'] for r in labels['labels'] if r['role']=='ground_fit'];fit_ground_plane(z['X'],gids,valid)
checks['all_ground_fit_points_pass_gates']=bool(valid[gids].all());checks['all_named_roof_heights_are_gated']=all(r['status']=='accepted_conditional' and bool(valid[r['track_id']]) for r in s['roof_point_estimates'])
checks['relative_vertical_no_hkpd_claim']='NOT HKPD' in s['vertical_reference'] and 'no HKPD' in d['vertical_reference']
checks['height_uncertainty_not_fabricated']=not s['sensitivity_is_calibrated_uncertainty'] and all(r['statistical_or_hard_error_bounds'] is None for r in s['roof_point_estimates'])
for prefix,expected in [('sparse',s['counts']['exported_ply_reprojection_under5px']),('dense',d['counts']['positive_finite_reprojection_accepted'])]:
 rows=list(csv.DictReader((HERE/f'{prefix}_stereo_points.csv').open()));lines=(HERE/f'{prefix}_stereo_points.ply').read_text().splitlines();header_end=lines.index('end_header');declared=int(next(x for x in lines[:header_end] if x.startswith('element vertex')).split()[-1]);checks[f'{prefix}_csv_ply_count_match']=len(rows)==len(lines)-header_end-1==declared==expected
 aa=np.array([[float(r['easting_hk1980_m']),float(r['northing_hk1980_m']),float(r['z_above_fitted_local_park_road_plane_m'])] for r in rows]);checks[f'{prefix}_finite_positions']=bool(np.isfinite(aa).all());checks[f'{prefix}_reprojection_filter']=all(float(r['reprojection_rms_px'])<=5 for r in rows)
 ii=np.linspace(0,len(rows)-1,min(1000,len(rows))).astype(int);rr=[rows[i] for i in ii];u=np.array([[float(r['frame42_x']),float(r['frame42_y'])] for r in rr]);v=np.array([[float(r['frame43_x']),float(r['frame43_y'])] for r in rr]);T=cv2.triangulatePoints(z['P1'],z['P2'],u.T,v.T);X=(T[:3]/T[3]).T;world=float(z['scale'])*X@z['A']+z['b']+np.r_[z['origin_EN'],0];err=float(np.max(np.abs(world-aa[ii])));checks[f'{prefix}_1000_point_retriangulation_matches']=err<1e-7;detail[f'{prefix}_retriangulation_max_abs_error_m']=err
 if prefix=='dense':
  checks['dense_lr_filter']=all(float(r['left_right_error_rectified_px'])<=.75 for r in rows);checks['dense_texture_filter']=all(float(r['texture_variance'])>=36 for r in rows)
qc=np.load(HERE/'dense_pixel_qc.npz');checks['dense_qc_mask_count']=int(qc['valid_correspondence'].sum())==d['counts']['lr_texture_valid_correspondences'];checks['dense_qc_bits_reproduce_acceptance']=np.array_equal(qc['qc_bits']==63,qc['valid_correspondence']);checks['all_accepted_right_support_valid']=bool(qc['right_all_support_valid'][qc['valid_correspondence']].all());checks['all_accepted_right_disparity_contributors_valid']=bool(qc['right_disparity_support_valid'][qc['valid_correspondence']].all())
changes={}
for prefix in ['sparse','dense']:
 h=hashlib.sha256((HERE/f'{prefix}_stereo_points.ply').read_bytes()).hexdigest();changes[f'{prefix}_ply_identical_to_pre_guard_repair']=h==before[f'{prefix}_ply_sha256']
changes['roof_heights_unchanged']=all(a['height_above_reference_plane_m']==b['height_above_reference_plane_m'] for a,b in zip(s['roof_point_estimates'],before['roof_point_estimates']))
changes['metric_baseline_unchanged']=s['metric_baseline_m_from_map_scale']==before['metric_baseline_m'];changes['map_holdout_rmse_unchanged']=s['map_holdout_horizontal_rmse_m']==before['holdout_rmse_m']
# Scope-bound acceptance evidence, not an assertion that the full city is reconstructed.
import test_stereo_guardrails
suite=unittest.defaultTestLoader.loadTestsFromModule(test_stereo_guardrails)
with (HERE/'guardrail_test_run.log').open('w') as f:result=unittest.TextTestRunner(stream=f,verbosity=2).run(suite)
checks['guardrail_tests_pass']=result.wasSuccessful()
report={'verified_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'all_passed':all(checks.values()),'guardrail_tests_run':result.testsRun,'numeric_detail':detail,'review_repair_geometry_changes':changes,'dense_change_reason':'49 exported samples removed:6 invalid-sentinel blends plus43 other invalid right-image interpolation supports; earlier outputs preserved under invalidated_dense_lr_blend/','full_historical_scene_complete':False,'independent_height_accuracy_calibrated':False}
(HERE/'stereo_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
(HERE/'requirements_stereo.txt').write_text(f'opencv-python-headless=={__import__("importlib.metadata",fromlist=["version"]).version("opencv-python-headless")}\nnumpy=={np.__version__}\n# OpenCV is installed only in this lane/python_deps; NumPy comes from existing geospatial venv.\n')
