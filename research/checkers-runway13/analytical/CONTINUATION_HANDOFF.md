# Finite roll and full landing: verified continuation

13 October 2026. **Overall requested closed-form optimal landing: INCOMPLETE.**

**Later continuation:** `coupled/RESULTS.md` and `coupled/START_HERE.md` now record
a complete candidate with an all-time interval feasibility certificate and a
finite-family existence proof. The missing-feasibility statements below describe
the earlier handoff, not the latest result. Global exact optimality remains missing.

## Achieved

- Finite-roll position matching and family monotonicity/uniqueness proofs; generally implicit scalar equations, not a full explicit optimum. Independent proof review exists.
- Explicit degree-7/6 approach/flare trajectory family preserving frozen endpoints, inverse forces and exact one-sided control rates, plus hybrid stopping equations.
- A necessary nominal upper bound on the primary margin: approximately 0.15769490255. This is not an attained optimum. The exact rational certificate is for nominal real decimal constants, not all binary floating execution errors.
- Parent reran 30 finite-roll ODE cases, five domain rejections, 41 trajectory comparisons, 50 derivative checks and the rational certificate. Four changed-bound-domain rejection tests also pass. No new numerical optimizer was used.

## Fresh defect and repair

A parent rerun exposed a triangular-endpoint inverse-test failure: the bank derivative of matched length vanishes there, and several floating bank values produced the same length. The recovered bank differed by 1.19e-7 radians despite zero forward length residual. The bisection helper now returns an endpoint when its evaluated value exactly equals the target, before iteration. No test tolerance, theorem, aircraft parameter or objective was relaxed. All 30 cases pass; maximum recovered-bank difference is 4.40e-14 radians. Earlier pass claims refer to earlier runs; this fresh failure and repair are retained here.

## Remaining requirements

| Requirement | Status |
|---|---|
| Finite-roll restricted position match and proof | Verified within stated domain |
| Explicit full path/control evaluation | Verified identity checks |
| Necessary objective upper certificate | Verified nominal real-decimal model |
| Optimal parameter formula | Not obtained |
| All-time candidate feasibility certificate | Not obtained |
| Matching global primary and secondary optimality proofs | Not obtained |
| Unrestricted full landing optimal policy | Not obtained |
| Historical terrain/obstacle/aircraft calibration | Missing |
| Routine-flight confrontation, go-around, uncertain-wind causal policy | Unfulfilled |

The existing candidate's sampled margin (~0.0388964) is not a certified continuous feasible lower bound, so its difference from the upper bound is not a certified optimality gap. Missing empirical inputs do not explain away the separate mathematical gap in the nominal scenario.

## Reproduce

From the project root, with requirements.lock installed in a Python environment:

    python analytical/verify_finite_roll_position.py
    python analytical/verify_full_landing_analysis.py

Full verifier uses the unchanged model source/config and saved scenario optimization_replay.json. See FULL_LANDING_ANALYSIS.md, FINITE_ROLL_POSITION.md and their proof-review files. No simulator/config changes, publication or outreach were performed.

Next mathematical requirement is a continuously feasible construction with a matching global upper certificate, or a sharper characterization of the optimum if this bound is slack. No such result is promised. This handoff records a completed bounded investigation, not completion of the requested research goal.
