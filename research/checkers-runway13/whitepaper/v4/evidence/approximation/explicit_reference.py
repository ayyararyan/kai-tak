"""Explicit fixed-witness research reference, NOT a conditional landing policy.

Run this file to export reference_formula.json and reference_outcomes.json.
No optimization, terrain clearance, confidence/prediction interval, or operational
flight instruction is supplied. Float polynomial evaluation is not the source's
real-decimal interval proof. Scalar envelopes are exact algebra on declared boxes.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = 'analytical/coupled/continuous_certificate_refined.json'
PINNED = {
    'model/config.json': '2165902413c100923ec27e07d7ba9ef1aba62a5e1850cec84e83b8bc2d322693',
    'model/trajectory.py': '9b557ce07c7e8f177b0b3cfac1765c1c9aec4997e28b52d3185ad533f7cf3f6a',
    'analytical/verify_full_landing_analysis.py': 'fbe4067189ab78a6f1f6d4c4e8a4ac7d639dbe10c43c550d1bb37ba794202f90',
    'analytical/coupled/certify_candidate.py': '028eb9c2b39041793ff8d8973abd9e92682325e628ea9da375dc1361b963777f',
    CERTIFICATE: '774f34ad182a5015eeed799c910cde01eb6b297c1b4e6c4a119582b0d83db973',
}
SCENE_ID = 'synthetic-v1-empty-obstacles-fixed-certified-witness'
INTERVAL_KEYS = ('touchdown_x_m', 'touchdown_speed_mps', 'brake_delay_s',
                 'brake_deceleration_mps2', 'runway_length_m', 'approach_s', 'flare_s')
FORMULAS = {
    'approach_s': 'Ta', 'flare_s': 'Tf', 'touchdown_time_s': 'Ta+Tf',
    'touchdown_x_m': 'xTD', 'touchdown_speed_mps': 'u',
    'brake_delay_s': 'd', 'braking_s': 'u/a', 'ground_roll_s': 'd+u/a',
    'delay_distance_m': 'u*d', 'braking_distance_m': 'u^2/(2*a)',
    'ground_roll_m': 'u*d+u^2/(2*a)',
    'total_runway_consumed_m': 'xTD+u*d+u^2/(2*a)',
    'runway_remaining_m': 'L-xTD-u*d-u^2/(2*a)',
    'entry_to_stop_s': 'Ta+Tf+d+u/a',
    'threshold_to_stop_s': 'Tf+d+u/a',
}


def verify_sources(root=ROOT):
    """Reject any changed source, configuration or witness before evaluation."""
    root = Path(root)
    for rel, expected in PINNED.items():
        try:
            actual = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        except OSError as exc:
            raise ValueError(f'required source unavailable: {rel}') from exc
        if actual != expected:
            raise ValueError(f'source/config/witness mismatch: {rel}')
    cert = json.loads((root / CERTIFICATE).read_text())
    if (cert['config_sha256'] != PINNED['model/config.json'] or
            cert['trajectory_source_sha256'] != PINNED['model/trajectory.py'] or
            cert['certified'] is not True):
        raise ValueError('certificate provenance mismatch')
    return cert


def _number(value):
    # No coercion of booleans or strings; JSON numeric inputs only.
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.number)):
        raise ValueError('finite numeric input required')
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError('finite numeric input required') from exc
    if not math.isfinite(number):
        raise ValueError('finite numeric input required')
    return number


def _scalar_formulas(p):
    x, u, d, a, L, Ta, Tf = (p[k] for k in INTERVAL_KEYS)
    delay, brake = u*d, u*u/(2*a)
    return dict(approach_s=Ta, flare_s=Tf, touchdown_time_s=Ta+Tf,
                touchdown_x_m=x, touchdown_speed_mps=u, brake_delay_s=d,
                braking_s=u/a, ground_roll_s=d+u/a, delay_distance_m=delay,
                braking_distance_m=brake, ground_roll_m=delay+brake,
                total_runway_consumed_m=x+delay+brake,
                runway_remaining_m=L-x-delay-brake,
                entry_to_stop_s=Ta+Tf+d+u/a, threshold_to_stop_s=Tf+d+u/a)


def stopping_envelope(intervals):
    """Algebraic ranges over a caller-declared Cartesian scalar box.

    Intervals are independent coordinates in a set, NOT statistically independent
    random variables. No assertion that any/all combinations are flyable. Decimal
    spelling of supplied numbers defines exact endpoints. Endpoint expressions are
    evaluated with Fraction, then rounded outward when displayed as binary floats.
    Negative runway remaining is retained (an overrun), not clipped or approved.
    """
    if not isinstance(intervals, dict) or set(intervals) != set(INTERVAL_KEYS):
        raise ValueError(f'exactly these interval keys required: {INTERVAL_KEYS}')
    box = {}
    for k in INTERVAL_KEYS:
        pair = intervals[k]
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError(f'{k}: [lower, upper] required')
        values = [_number(v) for v in pair]
        if values[0] > values[1] or values[0] < 0:
            raise ValueError(f'{k}: ordered nonnegative interval required')
        if k in ('touchdown_speed_mps', 'brake_deceleration_mps2', 'runway_length_m') and values[0] <= 0:
            raise ValueError(f'{k}: strictly positive lower endpoint required')
        box[k] = [Fraction(str(v)) for v in pair]
    low = {k: v[0] for k, v in box.items()}
    high = {k: v[1] for k, v in box.items()}
    # All distance/time outputs increase in u,d,x,Ta,Tf and decrease in a.
    low['brake_deceleration_mps2'], high['brake_deceleration_mps2'] = box['brake_deceleration_mps2'][::-1]
    lower, upper = _scalar_formulas(low), _scalar_formulas(high)
    lower['runway_remaining_m'] = box['runway_length_m'][0] - upper['total_runway_consumed_m']
    upper['runway_remaining_m'] = box['runway_length_m'][1] - lower['total_runway_consumed_m']

    def outward(value, direction):
        try:
            f = float(value)
        except OverflowError as exc:
            raise ValueError('range exceeds finite output domain') from exc
        if not math.isfinite(f):
            raise ValueError('range exceeds finite output domain')
        if (direction < 0 and Fraction.from_float(f) > value or
                direction > 0 and Fraction.from_float(f) < value):
            f = math.nextafter(f, direction * math.inf)
        if not math.isfinite(f):
            raise ValueError('range exceeds finite output domain')
        return f

    ranges = {k: [outward(lower[k], -1), outward(upper[k], 1)] for k in lower}
    return {
        'kind': 'deterministic algebraic parameter-box range',
        'inputs': {k: list(v) for k, v in intervals.items()},
        'endpoint_semantics': 'exact decimals from numeric input spelling',
        'ranges': ranges,
        'exact_rational_ranges': {k: [str(lower[k]), str(upper[k])] for k in lower},
        'coverage_probability': None, 'statistical_prediction_interval': None,
        'flight_feasibility': 'not assessed; combinations need not be feasible flights',
        'terrain_clearance': 'not assessed', 'conditional_policy': 'not supplied',
        'formulas': FORMULAS,
    }


class ExplicitReference:
    """Read-only fixed nominal witness. Other conditions/scenes are rejected."""

    def __init__(self, *, scene_id=SCENE_ID, conditions=None):
        if scene_id != SCENE_ID or conditions is not None:
            raise ValueError('only fixed nominal witness supported; changed conditions require a new solve/certificate')
        cert = verify_sources()
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from model import trajectory as tr
        from analytical.verify_full_landing_analysis import curves
        cfg = tr.load_config(ROOT / 'model/config.json')
        p = tr.values(cfg)
        cloud = tr.Evaluator(cfg).reference_tree.data
        if hashlib.sha256(cloud.tobytes()).hexdigest() != cert['reference_point_cloud_sha256']:
            raise ValueError('reference point cloud mismatch')
        self._cert = cert
        self._q = np.array(cert['q_real_decimal'], dtype=float)
        self._polys = curves(self._q, p)
        self._inputs = dict(zip(INTERVAL_KEYS, [self._q[2], self._q[3], p['brake_delay_s'],
                            p['brake_deceleration_mps2'], p['lda_m'], self._q[0], self._q[1]]))
        self._nominal = _scalar_formulas(self._inputs)
        self._reserve = p['reserve_m']

    def phase_state(self, phase, s):
        """Position and time derivatives through jerk; s in closed [0,1]."""
        verify_sources()
        if isinstance(phase, bool) or phase not in (0, 1):
            raise ValueError('phase must be 0 (approach) or 1 (flare)')
        phase = int(phase)
        s = _number(s)
        if not 0 <= s <= 1:
            raise ValueError('normalized phase time must be in [0,1]')
        return {key: [float(poly.deriv(k)(s) / self._q[phase]**k) for poly in self._polys[phase]]
                for k, key in enumerate(('position_m', 'velocity_mps', 'acceleration_mps2', 'jerk_mps3'))}

    def state(self, time_s):
        """Entry-relative state; right-hand limits at contact/brake/stop.

        At touchdown the prescribed lumped-contact impulse removes vertical
        velocity. At braking onset/stop acceleration jumps; jerk is undefined
        there. No post-stop extrapolation.
        """
        verify_sources()
        t = _number(time_s)
        Ta, Tf = self._q[:2]
        touchdown = Ta+Tf
        if t < 0 or t > self._nominal['entry_to_stop_s']:
            raise ValueError('time outside entry-through-stop domain')
        if t < touchdown:
            ph = 0 if t < Ta else 1
            s = t/Ta if ph == 0 else (t-Ta)/Tf
            return {'phase': ('approach', 'flare')[ph], **self.phase_state(ph, s)}
        dt = t-touchdown
        d, a, u, x = (self._inputs[k] for k in ('brake_delay_s', 'brake_deceleration_mps2', 'touchdown_speed_mps', 'touchdown_x_m'))
        if t == self._nominal['entry_to_stop_s']:
            pos, v, acc, phase = self._nominal['total_runway_consumed_m'], 0., 0., 'stopped'
        elif dt < d:
            pos, v, acc, phase = x+u*dt, u, 0., 'ground_delay'
        else:
            b = dt-d
            pos, v, acc, phase = x+u*d+u*b-a*b*b/2, u-a*b, -a, 'ground_braking'
        return {'phase': phase, 'position_m': [pos, 0., 0.], 'velocity_mps': [v, 0., 0.],
                'acceleration_mps2': [acc, 0., 0.],
                'jerk_mps3': None if dt == 0 or dt == d or phase == 'stopped' else [0., 0., 0.],
                'boundary_convention': 'right-hand; contact impulse not resolved'}

    def formula(self):
        verify_sources()
        return {
            'schema_version': 1, 'scene_id': SCENE_ID,
            'scope': 'fixed synthetic research witness; not conditional policy or operational guidance',
            'source_sha256': PINNED, 'certificate_point_cloud_sha256': self._cert['reference_point_cloud_sha256'],
            'q_real_decimal': self._cert['q_real_decimal'],
            'coordinate_frame': 'x forward from displaced threshold, y right, z above runway; not georeferenced',
            'time_origin': 'scenario entry, before threshold; not beginning of entire real approach',
            'airborne_formula': 'r_i(s)=sum_{k=0}^7 c_ik*s^k; s=(t-t0)/T; derivative j = sum_{k=j}^7 c_ik*k!/(k-j)!*s^(k-j)/T^j',
            'coefficient_order': 'ascending powers in dimensionless s; each coefficient has unit metre',
            'coefficient_evidence': 'floating evaluation of exact Hermite/bump formula; not rounded-coefficient interval certification',
            'phases': [dict(name=name, start_s=float(start), duration_s=float(T),
                       coefficients_xyz_m=[np.pad(p.coef, (0, 8-len(p.coef))).tolist() for p in polys])
                       for name,start,T,polys in zip(('approach','flare'), (0., self._q[0]), self._q[:2], self._polys)],
            'ground_formula': 'tau=t-(Ta+Tf); x=xTD+u*tau for 0<=tau<=d; x=xTD+u*d+u*(tau-d)-a*(tau-d)^2/2 for d<=tau<=d+u/a; y=z=0',
            'ground_contact': 'inelastic removal of vertical velocity at touchdown; fixed constant-speed delay then constant deceleration',
            'scalar_inputs': self._inputs, 'scalar_formulas': FORMULAS,
            'conditional_policy_status': 'unresolved', 'historical_clearance_status': 'blocked',
            'near_optimality_status': 'unresolved; prior 0.03972 bound withdrawn',
        }

    def outcomes(self):
        verify_sources()
        return {
            'schema_version': 1, 'scene_id': SCENE_ID, 'source_sha256': PINNED,
            'category': 'scenario-based deterministic evaluation', 'nominal': self._nominal,
            'required_reserve_m': self._reserve,
            'excess_over_required_reserve_m': self._nominal['runway_remaining_m']-self._reserve,
            'distance_semantics': 'ground_roll includes delay; total_runway_consumed is threshold-to-stop x, including airborne flare over runway; not total 3D path length',
            'time_origin': 'synthetic entry state; approach_s ends at threshold; flare_s ends at touchdown',
            'nominal_all_time_margin_source': {'lower': self._cert['eta_lower_real_decimal'], 'domain': self._cert['domain'],
                'note': 'existing source certificate; not newly proved by floating exporter'},
            'uncertainty': {'prediction_intervals': None, 'coverage_probability': None,
                'measurement_uncertainty': None, 'model_discrepancy': None, 'tracking_error': None,
                'reason': 'no supplied distributions, calibrated model/tracking errors or held-out coverage evidence'},
            'approximation_error': {'conditional_rule': None, 'note': 'no fitted conditional rule; floating numerical consistency is not physical error'},
            'optimality': {'globally_near_optimal': False, 'gap_status': 'unresolved', 'accepted_tolerance': None},
            'historical_feasibility': 'blocked: dated registered geometry, swept aircraft/tracking and calibration unresolved',
            'final_solution_status': 'incomplete',
        }


def export():
    ref = ExplicitReference()
    folder = Path(__file__).resolve().parent
    for name, payload in [('reference_formula.json', ref.formula()), ('reference_outcomes.json', ref.outcomes())]:
        (folder/name).write_text(json.dumps(payload, indent=2, allow_nan=False)+'\n')
    return ref.outcomes()['nominal']


if __name__ == '__main__':
    print(json.dumps(export(), indent=2))
