from pathlib import Path
import json,numpy as np,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];G=R/'integrated/geometry';j=json.loads((G/'south_control_picks.json').read_text());p=np.array([r['photo_uv'] for r in j['points']],float);m=np.array([r['map_uv'] for r in j['points']],float);xy=np.c_[2.5*p[:,1],3000-2.5*p[:,0]];en=m*[1.5,-1.5]+[839000,819800];X=np.c_[xy,np.ones(len(xy))];fit=np.array([r['role']=='fit' for r in j['points']]);A=np.linalg.lstsq(X[fit],en[fit],rcond=None)[0];pred=X@A;err=np.linalg.norm(pred-en,axis=1)
r={'method':'6parameter affine to source-mapped seawall at near-contemporary editions','photo':'A36172 1993-11-02','source_pixel_xy1_to_EN':A.tolist(),'fit_RMS_m':float(np.sqrt(np.mean(err[fit]**2))),'holdout_RMS_m':float(np.sqrt(np.mean(err[~fit]**2))),'physical_error_bound_m':None,'accepted_historical_registration':False,'controls':[dict(v,photo_original_xy=xy[i].tolist(),map_EN=en[i].tolist(),residual_m=float(err[i])) for i,v in enumerate(j['points'])],'limitations':['Outer edge versus mapline width and water/tidal boundary uncertain','Near-contemporary date does not prove unchangedgeometry','Seawall controls do not validate roof heights or verticaldatum','No physicalworstcasebounds; no thresholdlocation yet']}
for name,key,scale in [('south_runway_map','map_uv',1.5),('A36172_CW_view','photo_uv',1.25)]:
 im=Image.open(G/(name+'.png')).convert('RGB');d=ImageDraw.Draw(im)
 for v in j['points']:
  x,y=np.array(v[key])*scale;d.ellipse((x-7,y-7,x+7,y+7),outline='red',width=2);d.text((x+8,y),v['id'],fill='red')
 im.save(G/(name+'_controls.png'))
r['source_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [G/'south_control_picks.json',G/'south_map_sources.json',R/j['photo']]};(G/'south_registration_diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print('fit/holdout',r['fit_RMS_m'],r['holdout_RMS_m']);print([(v['id'],v['residual_m']) for v in r['controls']])
