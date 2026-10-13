from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from conditional_model import *
HERE=Path(__file__).resolve().parent
results={}
for typ,name,initial,bounds,unit in [('wind','tailwind3.5',3.5,(2,6),'kt'),('urban','urban58',58,(55,65),'m')]:
 row=next(r for r in json.loads((HERE/('continuation_'+typ+'.json')).read_text())if r['condition']['name']==name);cache={}
 def get(x):
  key=x.tobytes()
  if key not in cache:
   cache.clear();c=Case(wind=(x[-1]*tr.KT,0,0))if typ=='wind'else Case(urban=x[-1]);cache[key]=c.evaluate(x[:-1]*SCALE,601)
  return cache[key]
 def con(x):
  m,h,e=get(x);return np.r_[np.concatenate(list(m.values())),h]
 x=np.r_[np.array(row['q'])/SCALE,initial]
 rr=minimize(lambda x:-x[-1],x,method='SLSQP',bounds=[(a/s,b/s)for(a,b),s in zip(BOUNDS,SCALE)]+[bounds],constraints=[dict(type='ineq',fun=con)],options=dict(maxiter=350,ftol=1e-9,eps=1e-7))
 c=Case(wind=(rr.x[-1]*tr.KT,0,0))if typ=='wind'else Case(urban=rr.x[-1]);q=rr.x[:-1]*SCALE;m,h,e,ps=c.evaluate(q,20001,True)
 r=dict(success=bool(rr.success),message=str(rr.message),condition=float(rr.x[-1]),unit=unit,q=q.tolist(),sample_eta=float(min(map(np.min,m.values()))),hard_min=float(min(map(np.min,h.values()))),iterations=int(rr.nit),minima={k:float(np.min(v))for k,v in m.items()},status='local critical condition estimate, not global exclusion boundary')
 results[typ]=r;(HERE/'critical_conditions.json').write_text(json.dumps(results,indent=2)+'\n');print(typ,r['success'],r['condition'],r['sample_eta'],r['iterations'],flush=True)
