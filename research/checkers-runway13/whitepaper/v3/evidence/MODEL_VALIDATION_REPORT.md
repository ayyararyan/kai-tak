# Model validation report — v1

## Result

The executable **scenario** model is implemented, tested and dry-run verified. It includes approach, flare, touchdown and stopping, nominal constraint-margin/effort optimization, independent force integration and full replay-state inequality checks. It is not a calibrated Boeing simulator, a historical reconstruction, an operational safety result or a global optimum.

Authoritative run: `outputs/scenario/optimization_replay.json`, UTC 2026-10-13T10:35:26.454179+00:00 (Asia/Kolkata +05:30). Earlier outputs under `scenario-pre-review`, `scenario-refined` and `scenario-longer` are retained research/debug runs, not the final handoff. `outputs/search_failure` is an intentional negative test.

## Numerical result

- Aircraft: documented 747-409B configuration; estimated mass 238461.67357166 kg, flaps 30, gear down.
- Flight duration: 41.571163 s.
- Touchdown: 330.423404 m from displaced threshold, prescribed sink 0.7 m/s.
- Stop: 2533.061479 m; runway remaining 252.938521 m (required reserve 150 m).
- Maximum bank: 13.327469 degrees; maximum bank-angle rate 3.571532 degrees/s.
- EAS range: 136.560225–153.009572 kt.
- Dense minimum normalized slack: 0.0388964287; not a probability or a natural unit of safety.
- Both local objective stages terminated successfully, 34 and 191 iterations. Dense primary-to-secondary slack loss is below 1e-4. A stricter 5e-5 solver-mesh loss budget reserves room for validation-grid discrepancy.
- Independent replay maximum position error: 8.48e-08 m; velocity error 5.44e-08 m/s; stop error 5.35e-07 m. These are numerical discrepancies, not real-aircraft accuracy.

The baseline is an **infeasible synthetic seed** (negative thrust, thrust-rate and stop-reserve violations), not a historical pilot trajectory. The candidate's positive margin therefore constructs a sampled-feasible scenario path; it does not prove improvement over an admissible historical flight.

## Verification and coverage

- Correctness: **52/52 pytest tests passed** after all code repairs. Includes force reconstruction, bank sign, wind/heading distinction, continuous phase boundaries, braking, invalid inputs, historical refusal, nonfinite rejection, narrow-obstacle detection and independent-replay corruption tests.
- Existing analytical benchmark: **6/6 synthetic finite-roll cases passed**, independently rerun by parent. Conditional heading theorem remains separate from the variable-speed position-constrained optimizer.
- Artifact acceptance: **29/29 checks passed** from `reviews/verify_artifacts.py`, including code/output checksums, both solver stages, dense retention, replay-state constraints, phase ordering, independent stop formula and historical refusal.
- Grid: 121 points/phase for optimization; 1201 points/phase for validation. Arbitrary custom solver meshes now receive at least 10x interval refinement. Still not a continuous-time feasibility certificate.
- Historical CLI negative test: intentional exit 2 and blocked JSON. A success boolean cannot override missing calibrated inputs.
- Search-failure negative test: `--maxiter 1` produces `unresolved`, with `optimization_complete=false`; not a claim of infeasibility.
- Standalone plot inspected after repaired final run; it shows a short low-altitude climb and subsequent descent. Monotone descent was not a specified constraint; this is an important limitation of the chosen scenario design.
- No flight operations, public repository, commit, push, deployment, external custodian email or peer-machine sync occurred.

Executable specification: **7/7 requirements implemented**. Complete broader-study traceability retains 12 requirements: 2 implemented, 3 partial, 3 not implemented, 4 blocked. Across all 19 rows: 9 implemented, 3 partial, 3 not implemented, 4 blocked. **Full three-aim study remains incomplete.**

## Stress diagnostics: failures are retained

These hold the same nominal ground path and timing and recompute controls for known steady wind/changed parameters; they are not a common causal feedback policy.

- steady_crosswind_plus5: no sampled violation.
- steady_crosswind_minus5: violates eas_lower.
- mass_plus5percent: violates thrust_slew.
- braking_minus10percent: violates stop_reserve.

The negative crosswind case breaches the selected EAS floor; +5% mass breaches thrust slew; 10% less braking breaches the runway reserve. Therefore the nominal model solution is not robust to these stated perturbations. There is no gust-tolerance certificate.

## Review repairs and remaining scientific limits

Three independent reviews plus parent inspection identified and repaired: spline averaging of phase-side rates, fixed ground-obstacle sampling holes, nonfinite feasibility flags, malformed/physical-domain inputs, incorrect custom-wind stresses, insufficient custom-mesh refinement, mass-provenance qualification and missing full-state replay constraints. Exact-boundary replay cases are unresolved rather than silently passed or interpreted as physical impossibility. Decision record: `reviews/REVIEW_DECISIONS.md`.

Historical terrain/corridor, calibrated aerodynamic/actuator/braking envelopes, routine-flight observations, go-around viability and robust information-constrained feedback control remain absent. Constant-wind, coordinated point-mass, lumped ground-contact and braking assumptions remain explicit. Airborne geometry is sampled, not interval-certified. The nominal minimum EAS can lie below the case's published Vref; the chosen 135-kt floor is an uncalibrated research assumption, not approval to operate there.

No requirement or physical limit was loosened to make the code pass. Engineering repairs changed the final local optimizer result; the earlier approximately 395 m touchdown / 221 m reserve update describes a superseded run, not the final one above.
