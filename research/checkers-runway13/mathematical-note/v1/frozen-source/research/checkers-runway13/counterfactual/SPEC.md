---
title: Calculate the counterfactual complete landing
type: feature
created: 2026-10-13
status: done
baseline_commit: NO_VCS
context: []
---

<frozen-after-approval reason="Aryan explicitly requests the landing that should have happened; existing model and explicit approximate-procedure scope remain authorized">

## Intent

The relevant object is a constructed approach, flare, touchdown and stop under specified conditions, not a fit to the accident trace. Calculate a wind-conditioned candidate using the approved point-mass aircraft and minimum-slack/secondary-effort objective. Preserve the full historical optimal-landing and prediction-interval requirements; conditional progress must not be relabelled their completion.

Use the report-stated 070 degrees true / 21 kt surface mean as a declared steady, spatially uniform wind scenario. Convert runway 135 magnetic using the original chart's 1 degree 50 minutes west variation (1990), giving 133 degrees 10 minutes true. This is a chart-based scenario bearing, not an independently surveyed 1993 true axis or recovered aircraft wind. Store all source conventions and assumptions. Keep the original zero-wind result as comparator only.

## Boundaries & Constraints

Always preserve source model/config, twelve-dimensional decision bounds, aircraft mass/envelope, synthetic entry position/track/EAS, threshold conditions, original zero-wind reference point-cloud corridor, 2 s delay, 0.15g braking and 150 m reserve. Recompute endpoint ground velocity and inverse controls for the declared steady wind; do not reuse the nominal zero-wind certificate. Preserve both one-sided control derivatives. Primary objective stays maximum minimum normalized margin; secondary effort retains primary margin within 1e-4. Use multiple deterministic starting points and denser validation; these do not prove a global optimum.

No historical clearance claim with unknown historical geometry, whole-aircraft envelope, datum or tracking errors. No fabricated wind process, physical confidence interval, calibrated braking capability, global near-optimality or go-around result. Historical mode must remain blocked. The accident report says actual touchdown was controllable and not causal; conditional .15g results cannot contradict that by assertion. A time-indexed reference is not a feedback controller or pilot procedure.

Missing empirical inputs are recorded as unresolved, not replaced by accident-fitted curves. Candidate numerical feasibility, continuous certification, optimality gap and physical prediction uncertainty are separate outputs. If a search fails, report unresolved rather than physical impossibility. New research case files remain separate from frozen model and terrain work. No publication or external communication.

## I/O & Edge-Case Matrix

| Scenario | Required behavior |
|---|---|
| Fixed mean-wind scenario | Jointly optimize complete flight and stopping; export path, controls, coefficients, timeline and distances. |
| Feasible candidate | Check exact analytic rates, independent forward force replay and dense grid; explicitly report whether all-time interval verification succeeds. |
| Numeric optimization failure | Retain failed search details; never label infeasible or select a constraint-violating path. |
| Wind conversion | Meteorological FROM direction, signed west variation; reject nonfinite inputs; check head/tail/crosswind examples. |
| Missing historic input | Null historical certification and physical intervals; disclose synthetic entry/corridor and uniform mean-wind assumption next to results. |
| Coefficient export | Re-evaluation must match states/derivatives and phase joins. No extrapolation outside each phase. |

</frozen-after-approval>

## Code Map

- `../model/trajectory.py`: frozen aircraft, endpoints, rollout and independent Newton replay.
- `../analytical/verify_full_landing_analysis.py`: explicit polynomial family and scalar exact derivatives.
- `../analytical/coupled/solve_coupled.py`: numerical nominal exact-rate search reference; hard-coded zero-wind globals must not be reused silently.
- `../analytical/coupled/certify_candidate.py`: interval machinery, zero-wind domain; extension requires its own tests and evidence.
- `../evidence/EVIDENCE_REPORT.md`: primary runway bearing/variation and causality distinctions.
- `../evidence/cal605_reconstruction/noaa/README.md`: true-north wind and observational limitations.
- `../reconstruction/block_matching/HANDOFF.json`: incomplete relative-height scene; cannot supply clearance.

## Tasks & Acceptance

- [x] INPUT-01 `inputs.json`, `SCOPE_AUDIT.md`: record sources, scenario choices, frozen hashes and all outstanding full-scope requirements.
- [x] SOLVE-01 `calculate.py`: source-bound constant-wind exact-rate evaluator and deterministic multistart lexicographic solve, fixed original corridor.
- [x] OUT-01 `result.json`, `path_controls.csv`, `formula.json`, `landing.png`: explicit candidate and complete timeline; plot path and runway stop in plain English.
- [x] VAL-01 `test_counterfactual.py`, `verification.json`: coordinate conversion, scalar/vector controls, finite-difference rates, endpoints, exports, stopping, independent replay, failure semantics and source identity.
- [x] CERT-01 `continuous_check.json`: attempt independent all-time interval certification without modifying original checker; report the actual result and numerical/physical distinction. Missing global gap remains explicit.
- [x] OUT-02 `REPORT.md`: recommended candidate conditional on assumptions, main flight phases/timing, constraints, bounds, and exactly what is not established. Append canonical project state after verification.

Given the saved inputs, when the producer runs, then every selected candidate must pass dense hard/operating constraints and independent replay before a feasible-scenario label. Given source changes, validation must fail before reusing a certificate. Given unavailable terrain/calibration, historical feasibility and physical prediction intervals remain unavailable even if numeric tests pass. Given a positive result, present the constructed landing first, not accident commentary.

## Verification

Use existing project virtual environment. Run new targeted tests, independent forward replay and coefficient reconstruction; inspect the resulting figure and retained optimizer statuses. Review implementation and model-meaning compliance independently. Preserve solver failures and any invalidated artifacts. Record successful outputs and broader incompleteness separately.

## Spec Change Log

2026-10-13: latest correction prioritizes constructing a counterfactual. Existing historical reconstruction is evidence only. No second approval requested for executing the already-approved model. Conditional mean-wind computation is an in-scope case, not a reduction of historical/uncertainty requirements.


## Conditional-case acceptance — 13 October 2026, 14:08 UTC

All six requirements above are implemented and verified for this declared scenario. Parent independently reran 37 tests, the two-pass delivery/replay verifier, a 20,001-point-per-phase evaluation and the interval proof (376 covering boxes). All 22 delivery-manifest hashes matched. Three independent review roles completed; lifecycle findings repaired and regression-tested. Source physics and numerical candidate unchanged. See `reviews/parent_final_verification.json` and `reviews/DISPOSITION.md`.

This status closes only the conditional computation. `../approximation/SPEC.md` remains incomplete for historical scene integration, a condition-to-procedure map, justified near-optimality, physical prediction intervals and full final delivery. No scope requirement is waived; no commit, push or peer sync performed here.

## Suggested Review Order

- Start with the constructed landing and its assumptions.
  [REPORT.md:1](REPORT.md#L1)
- Preserve the distinction between conditional computation and outstanding historical requirements.
  [SCOPE_AUDIT.md:1](SCOPE_AUDIT.md#L1)
- Inspect exact controls, margin objective and fail-closed search selection.
  [calculate.py:1](calculate.py#L1)
- Inspect independent continuous-time proof and terminal obligations.
  [continuous.py:132](continuous.py#L132)
- Inspect certificate binding, replay and atomic artifact publication.
  [deliver.py:20](deliver.py#L20)
- Check failure-path regressions and independent verification evidence.
  [test_counterfactual.py:1](test_counterfactual.py#L1)
