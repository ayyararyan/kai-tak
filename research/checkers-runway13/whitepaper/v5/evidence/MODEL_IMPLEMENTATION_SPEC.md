---
title: Constrained Runway 13 trajectory model
type: feature
created: 2026-10-13
status: done
baseline_commit: NO_VCS
context: []
---

# Implementation specification v1

## Authority and intent

Aryan's 13 October instruction delegates selection of the aircraft, landing target and objective, then requests implementation. This is permission to select a research baseline, not evidence that aircraft performance or historical terrain are known. The three-aim study remains unchanged. The previous research draft remains archival; this file now specifies the executable model. No additional approval checkpoint is needed for the delegated selections.

<frozen-after-approval reason="user authorized baseline selection and implementation, 2026-10-13">

## Fixed decisions

**Aircraft:** Boeing 747-409B / 747-400, four PW4056 engines, flaps 30, gear down, constant landing mass 525718 lb converted exactly to kg. CAD Report 1/95 gives approximate 239 tonnes, Vref 141 kt and case target 153 kt. Use 153 kt EAS as the scenario initial/threshold speed, explicitly approximating low-altitude CAS by EAS, converting to TAS at model density. The choice anchors configuration to evidence; it does not calibrate an aerodynamic model or reproduce CAL605 weather.

**Frame/target:** runway-relative x forward from displaced threshold, y right, z above runway. Primary 1993 magnetic courses 88/135 degrees give -47-degree inbound nominal track. No true-north/georeferenced claim. Cross threshold at x=y=0, z=15.24 m, track=0, gamma=-3.1 degrees, zero bank; continue through a flare to y=z=0, vertical speed -0.7 m/s, positive forward speed, then stop within 2786 m LDA with 150 m reserve. Touchdown x must be 200–700 m; lateral tolerance 5 m, track 2 degrees, bank 3 degrees, sink 0–1.5 m/s. These tolerances and 50-foot threshold height are research choices, not a historical approved procedure. The point-mass ground-contact height is a lumped gear reference, not aircraft-CG clearance.

**Objective:** maximize minimum dimensionless nominal constraint slack eta across approach, flare and stopping, subject to hard constraints. Secondary: minimize integrated squared normalized bank/roll/thrust-rate demands while retaining primary eta to 1e-4. This is a deterministic safety-margin proxy, NOT the robust gust-tolerance objective or accident probability. Wind stress replays are separate diagnostics. Ultimate uncertain-wind causal-policy robustness and historical comparison remain required research work, not silently satisfied by this objective.

**Model:** coordinated 3D point mass with finite bank rate, lift/load/stall, thrust/drag and thrust-slew limits. Use smooth position trajectories with endpoint position/velocity/acceleration constraints; inverse dynamics derives V, gamma, air heading, bank, CL and thrust from ground velocity/acceleration and declared constant wind. Independent forward Newton integration replays derived controls. Bank-rate and thrust-slew are checked, not assumed. Flare is a continuous second flight segment. Ground rollout uses a fixed delay then declared deceleration; no optimization may improve braking secretly.

**Geometry:** fixed synthetic start (-2500,1000,140) m, inbound track -47 degrees, descending at 3.1 degrees; fixed nominal corridor tube with 400 m half-width around unoptimized reference. All are scenario inputs, not extracted middle-marker coordinates. Terrain/obstacle envelopes accept supplied obstacle data. Historical mode must fail closed while historical terrain, navigation corridor and calibrated aircraft envelope are absent. No empty obstacle list counts as historical clearance.

**Operating envelope:** bank <=25 degrees; bank rate <=5 degrees/s; CL 0–2.8, load 0.5–1.4g, EAS 135–175 kt, descent no steeper than 6 degrees, sink <=8 m/s before flare and <=1.5 at touchdown; thrust 0–700 kN, slew <=100 kN/s. rho=1.225 exp(-h/8500), wing area 541.2 m2, CD0=.08, induced factor .045; rollout delay 2 s and deceleration .15g. These are explicit uncalibrated scenario parameters, not Boeing-certified limits. Constant winds only; time-varying gusts must be rejected until wind acceleration is implemented.

## Invariants and unavailable evidence

Observed CAD metadata, exact conversions, simulated trajectories and assumed parameters must remain distinct in machine-readable output. Same initial state, corridor, aircraft and braking for baseline/candidate. Search failure means unresolved, never proven infeasible. Optimizer success alone cannot pass replay. No global-optimality, operational-safety or historical-suboptimality claim. No public publishing or outreach. Full study must retain missing routine-flight data, historical obstacle calibration, go-around viability and robust feedback-policy synthesis as open requirements.

## I/O cases

- Valid scenario -> baseline/candidate CSV, parameter provenance, optimization/replay JSON and plots.
- Missing historical inputs -> blocked status with reasons; never a feasible-historical label.
- Invalid V, mass, time, envelope, nonfinite data or nonconstant wind -> explicit validation error.
- Infeasible samples/replay or local search failure -> unresolved with violations, retained diagnostics.
- Stress wind -> same reference evaluated conditional on steady wind, not a common-policy robustness certificate.

</frozen-after-approval>

## Tasks & acceptance

- [x] DATA-01: `model/config.json` — parameter/source/category sheet with all choices above.
- [x] STATE-01: `model/trajectory.py` — flight inverse dynamics, finite-rate checks, flare and rollout.
- [x] OPT-01: `model/solve.py` — lexicographic slack/effort local optimization, fixed baseline, uncertainty-safe statuses.
- [x] VAL-01: `model/test_model.py` — force balance, heading/wind, ground stop, invalid inputs, historical gate and negative constraints.
- [x] VAL-02: independent forward replay, denser-grid checks and sensitivity diagnostics; retain mismatch/violations.
- [x] OUT-01: run outputs, standalone figure, reproducible README and dependency lock.
- [x] OPS-01: traceability, validation report, changelog and canonical state update.

Given a valid scenario, when solved, all required artifacts must exist with units and evidence labels. Given incomplete historical inputs, when historical mode runs, it must refuse historical feasibility. Given a claimed sample-feasible candidate, independent replay and dense sampling must agree within reported tolerances; neither is a continuous-time certificate. Given a stricter force/geometry constraint, the validator must expose the violation. The full landing sequence must include touchdown and a stop, not only threshold capture.

## Verification

Run pytest, the existing six-case finite-roll benchmark, scenario solve and explicit historical-mode refusal. Inspect numerical artifact contents and plot. Record every unresolved empirical requirement separately from executable correctness. No VCS exists at workspace root; no commit/push claim.

## Spec change log

Initial v1 selections made under explicit user delegation. Deterministic normalized slack is explicitly a research proxy; universal gust tolerance remains unimplemented and cannot be inferred from wind-conditioned trajectories.


## Implementation closure

Executable-model acceptance passed 13 October 2026. See MODEL_VALIDATION_REPORT.md for 52 correctness tests, 29 artifact checks and preserved full-study gaps. Numerical repairs did not alter the frozen aircraft, envelope, terminal target or nominal objective. Primary/secondary solver-mesh loss is budgeted at 5e-5 and verified against the required 1e-4 on the denser mesh. Default maximum iterations: 600. This closes implementation v1, not the historical study.

## Suggested review order

- Understand fixed meaning and evidence limitations first.
  [MODEL_EQUATIONS.md:1](MODEL_EQUATIONS.md#L1)
- Inspect constraints, phase transitions and independent replay.
  [trajectory.py:1](model/trajectory.py#L1)
- Inspect objective sequencing, evidence labels and artifacts.
  [solve.py:1](model/solve.py#L1)
- Check observed, estimated and scenario parameter provenance.
  [config.json:1](model/config.json#L1)
- Review test evidence and remaining scientific gaps.
  [MODEL_VALIDATION_REPORT.md:1](MODEL_VALIDATION_REPORT.md#L1)
