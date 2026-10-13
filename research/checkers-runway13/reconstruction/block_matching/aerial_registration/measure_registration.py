"""Local affine registration from independently identified road junctions.
No index corners; no orthorectification or height inference.
"""
from pathlib import Path
import json,csv,hashlib,zipfile
import numpy as np
import rasterio
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PHOTO=ROOT/'chronology/aerial/fullframes/A36143.jpg'
MAP=ROOT/'chronology/sheets/maps/1980_1990_678_11-NE-11A_1989-10-01.zip'
# Coordinates measured on full map resized to width1800, and photo rotated90CCW/resized1800.
# Named cross-streets use street-centerline junction, NOT visible roof corners.
points=[
 ('carpenter_nga_tsin_long',204,786,483,376,'fit'),
 ('carpenter_nam_kok',328,790,537,383,'holdout'),
 ('carpenter_lung_kong',450,796,590,389,'fit'),
 ('carpenter_south_wall',571,798,645,394,'holdout'),
 ('carpenter_tak_ku_ling',693,814,698,400,'fit'),
 ('nga_tsin_wai_nga_tsin_long',197,1199,463,538,'fit'),
 ('nga_tsin_wai_nam_kok',318,1201,517,547,'holdout'),
 ('nga_tsin_wai_lung_kong',441,1204,572,555,'fit'),
 ('nga_tsin_wai_south_wall',562,1208,627,563,'holdout'),
 ('nga_tsin_wai_tak_ku_ling',684,1215,681,572,'fit'),
]
with zipfile.ZipFile(MAP) as z: name=next(n for n in z.namelist() if n.endswith('.tif'))
with rasterio.open('/vsizip/'+str(MAP)+'/'+name) as ds:
 t=ds.transform; mw,mh=ds.width,ds.height
 # Pixel centers: image coordinate p (resized pixel-center convention) -> original.
 def ground(mx,my):
  ox=(mx+.5)*mw/1800-.5; oy=(my+.5)*mh/round(mh*1800/mw)-.5
  return t*(ox+.5,oy+.5)
 rows=[]
 for name,mx,my,rx,ry,role in points:
  E,N=ground(mx,my)
  # inverse ROTATE90 pixel mapping after isotropic resize: original x=2999-rot_y; original y=rot_x
  ox=2999-((ry+.5)*3000/1800-.5);oy=(rx+.5)*3000/1800-.5
  rows.append(dict(id=name,map1800_x=mx,map1800_y=my,rotated1800_x=rx,rotated1800_y=ry,photo_x=ox,photo_y=oy,easting=E,northing=N,role=role))
 X=np.array([[r['photo_x'],r['photo_y'],1] for r in rows]); Y=np.array([[r['easting'],r['northing']] for r in rows])
 fit=np.array([r['role']=='fit' for r in rows]); coef=np.linalg.lstsq(X[fit],Y[fit],rcond=None)[0]
 err=X@coef-Y
 for i,r in enumerate(rows):
  r.update(residual_easting_m=err[i,0],residual_northing_m=err[i,1],residual_m=np.linalg.norm(err[i]))
 with (HERE/'control_points.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 metrics={}
 for mask,label in [(fit,'fit'),(~fit,'holdout')]:
  d=np.linalg.norm(err[mask],axis=1);metrics[label]={'count':int(mask.sum()),'rmse_m':float(np.sqrt(np.mean(d*d))),'max_m':float(d.max()),'residuals_m':d.tolist()}
 # Convert ground->photo for Pillow pull resampling. Deliver only the local control footprint, not full-frame false orthophoto.
 inv=np.linalg.inv(np.vstack([coef.T,[0,0,1]]))
 bounds=[float(Y[:,0].min()),float(Y[:,1].min()),float(Y[:,0].max()),float(Y[:,1].max())]
 e0,n0,e1,n1=bounds;res=.5;W=int(np.ceil((e1-e0)/res));H=int(np.ceil((n1-n0)/res))
 out_to_world=np.array([[res,0,e0+res/2],[0,-res,n1-res/2],[0,0,1]])
 p=inv@out_to_world
 im=Image.open(PHOTO).convert('RGB').transform((W,H),Image.Transform.AFFINE,tuple(p[:2].ravel()),resample=Image.Resampling.BICUBIC)
 im.save(HERE/'A36143_local_affine_diagnostic.png')
 with rasterio.open(HERE/'A36143_local_affine_diagnostic.tif','w',driver='GTiff',height=H,width=W,count=3,dtype='uint8',crs='EPSG:2326',transform=rasterio.transform.from_origin(e0,n1,res,res),compress='deflate') as dst:
  dst.write(np.asarray(im).transpose(2,0,1));dst.update_tags(status='LOCAL_AFFINE_DIAGNOSTIC_NOT_ORTHOPHOTO',height_valid='false',fullframe_valid='false')
 summary={'frame':'A36143','capture_date':'1993-11-02','reference_sheet':'11-NE-11A','reference_edition_month':'1989-10','crs':'EPSG:2326','model':'local six-parameter affine','status':'local_ground_planimetric_diagnostic_not_orthophoto','ground_control_type':'manually matched street-centerline junctions','fit_holdout_split':'alternating cross streets selected before fit; 6 fit and 4 holdout; all on two parallel roads, not independent across regional surface','coefficients_pixel_xy1_to_EN':coef.tolist(),'metrics':metrics,'local_control_bbox_EN':bounds,'nominal_output_pixel_m':res,'pixel_size_is_accuracy':False,'manual_pick_uncertainty':'not calibrated; controls visually picked on 1800px inspection images; approximately several source pixels','not_valid_for':['whole-frame orthorectification','building footprints from roof edges','height measurement','clearance certification','controls outside local road grid'],'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [PHOTO,MAP]},'camera_label_observed':'WILD 15/UAGIA Nr 6098 152.12','camera_calibration_available':False,'calibration_note':'Film label numeric value not a distortion/principal-point/fiducial calibration; API FOCAL_LENGTH is 0.'}
 (HERE/'registration.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
