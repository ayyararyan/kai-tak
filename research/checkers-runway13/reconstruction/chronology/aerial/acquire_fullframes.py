"""Follow the public OpenData download flow. Do not bypass CAPTCHA if enabled."""
import json,subprocess,time,pathlib
P=pathlib.Path(__file__).parent;BASE='https://www.hkmapservice.gov.hk/OpenData/'
def curl(url,data=None):
 args=['curl','-fLsS','--retry','2','--max-time','60']
 if data:args+=['-H','Accept: application/json','-H','Content-Type: application/json','--data',json.dumps(data)]
 r=subprocess.run(args+[url],capture_output=True,check=True);return r.stdout
name='A36143';a={'request':{'product_name':'DAP','sheet_name':name,'product_format':'JPEG','paper_map_item_id':'','revision_date':'','request_token':None},'ts':round(time.time())}
d=json.loads(curl(BASE+'api/download/requestQueue',a));print('status',d.get('status'))
if d.get('status')==0:
 q=d['response']['queue_key'];(P/'queue_page.html').write_bytes(curl(BASE+'requestQueue?queueKey='+q))
 private=P/'queue_state_private.json';private.write_text(json.dumps(d));private.chmod(0o600)
