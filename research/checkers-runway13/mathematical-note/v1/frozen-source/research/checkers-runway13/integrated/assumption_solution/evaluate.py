"""Evaluate a stored conditional reference; never silently extrapolate conditions."""
from conditional_model import *
from export import make_case
import argparse,hashlib

def evaluate(name,time_s,side='right'):
 if name not in [p.name for p in (OUT/'cases').iterdir() if p.is_dir()]:raise ValueError('unknown condition case')
 if side not in ('left','right') or not np.isfinite(time_s):raise ValueError('invalid query')
 path=OUT/'cases'/name/'result.json'
 if not path.exists():raise ValueError('condition has no accepted landing')
 result=json.loads(path.read_text());case=make_case(result['condition']);q=result['selected']['q'];td=q[0]+q[1];stop_t=td+2+q[3]/1.4709975
 cert=json.loads((path.parent/'continuous.json').read_text())
 if not cert.get('certified') or cert.get('result_sha256')!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('missing/stale certificate')
 for p,h in cert['source_sha256'].items():
  if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError('certificate source changed')
 if time_s<0 or time_s>stop_t:raise ValueError('query outside entry-to-stop interval')
 if time_s<td or time_s==td and side=='left':
  ph=0 if time_s<q[0] or time_s==q[0] and side=='left' else 1
  s=(time_s-(q[0]if ph else 0))/q[ph];d=phase(case.curves(q)[ph],q[ph],np.array([s]),case.p)
  out=dict(phase='approach'if ph==0 else'flare',position_cg_m=d['pos'][0].tolist(),velocity_mps=d['vel'][0].tolist(),bank_deg=float(np.rad2deg(d['bank'][0])),thrust_N=float(d['thrust'][0]),CL=float(d['cl'][0]))
 else:
  u=time_s-td;b=max(0,u-2);x=q[2]+q[3]*min(u,2)+q[3]*b-.5*1.4709975*b*b
  out=dict(phase='ground_delay'if u<2 else'braking'if time_s<stop_t else'stopped',position_cg_m=[x,0,6],velocity_mps=[max(0,q[3]-1.4709975*b),0,0],bank_deg=0.,thrust_N=None,CL=None)
 return out|dict(case=name,t_s=time_s,side=side,historical_certified=False,conditional_reference_only=True,feedback_policy=False)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case');p.add_argument('time_s',type=float);p.add_argument('--side',choices=['left','right'],default='right');a=p.parse_args();print(json.dumps(evaluate(a.case,a.time_s,a.side),indent=2))
