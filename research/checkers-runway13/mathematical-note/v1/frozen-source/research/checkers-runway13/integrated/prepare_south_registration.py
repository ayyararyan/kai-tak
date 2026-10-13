from pathlib import Path
import json,zipfile,io,numpy as np
from PIL import Image
from rasterio.warp import reproject,Resampling
from rasterio.transform import from_origin,Affine
R=Path(__file__).resolve().parents[1];O=R/'integrated/geometry';Image.MAX_IMAGE_PIXELS=200000000
rs=json.loads((R/'reconstruction/block_matching/registered/sheet_registration_inventory.json').read_text())['records']
trans=from_origin(839000,819800,1,1);canvas=np.full((1800,1500),240,dtype='uint8')
used=[]
for id in ['865','871','1002','1007','1011']:
 r=next(x for x in rs if x['source_id']=='1980_1990:'+id)
 with zipfile.ZipFile(R/r['source_archive']) as z:im=Image.open(io.BytesIO(z.read(r['tiff_member']))).convert('L');src=np.array(im)
 dst=np.full_like(canvas,255);reproject(src,dst,src_transform=Affine(*r['affine_pixel_edges']),src_crs='EPSG:2326',dst_transform=trans,dst_crs='EPSG:2326',resampling=Resampling.min,dst_nodata=255)
 b=r['index_core_bounds_epsg2326'];x0=int(b[0]-839000);x1=int(b[2]-839000);y0=int(819800-b[3]);y1=int(819800-b[1]);canvas[y0:y1,x0:x1]=dst[y0:y1,x0:x1];used.append(r)
Image.fromarray(canvas).save(O/'south_runway_map.png')
im=Image.open(R/'reconstruction/chronology/aerial/fullframes/A36172.jpg').transpose(Image.Transpose.ROTATE_270);im.save(O/'A36172_CW.png');im.resize((1500,1500)).save(O/'A36172_CW_view.png')
(O/'south_map_sources.json').write_text(json.dumps({'map_pixel_to_grid':[1,0,839000,0,-1,819800],'sources':used},indent=2)+'\n')
