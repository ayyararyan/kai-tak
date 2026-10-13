### ADDED digitize.py
```python
"""Extract closed map interiors from explicitly inspected seed positions.
No automatic region is asserted a building until overlay review is recorded.
"""
import json,zipfile,hashlib
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
  a=d.read(1,out_shape=(h,w),resampling=Resampling.average)
  trans=d.transform*Affine.scale(d.width/w,d.height/h)
 return a,trans,r

def extract(a,trans,x,y):
 col,row=(~trans)*(x,y);col,row=round(col),round(row)
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

```

### ADDED accept_geometry.py
```python
"""Parent's explicit visual decisions, then reproducible geometry/identity joins."""
from pathlib import Path
import json,csv,hashlib
from collections import defaultdict
from shapely.geometry import shape,mapping,box
from shapely.ops import transform,unary_union
from shapely.strtree import STRtree
from pyproj import Transformer
R=Path(__file__).resolve().parent
PROJ=R.parent.parent
TOHK=Transformer.from_crs(4326,2326,always_xy=True).transform
TOWGS=Transformer.from_crs(2326,4326,always_xy=True).transform

def fc(fs,projected=False):
 d={'type':'FeatureCollection','features':fs}
 if projected:d['crs']={'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::2326'}}
 return d

def main():
 fs=json.loads((R/'digitization_candidates_hk1980.geojson').read_text())['features']
 accepted=[];decisions=[]
 for f in fs:
  p=f['properties'];i=p['id']
  if i=='clinic':
   decisions.append({'id':i,'source':p['source_id'],'decision':'reject','reason':'seed selected a small adjoining map subdivision, not the labelled clinic outline'});continue
  note='Parent visually inspected extracted exterior against the registered source overlay; agreement as a depicted building face, not a surveyed historical roof mesh.'
  if i=='lok_sin_school':note+=' Partial mapped face; north portion gains crossed/dashed symbol in 1994/1997, interpretation unresolved. Do not infer unchanged physical state.'
  if i=='market_podium':note+=' Mapped market face adjoining On Tung complex; distinct cartographic face, not necessarily an independent building.'
  if i=='ng_wah':note+=' Combined mapped school form, not a modern one-to-one structure identity.'
  p.update(review_status='visually_checked_map_face',geometry_role='historical_depicted_building_face',review_note=note,full_structure_mesh=False,review_evidence=f'digitization_overlay_{p["source_epoch"]}.png')
  accepted.append(f);decisions.append({'id':i,'source':p['source_id'],'decision':'accept_depicted_face','note':note})
 # Current features may be multiple vertically stacked parts of the same footprint.
 current=json.loads((PROJ/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson').read_text())['features']
 pairs=[]
 for f in current:
  g=transform(TOHK,shape(f['geometry']))
  if g.is_valid and g.intersects(box(837500,821000,838250,821600)):pairs.append((g,f))
 tree=STRtree([g for g,f in pairs]);modern_joins=[]
 for f in accepted:
  g=shape(f['geometry']);joins=[]
  for idx in tree.query(g):
   c,m=pairs[idx];inter=g.intersection(c).area
   if inter/max(1,min(g.area,c.area))<.35:continue
   iou=inter/g.union(c).area;props=m['properties']
   joins.append({'csuid':props['BuildingCSUID'],'name':props.get('BuildingNameEN'),'geometry_iou':iou,'historical_face_fraction':inter/g.area,'modern_fraction':inter/c.area,'modern_top_hkpd_m':props.get('TopHeight'),'modern_base_hkpd_m':props.get('BaseHeight'),'height_epoch':'2026-09-21','height_transfer_to_historical':False,'identity_status':'spatial_correspondence_candidate'})
  joins.sort(key=lambda j:j['geometry_iou'],reverse=True)
  f['properties']['modern_correspondences']=joins
  modern_joins.extend({'historical_id':f['properties']['id'],'map_epoch':f['properties']['source_epoch'],**j} for j in joins)
 (R/'historical_faces_hk1980.geojson').write_text(json.dumps(fc(accepted,True),indent=2))
 wgs=[]
 for f in accepted:wgs.append({'type':'Feature','geometry':mapping(transform(TOWGS,shape(f['geometry']))),'properties':f['properties']})
 (R/'historical_faces.geojson').write_text(json.dumps(fc(wgs),indent=2))
 # Cross-map correspondence identifies the depicted form, not day-specific survival.
 by=defaultdict(list)
 for f in accepted:by[f['properties']['id']].append(f)
 match=[]
 for i,group in by.items():
  base=next(f for f in group if f['properties']['source_epoch']=='1989-10');g=shape(base['geometry'])
  for f in group:
   h=shape(f['geometry']);match.append({'historical_id':i,'name':f['properties']['name'],'from_epoch':'1989-10','to_epoch':f['properties']['source_epoch'],'geometry_iou':g.intersection(h).area/g.union(h).area,'name_and_form_reviewed':True,'same_depicted_form':i!='lok_sin_school','continued_presence_every_day_verified':False,'historical_height_verified':False})
 (R/'structure_matches.json').write_text(json.dumps(match,indent=2))
 (R/'modern_correspondences.json').write_text(json.dumps(modern_joins,indent=2))
 (R/'manual_review_decisions.json').write_text(json.dumps({'reviewer':'parent direct image inspection','overlays_inspected':['1989-10','1994-07','1997-04'],'decisions':decisions,'prior_seed_corrections':['Dispensary seed initially traced its compound: rejected and re-picked inside actual labelled building.','Block 23 seed initially fell outside the E-shaped building: rejected and re-picked inside western spine.','Clinic subface rejected and not included in accepted layer.'],'count_accepted_source_faces':len(accepted),'count_named_forms':len(by)},indent=2))
 # Preserve full unknown coverage even where a horizontal face has been reviewed.
 mask=json.loads((R.parent/'chronology/historical_uncertainty_mask.geojson').read_text())
 for f in mask['features']:
  f['properties'].update(reason='Whole-area historical 3D completeness remains unresolved; reviewed 2D faces do not establish roof height or complete obstacle coverage.',historical_height_unknown=True,complete_historical_3d=False,physical_occupancy=None)
 (R/'historical_3d_unknown_mask.geojson').write_text(json.dumps(mask,indent=2))
 print('Accepted source faces',len(accepted),'named forms',len(by),'modern component joins',len(modern_joins))
if __name__=='__main__':main()

```

### ADDED register_sheets.py
```python
"""Audit official historical world files; resample selected sheet cores, never originals.

TFW pixel centres are converted to raster edge convention explicitly. Index polygons
provide cartographic core extents, not georeferencing. EPSG:2326 assignment follows
source Hong Kong 1980 Grid documentation and printed sheet legend. Output resolution
is a sampling choice, not an estimate of map, survey or ground accuracy.
"""
from pathlib import Path
import hashlib,json,math,zipfile
import numpy as np
import rasterio
from rasterio.transform import Affine,from_origin
from rasterio.warp import reproject,Resampling
from pyproj import Transformer
from PIL import Image

ROOT=Path(__file__).resolve().parent
SHEETS=ROOT.parent/'chronology/sheets'
OUT=ROOT/'registered'
SELECTED={'1980_1990:678','1980_1990:679','1980_1990:680'}

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def tfw_affine(text):
 a,d,b,e,c,f=map(float,text.split())
 if not all(math.isfinite(v) for v in (a,b,c,d,e,f)) or abs(a*e-b*d)<1e-15:
  raise ValueError('Invalid/singular world file')
 return Affine(a,b,c-(a+b)/2,d,e,f-(d+e)/2)

def core_bounds(feature):
 t=Transformer.from_crs(4326,2326,always_xy=True)
 xy=[t.transform(*p) for p in feature['geometry']['coordinates'][0]]
 raw=[min(p[0] for p in xy),min(p[1] for p in xy),max(p[0] for p in xy),max(p[1] for p in xy)]
 # Official sheet index coordinates round trip to an integral-metre grid. Round
 # only when the complete polygon is within 1 cm of integral-metre coordinates.
 snapped=all(abs(v-round(v))<.01 for p in xy for v in p)
 return ([round(v) for v in raw] if snapped else raw),raw,snapped

def audit_one(receipt,feature):
 p=SHEETS/receipt['file']
 with zipfile.ZipFile(p) as z:
  ts=[n for n in z.namelist() if n.lower().endswith(('.tif','.tiff'))]
  ws=[n for n in z.namelist() if n.lower().endswith('.tfw')]
  if len(ts)!=1 or len(ws)!=1:raise ValueError(f'Ambiguous/missing members: {p}')
  wtext=z.read(ws[0]).decode(); tr=tfw_affine(wtext)
  th=hashlib.sha256(z.read(ts[0])).hexdigest(); wh=hashlib.sha256(z.read(ws[0])).hexdigest()
  crc_bad=z.testzip()
 with rasterio.open('/vsizip/'+str(p.resolve())+'/'+ts[0]) as ds:
  bounds=list(rasterio.transform.array_bounds(ds.height,ds.width,tr))
  core,raw,snap=core_bounds(feature)
  err=max(abs(a-b) for a,b in zip(tr,ds.transform))
  margins=[core[0]-bounds[0],core[1]-bounds[1],bounds[2]-core[2],bounds[3]-core[3]]
  return dict(source_id=receipt['source_id'],sheet=receipt['sheet'],edition_date=receipt['edition_date'],date_precision='month',source_archive=str(p.relative_to(ROOT.parent.parent)),source_sha256=sha(p),receipt_sha256=receipt['sha256'],source_sha256_matches=sha(p)==receipt['sha256'],crc_ok=crc_bad is None,tiff_member=ts[0],tiff_sha256=th,tfw_member=ws[0],tfw_sha256=wh,tfw_text=wtext,crs='EPSG:2326',crs_in_tiff=str(ds.crs),crs_assignment_basis='Hong Kong 1980 Grid source documentation and printed sheet legend',affine_pixel_edges=list(tr)[:6],width=ds.width,height=ds.height,nominal_resolution_m=[math.hypot(tr.a,tr.d),math.hypot(tr.b,tr.e)],raster_bounds_epsg2326=bounds,index_core_bounds_epsg2326=core,index_reprojected_bounds_epsg2326=raw,index_integral_grid_snap=snap,index_snap_tolerance_m=.01,margins_west_south_east_north_m=margins,core_within_raster=all(x>=-.01 for x in margins),rasterio_tfw_max_coefficient_difference=err,metadata_checks_pass=crc_bad is None and err<1e-8 and all(x>=-.01 for x in margins),printed_grid_status='not_independently_checked',cartographic_ground_accuracy_m=None)

def render(record,res=.25):
 p=ROOT.parent.parent/record['source_archive']; tr=Affine(*record['affine_pixel_edges'])
 left,bottom,right,top=record['index_core_bounds_epsg2326']
 width=round((right-left)/res);height=round((top-bottom)/res)
 outtr=from_origin(left,top,res,res)
 with rasterio.open('/vsizip/'+str(p.resolve())+'/'+record['tiff_member']) as ds:
  # Decode palette BEFORE averaging: palette indices are not intensities.
  a=ds.read()
  if ds.count==1:
   try:
    cmap=ds.colormap(1);lut=np.array([cmap.get(i,(i,i,i,255))[:3] for i in range(256)],dtype=np.uint8)
    rgb=np.moveaxis(lut[a[0]],2,0)
   except ValueError:rgb=np.repeat(a,3,axis=0)
  else:rgb=a[:3]
  output=np.full((3,height,width),255,np.uint8)
  for k in range(3):
   reproject(rgb[k],output[k],src_transform=tr,src_crs='EPSG:2326',dst_transform=outtr,dst_crs='EPSG:2326',resampling=Resampling.average)
 stem=record['sheet']+'_'+record['edition_date'][:7]+'_core'
 tif=OUT/(stem+'.tif');png=OUT/(stem+'.png')
 with rasterio.open(tif,'w',driver='GTiff',width=width,height=height,count=3,dtype='uint8',crs='EPSG:2326',transform=outtr,compress='deflate',tiled=True) as ds:
  ds.write(output)
  ds.update_tags(source_sha256=record['source_sha256'],accuracy='Sampling resolution is not cartographic accuracy',epoch=record['edition_date'][:7])
 Image.fromarray(np.moveaxis(output,0,2)).save(png)
 meta=dict(source_id=record['source_id'],source_sha256=record['source_sha256'],crs='EPSG:2326',bounds=[left,bottom,right,top],width=width,height=height,resolution_m=res,affine_pixel_edges=list(outtr)[:6],pixel_center_formula='E=left+(col+0.5)*resolution; N=top-(row+0.5)*resolution',pixel_edge_formula='E=left+col*resolution; N=top-row*resolution',source_date=record['edition_date'][:7],date_precision='month',resampling='area_average_after_palette_decode',tif_sha256=sha(tif),png_sha256=sha(png),cartographic_ground_accuracy_m=None)
 (OUT/(stem+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
 return meta

def main():
 OUT.mkdir(exist_ok=True)
 features=json.loads((SHEETS/'aoi_sheet_index.geojson').read_text())['features']
 index={f['properties']['source_id']:f for f in features}
 records=[];renders=[]
 for receipt in sorted((SHEETS/'maps').glob('*.json')):
  r=json.loads(receipt.read_text())
  if r.get('status')!='validated_zip':continue
  a=audit_one(r,index[r['source_id']]);records.append(a)
  if a['source_id'] in SELECTED:renders.append(render(a))
 result=dict(schema_version=1,total=len(records),metadata_pass=sum(r['metadata_checks_pass'] and r['source_sha256_matches'] for r in records),crs='EPSG:2326',records=records,rendered=renders,limitations=['Metadata audit is not independent printed-grid or ground-accuracy verification.','Cartographic sheet dates are month-precision, not a date of survey for each object.','Margins outside official core contain legend and other non-geographic material.'])
 (OUT/'sheet_registration_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'total':result['total'],'metadata_pass':result['metadata_pass'],'rendered':[m['source_id'] for m in renders]}))

# Manual interpretation of the actual printed-grid crops on 2026-10-13.
# Seeds locate visible dotted-grid crossings, not source TFW projected positions.
# Source 678 has finer lines; 679/680 have thicker scan strokes. Dark-pixel
# projection in a 9 px strip refines the manually recognized line centre.
MANUAL_GRID_SEEDS={
 '1980_1990:678':[(174,180),(177,180),(178,180),(169,180)],
 '1980_1990:679':[(182,182),(182,182),(182,181),(180,181)],
 '1980_1990:680':[(182,182),(184,183),(184,183),(174,180)],
}
GRID_POINTS=[(837600,821500),(837700,821500),(837700,821400),(838000,821100)]

def check_printed_grids():
 from PIL import ImageDraw
 from rasterio.windows import Window
 inv=json.loads((OUT/'sheet_registration_inventory.json').read_text());checks=[]
 for rec in inv['records']:
  if rec['source_id'] not in MANUAL_GRID_SEEDS:continue
  seeds=MANUAL_GRID_SEEDS[rec['source_id']];id=rec['source_id'].split(':')[1]
  p=ROOT.parent.parent/rec['source_archive'];tr=Affine(*rec['affine_pixel_edges'])
  contact=Image.new('RGB',(800,860),'white');draw=ImageDraw.Draw(contact)
  rows=[]
  with rasterio.open('/vsizip/'+str(p.resolve())+'/'+rec['tiff_member']) as ds:
   for j,((e,n),(sx,sy)) in enumerate(zip(GRID_POINTS,seeds)):
    pc,pr=(~tr)*(e,n);left=round(pc)-180;top=round(pr)-180
    a=ds.read(1,window=Window(left,top,360,360))
    try:
     pal=ds.colormap(1);lut=np.array([pal.get(i,(i,i,i,255))[:3] for i in range(256)],dtype=np.uint8);rgb=lut[a]
    except ValueError:rgb=np.repeat(a[:,:,None],3,axis=2)
    bx=(j%2)*400;by=(j//2)*430
    contact.paste(Image.fromarray(rgb),(bx,by+45));draw.text((bx,by),f'{id} E{e} N{n}\nraw origin col={left}, row={top}',fill='black')
    dark=rgb.mean(axis=2)<128;cx=dark.sum(axis=0);cy=dark.sum(axis=1)
    xs=np.arange(sx-4,sx+5);ys=np.arange(sy-4,sy+5)
    col=float((xs*cx[xs]).sum()/cx[xs].sum()+.5+left)
    row=float((ys*cy[ys]).sum()/cy[ys].sum()+.5+top)
    oe,on=tr*(col,row);de=oe-e;dn=on-n
    rows.append(dict(grid_e=e,grid_n=n,crop_origin_col=left,crop_origin_row=top,manual_seed_local_col=sx,manual_seed_local_row=sy,observed_source_edge_col=col,observed_source_edge_row=row,expected_source_edge_col=pc,expected_source_edge_row=pr,observed_e=oe,observed_n=on,residual_e_m=de,residual_n_m=dn,residual_distance_m=math.hypot(de,dn),reading_uncertainty_pixels=2.0))
  contact.save(OUT/f'grid_crops_{id}.png')
  (OUT/f'grid_crops_{id}.json').write_text(json.dumps(rows,indent=2)+'\n')
  metrics=dict(source_id=rec['source_id'],method='Manually identified visible 100m dotted printed-grid crossings; independently read source pixel locations, dark projection centroids within manually identified 9px strips. No fitted correction applied.',point_count=len(rows),rms_2d_m=math.sqrt(sum(r['residual_distance_m']**2 for r in rows)/len(rows)),max_2d_m=max(r['residual_distance_m'] for r in rows),points=rows,image=f'grid_crops_{id}.png',interpretation='Scan/world-file agreement with printed cartographic grid only, not ground-control accuracy or survey accuracy.',cartographic_ground_accuracy_m=None)
  checks.append(metrics);rec['printed_grid_status']='four_visible_crossings_measured';rec['printed_grid_rms_m']=metrics['rms_2d_m'];rec['printed_grid_max_m']=metrics['max_2d_m']
 inv['printed_grid_checks']=checks
 (OUT/'sheet_registration_inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
 (OUT/'printed_grid_validation.json').write_text(json.dumps(dict(method='independent printed-grid inspection; no fitted transform',checks=checks,physical_ground_accuracy_established=False),indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ('source_id','rms_2d_m','max_2d_m')} for r in checks]))

if __name__=='__main__':
 main()
 check_printed_grids()

```

### ADDED candidates/extract_candidates.py
```python
#!/usr/bin/env python3
"""Reproducible image-content screening; never historical identity certification."""
import argparse, calendar, csv, hashlib, json, math, zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np
import rasterio
from affine import Affine
from PIL import Image, ImageDraw
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.features import rasterize
from shapely.geometry import shape, mapping, box, Polygon, MultiPolygon
from shapely import make_valid, transform as _transform
from shapely.strtree import STRtree

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
MAPS=HERE.parents[1]/'chronology/sheets/maps'
MODERN=PROJECT/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson'
TO_HK=Transformer.from_crs(4326,2326,always_xy=True).transform
TO_LL=Transformer.from_crs(2326,4326,always_xy=True).transform
RESOLUTION=.25

def geom_transform(fn,g):
    return _transform(g,fn,interleaved=False)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump_geo(path,features):
    path.write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':')))

def boundary_samples(poly,step=.5):
    lines=[p.exterior for p in (poly.geoms if isinstance(poly,MultiPolygon) else [poly]) if isinstance(p,Polygon)]
    return np.array([(q.x,q.y) for line in lines for q in [line.interpolate(d) for d in np.arange(0,line.length,step)]])

def read_map(meta):
    path=MAPS/Path(meta['file']).name
    with zipfile.ZipFile(path) as z:
        tif=next(n for n in z.namelist() if n.lower().endswith('.tif'))
        tfw=next(n for n in z.namelist() if n.lower().endswith('.tfw'))
        a,d,b,e,c,f=map(float,z.read(tfw).decode().split())
    native=Affine(a,b,c-.5*a-.5*b,d,e,f-.5*d-.5*e)
    with rasterio.open('/vsizip/'+str(path)+'/'+tif) as ds:
        h=math.ceil(ds.height*abs(e)/RESOLUTION); w=math.ceil(ds.width*abs(a)/RESOLUTION)
        arr=ds.read(1,out_shape=(h,w),resampling=Resampling.average)
        tf=native*Affine.scale(ds.width/w,ds.height/h)
    return arr,tf,path,tfw

def analyse(meta,features,geoms,tree):
    key=f"{meta['sheet']}_{meta['edition_date'][:7]}"
    out=HERE/key;out.mkdir(exist_ok=True)
    gray,tf,source,tfw=read_map(meta)
    # Index rectangle clips margins only; it is NOT used as image registration.
    coverage=geom_transform(TO_HK,box(meta['minlon'],meta['minlat'],meta['maxlon'],meta['maxlat']))
    valid=rasterize([(coverage,1)],out_shape=gray.shape,transform=tf,dtype='uint8')>0
    ink=(gray<200).astype('uint8')
    dist=cv2.distanceTransform(1-ink,cv2.DIST_L2,cv2.DIST_MASK_PRECISE)*abs(tf.a)
    # No artificial closing: gaps remain gaps and can reject a real structure.
    n,labels,stats,cents=cv2.connectedComponentsWithStats(((1-ink)*valid).astype('uint8'),8)
    coverage_edge=valid & (cv2.dilate((~valid).astype('uint8'),np.ones((3,3),dtype='uint8'))>0)
    coverage_edge_labels=set(map(int,np.unique(labels[coverage_edge])))
    areas=stats[:,cv2.CC_STAT_AREA]*abs(tf.a*tf.e)
    eligible=(areas>=12)&(areas<=25000);eligible[0]=False
    region_ids=np.flatnonzero(eligible)
    inv=~tf; rows=[];candidate_features=[];used=Counter()
    for idx in tree.query(coverage):
        original=geoms[idx];p=original
        props=features[idx]['properties']
        ident=props['BuildingCSUID']
        repaired=not p.is_valid
        if repaired:p=make_valid(p)
        if not isinstance(p,(Polygon,MultiPolygon)):
            continue
        if not coverage.covers(p):
            clipped=True
        else:clipped=False
        xy=boundary_samples(p)
        if not len(xy):continue
        ij=np.array([inv*(x,y) for x,y in xy]);cols=np.floor(ij[:,0]).astype(int);rr=np.floor(ij[:,1]).astype(int)
        ok=(rr>=0)&(rr<gray.shape[0])&(cols>=0)&(cols<gray.shape[1])
        dv=dist[rr[ok],cols[ok]]
        if not len(dv):continue
        left,bottom,right,top=p.bounds
        c0,r0=inv*(left,top);c1,r1=inv*(right,bottom)
        c0=max(0,int(c0)-1);r0=max(0,int(r0)-1);c1=min(gray.shape[1],math.ceil(c1)+1);r1=min(gray.shape[0],math.ceil(r1)+1)
        mask=rasterize([(p,1)],out_shape=(r1-r0,c1-c0),transform=tf*Affine.translation(c0,r0),dtype='uint8')>0
        labs=labels[r0:r1,c0:c1][mask];ids,count=np.unique(labs,return_counts=True)
        possible=[(int(i),int(k)) for i,k in zip(ids,count) if eligible[i]]
        best_id=None;best_iou=0.;overlap=0
        for i,k in possible:
            iou=k/(mask.sum()+stats[i,cv2.CC_STAT_AREA]-k)
            if iou>best_iou:best_id,best_iou,overlap=i,float(iou),k
        support=float(np.mean(dv<=1.5));score=.65*support+.35*best_iou
        if clipped:status='edge_clipped_review'
        elif support>=.75 and best_iou>=.50:status='strong_content_candidate_unverified'
        elif support>=.5 or best_iou>=.25:status='ambiguous_content_candidate'
        else:status='low_support_rejected_by_screen'
        if best_id is not None and best_iou>=.25:used[best_id]+=1
        pt=p.representative_point();work=f"{meta['sheet']}_E{int(pt.x//200)*200}_N{int(pt.y//200)*200}"
        y,m=map(int,meta['edition_date'][:7].split('-'))
        row=dict(candidate_id=key+'__'+str(ident),modern_csuid=ident,modern_name=props.get('BuildingNameEN'),modern_epoch='2026-09-21',sheet=meta['sheet'],source_id=meta['source_id'],edition_month=meta['edition_date'][:7],edition_date_min=f'{y}-{m:02}-01',edition_date_max=f'{y}-{m:02}-{calendar.monthrange(y,m)[1]}',source_sha256=meta['sha256'],review_work_unit=work,work_unit_type='200m_grid_review_unit_not_street_block',status=status,rank_score=round(score,6),boundary_within_075m=float(np.mean(dv<=.75)),boundary_within_15m=support,boundary_within_3m=float(np.mean(dv<=3)),boundary_distance_median_m=float(np.median(dv)),boundary_distance_p95_m=float(np.percentile(dv,95)),best_region_id=best_id,best_region_iou=best_iou,modern_area_m2=p.area,region_area_m2=float(areas[best_id]) if best_id is not None else None,interior_ink_fraction=float(ink[r0:r1,c0:c1][mask].mean()),edge_clipped=clipped,derived_geometry_repaired=repaired,historical_geometry_verified=False,historical_identity_verified=False,historical_presence_on_query_date=None,historical_roof_elevation_m=None,geometry_role='modern_outline_matching_template_not_historical_footprint')
        rows.append(row);candidate_features.append({'type':'Feature','geometry':mapping(geom_transform(TO_LL,p)),'properties':row})
    rows.sort(key=lambda r:r['rank_score'],reverse=True)
    for rank,row in enumerate(rows,1):row['rank_in_sheet']=rank
    with (out/'ranked_candidates.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['candidate_id']);writer.writeheader();writer.writerows(rows)
    dump_geo(out/'ranked_candidates.geojson',candidate_features)
    regions=[]
    for i in region_ids:
        x,y,w,h,px=map(int,stats[i]);mask=(labels[y:y+h,x:x+w]==i).astype('uint8')
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        polys=[]
        for contour in contours:
            if len(contour)<3:continue
            coords=[tf*(float(q[0][0]+x)+.5,float(q[0][1]+y)+.5) for q in contour]
            p=Polygon(coords)
            if not p.is_valid:p=make_valid(p)
            if isinstance(p,Polygon) and p.area>=10:polys.append(p.simplify(.25,preserve_topology=True))
        if not polys:continue
        p=polys[0] if len(polys)==1 else MultiPolygon(polys)
        regions.append({'type':'Feature','geometry':mapping(geom_transform(TO_LL,p)),'properties':dict(region_id=int(i),sheet=meta['sheet'],edition_month=meta['edition_date'][:7],source_sha256=meta['sha256'],classification='unclassified_closed_map_region_not_verified_building',screened_modern_matches=used[int(i)],status='no_modern_correspondence_above_iou_025' if not used[int(i)] else 'modern_correspondence_candidate',pixel_area_m2=float(areas[i]),touches_clipped_coverage_boundary=int(i) in coverage_edge_labels,historical_roof_elevation_m=None,geometry_method='white_connected_component_no_gap_closing_external_contour',caveat='May be building, road, garden, text, grid or map omission. Pixel interior excludes ink; external contour fills interior ink holes. Not a historic building census.' )})
    dump_geo(out/'map_regions.geojson',regions)
    # Audit contact sheet includes strong, middle and low score cases, not only successes.
    sample=rows[:12]+rows[len(rows)//2:len(rows)//2+6]+rows[-6:]
    canvas=Image.new('RGB',(1400,max(1,math.ceil(len(sample)/4))*310),'#efefeb');draw=ImageDraw.Draw(canvas)
    if not sample:draw.text((20,20),'No current building templates overlap this source sheet. Historical map regions remain unresolved.',fill='#222222')
    feature_lookup={f['properties']['candidate_id']:f for f in candidate_features}
    for j,row in enumerate(sample):
        p=geom_transform(TO_HK,shape(feature_lookup[row['candidate_id']]['geometry']));b=p.bounds
        pad=max(8.,(b[2]-b[0]+b[3]-b[1])*.08);x0,y0=inv*(b[0]-pad,b[3]+pad);x1,y1=inv*(b[2]+pad,b[1]-pad)
        x0=max(0,int(x0));y0=max(0,int(y0));x1=min(gray.shape[1],math.ceil(x1));y1=min(gray.shape[0],math.ceil(y1))
        crop=Image.fromarray(gray[y0:y1,x0:x1]).convert('RGB');cd=ImageDraw.Draw(crop)
        for pp in (p.geoms if isinstance(p,MultiPolygon) else [p]):
            coords=[(float((inv*(x,y))[0]-x0),float((inv*(x,y))[1]-y0)) for x,y in pp.exterior.coords]
            cd.line(coords,fill='#d04429',width=3)
        crop.thumbnail((340,250));cx=(j%4)*350;cy=(j//4)*310;canvas.paste(crop,(cx,cy))
        draw.text((cx+3,cy+252),f"rank {row['rank_in_sheet']} {row['modern_csuid']}\nink {row['boundary_within_15m']:.2f}; IoU {row['best_region_iou']:.2f}\n{str(row['modern_name'] or '')[:42]}",fill='#222222')
    canvas.save(out/'audit_contact_sheet.jpg',quality=92)
    summary=dict(key=key,source=str(source.relative_to(PROJECT)),source_sha256=sha(source),tfw_member=tfw,affine=list(tf)[:6],crs='EPSG:2326 assigned from official survey grid; independent checks in parent registration report',sampling_resolution_m=[abs(tf.a),abs(tf.e)],candidates=len(rows),counts=dict(Counter(r['status'] for r in rows)),map_regions=len(regions),map_regions_without_candidate=sum(not f['properties']['screened_modern_matches'] for f in regions),verified_historical_buildings=0,limitations=['No visual identity acceptance performed by this extractor','Ink includes text, road and grid lines','Candidate rank is heuristic, not calibrated probability','Current feature universe misses vanished structures; closed map regions remain unclassified','No height transfer and no historical volume produced','Date is edition month, not object survey date','No registration adjustment estimated; world file used verbatim'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary),flush=True)
    return summary

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--core-pre1993',action='store_true');args=parser.parse_args()
    allmeta=[json.loads(p.read_text()) for p in MAPS.glob('*.json')]
    selected=[m for m in allmeta if m['sheet']=='11-NE-11A' and m['edition_date'][:7] in ['1989-10','1994-07']]
    if args.core_pre1993:
        latest={}
        for m in allmeta:
            if m.get('in_core') and m['edition_date']<'1993-11-01' and (m['sheet'] not in latest or m['edition_date']>latest[m['sheet']]['edition_date']):latest[m['sheet']]=m
        selected+=list(latest.values())
    selected={m['source_id']:m for m in selected}
    features=json.loads(MODERN.read_text())['features'];geoms=[geom_transform(TO_HK,shape(f['geometry'])) for f in features];tree=STRtree(geoms)
    summaries=[]
    for m in sorted(selected.values(),key=lambda m:(m['sheet'],m['edition_date'])):summaries.append(analyse(m,features,geoms,tree))
    (HERE/'run_summary.json').write_text(json.dumps(dict(generated_utc=datetime.now(timezone.utc).isoformat(),modern_source_sha256=sha(MODERN),script_sha256=sha(Path(__file__)),sheets=summaries,total_candidate_rows=sum(s['candidates'] for s in summaries),verified_historical_buildings=0),indent=2))

if __name__=='__main__':main()

```

### ADDED aerial_registration/build_sparse_stereo.py
```python
"""Measured sparse stereo, nominal camera / locally planar ground assumptions.
No manufactured roof labels, HKPD elevations, confidence limits or clearance claims.
"""
from pathlib import Path
import sys,json,csv,hashlib
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'python_deps'))
import cv2,numpy as np
from PIL import Image
raw=np.load(HERE/'stereo_tracks.npz');sel=raw['fmask'];p1=raw['p1'][sel];p2=raw['p2'][sel];F=raw['F']
rows=list(csv.DictReader((HERE/'control_points.csv').open()));q=np.array([[float(r['photo_x']),float(r['photo_y'])] for r in rows]);EN=np.array([[float(r['easting']),float(r['northing'])] for r in rows]);origin=EN.mean(0);Y=np.c_[EN-origin,np.zeros(len(rows))];fit=np.array([r['role']=='fit' for r in rows]);ground_fit=[788,1030,74,1187];ground_check=[708];roof=[26,1135]
def align(X,Y):
 mx=X.mean(0);my=Y.mean(0);xc=X-mx;yc=Y-my;U,S,V=np.linalg.svd(xc.T@yc);D=np.eye(3);D[-1,-1]=np.linalg.det(U@V);A=U@D@V;s=np.trace(np.diag(S)@D)/np.sum(xc**2);b=my-s*mx@A;return s,A,b

def solve(fmult=1.,cx=1460.,cy=1440.):
 f=152.12*300/25.4*fmult;K=np.array([[f,0,cx],[0,f,cy],[0,0,1.]])
 _,R,t,positive=cv2.recoverPose(K.T@F@K,p1,p2,K)
 P1=K@np.hstack([np.eye(3),np.zeros((3,1))]);P2=K@np.hstack([R,t]);T=cv2.triangulatePoints(P1,P2,p1.T,p2.T);X=(T[:3]/T[3]).T
 plane_center=X[ground_fit].mean(0);_,_,V=np.linalg.svd(X[ground_fit]-plane_center);normal=V[-1]
 C=(-R.T@t).ravel();rays=(R.T@np.linalg.inv(K)@np.c_[q,np.ones(len(q))].T).T
 lam=((plane_center-C)@normal)/(rays@normal);G=C+lam[:,None]*rays
 scale,A,b=align(G[fit],Y[fit]);world=scale*X@A+b+np.r_[origin,0]
 gcworld=scale*G@A+b+np.r_[origin,0];gcerr=gcworld-np.c_[EN,np.zeros(len(rows))]
 projected=[]
 for P in [P1,P2]:
  uv=(P@np.c_[X,np.ones(len(X))].T).T;projected.append(uv[:,:2]/uv[:,2,None])
 re=np.sqrt((np.sum((projected[0]-p1)**2,axis=1)+np.sum((projected[1]-p2)**2,axis=1))/2)
 return dict(K=K,R=R,t=t,P1=P1,P2=P2,X=X,world=world,scale=scale,A=A,b=b,plane_center=plane_center,plane_normal=normal,gcerr=gcerr,reprojection=re,positive=positive.ravel()>0,gcworld=gcworld,camera1_world=scale*np.zeros(3)@A+b+np.r_[origin,0],camera2_world=scale*C@A+b+np.r_[origin,0])
s=solve();world=s['world'];good=s['positive']&(s['reprojection']<5)&np.isfinite(world).all(1)
# Original GCP reference bounds indicate local support only, not a guarantee for all points therein.
reg=json.loads((HERE/'registration.json').read_text());hull=np.array(reg['support_polygon_hk1980']['coordinates'][0][:-1]);local=np.array([cv2.pointPolygonTest(hull.astype(np.float32),(float(x),float(y)),False)>=0 for x,y in world[:,:2]])
# Standard GeoJSON supplies horizontal EPSG4326 only; height is a separate relative-plane field.
from pyproj import Transformer
tr=Transformer.from_crs(2326,4326,always_xy=True)
photo=np.array(Image.open(HERE.parents[1]/'chronology/aerial/fullframes/A36143.jpg').convert('RGB'))
fields=['track_id','frame42_x','frame42_y','frame43_x','frame43_y','easting_hk1980_m','northing_hk1980_m','z_above_fitted_local_park_road_plane_m','reprojection_rms_px','positive_depth_both_views','passes_diagnostic_5px_filter','within_map_control_hull','surface_class','manual_surface_note','r','g','b']
notes={788:('ground_fit','park paved-path intersection'),1030:('ground_fit','park court-adjacent paved path junction'),74:('ground_fit','paved path beside cleared Walled City site'),1187:('ground_fit','park boundary paved path'),708:('ground_holdout','Carpenter Road visible ground point'),26:('roof_observed','municipal market north roof feature'),1135:('roof_observed','municipal market south rooftop service structure'),72:('surface_diagnostic','cleared site surface; not guaranteed road-plane elevation'),124:('surface_diagnostic','court-edge visible surface; possible boundary height')}
records=[]
for i in range(len(world)):
 x,y=np.round(p2[i]).astype(int);rgb=photo[np.clip(y,0,2999),np.clip(x,0,2999)].tolist();kind,note=notes.get(i,('unclassified','no automatic building/ground assignment'))
 records.append(dict(zip(fields,[i,*p1[i],*p2[i],*world[i],s['reprojection'][i],bool(s['positive'][i]),bool(good[i]),bool(local[i]),kind,note,*rgb])))
with (HERE/'sparse_stereo_points.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
with (HERE/'sparse_stereo_points.ply').open('w') as f:
 f.write('ply\nformat ascii 1.0\ncomment x y are EPSG2326 metres; z relative fitted local park-road plane NOT HKPD\ncomment nominal camera calibration; unclassified sparse tiepoints NOT solid buildings\n'+f'element vertex {int(good.sum())}\nproperty double x\nproperty double y\nproperty double z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nproperty int track_id\nproperty float reprojection_px\nend_header\n')
 for r in records:
  if r['passes_diagnostic_5px_filter']:f.write(' '.join(str(r[k]) for k in ['easting_hk1980_m','northing_hk1980_m','z_above_fitted_local_park_road_plane_m','r','g','b','track_id','reprojection_rms_px'])+'\n')
# Finite perturbation experiment only. These offsets are declared sensitivity choices, NOT uncertainty bounds.
variants=[]
for fm,cx,cy in [(1.,1460.,1440.),(.95,1460.,1440.),(1.05,1460.,1440.),(1.,1440.,1440.),(1.,1480.,1440.),(1.,1460.,1420.),(1.,1460.,1460.)]:
 v=solve(fm,cx,cy);variants.append({'focal_multiplier':fm,'principal_x':cx,'principal_y':cy,'metric_baseline_m':v['scale'],'roof_point_26_height_m':v['world'][26,2],'roof_point_1135_height_m':v['world'][1135,2],'heldout_ground708_z_m':v['world'][708,2],'map_holdout_horizontal_rmse_m':float(np.sqrt(np.mean(np.sum(v['gcerr'][~fit,:2]**2,axis=1))))})
sourcefiles=[HERE.parents[1]/'chronology/aerial/fullframes/A36142.jpg',HERE.parents[1]/'chronology/aerial/fullframes/A36143.jpg',HERE.parents[1]/'chronology/sheets/maps/1980_1990_678_11-NE-11A_1989-10-01.zip']
report={'generated_utc':datetime.now(timezone.utc).isoformat(),'status':'measured_sparse_stereo_reconstruction_conditional_nominal_calibration','actual_same_epoch_content_overlap_verified':True,'source_date':'1993-11-02','source_frames':['A36142','A36143'],'same_camera_label':'WILD15/UAGIA Nr6098 152.12','crs_horizontal':'EPSG:2326 via original 1989 survey worldfile and 6 map road GCPs','vertical_reference':'relative to four observed park/paved-path stereo points fitted as common local plane; NOT HKPD or absolute elevation','assumptions':['nominal152.12mm focal number interpreted as focal length;300dpi taken as metric film scan scale','shared principal point approximated from corner fiducial layout at1460,1440 original pixels','no calibrated lens distortion or scan deformation correction','four selected park/path ground correspondences approximated by one locally planar reference; source ground elevations not equated to sea level','map road junctions unchanged between1989 and1993; six fitted and four held-out ground coordinates','all triangulated points remain unclassified except explicitly inspected surface IDs; vegetation/terrain/roof outliers not silently buildings'],'counts':{'ratio_matches':int(len(raw['p1'])),'fundamental_inliers':len(world),'positive_depth':int(s['positive'].sum()),'exported_ply_reprojection_under5px':int(good.sum()),'exported_points_within_map_control_hull':int((good&local).sum()),'map_control_fit':int(fit.sum()),'map_control_holdout':int((~fit).sum()),'stereo_ground_plane_fit':len(ground_fit),'stereo_ground_plane_holdout':len(ground_check),'observed_roof_points':len(roof)},'nominal_K':s['K'].tolist(),'nominal_relative_R':s['R'].tolist(),'nominal_relative_t_unit':s['t'].ravel().tolist(),'metric_baseline_m_from_map_scale':s['scale'],'index_center_baseline_m_comparison_only':float(np.hypot(838068-837543,820693-820672)),'ground_plane_fit_track_ids':ground_fit,'ground_plane_holdout_track_ids':ground_check,'ground_plane_fit_z_residuals_m':world[ground_fit,2].tolist(),'ground_plane_holdout_z_residuals_m':world[ground_check,2].tolist(),'map_fit_horizontal_rmse_m':float(np.sqrt(np.mean(np.sum(s['gcerr'][fit,:2]**2,axis=1)))),'map_holdout_horizontal_rmse_m':float(np.sqrt(np.mean(np.sum(s['gcerr'][~fit,:2]**2,axis=1)))),'map_holdout_horizontal_max_m':float(np.linalg.norm(s['gcerr'][~fit,:2],axis=1).max()),'map_control_residuals_ENZ_m':s['gcerr'].tolist(),'reprojection_rms_px_quantiles':np.percentile(s['reprojection'],[0,25,50,75,95,100]).tolist(),'camera1_relative_plane_height_m':s['camera1_world'][2],'camera2_relative_plane_height_m':s['camera2_world'][2],'roof_point_estimates':[{'track_id':i,'observed_object':notes[i][1],'height_above_reference_plane_m':world[i,2],'reprojection_rms_px':s['reprojection'][i],'ground_base_elevation_at_building_identified':False,'statistical_or_hard_error_bounds':None} for i in roof],'nominal_intrinsic_sensitivity_experiment':variants,'sensitivity_is_calibrated_uncertainty':False,'height_acceptance':'exploratory visualization point heights only; full building heights/roof meshes need more observations; one ground holdout is not vertical accuracy validation','source_sha256':{str(p.relative_to(HERE.parents[1])):hashlib.sha256(p.read_bytes()).hexdigest() for p in sourcefiles}}
(HERE/'sparse_stereo_report.json').write_text(json.dumps(report,indent=2)+'\n')
np.savez(HERE/'sparse_stereo_transform.npz',**{k:v for k,v in s.items() if isinstance(v,np.ndarray)},scale=s['scale'],origin_EN=origin)
print(json.dumps(report,indent=2))

```
