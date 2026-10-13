"""Conditional sensitivity examples; NOT recovered building heights/error intervals."""
from pathlib import Path
from datetime import datetime,timezone
import json,csv,math
import numpy as np
from pyproj import Transformer
HERE=Path(__file__).resolve().parent
r=list(csv.DictReader((HERE/'control_points.csv').open()))
s=json.loads((HERE/'registration.json').read_text())
coef=np.array(s['coefficients_pixel_xy1_to_EN']);scale=float(np.sqrt(abs(np.linalg.det(coef[:2]))))
# Analytic low-height first-order derivative H/R: H is a declared scenario, NOT identified camera height AGL.
H=4000*.3048
examples=[]
for R in [100.,250.,500.,750.]:
 for delta in [scale,math.sqrt(2)*3.]:
  examples.append({'camera_height_AGL_scenario_m':H,'ground_radial_distance_scenario_m':R,'relative_base_roof_ground_pick_error_scenario_m':delta,'first_order_height_error_scenario_m':H/R*delta,'interpretation':'sensitivity_only_not_uncertainty_bound'})
obj={'created_utc':datetime.now(timezone.utc).isoformat(),'observed_catalogue_flying_height_ft':4000,'observed_film_label_number':152.12,'nominal_film_number_unit_interpretation':'likely mm focal length, not independently calibrated','camera_height_above_ground_identified':False,'principal_point_identified':False,'local_ground_affine_area_scale_m_per_original_pixel':scale,'formula_assumptions':['central perspective','vertical camera','flat ground and correctly known camera height H above that ground','known principal point','roof and ground point on same vertical building edge','lens and scan distortion corrected'],'exact_relation':'d = h R/(H-h); h = H d/(R+d), where R is true ground radial distance and d is ground-plane-scaled roof relief displacement','derivatives':{'dh_dd':'H R/(R+d)^2','dh_dR':'-H d/(R+d)^2','dh_dH':'d/(R+d)'},'low_height_first_order':'delta_h ≈ (H/R) delta_d; uncertainty diverges toward nadir','sensitivity_scenarios':examples,'actual_roof_base_pairs_measured':0,'actual_building_heights_estimated':0,'height_bounds':None}
(HERE/'height_feasibility.json').write_text(json.dumps(obj,indent=2)+'\n')
tr=Transformer.from_crs(2326,4326,always_xy=True);features=[]
streets=['Nga Tsin Long','Nam Kok','Lung Kong','South Wall','Tak Ku Ling']
for i in range(4):
 rr=[r[i],r[i+1],r[i+6],r[i+5],r[i]]
 en=[(float(z['easting']),float(z['northing'])) for z in rr]
 area=abs(sum(en[j][0]*en[j+1][1]-en[j+1][0]*en[j][1] for j in range(4)))/2
 features.append({'type':'Feature','geometry':{'type':'Polygon','coordinates':[[tr.transform(x,y) for x,y in en]]},'properties':{'block_id':f'KC_ROAD_CONTROL_{i+1:02d}','west_road':streets[i],'east_road':streets[i+1],'north_road':'Carpenter Road','south_road':'Nga Tsin Wai Road','reference_edition_month':'1989-10','photo_epoch':'1993-11-02','area_m2':area,'geometry_semantics':'road-centre matching cell; includes portions of streets; not building/parcel outline','contents_verified':False,'height_valid':False,'role':'local blockwise inspection area'}})
(HERE/'four_road_control_blocks.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n')
print('Affine local area scale',scale,'m/source pixel; blocks',len(features),'total road-centre area',sum(z['properties']['area_m2'] for z in features))
