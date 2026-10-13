import pathlib,json,csv,datetime,subprocess,hashlib,concurrent.futures,re
P=pathlib.Path(__file__).parent;fs=json.loads((P/'aerial_footprints_1985_1998.geojson').read_text())['features']
points={'checkerboard':(114.185,22.337),'walled_city':(114.1904,22.332),'threshold':(114.201,22.326),'runway':(114.216,22.311)}
def pointin(pt,r):
 x,y=pt;b=False
 for (x1,y1),(x2,y2) in zip(r,r[1:]+r[:1]):
  if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:b=not b
 return b
rows=[];chosen={}
for name,pt in points.items():
 for year in range(1985,1999):
  a=[f['properties'] for f in fs if f['properties']['YEARFLIGHT']==year and f['properties']['OBLIQUE']==0 and pointin(pt,f['geometry']['coordinates'][0])]
  target=datetime.datetime(year,11,4,tzinfo=datetime.timezone.utc).timestamp()*1000
  a.sort(key=lambda x:(abs(x['DATEFLIGHT']-target),x['PHOTOSCALE']))
  for rank,f in enumerate(a):
   rows.append(dict(site=name,site_lon=pt[0],site_lat=pt[1],rank_in_year=rank+1,**f))
  for f in a[:3 if year==1993 else 1]:chosen[f['PHOTONO']]=f
with (P/'landmark_frame_matches.csv').open('w') as o:
 w=csv.DictWriter(o,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'previews').mkdir(exist_ok=True)
def download(f):
 product_id=re.sub(r'([A-Z]+)([0-9]+)$',lambda m:m[1]+m[2].zfill(5),f['PHOTONO'])
 u='https://www.hkmapservice.gov.hk/OneStopSystem/map-search/getPreviewFile?itemId=DAP&sheetNo='+product_id; p=P/'previews'/(f['PHOTONO']+'.jpg')
 r=subprocess.run(['curl','-fLsS','--max-time','60',u],capture_output=True)
 if r.returncode or not r.stdout.startswith(b'\xff\xd8'):return dict(frame_id=f['PHOTONO'],product_id=product_id,status='failed',url=u)
 p.write_bytes(r.stdout)
 return dict(frame_id=f['PHOTONO'],product_id=product_id,capture_date=f['capture_date_utc'][:10],url=u,path=str(p.relative_to(P)),bytes=len(r.stdout),sha256=hashlib.sha256(r.stdout).hexdigest(),status='downloaded_preview_not_full_resolution',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(download,chosen.values()))
(P/'preview_manifest.json').write_text(json.dumps(results,indent=2));print('downloaded',sum(x['status'].startswith('downloaded') for x in results),'of',len(results),flush=True)
