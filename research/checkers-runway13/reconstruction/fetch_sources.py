import urllib.request,concurrent.futures,pathlib,json,hashlib,datetime,re,sys
p=pathlib.Path(__file__).parent
urls=json.loads(sys.argv[1])
def get(k,u):
 try:
  r=urllib.request.urlopen(u,timeout=25);b=r.read();ext='.pdf' if b.startswith(b'%PDF') else '.html';f=p/'downloads'/f'{k}{ext}';f.write_bytes(b)
  return dict(id=k,url=u,final_url=r.url,status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),file=str(f),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(id=k,url=u,error=str(e))
rows=list(concurrent.futures.ThreadPoolExecutor(6).map(lambda x:get(*x),urls.items()));old=json.loads((p/'retrievals.json').read_text());(p/'retrievals.json').write_text(json.dumps(old+rows,indent=2));print(json.dumps(rows,indent=2))
for row in rows:
 if row.get('status')==200 and row['file'].endswith('.html'):
  s=pathlib.Path(row['file']).read_text(errors='replace');clean=re.sub('<script.*?</script>|<style.*?</style>','',s,flags=re.S);clean=re.sub('<[^>]+>',' ',clean);clean=re.sub(r'\s+',' ',clean);print('\nPAGE',row['id'],clean[clean.find('Mapping Services and Products')+28:] if 'Mapping Services and Products' in clean else clean[:22000]);print('LINKS',re.findall(r'(?:href|src)=[\"\x27]([^\"\x27]+)',s)[-70:])
