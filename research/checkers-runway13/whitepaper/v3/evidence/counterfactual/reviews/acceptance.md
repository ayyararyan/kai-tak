# Independent acceptance audit

2026-10-13T14:05:49Z. Reviewed current source and delivered artifacts against `counterfactual/SPEC.md`, frozen model specification, approximation specification and full-scope ledger. No source edits. This review covers the conditional calculation, not completion of the historical research task.

## Verdict

**Conditional mathematical result passes the checks performed; workflow acceptance remains pending the known lifecycle repairs and final regenerated verification.** No additional physics, interval-proof or upper-bound defect found. Full historical landing/uncertainty scope remains incomplete, as the report correctly states.

## Blocking workflow findings

1. **Runtime acceptance gates must not be Python assertions.** In addition to the already reported `continuous.py` terminal assertion, `verify_delivery.py` uses `assert` for numerical export identity and final feasible/optimization-complete/certified status. `python -O` removes these gates. Replace with unconditional explicit rejection, and regression-check optimized execution. Parent notified directly.
2. The already identified stale-selection-after-search-failure, pre-validation delivery writes and missing refined-primary hard-feasibility gate remain acceptance conditions. These are not new independent findings; parent is repairing them. Regenerate source-bound certificates after source edits and rerun relevant negative-path tests and delivery verification.

## Fresh evidence and scope checks

- Targeted suite rerun: **22 passed**. Frozen source identities and original zero-wind reference-cloud hash checked; cloud hash is `37575749333a7b020502769879776114a8baa5c4b25763eb261d6ee015db3b3e`. Baseline config remains calm and historical mode remains rejected.
- Separate **20,001-point-per-phase** evaluation gives minimum margin **0.15279338252804847**, hard minimum **1.4496799718699549e-06** (structural touchdown contact excluded), and stop position **2233.2308450169853 m**. This dense check is numerical evidence, not the continuous proof.
- Fresh interval checker rerun: **certified**, lower margin **0.1507934696816132**, **376 accepted intervals / 750 processed**, maximum depth **13**. Reviewed closed-phase coverage, structural flare-height factorization, branch-safe angle enclosure, interval constant-wind endpoint construction and fixed-reference-point corridor bound. Display floats are not the rigorous interval endpoints; report appropriately relies on the real-decimal target.
- Meteorological FROM conversion is consistent with forward/right/up: the scenario wind is approximately **[-4.87659, +9.64007, 0] m/s**. Signed west variation gives **133 1/6 degrees true**. Endpoint ground velocities are recalculated from EAS, air-relative descent angle and ground track. Constant wind makes air and ground acceleration equal; inverse-force derivatives correctly use the air-relative basis.
- Approach/flare position, velocity and acceleration joins are continuous; control-rate sides differ and are retained. At the join, roll rates are **-0.03288208 / -0.00231771 rad/s**, thrust-slew rates **-10660.58 / -79603.32 N/s**. Contact is the specified inelastic vertical-velocity removal followed by fixed delay/deceleration, not an airborne force continuation.
- Upper-bound derivation is valid for the fixed decision family: `xD >= 200+500 eta`, `u >= 69`, and monotone `xD+2u+u²/(2a) <= 2636(1-eta)` imply the reported rational upper bound **66656817/307536544**. It does not prove near-optimality, global attainment of the selected candidate, or an unrestricted-control optimum.
- Inspected `landing.png`: readable complete ground track, altitude, groundspeed through stop and bank. Touchdown/stop and assumptions are visible. The shallow early rise is genuine and permitted by the unchanged constraints; report discloses it.
- Report/result separate physical prediction uncertainty from replay residuals, sampled feasibility from interval evidence, and the loose global bound from local search. They preserve unresolved terrain/datum/whole-aircraft/tracking/calibration/go-around requirements and do not turn the fixed braking calculation into a causal claim about CAL605.

## Handoff qualifications

Correctness: positive fresh evidence above, with negative-path repairs pending. Specification coverage: conditional artifacts present; final state/traceability closure still to be recorded by parent. End-to-end readiness: existing outputs reviewed, but final repaired source/certificate/export workflow must be rerun before closure. Historical readiness and physical CI/PI: **not established**.
