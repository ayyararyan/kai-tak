from pathlib import Path
import csv,json,hashlib
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from PIL import Image,ImageDraw
from pyproj import Transformer
HERE=Path(__file__).resolve().parent
rows=list(csv.DictReader((HERE/'control_points.csv').open()))
s=json.loads((HERE/'registration.json').read_text())
# Monotone chain on measured reference controls, no frame-index footprint.
pts=sorted(set((float(r['easting']),float(r['northing'])) for r in rows))
def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
lo=[];hi=[]
for p in pts:
 while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
 lo.append(p)
for p in reversed(pts):
 while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
 hi.append(p)
hull=lo[:-1]+hi[:-1];hull.append(hull[0]);geom={'type':'Polygon','coordinates':[hull]}
with rasterio.open(HERE/'A36143_local_affine_diagnostic.tif','r+') as ds:
 mask=geometry_mask([geom],out_shape=(ds.height,ds.width),transform=ds.transform,invert=True)
 ds.write_mask(mask.astype('uint8')*255)
 s['support_mask_valid_pixels']=int(mask.sum());s['support_mask_total_pixels']=mask.size
 s['support_polygon_hk1980']=geom
tr=Transformer.from_crs(2326,4326,always_xy=True)
g={'type':'Polygon','coordinates':[[tr.transform(x,y) for x,y in hull]]}
(HERE/'local_control_support.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','geometry':g,'properties':{'status':'local_affine_diagnostic_only','historical_roof_height_valid':False,'planimetric_error_calibrated':False,'frame_id':'A36143','capture_date':'1993-11-02','holdout_rmse_m':s['metrics']['holdout']['rmse_m']}}]},indent=2)+'\n')
photo=Image.open(HERE/'A36143_northish_inspection.jpg').convert('RGB'); d=ImageDraw.Draw(photo)
for i,r in enumerate(rows,1):
 x=float(r['rotated1800_x']);y=float(r['rotated1800_y']);c='cyan' if r['role']=='holdout' else 'yellow'
 d.ellipse((x-5,y-5,x+5,y+5),outline=c,width=2);d.text((x+6,y-9),str(i),fill=c)
photo.crop((380,345,725,605)).resize((1035,780)).save(HERE/'picked_road_controls.png')
# Properly antialiased rendering of the reference map, display only.
import zipfile
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
zp=HERE.parents[1]/'chronology/sheets/maps/1980_1990_678_11-NE-11A_1989-10-01.zip'
with zipfile.ZipFile(zp) as zz:n=next(n for n in zz.namelist() if n.endswith('.tif'))
a=Image.open(HERE/'A36143_local_affine_diagnostic.png');W,H=a.size
with rasterio.open('/vsizip/'+str(zp)+'/'+n) as ds:
 ar=ds.read(1,window=from_bounds(*s['local_control_bbox_EN'],transform=ds.transform),out_shape=(H,W),resampling=Resampling.average)
b=Image.fromarray(ar).convert('RGB');b.save(HERE/'reference_local.png')
canvas=Image.new('RGB',(W*2,H+30),'white');canvas.paste(b,(0,30));canvas.paste(a,(W,30));d=ImageDraw.Draw(canvas);d.text((5,5),'1989 survey, official worldfile',fill='black');d.text((W+5,5),'1993 photo, local affine diagnostic',fill='black');canvas.save(HERE/'local_registration_comparison.png')
(HERE/'registration.json').write_text(json.dumps(s,indent=2)+'\n')
print('Validated source controls:',len(rows),'holdout',sum(r['role']=='holdout' for r in rows),'masked unsupported pixels',mask.size-int(mask.sum()))
