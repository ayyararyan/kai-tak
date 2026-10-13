# Conditional hybrid problem: explicit formulas and proof domains

This is the downstream derivation authorized by amendmentA1, not the empirically gated historical branch. Read ASSUMPTIONS.md for exactly which airport/aircraft is being solved. All new geometry inequalities are hard constraints; the original max-min normalized operating margin and secondary effort remain unchanged.

## 1. Complete trajectory and reference identities

Let q=(Ta,Tf,xD,U,bx,cx,by,cy,bz,cz,fx,fz), with the inherited compact box. The decision reference r is virtual,6m vertically below actualCG; rC=r+(0,0,6), so their velocities and accelerations coincide. Body points instead have positions rC+R(t)b. This does NOT identify r as a material wheel path during bank. Force inversion uses CG altitude for density.

For normalizeds∈[0,1], durationT, endpoint positionp0,p1, velocityv0,v1 and zero accelerations, define

 c0=p0, c1=Tv0, c2=0,
 A=p1−c0−c1, B=Tv1−c1,
 c3=10A−4B, c4=−15A+7B, c5=6A−3B.

The base curve is Σc_ks^k. Let b(s)=64s³(1−s)³ and o(s)=(2s−1)b(s). Add (bx b+cx o,by b+cy o,bz b+cz o) to approach and(fx b,0,fz b) to flare. These additions and their first two derivatives vanish at both ends. Hence position, velocity and acceleration join exactly at the threshold; jerk/control-rate limits must be checked separately on BOTH sides.

CG endpoints are(−2500,1000,146)→(0,0,21.24)→(xD,0,6). Landing velocity is(U,0,−σ),σ=.7m/s. For fixed EAS153kt, airpathangleγ=−3.1°, horizontal ground-track directiond and constant horizontalwindw,

 V=153k exp(zCG/17000),
 G=w·d+sqrt[(Vcosγ)²−|w|²+(w·d)²],
 v_ground=(Gd_x,Gd_y,Vsinγ), k=1852/3600.

Choose the positive radicand/forward-ground-speed branch. Entrytrack−47° and gatetrack0° are fixed assumptions, not inferred historical starting states. Different wind inputs generate different paths; this is not causal gust feedback.

For any suppliedq, these are explicit polynomial trajectories. q itself is found numerically in the examples. Printing the coefficients does NOT turn them into a closed-form condition-to-optimum solution.

## 2. Controls, objective and whole-body geometry

Put v_a=rdotC−w, V=|v_a|, e_t=v_a/V, e_r=(−v_ay,v_ax,0)/H and e_u=e_t×e_r. F=m(rddotC+ge_z); lu=F·e_u,lr=F·e_r. Then

 L=sqrt(lu²+lr²), φ=atan2(lr,lu), CL=L/(.5ρV²S),
 D=.5ρV²S(.08+.045CL²), T=F·e_t+D.

Analytic time derivatives give φdot=(lu lrdot−lr ludot)/L² and Tdot. The implementation differentiates the moving basis, not just F. This is the preserved reduced force model, not identified aircraft6DoF.

The objective is η(q)=min over all original normalized operating inequalities and phase times, including stopping, followed by minimum E=∫[(φ/25°)²+(φdot/5°s⁻¹)²+(Tdot/100000)²]dt atη≥η*−1e−4. The actual optimizer establishes a local numerical primary benchmark, notη*. Secondary completion is reported relative to that benchmark only.

Assumed bodypitch0, yawgroundtrack and bankφ imply exact lowest nongear height

 zB=zCG−4cosφ−32.7|sinφ|.

The lowest ideal wheelpoint is zG=zCG−6cosφ−6.0579|sinφ|. The whole-aircraft lower support is min(zB,zG). The55mhorizontal bound contains every bodybox corner and ideal gear point at any rotation, since sqrt(40.8²+32.7²+13.8²)<55. Trackingbufferb expands it to55+b.

For an assumed rectangular obstacle[lx,ux]×[ly,uy] with toph, impose

 max(lx−x,x−ux,ly−y,y−uy)−(55+b) ≥0
 OR min(zB,zG)−h−3 ≥0.

Equivalently max(horizontal_gap,vertical_gap)≥0. This is a sufficient whole-body separation test, deliberately more restrictive than exact shape collision. It is an exact definition of OUR conservative feasible set; failing it is not proof that the real shapes collide. Geometry never entersη with an arbitrary scale. The upstream urban halfplane has horizontal_gap=x−(55+b)+600; near-threshold side rectangles use the same disjunction. Flatground imposeszB≥.5,zG≥0; intended wheel/runway contact is permitted.

## 3. Contact and exact ground regimes

At touchdown the model resets vertical velocity tozero and bank/angular motion tolevel stationary pose via ideal contact. This deliberately idealizes impact/suspension; vertical impulse mσ and vertical kinetic-energy lossmσ²/2 are the translational reset, not verified gear loads. No engine/wing contact is allowed. Straight-ground tracking and lateral tyre authority are assumed.

Withτ=2,a=1.4709975, touchdown timetD=Ta+Tf andu=t−tD:

 0≤u≤τ: x=xD+Uu, vx=U;
 τ≤u≤τ+U/a: x=xD+Uτ+U(u−τ)−a(u−τ)²/2, vx=U−a(u−τ);
 u≥τ+U/a: x=xstop=xD+Uτ+U²/(2a),vx=0.

CGheight6 andy0 throughout rollout. The exact available-speed condition for a specifiedxD and required primarymarginη is

 U ≤ −aτ+sqrt[a²τ²+2a(2636(1−η)−xD)],

provided2636(1−η)−xD≥0 andU≥0. Otherwise no nonnegative speed satisfies the reserve condition. These are explicit stop regimes, not an optimized airborne policy. Rollout geometry is checked over the entire position interval[xD,xstop], not sampled only at endpoints.

## 4. Wind-dependent GLOBAL terminal relaxation and algebraic regimes

At touchdownEAS≥135+40ηkt. LetK=k exp(6/17000), c=w_y²+σ² and

 D(η)=[K(135+40η)]²−c,
 Umin(η)=w_x+sqrt[D(η)].

On the specifiedpositiveair-forwardbranch andD>0,Umin>0, any feasible full trajectory obeysU≥Umin,xD≥200+500η. Therefore

 F(η)=200+500η+τUmin+Umin²/(2a)−2636(1−η) ≤0.

F′=3136+(τ+Umin/a)Umin′>0. Also the fixed153ktentry givesη≤.45. Thus:

* F(0)>0: no nonnegative-margin landing in this terminal relaxation (hence none in the model on this branch).
* F(.45)≤0: the terminal relaxation upper value is.45.
* Otherwise the UNIQUE rootηT∈(0,.45) is the terminal upper value.

This is sufficient AND necessary for the RELAXED terminal subproblem, whose omitted constraints are the entire airborne dynamics, obstacles and additional contact/control conditions. ChoosingxD=200+500ηT,U=Umin(ηT) attains the relaxed objective; this does not construct a full landing. Scope matters: its sufficiency is not transferred to the full hybrid problem.

For a direct algebraic representation, let

 Q(η)=200−2636+3136η+τw_x+w_x²/(2a)+D(η)/(2a), B=τ+w_x/a.

The root satisfiesQ+B√D=0, hence thequarticQ²−B²D=0. Retain only real roots satisfyingD>0,Umin>0,the original unsquared equation and the interval[0,.45]. B can be NEGATIVE for headwind; assumingB>0 would select wrong roots. B=0 reduces directly toQ=0. This quartic-root specification is an algebraic closed representation of the terminal optimum; the evaluator uses stable scalarroot solving plus separate outward-interval rational brackets instead of unstable radical formulas.

The inherited finitefamily also hasU≥69. Its stronger relaxation replacesUminbymax(69,Umin). In the69-binding regime,

 η69=[2636−200−2×69−69²/(2a)]/3136
     =66656817/307536544≈.21674437819.

The regime-switchcondition isD(η)=(69−w_x)² with69−w_x≥0. If69binds at the optimum,η69 is an EXACT global value for that terminal-family relaxation; otherwise use the quarticroot. Both are upperbounds on the corresponding full problem. The code returns sign-certified rational brackets; its lower root-bracket endpoint is NOT a feasible-trajectory lowerbound.

A certified whole-path candidate ofmarginηL and terminalupperηU givesηL≤η*≤ηU. Report the gap, not “near-optimal” without a justified tolerance. Removing hard geometry cannot invalidate an upperbound; adding it may lower the optimum.

## 5. Fixed-boundary obstruction and geometry regimes

At the threshold theposition, velocity andzeroacceleration are fixed, so thebank iszero forhorizontalwind. Evaluate each geometry predicate there before optimizing. Anynegativehardpredicate excludes EVERY path in the imposed conservative model, independent of numerical solver behavior. For the tested(+80m,−50m)frame shift, the assumedurban-side constraint at the fixedgate is−10m. This is a full-model conditional exclusion, not a statement about KaiTak's actual feasibility.

Along a supplied path, switches between lateral passage and overflight occur where horizontal_gap=vertical_gap; contactwithanobstacleboundary occurs when the active gap iszero. Bankedsupport switches atφ=0 and at4cosφ+32.7|sinφ|=6cosφ+6.0579|sinφ|. These are explicit clearance regimes. Their intersection with optimalcontrolactive sets is the still-required optimal-path regime map.

## 6. Full optimum: what has actually been proved and attempted

For the fixed finitepolynomialfamily, feasibleq lie in a compact box. A positive-margin candidate supplies nonemptiness. EAS≥135 and a polynomial derivativebound|vz|<69m/s giveH>0; load≥.5g givesL>0; bank≤25° giveslu>0. Thus force/rate maps are continuous on the feasible set. Infinite-time inequalities are closed; maxima/minima ofcontinuous functions overcompacttime arecontinuous. The primarymaximum is attained, and the secondaryeffort minimum is attained onη≥η*−1e−4. The executable regularity calculation provides a conservative verticalspeedbound using exact rational Bernstein bounds. This is an EXISTENCE proof for the12dimensionalfamily, not identification or uniqueness of its optimizer or unrestricted-class attainment.

New multistart searches, dense repair, secondarysearch, intervalfeasibility and independent forwardintegration are performed across conditions. Numericalagreement acrossstarts is evidence about local search, not global sufficiency. Geometry can materiallyreduce the achievedmargin; it is not a cosmetic overlay.

For a smoothactive-setbranch with active constraintsc_i(q,t_i;θ)=η and hardh_j=0, interior active times satisfy∂tc_i=0. Local stationarity hasΣλ_i=1 andΣλ_i∇qc_i+Σμ_j∇qh_j=0 (plusboundnormals), λ,μ≥0. Under nonsingular active-systemJacobian, the implicitfunctiontheorem givesbranchderivative dz/dθ=−F_z⁻¹F_θ. Negative-definiteness of the reducedLagrangianHessian is a local sufficiency test only. At inactiveconstraintentry, zero multipliers, degenerate extrema, bank-support/disjunctionswitches or singularJacobian, that branch must be replaced. These transcendental/implicit branch systems have NOT been solved into a full parameter-domain partition; the report does not label them the final closedform.

The global upperbound remains separated from the best certified candidate. No matchingdual/globalexclusion proof, full secondary global minimizer, universal condition-to-optimum formula, causal gustpolicy, go-aroundviability or physical predictioninterval is established. These are MATHEMATICAL/model deliverable gaps, not a renewed request for data or authorization. No theorem of nonexistence of closedforms is claimed.

## 7. Continuous verification is a proof of feasibility only

Exact real-decimal decisionvalues and declared windvectors define the formulas. Outward-rounded intervalforce/geometry checks cover both closed phases. For flaregearcontact, factoringzCG−6=(1−s)h(s) andax=(1−s)ãx(s) avoids uncertain cancellation at touchdown. Sinceay=0,

 |sinφ|/(1−s)=m|w_y ãx|/(HL).

The sufficient inequalityh≥6.0579m|w_y ãx|/(HL), togetherwith6(1−cosφ)≥0, provesgear nonpenetration includingtheendpoint. Flatrolloutcontact is a structural equality; entire-segment obstacles useintervalenclosure. Force certificates are new percondition, never copied from the frozen meanwindrun.

## 8. Stronger finite-family global bound from flare energy (new)

The terminal-only relaxation ignores the work needed to decelerate through flare. We can add a rigorous necessary energy inequality without solving the path. This bound applies to the inherited polynomial family, not an arbitrary unrestricted flare.

The exact rational derivative calculation bounds flare |vz| by21.4311m/s; use the looser22m/s. Its height has the Hermite form z0+(z1−z0)H+T v0 A+T v1 B+fz b. On[0,1],0≤H≤1,A≥0,−.2≤B≤0,0≤b≤1, v0<0,v1=−.7,T≤12,fz≤10. HencezCG≤21.24+12×.7×.2+10=32.92<34m. Gear nonpenetration and|φ|≤25° implyzCG≥6 because6cosφ+6.0579|sinφ|≥6.

At any fixedη define

 v−=k(135+40η), v+=k(175−40η),
 Q−=.5ρ0S v−², Q+=.5ρ0S v+²,
 L+=mg(1.4−.9η),
 D+=max over Q∈{Q−,Q+} [.08Q+.045L+²/Q].

This is an upper drag bound: Q=.5ρ0S EAS² exactly; drag increases withL² and is convex inQ, so its maximum over the interval is at an endpoint. Ignoring the simultaneousCLcap only makes the bound conservative.

In the flare y=0. For the tested modest horizontal winds and the forward branch,

 u−=w_x+sqrt[(v−exp(6/17000))²−w_y²−22²]>0,
 V+=v+exp(34/17000),
 Tf≤xD/u−,    ∫Vdt≤V+ xD/u−.

Air-relative energy obeys d(V²/2+gz)/dt=(T−D)V/m becausewind is constant and verticalwindzero. SinceT≥700000η andD≤D+,

 V_D² ≥ V_gate²+2g×15.24−C(η)xD,
 C(η)=2 max(0,D+−700000η) V+/(m u−).

LetR=V_gate²+2g×15.24−w_y²−.7² andU0=max(69,Umin). Then ANY feasible finite-family landing satisfies

 U≥max[U0,w_x+sqrt(max(0,R−CxD))].

Thus minimize the exact relaxed stopping expressionS(x)=x+2U(x)+U(x)²/(2a) overx∈[200+500η,700−500η]. Its global scalar minimum requires only a finite explicit candidate set:

1. Both interval endpoints.
2. The speed-floor switchx=(R−(U0−w_x)²)/C ifC>0 and the point lies inside.
3. On the energy branch, the stationary point withr=sqrt(R−Cx)=BC/(2−C/a),B=2+w_x/a, ifr>0, the denominator is nonzero, x=(R−r²)/C lies inside, andw_x+r≥U0.

These candidates exhaust the smooth branches and their nonsmooth join. C=0 gives the constant-speed-floor case directly. The equation minS(x)=2636(1−η) is a one-dimensional implicit boundary, not a full-flight closed-form optimizer. Code solves it only to propose an upper value. A SEPARATE outward-rounded interval partition of the ENTIRE admissiblex interval proves minS(x)>2636(1−η) at the reported real-decimal upperη. Since all original constraints are nested inη, exclusion there excludes every largerη. The interval proof, not a scalar optimizer flag or rounded root, validates the global family upperbound.

This strengthens the candidate/global comparison while preserving scope: it is a sufficient global EXCLUSION certificate for the specified family, not sufficient construction of an optimum. It cannot certify the unrestricted class, where the polynomial height/vertical-speed bounds are unavailable. The terminal bound remains the reported full-class bound.
