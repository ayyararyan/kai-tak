from conditional_model import *
from export import make_case
from evaluate import evaluate
from analysis_tools import fixed_gate
import hashlib,csv
from datetime import datetime,timezone

def require(ok,msg):
 if not ok:raise RuntimeError(msg)

def check():
 errors=[];prior=json.loads((ROOT/'integrated/aircraft_followup/prior_integrity.json').read_text())
 for name,v in prior.items():
  p=ROOT/name;require(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'] and p.stat().st_size==v['bytes'],'prior artifact changed '+name)
 frozen=json.loads((ROOT/'integrated/source_manifest.json').read_text())['files']
 for name,h in frozen.items():require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'frozen input changed '+name)
 require(hashlib.sha256((ROOT/'integrated/geometry/integrated_evidence.geojson').read_bytes()).hexdigest()==SCENE['source_sha256'],'scene source changed')
 rows=json.loads((OUT/'conditions.json').read_text());accepted=0;excluded=0;unresolved=0;covers=0;maxpos=maxvel=0;rechecked_sources=set()
 for row in rows:
  d=OUT/'cases'/row['name']
  if 'certified_eta' not in row:
   if row['status']=='conditionally_excluded_by_fixed_gate':excluded+=1
   else:unresolved+=1
   continue
  accepted+=1;r=json.loads((d/'result.json').read_text());c=make_case(r['condition']);q=r['selected']['q'];cert=json.loads((d/'continuous.json').read_text());v=json.loads((d/'verification.json').read_text());b=v['energy_family_bound']
  require(cert['certified'] and cert['historical_certified'] is False,'wrong certificate state')
  require(cert['result_sha256']==hashlib.sha256((d/'result.json').read_bytes()).hexdigest(),'wrong result binding')
  require(v['result_sha256']==cert['result_sha256'] and v['certificate_sha256']==hashlib.sha256((d/'continuous.json').read_bytes()).hexdigest(),'wrong replay binding')
  for item in [cert,b]:
   for name,h in item['source_sha256'].items():
    require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'changed proof source '+name);rechecked_sources.add(name)
  require(b['exclusion']['excluded'] and b['exclusion']['residual_lower_display_m']>0,'energy exclusion missing')
  require(b['condition']==r['condition'],'bound condition mismatch')
  for ph in [0,1]:
   cells=sorted([x for x in cert['cover']if x[0]==ph],key=lambda x:x[1]);require(cells[0][1]==0 and cells[-1][2]==1,'time cover endpoints')
   require(all(x[2]==y[1]for x,y in zip(cells,cells[1:])),'time cover gap/overlap');covers+=len(cells)
  require(v['independent_replay']['passed'] and v['secondary_local_retention_passed'],'replay/secondary failed')
  maxpos=max(maxpos,v['independent_replay']['max_position_error_m']);maxvel=max(maxvel,v['independent_replay']['max_velocity_error_mps'])
  td=q[0]+q[1];left=evaluate(c.name,td,'left');right=evaluate(c.name,td,'right');require(abs(left['velocity_mps'][2]+.7)<1e-8 and right['velocity_mps'][2]==0,'hybrid reset')
  require(np.linalg.norm(np.array(left['position_cg_m'])-right['position_cg_m'])<1e-7,'touchdown position discontinuity')
  stop=q[2]+2*q[3]+q[3]*q[3]/(2*1.4709975)
  require(abs(stop-row['stop_x_m'])<1e-8 and abs(2786-stop-row['runway_remaining_m'])<1e-8,'ground metric mismatch')
  with(d/'path_controls.csv').open()as f:rr=list(csv.DictReader(f))
  require(abs(float(rr[-1]['x_m'])-stop)<1e-7 and abs(float(rr[-1]['vx_mps']))<1e-8,'CSV stop mismatch')
  for args in [(c.name,-1),(c.name,row['stop_s']+1)]:
   try:evaluate(*args)
   except ValueError:pass
   else:raise RuntimeError('extrapolation accepted')
 require((accepted,excluded,unresolved)==(8,1,3),'unexpected condition accounting')
 require(fixed_gate(Case('frame_shift',frame_dx=80,frame_dy=-50,runway_level=4))['violations_m']['urban_side_1']==-10,'fixed gate exclusion')
 core=(OUT/'tests_core.log').read_text();geo=(OUT/'tests_geospatial.log').read_text()
 require('48 passed' in core and 'Ran 16 tests' in geo and geo.rstrip().endswith('OK'),'test evidence incomplete')
 receipt=dict(verified_utc=datetime.now(timezone.utc).isoformat(),prior_artifacts_unchanged=len(prior),frozen_inputs_unchanged=len(frozen),tests_passed=64,continuous_conditional_landings=accepted,fixed_gate_excluded_conditions=excluded,unresolved_conditions=unresolved,closed_time_cells_verified=covers,proof_source_files_checked=len(rechecked_sources),max_independent_replay_position_error_m=maxpos,max_independent_replay_velocity_error_mps=maxvel,source_unknowns_preserved=True,historical_certified=False,full_condition_to_global_optimum=False,global_secondary_proof=False,physical_prediction_intervals=None,causal_feedback_policy=False,errors=errors)
 (OUT/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2));return receipt
if __name__=='__main__':check()
