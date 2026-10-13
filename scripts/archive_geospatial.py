#!/usr/bin/env python3
"""Read-only geospatial QA of installed collections 02/03; preserve invalid source features."""
import argparse,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUILDING_COUNTERS = ('features', 'BaseHeight_missing', 'TopHeight_missing', 'invalid_geometry')
def compare_building_counts(counts, expected):
 # These are whole-source checks; separately recorded subset counts are not measured here.
 return {key: key in expected and counts[key] == expected[key] for key in BUILDING_COUNTERS}
def check(data_root):
 import ijson,numpy as np,rasterio
 from shapely.geometry import shape
 g=data_root/'research/checkers-runway13/geospatial';expected=json.loads((ROOT/'research/checkers-runway13/geospatial/metadata/validation.json').read_text());counts=collections.Counter({key: 0 for key in BUILDING_COUNTERS});bbox=[180,90,-180,-90]
 with (g/'raw/Building_20260921.geojson').open('rb') as f:
  for x in ijson.items(f,'features.item',use_float=True):
   counts['features']+=1;props=x['properties']
   for k in ['BaseHeight','TopHeight']:
    if props.get(k) is None:counts[k+'_missing']+=1
   geom=shape(x['geometry']);counts['invalid_geometry']+=not geom.is_valid
   if not geom.is_empty:
    l,b,r,t=geom.bounds;bbox=[min(l,bbox[0]),min(b,bbox[1]),max(r,bbox[2]),max(t,bbox[3])]
 with rasterio.open(g/'derived/Hong_Kong_DTM_5m_HK1980.tif') as ds:
  valid=0;lo=float('inf');hi=float('-inf')
  for _,window in ds.block_windows(1):
   x=ds.read(1,window=window,masked=True);valid+=x.count();lo=min(lo,float(x.min()));hi=max(hi,float(x.max()))
  dtm={'shape':list(ds.shape),'bounds':list(ds.bounds),'crs':str(ds.crs),'nodata':ds.nodata,'valid_cells':int(valid),'total_cells':int(ds.width*ds.height),'min_height_m':lo,'max_height_m':hi}
 checks=compare_building_counts(counts, expected['buildings']['counts'])
 checks.update({'dtm_'+k:dtm[k]==expected['terrain'][k] for k in dtm});checks['building_wgs84_coverage']=all(abs(a-b)<1e-9 for a,b in zip(bbox,expected['buildings']['bounds_wgs84']))
 return {'schema_version':'1.0.0','status':'passed' if all(checks.values()) else 'failed','checks':checks,'buildings':dict(counts),'building_bounds_wgs84':bbox,'terrain':dtm,'observation_epoch':'DTM photography 2014–2015; building revision 2026-09-21, actual feature observation times unknown','vertical_datum':'HKPD; building BaseHeight/TopHeight are elevations, not AGL heights','historical_1993_validity':False,'source_repair_performed':False,'known_invalid_geometries_retained':counts['invalid_geometry'],'meaning':'Matches source QA counts, not survey calibration or historical accuracy.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data-root',type=Path,default=ROOT);p.add_argument('--report',type=Path);a=p.parse_args();r=check(a.data_root)
 if a.report:a.report.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2));return int(r['status']!='passed')
if __name__=='__main__':raise SystemExit(main())
