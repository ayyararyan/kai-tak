import pathlib,json,subprocess,time,urllib.parse
P=pathlib.Path(__file__).parent;B='https://www.hkmapservice.gov.hk/OpenData/'
def req(u,d=None):
 a=['curl','-fLsS','--retry','2','--max-time','90']
 if d:a+=['-H','Content-Type: application/json','--data',json.dumps(d)]
 return subprocess.run(a+[u],capture_output=True,check=True).stdout
q=json.loads((P/'queue_state_private.json').read_text())['response']['queue_key'];d=json.loads(req(B+'api/download/queueStatus',{'request':{'queue_key':q},'ts':round(time.time())}));print('status',d['status'],'queue',d.get('response',{}).get('queue_number'))
if d['status']==0 and d['response']['queue_number']==0:
 u=urllib.parse.urljoin(B,d['response']['download_path']);b=req(u);(P/'A36143_l0_download_result').write_bytes(b);print('bytes',len(b),'magic',b[:10])
