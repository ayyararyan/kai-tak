"""Independent source picks: diagnostic ONLY, never historical registration."""
from pathlib import Path
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];G=R/'integrated/geometry'
def j(p):return json.loads((R/p).read_text())
old=np.array(j('reconstruction/block_matching/aerial_registration/registration.json')['coefficients_pixel_xy1_to_EN'])
north=np.array(j('integrated/geometry/runway_registration_diagnostic.json')['source_pixel_xy1_to_EN'])
south=np.array(j('integrated/geometry/south_registration_diagnostic.json')['source_pixel_xy1_to_EN'])
# RW13 threshold bar centre, read on the explicit900x900 crop. Not the far end of piano keys.
north_detail=np.array([378.,403.]);full=np.array([1300,1250])+north_detail/3
old_en=full*[.5,-.5]+[837500,821000];north_px=(old_en-old[2])@np.linalg.inv(old[:2]);direct=np.r_[north_px,1]@north
# Southeast physical pavement-end centre and upstream runway31 mark, read on1200x1000 crop.
# Mapping crop=(1850,2350,2450,2850) of original3000x3000 CW-rotated image, resize2.
def south_point(detail):
 cw=np.array([1850,2350])+np.array(detail)/2
 xy=np.array([cw[1],3000-cw[0]])
 return xy,np.r_[xy,1]@south
end_px,end=south_point([716,747]);up_px,up=south_point([207,319]);axis=(end-up)/np.linalg.norm(end-up)
back=end-2786*axis;diff=direct-back
r={'status':'crosscheck_failure_diagnostic_not_accepted_registration','north_pick':{'image':'RW13_threshold_detail.png','pixel_xy':north_detail.tolist(),'meaning':'visually interpreted threshold bar centre','original_A36143_pixel_xy':north_px.tolist(),'derived_EN_m':direct.tolist()},'south_picks':{'image':'A36172_runway_end_detail.png','end_pixel_xy':[716,747],'axis_upstream_pixel_xy':[207,319],'end_original_A36172_pixel_xy':end_px.tolist(),'upstream_original_A36172_pixel_xy':up_px.tolist(),'end_EN_m':end.tolist(),'axis_grid_bearing_deg':float(np.degrees(np.arctan2(*axis))%360),'upstream_point_to_end_m':float(np.linalg.norm(end-up))},'back_projection':{'assumed_distance_m':2786,'basis':'CAD Report1/95 LDA; physical endpoint interpretation not independently validated','threshold_EN_m':back.tolist()},'threshold_difference_EN_m':diff.tolist(),'threshold_disagreement_m':float(np.linalg.norm(diff)),'uncertainty':{'physical_hard_bound_m':None,'northern_holdout_RMS_m':j('integrated/geometry/runway_registration_diagnostic.json')['holdout_rmse_m'],'southern_holdout_RMS_m':j('integrated/geometry/south_registration_diagnostic.json')['holdout_RMS_m']},'limitations':['Two local camera fits are not a jointly controlled orthophoto network.','Short southern direction baseline magnifies angular error over2786m.','Map edition differences, affine perspective error, edge semantics and manual picks remain unresolved.','Disagreement is evidence against acceptance, not a calibrated probability interval.','No averaged threshold or borrowed chart bearing is accepted.']}
r['source_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [G/'RW13_threshold_detail.png',G/'A36172_runway_end_detail.png',G/'runway_registration_diagnostic.json',G/'south_registration_diagnostic.json',Path(__file__)]}
(G/'runway_crosscheck.json').write_text(json.dumps(r,indent=2)+'\n');print('Threshold disagreement',r['threshold_disagreement_m'],'m; no historical registration accepted')
