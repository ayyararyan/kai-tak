"""Evidence gate and continuous supplied-scene diagnostic; not a flight solver."""
from pathlib import Path
import argparse,json,hashlib,math
import numpy as np
from clearance import enclose_body,polynomial_position_box,screen_scene,finite
ROOT=Path(__file__).resolve().parents[1]

def check_segments(segments,vertices,body_reference,features,tracking_xyz,coverage_complete=False):
 """Enclose all supplied phase cells. Angles must be independently all-time bounds.
 World frame must be the same declared forward/right/up Cartesian frame for all
 quantities. Polynomial argument is normalized phase time. Excludes dynamic and
 allowed-contact certification; reports possible intersections, never collisions.
 """
 if not segments:raise ValueError('no segments')
 cells=[];previous=None
 for seg in segments:
  duration=float(finite(seg['duration_s']));t0=float(finite(seg['start_s']));n=seg.get('cells',16)
  if duration<=0 or not isinstance(n,int) or isinstance(n,bool) or n<1 or n>10000:raise ValueError('invalid duration or cells')
  coeff=seg['coefficients_xyz_m'];start=np.array([float(c[0]) for c in coeff]);end=np.array([sum(map(float,c)) for c in coeff]);finite([start,end])
  if previous is not None:
   if not math.isclose(previous[0],t0,rel_tol=0,abs_tol=1e-9) or not np.allclose(previous[1],start,rtol=0,atol=1e-7):raise ValueError('noncontiguous position/time join')
  angles=seg['angle_ranges_rad'];previous=(t0+duration,end)
  for k in range(n):
   a=k/n;b=(k+1)/n;box=polynomial_position_box(coeff,a,b);body=enclose_body(vertices,body_reference,box,angles,tracking_xyz);result=screen_scene(body,features,coverage_complete)
   cells.append({'phase':seg['name'],'time_interval_s':[t0+duration*a,t0+duration*b],'body_outer_box_m':body.tolist(),**result})
 limiting=[]
 for cell in cells:
  for f in cell['cleared_features']:limiting.append(dict(f,phase=cell['phase'],time_interval_s=cell['time_interval_s']))
 return {'scope':'all-time geometry for supplied enclosures ONLY; not dynamics/contact/historical validity','status':'unknown' if any(c['unknown'] for c in cells) else ('possible_intersection' if any(c['possible_intersections'] for c in cells) else 'clear_for_supplied_enclosures'),'historical_certified':False,'cell_count':len(cells),'limiting_cleared_feature':min(limiting,key=lambda v:v['vertical_gap_lower_m']) if limiting else None,'cells':cells}

def evidence_gate(root=ROOT):
 def read(p):return json.loads((root/p).read_text())
 reg=read('integrated/registration.json');body=read('integrated/geometry/airframe_envelope.json');status=read('integrated/integration_status.json');manifest=read('integrated/source_manifest.json')
 changed=[p for p,h in manifest['files'].items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
 issues=[]
 if changed:issues.append({'id':'frozen_integrity','files':changed})
 for key,ok in status['gates'].items():
  if not ok:issues.append({'id':key,'status':'unresolved'})
 if not reg['accepted_historical_registration'] or any(reg[k] is None for k in ['threshold_EN_m','grid_runway_bearing_1993_deg','runway_HKPD_m']):issues.append({'id':'registration_values_not_accepted'})
 if not body['clearance_eligible_historical']:issues.append({'id':'static_drawing_not_inflight_bound'})
 # There is deliberately no success implementation that turns edited booleans into a certificate.
 # Full evidence validation and coupled flight/contact integration remain an explicit requirement.
 issues.append({'id':'full_historical_integration_not_implemented','status':'acceptance_not_established'})
 return {'requested_goal':'historical condition-dependent closed-form optimal full landing','overall':'INCOMPLETE','stage':'historical integration blocked','frozen_files_checked':len(manifest['files']),'frozen_files_changed':changed,'blockers':issues,'candidate':'counterfactual/formula.json','candidate_historical_clearance':None,'limiting_historical_feature':None,'reason_no_limiting_feature':'No accepted common frame, absolute obstacle top bounds or body-pose/reference history; no physical clearance number calculated.','downstream_optimality':'not_started_under_required_sequence','closed_form_optimum':None,'global_proof':None,'historical_condition_cells_certified':0}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();r=evidence_gate();s=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='');raise SystemExit(2)
