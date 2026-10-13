#!/usr/bin/env python3
"""Synthetic corroboration of SCS proofs; stdlib only, no fitted parameters."""
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

G = 9.80665


def geometry(delta, X, y, R):
    if not (0 < delta < math.pi and R > 0):
        raise ValueError('Requires 0 < delta < pi and R > 0')
    A = math.tan(delta / 2)
    B = 2 * A - delta
    C = X + y * A
    s = y / math.sin(delta) - R * A
    ell = X - y / math.tan(delta) - R * A
    hi = min(y / (2 * math.sin(delta / 2)**2),
             (X - y / math.tan(delta)) / A)
    return s, ell, C - B * R, hi, B, C


def simpson(fn, a, b, n=2000):
    h = (b-a)/n
    return h/3*(fn(a)+fn(b)+sum((4 if i % 2 else 2)*fn(a+i*h)
                               for i in range(1, n)))


def bank(U, R, D, H):
    return math.atan(U*U*math.sqrt(1+(H/D)**2)/(G*R))


def altitude_optimum(C, B, H, lo, hi):
    if H == 0:
        return hi, None
    d0 = 2*H*math.sqrt(2/3)*math.sinh(math.asinh(
        3*math.sqrt(3)*C/(4*math.sqrt(2)*H))/3)
    return max(lo, min(hi, (C-d0)/B)), d0


def run():
    rng = random.Random(20261013)
    worst = {'endpoint_m': 0.0, 'length_m': 0.0,
             'altitude_m': 0.0, 'yaw_rad_s': 0.0,
             'normalized_cubic': 0.0}
    records = []
    count = 0
    # Build endpoint data from independent constructive straights/arc.
    for i in range(80):
        delta = math.radians(rng.uniform(2, 170))
        R = rng.uniform(10, 2000)
        s0, e0 = rng.uniform(0, 2000), rng.uniform(0, 2000)
        if i == 0:
            s0 = 0
        if i == 1:
            e0 = 0
        y = s0*math.sin(delta)+R*(1-math.cos(delta))
        X = s0*math.cos(delta)+R*math.sin(delta)+e0
        s, ell, D, hi, B, C = geometry(delta, X, y, R)
        dx = R*simpson(math.cos, -delta, 0)
        dy = R*simpson(math.sin, -delta, 0)
        err = math.hypot(s*math.cos(delta)+dx+ell-X,
                         y-s*math.sin(delta)+dy)
        worst['endpoint_m'] = max(worst['endpoint_m'], err)
        worst['length_m'] = max(worst['length_m'], abs(D-(s0+R*delta+e0)))
        assert err < 1e-7 and abs(s-s0) < 1e-7 and abs(ell-e0) < 1e-7
        assert R <= hi+1e-7 and D > 0
        sa, ea, Da, *_ = geometry(delta, X, y, hi)
        assert min(sa, ea) > -1e-7 and abs(min(sa, ea)) < 1e-7
        sx, ex, *_ = geometry(delta, X, y, hi*(1+1e-5))
        assert min(sx, ex) < 0
        radii = [hi*(0.05+0.95*j/100) for j in range(101)]
        lengths = [C-B*r for r in radii]
        banks = [bank(70, r, d, 0) for r, d in zip(radii, lengths)]
        assert all(a>b for a,b in zip(lengths, lengths[1:]))
        assert all(a>b for a,b in zip(banks, banks[1:]))
        H = rng.uniform(1, 500)
        beta = math.atan(H/D)
        U, V = 70, 70/math.cos(beta)
        phi = bank(U, R, D, H)
        n = math.cos(beta)/math.cos(phi)
        yaw = G*n*math.sin(phi)/(V*math.cos(beta))
        worst['altitude_m'] = max(worst['altitude_m'], abs(D*math.tan(beta)-H))
        worst['yaw_rad_s'] = max(worst['yaw_rad_s'], abs(yaw-U/R))
        assert abs(n*math.cos(phi)-math.cos(beta)) < 1e-12
        assert abs(yaw-U/R) < 1e-10
        opt, d0 = altitude_optimum(C, B, H, 0.05*hi, hi)
        residual = abs(d0**3+2*H*H*d0-C*H*H)/(C*H*H)
        worst['normalized_cubic'] = max(worst['normalized_cubic'], residual)
        assert residual < 1e-12
        fopt = bank(U, opt, C-B*opt, H)
        assert all(fopt <= bank(U, r, C-B*r, H)+1e-12 for r in radii)
        count += 1

    # Two visible deterministic examples. No historical aircraft interpretation.
    for label, deg, X, y, H in [
            ('47_degree_synthetic_gate', 47, 2500, 1000, 124.76),
            ('steep_170_degree_counterexample', 170,
             1000*math.sin(math.radians(170)),
             1000*(1-math.cos(math.radians(170))), 2000)]:
        delta = math.radians(deg)
        _, _, _, hi, B, C = geometry(delta, X, y, 1)
        lo = .05*hi
        opt, d0 = altitude_optimum(C, B, H, lo, hi)
        grid = [lo+(hi-lo)*i/10000 for i in range(10001)]
        value = bank(70, opt, C-B*opt, H)
        assert all(value <= bank(70, r, C-B*r, H)+1e-12 for r in grid)
        if deg == 170:
            assert lo < opt < hi
            assert value < bank(70, hi, C-B*hi, H)
        records.append({'label': label, 'category': 'synthetic',
                        'delta_deg': deg, 'X_m': X, 'y0_m': y, 'H_m': H,
                        'horizontal_speed_m_s': 70, 'radius_interval_m': [lo, hi],
                        'minimum_time_radius_m': hi,
                        'minimum_bank_radius_m': opt,
                        'minimum_bank_deg': math.degrees(value),
                        'bank_at_largest_radius_deg': math.degrees(bank(70, hi, C-B*hi, H)),
                        'minimum_bank_descent_deg': math.degrees(math.atan(H/(C-B*opt))),
                        'cubic_root_length_m': d0})
    for delta, R in [(0, 1), (math.pi, 1), (.5, 0), (.5, -1)]:
        try:
            geometry(delta, 10, 10, R)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid domain accepted')
    # Empty family and exact fixed-gamma radius recovery.
    assert geometry(.5, 1, -1, 1)[3] < 0
    _, _, D, hi, B, C = geometry(math.radians(47), 2500, 1000, 1000)
    beta = math.radians(3.1)
    H = D*math.tan(beta)
    assert abs((C-H/math.tan(beta))/B-1000) < 1e-8
    # Selectable slope interval maps correctly; compatible bounded example.
    bmin, bmax = math.radians(2), math.radians(4)
    a = max(1, (C-H/math.tan(bmin))/B)
    b = min(hi, (C-H/math.tan(bmax))/B)
    assert a <= 1000 <= b
    for r in [a, (a+b)/2, b]:
        beta_r = math.atan(H/(C-B*r))
        assert bmin-1e-12 <= beta_r <= bmax+1e-12
    assert altitude_optimum(C, B, 0, 1, hi)[0] == hi
    return {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'passed',
            'evidence': 'synthetic numerical corroboration, not certified arithmetic',
            'seed': 20261013, 'random_constructed_cases': count,
            'deterministic_examples': records, 'domain_rejections': 4,
            'checks': ['quadrature endpoint', 'length identity', 'zero-straight boundaries',
                       'outside-family rejection', 'level bank/time monotonicity',
                       'altitude identity', 'lift/yaw identity', 'cubic identity',
                       'dense family optimum comparison', 'fixed-gamma radius uniqueness',
                       'bounded slope radius interval', 'zero-altitude branch'],
            'worst_residuals': worst,
            'historical_validation': False, 'full_landing_optimality': False}


if __name__ == '__main__':
    result = run()
    out = Path(__file__).with_name('verification_results.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
