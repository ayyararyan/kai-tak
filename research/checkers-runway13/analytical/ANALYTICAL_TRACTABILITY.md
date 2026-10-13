# Analytical tractability: position-constrained S–C–S benchmark

2026-10-13. Exploratory mathematics, not an operational approach. This is a new project derivation, **not a claim of literature novelty**. The frozen simulator and its nominal-margin objective are unchanged. The existing six finite-roll heading tests are prior work, not the result below.

## Result and scope

A closed elementary solution exists for the best straight–right-circle–straight (S–C–S) path in a deliberately restricted, no-wind, instantaneous-bank family with prescribed initial/final horizontal positions and headings. It solves a position-constrained problem, unlike the prior heading-only benchmark. Minimum horizontal distance/time and minimum peak bank agree when descent angle is held fixed and altitude is not independently fixed. If altitude loss is fixed and descent angle is allowed to vary between paths, the minimum-bank radius instead has an exact cubic characterization and an elementary hyperbolic-function expression. This distinction prevents an incorrect “largest radius is always best” claim.

Neither result solves full landing, proves optimality over all curves, validates the historical corridor, or optimizes the frozen full-model nominal minimum constraint slack. No whole-landing closed form or global certificate has been found.

## 1. Defined object, units and assumptions

Runway-relative x is forward, y is right; heading increases toward +y, so a right turn increases heading. Initial position is (x0,y0), initial heading −δ, final position (xt,0), final heading 0. Let X=xt−x0, 0<δ<π (radians), horizontal speed U>0 (m/s), g>0 (m/s²). Radius R, straight lengths s and ℓ, and horizontal arclength D are in metres. The turn has no extra winding. Zero-length straights are allowed. R>0; a zero-radius kink is not a trajectory.

The family consists of a straight at heading −δ, a constant-radius increasing-heading turn through δ, then a straight at heading 0. There is no wind, terrain, obstacle, finite-roll or engine-lag constraint in the geometric theorem. Coordinated point-mass lift/thrust feasibility is a separate conditional requirement. Endpoint zero bank is obtained only by instantaneous bank jumps. No jump is admissible in the frozen finite-roll model.

All numerical inputs below are synthetic/scenario-based. The 1993 reconstruction must ultimately supply constraints, not be inferred from these inputs. The target is an aligned gate, not touchdown/stop.

## 2. Exact geometry and feasibility interval

Put A=tan(δ/2)>0, B=2A−δ>0 and C=X+y0 A. Integrating the tangent over the circular arc gives displacement (R sinδ, R(cosδ−1)). Endpoint equations are

    y0 − s sinδ − R(1−cosδ) = 0,
    X = s cosδ + R sinδ + ℓ.

Consequently the unique straights for any R are

    s(R) = y0/sinδ − R A,
    ℓ(R) = X − y0 cotδ − R A,
    D(R) = s + Rδ + ℓ = C − B R.

With a prescribed positive minimum radius Rlo (or merely R>0), define

    Rgeo = min{ y0/(1−cosδ), (X−y0 cotδ)/A }.

The exact feasible radius set is [Rlo,Rgeo] if Rlo>0 and Rgeo≥Rlo; without a positive lower bound it is (0,Rgeo], nonempty precisely when Rgeo>0. Negative candidate upper bounds mean this family is empty. This is not infeasibility of other path families. Each admissible R yields s,ℓ≥0 and D≥Rδ>0. The upper bound is attained, with at least one straight zero. If strictly positive straights are required, the same endpoint may be only an infimum, not an attained optimum.

**Proof of the family optimum.** Since tan z>z for 0<z<π/2, B>0, so D′=−B<0. At fixed U, T=D/U decreases strictly with R. In level flight peak bank is atan(U²/(gR)), also strictly decreasing. Hence R*=Rgeo uniquely minimizes both over a nonempty closed interval. The proof is global over this one-parameter family, not over all admissible flights. Longer arcs, opposite turns, multiple turns and nonconstant curvature are not enumerated by it.

Degeneracies: δ=0 is a separate straight problem (y0=0, X≥0); the radius parameter is then irrelevant and the formulas must not be evaluated. δ=π is excluded: sinδ=0 and a separate semicircle construction is needed. Small δ causes floating-point cancellation in B and 1−cosδ; use series/stable identities in precision-sensitive applications. δ<0 is obtained by a reflected family only after changing y/sign consistently. A radius upper bound of zero is no positive-radius solution, even if a zero-radius limit exists.

## 3. Descent: compatible extensions, not an independent decoration

For constant flight-path angle γ∈(−π/2,0], U=V cosγ. Constant γ and V in the no-wind point-mass equations require

    Lift cosφ = mg cosγ,
    ψdot = (g/V)tanφ = U/R,
    tanφ = U²/(g R cosγ),
    n = Lift/(mg) = cosγ/cosφ,
    Thrust = Drag + mg sinγ.

Thus atan(U²/(gR)) is valid only at γ=0. At fixed γ, bank still decreases with R. Density variation may require changing CL and thrust along the path. Required lift, CL, nonnegative/available thrust, speed and load limits must be checked independently. Instantaneous bank changes also imply instantaneous changes in required lift and drag; this relaxation does not satisfy actuator limits.

**Fixed γ and exact altitude loss H≥0:** H=−D tanγ. For γ<0 this fixes Dreq=H/(−tanγ) and, since B>0, fixes R=(C−Dreq)/B. It is feasible only if that radius belongs to the geometric interval. There is generally no remaining radius optimization. At γ=0 only H=0 is compatible.

**Fixed H>0, selectable constant descent magnitude β=−γ in [βmin,βmax], 0≤βmin≤βmax<π/2:** each path must use β(R)=atan(H/D(R)). Boundary data fix positions, altitude loss, horizontal speed and horizontal headings only; initial and terminal vertical velocity, flight-path angle and total airspeed are free across candidates. Its time remains D/U, but its true airspeed V=U sqrt(1+(H/D)²) changes across paths. Thus this is not a fixed-TAS or fixed-full-initial-state comparison, and in particular not a fair replacement for the frozen scenario's fixed initial γ. Bounds translate exactly into

    H/tanβmax ≤ D ≤ H/tanβmin,

where the upper length is +∞ when βmin=0; βmax=0 is incompatible with H>0. Intersect the corresponding radius interval [(C−Dmax)/B, (C−Dmin)/B] with the geometric interval and any independently justified radius bounds. At H=0, γ=0 and the level theorem applies, provided βmin=0.

## 4. New altitude-coupled minimum-bank certificate

On a nonempty compact radius interval [a,b] with a>0, fixed H>0 and selectable constant slope as above, minimizing peak bank is equivalent to minimizing

    f(R) = sqrt(1 + H²/(C−BR)²)/R.

Here C>0 on any feasible family. With D=C−BR,

    d(log f)/dR = −1/R + B H²/[D(D²+H²)].

Its sign equals the sign of C H²−D³−2H²D. The polynomial P(D)=D³+2H²D−CH² is strictly increasing on D≥0, with P(0)<0 and P(C)>0. It has exactly one positive root D0∈(0,C). Therefore f decreases for R<(C−D0)/B and increases after it. The unique family minimum is

    Rbank = clip((C−D0)/B, a, b),
    D0 = 2H sqrt(2/3) sinh[(1/3) asinh(3 sqrt(3) C/(4 sqrt(2) H))].

This is an elementary expression (sinh/asinh have exponential/logarithmic definitions), not a numerical optimizer. The displayed real sinh/asinh branch is single-valued for H>0 and C>0; there is no choice among complex cubic branches. The interval must retain D=C−BR>0 (automatic inside the positive-radius geometric interval). At H=0 use the level result instead of the singular expression. Minimum time remains at b. Thus the two criteria can conflict under altitude coupling. A synthetic large-heading/steep-descent case below exercises an interior bank optimum; it is deliberately not representative of Kai Tak or an admissible airliner approach.

The certificate remains conditional if unmodeled lift/thrust/terrain constraints are imposed: intersecting an arbitrary feasible set need not leave an interval, and a rejected analytic minimizer does not prove that every smaller-radius path is rejected. Constraints on speed, sink, γ and altitude can be translated where possible; general aerodynamic constraints require their own exact feasibility analysis.

## 5. What “analytical full landing” would require

1. **Elementary geometry:** the result above is exact but family-restricted. It can calibrate endpoint handling and conditional bounds; it is not automatically an outer relaxation of the full variable-speed problem, because fixed U/γ and S–C–S are restrictions. Therefore its optimal objective is not automatically a lower bound on the whole-landing optimum.
2. **Special-function/quadrature representation:** finite roll produces ψ from log sec on ramps; integrating sin/cos of that heading need not be elementary. A recognized special-function or quadrature representation still describes a trajectory exactly, without selecting its optimal switches.
3. **Implicit switching equations:** endpoint matching, force envelopes and phase joins can reduce to roots of analytic/transcendental equations. Calling that “closed form” must disclose the root problem and how all relevant roots are isolated. A numerical root is not an elementary expression.
4. **PMP necessary conditions:** these can identify candidate bang/boundary/singular arcs but generally do not prove global optimality; state-constrained arcs, nonsmooth phase joins, and abnormal cases require attention. No PMP derivation for the complete frozen model is supplied here.
5. **Global proof:** needs a sufficient verification theorem/value function, a proved exhaustive candidate class with certified root/objective comparison, or a matching global lower bound and feasible construction. Dense simulator replay and multistart success provide none of these by themselves.

Finite roll changes turn displacement and matching lengths, not just time; adding prior roll-in/roll-out time to this S–C–S solution is not a valid extension. The earlier heading-only envelope remains a conditional independent check, not a certificate for this position problem. Variable speed, lift/thrust slew, altitude-dependent aerodynamics, flare/contact, braking, dated corridor/obstacles, uncertain wind, available information and go-around viability remain the full-solution gap. No theorem here establishes that an elementary full solution is impossible either.

The frozen objective is nominal minimum dimensionless constraint slack over approach/flare/stopping, then normalized effort. Neither shortest time nor minimum bank silently replaces it. A full proof must target that objective or an explicitly authorized new mathematical objective. Historical reconstruction and interval uncertainty should define admissible comparisons before attributing superiority to a curve.

## 6. Literature boundary and verification

[Wu & Chen (2024), arXiv v1](https://arxiv.org/abs/2412.04797) is a primary precedent for analytically characterized constant-speed steady-wind candidate paths, including transcendental root problems. Its archived PDF under ../literature/sources/wu_chen_2024.pdf was text-inspected in this session. It is not a finite-roll descending full-landing theorem. The existing literature report contains further leads, not a novelty certificate. New web access failed with a provider permission error; no fresh exhaustive literature search is claimed.

`verify_scs.py` independently integrates turn tangents using composite Simpson quadrature, checks endpoint/length identities, geometric boundary and rejection cases, within-family monotonicity, altitude matching, force/yaw identities and the cubic optimum against dense synthetic comparisons. Results are `verification_results.json`; all inputs, test counts and worst residuals are retained. Numerical checks corroborate the algebra; they are not certified interval arithmetic or solver calibration. Run from any directory: `python3 research/checkers-runway13/analytical/verify_scs.py` (adjust relative path as needed).

Executed 2026-10-13T10:49:57Z: 80 constructed random cases, two deterministic examples, four explicit domain rejections and the fixed/bounded-descent branches passed. Largest endpoint quadrature residual was 1.05×10⁻¹⁰ m; normalized cubic residual 7.36×10⁻¹⁶. These are floating-point algebra-check errors, not accuracy of an aircraft model. The 47° synthetic gate gives Rgeo≈3144.64 m and conditional minimum bank≈9.037° at U=70 m/s, H=124.76 m; it frees descent angle to about 2.570° and has a zero-length first straight. It is not compatible with the frozen model's fixed 3.1° initial descent and finite roll. The intentionally steep 170° example gives minimum-bank R≈952.24 m versus minimum-time R=1000 m, verifying a strict separation of the objectives.

**Correctness:** proofs above plus synthetic numerical checks. **Specification completeness:** this bounded analytical task is supplied; full analytical landing remains incomplete. **End-to-end readiness:** no historical feasibility, whole-landing global optimum, operational clearance, live flight or publication claim. Frozen simulator untouched.
