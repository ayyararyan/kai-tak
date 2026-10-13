from conditional_model import *
from analysis_tools import terminal_interval_bound,fixed_gate,replay
from certify import coeff,geometry_cell,I,ic
from analytical.verify_full_landing_analysis import analytic
from integrated.clearance import rotation
import pytest,itertools

def candidate():return json.loads((OUT/'cases/mean/result.json').read_text())['selected']['q']

def test_joins_and_cg_contact():
 c=Case();q=candidate();a,f=c.curves(q)
 for k in range(3):
  np.testing.assert_allclose([v.deriv(k)(1)/q[0]**k for v in a],[v.deriv(k)(0)/q[1]**k for v in f],atol=1e-8)
 assert f[2](1)==pytest.approx(6)
 assert f[2].deriv()(1)/q[1]==pytest.approx(-.7)

def test_vector_scalar_force_equivalence():
 c=Case();q=candidate()
 for polys,T in zip(c.curves(q),q[:2]):
  for s in [.13,.44,.83]:
   a=analytic(polys,T,s,c.p);b=phase(polys,T,np.array([s]),c.p)
   for key in ['pos','vel','acc','bank','roll','slew','thrust','eas','gamma']:np.testing.assert_allclose(b[key][0],a[key],rtol=2e-10,atol=1e-7)
   assert a['acceleration_residual']<1e-11

def test_whole_aircraft_bound_not_point_only():
 c=Case(urban=25)
 d={'pos':np.array([[-650.,0.,40.]]),'bank':np.array([np.deg2rad(25)])}
 assert d['pos'][0,2]>c.urban+3
 assert c.geometry(d)['urban_upstream'][0]<0
 assert np.sqrt(40.8**2+32.7**2+13.8**2)<55
 # Actual rotated box minima agree with bank support used for non-gear body.
 box=np.array(list(itertools.product([-40.8,30.2],[-32.7,32.7],[-4,13.8])))
 for phi in [-.4,0,.4]:
  v=box@rotation(.2,0,phi).T
  assert v[:,2].min()==pytest.approx(-4*np.cos(phi)-32.7*abs(np.sin(phi)))

def test_shift_gate_excludes_entire_family():
 assert fixed_gate(Case('shift',frame_dx=80,frame_dy=-50,runway_level=4))['violations_m']['urban_side_1']==pytest.approx(-10)
 assert fixed_gate(Case())['feasible_under_imposed_gate_constraints']

def test_terminal_global_bounds_and_no_squared_spurious_root():
 for w in [(0,0,0),(-5,9,0),(1,0,0)]:
  c=Case(wind=w);a=terminal_bound(c);b=terminal_interval_bound(c)
  assert abs(a['residual'])<1e-8
  assert b['full']['lower_F_upper_display']<0<b['full']['upper_F_lower_display']
  assert b['family']['upper_display']<=b['full']['upper_display']+1e-12
  assert a['eta_upper']==pytest.approx(b['full']['upper_display'],abs=1e-12)

def test_interval_geometry_encloses_samples():
 c=Case();q=candidate();cs,W=coeff([I(repr(v)) for v in q],c.p['wind_mps'])
 for ph,l,r in [(0,.3,.31),(1,.7,.71)]:
  values,_=geometry_cell(c,cs[ph],I(repr(q[ph])),l,r,ph)
  numeric=c.geometry(phase(c.curves(q)[ph],q[ph],np.linspace(l,r,11),c.p))
  for k in numeric:
   if k not in values:continue
   assert float(values[k].a)-1e-8<=np.min(numeric[k])
   assert float(values[k].b)+1e-8>=np.max(numeric[k])

def test_historical_source_unknowns_preserved():
 j=json.loads((ROOT/'integrated/geometry/integrated_evidence.geojson').read_text())
 assert any(f['properties'].get('historical_upper_elevation_hkpd_m') is None for f in j['features'])
 assert not SCENE['historical_certified'] and not SCENE['source_nulls_modified']

def test_reject_wrong_condition_or_decisions():
 with pytest.raises(ValueError):Case(wind=(0,0,1))
 with pytest.raises(ValueError):Case(buffer=-1)
 with pytest.raises(ValueError):Case().curves([0]*12)

def test_exact_exit_limit_detects_preserved_mesh_alias():
 path=OUT/'cases/urban55/pre_exit_limit_repair/result.json'
 if not path.exists():pytest.skip('preserved repair fixture absent')
 old=json.loads(path.read_text());c=Case('urban55',urban=55)
 m,h,e,ps=c.evaluate(old['selected']['q'],3001,True)
 assert np.min(h['urban_exit_limit'])<0
 # Original sampled disjunction passed despite the actual one-sided-limit failure.
 assert np.min(h['urban_upstream'])>0

def test_energy_scalar_regime_minimum_and_exclusion():
 from energy_bound import scalar_minimum,constants,exclusion
 for wind in [(0,0,0),(-4.876589552990943,9.64006667211232,0),(1,0,0)]:
  c=Case(wind=wind)
  for eta in [.02,.15,.22]:
   r=scalar_minimum(c,eta);C,R,u0=constants(c,eta);xs=np.linspace(200+500*eta,700-500*eta,10001)
   us=np.maximum(u0,wind[0]+np.sqrt(np.maximum(0,R-C*xs)))
   sampled=xs+2*us+us*us/(2*1.4709975)
   assert r['best']['stop_m']<=sampled.min()+1e-8
   assert sampled.min()-r['best']['stop_m']<.05
 proof=exclusion(Case(),'0.193',cells=1024)
 assert proof['excluded'] and proof['residual_lower_display_m']>0

def test_flare_height_bound_primitives():
 from integrated.clearance import polynomial_range
 B=Poly([0,0,0,-4,7,-3])
 for i in range(128):
  lo,hi=polynomial_range(B.coef.tolist(),i/128,(i+1)/128)
  assert lo>=-.2 and hi<=0
 assert 21.24+12*.7*.2+10<34

def test_certificate_refuses_domain_substitution():
 from certify import certify_case
 c=Case();q=candidate()
 with pytest.raises(ValueError):certify_case(c,q,'-0.1')
 c.p['mass_kg']*=1.01
 with pytest.raises(ValueError):certify_case(c,q,'0.01')
 q[0]=29
 with pytest.raises(ValueError):certify_case(Case(),q,'0.01')
