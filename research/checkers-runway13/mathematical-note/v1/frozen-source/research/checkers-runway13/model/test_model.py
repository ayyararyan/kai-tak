"""Physics, boundary and fail-closed tests; no historical safety assertions."""
import copy
import numpy as np
import pytest
from .trajectory import (BASE_Q,G,KT,LB,Evaluator,HistoricalUnavailable,curves,density,
    endpoint_velocity,flight_basis,inverse,kinematics,load_config,replay,rollout,summary,validate_config)

@pytest.fixture
def cfg():return load_config()


def test_exact_mass_conversion(cfg):
    p=validate_config(cfg)
    assert p['mass_kg']==525718*LB
    assert KT==1852/3600


def test_straight_level_force_balance(cfg):
    p=validate_config(cfg)
    pos=np.array([[0,0,100.]])
    vel=np.array([[80.,0,0]])
    d=inverse(pos,vel,np.zeros((1,3)),p)
    assert d['bank_rad'][0]==0
    assert d['load_g'][0]==pytest.approx(1)
    assert d['lift_n'][0]==pytest.approx(p['mass_kg']*G)
    assert d['thrust_n'][0]==pytest.approx(d['drag_n'][0])


def test_turn_force_balance_and_bank_sign(cfg):
    p=validate_config(cfg)
    pos=np.array([[0.,0.,100.]])
    vel=np.array([[80.,0,0]])
    acc=np.array([[.4,2.,-.1]])
    d=inverse(pos,vel,acc,p)
    assert d['bank_rad'][0]>0 # right bank produces positive y acceleration
    phi=d['bank_rad'][0];L=d['lift_n'][0];T=d['thrust_n'][0];D=d['drag_n'][0]
    reconstructed=np.array([T-D,L*np.sin(phi),L*np.cos(phi)-p['mass_kg']*G])/p['mass_kg']
    np.testing.assert_allclose(reconstructed,acc[0],atol=1e-12)


def test_wind_air_heading_differs_from_track(cfg):
    cfg['parameters']['wind_mps']['value']=[0,8,0]
    p=validate_config(cfg)
    vel=endpoint_velocity(153,100,-47,-3.1,p)
    V,psi,gamma,*_=flight_basis(vel-np.array(p['wind_mps']))
    assert np.rad2deg(np.arctan2(vel[1],vel[0]))==pytest.approx(-47)
    assert np.rad2deg(psi)!=pytest.approx(-47)
    assert np.rad2deg(gamma)==pytest.approx(-3.1)
    assert V*np.sqrt(density(100,p)/p['rho0_kg_m3'])/KT==pytest.approx(153)


def test_continuous_flare_and_fixed_endpoints(cfg):
    a,f=curves(BASE_Q,cfg)
    for j in range(3):
        for order in range(3):
            assert a[j].deriv(order)(1)/BASE_Q[0]**order==pytest.approx(f[j].deriv(order)(0)/BASE_Q[1]**order,abs=1e-10)
    assert f[0](1)==pytest.approx(BASE_Q[2])
    assert f[1](1)==pytest.approx(0)
    assert f[2](1)==pytest.approx(0,abs=1e-10)
    assert f[2].deriv()(1)/BASE_Q[1]==pytest.approx(-.7)
    d=Evaluator(cfg).evaluate(BASE_Q,501)[0]
    np.testing.assert_allclose(d['bank_rad'][[0,500,-1]],0,atol=1e-10)


def test_stopping_distance_delay_and_braking(cfg):
    p=validate_config(cfg);r=rollout(BASE_Q,p)
    expected=BASE_Q[2]+BASE_Q[3]*2+BASE_Q[3]**2/(2*.15*G)
    assert r['stop_x_m']==pytest.approx(expected)
    assert r['speed_mps'][-1]==pytest.approx(0,abs=1e-10)
    i=np.flatnonzero(np.isclose(r['time_s']-BASE_Q[0]-BASE_Q[1],2))[0]
    assert r['speed_mps'][i]==pytest.approx(BASE_Q[3])
    assert r['x_m'][i]==pytest.approx(BASE_Q[2]+2*BASE_Q[3])


@pytest.mark.parametrize('key,value',[('mass_kg',0),('mass_kg',float('nan')),('initial_eas_kt',0),('eas_min_kt',180),('load_max_g',.2),('brake_deceleration_mps2',0),('wind_mps',[0,0]),('wind_mps',[0,float('inf'),0]),('thrust_max_n',-1)])
def test_invalid_configuration_rejected(cfg,key,value):
    cfg['parameters'][key]['value']=value
    with pytest.raises(ValueError):validate_config(cfg)


def test_nonconstant_wind_rejected(cfg):
    cfg['wind_type']='time-varying'
    with pytest.raises(ValueError,match='constant'):validate_config(cfg)


def test_historical_flags_cannot_bypass_gate(cfg):
    cfg['historical_inputs']={k:True for k in cfg['historical_inputs']}
    with pytest.raises(HistoricalUnavailable,match='BLOCKED'):validate_config(cfg,'historical')


@pytest.mark.parametrize('index,value',[(0,0),(1,-2),(3,0),(4,float('inf'))])
def test_invalid_trajectory_rejected(cfg,index,value):
    q=BASE_Q.copy();q[index]=value
    with pytest.raises(ValueError):kinematics(q,cfg)


def test_zero_air_velocity_rejected(cfg):
    with pytest.raises(ValueError,match='airspeed'):inverse(np.zeros((1,3)),np.zeros((1,3)),np.zeros((1,3)),validate_config(cfg))


def test_tight_bank_thrust_and_stop_expose_violations(cfg):
    cfg['parameters']['bank_limit_deg']['value']=1
    cfg['parameters']['thrust_max_n']['value']=1000
    s=summary(Evaluator(cfg).evaluate(BASE_Q,501))
    assert 'bank' in s['violations']
    assert 'thrust_upper' in s['violations']
    assert 'stop_reserve' in s['violations']
    assert not s['sampled_feasible']


def test_obstacle_intersection_exposed(cfg):
    cfg['obstacles']=[{'x_m':-2500,'y_m':1000,'radius_m':100,'height_m':200,'clearance_m':10}]
    s=summary(Evaluator(cfg).evaluate(BASE_Q))
    assert s['violations']['obstacle_0']<0


def test_dense_forward_replay(cfg):
    r=replay(Evaluator(cfg).evaluate(BASE_Q,1201),cfg)
    assert r['integration_success']
    assert r['passed'],r


def test_force_controls_replay_not_auto_accept(cfg):
    e=Evaluator(cfg).evaluate(BASE_Q,501)
    # Corrupt the supplied controls only: independent replay must detect mismatch.
    e[0]['thrust_n']+=200000
    r=replay(e,cfg)
    assert not r['passed']
    assert r['max_position_error_m']>1


def test_rollout_obstacle_exposed(cfg):
    cfg['obstacles']=[{'x_m':1800,'y_m':0,'radius_m':100,'height_m':2,'clearance_m':1}]
    s=summary(Evaluator(cfg).evaluate(BASE_Q))
    assert s['violations']['obstacle_0']<0
