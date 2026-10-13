# Analytical-first research direction

Updated 13 October 2026 from Aryan's explicit voice request at 16:14 IST. This records the interpreted task, not the raw transcript.

## Objective

Investigate whether an analytically derived, provably optimal landing solution can be obtained for the Kai Tak Runway 13 checkerboard approach. Reconstruct historical terrain/obstacles and procedure requirements, obtain relevant approach instructions and flight evidence, and use those to define and confront the mathematics. A calibrated numerical path alone does not fulfill this request.

The requested end object is a parameterized optimal trajectory or policy as a function of specified entry state, aircraft parameters, environment and landing target, accompanied by a proof and a stated validity domain. A convenient closed-form feasible path is not enough: optimality must be shown for a precisely defined objective and admissible set.

## Binding interpretation

- Keep the three original aims: mathematical bounds/solution; confrontation with historical flight evidence; investigation of an improved admissible approach.
- Analytical derivation is now the active front. Preserve numerical model v1 and its evidence as a verification/reference instrument, not the project's main claimed contribution.
- 1993 is the working reconstruction date because it matches the CAD primary chart and documented aircraft case. This date is a stated research assumption, not an assertion that all archive inputs from that year are available.
- Separate natural terrain, historical buildings/obstructions, coast/reclamation geometry, runway/threshold, and procedure/navigation constraints. A modern DEM or current 3D city model is not a 1993 obstacle map.
- Historical procedures specify allowed operations, not one uniquely optimal pilot path. Flight records can falsify or validate model implications but cannot by themselves prove an optimum.
- Retain v1's nominal minimum-constraint-margin objective for its own scope. Tractable minimum-bank/minimum-time subproblems are analytical benchmarks, not silently substituted full-study objectives.
- Do not presume that the complete nonlinear, terrain-constrained, uncertain-wind landing admits an elementary formula. Do not presume it cannot either; investigate the exact formulation.

## Solution/evidence classes

1. Explicit elementary formula, with domains and branches.
2. Explicit special-function representation; distinguish evaluation from solving an optimization.
3. Analytical characterization requiring scalar roots or switching-time equations; call semi-analytical/implicit, not fully explicit.
4. Necessary optimal-control conditions without sufficiency: candidates, not global proof.
5. Numerical optimization/checks: useful verification, not the requested analytical result.

An exact formula in uncertain parameters is still conditional on those parameters. Terrain uncertainty and aerodynamic calibration do not disappear because the optimization is analytical.

## Current bounded investigation

- Reconstruction lane: verify primary historical map/aerial/procedure/record sources; acquire accessible small public artifacts; identify date, datum, precision, license/access and uncertainty barriers. No external outreach or paid purchases authorized.
- Analytical lane: attempt an exact position-constrained straight–circular-turn–straight theorem with explicit parameter domain and family-optimality proof, then examine descent/altitude coupling and finite-roll limitations. This is a test of tractability, not completion of the full landing problem.
- Parent: challenge proof assumptions, distinguish altered initial-state data from valid same-state comparisons, reconcile results and preserve the next proof milestone.

## Acceptance of this investigation

Deliver source evidence with acquisition status; an inspectable derivation and synthetic verification where achieved; a clear account of which constraints break the current closed-form reduction; and a concrete next analytical problem. Do not relabel this investigation as an exact full Kai Tak solution, a completed 1993 terrain reconstruction, or demonstrated historical superiority.

## Authorized continuation — 13 October, 16:49 IST

Aryan requests finite-roll position matching first, then derivation and completion of the full closed-form landing. Preserve that sequence and the full target; do not equate completion of the first theorem with completion of the request. The existence of a full closed form is unestablished. Attempt the derivation with the existing aircraft, full boundary states, nominal margin objective and hybrid approach/flare/stop model. Distinguish the finite-dimensional numerical trajectory family from the unrestricted physical control problem and from historical/robust claims.

Deliver inspectable finite-roll derivations with independent integration checks, then the full-landing analytical formulation and any achieved sufficient certificates. Where no full solution is achieved, report the exact unresolved mathematics or missing inputs, not a fabricated formula or a claim of impossibility. No change to frozen numerical v1 is authorized merely to make the mathematics tractable.
