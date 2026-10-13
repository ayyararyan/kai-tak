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
 if not (record.get('metadata_checks_pass') and record.get('source_sha256_matches')):
  raise ValueError('Refusing to render failed source integrity/registration audit')
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
  try:a=audit_one(r,index[r['source_id']])
  except (ValueError,OSError,zipfile.BadZipFile,KeyError) as exc:
   a=dict(source_id=r.get('source_id'),metadata_checks_pass=False,source_sha256_matches=False,audit_error=str(exc))
  records.append(a)
 result=dict(schema_version=1,total=len(records),metadata_pass=sum(r['metadata_checks_pass'] and r['source_sha256_matches'] for r in records),crs='EPSG:2326',records=records,rendered=renders,limitations=['Metadata audit is not independent printed-grid or ground-accuracy verification.','Cartographic sheet dates are month-precision, not a date of survey for each object.','Margins outside official core contain legend and other non-geographic material.'])
 (OUT/'sheet_registration_inventory.json').write_text(json.dumps(result,indent=2)+'\n')
 if result['metadata_pass']!=result['total']:
  raise ValueError('Source integrity/registration audit failed; inventory preserved and no new rasters rendered')
 for a in records:
  if a['source_id'] in SELECTED:renders.append(render(a))
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
