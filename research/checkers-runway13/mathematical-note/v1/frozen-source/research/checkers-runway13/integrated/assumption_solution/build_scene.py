from pathlib import Path
import json,hashlib
import numpy as np
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'integrated/geometry/integrated_evidence.geojson'
j=json.loads(source.read_text());tf=Transformer.from_crs(4326,2326,always_xy=True)
origin=np.array([838277.9926795285,820320.961097593]);beta=np.deg2rad(134.02)
R=np.array([[np.sin(beta),np.cos(beta)],[np.cos(beta),-np.sin(beta)]])
def local(x,y,z=None):
 en=np.array(tf.transform(x,y));v=R@(en-origin[:,None] if en.ndim==2 else en-origin);return v[0],v[1]
obs=[];hill=[]
for i,f in enumerate(j['features']):
 p=f['properties'];g=transform(local,shape(f['geometry']));ident=f.get('id') or p.get('id') or f'source_feature_{i}'
 if ident=='whole_approach_acquisition_core_unknown':continue
 if g.geom_type=='Polygon':
  obs.append(dict(id=ident,source_index=i,bounds_xy=list(g.bounds),top_hkpd_assumed_m=45.,category='source_footprint_assumed_top_and_epoch'))
 elif p.get('integrated_role') in ('surface_point_observation','additional_historical_terrain_evidence'):
  hill.extend(np.array(g.coords).tolist())
 elif p.get('integrated_role')=='mapped_equipment_point':
  x,y=g.x,g.y;obs.append(dict(id=ident,source_index=i,bounds_xy=[x-2,y-2,x+2,y+2],top_hkpd_assumed_m=12.,category='source_point_assumed_equipment_solid'))
h=np.array(hill);lo=h.min(axis=0)-50;hi=h.max(axis=0)+50
obs.append(dict(id='assumed_hill_and_equipment_cap',bounds_xy=[*lo,*hi],top_hkpd_assumed_m=140.,category='assumed_rectangle_and_cap_from_source_spot_extent'))
scene=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),origin_EN_assumed_m=origin.tolist(),grid_bearing_assumed_deg=134.02,runway_HKPD_assumed_m=6.,obstacles=obs,historical_certified=False,source_nulls_modified=False,
 background=dict(urban_top_above_runway_m=25.,urban_end_x_m=-600.,clear_approach_halfwidth_m=100.,ground_m=0.,category='assumed_completion_of_unknown_coverage'))
(OUT/'scene.json').write_text(json.dumps(scene,indent=2)+'\n');print(len(obs),'obstacles')
