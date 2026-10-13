import pathlib,subprocess,urllib.parse,json,re,tempfile,os
P=pathlib.Path(__file__).parent; BASE='https://www.hkmapservice.gov.hk/OneStopSystem/'
with tempfile.TemporaryDirectory(dir=P) as td:
 c=str(pathlib.Path(td)/'cookies');pathlib.Path(c).touch(mode=0o600)
 def req(url,data=None,headers=[]):
  cmd=['curl','-fLsS','--max-time','60','-b',c,'-c',c]
  for h in headers: cmd+=['-H',h]
  if data is not None:cmd+=['--data',urllib.parse.urlencode(data)]
  return subprocess.run(cmd+[url],capture_output=True,check=True).stdout
 page=req(BASE+'map-search?product=OSSCatA').decode()
 token=re.search(r'<meta name="_csrf" content="([^"]+)"',page).group(1)
 header=re.search(r'<meta name="_csrf_header" content="([^"]+)"',page).group(1)
 items=[{'itemId':'DAP-L0','photoNo':'A36143','shtName':'A36143','prodFormat':'JPEG','quantity':'1'}]
 r=json.loads(req(BASE+'downloadList/addItem?'+urllib.parse.urlencode({'items':json.dumps(items)})));d=json.loads(r['data']);print({k:v for k,v in d.items() if k not in ['downloadListId','downloadItemId']})
 if d.get('isAdd') or d.get('hasAddedItem'):
  r=json.loads(req(BASE+'downloadList/getDownloadLink',{'downloadListId':d['downloadListId'],'downloadItemId':d['downloadItemId']},[header+': '+token]));d=json.loads(r['data']);u=d.get('downloadLink')
  if u:
   if u.startswith('/'):u='https://www.hkmapservice.gov.hk'+u
   b=req(u+'&locale=en');(P/'A36143_l0_download_page.html').write_bytes(b);print('download_page',len(b))
