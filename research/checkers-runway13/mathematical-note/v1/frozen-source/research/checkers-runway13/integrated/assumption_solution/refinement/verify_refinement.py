"""Read-only artifact/proof validation by default; --write refreshes receipt."""
from pathlib import Path
import sys,json,hashlib,csv
from datetime import datetime,timezone
from decimal import Decimal
HERE=Path(__file__).resolve().parent;PARENT=HERE.parent;ROOT=HERE.parents[2]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,msg):
 if not x:raise RuntimeError(msg)
def cover(cells):
 for ph in [0,1]:
  rows=sorted((a,b)for p,a,b,*_ in cells if p==ph)
  require(bool(rows) and rows[0][0]==0 and rows[-1][1]==1,'cover endpoints')
  require(all(x[1]==y[0]for x,y in zip(rows,rows[1:])),'cover gap/overlap')
def sources(r):
 for p,h in r.get('source_sha256',{}).items():require(sha(Path(p)if Path(p).is_absolute()else ROOT/p)==h,'source mismatch '+p)
def check():
 snap=json.loads((HERE/'parent_snapshot.json').read_text())
 for p,h in snap.items():require(sha(PARENT/p)==h,'parent snapshot changed '+p)
 manifest=json.loads((PARENT/'artifact_manifest.json').read_text())['files']
 for p,v in manifest.items():require(sha(PARENT/p)==v['sha256'] and (PARENT/p).stat().st_size==v['bytes'],'parent manifest mismatch '+p)
 prior=json.loads((ROOT/'integrated/aircraft_followup/prior_integrity.json').read_text())
 for p,v in prior.items():require(sha(ROOT/p)==v['sha256'] and (ROOT/p).stat().st_size==v['bytes'],'prior mismatch '+p)
 frozen=json.loads((ROOT/'integrated/source_manifest.json').read_text())['files']
 for p,h in frozen.items():require(sha(ROOT/p)==h,'frozen mismatch '+p)
 retention=list(HERE.glob('retention_*.json'));require(len(retention)==8,'retention count');cells=0
 for f in retention:
  r=json.loads(f.read_text());require(r['certified'],'retention uncertified');cover(r['cover']);sources(r);cells+=len(r['cover'])
  require(Decimal(r['primary_upper']['upper_real_decimal'])-Decimal(r['eta_lower_real_decimal'])<=Decimal('.0001'),'retention loss')
  path=PARENT/'cases'/f.stem.removeprefix('retention_')/'result.json';require(sha(path)==r['result_sha256'],'retention path binding')
  require(sha(HERE/'retention_proof.py')==r['proof_source_sha256'],'retention checker binding')
 new=[]
 for name in ['tailwind3','urban58']:
  r=json.loads((HERE/(name+'_verified.json')).read_text());p=r['continuous'];require(p['certified'] and r['secondary_complete'] and r['replay']['passed'],'new path incomplete');cover(p['cover']);sources(p);cells+=len(p['cover'])
  require(p['q_real_decimal']==[repr(float(x))for x in r['selected']['q']],'new coefficient binding')
  require(p['condition']==r['condition'],'new condition binding')
  require(Decimal(p['primary_upper']['upper_real_decimal'])-Decimal(p['eta_lower_real_decimal'])<=Decimal('.0001'),'new secondary retention')
  q=r['selected']['q'];stop=q[2]+2*q[3]+q[3]*q[3]/(2*1.4709975)
  with(HERE/(name+'_path_controls.csv')).open()as f:rows=list(csv.DictReader(f))
  require(abs(float(rows[-1]['cg_x_m'])-stop)<1e-7 and abs(float(rows[-1]['vx_mps']))<1e-8,'new ground endpoint')
  require(2786-stop>=150,'reserve altered');new.append(dict(name=name,certified_eta=p['eta_lower_real_decimal'],secondary_complete=True,replay_position_error_m=r['replay']['max_position_error_m']))
 domains=json.loads((HERE/'taylor_domain_refined.json').read_text());accepted=[]
 for r in domains:
  if not r['certified']:continue
  cover(r['cover']);sources(r);require(r['parameter_taylor'] and r['interval_precision_decimal_digits']==40,'domain method');accepted.append(dict(radius_mps=r['delta_radius'],certified_eta=r['eta_lower_real_decimal']));cells+=len(r['cover'])
 require(len(accepted)==3,'domain count')
 bounds=json.loads((HERE/'strong_bound.json').read_text());sources(bounds['_provenance'])
 require(bounds['mean']['excluded'] and bounds['mean']['cells']==4096 and float(bounds['mean']['eta_upper_real_decimal'])<.191605,'stronger bound')
 require(not bounds['tailwind5']['eta_zero_exclusion']['excluded'],'infeasibility overclaim')
 require('97 passed' in (HERE/'tests_core.log').read_text(),'core tests')
 geo=(HERE/'tests_geospatial.log').read_text();require('Ran 16 tests' in geo and geo.rstrip().endswith('OK'),'geo tests')
 low=json.loads((HERE/'retention_mean.json').read_text())['eta_lower_real_decimal'];high=bounds['mean']['eta_upper_real_decimal']
 return dict(verified_utc=datetime.now(timezone.utc).isoformat(),parent_manifest_artifacts_unchanged=len(manifest),parent_snapshot_files_including_manifest_unchanged=len(snap),prior_artifacts_unchanged=len(prior),frozen_inputs_unchanged=len(frozen),core_tests_passed=97,geospatial_tests_passed=16,new_tests_within_core=12,original_continuous_retention_proofs=8,new_landings=new,parameter_domains=accepted,closed_time_cells_checked=cells,baseline_family_lower=low,baseline_family_upper=high,gap=str(Decimal(high)-Decimal(low)),parent_independent_QA=dict(provenance='parent inter-session read-only report, original delivered snapshot; not rerun attribution',manifest_artifacts=136,prior_artifacts=397,frozen_inputs=13,core_tests=85,geospatial_tests=16,assumption_tests_separately=12,baseline_certificate_eta='0.14930569444740496',baseline_certificate_processed=592,old_energy_exclusion_eta='0.191605',old_energy_exclusion_cells=2048,old_energy_residual_lower_m=.6839037985926542),historical_certified=False,global_optimum_proved=False,global_secondary_proved=False,unresolved_target_conditions=['tailwind5','urban60','urban65'],errors=[])
if __name__=='__main__':
 if '--write' not in sys.argv and (HERE/'artifact_manifest.json').exists():
  manifest=json.loads((HERE/'artifact_manifest.json').read_text())['files']
  for name,v in manifest.items():require(sha(HERE/name)==v['sha256'] and (HERE/name).stat().st_size==v['bytes'],'refinement manifest mismatch '+name)
 r=check()
 if '--write'in sys.argv:(HERE/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
