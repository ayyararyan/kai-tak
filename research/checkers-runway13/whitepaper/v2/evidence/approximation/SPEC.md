---
title: Terrain-aware explicit approximate landing procedure and outcome uncertainty
type: feature
created: 2026-10-13
status: in-progress
baseline_commit: NO_VCS
context: []
---

<frozen-after-approval reason="Aryan explicitly requests this revised approximate target on 13 October; exact symbolic optimum and centimetre precision are not required">

## Intent

Construct an explicit approximate Kai Tak landing procedure conditional on dated geometry, entry state, aircraft configuration, wind and braking conditions. Return trajectory, phase timing, touchdown, ground distance, total runway consumed and runway remaining, with justified approximation/optimality bounds and outcome uncertainty. A fixed candidate's exact polynomial evaluation is not a solved condition-to-procedure map.

Retain the current aircraft, nominal primary minimum-margin objective, secondary effort objective, braking rules and verification distinctions unless explicitly changed. Use the terrain owner's stable handoff; do not duplicate that work or consume live-changing chronology as verified geometry. Exact symbolic global optimality is no longer necessary; scientifically justified near-optimality remains required, without promising it exists for every condition.

## Boundaries

Always preserve v1/coupled source and config. Keep separate: input/measurement uncertainty, aircraft-model discrepancy, approximation error, constraint satisfaction and optimality gap. Keep years separate. Null height/presence is unknown; an unknown scene cannot pass clearance. Use whole-aircraft swept volume and registration uncertainty before historical feasibility claims. Wind-dependent offline paths are not a gust-rejecting feedback controller; controller/tracking uncertainty remains required for claims about actually following the procedure.

Statistical output intervals for an individual landing are prediction intervals, not confidence intervals for a mean. Report coverage level, population/domain, calibration source and validation evidence; return unavailable without them. A deterministic parameter-box range has no probability coverage. A terrain accuracy statement at 90% confidence is not a hard height bound. Do not choose fictitious wind/braking distributions or an arbitrary accepted near-optimality tolerance. Preserve exact evaluated bounds and label whether any tolerance has been approved. No operational guidance, publication or live aviation actions are authorized.

## Inputs and outputs

| Case | Required behaviour |
|---|---|
| Existing nominal certified witness | Export explicit piecewise coefficients and scalar outcome formulas, marked synthetic-reference only; verify provenance hashes. |
| Other condition or scene | Reject use of the nominal witness as a certified solution; require that condition's solved/validated policy. |
| Declared scalar parameter intervals | Compute conditional algebraic stopping/time ranges; no claim that their endpoint combinations describe a feasible flight or statistical coverage. |
| Missing terrain/height/datum/tracking evidence | Report blockers; no historical clearance or real-world reliability claim. |
| Invalid or nonfinite intervals; zero braking | Reject, rather than divide or extrapolate. |
| Stable full inputs and calibrated uncertainty | Solve reference cases, fit explicit piecewise condition-to-coefficient rule, validate held-out outcomes and clearance, then quantify approximation and optimality bounds. |

</frozen-after-approval>

## Code map

- `../analytical/coupled/continuous_certificate_refined.json`: fixed nominal witness and real-decimal parameters.
- `../analytical/FULL_LANDING_ANALYSIS.md`, `../model/trajectory.py`: explicit Hermite family, endpoint semantics and ground model; read-only.
- `../analytical/coupled/RESULTS.md`: corrected certificate domain; 0.03972 upper bound withdrawn.
- `../reconstruction/chronology/REPORT.md`, `HANDOFF.json`: stable documentary/source handoff received and hash-verified; historical scene remains incomplete.
- `../geospatial/README.md`: acquired terrain/buildings and mixed-epoch limitations.

## Tasks and acceptance

- [x] FORM-01 `explicit_reference.py`: export polynomial coefficients, phase times and fixed stopping formula from verified source; reject source/config mismatch and invalid queries. This is reference evaluation, not new optimization.
- [x] OUT-01 `reference_formula.json`, `reference_outcomes.json`: readable evaluation with metre/second reporting; uncertainty fields explicitly unavailable; provenance and synthetic-scene identity preserved.
- [x] UNC-01 `explicit_reference.py`: propagate caller-supplied independent scalar intervals through stopping/time formulas by monotonic endpoints; retain inputs and nonprobabilistic scope. No new uncertainty numbers assumed.
- [x] VAL-01 `test_explicit_reference.py`: compare position/velocity/acceleration and phase joins against source; check stopping agreement, interval corner enclosure, invalid input and tamper rejection; retain verification output.
- [x] DATA-01 `scene_contract.md`: stable terrain interface specified and delivered handoff reconciled; all nine listed artifact sizes/hashes verified. Historical geometry, datum and height deficiencies remain explicit blockers under GEO-01, not waived.
- [ ] GEO-01 terrain-aware model branch: georeference historical runway, reconstruct/validate dated obstacle surface and swept-volume clearance; unresolved until stable geometry and approved physical clearance inputs exist.
- [ ] MAP-01 conditional explicit rule: fit piecewise coefficient functions using fully specified condition domain and terrain-aware reference solves; preserve endpoint identities and refuse extrapolation. No solved domain presently available.
- [ ] CERT-01 feasibility/near-optimality: validate complete intervals, tracking envelope and full condition domain; use only valid global bounds. Without an upper certificate label numerical comparator regret, not global near-optimality.
- [ ] STAT-01 outcome prediction intervals: use justified input distributions and model/tracking calibration, held-out validation and stated coverage; real-world intervals blocked without those inputs.
- [ ] OUT-02 final report/formulas: unify procedure, conditions, path, touchdown/runway/time intervals, proof scope and remaining gaps. No final-solution label before preceding requirements pass.

Given a reference query, evaluation must reproduce its saved trajectory and clearly deny terrain certification. Given interval inputs, every valid corner must be enclosed and coverage must remain null. Given missing scene or calibration evidence, final historical/predictive status must remain blocked. Given new terrain or condition cells, old certificates must not be reused without revalidation.

## Design notes

Use the existing endpoint-constrained polynomials as the interpretable path representation. Ultimately q-hat(theta,epoch) selects coefficients through a piecewise explicit function; fixed-coefficient path evaluation alone does not satisfy MAP-01. Known-condition guidance and causal feedback are distinct. Retain the full requested scope despite blocked inputs; independent preparation does not constitute completion.

## Verification

Run `../.venv/bin/python -m pytest test_explicit_reference.py -q` from this directory. Export reference outputs and inspect units, time origin, ground/air distances and null interval labels. Parent checks all requirement statuses and coordinates with terrain owner. No solver, scene, performance distribution or frozen model is altered by reference preparation.

## Spec change log

2026-10-13: latest instruction replaces exact symbolic optimality as a completion gate with explicit approximation and justified bounds; not a waiver of terrain, near-optimality or uncertainty. Global-checker invalidation from the mathematical owner is binding: current nominal bracket [0.0397,0.1559772), no tight near-optimality claim.
