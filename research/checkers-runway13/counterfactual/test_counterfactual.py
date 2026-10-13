import json,sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parent))
import calculate as c
from deliver import upper_bound
from analytical.verify_full_landing_analysis import analytic
from numpy.polynomial import Polynomial

@pytest.fixture
def q():return np.array(json.loads((c.OUT/'selected.json').read_text())['selected']['q'])

@pytest.mark.parametrize('speed,frm,run,expected',[(10,0,0,[-10,0,0]),(10,180,0,[10,0,0]),(10,90,0,[0,-10,0]),(10,270,0,[0,10,0]),(10,135,135,[-10,0,0])])
def test_wind_sign(speed,frm,run,expected):np.testing.assert_allclose(c.wind_vector(speed,frm,run)/c.tr.KT,expected,atol=1e-13)

@pytest.mark.parametrize('args',[(np.nan,0,0),(1,np.inf,0),(1,0,np.nan),(-1,0,0)])
def test_bad_wind(args):
    with pytest.raises(ValueError):c.wind_vector(*args)

def test_frozen_inputs_and_corridor():
    c.check_sources();assert c.BASE_CFG['parameters']['wind_mps']['value']==[0,0,0]
    assert c.inputs()['reference_cloud_sha256']==c.hashlib.sha256(c.tr.Evaluator(c.BASE_CFG).reference_tree.data.tobytes()).hexdigest()
    assert c.P['wind_mps'][0]<0 and c.P['wind_mps'][1]>0

@pytest.mark.parametrize('bad',[[0]*11,[float('nan')]*12,[0]*12])
def test_bad_decisions(bad):
    with pytest.raises(ValueError):c.evaluate(bad)

def test_endpoints(q):
    cs=c.curves(q,c.P)
    a0=analytic(cs[0],q[0],0,c.P);a1=analytic(cs[0],q[0],1,c.P);b0=analytic(cs[1],q[1],0,c.P);b1=analytic(cs[1],q[1],1,c.P)
    np.testing.assert_allclose(a0['pos'],[-2500,1000,140],atol=1e-8)
    np.testing.assert_allclose(a1['pos'],[0,0,15.24],atol=1e-8)
    for k in ['pos','vel','acc']:np.testing.assert_allclose(a1[k],b0[k],atol=1e-8)
    np.testing.assert_allclose(b1['pos'],[q[2],0,0],atol=1e-8)
    np.testing.assert_allclose(b1['vel'],[q[3],0,-.7],atol=1e-8)
    for x in [a0,a1,b0]:assert abs(x['eas']-153)<1e-8 and abs(np.rad2deg(x['gamma'])+3.1)<1e-8

def test_scalar_rates_and_fd(q):
    for cs,T in zip(c.curves(q,c.P),q[:2]):
        for s in np.linspace(.02,.98,15):
            a=analytic(cs,T,s,c.P);v=c.phase(cs,T,np.array([s]));dt=1e-4
            for k in ['bank','thrust','roll','slew','eas','gamma']:assert abs(a[k]-v[k][0])<1e-7
            l=analytic(cs,T,s-dt/T,c.P);r=analytic(cs,T,s+dt/T,c.P)
            assert abs((r['bank']-l['bank'])/(2*dt)-a['roll'])<1e-7
            assert abs((r['thrust']-l['thrust'])/(2*dt)-a['slew'])<.1
            assert a['acceleration_residual']<1e-10

def test_coefficients_roundtrip(q):
    exp=json.loads((c.OUT/'formula.json').read_text())
    for p,cs in zip(exp['phases'],c.curves(q,c.P)):
        for values,poly in zip(p['coefficients_xyz_m'],cs):
            rec=Polynomial(values)
            for k in range(4):np.testing.assert_allclose(rec.deriv(k)(np.linspace(0,1,31)),poly.deriv(k)(np.linspace(0,1,31)),atol=1e-10)

def test_dense_replay_and_stopping(q):
    r=json.loads((c.OUT/'result.json').read_text());assert r['status']=='conditional_scenario_feasible'
    assert r['dense_eta']>0 and r['secondary_retention_passed']
    for k in ['passed','terminal_constraints_passed','path_constraints_passed','stop_constraint_passed']:assert r['independent_forward_replay'][k]
    assert abs(r['metrics']['stop_x_m']-(q[2]+2*q[3]+q[3]**2/(2*c.P['brake_deceleration_mps2'])))<1e-9
    assert r['physical_CI'] is None and r['historical_feasibility'] is None

def test_historical_closed():
    with pytest.raises(c.tr.HistoricalUnavailable):c.tr.validate_config(c.CFG,'historical')

def test_upper_bound():
    b=upper_bound();assert b['upper_exact']=='66656817/307536544';assert .21674<b['upper_display']<.21675

def test_interval_coefficients_and_air_controls(q):
    import continuous as ivc
    qs=[ivc.I(repr(float(x))) for x in q];cs=ivc.coefficients(qs)
    for i,(coeff,T) in enumerate(zip(cs,qs[:2])):
        for s in [.1,.4,.8]:
            scalar=analytic(c.curves(q,c.P)[i],q[i],s,c.P)
            vals=[[ivc.poly(ivc.deriv(cc,k),s-1e-9,s+1e-9)/T**k for cc in coeff] for k in range(4)]
            for k,key in enumerate(['pos','vel','acc']):
                for interval,value in zip(vals[k],scalar[key]):assert ivc.lo(interval)-1e-8<=value<=ivc.hi(interval)+1e-8
            m,hard,_=ivc.enclose(coeff,T,s-1e-9,s+1e-9,i,c.EV.reference_tree)
            assert hard
            expected={'eas_lower':(scalar['eas']-135)/40,'bank':1-abs(scalar['bank'])/np.deg2rad(25),'roll':1-abs(scalar['roll'])/np.deg2rad(5),'slew':1-abs(scalar['slew'])/1e5,'descent':1+scalar['gamma']/np.deg2rad(6)}
            for key,value in expected.items():assert ivc.lo(m[key])-1e-8<=value<=ivc.hi(m[key])+1e-8

def test_stale_certificate_rejected(q):
    from deliver import validate_certificate
    cert=json.loads((c.OUT/'continuous_check.json').read_text())
    validate_certificate(cert,q)
    for key in ['q_real_decimal','wind_speed_kt','wind_from_true_deg','runway_true_deg_exact','checker_source_sha256','calculator_source_sha256','reference_point_cloud_sha256','inputs_sha256','config_sha256','trajectory_source_sha256']:
        bad=dict(cert);bad[key]=None
        with pytest.raises(ValueError,match='certificate'):validate_certificate(bad,q)

def test_continuous_cover_and_gap():
    from fractions import Fraction
    cert=json.loads((c.OUT/'continuous_check.json').read_text());assert cert['certified']
    for p in [0,1]:
        spans=sorted((left,right) for phase,left,right,depth in cert['cover'] if phase==p)
        assert spans[0][0]==0 and spans[-1][1]==1
        assert all(a[1]==b[0] for a,b in zip(spans,spans[1:]))
    r=json.loads((c.OUT/'result.json').read_text())
    assert Fraction(r['global_bound']['candidate_certified_gap_upper_exact'])==Fraction(upper_bound()['upper_exact'])-Fraction(cert['eta_lower_real_decimal'])

@pytest.mark.parametrize('qbad,eta,depth',[(None,'.1',22),(['0']*11,'.1',22),(['nan']*12,'.1',22),(['[0,1]']*12,'.1',22),(['0']*12,'nan',22),(['0']*12,'[0,.1]',22),(['0']*12,'-.1',22),(['0']*12,'.1',-1)])
def test_interval_malformed_rejected(qbad,eta,depth):
    import continuous as ivc
    with pytest.raises(ValueError):ivc.validate_certificate_arguments(qbad,eta,depth)

def test_terminal_gate_survives_optimized_python(q):
    import subprocess
    script='import sys;sys.path.insert(0,'+repr(str(c.OUT))+');import continuous as x;x.certify('+repr([repr(float(x)) for x in q])+',"0.49")'
    result=subprocess.run([sys.executable,'-O','-c',script],capture_output=True,text=True)
    assert result.returncode!=0 and 'terminal margin below' in result.stderr

def setup_temp_search(tmp_path,monkeypatch):
    original=c.OUT
    for name in ['inputs.json','selected.json','search_state.json','continuous_check.json']:
        (tmp_path/name).write_bytes((original/name).read_bytes())
    monkeypatch.setattr(c,'OUT',tmp_path)
    return original

def test_failed_search_blocks_old_selection(tmp_path,monkeypatch):
    setup_temp_search(tmp_path,monkeypatch)
    old=(tmp_path/'selected.json').read_bytes()
    monkeypatch.setattr(c,'solve',lambda *a,**k:dict(success=False,sampled_exact_eta=-.1,hard_min=-.1))
    c.search()
    assert (tmp_path/'selected.json').read_bytes()==old
    assert list((tmp_path/'archive').glob('*/selected.json'))
    with pytest.raises(ValueError,match='not completed'):c.current_selection()

def test_interrupted_search_blocks_selection(tmp_path,monkeypatch):
    setup_temp_search(tmp_path,monkeypatch)
    def interrupted(*a,**k):raise KeyboardInterrupt('simulated interruption')
    monkeypatch.setattr(c,'solve',interrupted)
    with pytest.raises(KeyboardInterrupt):c.search()
    with pytest.raises(ValueError,match='failed_or_interrupted'):c.current_selection()

def test_bad_refinement_keeps_feasible_incumbent(tmp_path,monkeypatch,q):
    setup_temp_search(tmp_path,monkeypatch)
    good=dict(success=True,sampled_exact_eta=.1,hard_min=.001,q=q.tolist())
    calls=iter([good.copy() for _ in range(4)]+[dict(good,sampled_exact_eta=.2,hard_min=-1e-5),dict(good,success=False)])
    monkeypatch.setattr(c,'solve',lambda *a,**k:next(calls))
    c.search();selected=c.current_selection()
    assert selected['selected']['hard_min']>.0 and selected['selected']['sampled_exact_eta']==.1

def test_stale_certificate_failure_preserves_bundle(tmp_path,monkeypatch):
    import deliver as d
    original=setup_temp_search(tmp_path,monkeypatch)
    monkeypatch.setattr(d,'OUT',tmp_path)
    cert=json.loads((tmp_path/'continuous_check.json').read_text());cert['checker_source_sha256']='stale'
    (tmp_path/'continuous_check.json').write_text(json.dumps(cert))
    for name in ['continuous.py','calculate.py']:(tmp_path/name).write_bytes((original/name).read_bytes())
    for name in d.BUNDLE_FILES:(tmp_path/name).write_bytes(b'original-'+name.encode())
    before={name:(tmp_path/name).read_bytes() for name in d.BUNDLE_FILES}
    with pytest.raises(ValueError,match='certificate'):d.produce()
    assert before=={name:(tmp_path/name).read_bytes() for name in d.BUNDLE_FILES}

def test_generation_failure_preserves_bundle(tmp_path,monkeypatch):
    import deliver as d
    monkeypatch.setattr(d,'OUT',tmp_path)
    for name in d.BUNDLE_FILES:(tmp_path/name).write_bytes(b'original')
    def fail(stage):
        (stage/'formula.json').write_text('new')
        raise ValueError('simulated plot failure')
    monkeypatch.setattr(d,'_produce',fail)
    with pytest.raises(ValueError,match='plot'):d.produce()
    assert all((tmp_path/name).read_bytes()==b'original' for name in d.BUNDLE_FILES)

def test_publish_pointer_bundle(tmp_path,monkeypatch):
    import deliver as d
    monkeypatch.setattr(d,'OUT',tmp_path)
    for name in d.BUNDLE_FILES:(tmp_path/name).write_bytes(b'original')
    for iteration in range(2):
        stage=tmp_path/('stage'+str(iteration));stage.mkdir()
        for name in d.BUNDLE_FILES:(stage/name).write_bytes(('generation'+str(iteration)).encode())
        d.publish_bundle(stage)
        assert all((tmp_path/name).read_bytes()==('generation'+str(iteration)).encode() for name in d.BUNDLE_FILES)
        assert all((tmp_path/name).is_symlink() for name in d.BUNDLE_FILES)
    assert len(list((tmp_path/'bundles').iterdir()))==3
