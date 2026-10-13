from search import *
d=OUT/'cases/urban55';r=json.loads((d/'result.json').read_text());c=Case('urban55',urban=55)
sec=c.solve(np.array(r['secondary']['q']),1201,True,r['primary']['eta']-5e-5,maxiter=1800);sec['stage']='secondary_warm_restart'
runs=json.loads((d/'runs.json').read_text());runs.append(sec);write(d/'runs.json',runs)
print({k:sec[k]for k in ['success','message','eta','hard_min','iterations','effort']},flush=True)
if eligible(sec) and sec['eta']>=r['primary']['eta']-1e-4:
 r['secondary']=sec;r['selected']=sec;r['secondary_complete']=True;write(d/'result.json',r);write(d/'state.json',dict(status='completed_numerical_after_secondary_restart',condition=c.parameters(),result_sha256=hashlib.sha256((d/'result.json').read_bytes()).hexdigest()))
