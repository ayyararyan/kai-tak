"""Proof-producing tests, algebraic AD checks, independent implementation checks.
Finite differences are regression diagnostics only, never certificate premises.
"""
import sys,json
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate import *
from conditional_model import phase

@pytest.fixture(scope='module')
def proof():
 stored=json.loads((HERE/'certificate.json').read_text())
 r,X,m=krawczyk(stored['root']['center'],stored['root']['radius'])
 return r,X,m,stored

def contains(v,x):
 x=interval(x);return v.a<=x.a and v.b>=x.b

def test_dual_chain_exact_rational():
 x=D(2,[I(1)]+[I(0)]*8);f=(x*x+3)/(x+1)
 assert contains(f.v,I(7)/3) and contains(f.d[0],I(5)/9)
 y=(x*x).sqrt();assert contains(y.v,2) and contains(y.d[0],1)
 e=x.exp();assert contains(e.d[0],iv.exp(I(2)))

def test_jet_exact_coefficients_and_mixed_derivatives():
 x=D(2,[I(1)]+[I(0)]*8);s=J([x,1])
 f=1/s
 for k in range(4):
  assert contains(f.c[k].v,I((-1)**k)/2**(k+1))
  assert contains(f.c[k].d[0],I((-1)**(k+1)*(k+1))/2**(k+2))
 y=(s*s).sqrt()
 for k,target in enumerate([2,1,0,0]):assert contains(y.c[k].v,target)
 e=s.exp()
 for k in range(4):
  assert contains(e.c[k].v,iv.exp(I(2))/math.factorial(k))
  assert contains(e.c[k].d[0],iv.exp(I(2))/math.factorial(k))

def test_force_and_slew_against_independent_numpy():
 z=variables([str(x)for x in BASE['z']]);q=BASE['q'];c=Case();polys=c.curves(q)[1]
 for s in [0.,.13,.3671596,.7425247,.7635208,1.]:
  th,ld,T=state(z,D(str(s)));p=phase(polys,q[1],np.array([s]),c.p)
  assert abs(float(decimal_mid(th.c[0].v))-p['thrust'][0])<2e-7
  assert abs(float(decimal_mid(th.c[1].v/T.v))-p['slew'][0])<2e-7
  assert abs(float(decimal_mid(ld.c[0].v))-p['load'][0])<2e-12

def test_analytic_system_jacobian_regression(proof):
 r,X,m,stored=proof;x=np.array([float(v)for v in r['center']]);f,j,*_=system([repr(float(v))for v in x]);J0=np.array([[float(decimal_mid(v))for v in row]for row in j])
 # Deliberately only selected mixed derivative columns; 3-point diagnostic.
 for k in [0,5,6,7,8]:
  h=1e-6;xp=x.copy();xm=x.copy();xp[k]+=h;xm[k]-=h
  fp=system([repr(float(v))for v in xp])[0];fm=system([repr(float(v))for v in xm])[0]
  d=np.array([float(decimal_mid(a-b))/(2*h)for a,b in zip(fp,fm)])
  assert np.allclose(d,J0[:,k],rtol=2e-6,atol=2e-6)

def test_krawczyk_existence_uniqueness_and_nonsingularity(proof):
 r,X,m,stored=proof
 assert r['certified']and r['strict_inclusion']and r['all_jacobians_nonsingular']
 assert r['jacobian_contraction_bound_display']<1e-12
 assert all(max(abs(a),abs(b))<1e-30 for a,b in r['offset_display'])

def test_wrong_root_and_invalid_boxes_rejected(proof):
 r,X,m,stored=proof;bad=r['center'].copy();bad[5]='.153'
 assert not krawczyk(bad,'1e-20')[0]['certified']
 for radius in ['0','-1','nan','inf']:
  with pytest.raises(ValueError):krawczyk(r['center'],radius)
 with pytest.raises(ValueError):krawczyk(r['center'][:-1],'1e-20')

def test_strict_positive_simplex(proof):
 r,X,m,stored=proof;s=simplex(m)
 assert s['certified']and s['contraction_display']<1e-12
 assert min(a for a,b in s['multiplier_display'])>.00096
 assert sum(a for a,b in s['multiplier_display'])<1<sum(b for a,b in s['multiplier_display'])

def test_stationary_and_endpoint_extrema(proof):
 r,X,m,stored=proof;zones=events(X,'.01')
 assert len(zones)==5 and all(z['certified']for z in zones)
 assert all(z['curvature_display'][0]>0 for z in zones[:3])
 assert zones[3]['slope_display'][0]>0 and zones[4]['slope_display'][1]<0

def test_complete_path_fresh_all_time_certificate(proof):
 r,X,m,stored=proof;zones=events(X,'.01');p=full_path(X,zones)
 assert p['certified']
 for ph in [0,1]:
  cells=sorted((a,b)for phase,a,b,*_ in p['cover']if phase==ph)
  assert cells[0][0]==0 and cells[-1][1]==1 and all(x[1]==y[0]for x,y in zip(cells,cells[1:]))
 assert min(p['strict_force_slack_display'].values())>0
 assert min(p['geometry_minima_display'].values())>=0


def test_secondary_receipt_and_replay():
 r=json.loads((HERE/'retention_replay.json').read_text());p=r['secondary_retention']
 assert p['certified']and r['root_center_replay']['passed']
 from decimal import Decimal
 root=json.loads((HERE/'certificate.json').read_text())['root']
 assert Decimal(p['eta_lower_real_decimal'])+Decimal('.0001')>=Decimal(root['center'][5])+Decimal(root['radius'])
 for name,sha in p['source_sha256'].items():assert hashlib.sha256((bc.ROOT/name).read_bytes()).hexdigest()==sha

def test_preserved_packages():assert check_preserved()==610
