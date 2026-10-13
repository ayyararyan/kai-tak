"""Endpoint-semantics and registration diagnostics, never an accepted runway frame."""
from pathlib import Path
import json, hashlib, math
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def unit_bearing(deg):
    b = math.radians(deg)
    return np.array([math.sin(b), math.cos(b)])

def residual(north, south, bearing, lda, extra_pavement=0.0):
    north, south = np.asarray(north, float), np.asarray(south, float)
    u = unit_bearing(bearing)
    back = south - (lda + extra_pavement) * u
    d = north - back
    right = np.array([-u[1], u[0]])
    return dict(back_projected_EN_m=back.tolist(),
                difference_EN_m=d.tolist(), along_m=float(d @ u),
                right_m=float(d @ right), norm_m=float(np.linalg.norm(d)),
                extra_pavement_m=extra_pavement,
                accepted_historical_registration=False,
                physical_error_bound_m=None)

def build():
    paths = [
        ROOT/'integrated/geometry/runway_crosscheck.json',
        ROOT/'integrated/geometry/mapped_runway_axis_check.json',
        ROOT/'integrated/geometry/runway_registration_diagnostic.json',
        ROOT/'integrated/geometry/south_registration_diagnostic.json',
        ROOT/'../../data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf',
        ROOT/'integrated/sources/appendix9_followup.png',
        OUT/'appendix14_controlblock.png',
    ]
    cross, axis, northern = [json.loads(p.read_text()) for p in paths[:3]]
    n = np.array(cross['north_pick']['derived_EN_m'])
    s = np.array(cross['south_picks']['end_EN_m'])
    lda = cross['back_projection']['assumed_distance_m']
    bearing = axis['mean_mapped_grid_bearing_deg']
    distance = float(np.linalg.norm(s-n))
    controls = northern['controls']
    x = np.array([v['source_photo_pixel_xy'] for v in controls])
    y = np.array([v['map_EN_m'] for v in controls])
    fit = np.array([v['role']=='fit' for v in controls])
    threshold_px = cross['north_pick']['original_A36143_pixel_xy']
    target = axis['threshold_crosscheck_with_mapped_axis']['back_projected_EN_m']
    influence = []
    for i in np.where(fit)[0]:
        f = fit.copy(); f[i] = False
        # Centering prevents large map offsets from degrading the condition check.
        center = x[f].mean(axis=0)
        X = np.c_[x-center, np.ones(len(x))]
        a = np.linalg.lstsq(X[f], y[f], rcond=None)[0]
        t = np.r_[np.array(threshold_px)-center, 1] @ a
        holdout = X[~fit] @ a - y[~fit]
        influence.append(dict(omitted=controls[i]['id'],
                              threshold_EN_m=t.tolist(),
                              mismatch_with_uncorrected_south_m=float(np.linalg.norm(t-target)),
                              heldout_RMS_m=float(np.sqrt(np.mean(np.sum(holdout**2,axis=1))))))
    return dict(
        status='diagnostic_only_endpoint_semantics_unresolved',
        original_artifacts_preserved=True,
        source_sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        lda_m=lda,
        fitted_endpoint_distance_m=distance,
        minimum_disagreement_over_all_bearings_m=abs(distance-lda),
        minimum_disagreement_proof='Reverse triangle inequality: min over unit u ||n-(s-Lu)|| = abs(||s-n||-L). This is exact for supplied fitted points, not ground truth.',
        uncorrected_mapped_axis=residual(n,s,bearing,lda),
        concrete_extension_hypothesis=dict(
            primary_paved_concrete_length_m=152,
            primary_declared_runway_last_concrete_length_m=91,
            conditional_difference_m=61,
            basis='CAD1/95 Appendix9 southeast concrete label152m; section1.10.1 printed27 last91m of runway concrete; strip3392.5 versus runway3331.5 also differs61m.',
            missing_link='The scan does not explicitly identify a surveyed61m declared-end-to-selected-pavement-end vector. Same concrete section and endpoint interpretation require confirmation.',
            category='source-backed hypothesis; not observed surveyed offset',
            mapped_axis_result=residual(n,s,bearing,lda,61),
            short_axis_result=residual(n,s,cross['south_picks']['axis_grid_bearing_deg'],lda,61),
            minimum_disagreement_over_all_bearings_m=abs(distance-(lda+61))),
        north_fit_leave_one_out=influence,
        accepted_threshold_EN_m=None,
        physical_ground_accuracy_m=None,
        aviation_to_HKPD_offset_m=None,
        historical_clearance_ready=False,
        cautions=[
            'No change to2786mLDA or frozen braking/objective.',
            'A reduced residual does not validate the endpoint hypothesis or the camera fits.',
            'Do not choose an offset equal to the measured residual merely to close the gap.',
            'Cross-check is not two surveyed thresholds; it combines distinct image fits and an unverified endpoint semantic link.',
            'Leave-one-out instability identifies weak control geometry, not a probabilistic confidence interval.'
        ])

if __name__ == '__main__':
    r=build()
    (OUT/'threshold_diagnosis.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['fitted_endpoint_distance_m','minimum_disagreement_over_all_bearings_m','uncorrected_mapped_axis','concrete_extension_hypothesis']},indent=2))
