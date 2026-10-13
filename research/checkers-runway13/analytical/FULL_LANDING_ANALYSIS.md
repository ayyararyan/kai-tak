# Full-landing analytical attempt: explicit trajectories, exact rates and a global bound

2026-10-13. Scope: preserve numerical specification v1, not replace its nominal-margin objective with minimum bank/time. **The full optimal landing has not been solved.** What is obtained here is an explicit parameterized approach–flare–stop family, exact inverse controls/rates, and a proved nonattainment-neutral upper bound on its primary objective. A formula for a path at chosen parameters is not a formula for optimal parameters. No simulator source or configuration is modified; no new local optimizer is run.

## 1. Three distinct mathematical objects

1. **Existing executable:** 12 bounded parameters q, fixed polynomial family, finite evaluation grid, phasewise cubic-spline estimates of bank/thrust derivatives, nearest distance to a fixed sampled reference point cloud, and local SLSQP. This is precisely what its recorded output measures.
2. **Continuous counterpart of that family:** retain the same parameters, endpoint equalities, density, force model, reference point cloud, margin definitions and ground rule, but require inequalities at every phase time and evaluate exact one-sided derivatives. This is the natural analytic object, not a claim that the finite code already implements it. Spline-rate errors mean even a simple ordering of the two reported eta values is not guaranteed without extra error bounds.
3. **Unrestricted control problem:** keep physical endpoints, aircraft model, margins, wind, corridor and phase/reset rules, while removing the polynomial ansatz. Its feasible set is larger if all other conditions coincide. Parameter-box bounds on bump coefficients have no physical all-path meaning; phase-duration and touchdown-speed bounds must be separately retained if claiming comparison with that domain. No theorem that its optimum lies in the polynomial family is available.

Historical calibration/terrain/information uncertainty remain unresolved, independently of these distinctions. This analysis is nominal zero wind where stated, matching the authoritative scenario; it is not a historical or robust-policy solution.

## 2. Explicit full airborne path preserving boundary EAS and gamma

Let κ=1852/3600 m/s per knot, ρ(h)=ρ0 exp(−h/Hρ). For endpoint EAS E, air-relative elevation γ, prescribed horizontal ground direction d=(cosχ,sinχ), and constant wind w, set

    V=κ E exp(h/(2Hρ)),
    u=w_h·d + sqrt((V cosγ)²−|w_h|²+(w_h·d)²),
    v_ground=(u d, V sinγ+w_z).

The square-root argument and u must be positive. This is the exact `endpoint_velocity` branch. It preserves both initial/threshold EAS=153 kt despite different altitude; it does not impose constant TAS or constant descent through the segment.

For a phase duration T and normalized time s=t/T, let endpoints be p0,p1, velocities v0,v1 and accelerations a0,a1. Define

    c0=p0, c1=T v0, c2=T² a0/2,
    A=p1−c0−c1−c2, B=T v1−c1−2c2, C=T² a1−2c2,
    c3=10A−4B+C/2,
    c4=−15A+7B−C,
    c5=6A−3B+C/2,
    P(s)=Σ[j=0..5] c_j s^j.

Direct differentiation proves P(0)=p0, P(1)=p1, P′(0)/T=v0, P′(1)/T=v1 and P″(0)/T²=a0, P″(1)/T²=a1. No matrix inversion or ODE solve is needed. With B0(s)=64s³(1−s)³ and B1(s)=(2s−1)B0(s), both bumps and their first two derivatives vanish at each endpoint.

Write q=(Ta,Tf,xTD,uTD,a_x,b_x,a_y,b_y,a_z,b_z,f_x,f_z). Approach:

    rA(s)=P(start,gate,v0,vg,0,0,Ta)+Σ_j e_j[a_j B0(s)+b_j B1(s)].

Flare:

    rF(s)=P(gate,(xTD,0,0),vg,(uTD,0,−0.7),0,0,Tf)
           +e_x f_x B0(s)+e_z f_z B0(s).

These are exactly the existing degree≤7/6 curves, not a newly relaxed family. q bounds are the source's Ta∈[30,55], Tf∈[4,12], xTD∈[200,700], uTD∈[69,88], approach x/y even/odd amplitudes ±400 m, approach z amplitudes ±50 m, flare x±50 m and z±10 m. At the threshold positions, velocities and accelerations agree (C²), but jerk and control derivatives can differ; both one-sided rate limits must hold.

## 3. Exact inverse forces and rates from position derivatives

Set v=r′, a=r″, j=r‴, v_air=v−w, V=|v_air|>0, e_t=v_air/V, ψ=atan2(v_air,y,v_air,x), γ=atan2(v_air,z,|v_air,h|). Use e_r=(−sinψ,cosψ,0), e_u=e_t×e_r, F=m(a+g e_z). Then

    Lu=F·e_u, Lr=F·e_r, L=sqrt(Lu²+Lr²), φ=atan2(Lr,Lu),
    Q=ρ V² S/2, CL=L/Q,
    Drag=Q(CD0+kD CL²), Thrust=Drag+F·e_t.

These exactly reconstruct the reduced Newton acceleration on the positive-lift branch. The following derivatives avoid the implementation's spline approximation:

    Vdot=e_t·a, e_tdot=(a−e_t Vdot)/V,
    ψdot=(v_air,x a_y−v_air,y a_x)/|v_air,h|²,
    e_rdot=−ψdot(cosψ,sinψ,0),
    e_udot=e_tdot×e_r+e_t×e_rdot, Fdot=m j,
    Ludot=Fdot·e_u+F·e_udot, Lrdot=Fdot·e_r+F·e_rdot,
    φdot=(Lu Lrdot−Lr Ludot)/L²,
    Ldot=(Lu Ludot+Lr Lrdot)/L,
    Qdot=Q(−v_z/Hρ+2Vdot/V), CLdot=Ldot/Q−CL Qdot/Q,
    Dragdot=Qdot(CD0+kD CL²)+2Q kD CL CLdot,
    Thrustdot=Dragdot+Fdot·e_t+F·e_tdot.

Domains additionally require nonzero horizontal airspeed and L>0; at admissible positive load and modest bank these hold, but they must not be assumed for arbitrary q. Evaluate each phase separately at the join. Exact rates and elementary density/angle expressions make trajectory evaluation analytical; maximizing its worst margin is still an unsolved optimization.

## 4. Exact hybrid ground phase

At touchdown retain horizontal u=uTD and impose the model's inelastic vertical reset v_z:−0.7→0. This is a stipulated hybrid contact, not a derived landing-gear dynamics result. With delay τ=2 s and fixed braking aB=0.15g, for ground time z≥0:

    0≤z≤τ: x=xTD+uz, v=u;
    τ≤z≤τ+u/aB: x=xTD+uτ+u(z−τ)−aB(z−τ)²/2,
                            v=u−aB(z−τ);
    xstop=xTD+uτ+u²/(2aB), tstop=Ta+Tf+τ+u/aB.

There is no braking optimization. The ground obstacle rule checks the complete straight interval [xTD,xstop] exactly. Airborne aerodynamics are not applied to the stopped ground state.

## 5. Full objective with continuous quantifiers

Let m_i(q,s) be every original normalized airborne margin at its applicable phase, and m^T_j(q) the touchdown/stop margins. For any band [lo,hi], margins are (z−lo)/(hi−lo) and (hi−z)/(hi−lo). Preserve bands for EAS, CL, load and thrust; bank/roll/thrust-slew use 1−|value|/limit; descent uses 1+γ/γlimit; approach sink uses 1+v_z/8 only on approach; corridor uses 1−distance/400. The corridor is distance to the implementation's fixed 2001 reference samples (1001 per phase, shared gate), not an unannounced replacement by continuous-curve distance. Obstacle margin is max(radial clearance, vertical clearance)/400, including the exact ground check. Touchdown x/sink use both bands; lateral/track/bank use one-minus-normalized-absolute-error. Stop margin is (2636−xstop)/2636.

The continuous-family primary problem is

    eta* = sup {eta: q in Q, m_i(q,s)≥eta for EVERY applicable s∈[0,1],
                        all m^T_j(q)≥eta,
                        h(q,s)≥0, v_x(q,s)≥0, cosφ(q,s)≥0 for EVERY s}.

Both one-sided phase-join rates enter. The implementation accepts nonnegative versions of its hard-only “positive” constraints; this analysis does not strengthen them silently. Singular inverse-dynamics states are excluded from the domain.

Secondary minimization is the original integral of squared normalized bank, roll rate and thrust slew, subject to retaining primary eta within 1e−4. The code reserves 5e−5 on its solver mesh. Exact-rate/integral versions must be distinguished from spline rates and trapezoidal sums; a code result is not a continuous-time certificate.

## 6. New necessary global objective upper bound

Any feasible nominal zero-wind landing in this family with eta≥0 must satisfy touchdown x lower margin, touchdown EAS lower margin, and stop margin simultaneously. Since touchdown height=0, density=ρ0, lateral speed=0 and sink σ=0.7,

    xTD ≥ 200+500 eta,
    u ≥ vmin(eta)=sqrt([κ(135+40 eta)]²−σ²),
    xTD+2u+u²/(2aB) ≤ 2636(1−eta).

The q-bound u≥69 can also be retained via max(69,vmin); vmin>69 for eta≥0 here. Therefore

    F(eta)=200+500eta+2vmin(eta)+vmin(eta)²/(2aB)
                         −2636(1−eta) ≤0.

F is strictly increasing for eta≥0: vmin′>0 and every nonconstant term in F has positive derivative. F(0)<0 and F(0.45)>0. Its unique root etaUB gives a global upper bound for both sampled and continuous polynomial-family objectives, without solving any local optimizer. It also applies to a broader flight class ONLY if the same exact touchdown velocity/reset and margin conventions remain. Different lateral velocity or allowed touchdown sink would change this bound.

Numerically etaUB≈**0.157694902550945**, with vmin≈72.69164034 m/s. The verifier brackets the root using exact rational arithmetic plus integer-square-root enclosures; this bound is not based on a sampled flight or unvalidated floating root. Attainment has not been established: achieving it would require simultaneous touchdown x/EAS/stop saturation and all other margins no smaller, which has not been constructed.

An elementary conservative bound is also available: since sqrt(A²−σ²)≥A−σ for A≥σ, replace vmin by κ(135+40eta)−σ. The resulting necessary inequality is an increasing quadratic in eta; its positive root is an explicit, weaker upper bound. This does not change the objective or claim the relaxation's minimizer is feasible.

In detail let a=40κ, b=135κ−σ and define c2=a²/(2aB), c1=500+2636+2a+ab/aB, c0=200+2b+b²/(2aB)−2636. The explicit upper bound is (−c1+sqrt(c1²−4c2c0))/(2c2)≈0.166213164111. It is weaker than the exact-sqrt bound, but genuinely requires only elementary evaluation.

Other bounds include eta≤1/2 from any two-sided band, eta≤0.45 from fixed EAS153 in [135,175], eta≤0.466666… from fixed touchdown sink0.7 in [0,1.5], and eta≤1−3.1/6 from fixed boundary gamma. Fixed endpoint accelerations also fix load/CL/thrust values and yield endpoint upper bounds, computed by the verifier. None is presented as an attained optimum.

The authoritative candidate's sampled eta is 0.0388964287344991. Difference from etaUB is about **0.1187984738**. This is an upper-bound-to-sampled-value diagnostic, NOT a certified continuous optimality gap: the candidate has no all-time feasibility/lower-bound certificate. Its saved status and replay remain valid at their stated sampled evidence level.

## 7. Attempted global sufficiency: what remains unsolved

For the finite family, one sufficient route is a matching feasible construction and global dual majorant. If nonnegative weights/measures λ over original margins have total mass one, then every feasible eta satisfies eta≤Σ∫m_i(q,s)dλ_i(s), including discrete terminal masses. Proving this weighted expression≤U for all admissible q gives an upper certificate. If a continuously feasible q* reaches eta=U, global primary optimality follows. The coupled stop/EAS inequality above supplies a useful global exclusion but no matching q*. A first-order KKT multiplier fit or local Hessian would not prove the required global inequality. Exact secondary optimality additionally needs its own certificate under the retained-primary constraint.

For the unrestricted problem, fix a trial eta and use state (r,v,φ,Thrust), with controls (φdot,Thrustdot,CL), constant-wind Newton dynamics and every tightened margin as an admissibility constraint. The approach/flare modes differ in applicable sink restrictions, and threshold/contact/stop are guards/resets. A backward reachability/value function with appropriate state constraints and hybrid boundary conditions could give a sufficient verification theorem: membership must include the fixed initial state, exact threshold equalities and final stop set, not merely endpoint position. No such value function or verified global solution is obtained here. PMP supplies necessary candidate equations only; no exhaustive switching family has been established for terrain, slew constraints and phase changes.

The unsolved core is explicitly the maximization over q with all-time constraints (and its unrestricted counterpart), not evaluation of the paths or controls. Finite q does not make the problem a linear program: time scaling, normalized force ratios, exponentials, inverse trigonometric functions, nearest-point/obstacle branches and continuum minima remain coupled and nonconvex. This is an obstacle to the current derivation, **not an impossibility theorem** for analytical solution.

## 8. Verification and completion status

`verify_full_landing_analysis.py` verifies the Hermite coefficient inverse with exact rational matrix multiplication; checks explicit curves against the unchanged implementation across synthetic q and the saved candidate; verifies endpoint EAS/gamma, Newton reconstruction and exact analytic rate formulas against centered finite differences at interior points; brackets the global upper bound with exact rational arithmetic; compares the saved stop formula and reports sampled exact-rate diagnostics separately from spline-rate diagnostics. It reads authoritative artifacts and source hashes; no solve is called.

Run using the existing environment from workspace root:

    research/checkers-runway13/.venv/bin/python research/checkers-runway13/analytical/verify_full_landing_analysis.py

Results in `full_landing_analysis_results.json`, verified 2026-10-13T11:31:19Z: exact rational Hermite identity passed; 41 parameter vectors matched source curves (maximum coefficient discrepancy 5.83×10⁻¹¹); 50 interior derivative checks had maximum roll discrepancy 7.97×10⁻¹² rad/s and thrust-slew discrepancy 4.44×10⁻⁴ N/s. Newton reconstruction residual was below 7.68×10⁻¹⁵ m/s². These floating discrepancies are identity checks, not aircraft accuracy. On the 1201-point/phase grid with both sides of the join retained, exact-rate eta was 0.0388964287293, close to but distinct from the saved spline-rate eta.

The certified root bracket is

    3636196886357314389 / 23058430092136939520 < etaUB
      < 1818098443178657199 / 11529215046068469760.

Its exact width is 9/23058430092136939520 (about 3.90×10⁻¹⁹). The JSON's binary-float decimal approximations can display the same number for both ends; the rational endpoints and exact signed enclosures are the certificate. Source SHA-256 matches the authoritative saved artifact and is unchanged after verification.

Precision domain: this rational bracket certifies the real-number model with exact nominal decimal constants, not every rounding operation of the floating-point executable. Treating its binary unit/braking/sink constants as exact instead moves the root by roughly 7.72×10⁻¹⁷. The substantive upper bound is unchanged at the displayed practical precision, but the narrow rational bracket must not be called a machine-execution enclosure. The verifier now rejects changed nominal bound assumptions (including nonzero wind) before reporting this certificate.

**Achieved:** explicit full path family and inverse derivatives; exact hybrid stopping expression; new rigorous nominal upper bound; independent checks. **Not achieved:** optimal q*(parameters), all-time feasibility certificate for the saved candidate, matching global primary/secondary proof, unrestricted full landing optimum or historical calibration. Overall requested complete analytical optimal landing: **INCOMPLETE**. The constant-slope obstruction is resolved at the parameterization level by retaining v1's variable slope/speed, not by altering its boundary states.
