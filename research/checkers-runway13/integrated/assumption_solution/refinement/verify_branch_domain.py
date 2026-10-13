from pathlib import Path
import json
from box_certifier import *
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'active_branch.json').read_text())['baseline'];q=r['q'];dq=[0.]*12
for i,v in zip([1,2,3,10,11],r['dq_dwx']):dq[i]=v
results=[]
for delta,eta in [('.01','.145'),('.002','.148'),('.001','.149')]:
 p=certify_box(Case(),q,dq,delta,eta,maxdepth=16);p['source_sha256']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [HERE/'box_certifier.py',HERE/'active_branch.py',OUT/'certify.py',ROOT/'counterfactual/continuous.py',OUT/'conditional_model.py',OUT/'forces.py',OUT/'scene.json',OUT/'reference_cloud.npy',ROOT/'model/config.json']};results.append(p)
 print(delta,eta,{k:p[k]for k in ['certified','processed']if k in p},p.get('unresolved'),flush=True)
 (HERE/'branch_domain.json').write_text(json.dumps(results,indent=2)+'\n')
