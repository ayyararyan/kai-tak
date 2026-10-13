from pathlib import Path
import json,zipfile,io
import numpy as np
import rasterio
from rasterio.warp import reproject,Resampling
from rasterio.transform import from_origin
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'integrated/geometry';Image.MAX_IMAGE_PIXELS=200000000
rows=json.loads((ROOT/'reconstruction/block_matching/registered/sheet_registration_inventory.json').read_text())['records']
trans=from_origin(837500,821000,.5,.5);canvas=np.full((2400,3000),240,dtype='uint8')
for id in ['695','702','821','830']:
 r=next(x for x in rows if x['source_id']=='1980_1990:'+id)
 with zipfile.ZipFile(ROOT/r['source_archive']) as z:im=Image.open(io.BytesIO(z.read(r['tiff_member']))).convert('L');src=np.array(im)
 dst=np.full_like(canvas,255)
 reproject(src,dst,src_transform=rasterio.Affine(*r['affine_pixel_edges']),src_crs='EPSG:2326',dst_transform=trans,dst_crs='EPSG:2326',resampling=Resampling.min,dst_nodata=255)
 b=r['index_core_bounds_epsg2326'];x0=int((b[0]-837500)/.5);x1=int((b[2]-837500)/.5);y0=int((821000-b[3])/.5);y1=int((821000-b[1])/.5)
 canvas[y0:y1,x0:x1]=dst[y0:y1,x0:x1]
Image.fromarray(canvas).save(OUT/'runway_registration_map.png')
a=json.loads((ROOT/'reconstruction/block_matching/aerial_registration/registration.json').read_text())['coefficients_pixel_xy1_to_EN'];src=np.array(Image.open(ROOT/'reconstruction/chronology/aerial/fullframes/A36143.jpg').convert('L'));dst=np.full_like(canvas,255)
reproject(src,dst,src_transform=rasterio.Affine(a[0][0],a[1][0],a[2][0],a[0][1],a[1][1],a[2][1]),src_crs='EPSG:2326',dst_transform=trans,dst_crs='EPSG:2326',resampling=Resampling.bilinear,dst_nodata=255)
Image.fromarray(dst).save(OUT/'runway_photo_diagnostic.png')
for name in ['runway_registration_map','runway_photo_diagnostic']:
 im=Image.open(OUT/(name+'.png'));im.resize((1500,1200)).save(OUT/(name+'_view.png'))
print('Diagnostic only; extrapolated old affine for landmark selection, not accepted registration.')
