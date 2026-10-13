"""Independent evaluator, boundary, domain, provenance and algebraic box tests."""
import itertools
import json
import math
import shutil
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import pytest
from explicit_reference import (ExplicitReference, INTERVAL_KEYS, PINNED, ROOT,
                                SCENE_ID, stopping_envelope, verify_sources)

@pytest.fixture(scope='module')
def ref():
    return ExplicitReference()


def test_independent_full_state(ref):
    from model import trajectory as tr
    q=np.array(verify_sources()['q_real_decimal'],dtype=float)
    curves=tr.curves(q,tr.load_config())  # original uses matrix solve, not explicit coefficients
    for phase in (0,1):
        for s in np.r_[np.linspace(0,1,101),1e-9,1-1e-9]:
            state=ref.phase_state(phase,float(s))
            for k,key in enumerate(('position_m','velocity_mps','acceleration_mps2','jerk_mps3')):
                expected=[p.deriv(k)(s)/q[phase]**k for p in curves[phase]]
                np.testing.assert_allclose(state[key],expected,atol=2e-8,rtol=1e-10)


def test_endpoints_joins_and_absolute_time(ref):
    from model import trajectory as tr
    p=tr.values(tr.load_config());nom=ref.outcomes()['nominal']
    first,left,right,last=[ref.phase_state(i,s) for i,s in [(0,0),(0,1),(1,0),(1,1)]]
    np.testing.assert_allclose(first['position_m'],p['start_xyz_m'],atol=1e-10)
    for key in ('position_m','velocity_mps','acceleration_mps2'):
        np.testing.assert_allclose(left[key],right[key],atol=2e-8)
    np.testing.assert_allclose(right['position_m'],[0,0,p['threshold_height_m']],atol=1e-10)
    np.testing.assert_allclose(last['position_m'],[nom['touchdown_x_m'],0,0],atol=2e-8)
    np.testing.assert_allclose(last['velocity_mps'],[nom['touchdown_speed_mps'],0,-p['touchdown_sink_mps']],atol=2e-8)
    np.testing.assert_allclose(last['acceleration_mps2'],0,atol=2e-8)
    assert np.linalg.norm(np.array(left['jerk_mps3'])-right['jerk_mps3'])>1e-4
    for i in (0,1):
        T=nom['approach_s'] if i==0 else nom['flare_s']; start=0 if i==0 else nom['approach_s']
        for s in (0,.23,.6,.999):
            np.testing.assert_allclose(ref.state(start+s*T)['position_m'],ref.phase_state(i,s)['position_m'],atol=2e-8)
    assert ref.state(nom['approach_s'])['phase']=='flare'


def test_ground_and_scalar_outcomes(ref):
    from model import trajectory as tr
    q=np.array(verify_sources()['q_real_decimal'],dtype=float)
    roll=tr.rollout(q,tr.values(tr.load_config()),n=107);nom=ref.outcomes()['nominal']
    for t,x,u in zip(roll['time_s'],roll['x_m'],roll['speed_mps']):
        got=ref.state(min(float(t),nom['entry_to_stop_s']))
        np.testing.assert_allclose(got['position_m'],[x,0,0],atol=2e-9)
        np.testing.assert_allclose(got['velocity_mps'],[u,0,0],atol=2e-9)
    assert abs(nom['total_runway_consumed_m']-roll['stop_x_m'])<1e-9
    assert abs(nom['runway_remaining_m']-roll['reserve_remaining_m'])<1e-9
    assert nom['ground_roll_m']==nom['delay_distance_m']+nom['braking_distance_m']
    assert math.isclose(nom['total_runway_consumed_m'],nom['touchdown_x_m']+nom['ground_roll_m'],abs_tol=1e-10)
    assert math.isclose(nom['entry_to_stop_s'],nom['touchdown_time_s']+nom['ground_roll_s'],abs_tol=1e-10)
    assert ref.state(nom['touchdown_time_s'])['jerk_mps3'] is None
    assert ref.state(nom['touchdown_time_s'])['velocity_mps'][2]==0
    assert ref.state(nom['entry_to_stop_s'])['velocity_mps']==[0,0,0]


def sample_box():
    # Artificial TEST fixture, not data-derived/model uncertainty.
    return dict(zip(INTERVAL_KEYS,[[280,350],[70,85],[1,3],[1.1,1.8],[2600,2900],[32,45],[4,7]]))


def test_all_128_corners_exact_enclosure():
    box=sample_box();result=stopping_envelope(box)
    for corner in itertools.product(*box.values()):
        x,u,d,a,L,Ta,Tf=map(lambda v:F(str(v)),corner)
        expected=dict(approach_s=Ta,flare_s=Tf,touchdown_time_s=Ta+Tf,
            touchdown_x_m=x,touchdown_speed_mps=u,brake_delay_s=d,
            braking_s=u/a,ground_roll_s=d+u/a,delay_distance_m=u*d,
            braking_distance_m=u*u/(2*a),ground_roll_m=u*d+u*u/(2*a),
            total_runway_consumed_m=x+u*d+u*u/(2*a),runway_remaining_m=L-x-u*d-u*u/(2*a),
            entry_to_stop_s=Ta+Tf+d+u/a,threshold_to_stop_s=Tf+d+u/a)
        for key,value in expected.items():
            lo,hi=result['ranges'][key];rlo,rhi=map(F,result['exact_rational_ranges'][key])
            assert F.from_float(lo)<=value<=F.from_float(hi)
            assert rlo<=value<=rhi
    assert result['coverage_probability'] is None
    assert result['statistical_prediction_interval'] is None
    assert result['ranges']['runway_remaining_m'][0]<0


def test_nominal_point_box(ref):
    result=stopping_envelope({k:[v,v] for k,v in ref.formula()['scalar_inputs'].items()})
    for key,value in ref.outcomes()['nominal'].items():
        lo,hi=result['ranges'][key]
        assert math.isclose(value,lo,rel_tol=2e-15,abs_tol=1e-10)
        assert math.isclose(value,hi,rel_tol=2e-15,abs_tol=1e-10)
        assert result['exact_rational_ranges'][key][0]==result['exact_rational_ranges'][key][1]

@pytest.mark.parametrize('bad',[[2,1],[-1,2],[float('nan'),2],[1,float('inf')],[True,2],['1',2],[1],None])
def test_invalid_intervals(bad):
    box=sample_box();box['brake_delay_s']=bad
    with pytest.raises(ValueError):stopping_envelope(box)

@pytest.mark.parametrize('key',['brake_deceleration_mps2','touchdown_speed_mps','runway_length_m'])
def test_strict_positive_inputs(key):
    box=sample_box();box[key]=[0,1]
    with pytest.raises(ValueError):stopping_envelope(box)


def test_schema_and_overflow():
    box=sample_box();del box['approach_s']
    with pytest.raises(ValueError):stopping_envelope(box)
    box=sample_box();box['unknown']=[0,1]
    with pytest.raises(ValueError):stopping_envelope(box)
    box=sample_box();box['touchdown_speed_mps']=[1e308,1e308]
    with pytest.raises(ValueError):stopping_envelope(box)

@pytest.mark.parametrize('bad',[-1,float('nan'),float('inf'),True,'0'])
def test_invalid_time(ref,bad):
    with pytest.raises(ValueError):ref.state(bad)


def test_no_extrapolation_or_condition_reuse(ref):
    with pytest.raises(ValueError):ref.state(ref.outcomes()['nominal']['entry_to_stop_s']+1)
    for phase,s in [(2,.5),(True,.5),(0,-.1),(1,1.01)]:
        with pytest.raises(ValueError):ref.phase_state(phase,s)
    for conditions in ({},{'wind_mps':[1,0,0]}):
        with pytest.raises(ValueError):ExplicitReference(conditions=conditions)
    with pytest.raises(ValueError):ExplicitReference(scene_id='Hong Kong 1993')

@pytest.mark.parametrize('changed',list(PINNED))
def test_source_config_witness_tamper(tmp_path,changed):
    for rel in PINNED:
        target=tmp_path/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/rel,target)
    with (tmp_path/changed).open('a') as out:out.write('\n')
    with pytest.raises(ValueError,match='mismatch'):verify_sources(tmp_path)


def test_missing_source(tmp_path):
    with pytest.raises(ValueError,match='unavailable'):verify_sources(tmp_path)


def test_artifact_semantics(ref):
    for name,expected in [('reference_formula.json',ref.formula()),('reference_outcomes.json',ref.outcomes())]:
        actual=json.loads((Path(__file__).parent/name).read_text())
        assert actual==expected
        assert actual['source_sha256']==PINNED
        assert actual['scene_id']==SCENE_ID
    out=ref.outcomes()
    assert out['uncertainty']['prediction_intervals'] is None
    assert out['uncertainty']['coverage_probability'] is None
    assert out['final_solution_status']=='incomplete'
    assert not out['optimality']['globally_near_optimal']
