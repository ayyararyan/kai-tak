"""Two visually inspected long mapped runway edges, not surveyed threshold."""
from pathlib import Path
import json,hashlib,numpy as np
from pyproj import Transformer
from shapely.geometry import LineString,box
R=Path(__file__).resolve().parents[1];G=R/'integrated/geometry';j=json.loads((G/'mapped_runway_edge_candidates.json').read_text());sources=json.loads((G/'south_map_sources.json').read_text());sources=sources.get('sources',sources) if isinstance(sources,dict) else sources
# Reviewed candidate3/4 are opposing runwayedges; longcandidates extrapolatinginto
# sea and roadside/typhoonshelter lines are excluded. Picks are source-raster data.
selection=json.loads((G/'mapped_runway_edge_selection.json').read_text())
if hashlib.sha256((G/'south_runway_map.png').read_bytes()).hexdigest()!=selection['source_mosaic_sha256']:raise ValueError('reviewed source changed')
selected=[]
for pixels in selection['selected_pixels']:
 matches=[row for row in j if row['px']==pixels]
 if len(matches)!=1:raise ValueError('reviewed edge absent or duplicate; new visual review required')
 selected.append(matches[0])
T=Transformer.from_crs(2326,4326,always_xy=True);features=[]
for i,p in enumerate(selected):
 xy=np.array(p['px']).reshape(2,2);en=xy*[1,-1]+[839000,819800];ll=np.array(T.transform(en[:,0],en[:,1])).T;used=[]
 for s in sources:
  if LineString(en).intersects(box(*s['index_core_bounds_epsg2326'])):used.append(s)
 features.append({'type':'Feature','properties':{'id':f'mapped_runway_edge_{i}_1993','meaning':'partial opposing mapped runway edge, visually selected fromHoughcandidates','source_mosaic':'integrated/geometry/south_runway_map.png','source_mosaic_sha256':hashlib.sha256((G/'south_runway_map.png').read_bytes()).hexdigest(),'source_sheet_records':used,'mosaic_pixel_edge_endpoints':xy.tolist(),'EN_m':en.tolist(),'grid_crs':'EPSG:2326','query_date':'1993-11-04','query_date_presence_certified':False,'category':'derived from selected mapped line','top_height_HKPD_m':None,'physical_horizontal_error_bound_m':None,'physical_vertical_error_bound_m':None,'clearance_eligible':False},'geometry':{'type':'LineString','coordinates':ll.tolist()}})
a,b=selected;x=400;m1=(a['px'][3]-a['px'][1])/(a['px'][2]-a['px'][0]);m2=(b['px'][3]-b['px'][1])/(b['px'][2]-b['px'][0]);m=(m1+m2)/2;dy=(m1*x+a['intercept'])-(m2*x+b['intercept']);width=abs(dy)/np.sqrt(1+m*m);bearing=float(np.mean([a['bearing'],b['bearing']]))
cross=json.loads((G/'runway_crosscheck.json').read_text());end=np.array(cross['south_picks']['end_EN_m']);th=np.array(cross['north_pick']['derived_EN_m']);beta=np.radians(bearing);back=end-2786*np.array([np.sin(beta),np.cos(beta)])
result={'status':'mapped_line_diagnostic_not_historical_survey','selected_candidate_indices':[3,4],'grid_bearings_deg':[a['bearing'],b['bearing']],'mean_mapped_grid_bearing_deg':bearing,'normal_width_at_mosaic_x400_m':float(width),'reported_width_m':61,'width_difference_m':float(width-61),'source_error_hard_bound_m':None,'threshold_crosscheck_with_mapped_axis':{'back_projected_EN_m':back.tolist(),'disagreement_m':float(np.linalg.norm(th-back)),'accepted':False},'limitations':['Source-map line/raster/edition error notcalibrated.','Crossedges are approximatelyparallel, not exactrectangles imposedondata.','A mappedaxis cannot validate photographictranslation or the aviationdatum.','Chartmagneticbearingplusvariation is not silentlyoverwritten.']}
(G/'mapped_runway_edges.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n');(G/'mapped_runway_axis_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
