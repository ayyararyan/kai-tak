from search import *
d=OUT/'cases/urban55';old=json.loads((d/'result.json').read_text());c=Case('urban55',urban=55);runs=json.loads((d/'runs.json').read_text())
r=c.solve(np.array(old['selected']['q']),601,maxiter=500);r['stage']='primary_exact_exit_constraint';runs.append(r);write(d/'runs.json',runs);print('PRIMARY',{k:r[k]for k in ['success','eta','hard_min','iterations','effort']},flush=True)
if eligible(r):
 sec=c.solve(np.array(r['q']),601,True,r['eta']-5e-5,maxiter=700);sec['stage']='secondary_exact_exit_constraint';runs.append(sec);write(d/'runs.json',runs);print('SECONDARY',{k:sec[k]for k in ['success','eta','hard_min','iterations','effort']},flush=True)
 chosen=sec if eligible(sec) and sec['eta']>=r['eta']-1e-4 else r
 write(d/'result.json',dict(condition=c.parameters(),primary=r,secondary=sec,selected=chosen,secondary_complete=chosen is sec,terminal_bound=terminal_bound(c),historical_certified=False,full_global_optimum_proved=False))
 write(d/'state.json',dict(status='completed_numerical_exact_exit_constraint',condition=c.parameters(),result_sha256=hashlib.sha256((d/'result.json').read_bytes()).hexdigest()))
