"""Recheck fixed witnesses using frozen original proof code. Never rerun search or overwrite sources."""
from pathlib import Path
import json,sys,hashlib,datetime,subprocess
P=Path(__file__).resolve().parent;E=P/'evidence';Q=P/'qa';Q.mkdir(exist_ok=True)
if len(sys.argv)==1:
 for name in ['calm','wind']:subprocess.run([sys.executable,__file__,name],check=True)
 raise SystemExit
name=sys.argv[1];sys.path.insert(0,str(E))
if name=='calm':
 from analytical.coupled import certify_candidate as c
 source=E/'analytical/coupled/continuous_certificate_refined.json'
else:
 sys.path.insert(0,str(E/'counterfactual'))
 import continuous as c
 source=E/'counterfactual/continuous_check.json'
saved=json.loads(source.read_text());r=c.certify(saved['q_real_decimal'],saved['eta_lower_real_decimal'])
if not r['certified']:raise RuntimeError(r)
if r['cover']!=saved['cover']:raise RuntimeError('Accepted interval cover changed')
for ph in [0,1]:
 spans=sorted((x[1],x[2]) for x in r['cover'] if x[0]==ph)
 if spans[0][0]!=0 or spans[-1][1]!=1 or any(a[1]!=b[0] for a,b in zip(spans,spans[1:])):raise RuntimeError('Incomplete cover')
receipt={'scenario':name,'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fresh_proof':r,'exact_cover_matches_saved':True,'physical_calibration':False,'independent_peer_review':False}
(Q/f'fresh_{name}_certificate.json').write_text(json.dumps(receipt,indent=2)+'\n');print(name,r['certified'],r['accepted_intervals'],r['eta_lower_real_decimal'],flush=True)
