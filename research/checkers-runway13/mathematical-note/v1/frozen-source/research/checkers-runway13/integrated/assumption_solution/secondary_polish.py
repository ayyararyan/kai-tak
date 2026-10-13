"""Retry numerical secondary stages with a smaller differencing step.
Changes optimizer tolerances only, never physical constraints or retention budget.
"""
from search import *
for name in ['calm','urban55']:
 d=OUT/'cases'/name;old=json.loads((d/'result.json').read_text());c=Case(name,wind=(0,0,0))if name=='calm'else Case(name,urban=55)
 floor=min(map(np.min,c.evaluate(old['primary']['q'],10001)[0].values()))-5e-5
 q=np.array(old['secondary']['q']);cache={}
 def get(x):
  key=x[:-1].tobytes()
  if key not in cache:cache.clear();cache[key]=c.evaluate(x[:-1]*SCALE,1201)
  return cache[key]
 def con(x):
  m,h,e=get(x);return np.r_[np.concatenate(list(m.values()))-x[-1],h]
 x0=np.r_[q/SCALE,floor];b=[(a/s,b/s)for(a,b),s in zip(BOUNDS,SCALE)]+[(floor,.49)]
 rr=minimize(lambda x:get(x)[2]/50,x0,method='SLSQP',bounds=b,constraints=[dict(type='ineq',fun=con)],options=dict(maxiter=650,ftol=1e-8,eps=1e-7))
 q=rr.x[:-1]*SCALE;m,h,e,ps=c.evaluate(q,10001,True)
 r=dict(success=bool(rr.success),message=str(rr.message),iterations=int(rr.nit),q=q.tolist(),eta=float(min(map(np.min,m.values()))),effort=float(e),minima={k:float(np.min(v))for k,v in m.items()},hard_minima={k:float(np.min(v))for k,v in h.items()},hard_min=float(min(map(np.min,h.values()))),mesh=1201,secondary=True,geometry=True,stage='smaller_step_secondary_polish')
 runs=json.loads((d/'runs.json').read_text());runs.append(r);write(d/'runs.json',runs);print(name,{k:r[k]for k in ['success','message','eta','hard_min','iterations','effort']},flush=True)
 if eligible(r) and r['eta']>=floor-5e-5 and r['effort']<old['selected']['effort']:
  arc=d/'pre_secondary_polish';arc.mkdir(exist_ok=True)
  import shutil
  for f in ['result.json','continuous.json','verification.json','state.json','formula.json']:
   if(d/f).exists():shutil.copy2(d/f,arc/f)
  old['secondary']=r;old['selected']=r;old['secondary_complete']=True;write(d/'result.json',old);write(d/'state.json',dict(status='completed_numerical_secondary_polish',condition=c.parameters(),result_sha256=hashlib.sha256((d/'result.json').read_bytes()).hexdigest()))
