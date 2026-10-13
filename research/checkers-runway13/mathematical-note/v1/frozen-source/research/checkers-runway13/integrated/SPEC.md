# Historical integration specification v1 — 2026-10-13

Authorized scope: HANDOFF_TASK.md and the latest objective correction in PROJECT_STATE.md. This specification formalizes the accepted work, not a new approval request. Status: in progress; scientific completion requires every requirement below. Canonical project ledger remains ../PROJECT_STATE.md.

## Object and invariants
Historical epoch 1993-11-04. Aircraft Boeing 747-409B/PW4056, flaps30, gear down, baseline estimated mass238461.67357166kg. Preserve scenario v1, its exact numerical artifacts, all invalidated evidence and the constant-wind counterfactual. New files under integrated/. No public-checkout mutation, publication, spending or outreach. No delegation.

Primary objective is maximum minimum existing normalized operating-constraint margin; secondary is integrated squared normalized bank/roll/thrust-slew effort at primary loss <=1e-4. Historical collision/procedure restrictions enter as HARD constraints unless a justified normalization is explicitly accepted; no arbitrary new scale may redefine the objective. Preserve 2s brake delay,1.4709975m/s² deceleration,150m reserve and existing envelope. Source-backed calibration is evidence to assess applicability, not authority to improve brakes or relax limits.

## Required sequence
1. Establish evidence categories, frame and supported historical constraints.
2. Integrate dated hazards with full rigid-body occupancy, attitude/reference and tracking allowance; test physical-constraint joins.
3. Only after that prerequisite is established, derive the complete condition-dependent hybrid optimum and sufficiency/global results for the precise claimed class. Missing prerequisite blocks downstream historical solution, not independent evidence acquisition or prerequisite implementation.
4. Verify and hand off without conflating correctness, completeness and acceptance.

## Requirement IDs and acceptance
| ID | Requirement | Acceptance |
|---|---|---|
| INT-01 | Scope, source integrity and single-ledger continuity | Frozen inputs hashed; baseline untouched; all requirements traced |
| GEO-01 | Runway/threshold/true-grid-magnetic registration | Primary image observations, transforms, uncertainty, independent checkpoints |
| GEO-02 | Common vertical reference | Aviation AMSL/HKPD relation supported or unresolved variable; no guessed offset |
| GEO-03 | Historical approach and alternative entries | Source-backed IGS/MM, visual/missed constraints; entry conditions separate from synthetic tube |
| GEO-04 | Dated terrain/coast | Actual source-derived geometry, date and coverage; independent uncertainty evidence |
| GEO-05 | Dated roofs/equipment/changed identities | Full solids or explicitly unknown heights/presence; no modern-height transfer |
| GEO-06 | Machine-readable scene and coverage | Provenance for each feature, datum and date; null propagation; unknown masks |
| AIR-01 | Whole 747 occupancy and reference | Wing/tail/gear geometry, attitude/CG/eye/gear transformation; calibrated or conditional status |
| AIR-02 | Clearance integration | Swept-volume/terrain checks and limiting feature/time; unknown refuses certificate |
| AIR-03 | Physical dynamics calibration | Aircraft/control/braking source review with frozen-law comparison and unresolved calibration |
| OPT-01 | Full hybrid parameterized problem | Entry/wind/mass/config/control/landing domains; source-supported condition table |
| OPT-02 | Closed-form regimes | Explicit trajectories and controls, switching/regime domains, no optimized-coefficient substitution |
| OPT-03 | Primary and secondary sufficiency | Global proof in exact claimed admissible class; no necessary-condition substitution |
| UNC-01 | Uncertainty and feedback/go-around | Deterministic vs statistical intervals; known wind vs one causal policy; viability retained |
| VAL-01 | Reproducible validation | Independent transforms, collisions, joins/rates/stop, domain boundaries, continuous claims tested |
| OUT-01 | Usable report, figures, evaluator and handoff | Results and gaps, evidence levels and coverage; sole ledger updated |

## Input/evidence contract
Every observation: unique ID, source file/hash/page or pixel, edition/capture date and precision, query-date presence status, geometry CRS, vertical datum, units, meaning (surface/roof/equipment), category, measurement uncertainty, hard-bound status and coverage. Categories: observed source statement; deterministic derivation; estimate; scenario; proxy; unidentified. A map height is a source observation, not a certified true elevation. Index polygons are acquisition extents, not reconstructed surfaces. Source residuals and digitizing tolerances are not physical worst-case bounds. Repeated map content does not establish independent survey or date persistence.

## Condition domains
- Source baseline: documented1993 aircraft/configuration; measured source mass estimate, report wind and navigation instructions with uncertainty retained.
- Mathematical evaluator: finite real supplied pose/geometry and explicitly supplied attitude/offset intervals; no empirical support implied.
- Historical certified landing condition domain: EMPTY until all registration, relevant coverage and aircraft/tracking gates pass. This is an absence of certified inputs, not proof no landing is feasible.
- Known constant winds may be parameterized. Nonconstant winds need material wind derivative and causal information model; no reuse of constant-wind certificates.
- Alternative entry arms: published IGS visual transition; source-supported chart alternative acquisition; explicitly conditional visual entry set. Not arbitrary relocation masquerading as historical entry.

## Artifact contract
SPEC.md and TRACEABILITY.md: producer this owner; every requirement once; update on evidence change.
source_manifest.json: baseline and primary source path/hash/semantics; fail on mutation before reuse.
geometry/*.geojson, registration.json, source_observations.json: actual geometry/transform, datum/date/reference, uncertainty and provenance; unavailable values null; no inferred filled coverage.
clearance.py, test_integrated.py, verification.json: explicit assumptions, analytic whole-body extent and continuous segment checks where supported; no historical pass from scenario fixtures.
conditions.json, derivations/: condition domains and proved regimes only after sequence gate; unavailable historical optimum null with exact dependency.
REPORT.md and exported figures: limiting physical evidence and unresolved zones; figures cannot imply clearance by omission.

No data download, successful test or partial analytical lemma completes the requested study. Source-backed hazard influence with defensible bounds is a required integration acceptance gate. An unresolved datum, object top, reference/attitude or relevant coverage blocks a physical clearance claim.
