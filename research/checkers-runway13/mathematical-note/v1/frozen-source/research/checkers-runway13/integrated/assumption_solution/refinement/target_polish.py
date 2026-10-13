from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from conditional_model import *
HERE=Path(__file__).resolve().parent
rows=[]
for name,typ,val in [('tailwind5','wind',5),('urban60','urban',60),('urban65','urban',65)]:
 old=json.loads((HERE/('continuation_'+typ+'.json')).read_text());seeds=[r['q'] for r in old if r['condition']['name']==name]
 if name=='urban65':seeds.append(next(r['q'] for r in old if r['condition']['name']=='urban60'))
 for j,q in enumerate(seeds):
  c=Case(name,urban=val) if typ=='urban' else Case(name,wind=(val*tr.KT,0,0));cache={}
  def get(x):
   key=x[:-1].tobytes()
   if key not in cache:cache.clear();cache[key]=c.evaluate(x[:-1]*SCALE,1201)
   return cache[key]
  def con(x):
   m,h,_=get(x);return np.r_[np.concatenate(list(m.values()))-x[-1],h]
  m,_,_=c.evaluate(q,1201);x=np.r_[np.array(q)/SCALE,min(map(np.min,m.values()))-1e-5]
  rr=minimize(lambda x:-x[-1],x,method='SLSQP',bounds=[(a/s,b/s) for(a,b),s in zip(BOUNDS,SCALE)]+[(-2,.49)],constraints=[dict(type='ineq',fun=con)],options=dict(maxiter=400,ftol=1e-9,eps=1e-7))
  q=rr.x[:-1]*SCALE;m,h,e,ps=c.evaluate(q,20001,True);r=dict(name=name,start=j,success=bool(rr.success),message=str(rr.message),q=q.tolist(),eta=float(min(map(np.min,m.values()))),mesh_eta=float(rr.x[-1]),hard_min=float(min(map(np.min,h.values()))),minima={k:float(np.min(v)) for k,v in m.items()},urban_exit=float(h['urban_exit_limit'][0]),iterations=int(rr.nit));rows.append(r)
  (HERE/'target_polish.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,j,r['success'],r['eta'],r['mesh_eta'],r['urban_exit'],flush=True)
