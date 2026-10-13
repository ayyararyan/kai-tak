#!/usr/bin/env python3
"""Independent finite-roll quadrature/RK4 corroboration; no simulator imports."""
import cmath
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

G = 9.80665


def simpson(f, a, b, n=800):
    h = (b-a)/n
    return h/3*(f(a)+f(b)+sum((4 if i % 2 else 2)*f(a+i*h)
                               for i in range(1, n)))


def turn(U, gamma, delta, p, b):
    if not (U > 0 and -math.pi/2 < gamma <= 0 and 0 < delta < math.pi
            and p > 0 and 0 < b < math.pi/2):
        raise ValueError('Outside finite-roll theorem domain')
    k = G*math.cos(gamma)/U
    a = k/p
    q = a*(-math.log(math.cos(b)))
    if 2*q > delta+1e-12:
        raise ValueError('Peak requires negative hold duration')
    omega = k*math.tan(b)
    hold_angle = max(0, delta-2*q)
    hold = hold_angle/omega
    ramp = b/p
    I = simpson(lambda z: cmath.exp(-1j*a*math.log(math.cos(z))), 0, b)/p
    # Symmetric hold chord avoids cancellation when the hold vanishes.
    W = 2*U*(cmath.exp(-.5j*delta)*I).real + 2*U*math.sin(hold_angle/2)/omega
    Z = cmath.exp(-.5j*delta)*W
    return {'Z': Z, 'W': W, 'T': 2*ramp+hold, 'ramp': ramp,
            'hold': hold, 'k': k, 'q': q}


def match(U, gamma, delta, p, b, X, y):
    t = turn(U, gamma, delta, p, b)
    W = t['W']
    s = y/math.sin(delta)-W/(2*math.cos(delta/2))
    ell = X-y/math.tan(delta)-W/(2*math.cos(delta/2))
    D = s+ell+U*t['T']
    return {**t, 's': s, 'ell': ell, 'D': D}


def ode(U, gamma, delta, p, b, t, n=800):
    # No analytic heading formula is used by this independent integrator.
    state = [-delta, 0., 0., 0.]
    segments = [(t['ramp'], lambda u: p*u),
                (t['hold'], lambda u: b),
                (t['ramp'], lambda u: b-p*u)]
    for duration, phi in segments:
        if duration == 0:
            continue
        h = duration/n
        def f(u, z):
            return [G*math.cos(gamma)/U*math.tan(phi(u)),
                    U*math.cos(z[0]), U*math.sin(z[0]), U*math.tan(gamma)]
        for j in range(n):
            u = j*h
            k1 = f(u, state)
            k2 = f(u+h/2, [z+h*v/2 for z,v in zip(state,k1)])
            k3 = f(u+h/2, [z+h*v/2 for z,v in zip(state,k2)])
            k4 = f(u+h, [z+h*v for z,v in zip(state,k3)])
            state = [z+h*(v1+2*v2+2*v3+v4)/6 for z,v1,v2,v3,v4
                     in zip(state,k1,k2,k3,k4)]
    return state


def bisect_increasing(f, lo, hi, target):
    assert f(lo) <= target+1e-8 and f(hi) >= target-1e-8
    # Preserve exact endpoint roots. At the triangular peak D' vanishes:
    # several nearby floating peaks can evaluate to the same length.
    if f(lo) == target:
        return lo
    if f(hi) == target:
        return hi
    for _ in range(55):
        mid = (lo+hi)/2
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def run():
    rng = random.Random(20261013)
    worst = {'ode_position_m': 0., 'ode_heading_rad': 0., 'altitude_m': 0.,
             'matched_position_m': 0., 'altitude_root_bank_rad': 0.}
    samples = []
    for j in range(30):
        U = rng.uniform(40, 100)
        gamma = -math.radians(rng.uniform(0, 6))
        delta = math.radians(rng.uniform(5, 145))
        p = math.radians(rng.uniform(1, 12))
        a = G*math.cos(gamma)/(U*p)
        btri = math.acos(math.exp(-delta/(2*a)))
        bmax = min(math.radians(35), btri)
        b = bmax if j % 5 == 0 else bmax*rng.uniform(.25, .95)
        t = turn(U, gamma, delta, p, b)
        z = ode(U, gamma, delta, p, b, t)
        pe = abs(complex(z[1],z[2])-t['Z'])
        he = abs(z[0])
        ae = abs(z[3]-U*math.tan(gamma)*t['T'])
        worst['ode_position_m'] = max(worst['ode_position_m'], pe)
        worst['ode_heading_rad'] = max(worst['ode_heading_rad'], he)
        worst['altitude_m'] = max(worst['altitude_m'], ae)
        assert pe < 2e-6 and he < 1e-9 and ae < 1e-7
        s0, e0 = rng.uniform(0, 800), rng.uniform(0, 800)
        if j == 0:
            s0 = 0
        X = s0*math.cos(delta)+t['Z'].real+e0
        y = s0*math.sin(delta)-t['Z'].imag
        m = match(U,gamma,delta,p,b,X,y)
        err = math.hypot(m['s']*math.cos(delta)+z[1]+m['ell']-X,
                         y-m['s']*math.sin(delta)+z[2])
        worst['matched_position_m'] = max(worst['matched_position_m'],err)
        assert err < 2e-6 and abs(m['s']-s0) < 1e-8 and abs(m['ell']-e0) < 1e-8
        Wlim = 2*math.cos(delta/2)*min(y/math.sin(delta),X-y/math.tan(delta))
        wf = lambda peak: -turn(U,gamma,delta,p,peak)['W']
        bgeo = bisect_increasing(wf,bmax*1e-4,bmax,-Wlim)
        assert bgeo <= b+1e-10
        gf = lambda peak: match(U,gamma,delta,p,peak,X,y)
        assert abs(min(gf(bgeo)['s'],gf(bgeo)['ell'])) < 1e-7
        assert min(gf(bgeo*.999)['s'],gf(bgeo*.999)['ell']) < 0
        grid = [gf(bgeo+(bmax-bgeo)*i/30) for i in range(31)]
        if bmax-bgeo > 1e-8:
            assert all(t1['W']>t2['W'] and t1['D']<t2['D']
                       for t1,t2 in zip(grid,grid[1:]))
        H = -m['D']*math.tan(gamma)
        br = bisect_increasing(lambda peak: gf(peak)['D'],bgeo,bmax,H/(-math.tan(gamma)))
        worst['altitude_root_bank_rad'] = max(worst['altitude_root_bank_rad'],abs(br-b))
        assert abs(br-b) < 1e-7
        if j < 3:
            samples.append({'category':'synthetic','U_m_s':U,'gamma_deg':math.degrees(gamma),
                            'delta_deg':math.degrees(delta),'p_deg_s':math.degrees(p),
                            'X_m':X,'y0_m':y,'H_m':H,'bank_deg':math.degrees(b),
                            'geometric_minimum_bank_deg':math.degrees(bgeo),
                            'altitude_matched_bank_deg':math.degrees(br),
                            'initial_straight_m':m['s'],'final_straight_m':m['ell']})
    # Exact triangular boundary and just-infeasible peak.
    U,gamma,delta,p=70,-math.radians(3.1),math.radians(5),math.radians(2)
    k=G*math.cos(gamma)/U
    bt=math.acos(math.exp(-delta*p/(2*k)))
    tri=turn(U,gamma,delta,p,bt)
    assert tri['hold'] < 1e-12
    rejected=0
    for args in [(U,gamma,delta,p,bt*1.01),(U,gamma,0,p,bt),(0,gamma,delta,p,bt),
                 (U,gamma,delta,0,bt),(U,gamma,delta,p,0)]:
        try:
            turn(*args)
        except ValueError:
            rejected+=1
        else:
            raise AssertionError('Invalid input accepted')
    # Circular limit at fixed peak and gamma, with exact limiting radius.
    delta,b=math.radians(47),math.radians(20)
    R=U/(k*math.tan(b))
    limit=complex(R*math.sin(delta),R*(math.cos(delta)-1))
    limit_errors=[]
    for pfast in [1e2,1e3,1e4,1e5]:
        fast=turn(U,gamma,delta,pfast,b)
        limit_errors.append(abs(fast['Z']-limit))
    assert all(x>y for x,y in zip(limit_errors,limit_errors[1:]))
    assert limit_errors[-1] < .001
    H=124.76
    req=H/math.tan(math.radians(3.1))
    chord=math.hypot(2500,1000)
    assert req < chord
    # Constant TAS conflicts with equal EAS at unequal model densities.
    eas_ratio=math.exp((140-15.24)/(2*8500))
    assert eas_ratio>1
    return {'utc':datetime.now(timezone.utc).isoformat(),'status':'passed',
            'evidence':'synthetic quadrature vs independent RK4; no interval certification',
            'random_cases':30,'seed':20261013,'domain_rejections':rejected,
            'worst_residuals':worst,'examples':samples,
            'instantaneous_roll_position_errors_m':limit_errors,
            'frozen_constant_slope_obstruction':{'required_length_m':req,
                 'endpoint_distance_m':chord,'deficit_m':chord-req,
                 'constant_TAS_terminal_to_initial_EAS_ratio':eas_ratio,
                 'claim':'constant-slope/TAS restricted family incompatible, not v1 infeasible'},
            'checks':['turn quadrature/RK4','position matching','altitude fixed-state root',
                      'monotone W and D','geometric feasible interval boundary',
                      'triangular zero hold','invalid domain','instantaneous-roll limit',
                      'constant-slope chord obstruction','equal-EAS incompatibility'],
            'whole_landing_solution':False,'full_aircraft_envelope_verified':False}


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('finite_roll_position_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
