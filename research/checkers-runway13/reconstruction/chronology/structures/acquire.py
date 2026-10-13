"""Complete read-only official CSDI table snapshots; ID and count validation."""
import concurrent.futures, datetime, hashlib, json, pathlib, time, urllib.parse, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
BASE='https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer'
TABLES={1000:'BuildingWorksHistory',1002:'BuildingRelateOPStructure',1003:'OPStructure',1004:'OP'}
def request(url):
    for n in range(4):
        try:
            raw=urllib.request.urlopen(url,timeout=90).read(); obj=json.loads(raw)
            if 'error' in obj: raise ValueError(obj)
            return raw,obj
        except Exception:
            if n==3: raise
            time.sleep(2**n)
def get(path,params,out):
    url=BASE+path+'?'+urllib.parse.urlencode(params);raw,obj=request(url)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
    return obj,{'path':str(out.relative_to(ROOT)),'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def table(tid):
    name=TABLES[tid];folder=ROOT/'raw'/name;files=[]
    def fetch(path,params,filename):
        obj,entry=get(path,params,folder/filename);files.append(entry);return obj
    meta=fetch('/'+str(tid),{'f':'json'},'metadata.json')
    q='/'+str(tid)+'/query'
    before=fetch(q,{'where':'1=1','returnCountOnly':'true','f':'json'},'count_before.json')['count']
    ids=fetch(q,{'where':'1=1','returnIdsOnly':'true','f':'json'},'ids.json')['objectIds']
    assert len(ids)==len(set(ids))==before
    rows=[];oid=meta['objectIdField'];limit=meta['maxRecordCount']
    for offset in range(0,before,limit):
        data=fetch(q,{'where':'1=1','outFields':'*','returnGeometry':'false','orderByFields':oid+' ASC','resultOffset':offset,'resultRecordCount':limit,'f':'json'},f'page_{offset:06d}.json')
        rows += [r['attributes'] for r in data['features']]
    after=fetch(q,{'where':'1=1','returnCountOnly':'true','f':'json'},'count_after.json')['count']
    assert len(rows)==after==before and set(r[oid] for r in rows)==set(ids)
    assert len(set(r[oid] for r in rows))==len(rows)
    (ROOT/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False))
    print(name,len(rows),'count/ID validation passed',flush=True)
    return {'table_id':tid,'name':name,'count_before':before,'count_after':after,'retrieved_count':len(rows),'objectids_match':True,'files':files}
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(table,TABLES))
    (ROOT/'acquisition_manifest.json').write_text(json.dumps({'provider':'Lands Department, HKSAR Government, CSDI','tables':results},indent=2))
