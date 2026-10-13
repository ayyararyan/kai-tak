from pathlib import Path
import sys,json,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from conditional_model import *

def save(name,data): (HERE/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def run(seq,seed):
 q=np.array(json.loads((OUT/'cases'/seed/'result.json').read_text())['primary']['q']); rows=[]
 for name,val,typ in seq:
  c=Case(name,urban=val) if typ=='urban' else Case(name,wind=(val*tr.KT,0,0))
  r=c.solve(q,401,maxiter=450);r['condition']=c.parameters();rows.append(r);save('continuation_'+typ+'.json',rows)
  print(name,{k:r[k] for k in ['success','eta','hard_min','iterations']},flush=True)
  # Preserve negative-margin continuations too: they may guide the next stage, not establish feasibility.
  if r['hard_min']>=-1e-5:q=np.array(r['q'])
 return rows
if __name__=='__main__':
 run([(f'tailwind{v}',v,'wind') for v in [2.5,3,3.5,4,4.5,5]],'tailwind2')
 run([(f'urban{v}',v,'urban') for v in [56,57,58,59,60,61,62,63,64,65]],'urban55')
