"""Read-only public HKMS index lookup; no credentials in receipts or logs."""
from pathlib import Path
import urllib.request,urllib.parse,re,json,datetime,hashlib
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent/'sources';base='https://api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2/query'
key=re.search("API_KEY= '([^']+)'",(R/'reconstruction/chronology/aerial/constants_appConstant.js').read_text()).group(1)
def get(params):
 with urllib.request.urlopen(base+'?'+urllib.parse.urlencode(dict(f='json',key=key,**params)),timeout=25) as response:r=json.load(response)
 if 'error' in r:raise RuntimeError(str(r['error']))
 return r
ids=get(dict(where='YEARFLIGHT = 1993',returnIdsOnly='true'))['objectIds'];rows=[]
for i in range(0,len(ids),500):
 out=O/f'all_hk_1993_index_{i:05d}.json'
 data=get(dict(objectIds=','.join(map(str,ids[i:i+500])),outFields='*',returnGeometry='false'))
 if data.get('exceededTransferLimit'):raise RuntimeError('Incomplete response')
 out.write_text(json.dumps(data));rows.extend(f['attributes'] for f in data['features'])
hits=[]
for r in rows:
 date=datetime.datetime.fromtimestamp(r['DATEFLIGHT']/1000,datetime.timezone.utc).date().isoformat()
 if date=='1993-11-05' or any(n in r['PHOTONO'] for n in ['72998','72999','73000','73001']):hits.append(dict(r,capture_date=date))
assert len(rows)==len(set(ids))
receipt=dict(endpoint=base,where='YEARFLIGHT = 1993',scope='all public layer2 records for1993; not special-survey completeness',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),count=len(rows),matches=hits,files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.glob('all_hk_1993_index_*.json')},query_keys_not_saved=True)
(O/'survey_archive_check.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:v for k,v in receipt.items() if k!='files'},indent=2))
