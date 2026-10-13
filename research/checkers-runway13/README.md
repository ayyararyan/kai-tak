# Checkers with Runway 13

Executable **scenario research model**, specification: `MODEL_IMPLEMENTATION_SPEC.md`.
Aircraft selection is tied to the historical 747-409B case, but aerodynamic limits,
terrain, start point, corridor and braking are uncalibrated declared scenarios.
No output is flight guidance, a historical reconstruction, a safety certificate,
or a demonstration that a historical approach was suboptimal.

## Reproduce

From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pytest model -q
.venv/bin/python -m model.solve --out outputs/scenario
.venv/bin/python -m model.solve --mode historical --out outputs/historical
```

The last command intentionally exits **2** and writes a blocked JSON record.
Historical-input flags cannot bypass the gate. Calibrated historical aircraft,
terrain/obstacles and navigation-corridor ingestion remain unavailable.

A custom configuration may be supplied with `--config path.json`. Only constant
runway-frame wind vectors are accepted; time-varying gusts are rejected because
wind acceleration has not been modeled. Every scalar/vector parameter carries
units, source and observed/derived/scenario category in `model/config.json`.

## Fixed model and numerical method

The runway-relative frame has x along runway, y right, z up. Air velocity equals
ground velocity minus the declared steady wind. For airspeed V, air heading psi
and flight-path angle gamma, the orthonormal basis is tangent e_t, right e_r,
and upward normal e_u. With required acceleration a and gravity g:

```
F = m (a + g e_z)
L_u = F dot e_u; L_r = F dot e_r
L = hypot(L_u,L_r); bank = atan2(L_r,L_u)
qS = 0.5 rho V² S
CL = L/qS; D = qS (CD0 + k CL²)
T = D + F dot e_t
```

Density is `rho0 exp(-z/8500)`. Rate constraints use phasewise derivatives of interpolated bank/thrust, retaining
the larger-magnitude one-sided value at the phase join. Validation uses at least
10 times as many intervals as optimization, with a minimum of 1201 points/phase. The geometry is a quintic
Hermite approach and quintic Hermite flare, with endpoint-null polynomial shape
terms. Position, velocity and acceleration join continuously at the threshold;
there is no bank/thrust reset at this join. Initial/final accelerations are zero.
The initial EAS and air gamma are fixed with ground track −47°; threshold ground
track is 0°. Wind can separate air heading from ground track.

The optimizer changes two phase durations, touchdown distance and forward speed,
six approach-shape and two flare-shape coefficients. Exact decision order/bounds
are documented in `model/trajectory.py`. SLSQP first maximizes minimum normalized
operating-inequality slack eta, then minimizes integrated squared normalized bank,
roll-rate and thrust-rate demand while retaining first-stage eta within 1e−4. The solver allocates half that
tolerance to its own mesh and checks retention again on the denser validation
mesh. The default iteration cap is 600; feasibility and successful completion
of both objective stages are reported separately.
It is a **local finite-parameter, finite-grid search**, not a global optimum or
analytic feasibility proof. Search failure is `unresolved`, never infeasible.

For finite intervals, lower/upper margins are distance to each bound divided by
interval width; symmetric magnitude limits use `1-abs(value)/limit`. Stop slack
is excess distance beyond the 150 m required reserve divided by usable LDA.
Imposed endpoint equalities and inevitable zero altitude at ground contact are
excluded from eta; nonnegative height and positive forward ground speed remain
hard constraints. These scaling choices are part of the declared proxy objective.

The nominal 400 m corridor is a 3D nearest-distance tube around a fixed dense
unoptimized reference, unchanged for the candidate and sensitivities. Optional
obstacles are vertical cylinders with keys `x_m,y_m,radius_m,height_m,clearance_m`.
The default empty list establishes **no historical clearance**. Obstacle margins
use the union of going outside an expanded cylinder or above its expanded top.
Airborne clearance remains sampled. The minimum distance to each obstacle along
the entire straight ground-roll segment is checked analytically, not just at
plot samples.

At touchdown the point-mass gear-reference vertical velocity is removed by an
inelastic contact impulse. Ground motion is straight: constant speed for 2 s,
then fixed 0.15g deceleration until stop. Ground steering, braking physics,
load transfer and gear dynamics are not inferred from this lumped rule.

## Independent verification

`solve_ivp` integrates Newton's law from the initial position/velocity, using only
time-indexed bank, CL and thrust interpolated from the inverse solution. It
recomputes airspeed, force directions, lift and drag from its own integrated state;
it does not call the reference acceleration as its RHS. It then independently
integrates the delayed-braking stop. Replay matching tolerances are 0.05 m maximum
position error, 0.005 m/s velocity error and 0.1 m stop error. All replayed path inequalities, terminal and stop constraint checks are
recorded separately from replay fidelity. A numerical margin within 1e-6 of a
constraint boundary is reported unresolved, not passed; the final z=0 ground
contact is treated as an equality residual.

Correct replay of an infeasible baseline is expected: replay fidelity proves
consistency, not feasibility. A candidate is labeled `sampled_scenario_feasible`
only after optimizer success, dense hard/operating constraint checks, replay
fidelity, touchdown checks and stop-reserve checks. Neither replay nor dense
sampling is a continuous-time certificate.

Sensitivity records include ±5 m/s changes to the nominal steady crosswind, +5% mass, and 10% less
braking. Wind cases hold the exact nominal ground curve and timing fixed and
recompute inverse controls conditional on known wind. This can change air-relative
endpoint speed/gamma: those cases are diagnostics, not re-solutions of the fixed
nominal boundary problem. They do not use one common feedback policy and **are
not robust gust-tolerance certificates**.

## Outputs

Each run directory contains:

- `baseline.csv`, `candidate.csv`: approach, flare and rollout with SI/unit-bearing
  column names; aerodynamic controls are blank during rollout, not false zeroes.
- `optimization_replay.json`: both optimizer stages, all margin minima/violations,
  denser-grid changes, forward replay, sensitivity, runtime and source hashes.
- `parameter_provenance.json`: complete executed parameter/source/category sheet.
- `trajectory.png`: standalone track, height, bank and EAS plot.
- `manifest.json`: sizes and SHA-256 checksums for delivered run artifacts.

The baseline is a synthetic unoptimized polynomial, **not a historical path**.
In the delivered run it violates modeled constraints: it is an infeasible seed,
not an admissible flight against which historical improvement can be claimed.
An improvement in its objective does not fulfill the historical-comparison aim.
The broader project still needs normal-flight observations, calibrated historical
obstacles/performance, go-around viability and robust feedback-policy analysis.

## Review and acceptance

Independent findings and repair decisions are recorded in `reviews/`.
`reviews/verify_artifacts.py` checks saved output schemas, hashes, phase ordering,
stop formulas and numerical acceptance separately from the solver.
The broad study remains incomplete even when these executable-model checks pass.
