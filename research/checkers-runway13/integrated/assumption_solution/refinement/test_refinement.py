from pathlib import Path
import sys,json,hashlib
import numpy as np
import pytest
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(1,str(HERE.parent))
from strong_bound import exclusion,data
from conditional_model import Case
from box_certifier import certify_box,coeff,ic,I,iv
from parameter_taylor import Dual,dual_coeff,prepare

def branch():
 r=json.loads((HERE/'active_branch.json').read_text())['baseline'];q=r['q'];dq=[0.]*12
 for i,v in zip([1,2,3,10,11],r['dq_dwx']):dq[i]=v
 return q,dq

def cover(rows):
 for ph in [0,1]:
  cells=sorted((a,b)for p,a,b,*_ in rows if p==ph)
  assert cells[0][0]==0 and cells[-1][1]==1
  assert all(a[1]==b[0]for a,b in zip(cells,cells[1:]))

def test_parent_snapshot_unchanged():
 for path,sha in json.loads((HERE/'parent_snapshot.json').read_text()).items():assert hashlib.sha256((HERE.parent/path).read_bytes()).hexdigest()==sha

def test_stronger_interval_exclusion():
 r=exclusion(Case(),'0.181970215',4096)
 assert r['excluded'] and r['residual_lower_display_m']>.9

def test_tailwind_zero_is_not_excluded():
 from conditional_model import tr
 assert not exclusion(Case(wind=(5*tr.KT,0,0)),'0',2048)['excluded']
 with pytest.raises(ValueError):exclusion(Case(),'0',0)
 c=Case();c.p['mass_kg']*=.9
 with pytest.raises(ValueError):exclusion(c,'.18',16)

def test_ratio_extrema_and_ramp():
 for wx in [-5.,0.,3.]:
  lo=60.;u=np.linspace(lo,300,2000);r=np.sqrt((u-wx)**2+10**2+22**2)/u
  assert np.max(r)<=max(1,np.sqrt((lo-wx)**2+10**2+22**2)/lo)+1e-14
 A=5.;K=3.
 for T in [.1,1.,3.]:
  z=min(T,A/K);exact=A*z-K*z*z/2
  t=np.linspace(0,T,100001);numeric=np.trapezoid(np.maximum(A-K*t,0),t)
  assert abs(exact-numeric)<1e-8

def test_dual_derivative_product_quotient():
 x=Dual('2','1');y=(x*x+3)/(x+1)
 assert y.d.a<=I(5)/9<=y.d.b

def test_analytic_parameter_kinematics_enclose_samples():
 q,dq=branch();kin=prepare(q,dq,Case(),'.005');rad=I('.005');ds=iv.mpf([-rad.b,rad.b]);qs=[I(repr(v))+I(repr(d))*ds for v,d in zip(q,dq)];c=Case();wx=c.p['wind_mps'][0];c.p['wind_mps'][0]=I(repr(wx))+ds
 cs,W=coeff(qs,c.p['wind_mps'])
 for ph in [0,1]:
  for s in [0.,.13,.5,.9,1.]:
   box=kin(cs[ph],qs[ph],s,s,ph)
   for delta in [-.005,0,.005]:
    qd=[I(repr(v))+I(repr(d))*I(repr(delta))for v,d in zip(q,dq)];wd=[I(repr(wx))+I(repr(delta)),I(repr(Case().p['wind_mps'][1])),I(0)];cd,_=coeff(qd,wd)
    for k in range(4):
     for j in range(3):
      value=ic.poly(ic.deriv(cd[ph][j],k),s,s)/qd[ph]**k
      # At structural zeros both interval computations have rounding-radius noise.
      assert float(value.a)>=float(box[k][j].a)-1e-30 and float(value.b)<=float(box[k][j].b)+1e-30

def test_parameter_domain_proof_and_binding():
 receipts=json.loads((HERE/'taylor_domain_refined.json').read_text());assert sum(r['certified']for r in receipts)==3
 for r in receipts:
  if not r['certified']:continue
  assert r['parameter_taylor'];assert r['condition_center']['wind_mps']==Case().p['wind_mps'];cover(r['cover'])
  for p,sha in r['source_sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha

def test_parameter_checker_rejects_invalid_domain():
 q,dq=branch()
 with pytest.raises(ValueError):certify_box(Case(),q,dq,'-.01','.14')
 bad=q.copy();bad[1]=3.
 with pytest.raises(ValueError):certify_box(Case(),bad,dq,'.001','.14')
 c=Case();c.p['mass_kg']*=.9
 with pytest.raises(ValueError):certify_box(c,q,dq,'.001','.14')

def test_all_original_retention_proofs():
 from decimal import Decimal
 files=list(HERE.glob('retention_*.json'));assert len(files)==8
 for f in files:
  r=json.loads(f.read_text());assert r['certified'];cover(r['cover'])
  assert Decimal(r['primary_upper']['upper_real_decimal'])-Decimal(r['eta_lower_real_decimal'])<=Decimal('.0001')
  src=HERE.parent/'cases'/f.stem.removeprefix('retention_')/'result.json';assert hashlib.sha256(src.read_bytes()).hexdigest()==r['result_sha256']

def test_active_branch_derivative_matches_resolved_points():
 r=json.loads((HERE/'active_branch.json').read_text());rows={x['wx_delta']:x for x in r['continuation']};fd=(rows[.01]['eta']-rows[-.01]['eta'])/.02
 assert abs(fd-r['baseline']['deta_dwx'])<1e-6
 for x in r['continuation']:
  if abs(x['wx_delta'])<=.1:assert min(x['multipliers'])>0 and x['max_equation_residual']<2e-8
 assert min(rows[-.2]['multipliers'])<0 # A solved equality system is not necessarily an optimum.

def test_new_frontier_receipts():
 for name in ['tailwind3','urban58']:
  r=json.loads((HERE/(name+'_verified.json')).read_text());assert r['continuous']['certified'] and r['replay']['passed'];cover(r['continuous']['cover'])
  assert r['selected']['eta']>0
  from export_refinement import evaluate
  q=r['selected']['q'];td=q[0]+q[1]
  left=evaluate(name,td,'left');right=evaluate(name,td,'right')
  assert abs(left['velocity_mps'][2]+.7)<1e-8 and right['velocity_mps'][2]==0
  assert np.linalg.norm(np.array(left['position_cg_m'])-right['position_cg_m'])<1e-7
  with pytest.raises(ValueError):evaluate(name,-1)

def test_unresolved_cases_not_relabelled():
 rows=json.loads((HERE/'target_polish.json').read_text());assert {r['name']for r in rows}=={'tailwind5','urban60','urban65'}
 assert all(r['eta']<0 for r in rows)
