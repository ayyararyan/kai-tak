"""Independent acceptance of saved outputs, separate from solver logic."""
import csv
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
run=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'outputs/scenario'
r=json.loads((run/'optimization_replay.json').read_text())
m=json.loads((run/'manifest.json').read_text())
cfg=json.loads((run/'parameter_provenance.json').read_text())
p={k:v['value'] for k,v in cfg['parameters'].items()}
checks={}
checks['scenario_status']=r['status']=='sampled_scenario_feasible'
checks['unidentified_calibration']=r['aircraft_calibration']=='unavailable'
checks['not_historical']=r['historical_comparison']=='not performed'
checks['source_hashes_current']=all(hashlib.sha256((ROOT/'model'/name).read_bytes()).hexdigest()==h for name,h in r['source_sha256'].items())
checks['manifest']=all((run/name).stat().st_size==v['bytes'] and hashlib.sha256((run/name).read_bytes()).hexdigest()==v['sha256'] for name,v in m.items())
checks['primary_success']=r['optimization']['primary']['success']
checks['secondary_success']=r['optimization']['secondary']['success']
checks['eta_retained']=r['optimization']['secondary']['eta_variable'] >= r['optimization']['primary']['eta_variable']-r['optimization']['eta_retention_tolerance']-1e-8
checks['dense_constraints']=all(v is not None and v>=-1e-6 for v in r['candidate']['margin_minima'].values())
checks['dense_hard_constraints']=all(v is not None and v>=-1e-6 for v in r['candidate']['hard_minima'].values())
checks['forward_replay']=r['candidate_replay']['passed']
checks['replay_path_constraints']=r['candidate_replay']['path_constraints_passed']
checks['dense_eta_retained']=r['mesh_check']['secondary_retains_primary_dense_eta']
checks['optimization_complete']=r['optimization_complete']
checks['replay_terminal']=r['candidate_replay']['terminal_constraints_passed']
checks['replay_stop']=r['candidate_replay']['stop_constraint_passed']
for name in ('baseline','candidate'):
    rows=list(csv.DictReader((run/f'{name}.csv').open()))
    checks[name+'_phases']=set(x['phase'] for x in rows)=={'approach','flare','rollout'}
    checks[name+'_strict_time']=all(float(a['time_s'])<float(b['time_s']) for a,b in zip(rows,rows[1:]))
    checks[name+'_stopped']=abs(float(rows[-1]['vx_mps']))<1e-8
    checks[name+'_ground_controls_blank']=all(x['bank_rad']==x['thrust_n']=='' for x in rows if x['phase']=='rollout')
    td=[x for x in rows if x['phase']!='rollout'][-1]
    expected=float(td['x_m'])+float(td['vx_mps'])*p['brake_delay_s']+float(td['vx_mps'])**2/(2*p['brake_deceleration_mps2'])
    checks[name+'_stop_formula']=abs(expected-float(rows[-1]['x_m']))<1e-7
checks['candidate_reserve']=r['candidate']['stop_x_m']<=p['lda_m']-p['reserve_m']
checks['stress_cases']=len(r['sensitivity'])==4
checks['historical_refusal']=json.loads((ROOT/'outputs/historical/historical_blocked.json').read_text())['status']=='blocked'
result={'passed':sum(map(bool,checks.values())),'total':len(checks),'checks':checks,'run':str(run)}
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
