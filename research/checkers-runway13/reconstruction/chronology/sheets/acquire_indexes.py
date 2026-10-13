"""Acquire official survey-sheet indexes, preserve raw pages and derive AOI matches."""
from pathlib import Path
import concurrent.futures,csv,datetime,hashlib,json,subprocess,urllib.parse
from zoneinfo import ZoneInfo
from shapely.geometry import shape,box,mapping
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'raw';RAW.mkdir(exist_ok=True)
SERVICES=[('old600','landsd_rcd_1631584892859_72892',0),('t600','landsd_rcd_1631584892859_72892',1),('t1200','landsd_rcd_1639990901210_47291',0),('1960_1970','landsd_rcd_1640047202071_61921',0),('1980_1990','landsd_rcd_1640047456225_68329',0),('2000s','landsd_rcd_1671592436814_1059',0)]
AOI=box(114.10,22.27,114.25,22.40)
CORE=box(114.16,22.30,114.22,22.35)

def get(url,path):
 if not path.exists():
  p=path.with_suffix(path.suffix+'.part')
  r=subprocess.run(['curl','-f','-sSL','--retry','2','--connect-timeout','15','--max-time','90',url,'-o',str(p)],capture_output=True,text=True)
  if r.returncode:raise RuntimeError(r.stderr)
  d=json.loads(p.read_text())
  if 'error' in d:raise RuntimeError(d)
  p.replace(path)
 d=json.loads(path.read_text())
 if 'error' in d:raise RuntimeError(d)
 path.with_suffix(path.suffix+'.source.json').write_text(json.dumps({'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2)) if not path.with_suffix(path.suffix+'.source.json').exists() else None
 return d

def acquire(s):
 name,ds,layer=s
 base=f'https://portal.csdi.gov.hk/server/rest/services/common/{ds}/FeatureServer/{layer}'
 meta=get(base+'?f=json',RAW/f'{name}_metadata.json')
 count=get(base+'/query?f=json&where=1%3D1&returnCountOnly=true',RAW/f'{name}_count.json')['count']
 fs=[]
 for offset in range(0,count,2000):
  q={'f':'geojson','where':'1=1','outFields':'*','returnGeometry':'true','outSR':4326,'orderByFields':'OBJECTID','resultOffset':offset,'resultRecordCount':2000}
  page=get(base+'/query?'+urllib.parse.urlencode(q),RAW/f'{name}_{offset:06d}.geojson')
  fs.extend(page['features'])
 assert len(fs)==count,(name,count,len(fs))
 assert len({f['properties']['OBJECTID'] for f in fs})==count
 rows=[];selected=[]
 for f in fs:
  p=f['properties'];g=shape(f['geometry']) if f.get('geometry') else None
  usable=g is not None and not g.is_empty; bounds=g.bounds if usable else [None]*4
  dt=p.get('EDITION_DATE');iso=datetime.datetime.fromtimestamp(dt/1000,ZoneInfo('Asia/Hong_Kong')).date().isoformat() if isinstance(dt,(int,float)) else str(dt or '')
  row={'source_id':f"{name}:{p['OBJECTID']}",'family':name,'objectid':p['OBJECTID'],'sheet':p.get('SHEETNO'),'edition_date':iso,'edition':p.get('EDITION'),'download_url':p.get('GeoTiff'),'in_aoi':bool(usable and g.intersects(AOI)),'in_core':bool(usable and g.intersects(CORE)),'geometry_status':'valid' if usable and g.is_valid else 'invalid' if usable else 'missing_or_empty','minlon':bounds[0],'minlat':bounds[1],'maxlon':bounds[2],'maxlat':bounds[3]}
  rows.append(row)
  if row['in_aoi']:selected.append({'type':'Feature','properties':row,'geometry':f['geometry']})
 print(name,'complete',count,'aoi',len(selected),flush=True)
 return rows,selected,{'family':name,'source_count':count,'downloaded_count':len(fs),'aoi_count':len(selected),'metadata_fields':[v['name'] for v in meta['fields']]}

if __name__=='__main__':
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  for out in ex.map(acquire,SERVICES):results.append(out)
 rows=[r for a,_,_ in results for r in a];features=[f for _,a,_ in results for f in a]
 with (ROOT/'all_hk_sheet_index.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (ROOT/'aoi_sheet_index.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
 (ROOT/'index_validation.json').write_text(json.dumps({'sources':[a for _,_,a in results],'total':len(rows),'aoi':len(features),'aoi_bbox':[114.10,22.27,114.25,22.40],'core_bbox':[114.16,22.30,114.22,22.35],'date_semantics':'edition date, Asia/Hong_Kong; not per-object survey date'},indent=2))
 print('DONE',len(rows),len(features),flush=True)
