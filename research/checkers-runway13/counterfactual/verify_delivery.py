"""Fail-closed delivery verification; rerun exports/replay twice without repeating search."""
import json,sys,subprocess,hashlib
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT))
from calculate import check_sources

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    check_sources()
    numerical=['formula.json','path_controls.csv']
    previous={n:digest(OUT/n) for n in numerical}
    generated=[]
    for i in range(2):
        p=subprocess.run([sys.executable,str(OUT/'deliver.py')],capture_output=True,text=True)
        (OUT/f'regeneration_{i+1}.log').write_text(p.stdout+p.stderr)
        if p.returncode:raise RuntimeError('producer failed')
        now={n:digest(OUT/n) for n in numerical}
        if now!=previous:raise ValueError('numerical artifact reproducibility failed')
        generated.append(now)
    p=subprocess.run([sys.executable,'-m','pytest','-q',str(OUT/'test_counterfactual.py')],capture_output=True,text=True)
    (OUT/'test.log').write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('tests failed')
    result=json.loads((OUT/'result.json').read_text());cert=json.loads((OUT/'continuous_check.json').read_text())
    if not (result['status']=='conditional_scenario_feasible' and result['optimization_complete'] and cert['certified']):raise ValueError('delivery acceptance gates failed')
    from PIL import Image
    with Image.open(OUT/'landing.png') as im:im.verify()
    hashes={p.name:digest(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ['verification.json','delivery_manifest.json','SPEC.md','SCOPE_AUDIT.md','verification.log']}
    (OUT/'delivery_manifest.json').write_text(json.dumps(hashes,indent=2)+'\n')
    record=dict(utc=datetime.now(timezone.utc).isoformat(),status='passed',tests=p.stdout.strip(),producer_reruns=2,byte_identical_numerical_artifacts=numerical,
        numerical_hashes=previous,source_bindings_checked=True,certificate_identity_checked=True,independent_force_replay_passed=True,
        image_decode_passed=True,manifest_files=len(hashes),historical_landing_complete=False,physical_prediction_intervals=None,
        global_near_optimality=False,notes='Correctness and conditional model delivery verified; full historical/robust scope remains incomplete. Parent independent review separate.')
    (OUT/'verification.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))

if __name__=='__main__':run()
