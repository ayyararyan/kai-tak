from search import *
for name,H in [('urban55',55),('urban60',60),('urban65',65)]:
 c=Case(name,urban=H);d=OUT/'cases'/name;runs=json.loads((d/'runs.json').read_text());seeds=sorted(runs,key=lambda r:r['eta'],reverse=True)[:2]
 for i,seed in enumerate(seeds):
  r=c.solve(np.array(seed['q']),1201,maxiter=550);r['stage']=f'dense_geometry_repair_{i}';runs.append(r);write(d/'runs.json',runs);print(name,r['stage'],r['success'],r['eta'],r['hard_min'],flush=True)
 good=[r for r in runs if eligible(r)]
 if not good:continue
 best=max(good,key=lambda r:r['eta']);sec=c.solve(np.array(best['q']),1201,True,best['eta']-5e-5,maxiter=550);runs.append(sec);write(d/'runs.json',runs)
 chosen=sec if eligible(sec) and sec['eta']>=best['eta']-1e-4 else best
 write(d/'result.json',dict(condition=c.parameters(),primary=best,secondary=sec,selected=chosen,secondary_complete=chosen is sec,terminal_bound=terminal_bound(c),historical_certified=False,full_global_optimum_proved=False))
 write(d/'state.json',dict(status='completed_numerical_after_dense_repair',condition=c.parameters(),result_sha256=hashlib.sha256((d/'result.json').read_bytes()).hexdigest()))
 print(name,'SELECTED',chosen['eta'],chosen['hard_min'],flush=True)
