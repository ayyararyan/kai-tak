# Checkers with Runway 13 — research specification draft

13 October 2026. Research-scoping package completed; model scope proposed, not frozen. No operational safety or novelty claim.

## Executive conclusion

All three research lanes delivered inspectable artifacts. A closed-form finite-bank-rate heading-change benchmark is derived and numerically checked. Primary historical geometry and the limitations of available recorder evidence are documented. Existing landing-optimization literature supplies serious comparators. No historical approach has been proved suboptimal, and no improved landing has been demonstrated.

## Aim 1: derive bounds

MATH-01: reproduce circular-turn geometry and the finite-bank-rate heading benchmark, with stated domains and units. Status: finite-roll benchmark derived; six synthetic cases pass; not a complete landing solution.
MATH-02: formulate position, heading/track, speed, descent, bank and finite bank-rate constraints with lift, thrust and stall/load feasibility. Status: proposed equations in foundations/MATHEMATICAL_FOUNDATIONS.md; calibration unperformed.
MATH-03: derive necessary exclusions and constructive sufficient conditions for a terminal target, retaining unresolved states. Status: pending. A heading-only minimum cannot be transferred unchanged to variable-speed/descent dynamics.
MATH-04: incorporate historical terrain, wind uncertainty, tracking information and go-around conditions. Status: specification and data pending; no such guarantee exists yet.

The exact benchmark assumes fixed airspeed/descent, constant wind, sufficient lift/thrust and wings-level endpoints. Its optimum is a ramp/hold/ramp bank profile, or triangular bank profile for small heading changes. Illustratively, 70 m/s, 25-degree bank cap, 5-degree/s bank-rate and 47-degree AIR-HEADING change gives 17.7218 seconds, versus 12.5568 seconds with instantaneous banking. These are synthetic values, not historical operating parameters or full landing bounds.

## Aim 2: confront historical records

DATA-01: retain primary dated procedure geometry. Status: CAD1993 chart recovered:088-degree magnetic IGS and135-degree runway. Do not replace with IVAO simulation redraw136/48-degree values. Magnetic/true coordinates and historical obstacles still need georeferencing.
DATA-02: obtain numerical routine-flight records plus dictionary, timing, aircraft/load/configuration and use permissions. Status: blocked on archive access; BA/Cathay raw records not obtained. Requests drafted, unsent.
VAL-01: uncertainty-aware CAL605 curve digitization and consistency tests. Status: not started. This is an accident case, not a successful-expert distribution. The ground track is acceleration-integrated, so testing it against the same acceleration is not independent validation.
VAL-02: compare held-out historical paths against bounds, explaining any apparent impossibility before drawing conclusions. Status: pending; general normal-flight validation requires DATA-02.

The CAL605 report does not attribute the accident to unacceptable touchdown parameters; the case cannot be used to presume the final-turn geometry caused its runway overrun. Cockpit control positions are not interchangeable with surface deflections; throttle-lever angle is missing.

## Aim 3: investigate improvement

OPT-01: define a reproducible baseline, common feasible set and objective before optimizing. Status: proposed.
OPT-02: produce and independently verify an admissible alternative; quantify advantage beyond measurement and numerical errors. Status: not started.
OPT-03: compare robustness/tracking burden and retain go-around requirements. Status: not started.
OPT-04: separate any modern-guidance or route-redesign arm from same-historical-conditions comparison. Status: design rule only.

One feasible strictly better candidate disproves optimality of the specified baseline for the specified objective. It does not prove global optimality or lower real-world accident probability. Local solver failure and Monte Carlo nonfailure cannot supply universal certificates.

## Recommended decisions, still unfrozen

1. Main arm: optimize within the historical approach corridor; label any redesigned route/modern-guidance arm separately.
2. Begin the analytical phase with a documented parameter envelope, not an invented aircraft calibration. CAL605's747-400 configuration is an available case, not automatically the chosen representative aircraft.
3. Separate runway-aligned pre-flare capture from complete landing. A pre-flare model is a stage, not fulfillment of the full landing aim; flare/touchdown/runout must be modelled before claiming full-landing improvement, or explicitly excluded by Aryan.
4. Prefer robust constraint margin over minimum time as the safety-oriented primary objective. Wind class, available observations, controller/pilot dynamics, commitment gate and secondary objectives need definition. Do not silently adopt this recommendation as approval.

## Next concrete milestone

Prepare a source-backed geometry and parameter sheet and select the comparison target/objective. Reproduce the finite-roll benchmark in runway coordinates, then establish a position/descent-constrained numerical reference under the same declared reduced model. Confront the available historical case only with propagated reconstruction uncertainty. Routine-flight acquisition continues as a separate dependency and is not reported complete.

## Files and verification

- foundations/MATHEMATICAL_FOUNDATIONS.md: proof, model proposal and limitations.
- foundations/verify_finite_roll.py and verification_results.json: six synthetic cases. Parent reran successfully13 October2026; numerical checks corroborate, not replace, proof.
- evidence/EVIDENCE_REPORT.md and CSV inventories: historical source checks and provenance.
- literature/LITERATURE_AND_COMPARISON.md and SOURCE_MATRIX.csv: eight-source matrix, including6-DoF landing comparator Kim et al2024 (https://arxiv.org/html/2405.16680v1).

Reports inspected by parent. This is a completed initial research package, not completed three-aim study. No publication, outreach, full simulator or proven safer alternative. Some literature/source retrieval failed and is documented; absence of a located KaiTak paper is not proof of novelty.
