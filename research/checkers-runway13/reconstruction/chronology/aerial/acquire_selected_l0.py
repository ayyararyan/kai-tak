"""Download selected unrestricted DAP-L0 frames by ordinary public download queue.
The inspected product page has inputRecaptchaEnabled=false. Stop if that changes.
Download URLs are transient, not published in the manifest. No payment/account operation.
"""
import pathlib,json,subprocess,time,urllib.parse,hashlib,datetime,concurrent.futures,struct,re
P=pathlib.Path(__file__).parent;B='https://www.hkmapservice.gov.hk/OpenData/';(P/'fullframes').mkdir(exist_ok=True)
frames={x['properties']['PHOTONO']:x['properties'] for x in json.loads((P/'aerial_footprints_1985_1998.geojson').read_text())['features']}
selected=[x['frame_id'] for x in json.loads((P/'preview_manifest.json').read_text())];selected=sorted(set(selected+['A36143']))
def req(u,d=None):
 a=['curl','-fLsS','--retry','2','--max-time','90']
 if d:a+=['-H','Content-Type: application/json','--data',json.dumps(d)]
 return subprocess.run(a+[u],capture_output=True,check=True).stdout

def get(name):
 product_id=re.sub(r'([A-Z]+)([0-9]+)$',lambda m:m[1]+m[2].zfill(5),name)
 row={'frame_id':name,'product_id':product_id,'capture_date':frames[name]['capture_date_utc'][:10],'product':'DAP-L0','format':'JPEG','source_interface':'https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA','stable_preview_url':'https://www.hkmapservice.gov.hk/OneStopSystem/map-search/productPreview?itemId=DAP&sheetNo='+product_id,'download_method':'public OpenData requestQueue and queueStatus','full_resolution_photogrammetric_scan':False,'download_tier':'300 dpi compressed DAP-L0, not paid high-resolution DAP'}
 try:
  target=P/'fullframes'/(name+'.jpg')
  if target.exists():b=target.read_bytes()
  else:
   payload={'request':{'product_name':'DAP','sheet_name':product_id,'product_format':'JPEG','paper_map_item_id':'','revision_date':'','request_token':None},'ts':round(time.time())}
   d=json.loads(req(B+'api/download/requestQueue',payload));assert d['status']==0, 'queue_request_failed'
   q=d['response']['queue_key']
   for attempt in range(4):
    d=json.loads(req(B+'api/download/queueStatus',{'request':{'queue_key':q},'ts':round(time.time())}));assert d['status']==0,'queue_status_failed'
    if d['response']['queue_number']==0:break
    time.sleep(5)
   assert d['response']['queue_number']==0,'queued_not_ready'
   b=req(urllib.parse.urljoin(B,d['response']['download_path']));assert b[:2]==b'\xff\xd8','not_jpeg';target.write_bytes(b)
  row.update(status='downloaded',path=str(target.relative_to(P)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),retrieved_utc=datetime.datetime.fromtimestamp(target.stat().st_mtime,datetime.timezone.utc).isoformat(),verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:row.update(status='failed',error_type=type(e).__name__)
 print(name,row['status'],flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(get,selected))
(P/'fullframe_manifest.json').write_text(json.dumps(results,indent=2));print('DONE',sum(x['status']=='downloaded' for x in results),len(results),flush=True)
