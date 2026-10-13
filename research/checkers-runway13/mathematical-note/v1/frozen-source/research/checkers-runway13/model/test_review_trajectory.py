"""Regression evidence for independently reviewed trajectory boundaries."""
import copy
import numpy as np
import pytest
from .trajectory import (BASE_Q, Evaluator, curves, inverse, load_config,
                         phase_derivative, replay, summary, validate_config)

# Previously saved feasible point; not an assertion of optimality.
CANDIDATE = np.array([37.4072273491302,5.0631400454252695,394.53037006867845,
    77.01370703173767,15.696730809985365,-20.582414120208266,24.939649903019756,
    7.54270603958002,48.49398114470981,-0.7867117272450713,-0.01222788205695699,
    0.018970585826368916])


@pytest.mark.parametrize('part,key', [(0,'pos'),(1,'bank'),(2,'ground_height'),
                                     (3,'stop_x_m'),(4,None)])
def test_summary_rejects_nonfinite_every_component(part,key):
    e=list(Evaluator(load_config()).evaluate(CANDIDATE))
    if key is None:
        e[part]=float('nan')
    else:
        e[part][key]=np.full_like(e[part][key],float('nan'))
    with pytest.raises(ValueError,match='nonfinite'):
        summary(e)


@pytest.mark.parametrize('mutation', [
    lambda c:c['parameters'].pop('mass_kg'),
    lambda c:c['parameters']['mass_kg'].pop('value'),
    lambda c:c['parameters']['mass_kg'].update(value=[2]),
    lambda c:c['parameters']['mass_kg'].update(value='2'),
    lambda c:c['parameters']['mass_kg'].update(source=''),
    lambda c:c['parameters']['descent_limit_deg'].update(value=180),
    lambda c:c['parameters']['threshold_gamma_deg'].update(value=-100),
    lambda c:c.update(obstacles=[None]),
])
def test_malformed_config_is_explicit_value_error(mutation):
    cfg=load_config();mutation(cfg)
    with pytest.raises(ValueError):validate_config(cfg)


def test_join_rate_keeps_larger_one_sided_derivative():
    t=np.array([0.,.25,.5,.75,1.,1.25,1.5,1.75,2.])
    phase=np.array([0,0,0,0,0,1,1,1,1])
    value=np.where(t<=1,3*t,3-7*(t-1))
    rate=phase_derivative(t,value,phase)
    assert rate[4]==pytest.approx(-7)
    np.testing.assert_allclose(rate[:4],3)
    np.testing.assert_allclose(rate[5:],-7)


def test_real_join_matches_one_sided_polynomial_force_derivatives():
    cfg=load_config();ev=Evaluator(cfg);e=ev.evaluate(BASE_Q,1201)
    rates=[]
    for polys,T,s in zip(curves(BASE_Q,cfg),BASE_Q[:2],
                         (np.array([1-1e-7,1.]),np.array([0.,1e-7]))):
        pos=np.column_stack([v(s) for v in polys])
        vel=np.column_stack([v.deriv()(s)/T for v in polys])
        acc=np.column_stack([v.deriv(2)(s)/T**2 for v in polys])
        d=inverse(pos,vel,acc,ev.p)
        rates.append(np.diff(d['thrust_n'])[0]/(1e-7*T))
    assert e[0]['thrust_slew_n_s'][1200]==pytest.approx(max(rates,key=abs),rel=2e-5)


def test_thin_obstacle_between_rollout_samples_cannot_disappear():
    cfg=load_config();e=Evaluator(cfg).evaluate(CANDIDATE)
    x=e[3]['x_m'];mid=(x[10]+x[11])/2
    assert min(abs(x-mid)) > 1
    cfg['obstacles']=[dict(x_m=float(mid),y_m=0,radius_m=.1,height_m=2,clearance_m=0)]
    tested=Evaluator(cfg).evaluate(CANDIDATE)
    assert summary(tested)['violations']['obstacle_0']==pytest.approx(-.1/400)
    r=replay(tested,cfg)
    assert not r['path_constraints_passed']
    assert r['replay_constraint_summary']['violations']['obstacle_0'] < 0


def test_replay_checks_all_constraints_independently_of_fidelity():
    cfg=load_config();e=Evaluator(cfg).evaluate(CANDIDATE,1201)
    strict=copy.deepcopy(cfg);strict['parameters']['bank_limit_deg']['value']=1
    r=replay(e,strict)
    assert r['passed']
    assert not r['path_constraints_passed']
    assert r['replay_constraint_summary']['violations']['bank'] < 0


def test_replay_feasible_candidate_still_passes():
    cfg=load_config();r=replay(Evaluator(cfg).evaluate(CANDIDATE,1201),cfg)
    assert r['passed'] and r['path_constraints_passed']
    assert r['terminal_constraints_passed'] and r['stop_constraint_passed']


def test_exact_sink_boundary_is_unresolved_not_numerically_certified():
    cfg=load_config();cfg['parameters']['touchdown_sink_mps']['value']=0
    r=replay(Evaluator(cfg).evaluate(CANDIDATE,1201),cfg)
    assert r['passed']
    assert r['terminal_constraint_status']=='boundary_unresolved'
    assert not r['terminal_constraints_passed']
    assert 'touchdown_sink_lower' in r['terminal_boundary_unresolved']
