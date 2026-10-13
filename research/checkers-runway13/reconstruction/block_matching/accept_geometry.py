"""Parent's explicit visual decisions, then reproducible geometry/identity joins."""
from pathlib import Path
import json,csv,hashlib
from collections import defaultdict
from shapely.geometry import shape,mapping,box
from shapely.ops import transform,unary_union
from shapely.strtree import STRtree
from pyproj import Transformer
R=Path(__file__).resolve().parent
PROJ=R.parent.parent
TOHK=Transformer.from_crs(4326,2326,always_xy=True).transform
TOWGS=Transformer.from_crs(2326,4326,always_xy=True).transform

def fc(fs,projected=False):
 d={'type':'FeatureCollection','features':fs}
 if projected:d['crs']={'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::2326'}}
 return d

def reviewed_candidate_matches(feature, review):
 if review is None:return False
 digest=hashlib.sha256(json.dumps(feature,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return digest==review.get('candidate_sha256')

def main():
 fs=json.loads((R/'digitization_candidates_hk1980.geojson').read_text())['features']
 reviews=json.loads((R/'reviewed_geometry_manifest.json').read_text())['rows']
 approved={(p['id'],p['source_id']):p for p in reviews}
 accepted=[];decisions=[]
 for f in fs:
  p=f['properties'];i=p['id']
  if i=='clinic':
   decisions.append({'id':i,'source':p['source_id'],'decision':'reject','reason':'seed selected a small adjoining map subdivision, not the labelled clinic outline'});continue
  review=approved.get((i,p['source_id']))
  geometry_hash=hashlib.sha256(json.dumps(f['geometry'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
  if not reviewed_candidate_matches(f,review) or review['geometry_sha256']!=geometry_hash or review['source_sha256']!=p['source_sha256']:
   decisions.append({'id':i,'source':p['source_id'],'decision':'pending_new_visual_review','reason':'not identical to the hash-bound inspected source geometry'});continue
  overlay=R/review['overlay']
  if not overlay.exists() or hashlib.sha256(overlay.read_bytes()).hexdigest()!=review['overlay_sha256']:
   raise ValueError('Reviewed overlay missing or modified: '+str(overlay))
  archive=R.parent/'chronology/sheets'/p['source_archive']
  if hashlib.sha256(archive.read_bytes()).hexdigest()!=review['source_sha256']:
   raise ValueError('Reviewed original source changed: '+str(archive))
  note='Parent visually inspected extracted exterior against the registered source overlay; agreement as a depicted building face, not a surveyed historical roof mesh.'
  if i=='lok_sin_school':note+=' Partial mapped face; north portion gains crossed/dashed symbol in 1994/1997, interpretation unresolved. Do not infer unchanged physical state.'
  if i=='market_podium':note+=' Mapped market face adjoining On Tung complex; distinct cartographic face, not necessarily an independent building.'
  if i=='ng_wah':note+=' Combined mapped school form, not a modern one-to-one structure identity.'
  p.update(review_status='visually_checked_map_face',geometry_role='historical_depicted_building_face',review_note=note,full_structure_mesh=False,review_evidence=f'digitization_overlay_{p["source_epoch"]}.png')
  accepted.append(f);decisions.append({'id':i,'source':p['source_id'],'decision':'accept_depicted_face','note':note})
 # Current features may be multiple vertically stacked parts of the same footprint.
 current=json.loads((PROJ/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson').read_text())['features']
 pairs=[]
 for f in current:
  g=transform(TOHK,shape(f['geometry']))
  if g.is_valid and g.intersects(box(837500,821000,838250,821600)):pairs.append((g,f))
 tree=STRtree([g for g,f in pairs]);modern_joins=[]
 for f in accepted:
  g=shape(f['geometry']);joins=[]
  for idx in tree.query(g):
   c,m=pairs[idx];inter=g.intersection(c).area
   if inter/max(1,min(g.area,c.area))<.35:continue
   iou=inter/g.union(c).area;props=m['properties']
   joins.append({'csuid':props['BuildingCSUID'],'name':props.get('BuildingNameEN'),'geometry_iou':iou,'historical_face_fraction':inter/g.area,'modern_fraction':inter/c.area,'modern_top_hkpd_m':props.get('TopHeight'),'modern_base_hkpd_m':props.get('BaseHeight'),'height_epoch':'2026-09-21','height_transfer_to_historical':False,'identity_status':'spatial_correspondence_candidate'})
  joins.sort(key=lambda j:j['geometry_iou'],reverse=True)
  f['properties']['modern_correspondences']=joins
  modern_joins.extend({'historical_id':f['properties']['id'],'map_epoch':f['properties']['source_epoch'],**j} for j in joins)
 (R/'historical_faces_hk1980.geojson').write_text(json.dumps(fc(accepted,True),indent=2))
 wgs=[]
 for f in accepted:wgs.append({'type':'Feature','geometry':mapping(transform(TOWGS,shape(f['geometry']))),'properties':dict(f['properties'],crs='EPSG:4326',source_grid_crs='EPSG:2326')})
 (R/'historical_faces.geojson').write_text(json.dumps(fc(wgs),indent=2))
 # Cross-map correspondence identifies the depicted form, not day-specific survival.
 by=defaultdict(list)
 for f in accepted:by[f['properties']['id']].append(f)
 match=[]
 for i,group in by.items():
  base=next(f for f in group if f['properties']['source_epoch']=='1989-10');g=shape(base['geometry'])
  for f in group:
   h=shape(f['geometry']);match.append({'historical_id':i,'name':f['properties']['name'],'from_epoch':'1989-10','to_epoch':f['properties']['source_epoch'],'geometry_iou':g.intersection(h).area/g.union(h).area,'name_and_form_reviewed':True,'same_depicted_form':i!='lok_sin_school','continued_presence_every_day_verified':False,'historical_height_verified':False})
 (R/'structure_matches.json').write_text(json.dumps(match,indent=2))
 (R/'modern_correspondences.json').write_text(json.dumps(modern_joins,indent=2))
 (R/'manual_review_decisions.json').write_text(json.dumps({'reviewer':'parent direct image inspection','overlays_inspected':['1989-10','1994-07','1997-04'],'decisions':decisions,'prior_seed_corrections':['Dispensary seed initially traced its compound: rejected and re-picked inside actual labelled building.','Block 23 seed initially fell outside the E-shaped building: rejected and re-picked inside western spine.','Clinic subface rejected and not included in accepted layer.'],'count_accepted_source_faces':len(accepted),'count_named_forms':len(by)},indent=2))
 # Preserve full unknown coverage even where a horizontal face has been reviewed.
 mask=json.loads((R.parent/'chronology/historical_uncertainty_mask.geojson').read_text())
 for f in mask['features']:
  f['properties'].update(reason='Whole-area historical 3D completeness remains unresolved; reviewed 2D faces do not establish roof height or complete obstacle coverage.',historical_height_unknown=True,complete_historical_3d=False,physical_occupancy=None)
 (R/'historical_3d_unknown_mask.geojson').write_text(json.dumps(mask,indent=2))
 print('Accepted source faces',len(accepted),'named forms',len(by),'modern component joins',len(modern_joins))
if __name__=='__main__':main()
