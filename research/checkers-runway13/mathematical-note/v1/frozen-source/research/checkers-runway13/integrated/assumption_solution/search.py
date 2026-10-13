from conditional_model import *
import time,hashlib

def write(path,data):
 path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')

def eligible(r):return r['success'] and r['eta']>0 and r['hard_min']>=-1e-7

def run(case,seeds):
 d=OUT/'cases'/case.name;d.mkdir(parents=True,exist_ok=True)
 runs=[];write(d/'state.json',dict(status='running',condition=case.parameters()))
 for i,q in enumerate(seeds):
  r=case.solve(np.array(q),121);r['stage']=f'primary_start_{i}';runs.append(r);write(d/'runs.json',runs)
  print(case.name,r['stage'],r['success'],r['eta'],r['hard_min'],flush=True)
 ok=[r for r in runs if eligible(r)]
 if not ok:write(d/'state.json',dict(status='unresolved',condition=case.parameters()));return None
 best=max(ok,key=lambda r:r['eta'])
 r=case.solve(np.array(best['q']),501);r['stage']='refinement';runs.append(r)
 if eligible(r) and r['eta']>=best['eta']:best=r
 sec=case.solve(np.array(best['q']),501,True,best['eta']-5e-5);sec['stage']='secondary';runs.append(sec)
 chosen=sec if eligible(sec) and sec['eta']>=best['eta']-1e-4 else best
 write(d/'runs.json',runs)
 result=dict(condition=case.parameters(),primary=best,secondary=sec,selected=chosen,secondary_complete=chosen is sec,terminal_bound=terminal_bound(case),historical_certified=False,full_global_optimum_proved=False)
 write(d/'result.json',result);write(d/'state.json',dict(status='completed_numerical',condition=case.parameters(),result_sha256=hashlib.sha256((d/'result.json').read_bytes()).hexdigest()))
 print(case.name,'SELECTED',chosen['eta'],chosen['q'][:4],flush=True)
 return chosen['q']

if __name__=='__main__':
 seed=json.loads((ROOT/'counterfactual/selected.json').read_text())['selected']['q']
 calm=json.loads((ROOT/'outputs/scenario/optimization_replay.json').read_text())['optimization']['secondary']['decisions']
 configs=[Case('mean'),Case('calm',wind=(0,0,0)),Case('urban45',urban=45),Case('urban65',urban=65),Case('headwind10',wind=(-10*tr.KT,0,0)),Case('tailwind5',wind=(5*tr.KT,0,0)),Case('frame_shift',frame_dx=80,frame_dy=-50,runway_level=4),Case('buffer15',buffer=15)]
 for case in configs:
  pert=np.clip(np.array(seed)+np.array([2,1,20,-2,10,-10,15,-15,4,-2,0,0]),BOUNDS[:,0],BOUNDS[:,1])
  run(case,[seed,calm,pert])
