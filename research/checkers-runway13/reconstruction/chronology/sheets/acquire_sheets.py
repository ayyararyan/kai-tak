"""Acquire source rasters for historical approach core; selected pre/post-date editions."""
from pathlib import Path
import collections,concurrent.futures,csv,datetime,hashlib,json,subprocess,zipfile,os,time,calendar
ROOT=Path(__file__).resolve().parent
TARGET='1993-11-04'
RAW=ROOT/'maps';RAW.mkdir(exist_ok=True)
KEY={'11-NW-10D','11-NE-11A','11-NE-16B','11-NE-17C','11-NW-15B','11-NE-11C','11-NE-16A'}

def month_bounds(value):
 d=datetime.date.fromisoformat(value[:10]);return d.replace(day=1),d.replace(day=calendar.monthrange(d.year,d.month)[1])

def cached_valid(receipt,dest):
 return receipt.get('status')=='validated_zip' and dest.is_file() and hashlib.sha256(dest.read_bytes()).hexdigest()==receipt.get('sha256')

def select():
 fs=json.loads((ROOT/'aoi_sheet_index.geojson').read_text())['features'];by=collections.defaultdict(list)
 for f in fs:
  p=f['properties']
  if p['in_core'] and p['family']=='1980_1990':by[p['sheet']].append(p)
 selected={}
 for sheet,rows in by.items():
  before=sorted([p for p in rows if month_bounds(p['edition_date'])[1]<=datetime.date.fromisoformat(TARGET)],key=lambda p:p['edition_date'])
  after=sorted([p for p in rows if month_bounds(p['edition_date'])[0]>datetime.date.fromisoformat(TARGET)],key=lambda p:p['edition_date'])
  same=[p for p in rows if month_bounds(p['edition_date'])[0]<=datetime.date.fromisoformat(TARGET)<=month_bounds(p['edition_date'])[1]]
  for p in before[-1:]+after[:1]+same:selected[p['source_id']]=dict(p,selection='core_before_after_reference_date')
  if sheet in KEY:
   for p in rows:selected[p['source_id']]=dict(p,selection='key_site_time_series')
 return sorted(selected.values(),key=lambda p:(p['sheet'] not in KEY,p['sheet'],p['edition_date']))

def acquire(p):
 stem=p['source_id'].replace(':','_')+'_'+p['sheet']+'_'+p['edition_date'];dest=RAW/(stem+'.zip');receipt=RAW/(stem+'.json')
 if receipt.exists():
  d=json.loads(receipt.read_text())
  if cached_valid(d,dest):return d
  if dest.exists() and d.get('status')=='validated_zip':dest.rename(dest.with_suffix('.zip.invalidated-'+str(time.time_ns())))
 previous=json.loads(receipt.read_text()) if receipt.exists() else None
 if previous:time.sleep(1)
 d=dict(p,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),file=str(dest.relative_to(ROOT)))
 try:
  if not dest.exists():
   part=dest.with_suffix('.zip.part')
   r=subprocess.run(['curl','-f','-sSL','--connect-timeout','15','--max-time','100','--retry','1',p['download_url'],'-o',str(part)],capture_output=True,text=True)
   if r.returncode:raise RuntimeError(r.stderr[-600:])
   if not zipfile.is_zipfile(part):raise RuntimeError('Response is not ZIP: '+part.read_bytes()[:100].decode(errors='replace'))
   part.replace(dest)
  with zipfile.ZipFile(dest) as z:
   bad=z.testzip()
   if bad:raise RuntimeError('ZIP CRC failure '+bad)
   d['members']=[{'name':i.filename,'bytes':i.file_size} for i in z.infolist()]
   if not any(i.filename.lower().endswith(('.tif','.tiff')) for i in z.infolist()):raise RuntimeError('No TIFF member')
  d.update(status='validated_zip',bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
 except Exception as e:d.update(status='failed',error=str(e))
 if previous:d['previous_attempts']=previous.get('previous_attempts',[])+[{k:v for k,v in previous.items() if k!='previous_attempts'}]
 receipt.write_text(json.dumps(d,indent=2));return d

if __name__=='__main__':
 sel=select();(ROOT/'selected_sheets.json').write_text(json.dumps(sel,indent=2));print('SELECTED',len(sel),len(set(p['sheet'] for p in sel)),flush=True)
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get("SHEET_WORKERS","4"))) as ex:
  for i,r in enumerate(ex.map(acquire,sel),1):
   results.append(r)
   if i%10==0:print('PROGRESS',i,len(sel),collections.Counter(r['status'] for r in results),flush=True)
 (ROOT/'map_downloads.json').write_text(json.dumps(results,indent=2))
 print('DONE',len(results),collections.Counter(r['status'] for r in results),sum(r.get('bytes',0) for r in results),flush=True)
