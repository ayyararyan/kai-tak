"""Spatial source coverage matching, never historical object identity matching."""
from pathlib import Path
import csv,datetime,json,collections,calendar
import numpy as np
from shapely.geometry import shape,box
from shapely import STRtree
from shapely.ops import transform
from pyproj import Transformer
ROOT=Path(__file__).resolve().parent
TARGET=datetime.date(1993,11,4)

def month_bounds(s):
 d=datetime.date.fromisoformat(s[:10]);return d.replace(day=1),d.replace(day=calendar.monthrange(d.year,d.month)[1])

MATCH_FIELDS=['objectid','building_csuid','name_en','lon','lat','status','completion_or_permit_by_target','has_date_conflict','target_date','sheet_before_id','sheet_before_edition_month','sheet_before_downloaded','sheet_after_id','sheet_after_edition_month','sheet_after_downloaded','same_month_sheet_ids','aerial_before_frame','aerial_before_capture_date','aerial_after_frame','aerial_after_capture_date','coverage_match_method','content_match_status','historical_geometry_status']
PAIR_FIELDS=['sheet_id','sheet','edition_month','frame','capture_date','overlap_m2','fraction_sheet_covered','fraction_frame_covered','days_from_edition_month','match_kind']

def valid_sources(features,kind):
 good=[];issues=[]
 for f in features:
  try:
   if not f.get('geometry'):raise ValueError('missing geometry')
   g=shape(f['geometry'])
   if g.is_empty or not g.is_valid:raise ValueError('empty or invalid geometry')
   if kind=='sheet':month_bounds(f['properties'].get('edition_date',''))
   else:datetime.datetime.fromtimestamp(float(f['properties']['DATEFLIGHT'])/1000,datetime.timezone.utc)
   good.append(f)
  except (ValueError,TypeError,KeyError,OverflowError) as e:
   issues.append({'source_id':f.get('properties',{}).get('source_id',f.get('properties',{}).get('PHOTONO')),'kind':kind,'reason':str(e),'treatment':'preserved in original index; unresolved matching'})
 return good,issues

def write_csv(path,rows,fields):
 with path.open('w') as out:
  w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
 all_sheets=json.loads((ROOT/'sheets/aoi_sheet_index.geojson').read_text())['features']
 sheets=[f for f in all_sheets if f['properties']['family']=='1980_1990']
 downloads=json.loads((ROOT/'sheets/map_downloads.json').read_text())
 downloaded={d['source_id'] for d in downloads if d['status']=='validated_zip'}
 frames=json.loads((ROOT/'aerial/aerial_footprints_1985_1998.geojson').read_text())['features']
 frames=[f for f in frames if f['properties']['YEARFLIGHT']==1993]
 sheets,si_issues=valid_sources(sheets,'sheet');frames,fi_issues=valid_sources(frames,'frame');issues=si_issues+fi_issues
 sg=[shape(f['geometry']) for f in sheets];fg=[shape(f['geometry']) for f in frames]
 st=STRtree(sg);ft=STRtree(fg)
 frame_dates=[datetime.datetime.fromtimestamp(f['properties']['DATEFLIGHT']/1000,datetime.timezone.utc).date() for f in frames]
 sheet_bounds=[month_bounds(f['properties']['edition_date']) for f in sheets]
 rows=[]
 src=ROOT/'structures/aoi_features_1993-11-04.csv'
 from shapely.geometry import Point
 for i,b in enumerate(csv.DictReader(src.open())):
  try:
   pt=Point(float(b['lon']),float(b['lat']));si=st.query(pt,predicate='intersects');fi=ft.query(pt,predicate='intersects')
  except (ValueError,TypeError):
   si=[];fi=[];issues.append({'kind':'current_feature','source_id':b['building_csuid'],'reason':'missing representative point','treatment':'retained; no source coverage claim'})
  before=[int(j) for j in si if sheet_bounds[int(j)][1]<=TARGET];after=[int(j) for j in si if sheet_bounds[int(j)][0]>TARGET];same=[int(j) for j in si if sheet_bounds[int(j)][0]<=TARGET<sheet_bounds[int(j)][1]]
  pre=max(before,key=lambda j:(sheet_bounds[j][1],sheets[j]['properties'].get('edition') or 0,sheets[j]['properties']['source_id'])) if before else None;post=min(after,key=lambda j:(sheet_bounds[j][0],sheets[j]['properties'].get('edition') or 0,sheets[j]['properties']['source_id'])) if after else None
  fp=[int(j) for j in fi if frame_dates[int(j)]<=TARGET];fa=[int(j) for j in fi if frame_dates[int(j)]>TARGET]
  fpre=min(fp,key=lambda j:(abs((TARGET-frame_dates[j]).days),fg[j].area,frames[j]['properties']['PHOTONO'])) if fp else None
  fpost=min(fa,key=lambda j:(abs((TARGET-frame_dates[j]).days),fg[j].area,frames[j]['properties']['PHOTONO'])) if fa else None
  r={k:b[k] for k in ['objectid','building_csuid','name_en','lon','lat','status','completion_or_permit_by_target','has_date_conflict']}
  r['target_date']=str(TARGET)
  for label,j in [('sheet_before',pre),('sheet_after',post)]:
   p=sheets[j]['properties'] if j is not None else {}
   r[label+'_id']=p.get('source_id','');r[label+'_edition_month']=p.get('edition_date','')[:7];r[label+'_downloaded']=int(p.get('source_id') in downloaded)
  r['same_month_sheet_ids']='|'.join(sheets[j]['properties']['source_id'] for j in same)
  for label,j in [('aerial_before',fpre),('aerial_after',fpost)]:
   r[label+'_frame']=frames[j]['properties']['PHOTONO'] if j is not None else '';r[label+'_capture_date']=str(frame_dates[j]) if j is not None else ''
  r['coverage_match_method']='current_footprint_representative_point_in_index_polygon';r['content_match_status']='not_visually_verified';r['historical_geometry_status']='unresolved'
  rows.append(r)
 write_csv(ROOT/'structure_source_matches_1993-11-04.csv',rows,MATCH_FIELDS)
 # Exact index-polygon overlap for downloaded-sheet / 1993-frame pairs.
 project=Transformer.from_crs(4326,2326,always_xy=True).transform
 fgp=[transform(project,g) for g in fg];pairs=[]
 for f,g in zip(sheets,sg):
  p=f['properties']
  if p['source_id'] not in downloaded:continue
  gp=transform(project,g)
  for j in ft.query(g,predicate='intersects'):
   j=int(j)
   if not gp.is_valid or not fgp[j].is_valid:
    issues.append({'kind':'overlap','source_id':p['source_id'],'frame':frames[j]['properties']['PHOTONO'],'reason':'invalid projected polygon','treatment':'overlap unresolved'});continue
   area=gp.intersection(fgp[j]).area
   if area<=0:continue
   lo,hi=month_bounds(p['edition_date']);fd=frame_dates[j]
   gap=(lo-fd).days if fd<lo else (fd-hi).days if fd>hi else 0
   pairs.append({'sheet_id':p['source_id'],'sheet':p['sheet'],'edition_month':p['edition_date'][:7],'frame':frames[j]['properties']['PHOTONO'],'capture_date':str(fd),'overlap_m2':area,'fraction_sheet_covered':area/gp.area,'fraction_frame_covered':area/fgp[j].area,'days_from_edition_month':gap,'match_kind':'index_polygon_overlap_only'})
 write_csv(ROOT/'sheet_photo_pairs_1993.csv',pairs,PAIR_FIELDS)
 (ROOT/'matching_issues.json').write_text(json.dumps(issues,indent=2))
 summary={'target_date':str(TARGET),'current_aoi_features':len(rows),'unique_csuid':len({r['building_csuid'] for r in rows}),'has_both_bracketing_sheet_months':sum(bool(r['sheet_before_id'] and r['sheet_after_id']) for r in rows),'has_any_downloaded_bracketing_sheet':sum(bool(r['sheet_before_downloaded'] or r['sheet_after_downloaded']) for r in rows),'has_1993_aerial_before':sum(bool(r['aerial_before_frame']) for r in rows),'has_1993_aerial_after':sum(bool(r['aerial_after_frame']) for r in rows),'sheet_frame_overlap_pairs':len(pairs),'downloaded_sheets_paired':len(set(r['sheet_id'] for r in pairs)),'frame_count_1993':len(frames),'unresolved_input_or_overlap_issues':len(issues),'semantics':'Source coverage candidates, not visual confirmation, footprint identity, height measurement or historical clearance.'}
 (ROOT/'matching_validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
