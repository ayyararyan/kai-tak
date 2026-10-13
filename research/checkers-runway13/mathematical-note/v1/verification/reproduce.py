#!/usr/bin/env python3
"""Read-only reproduction of the public scientific inputs; writes only --output.

No optimizer is invoked and no sealed producer's main program is run. Use a
separate process for each stage because the original interval code has mutable
module-level wind state. The accepted source commit is fixed below.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

SOURCE_COMMIT = "78a9ce1c627f917c94306af5529d5e9ebeb743e8"
STAGES = ("public-tests", "local", "retention", "bounds", "domains", "conditions", "legacy")


def write(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coverage(rows):
    counts = {}
    for phase in (0, 1):
        cells = sorted((a, b) for ph, a, b, *_ in rows if ph == phase)
        assert cells and cells[0][0] == 0 and cells[-1][1] == 1
        assert all(a[1] == b[0] for a, b in zip(cells, cells[1:]))
        counts[str(phase)] = len(cells)
    return counts


def condition_case(Case, p):
    return Case(p["name"], p["wind_mps"], p["urban"], p["roof_delta"],
                p["frame_dx"], p["frame_dy"], p["runway_level"], p["buffer"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="repository checkout root")
    parser.add_argument("--output", type=Path, required=True, help="new writable receipts directory")
    parser.add_argument("--stage", choices=("all",) + STAGES, default="all")
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    project = source / "research/checkers-runway13"
    conditional = project / "integrated/assumption_solution"
    refinement = conditional / "refinement"
    local = refinement / "local_certificate"
    if output == source or output in (conditional, refinement, local):
        parser.error("output must not be a source or sealed certificate directory")
    output.mkdir(parents=True, exist_ok=True)
    snapshot = source / "PUBLIC_SOURCE_MANIFEST.json"
    if snapshot.exists():
        manifest = read(snapshot)
        assert manifest["source_commit"] == SOURCE_COMMIT
        for name, record in manifest["files"].items():
            path = source / name
            assert path.stat().st_size == record["bytes"] and sha(path) == record["sha256"], name
        head = SOURCE_COMMIT + " (hash-bound source subset, no Git needed)"
    else:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
    if not snapshot.exists() and head != SOURCE_COMMIT:
        # A note commit may be a descendant; accept only unchanged original
        # scientific and publication-checker inputs, checked against the pin.
        subprocess.run(["git", "diff", "--exit-code", SOURCE_COMMIT, "--",
                        "research/checkers-runway13/integrated",
                        "research/checkers-runway13/counterfactual",
                        "research/checkers-runway13/analytical",
                        "research/checkers-runway13/model",
                        "publication/scientific-results-20261013"], cwd=source, check=True)
    # The public mapping checker accounts explicitly for normalized files and
    # unavailable restricted originals. The original-workspace checker is not
    # bypassed or falsely counted as passing in this public checkout.
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONPATH", None)
    if args.stage == "all":
        started = time.monotonic()
        write(output / "environment.json", {
            "source_commit": SOURCE_COMMIT,
            "checkout_head": head,
            "utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "packages": subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True).splitlines(),
            "no_optimization": True,
            "no_private_pythonpath": True,
        })
        results = []
        for stage in STAGES:
            command = [sys.executable, str(Path(__file__).resolve()), "--source", str(source),
                       "--output", str(output), "--stage", stage]
            t = time.monotonic()
            with (output / (stage + ".log")).open("w") as log:
                result = subprocess.run(command, cwd=project, env=env, stdout=log, stderr=subprocess.STDOUT)
            item = {"stage": stage, "returncode": result.returncode, "seconds": time.monotonic() - t,
                    "command": "python verification/reproduce.py --source SOURCE --output OUTPUT --stage " + stage,
                    "log": stage + ".log"}
            results.append(item)
            write(output / "run.json", {"source_commit": SOURCE_COMMIT, "results": results,
                  "complete": len(results) == len(STAGES), "passed": all(x["returncode"] == 0 for x in results),
                  "seconds": time.monotonic() - started})
            print(stage, result.returncode, round(item["seconds"], 3), flush=True)
        # Preserve sources, including normalized public versions, byte for byte.
        check = subprocess.run([sys.executable, str(Path(__file__).with_name("verify_public_inputs.py")), "--source", str(source)],
                               cwd=source, env=env, capture_output=True, text=True)
        (output / "preservation.log").write_text(check.stdout + check.stderr)
        diff = None if snapshot.exists() else subprocess.run(["git", "diff", "--exit-code", SOURCE_COMMIT, "--",
                               "research/checkers-runway13/integrated",
                               "research/checkers-runway13/analytical",
                               "research/checkers-runway13/counterfactual",
                               "research/checkers-runway13/model",
                               "publication/scientific-results-20261013"], cwd=source, capture_output=True, text=True)
        write(output / "preservation.json", {"append_aware_public_mapping_returncode": check.returncode,
              "source_subset_manifest_verified": snapshot.exists(),
              "pinned_scientific_diff_returncode": diff.returncode if diff is not None else None,
              "pinned_scientific_diff": diff.stdout if diff is not None else None,
              "preserved": check.returncode == 0 and (diff is None or diff.returncode == 0),
              "original_private_workspace_check": "not run: restricted originals and unnormalized bytes unavailable"})
        if any(x["returncode"] for x in results) or check.returncode or (diff is not None and diff.returncode):
            raise SystemExit(1)
        return

    os.chdir(project)
    sys.path[:0] = [str(local), str(refinement), str(conditional), str(project)]
    t = time.monotonic()
    if args.stage == "public-tests":
        from verify_public_inputs import check
        write(output / "public-input-integrity.json", check(source))
        # Import only the published selection (no tests altered). The original
        # driver's stale ledger gate fails on current main, recorded separately.
        import importlib.util
        spec = importlib.util.spec_from_file_location("published_runner", source / "publication/scientific-results-20261013/run_public_tests.py")
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *runner.FILES,
                   "-k", " and ".join("not " + name for name in runner.EXCLUDED)]
        result = subprocess.run(command, cwd=project, env=env, capture_output=True, text=True)
        print(result.stdout + result.stderr, flush=True)
        assert result.returncode == 0
        assert re.search(r"102 passed, 6 deselected", result.stdout), "unexpected test count"
        geometry = subprocess.run([sys.executable, "-c", runner.GEO], cwd=project, env=env,
                                  capture_output=True, text=True)
        print(geometry.stdout + geometry.stderr, flush=True)
        assert geometry.returncode == 0 and "Ran 15 tests" in geometry.stderr
        write(output / "public-tests.json", {
            "numerical_core_proof_passed": 102, "geometry_passed": 15, "total_passed": 117,
            "pytest_deselected": 6, "geometry_excluded": 1,
            "restricted_source_tests_not_run": 5, "original_workspace_tests_not_run": 2,
            "seconds": time.monotonic() - t,
            "counts_cross_checked_in_log": "public-tests.log",
        })
        return

    if args.stage == "local":
        import validate as v
        stored = read(local / "certificate.json")
        root, X, margins = v.krawczyk(stored["root"]["center"], stored["root"]["radius"])
        assert root["certified"] and root["strict_inclusion"] and root["all_jacobians_nonsingular"]
        simplex = v.simplex(margins)
        assert simplex["certified"]
        zones = v.events(X, ".01")
        assert len(zones) == 5 and all(z["certified"] for z in zones)
        path = v.full_path(X, zones)
        assert path["certified"]
        counts = coverage(path["cover"])
        assert len(path["cover"]) == 398 and path["processed"] == 786
        with localcontext() as ctx:
            ctx.prec = 80
            eta_lo = str(Decimal(root["center"][5]) - Decimal(root["radius"]))
            eta_hi = str(Decimal(root["center"][5]) + Decimal(root["radius"]))
        result = {"root": root, "simplex": simplex, "zones": zones, "path": path,
                  "coverage_counts": counts, "eta_outer_decimal_box": [eta_lo, eta_hi],
                  "source_certificate_sha256": sha(local / "certificate.json"),
                  "fresh": True, "seconds": time.monotonic() - t}
        write(output / "local-certificate.json", result)
        print("root, simplex, active extrema and full path certified", counts, flush=True)

    elif args.stage == "retention":
        import validate as v
        from certify import certify_case, bind
        from analysis_tools import replay
        root = read(local / "certificate.json")["root"]
        with localcontext() as ctx:
            ctx.prec = 80
            upper = str(Decimal(root["center"][5]) + Decimal(root["radius"]))
            target = str(Decimal(upper) - Decimal(".0001"))
        c = v.Case()
        old = read(conditional / "cases/mean/result.json")
        proof = bind(certify_case(c, old["selected"]["q"], target, maxdepth=24))
        assert proof["certified"] and proof["processed"] == 4020
        counts = coverage(proof["cover"])
        q = v.BASE["q"].copy()
        for k, i in enumerate([1, 2, 3, 10, 11]):
            q[i] = float(root["center"][k]) * v.SCALE[k]
        replayed = replay(c, q)
        assert replayed["passed"]
        write(output / "secondary-retention.json", {
            "secondary_retention": proof, "primary_upper_real_decimal": upper,
            "retention_budget_real_decimal": ".0001", "root_center_replay": replayed,
            "replay_is_numerical_center_not_exact_root": True, "coverage_counts": counts,
            "global_secondary_optimum": False, "fresh": True, "seconds": time.monotonic() - t})
        print("secondary retention", target, "processed", proof["processed"], "replay", replayed, flush=True)

    elif args.stage == "bounds":
        from conditional_model import Case, tr
        from strong_bound import exclusion
        from analysis_tools import terminal_interval_bound
        baseline = exclusion(Case(), "0.181970215", 4096)
        assert baseline["excluded"] and baseline["residual_lower_display_m"] > 0
        zero = exclusion(Case("tailwind5", wind=(5 * tr.KT, 0, 0)), "0", 2048)
        assert not zero["excluded"]
        terminal = terminal_interval_bound(Case())
        assert terminal["full"]["lower_F_upper_display"] < 0 < terminal["full"]["upper_F_lower_display"]
        write(output / "analytical-bounds.json", {"baseline_strong_family_exclusion": baseline,
              "tailwind5_zero_not_excluded": zero, "terminal_interval_bounds": terminal,
              "fresh": True, "seconds": time.monotonic() - t})
        print("strong family exclusion", baseline, flush=True)

    elif args.stage == "domains":
        import box_certifier as bc
        from conditional_model import Case
        branch = read(refinement / "active_branch.json")["baseline"]
        q, dq = branch["q"], [0.0] * 12
        for i, value in zip([1, 2, 3, 10, 11], branch["dq_dwx"]):
            dq[i] = value
        rows = []
        for delta, eta in [(".001", ".149"), (".002", ".147"), (".005", ".14")]:
            proof = bc.certify_box(Case(), q, dq, delta, eta, maxdepth=18, parameter_taylor=True)
            assert proof["certified"]
            proof["coverage_counts"] = coverage(proof["cover"])
            rows.append(proof)
            print(delta, eta, "certified", proof["processed"], flush=True)
        write(output / "wind-domains.json", {"certificates": rows,
              "deta_dwx_numerical": branch["deta_dwx"], "sensitivity_interval_enclosed": False,
              "source_branch_sha256": sha(refinement / "active_branch.json"),
              "known_constant_wind_family_not_feedback_policy": True,
              "fresh": True, "seconds": time.monotonic() - t})

    elif args.stage == "conditions":
        from conditional_model import Case, tr
        from certify import certify_case, bind
        from analysis_tools import replay
        from retention_proof import primary_upper
        rows = []
        for path in sorted((conditional / "cases").glob("*/result.json")):
            old = read(path)
            c = condition_case(Case, old["condition"])
            upper, where = primary_upper(c, old["primary"]["q"])
            with localcontext() as ctx:
                ctx.prec = 80
                target = str(Decimal(repr(upper)) - Decimal(".0001"))
            proof = bind(certify_case(c, old["selected"]["q"], target, maxdepth=22))
            assert proof["certified"]
            replayed = replay(c, old["selected"]["q"])
            assert replayed["passed"]
            result = {"name": c.name, "continuous": proof, "replay": replayed,
                      "primary_upper": where, "retention_budget_real_decimal": ".0001",
                      "source_result_sha256": sha(path), "coverage_counts": coverage(proof["cover"]),
                      "primary_comparison_scope": "stored numerical primary path, not a proved optimum"}
            write(output / ("condition-" + c.name + ".json"), result)
            rows.append({"name": c.name, "eta_lower_real_decimal": target,
                         "processed": proof["processed"], "accepted_cells": len(proof["cover"]),
                         "certified": True, "replay_passed": True,
                         "condition": old["condition"], "stop_display": proof["stop_display"]})
            print(c.name, "certified", target, proof["processed"], flush=True)
        for name, c in [("tailwind3", Case("tailwind3", wind=(3 * tr.KT, 0, 0))),
                        ("urban58", Case("urban58", urban=58))]:
            path = refinement / (name + "_verified.json")
            old = read(path)
            target = old["continuous"]["eta_lower_real_decimal"]
            proof = bind(certify_case(c, old["selected"]["q"], target, maxdepth=24))
            assert proof["certified"]
            replayed = replay(c, old["selected"]["q"])
            assert replayed["passed"]
            result = {"name": name, "continuous": proof, "replay": replayed,
                      "source_result_sha256": sha(path), "coverage_counts": coverage(proof["cover"])}
            write(output / ("condition-" + name + ".json"), result)
            rows.append({"name": name, "eta_lower_real_decimal": target,
                         "processed": proof["processed"], "accepted_cells": len(proof["cover"]),
                         "certified": True, "replay_passed": True,
                         "condition": c.parameters(), "stop_display": proof["stop_display"]})
            print(name, "certified", target, proof["processed"], flush=True)
        assert len(rows) == 10
        write(output / "conditions.json", {"cases": rows, "certified_count": len(rows),
              "unresolved_not_infeasible": ["tailwind5", "urban60", "urban65"],
              "fresh": True, "seconds": time.monotonic() - t})

    elif args.stage == "legacy":
        coupled = project / "analytical/coupled"
        sys.path[:0] = [str(coupled), str(project / "counterfactual")]
        import certify_candidate as calm
        from counterfactual import continuous as wind
        from existence_and_bounds import vertical_bound, stronger_bound
        rows = []
        for name, module, certificate in [
                ("synthetic-calm", calm, coupled / "continuous_certificate_refined.json"),
                ("synthetic-wind", wind, project / "counterfactual/continuous_check.json")]:
            stored = read(certificate)
            fresh = module.certify(stored["q_real_decimal"], stored["eta_lower_real_decimal"])
            assert fresh["certified"] and fresh["cover"] == stored["cover"]
            result = {"scenario": name, "fresh_proof": fresh, "exact_cover_matches_saved": True,
                      "coverage_counts": coverage(fresh["cover"]), "source_certificate_sha256": sha(certificate),
                      "model": "original synthetic V5 model; not the A1 CG/geometry model"}
            write(output / (name + ".json"), result)
            rows.append({"scenario": name, "certified": True,
                         "eta_lower_real_decimal": fresh["eta_lower_real_decimal"],
                         "accepted_intervals": len(fresh["cover"]), "processed": fresh["processed"]})
            print(name, "certified", fresh["eta_lower_real_decimal"], len(fresh["cover"]), flush=True)
        bounds = {"vertical_speed": vertical_bound(), "family_upper_bound": stronger_bound()}
        write(output / "legacy-summary.json", {"witnesses": rows, "bounds": bounds,
              "model": "original synthetic V5 model; numbers not substituted into A1",
              "fresh": True, "seconds": time.monotonic() - t})


if __name__ == "__main__":
    main()
