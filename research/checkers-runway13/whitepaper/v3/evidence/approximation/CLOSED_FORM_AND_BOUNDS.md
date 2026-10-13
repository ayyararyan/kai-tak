# Explicit landing equations and the bounds actually supported

13 October 2026. **Full requested Kai Tak solution: INCOMPLETE.**

The stable terrain handoff is a verified documentary/source package, not a registered historical obstacle scene. Its `clearance_certified` field is false; historical footprint verification is zero; hard historical height intervals and aviation-datum reconciliation are null. The whole-AOI mask means historical validity is unknown, not that the area is physically blocked. Nine listed handoff artifacts match their sizes and SHA256 values on this lane's fresh verification.

The equations below reproduce the existing **synthetic, empty-obstacle reference**. They are not a terrain-aware Kai Tak solution, an operational procedure, or a calibrated real-aircraft prediction. The model configuration and source certificate are unchanged. The requested condition-to-procedure map remains unsolved.

## 1. Conditions and coordinates

The fixed research scenario uses the documented 747-409B configuration but an uncalibrated point-mass performance envelope. Initial position is (-2500,1000,140) metres in a synthetic runway-relative frame. x points forward from the displaced threshold, y right, z above runway. The initial inbound track is -47 degrees; nominal wind is the unchanged source configuration. This frame has no historical georeferencing.

Time zero is this synthetic entry state, not the beginning of an entire real approach. Two airborne phases are followed by an idealized ground-contact transition, a two-second braking delay and constant deceleration. The reference includes a brief climb permitted by the frozen model; it must not be described as monotone descent.

## 2. Complete explicit airborne path

For each phase i, define s=(t-t_i)/T_i, with 0 <= s <= 1, and

\[
\mathbf r_i(t)=\sum_{k=0}^{7}\mathbf c_{ik}s^k,
\qquad
\frac{d^j\mathbf r_i}{dt^j}
=\frac{1}{T_i^j}\sum_{k=j}^{7}\frac{k!}{(k-j)!}\mathbf c_{ik}s^{k-j}.
\]

All position coefficients have units of metres. The tables below preserve the stored floating-point coefficient representations. They are an explicit evaluation representation; the all-time source proof instead reconstructs exact real-decimal Hermite/bump expressions with interval arithmetic. Rounded displays must not be substituted into that proof.

### Approach

Start t = 0.0 s; duration T = 37.337760643281456 s.

| Power k | x coefficient | y coefficient | z coefficient |
|---:|---:|---:|---:|
| 0 | -2500.0 | 1000.0 | 140.0 |
| 1 | 2017.9112956851186 | -2163.944933098086 | -160.24403528424745 |
| 2 | 0.0 | 0.0 | 0.0 |
| 3 | 3413.9292942790535 | 4100.69024839948 | 3438.0222407732413 |
| 4 | -10204.99995335449 | -4778.257389770894 | -9897.948219629578 |
| 5 | 14739.635372583049 | 1189.8046753870922 | 9803.845767246206 |
| 6 | -10064.64238408444 | 1536.071423529094 | -3418.7192897022915 |
| 7 | 2598.1663748917094 | -884.364024446686 | 110.28353659666904 |

### Flare

Start t = 37.337760643281456 s; duration T = 4.000000000000006 s.

| Power k | x coefficient | y coefficient | z coefficient |
|---:|---:|---:|---:|
| 0 | 0.0 | 0.0 | 15.24 |
| 1 | 314.6612434330239 | 0.0 | -17.041443787549866 |
| 2 | 0.0 | 0.0 | 0.0 |
| 3 | -1.7953764829343304 | 0.0 | -51.839797578524994 |
| 4 | 3.3953132923579705 | 0.0 | 111.33383061107367 |
| 5 | -5.309847192239262 | 0.0 | -70.581049548823 |
| 6 | 2.540848107803186 | 0.0 | 12.888460303824205 |
| 7 | 0.0 | 0.0 | 0.0 |

The approach joins the flare at (0,0,15.24) m. The flare ends at (313.4921811580115,0,0) m with forward speed 77.88805495981877 m/s and incoming vertical velocity -0.7 m/s. Position, velocity and acceleration join continuously between the two airborne phases. At ground contact the existing model removes vertical velocity instantaneously; it does not model landing-gear impact physics.

These equations give a reference position schedule. Analytic derivatives and the existing inverse dynamics give nominal control demands. They do not constitute a gust-rejecting feedback law or a guarantee that a real aircraft tracks the reference.

## 3. Ground phase and outcomes

Let t_D=T_A+T_F, q=t-t_D, touchdown location x_D, forward touchdown speed u, braking delay d, deceleration a>0 and usable runway L. In this model,

\[
x(t)=\begin{cases}
x_D+u q,&0\le q\le d,\\
x_D+ud+u(q-d)-\frac12a(q-d)^2,&d\le q\le d+u/a.
\end{cases}
\qquad y(t)=z(t)=0.
\]

The solution ends at full stop; no later extrapolation is needed. Thus

\[
G=ud+\frac{u^2}{2a},\quad S=x_D+G,\quad R=L-S,
\qquad t_D=T_A+T_F,\quad t_{\rm stop}=T_A+T_F+d+\frac ua.
\]

Here G is ground travel including braking delay, S is threshold-to-stop runway consumption, and R is runway remaining. S is not the airborne 3D path length.

For x_D=313.4921811580115 m, u=77.88805495981877 m/s, d=2 s, a=1.4709975 m/s² and L=2786 m:

| Deterministic synthetic-model output | Value, rounded for reporting |
|---|---:|
| Entry to threshold | 37.34 s |
| Flare duration | 4.00 s |
| Entry to touchdown | 41.34 s |
| Touchdown beyond threshold | 313.49 m |
| Ground travel including braking delay | 2217.83 m |
| Threshold to stopping point | 2531.32 m |
| Runway remaining | 254.68 m |
| Entry to complete stop | 96.29 s |

Decimal precision is arithmetic, not physical accuracy. Real-world confidence/prediction intervals for every row remain unavailable.

## 4. Conditional deterministic error envelopes

Suppose evidence establishes a joint enclosing parameter box with x_D in [x_-,x_+], u in [u_-,u_+], d in [d_-,d_+], a in [a_-,a_+], L in [L_-,L_+], T_A in [A_-,A_+] and T_F in [F_-,F_+]. Require a_->0, u_->=0 and d_->=0. Monotonicity gives the exact range over that Cartesian box:

\[
S_- =x_-+u_-d_-+\frac{u_-^2}{2a_+},\qquad
S_+ =x_++u_+d_++\frac{u_+^2}{2a_-},
\]
\[
\boxed{R\in[L_- - S_+,\ L_+ - S_-]},
\]
\[
\boxed{t_{\rm stop}\in
[A_-+F_-+d_-+u_-/a_+,\ A_++F_++d_++u_+/a_-]}.
\]

Touchdown time is in [A_-+F_-,A_++F_+]. For any nominal R_0 and t_0, these also give absolute-error bounds max(|R_--R_0|,|R_+-R_0|) and max(|t_--t_0|,|t_+-t_0|). Dependence or flight constraints may make the box conservative. No statistical independence assumption is needed. Containment of scalars does not establish flight feasibility.

The existing `stopping_envelope` implementation uses exact rational endpoint algebra and outward-rounded output. Its test box is synthetic software verification, not estimated landing uncertainty. No actual physical parameter box is supplied by the terrain handoff, so no numerical physical error band can yet be attached.

## 5. Prediction intervals are not currently identified

For an individual landing outcome Y under stated conditions theta and policy pi, a central 95% model prediction interval would be

\[
[Q_{0.025}(Y\mid\theta,\pi),\ Q_{0.975}(Y\mid\theta,\pi)].
\]

This defines the requested statistical object; it is not a computed interval. It requires a justified joint law for inputs, aircraft-model discrepancy and tracking error, with relevant calibration and coverage validation. A CI for mean stopping distance answers a different question. Marginal intervals for several outcomes also do not establish joint or whole-path coverage. The 95% level here is illustrative notation, not a newly selected acceptance requirement.

Terrain's reported ±5 m at 90% is neither a worst-case bound nor a distribution for aircraft landing outcomes. It cannot produce a 90% or 95% runway-remaining interval. No Gaussian errors, independence assumptions, wind/braking ranges or missing-building probabilities have been fabricated.

## 6. Feasibility, approximation and optimality bounds

The saved source certificate establishes an all-time normalized margin of at least 0.0397 for the exact-decimal synthetic witness and its original constraints. It does not include Hong Kong obstacles. The surviving necessary upper bound for the same nominal finite trajectory family is 0.1559772. Consequently,

\[
0.0397\le\eta^*<0.1559772,
\qquad 0\le\eta^*-\eta_{\rm witness}<0.1162772.
\]

This is an objective-score gap, not metres, seconds, probability or a close-optimality claim. The earlier 0.03972 bound is invalidated. Neither bound supplies a historical feasibility certificate. A restricted feasible set may inherit a valid upper bound only if all other model assumptions remain unchanged; the synthetic witness lower bound cannot transfer without clearance verification.

The fixed coefficient export is not a fitted approximation across conditions. Its numerical agreement with the original evaluator does not bound physical tracking, model discrepancy, historical geometry error or condition-to-policy approximation error. Those bounds remain unavailable.

## 7. Fresh verification and remaining deliverable

Thirty reference tests pass on the fresh rerun. Fresh formula/outcome evaluation exactly reproduces the stored JSON objects. All nine terrain-handoff artifacts match their sizes and hashes. Verification evidence is in `handoff_reconciliation_verification.json`; interface reconciliation is in `scene_contract.md`.

Requirements: five implemented (FORM-01, OUT-01, UNC-01, VAL-01, DATA-01); five blocked (GEO-01, MAP-01, CERT-01, STAT-01, OUT-02). No scope exclusions or model changes were introduced.

The requested final deliverable still needs registered historical runway/obstacle geometry and defensible heights, whole-aircraft/tracking clearance, a solved condition domain with a published coefficient map, a valid useful optimality-gap bound, and calibrated outcome uncertainty. A terrain-aware solve has not occurred. The package does not prove that landing is impossible; it leaves that question unresolved. No background solver or reconstruction is claimed.

Sources: `../reconstruction/chronology/HANDOFF.json`, `REPORT.md`; `SPEC.md`; `reference_formula.json`, `reference_outcomes.json`; `../analytical/coupled/RESULTS.md`. This report is a faithful presentation of available mathematics and blockers, not completion of OUT-02.
