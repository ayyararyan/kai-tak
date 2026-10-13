"""Independent V5 display arithmetic and frozen-science integrity checks.

No optimization, historical reconstruction or source mutation occurs here. This
checks exported floating curves, not the exact-real proof object. Use the separate
verify_certificates.py for fresh all-time fixed-witness proofs.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import csv
import datetime
import hashlib
import json
import itertools
import math
import sys

import numpy as np

P = Path(__file__).resolve().parents[1]
E = P / "evidence"
Q = P / "qa"
CHECKS = []
VALUES = {}


def load(path):
    return json.loads((P / path).read_text())


def rows(path):
    with (P / path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def near(name, actual, expected, tolerance=1e-8):
    check(name, bool(np.max(np.abs(np.asarray(actual) - expected)) <= tolerance))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def curve(phase, s, derivative=0):
    return np.column_stack([
        np.polynomial.polynomial.polyval(
            s, np.polynomial.polynomial.polyder(c, derivative)
        ) / phase["duration_s"] ** derivative
        for c in phase["coefficients_xyz_m"]
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh-bound", action="store_true",
                        help="Rerun original outward-rounded calm bound without writing its source")
    args = parser.parse_args()
    Q.mkdir(exist_ok=True)
    original_ledger = rows("editorial/V4_CLAIMS_AND_EVIDENCE.csv")
    active_ledger = rows("CLAIMS_AND_EVIDENCE.csv")
    baseline_by_id = {r["claim_id"]: r for r in original_ledger}
    active_by_id = {r["claim_id"]: r for r in active_ledger}
    check("baseline_51_claim_ids_retained", len(baseline_by_id) == 51 and
          set(baseline_by_id) <= set(active_by_id))
    check("active_claim_ids_unique", len(active_by_id) == len(active_ledger))
    check("baseline_50_scientific_claim_texts_preserved", all(
        r["claim"] == active_by_id[key]["claim"] for key, r in baseline_by_id.items() if key != "C01"))
    check("baseline_scientific_scope_preserved", all(
        r["scope_limit"] == active_by_id[key]["scope_limit"] for key, r in baseline_by_id.items() if key != "C01"))
    check("all_active_claim_supporting_files_resolve", all((P / name.strip()).is_file()
        for r in active_ledger for name in r["supporting_files"].split(";")))
    for item in load("SOURCE_MANIFEST.json")["files"]:
        check("frozen_sha256:" + item["path"], sha(P / item["path"]) == item["sha256"])
    for item in load("evidence_manifest.json")["files"]:
        if "snapshot" in item:
            check("snapshot_sha256:" + item["snapshot"], sha(P / item["snapshot"]) == item["sha256"])
    historical_inputs = load("inputs/historical/SOURCE_MANIFEST.json")["records"]
    for item in historical_inputs:
        check("visual_input_sha256:" + item["snapshot"], sha(P / item["snapshot"]) == item["sha256"])
    for frame in ("CN4581", "CN4589"):
        item = next(r for r in historical_inputs if r.get("frame_id") == frame)
        check(frame + "_catalogue_epoch", item["catalogue_date"] ==
              item["metadata_record"]["capture_date"] == "1993-10-08")
        check(frame + "_compressed_source_tier", item["metadata_record"]["product"] == "DAP-L0"
              and item["metadata_record"]["full_resolution_photogrammetric_scan"] is False)
    sparse = rows("inputs/historical/sparse_stereo_points.csv")
    labels = load("inputs/historical/manual_stereo_labels.json")["labels"]
    roof_examples = {}
    for track, expected_z in ((26, 10.769431630259533), (1135, 19.195490912459263)):
        point = next(r for r in sparse if int(r["track_id"]) == track)
        label = next(r for r in labels if r["fundamental_inlier_row"] == track)
        near(f"stereo_roof_{track}_relative_height", float(point["z_above_fitted_local_park_road_plane_m"]), expected_z, 1e-12)
        check(f"stereo_roof_{track}_outside_control_hull", point["within_map_control_hull"] == "False")
        check(f"stereo_roof_{track}_accepted_manual_role", label["role"] == "roof_observed")
        for frame in (42, 43):
            near(f"stereo_roof_{track}_frame{frame}_correspondence",
                 [float(point[f"frame{frame}_x"]), float(point[f"frame{frame}_y"])],
                 np.array(label[f"frame{frame}_xy"]), 1e-12)
        roof_examples[str(track)] = dict(relative_plane_height_m=expected_z,
                                        within_map_control_hull=False,
                                        source_interpretation=label["observed_surface"])
    VALUES["new_visual_inputs"] = dict(hash_verified_count=len(historical_inputs),
                                      supplemental_photo_epoch="1993-10-08", roof_examples=roof_examples)

    g = 9.80665
    kt = 1852 / 3600
    p = {k: v["value"] for k, v in load("evidence/model/config.json")["parameters"].items()}
    near("mass_conversion", p["mass_kg"], 525718 * 0.45359237, 1e-9)
    near("fixed_deceleration", p["brake_deceleration_mps2"], 0.15 * g, 1e-14)
    check("fixed_delay_LDA_reserve", (p["brake_delay_s"], p["lda_m"], p["reserve_m"]) == (2, 2786, 150))

    radius = 78 ** 2 / (g * math.tan(math.radians(15)))
    arc = radius * math.radians(47)
    VALUES["turn"] = dict(radius_m=radius, time_s=arc / 78, arc_m=arc,
                          load_factor=1 / math.cos(math.radians(15)),
                          straight_descent_mps=78 * math.sin(math.radians(-3.1)))
    near("turn_display_radius", radius, 2315.347, .001)
    near("turn_display_time", arc / 78, 24.3499, .0001)
    near("quadratic_braking_ratio", 1.1 ** 2, 1.21, 1e-14)

    calm = load("evidence/approximation/reference_formula.json")
    calm_result = load("evidence/approximation/reference_outcomes.json")
    wind = load("evidence/counterfactual/formula.json")
    wind_result = load("evidence/counterfactual/result.json")
    wind_input = load("evidence/counterfactual/inputs.json")
    w = -21 * kt * np.array([math.cos(math.radians(70 - 799 / 6)),
                            math.sin(math.radians(70 - 799 / 6)), 0])
    near("wind_from_bearing_sign_and_rotation", w, wind_input["wind_runway_mps"], 1e-13)
    projections = {}
    for chi in (-47, 0):
        a = math.radians(chi)
        projections[str(chi)] = {"along_mps": float(w @ [math.cos(a), math.sin(a), 0]),
                                 "right_mps": float(w @ [-math.sin(a), math.cos(a), 0])}
    VALUES["wind_projection"] = dict(runway_vector_mps=w.tolist(), track_projections=projections)

    for name, formula, wind_vector in (("calm", calm, np.zeros(3)), ("wind", wind, w)):
        a, b = formula["phases"]
        for d in range(3):
            near(f"{name}_phase_join_derivative_{d}", curve(a, [1], d), curve(b, [0], d), 1e-8)
        near(f"{name}_entry", curve(a, [0]), [[-2500, 1000, 140]])
        near(f"{name}_threshold", curve(a, [1]), [[0, 0, 15.24]])
        for phase, s in ((a, 0), (a, 1), (b, 0)):
            pos = curve(phase, [s])[0]
            vel = curve(phase, [s], 1)[0] - wind_vector
            eas = np.linalg.norm(vel) * math.exp(-pos[2] / 17000) / kt
            gamma = math.degrees(math.asin(vel[2] / np.linalg.norm(vel)))
            near(f"{name}_{phase['name']}_{s}_EAS", eas, 153, 1e-7)
            near(f"{name}_{phase['name']}_{s}_gamma", gamma, -3.1, 1e-7)
        state = curve(b, [1])[0]
        vel = curve(b, [1], 1)[0]
        near(f"{name}_touchdown_lateral_vertical", state[1:], [0, 0])
        near(f"{name}_touchdown_lateral_sink_velocity", vel[1:], [0, -.7])
        xd, u = float(state[0]), float(vel[0])
        delay = u * 2
        braking = u ** 2 / (2 * .15 * g)
        stop = xd + delay + braking
        stop_time = a["duration_s"] + b["duration_s"] + 2 + u / (.15 * g)
        expected = calm_result["nominal"] if name == "calm" else wind_result["metrics"]
        near(f"{name}_stopping_remainder", 2786 - stop, expected["runway_remaining_m"], 1e-7)
        near(f"{name}_stopping_time", stop_time, expected["entry_to_stop_s" if name == "calm" else "stop_time_s"], 1e-8)
        check(f"{name}_reserve", 2786 - stop > 150)
        # A positive rise is retained, not removed by a smoothing/monotonicity edit.
        max_climb = max(float(np.max(curve(ph, np.linspace(0, 1, 1001), 1)[:, 2])) for ph in (a, b))
        check(f"{name}_brief_climb_retained", max_climb > 0)
        VALUES[name] = dict(touchdown_x_m=xd, touchdown_groundspeed_mps=u,
                            delay_distance_m=delay, braking_distance_m=braking,
                            stop_x_m=stop, remaining_m=2786-stop,
                            entry_to_stop_s=stop_time, sampled_max_climb_mps=max_climb,
                            dR_du=-2-u/(.15*g), dR_dd=-u)

    data = rows("evidence/counterfactual/path_controls.csv")
    for phase in wind["phases"]:
        selected = [r for r in data if r["phase"] == phase["name"]]
        s = (np.array([float(r["time_s"]) for r in selected]) - phase["t0_s"]) / phase["duration_s"]
        position, velocity = curve(phase, s), curve(phase, s, 1)
        near(phase["name"] + "_wind_csv_position", position,
             np.array([[float(r[k]) for k in ("x_m", "y_m", "z_m")] for r in selected]))
        near(phase["name"] + "_wind_csv_velocity", velocity,
             np.array([[float(r[k]) for k in ("vx_mps", "vy_mps", "vz_mps")] for r in selected]))
        eas = np.linalg.norm(velocity - w, axis=1) * np.exp(-position[:, 2] / 17000) / kt
        near(phase["name"] + "_wind_csv_eas", eas, np.array([float(r["eas_kt"]) for r in selected]))

    for name, path, count, eta in (
        ("calm", "evidence/analytical/coupled/continuous_certificate_refined.json", 2502, "0.0397"),
        ("wind", "evidence/counterfactual/continuous_check.json", 376, "0.1507934696816132"),
    ):
        cert = load(path)
        check(name + "_frozen_certificate_identity", cert["certified"] and cert["eta_lower_real_decimal"] == eta)
        check(name + "_certificate_interval_count", len(cert["cover"]) == count)
        for ph in (0, 1):
            spans = sorted((r[1], r[2]) for r in cert["cover"] if r[0] == ph)
            check(f"{name}_{ph}_closed_cover", spans[0][0] == 0 and spans[-1][1] == 1 and
                  all(a[1] == b[0] for a, b in zip(spans, spans[1:])))

    upper = (Fraction(2636-200-138) - Fraction(69**2) / (2*Fraction("1.4709975"))) / 3136
    lower = Fraction("0.1507934696816132")
    check("wind_upper_independent_rational", upper == Fraction(66656817, 307536544))
    check("wind_gap_independent_rational", upper-lower == Fraction(wind_result["global_bound"]["candidate_certified_gap_upper_exact"]))
    VALUES["wind_bound"] = dict(upper_exact=str(upper), gap_exact=str(upper-lower), gap=float(upper-lower))
    VALUES["scenario_difference"] = dict(
        remaining_m=VALUES["wind"]["remaining_m"]-VALUES["calm"]["remaining_m"],
        touchdown_m=VALUES["calm"]["touchdown_x_m"]-VALUES["wind"]["touchdown_x_m"],
        ground_travel_m=sum(VALUES["calm"][k]-VALUES["wind"][k] for k in ("delay_distance_m", "braking_distance_m")),
        interpretation="separately optimized scenarios, not causal wind effect")
    diff = VALUES["scenario_difference"]
    near("scenario_difference_decomposition", diff["remaining_m"], diff["touchdown_m"]+diff["ground_travel_m"])

    obstacle = load("evidence/reconstruction/obstacles/readiness.json")
    check("obstacle_scope", (obstacle["accepted_source_observations"], obstacle["distinct_digitized_sites"],
          obstacle["complete_obstacle_volumes"], obstacle["physical_upper_bounds_available"],
          obstacle["historical_clearance_ready"]) == (24, 12, 0, 0, False))
    stereo = rows("evidence/stereo_plot_data.csv")
    check("stereo_every_fifth_display_count", len(stereo) == 34262)
    handoff = load("evidence/reconstruction/block_matching/HANDOFF.json")
    check("stereo_retained_count", (handoff["dense_points"], handoff["dense_points_inside_control_hull"], handoff["surface_triangles"], handoff["clearance_certified"]) == (171307, 3780, 225371, False))
    VALUES["control_hull_share"] = 3780 / 171307
    check("digitized_anchors_count", len(rows("evidence/evidence/cal605_reconstruction/flight/flight_anchor_readings.csv")) +
          len(rows("evidence/evidence/cal605_reconstruction/flight/approach_anchor_readings.csv")) == 190)
    flight_summary = load("evidence/evidence/cal605_reconstruction/flight/flight_summary.json")
    # Published-plot calibration: 566px=0s, 1573px=70s; first ground indication
    # read at 1012px. These are retained original digitization choices, not new
    # readings or a sensor/physical-time uncertainty model.
    flag_time = (1012-566)/(1573-566)*70
    flag_corners = [(x-a)/(b-a)*70 for x, a, b in
                    itertools.product((1009, 1015), (563, 569), (1570, 1576))]
    flag_range = [min(flag_corners), max(flag_corners)]
    near("ground_flag_datum_B_affine_calibration", flag_time, flight_summary["touchdown_flag_datum_B_s"], 1e-12)
    near("ground_flag_raster_reading_range", flag_range,
         np.array(flight_summary["touchdown_flag_reading_range_s"]), 1e-12)
    VALUES["ground_indication_reading"] = dict(datum_B_s=flag_time, range_s=flag_range,
         scope="Declared raster-reading sensitivity only; not exact physical touchdown or sensor uncertainty")
    weather = rows("evidence/weather_plot_data.csv")
    selected = [r for r in weather if r["report_type"] == "FM-15" and r["source_flag"] == "4" and
                r["datetime_utc"][14:19] == "00:00" and r["wind_type"] == "N" and r["wind_speed_mps"] and
                r["wind_speed_mps_strict_qc_accepted"] == "True" and r["partial_weather_row"] == "False"]
    v = np.array([float(r["wind_speed_mps"]) for r in selected])
    check("weather_year_event_routine_counts", (len(weather), sum(r["datetime_utc"].startswith("1993-11-04") for r in weather), len(selected)) == (8549, 24, 8360))
    check("weather_empirical_rank_counts", tuple(int(x) for x in ((v<10.8).sum(), (v==10.8).sum(), (v>10.8).sum())) == (8285, 17, 58))
    for hour, gust in (("03", 17.5), ("04", 20.6)):
        r = next(r for r in weather if r["datetime_utc"] == f"1993-11-04T{hour}:00:00Z")
        check("event_weather_"+hour, float(r["wind_speed_mps"]) == 10.8 and float(r["gust_mps"]) == gust)
    ground_wind = rows("evidence/evidence/cal605_reconstruction/wind/wind_records.csv")
    check("ground_wind_pairs", len(ground_wind) == 225)
    for time, sensor, field, speed in (("03:35:30", "NW", "A", 37), ("03:35:30", "NW", "B", 23),
                                     ("03:35:30", "NW", "C", 19), ("03:38:00", "NW", "A", 12), ("03:38:00", "LYM", "A", 37)):
        r = next(r for r in ground_wind if (r["wind_clock_time"], r["sensor"], r["field"]) == (time, sensor, field))
        check(f"wind_record_{time}_{sensor}_{field}", float(r["speed_kt_printed"]) == speed)
    historical = load("evidence/evidence/cal605_reconstruction/analysis.json")
    for r in historical["fixed_formula"]:
        speed = r["touchdown_speed_kt"] * kt
        remainder = 2786-r["touchdown_x_m"]-speed*r["delay_s"]-speed**2/(2*r["deceleration_g"]*g)
        near("historical_conditional_"+r["case"], remainder, r["remaining_m"])
    for i, r in enumerate(historical["report_landmark_stopping_frontier"]):
        speed = r["speed_kt"] * kt
        for lag, key in ((0, "required_decel_no_delay_g"), (2, "required_decel_with_2s_delay_g")):
            near(f"historical_frontier_{i}_{lag}", speed**2/(2*(r["remaining_m"]-speed*lag))/g, r[key], 1e-12)
    if args.fresh_bound:
        sys.path.insert(0, str(E / "analytical/coupled"))
        import existence_and_bounds as bounds
        result = dict(vertical_speed=bounds.vertical_bound(), family_upper_bound=bounds.stronger_bound())
        check("fresh_original_calm_bound_matches_frozen", result == load("evidence/analytical/coupled/existence_bounds.json"))
        (Q/"science_fresh_calm_bound.json").write_text(json.dumps(result, indent=2)+"\n")
    receipt = dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   checker_sha256=sha(Path(__file__)), python=sys.version,
                   checks_passed=len(CHECKS), checks=CHECKS, values=VALUES,
                   fresh_calm_bound=args.fresh_bound,
                   evidence_level="tested; exported arithmetic recomputed from frozen inputs",
                   proof_scope="Fresh all-time proof reruns are separate receipts; floating sampling here is not certification.",
                   optimization_rerun=False, historical_measurements_reacquired=False,
                   aircraft_calibration=False, historical_clearance=False)
    (Q/"science_checks.json").write_text(json.dumps(receipt, indent=2)+"\n")
    if args.fresh_bound:
        (Q/"science_checks_fresh_bound.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(f"V5 science: {len(CHECKS)} checks passed; no optimization or source mutation.")


if __name__ == "__main__":
    main()
