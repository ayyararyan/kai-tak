from pathlib import Path
import json,zipfile,hashlib,io
import numpy as np
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from rasterio.warp import reproject,Resampling
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'integrated/geometry';OUT.mkdir(exist_ok=True)
rows=json.loads((ROOT/'reconstruction/block_matching/registered/sheet_registration_inventory.json').read_text())['records']
latest={}
for r in rows:
 b=r['index_core_bounds_epsg2326']
 if r['edition_date']<'1993-11-01' and b[0]<840500 and b[2]>837500 and b[1]<821600 and b[3]>818000:
  if r['sheet'] not in latest or latest[r['sheet']]['edition_date']<r['edition_date']:latest[r['sheet']]=r
canvas=np.full((1800,1500),240,dtype='uint8'); trans=from_origin(837500,821600,2,2); manifest=[]
for r in latest.values():
 p=ROOT/r['source_archive'];sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if sha!=r['source_sha256']:raise ValueError('source changed')
 with zipfile.ZipFile(p) as z,MemoryFile(z.read(r['tiff_member'])) as mem,mem.open() as src:
  dst=np.full_like(canvas,255)
  with zipfile.ZipFile(p) as z:
   grey=np.array(Image.open(io.BytesIO(z.read(r['tiff_member']))).convert('L'))
  reproject(grey,dst,src_transform=rasterio.Affine(*r['affine_pixel_edges']),src_crs='EPSG:2326',dst_transform=trans,dst_crs='EPSG:2326',resampling=Resampling.average,dst_nodata=255)
  b=r['index_core_bounds_epsg2326'];x0=int((b[0]-837500)/2);x1=int((b[2]-837500)/2);y0=int((821600-b[3])/2);y1=int((821600-b[1])/2)
  canvas[y0:y1,x0:x1]=dst[y0:y1,x0:x1]
 manifest.append({k:r[k] for k in ['source_id','sheet','edition_date','source_archive','source_sha256','tiff_member','affine_pixel_edges','index_core_bounds_epsg2326']})
im=Image.fromarray(canvas).convert('RGB');d=ImageDraw.Draw(im)
for r in manifest:
 b=r['index_core_bounds_epsg2326'];x=int((b[0]-837500)/2);y=int((821600-b[3])/2);d.text((x+4,y+4),r['sheet']+' '+r['edition_date'][:7],fill='red')
im.save(OUT/'runway_map_mosaic.png')
(OUT/'map_mosaic_manifest.json').write_text(json.dumps({'pixel_edge_transform':[2,0,837500,0,-2,821600],'crs':'EPSG:2326','dates':'latest acquired edition strictly before November1993; not proof of query-date geometry','sources':manifest},indent=2)+'\n')
print(len(manifest),'sheets rendered')
