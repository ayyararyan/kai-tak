"""Extract closed map interiors from explicitly inspected seed positions.
No automatic region is asserted a building until overlay review is recorded.
"""
import json,zipfile,hashlib,math
from pathlib import Path
import cv2,numpy as np,rasterio
from rasterio.enums import Resampling
from rasterio.features import shapes
from affine import Affine
from shapely.geometry import shape,mapping,Polygon
from shapely.ops import transform as geom_transform
from pyproj import Transformer
ROOT=Path(__file__).resolve().parent
SHEETS=ROOT.parent/'chronology/sheets'
SEEDS=[
('shing_tung','Shing Tung House',650,145),('mau_tung','Mau Tung House',686,282),
('on_tung','On Tung House',855,215),('hong_tung','Hong Tung House',1020,272),
('market_podium','Cooked food centre and market',841,133),
('block22','Tung Tau Block 22',876,411),('block23','Tung Tau Block 23',1070,371),
('lee_school','Lee Kau Yan Memorial School',1365,435),('ng_wah','Ng Wah College',1355,225),
('regal','Regal Airport Hotel',945,865),('po_sing','Po Sing Court',930,795),
('city_market','Kowloon City Market',130,950),('lok_sin_school','Lok Sin Tong Primary School',366,780),
('clinic','Clinic',356,872),('maternity','Maternity Home',130,815),('dispensary','Lee Kee Memorial Dispensary',135,782)
]

def read_map(source_id):
 records=json.loads((SHEETS/'map_downloads.json').read_text())
 r=next(r for r in records if r['source_id']==source_id)
 p=SHEETS/r['file']
 with zipfile.ZipFile(p) as z:n=next(n for n in z.namelist() if n.lower().endswith('.tif'))
 with rasterio.open('/vsizip/'+str(p)+'/'+n) as d:
  scale=.125/abs(d.transform.a);w=round(d.width/scale);h=round(d.height/scale)
  if d.count!=1 or d.colorinterp[0].name not in {'gray','undefined'} or d.nodata is not None:
   raise ValueError('This threshold extractor requires grayscale without nodata; palette/RGB/nodata need an explicit decoded reader')
  a=d.read(1,out_shape=(h,w),resampling=Resampling.average)
  trans=d.transform*Affine.scale(d.width/w,d.height/h)
 return a,trans,r

def extract(a,trans,x,y):
 col,row=(~trans)*(x,y);col,row=math.floor(col),math.floor(row)
 white=(a>180).astype('uint8')
 # no gap-closing that might alter narrow historical outlines
 if not (0<=row<a.shape[0] and 0<=col<a.shape[1]) or not white[row,col]:return None,{'error':'seed_on_ink_or_outside'}
 mask=np.zeros((a.shape[0]+2,a.shape[1]+2),np.uint8)
 count,_,mask,rect=cv2.floodFill(white,mask,(col,row),2,flags=4|cv2.FLOODFILL_MASK_ONLY|(255<<8))
 if count*abs(trans.a*trans.e)>20000:return None,{'error':'open_or_excessive_region','area_m2':count*abs(trans.a*trans.e)}
 if count*abs(trans.a*trans.e)<15:return None,{'error':'text_or_small_region','area_m2':count*abs(trans.a*trans.e)}
 rx,ry,rw,rh=rect
 sub=mask[1+ry:1+ry+rh,1+rx:1+rx+rw]
 found=list(shapes(sub,mask=sub>0,transform=trans*Affine.translation(rx,ry)))
 g=max((shape(g) for g,v in found),key=lambda g:g.area)
 # Interior text/labels are ink holes, not inferred open courtyards.
 # Keep original region for audit, outer envelope is only a candidate building face.
 if g.geom_type!='Polygon':return None,{'error':'nonpolygon'}
 g=Polygon(g.exterior).simplify(.18,preserve_topology=True)
 return g,{'seed_e':x,'seed_n':y,'interior_holes_removed':len(max((shape(g) for g,v in found),key=lambda g:g.area).interiors),'area_m2':g.area,'geometry_valid':g.is_valid}

def main():
 a,t,r=read_map('1980_1990:678');pix_to_world=t*Affine.scale(a.shape[1]/1664,a.shape[0]/1485)
 seeds=[(i,n,* (pix_to_world*(x,y))) for i,n,x,y in SEEDS]
 features=[];attempts=[]
 for sid in ['1980_1990:678','1980_1990:679','1980_1990:680']:
  a,t,r=read_map(sid)
  for i,n,x,y in seeds:
   g,meta=extract(a,t,x,y);meta.update(id=i,source_id=sid,name=n)
   attempts.append(meta)
   if g is None:continue
   features.append({'type':'Feature','geometry':mapping(g),'properties':dict(meta,source_epoch=r['edition_date'][:7],source_sha256=r['sha256'],source_archive=r['file'],method='manual_seed_closed_ink_region_outer_envelope',historical_top_hkpd_m=None,historical_base_hkpd_m=None,height_status='unidentified',presence_at_1993_11_04='requires_temporal_corroboration',review_status='candidate_pending_overlay_review',geometry_role='historical_map_outline_candidate',crs='EPSG:2326',not_clearance_geometry=True)})
 (ROOT/'digitization_candidates_hk1980.geojson').write_text(json.dumps({'type':'FeatureCollection','crs':{'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::2326'}},'features':features},indent=2))
 (ROOT/'digitization_attempts.json').write_text(json.dumps(attempts,indent=2))
 print(json.dumps(attempts,indent=2))
if __name__=='__main__':main()
