from pathlib import Path
import json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'integrated/geometry'
j=json.loads((OUT/'runway_control_picks.json').read_text());old=np.array(json.loads((ROOT/'reconstruction/block_matching/aerial_registration/registration.json').read_text())['coefficients_pixel_xy1_to_EN'])
p=np.array([v['photo_uv'] for v in j['points']],float);m=np.array([v['map_uv'] for v in j['points']],float)
# map picking frame to original photo pixel-edge frame, with explicit resampling convention
p_en=p*np.array([1.25,-1.25])+[837500,821000];p_src=(p_en-old[2])@np.linalg.inv(old[:2]);m_en=m*[1.25,-1.25]+[837500,821000]
fit=np.array([v['role']=='fit' for v in j['points']]);X=np.c_[p_src,np.ones(len(p))];a=np.linalg.lstsq(X[fit],m_en[fit],rcond=None)[0];pred=X@a;errors=np.linalg.norm(pred-m_en,axis=1)
report={'method':'local6parameter affine, manually picked ground features','historical_clearance_ready':False,'physical_accuracy_bound_m':None,'crs':'EPSG:2326','source_pixel_xy1_to_EN':a.tolist(),'controls':[],'fit_rmse_m':float(np.sqrt(np.mean(errors[fit]**2))),'holdout_rmse_m':float(np.sqrt(np.mean(errors[~fit]**2))),'limitations':['1989/1990 map versus1993 photograph; same-surface identity manually interpreted','Fit/holdout samples not independent surveys','Perspective relief distortion and camera calibration unresolved','No hard accuracy bound; no vertical calibration','Some picks are approximate tangencies, not surveyed monument points']}
for i,v in enumerate(j['points']):report['controls'].append(dict(v,source_photo_pixel_xy=p_src[i].tolist(),map_EN_m=m_en[i].tolist(),residual_m=float(errors[i])))
for name,key in [('runway_registration_map_view','map_uv'),('runway_photo_diagnostic_view','photo_uv')]:
 im=Image.open(OUT/(name+'.png')).convert('RGB');d=ImageDraw.Draw(im)
 for v in j['points']:
  x,y=np.array(v[key])*1.25;d.ellipse((x-8,y-8,x+8,y+8),outline='red',width=2);d.text((x+9,y-10),v['id'],fill='red')
 im.save(OUT/(name+'_controls.png'))
report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'runway_control_picks.json',ROOT/'reconstruction/chronology/aerial/fullframes/A36143.jpg',ROOT/'reconstruction/block_matching/aerial_registration/registration.json',ROOT/'integrated/prepare_registration.py']}
(OUT/'runway_registration_diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(report['fit_rmse_m'],report['holdout_rmse_m']);print([(v['id'],round(v['residual_m'],2)) for v in report['controls']])
