from pathlib import Path
import json
from box_certifier import *
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'active_branch.json').read_text())['baseline'];q=r['q'];dq=[0.]*12
for i,v in zip([1,2,3,10,11],r['dq_dwx']):dq[i]=v
results=[]
for delta,eta in [('.001','.13'),('.0001','.149'),('.00001','.15')]:
 p=certify_box(Case(),q,dq,delta,eta,maxdepth=18);results.append(p);print(delta,eta,p.get('certified'),p.get('processed'),p.get('unresolved'),flush=True)
 (HERE/'domain_probe.json').write_text(json.dumps(results,indent=2)+'\n')
