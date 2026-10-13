# Checkers with Runway 13: mathematical foundations

Date: 2026-10-13. Status: exploratory derivation and **proposed**, unfrozen model design.

## Answer to the research question

It is mathematically possible to demonstrate that a specified historical flight path is suboptimal: produce another admissible path with a strictly better value of a declared objective, while holding the aircraft, initial state, destination, environment and available information fixed. We have **not** demonstrated that for Kai Tak. There is no evidence here that the historical procedure was advertised or proved globally optimal. A procedure defines permitted operations, not one universal trajectory.

Closed form is useful for understanding and verification, but is neither necessary nor sufficient for proving improvement. A numerical candidate can establish improvement if its continuous-time feasibility and objective difference are certified with error bounds; a closed-form candidate can fail to be feasible.

The three user aims remain intact: establish bounds; compare historical observations; investigate an improved path. This note supplies a mathematical starting point, not a substitute for the unavailable normal-flight data or a completed comparison.

## 1. Fixed comparison versus route redesign

Two different questions must not be conflated:

1. **Within-procedure optimization:** keep the same entry gate, historical corridor, runway target, aircraft envelope and pilot/navigation information. Change the timing and shape of the turn and descent within those constraints.
2. **Procedure redesign:** allow a different approach corridor, earlier turn, different navigation technology or entry geometry. This can be valuable, but an improvement does not show that pilots or the old procedure were suboptimal under their original constraints.

Recommend the first as the main comparison, with the second explicitly labelled an extension. This is a recommendation, not a frozen choice. In particular, a trajectory cutting through an unavailable visual-reference region or relying on perfect wind preview is not a valid improvement on a visual historical procedure.

The approximately 47-degree historical offset is a **nominal ground-track/procedure angle**. With wind, air-relative heading and ground track differ. Do not hard-code 47 degrees as the aircraft's heading change for every weather scenario.

## 2. Proposed state, controls and force model

Use a local North–East–Up frame, converted to a runway-relative frame for plots. All angles below are radians. Let

\[
z=(N,E,h,V,\gamma,\psi,\phi),\qquad u=(q,T,C_L),\quad \dot\phi=q.
\]

Here V is true **air**speed; gamma is air-relative flight-path elevation; psi is heading measured from north toward east; phi is bank toward increasing psi; q is bank-angle rate, not necessarily body-axis roll rate. T is thrust along air-relative velocity. C_L is a reduced lift command, not a measured elevator position. Mapping these commands to real actuators requires another aircraft model. Mass m and configuration are held fixed over this short segment; their numerical values remain unset.

Define the orthonormal basis

\[
e_V=(\cos\gamma\cos\psi,\cos\gamma\sin\psi,\sin\gamma),
\]
\[
e_\gamma=(-\sin\gamma\cos\psi,-\sin\gamma\sin\psi,\cos\gamma),
\qquad e_\psi=(-\sin\psi,\cos\psi,0).
\]

Let wind w be a vector in this frame. Then

\[
\dot r=V e_V+w,
\quad L=\tfrac12\rho(h)V^2SC_L,
\quad D=\tfrac12\rho(h)V^2S(C_{D0}+kC_L^2).
\]

The parabolic drag polar is a proposed approximation to calibrate, not an aircraft fact. For differentiable wind, let its material acceleration along the trajectory be

\[
a_w=\partial_t w+(\nabla w)\dot r.
\]

A coordinated point-mass model is

\[
\dot V=(T-D)/m-g\sin\gamma-a_w\cdot e_V,
\]
\[
\dot\gamma=\{L\cos\phi/m-g\cos\gamma-a_w\cdot e_\gamma\}/V,
\]
\[
\dot\psi=\{L\sin\phi/m-a_w\cdot e_\psi\}/(V\cos\gamma),\qquad\dot\phi=q.
\]

These equations follow by projecting Newton's equation for ground acceleration onto the three basis vectors. They assume negligible sideslip, lift perpendicular to air velocity, thrust aligned with it, no explicit pitch/yaw dynamics and V>0, |gamma|<pi/2. This is not a six-degree-of-freedom airliner model.

For **constant** wind a_w=0. An arbitrary time-varying wind cannot simply be added to the position equations while leaving airspeed/attitude force equations unchanged. A merely amplitude-bounded but arbitrarily rapidly changing wind is not enough to define this force model: specify temporal/spatial regularity or use a stochastic/gust-state model and its own equations.

To improve physical fidelity later, add thrust lag, lift/angle-of-attack dynamics and roll acceleration limits, and calibrate against aircraft evidence. They are not silently assumed covered by a bank-rate cap.

### Required admissibility constraints

- Bank and bank rate: |phi|<=b, |q|<=p; parameters depend on aircraft/configuration and authority definition.
- Lift/load/stall: n=L/(mg); 0<=C_L<=C_L,max with a declared operating margin, n<=n_max and configuration-dependent speed limits. No numerical C_L,max or n_max selected here.
- Thrust and drag: T_min<=T<=T_max(V,h,configuration); a constant-speed descending turn is feasible only if the required thrust is available. Add engine response limits where needed.
- Descent: allowable gamma, ground vertical speed V sin(gamma)+w_h, and vertical acceleration/load limits; do not independently prescribe mutually incompatible speed, descent, lift and thrust.
- Geometry: r(t) must lie in a dated historical permitted corridor; h(t)>=H_terrain(N,E)+m_clearance. The clearance definition must account for terrain/building errors and aircraft dimensions, not just a point passing over a DEM.
- Time: a defined finite horizon or crossing target; no indefinite circling to evade the intended approach task.
- Information: controls use observations available at that time. Perfect foresight and feedback control are different comparison classes.

The FAA handbook supports the fundamental coupling between bank, load factor and stall speed in level turns, but it is **not** evidence for this project's aircraft-specific operating limits. [FAA Pilot's Handbook of Aeronautical Knowledge](https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak).

### Terminal target and go-around

Proposed target: a **pre-flare runway-aligned gate**, not touchdown. Specify along-runway station, cross-track and altitude tolerances, speed range, flight-path angle/vertical-speed range, bank tolerance and heading/ground-track requirements separately. Crosswind touchdown cannot be reduced to a single heading-equals-runway equality.

Reaching this gate does not certify flare, touchdown or stopping distance. A full landing claim must add those stages.

If preserving a go-around option is part of safety, define a second target and recovery constraints. A proposed viable state set is the set from which an admissible feedback policy reaches that recovery target for every allowed disturbance. Requiring the approach to stay in this set up to a declared commitment boundary is stronger than checking nominal landing feasibility. No recovery set has yet been computed.

## 3. Exact finite-roll analytical benchmark

This derivation is our own elementary benchmark; **no novelty is claimed**. It solves a restricted heading-change problem, not a position-constrained landing.

Assume constant true airspeed V; constant flight-path angle gamma; uniform constant wind; sufficient lift/thrust to maintain these conditions; bank magnitude cap 0<b<pi/2; bank-rate cap p>0; wings-level endpoints phi(0)=phi(T)=0. Define an unwrapped positive heading change delta>=0 with no extra winding. The still-air case is included.

From dot gamma=0,

\[
n\cos\phi=\cos\gamma,\qquad n=\cos\gamma/\cos\phi.
\]

Therefore

\[
\dot\psi=\frac{g n\sin\phi}{V\cos\gamma}=\frac gV\tan\phi.
\]

At fixed T any admissible phi obeys the pointwise envelope

\[
\phi(t)\leq\min\{pt,p(T-t),b\}.
\]

This follows from the two zero-bank endpoints and the rate cap. Because tan is increasing on (-pi/2,pi/2), its integral, hence positive net heading change, is maximized by exactly this envelope. Negative banks cannot improve the maximum. Thus the greatest attainable heading change is

\[
A(T)=\begin{cases}
\frac{2g}{Vp}\log\sec(pT/2),&T\leq2b/p,\\
\frac gV\left[\frac2p\log\sec b+(T-2b/p)\tan b\right],&T\geq2b/p.
\end{cases}
\]

Any trajectory with delta>A(T) is impossible **under these assumptions**. For the heading-only problem the bound is tight: the envelope attains it, so inverting A gives the exact minimum time.

Define

\[
\delta_c=\frac{2g}{Vp}\log\sec b.
\]

Then

\[
T_{\min}(\delta)=\begin{cases}
\frac2p\arccos\!\left(e^{-Vp\delta/(2g)}\right),&0\leq\delta\leq\delta_c,\\
\frac{2b}p+\frac{V\delta/g-(2/p)\log\sec b}{\tan b},&\delta\geq\delta_c.
\end{cases}
\]

The first branch is a triangular bank profile; the second ramps to the bank cap, holds it, and ramps down. An exact constructive heading history on the entry ramp is

\[
\psi(t)-\psi(0)=\frac{g}{Vp}\log\sec(pt).
\]

The hold and exit segments follow by integrating the same scalar equation. Position is then obtained by quadrature of V cos(gamma)(cos psi,sin psi)+w_horizontal. We do **not** claim an elementary closed form for that position integral. The result is already useful because it exactly rejects insufficient time for a required heading correction, independently of a numerical optimizer.

For an available gate-time upper bound T_avail, delta>A(T_avail) rules out the approach in this model. A feasible heading time does not establish feasible position, clearance or descent. If constant gamma<0 and still air are retained, the associated altitude loss is -V sin(gamma) T; this supplies an additional conditional altitude-budget test. It is not valid unchanged when gamma is controlled.

### Illustrative numbers, not Kai Tak aircraft calibration

V=70 m/s, delta=47 degrees, b=25 degrees, p=5 degrees/s yield:

- Instantaneous-bank heading time: 12.55683 s.
- Finite-roll minimum heading time: **17.72178 s**.
- Roll in/out: 5 s each; bank-cap hold: 7.72178 s.

Finite roll adds 5.16495 s, about 41%, in this particular comparison. This illustrates why the circular-turn baseline alone is insufficient. It is **not** evidence that historical pilots turned too late or that our path is safer. For 2 degrees/s the same mathematical heading minimum is 25.46922 s.

At constant gamma the reduced-model load requirement is cos(gamma)/cos(phi), so bank feasibility additionally requires this to remain below both structural and aerodynamic availability. In level flight the speed constraint can be written V>=sqrt(2mg/(rho S C_L,max cos(phi))) before applying any operating margin. A bank cap alone does not enforce it.

### Proof scope and relaxation caution

The exact heading optimum is a lower bound for a more constrained problem **only when its dynamics and speed/descent assumptions are compatible**. Adding position/terrain constraints while keeping V and gamma fixed cannot reduce the minimum time. Allowing variable speed/gamma changes the problem, so our numerical 17.72 s must not be reused as its universal lower bound. For a truly relaxed bound, prove a uniform heading-rate envelope over the larger state/control set first.

## 4. What optimal and safer can mean

Proposed primary criterion: maximize a specified disturbance tolerance, subject to hard physical/geometric/terminal constraints. Define

\[
\eta^*(z_0)=\sup\{\eta:\ \exists\text{ causal policy }\pi\ \forall w\in\mathcal W_\eta,
\ z^{\pi,w}\text{ satisfies constraints and reaches target}\}.
\]

This is robust **model-relative feasibility**, not a probability of an accident. It differs from an oracle that chooses a separate path after seeing each entire wind realization: swapping exists-policy and for-all-wind changes the object. The uncertainty set must encode measurement uncertainty, gust regularity and actual feedback information. Minimize effort/bank demand or time only as declared secondary objectives, or publish a Pareto frontier instead of an arbitrary weighted score. This preference remains proposed.

To claim baseline suboptimality, define baseline B and objective J before tuning. For minimization, establish both trajectories feasible under identical conditions and J_new<J_B by more than numerical/data uncertainty. Proving global optimality of the new candidate is a different requirement. A local solver failure is not proof of infeasibility; retain **feasible / infeasible by certificate / unresolved** labels.

## 5. Historical comparison and what the evidence identifies

- Historical charts and procedures: observed documentary constraints, subject to edition/georeferencing errors.
- Recorder samples: observed parameters if raw decoded files obtained; parameters have units, timing and sensor errors.
- Digitized accident-report curves: approximate measurements with digitization/calibration uncertainty, not restored raw samples.
- Reconstructed path/model controls: deterministically derived or estimated conditional on assumptions; controls are not uniquely identified from position alone.
- Proposed counterfactual path: scenario-based.
- Historical airline normal-flight distribution and pilot policy: currently unidentified from aggregate bank statistics and one accident case.

The acquired CAL605 material can test consistency or expose model failures, but it is an accident flight. It does not establish a normal expert baseline or typical pilot performance. Missing thrust-lever recordings must not be fabricated from engine indications. Its wind, aircraft and geometry can only be conditioned on after evidence review.

## 6. Relation to verified prior work

The checked version of [Closed-Form Solutions for Minimum-Time Paths of Dubins Airplane in Steady Wind](https://arxiv.org/html/2412.04797v1), particularly section 2, fixes altitude and airspeed, uses a bounded turning control, and imposes terminal position and heading. It assumes wind speed smaller than airspeed. Its candidate-path characterization is not a finite-roll descending-airliner theorem. It also uses transcendental root solving for some path families. Our inference: applying it directly to coordinates is a benchmark, not evidence of novelty, and it does not solve the full proposed problem. No exhaustive novelty search has been completed in this lane.

## 7. Four material choices to resolve before freezing the model

1. **Aircraft/configuration/mass:** recommend one historically documented aircraft configuration with an envelope sensitivity analysis. Do not pick a 747 solely because CAL605 is available; weigh access to reliable performance parameters and successful-flight evidence.
2. **Comparison and target:** recommend within-historical-corridor optimization to a specified pre-flare gate, keeping route redesign as a separately labelled extension. This gives a fair comparison and avoids claiming a completed landing when only the final turn is modelled.
3. **Objective and uncertainty:** recommend robust constraint feasibility as primary, then bank/effort; define the admissible wind/gust class and whether go-around viability is required. Shortest time alone is not a safety metric.
4. **Model fidelity and baseline:** recommend the finite-roll point-mass model as an analytical benchmark, checked against a higher-fidelity numerical model before historical performance conclusions. Specify whether B is one reconstructed flight, a family of observed flights, or a documented procedure-following controller; these support different claims.

These are pending model choices, not permission requests for the already-authorized source collection and mathematical exploration.

## 8. Verification and handoff

`verify_finite_roll.py` uses independent composite-Simpson integration of the heading ODE over roll/hold/roll segments. Six synthetic cases include triangular, capped, slow-roll, near-instantaneous-roll, zero-angle and a larger turn. It checks heading residuals, exclusion at 99.9% of the computed minimum time, the instantaneous-bank lower bound, branch continuity and the steady-descent yaw identity. Results are in `verification_results.json`. Run: `python3 research/checkers-runway13/foundations/verify_finite_roll.py`.

**Correctness:** analytical proof supplied; implemented formulas pass these synthetic numerical checks (largest recorded heading residual 2.23e-16 rad). The script corroborates, rather than replaces, the proof.

**Completeness:** this is the first mathematical foundations package only. Aircraft calibration, historical path comparison, wind/terrain reachability and improved landing-path demonstration remain incomplete.

**End-to-end readiness:** no landing simulator or operational controller; no demonstrated Kai Tak safety improvement; no certified result; no publication or external messages sent.
