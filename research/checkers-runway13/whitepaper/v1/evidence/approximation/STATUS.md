# Explicit landing approximation: verified status

13 October 2026. Overall requested solution: **INCOMPLETE**.

The target is a dated-terrain-aware, condition-dependent explicit landing procedure with quantified approximation/optimality error and justified outcome prediction intervals. Exact symbolic optimality and centimetre accuracy are not requirements. Existing model meaning is preserved.

## Requirement coverage

| Requirement | Status | Evidence or dependency |
|---|---|---|
| FORM-01 fixed-reference formula | Implemented, tested | `explicit_reference.py`, `reference_formula.json` |
| OUT-01 reference outcome export | Implemented, dry-run verified | `reference_outcomes.json`; individual uncertainty fields remain null |
| UNC-01 conditional scalar bounds | Implemented, tested | Exact rational endpoint algebra; all 128 synthetic test-box corners enclosed; no probability claim |
| VAL-01 reference verification | Implemented, tested | 30 tests passed in child and parent reruns; source/artifact hashes verified |
| DATA-01 scene interface and reconciliation | Implemented, verified | Stable REPORT/HANDOFF inspected; nine artifact sizes/hashes match; `scene_contract.md` records accepted evidence and unresolved geometry |
| GEO-01 historical terrain-aware flight | Blocked | Dated geometry/unknown masks, runway registration, whole-aircraft clearance and tracking bounds absent |
| MAP-01 explicit condition-to-procedure rule | Blocked | Needs GEO-01 and a specified condition domain with validated reference solves |
| CERT-01 full feasibility and near-optimality bounds | Blocked | No terrain-aware family or sufficiently tight valid optimum bound; old tight bound withdrawn |
| STAT-01 calibrated prediction intervals | Blocked | No relevant calibrated input/model/tracking distributions or held-out coverage evidence |
| OUT-02 complete requested delivery | Blocked | Remaining requirements above are not waived |

Coverage: 5 implemented, 5 blocked, of 10 requirements. Correctness of implemented components is tested; full specification completeness and realistic end-to-end readiness are not established. Scene-interface completion does not mean historical geometry is complete.

## What the current numbers mean

The fixed **synthetic, empty-obstacle reference** gives touchdown 313.49 m beyond the usable threshold, ground roll 2,217.83 m (including braking delay), threshold-to-stop distance 2,531.32 m and remaining runway 254.68 m. From its declared entry state, touchdown occurs at 41.34 s and complete stop at 96.29 s. These are deterministic scenario outputs, not empirical predictions or an obstacle-checked Hong Kong solution.

The exported formula reproduces source position, velocity, acceleration and jerk; it rejects other scenes/conditions, extrapolation, changed source/configuration and invalid interval inputs. Floating coefficient consistency does not establish physical accuracy or extend the source interval certificate to rounded coefficients. Ground contact uses the existing idealized velocity transition.

The earlier near-optimality statement relying on upper bound 0.03972 was incorrect. The bound was withdrawn after global-checker defects. The valid nominal finite-family bracket remains [0.0397,0.1559772); all-time feasibility of the fixed nominal witness survives. This is not a near-optimality certificate for Hong Kong.

## Dependency ownership and resumption

Terrain/chronology owner: OpenClaw dashboard session `[local-session-reference]`. Its stable `reconstruction/chronology/REPORT.md`, `HANDOFF.json` and validation have been received. The approximation lane verified all nine handoff artifacts. Historical footprints/heights, aviation datum reconciliation and clearance-ready geometry remain unresolved; the whole-AOI uncertainty mask explicitly preserves that fact.

Handoff reconciliation is complete in `scene_contract.md`. Next dependencies are registered historical runway/obstacle geometry and defensible heights, aircraft/tracking bounds, a solved condition domain and outcome calibration. Current source/configuration and certificates are unchanged. Neither lane reports an active solver, acquisition run or automatic monitor. Existing authorization to complete the agreed work is preserved.

Latest verification, 13 October 2026: 30 reference tests passed on a fresh rerun; nine handoff artifacts match both size and SHA256. `CLOSED_FORM_AND_BOUNDS.md` presents the actual fixed-reference coefficients, scalar outcome equations and conditional error envelopes. It explicitly leaves historical landing predictions, calibrated CIs and near-optimality unresolved. This is not OUT-02 completion.

Verification: `verification.json` records the child checks; `parent_verification.json` records the independent parent test rerun and nine source/artifact hash checks. Design: `APPROXIMATION_DESIGN.md`; full scope: `SPEC.md`.
