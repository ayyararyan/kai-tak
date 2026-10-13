# Finite-roll position matching with fixed boundary speed and descent

2026-10-13. New derivation for a restricted analytical family; no literature-novelty claim. This completes the finite-roll position-matching stage, **not the requested entire analytical landing**. Frozen simulator files are unchanged.

## 1. Exact problem and boundary data

Use the prior runway frame, no wind, initial horizontal position (x0,y0), heading −δ and final (xt,0), heading 0, where 0<δ<π and X=xt−x0. Fix horizontal speed U>0, constant flight-path angle −π/2<γ≤0, gravitational acceleration g>0, bank-rate magnitude p>0, and bank cap 0<bcap<π/2. Both boundary banks are zero. Thus the SAME true airspeed V=U/cosγ and vertical velocity U tanγ are held at both boundaries and throughout every candidate. They are not adjusted to force an endpoint fit. Altitudes h0,ht can additionally be fixed, with H=h0−ht≥0. Times are free unless explicitly prescribed.

The family is: initial straight; bank ramp 0→b at rate p; constant bank b hold; bank ramp b→0 at rate −p; final straight. The peak b is the only free turn parameter; each candidate uses maximum-magnitude roll on both ramps. Nonnegative, including zero, straight and hold durations are allowed. No extra winding, opposite bank or multiple turns. No roll-acceleration bound is imposed; bank rate jumps at phase boundaries, while bank and acceleration remain continuous. Sufficient lift/thrust are assumptions, not verified aircraft capabilities.

Coordinated constant-γ force balance gives Lift cosφ=mg cosγ and

    ψdot = k tanφ,    k=g cosγ/U=g/V.

This descending coefficient is essential. In particular, a circular hold has horizontal radius U/(k tan b)=U²/(g cosγ tan b), not the level-flight radius unless γ=0. Lift/(mg)=cosγ/cosφ and Thrust=Drag+mg sinγ. Density-dependent CL, thrust/slew, stall/load constraints and force commands at the fixed boundary states still need separate verification; bank feasibility alone does not establish these.

## 2. Elementary heading/time and exact displacement

Let a=k/p and q(b)=a log(sec b). Each ramp changes heading by q. The hold rate is ω=k tan b; hold duration τ=(δ−2q)/ω, ramp duration r=b/p. Nonnegative hold requires

    0<b≤bmax=min{bcap, acos(exp(−δ/(2a)))}.

The second upper bound is the triangular-bank endpoint (τ=0). Total turn time is Tturn=2r+τ. On entry ψ(t)=−δ+a log(sec(pt)); on the hold ψ=−δ+q+ω(t−r). On the exit, symmetry gives ψ(Tturn−t)=−δ−ψ(t). These formulas are elementary.

For complex horizontal displacement Z=Δx+iΔy define

    I(b)=(1/p)∫[0,b] exp(i a log(sec z)) dz.
    Z=U{exp(−iδ)I + conjugate(I)
        + [exp(−iq)−exp(i(−δ+q))]/(iω)}.

This is exact quadrature, not an elementary position formula. The hold quotient is interpreted continuously at τ=0. A special-function representation is

    I(b)=(1/(2p)) B_{sin²b}(1/2,(1−ia)/2),

where the incomplete beta function is defined by its integral on real 0≤sin²b<1 using real logarithms of positive bases. This specifies the complex branch, rather than relying on a library's undocumented convention. It follows directly by u=sin²z; no external theorem is needed. For an intermediate entry-ramp point replace b by pt; the hold is an elementary circular increment and the exit follows by reflection. Altitude is h(t)=h0+U tanγ·t, including straights. This supplies the complete path in the family, not only endpoint equations.

Reflection symmetry forces

    Z=exp(−iδ/2)W(b),
    W=2U Re[exp(−iδ/2)I]
      +2U sin((δ−2q)/2)/ω >0.

Thus only the scalar chord length W needs a non-elementary evaluation. Exact horizontal matching gives

    s(b)=y0/sinδ−W/(2cos(δ/2)),
    ell(b)=X−y0 cotδ−W/(2cos(δ/2)),
    D(b)=s+ell+U Tturn=C+U Tturn−W/cos(δ/2),
    C=X+y0 tan(δ/2),    Ttotal=D/U.

These equations solve both position constraints without changing speed, heading, bank or γ at either endpoint. They do not automatically solve altitude.

## 3. Monotone feasible interval and family-optimality theorem

Use the heading progress α=ψ+δ∈[0,δ]. On entry/exit the bank is determined by roll and heading; across the entire symmetric turn,

    φ_b(α)=min{b, acos(exp(−min(α,δ−α)/a))},
    dt/dα=1/[k tan φ_b(α)].

The endpoint singularities scale as α^(−1/2), hence the integrals below are proper improper integrals with finite values. Increasing b weakly increases φ_b everywhere, strictly on a positive-measure central interval for b<bmax (unless comparing identical peaks). Because cos(α−δ/2)>0 for δ<π,

    W(b)=U∫[0,δ] cos(α−δ/2)/[k tanφ_b(α)] dα

is continuous and strictly decreasing on (0,bmax], diverging to +∞ as b→0. Define

    Wlim=2cos(δ/2) min{y0/sinδ, X−y0 cotδ}.

**Feasibility theorem.** The geometric family is empty if Wlim<W(bmax); otherwise there is exactly one bgeo∈(0,bmax] satisfying W(bgeo)=Wlim, and the feasible peak-bank set is [bgeo,bmax]. Equality yields a singleton; at bgeo at least one straight has zero length. Negative Wlim is automatically infeasible. This is a family exclusion, not an all-path exclusion. With strictly positive straights the endpoint may be excluded and the optimum becomes only an infimum.

**Optimality theorem, altitude free.** The matched total length has heading-domain representation

    D(b)=C+U∫[0,δ] {1−cos(α−δ/2)/cos(δ/2)}
                         /[k tanφ_b(α)] dα.

The brace is negative in the interior and zero at the endpoints. Its magnitude is integrable there. Increasing b reduces the positive denominator reciprocal, so D(b) is continuous and strictly INCREASING on the same interval. Therefore bgeo uniquely and simultaneously minimizes peak bank, matched total horizontal length, and total time in this family. This is not the heading-only minimum-time result: the latter fixes no position and favors large bank, whereas here the straights change to preserve endpoints.

The theorem is analytical and global within the stated family. Evaluating bgeo usually requires a scalar monotone root of a special-function/quadrature expression. The numerical root in the verifier is **implicit/semi-analytical**, not an explicit elementary optimum. A bisection bracket with rigorous quadrature error would permit certification; our floating-point checks are not that certificate. No all-flight candidate classification or full-margin objective proof follows.

## 4. Exact altitude and full-state compatibility

For fixed γ<0 and H, all candidates must satisfy Dreq=H/(−tanγ). On a nonempty horizontal interval the necessary and sufficient kinematic condition is

    D(bgeo)≤Dreq≤D(bmax).

Strict monotonicity then supplies exactly one b satisfying D(b)=Dreq, including the possible endpoint/singleton cases. This is a second monotone scalar root, not freedom to optimize over a continuum of altitude-matched peaks. At γ=0 only H=0 is compatible; with H=0 all horizontal candidates remain. With a fixed total time and γ<0, additionally require Dreq=U Tfixed; at γ=0 impose D(b)=U Tfixed directly without defining H/(−tanγ). Differing initial/final V or γ are incompatible with this constant-V/γ family and must not be quietly overwritten.

An even simpler necessary condition for any constant-γ horizontal curve is

    H/(−tanγ) ≥ sqrt(X²+y0²).

It follows from arclength≥endpoint distance and is independent of the turn construction, roll limit or bank cap.

**Frozen scenario incompatibility.** Its synthetic start (−2500,1000,140) and threshold (0,0,15.24) have H=124.76 m and γ=−3.1°. They require only about 2303.63 m of horizontal arclength, less than endpoint distance 2692.58 m, a 388.96 m deficit. Therefore no constant-γ path can join these states, even before roll constraints. This is a proof of incompatibility of the constant-slope restriction with those endpoints, not proof that the frozen variable-γ landing is impossible. Separately, v1 prescribes 153 kt EAS at different altitudes with altitude-varying density; constant V would produce different EAS (terminal/initial ratio about 1.007366). Exact fixed EAS at both ends is another incompatibility. We do not relabel the benchmark a same-full-state solution to v1.

## 5. Limits, degeneracies and next full-landing obstacle

For p→∞ with a fixed b<bcap, ramps vanish, q→0, Tturn→δ/(k tan b), and Z→R(sinδ+i(cosδ−1)), with R=U/(k tan b). Thus the previous instantaneous-bank geometry is recovered with the correct descending radius. At b=btri the hold vanishes continuously. δ=0 is a separate straight problem; δ=π makes this straight-matching linear system singular and is excluded. Domains must be checked before formulas are evaluated; near-zero δ/b may require asymptotic/numerically stable evaluation. The supplied verifier tests ordinary-domain synthetic values, not arbitrary precision or all extreme parameters.

This stage removes instantaneous bank and includes position, but does not remove constant slope/speed or the prescribed switch pattern. For the actual full boundary data, the next analytical stage must admit variable γ and, to preserve EAS endpoints, compatible variable TAS. That introduces lift/thrust-controlled vertical and speed dynamics, plus phase matching to flare, touchdown and stopping. Adding terrain/wind/actuator constraints and proving optimality for the frozen nominal-margin objective still require an appropriate global argument; merely concatenating exact segments is not such a proof. Nothing here proves that the full solution cannot be analytical.

## 6. Verification and evidence

`verify_finite_roll_position.py` uses complex Simpson quadrature for I and an independent phase-separated RK4 integration of ψdot=k tanφ, xdot=U cosψ, ydot=U sinψ, hdot=U tanγ. It tests constructed positions, reflected displacement, triangular/capped branches, monotonic interval/root claims, exact-altitude recovery at fixed boundary γ/V, the instantaneous-roll limit and the frozen-state endpoint-distance obstruction. It does not invoke or fit the frozen optimizer. Results: `finite_roll_position_results.json`.

Correctness is backed by the proofs and independent synthetic integration; full aircraft force feasibility, historical terrain constraints and full landing optimality are unverified/incomplete. No external messages, flight actions or simulator edits.

Recorded run: 30 constructed synthetic cases and five explicit domain rejections passed. Largest independent ODE turn-position discrepancy was 1.45×10⁻¹⁰ m, heading discrepancy 3.45×10⁻¹⁴ rad. Recovering the bank from fixed altitude had a worst discrepancy of 6.90×10⁻⁸ rad near a flat triangular-boundary root; this is numerical conditioning, not an exact finite-precision certificate. The instantaneous-roll limit error decreased by about tenfold at each tenfold p increase, reaching 2.29×10⁻⁴ m. These are checks of the mathematics/code, not real-aircraft accuracy.

Fresh parent rerun, 13 October 2026 at 11:43 UTC: the old endpoint inversion assertion failed at one triangular case despite zero forward length residual. Exact endpoint equality is now handled before bisection; no tolerance was loosened. All 30 cases and five rejections pass, with maximum recovered-bank discrepancy 4.40×10⁻¹⁴ rad. See CONTINUATION_HANDOFF.md for failure and repair evidence. This improves endpoint handling, not a general interval-certified inverse.
