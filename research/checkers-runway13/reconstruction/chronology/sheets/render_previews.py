from pathlib import Path
import zipfile,json
import numpy as np
import rasterio
from rasterio.enums import Resampling
from PIL import Image
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'previews';OUT.mkdir(exist_ok=True)
records=[]
for receipt in sorted((ROOT/'maps').glob('*.json')):
 d=json.loads(receipt.read_text())
 if d.get('status')!='validated_zip':continue
 if d['sheet'] not in {'11-NE-11A','11-NW-10D','11-NE-16B','11-NE-17C','11-NW-15B','11-NE-11C','11-NE-16A'}:continue
 path=ROOT/d['file'];out=OUT/(path.stem+'.png')
 with zipfile.ZipFile(path) as z:n=next(n for n in z.namelist() if n.lower().endswith(('.tif','.tiff')))
 with rasterio.open('/vsizip/'+str(path.resolve())+'/'+n) as ds:
  scale=min(1,2200/ds.width);a=ds.read(out_shape=(ds.count,int(ds.height*scale),int(ds.width*scale)),resampling=Resampling.average)
  if not out.exists():
   if ds.count==1:
    try:
     pal=ds.colormap(1);lut=np.array([pal.get(i,(i,i,i,255))[:3] for i in range(256)],dtype=np.uint8);im=Image.fromarray(lut[a[0]])
    except ValueError:im=Image.fromarray(a[0])
   else:im=Image.fromarray(np.moveaxis(a[:3],0,2))
   im.save(out)
  records.append({'source_id':d['source_id'],'preview':str(out.relative_to(ROOT)),'width':ds.width,'height':ds.height,'bounds':list(ds.bounds),'crs_in_file':str(ds.crs),'crs_from_source':'EPSG:2326','source_tiff':n})
(OUT/'index.json').write_text(json.dumps(records,indent=2));print(len(records),'previews')
