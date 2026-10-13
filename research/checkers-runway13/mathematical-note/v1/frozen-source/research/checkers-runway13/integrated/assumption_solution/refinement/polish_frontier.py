from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from certify import *
from analysis_tools import replay
from retention_proof import primary_upper
from decimal import Decimal
HERE=Path(__file__).resolve().parent;path=HERE/'urban58_verified.json';old=json.loads(path.read_text());(HERE/'urban58_pre_secondary_polish.json').write_bytes(path.read_bytes());c=Case('urban58',urban=58);upper,where=primary_upper(c,old['primary']['q']);floor=upper-5e-5;cache={}
def get(x):
 key=x[:-1].tobytes()
 if key not in cache:cache.clear();cache[key]=c.evaluate(x[:-1]*SCALE,1201)
 return cache[key]
def con(x):
 m,h,e=get(x);return np.r_[np.concatenate(list(m.values()))-x[-1],h]
x=np.r_[np.array(old['secondary']['q'])/SCALE,floor]
rr=minimize(lambda x:get(x)[2]/50,x,method='SLSQP',bounds=[(a/s,b/s)for(a,b),s in zip(BOUNDS,SCALE)]+[(floor,.49)],constraints=[dict(type='ineq',fun=con)],options=dict(maxiter=500,ftol=1e-8,eps=1e-7))
q=rr.x[:-1]*SCALE;m,h,e,ps=c.evaluate(q,20001,True);r=dict(success=bool(rr.success),message=str(rr.message),iterations=int(rr.nit),q=q.tolist(),eta=float(min(map(np.min,m.values()))),effort=float(e),hard_min=float(min(map(np.min,h.values()))),mesh=1201,secondary=True)
(HERE/'urban58_secondary_polish.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='q'},flush=True)
if r['success'] and r['eta']>=upper-1e-4 and r['hard_min']>=-1e-8:
 proof=bind(certify_case(c,r['q'],str(Decimal(repr(upper))-Decimal('.0001')),maxdepth=22));proof['primary_upper']=where;proof['retention_budget']='0.0001'
 if proof['certified']:
  old.update(secondary=r,selected=r,secondary_complete=True,continuous=proof,replay=replay(c,r['q']));path.write_text(json.dumps(old,indent=2)+'\n');print('accepted continuous secondary',flush=True)
