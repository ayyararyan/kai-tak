from pathlib import Path
import json,hashlib
import box_certifier as bc
from parameter_taylor import prepare,Case
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'active_branch.json').read_text())['baseline'];q=r['q'];dq=[0.]*12
for i,v in zip([1,2,3,10,11],r['dq_dwx']):dq[i]=v
results=[]
for delta,eta in [('.001','.149'),('.002','.147'),('.005','.14'),('.01','.13')]:
 p=bc.certify_box(Case(),q,dq,delta,eta,maxdepth=18,parameter_taylor=True);p['source_sha256']={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [HERE/'box_certifier.py',HERE/'parameter_taylor.py',HERE/'active_branch.json']};results.append(p)
 (HERE/'taylor_domain_refined.json').write_text(json.dumps(results,indent=2)+'\n');print(delta,eta,p.get('certified'),p.get('processed'),p.get('seconds'),p.get('unresolved'),flush=True)
