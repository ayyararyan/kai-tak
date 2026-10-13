# Additive mathematical refinement, unchanged amendment A1

All claims below concern the existing assumed aircraft, scene, force law, ideal contact and original 12-parameter box. The two-second delay, 1.4709975 m/s² deceleration, 150 m reserve, operating margins and hard geometry are unchanged. Parent artifacts are immutable; `parent_snapshot.json` binds them. No new external data are used.

## 1. A sharper globally valid family exclusion

Retain the notation and exact rational height/vertical-velocity bounds in parent DERIVATION §8: flare CG height lies in [6,34] m and |vz|≤22 m/s. Let m be mass, a the fixed braking acceleration, k=1852/3600, e the tested margin,

    v−=k(135+40e), v+=k(175−40e),
    V−=v− exp(6/17000), V+=v+ exp(34/17000),
    Q±=.5×1.225×541.2×v±²,
    L+=mg(1.4−.9e),
    D+=max_{Q∈{Q−,Q+}}(.08Q+.045L+²/Q).

The lower-height assertion follows from gear nonpenetration and |bank|≤25°: 6 cos φ+6.0579|sin φ|≥6 on that interval. The upper height and vertical-speed estimates are family-specific. These premises cannot be transferred to the unrestricted full path class.

### Forward air branch, explicitly justified

Throughout the flare, ydot=0. EAS, height and vertical-speed bounds give

    |va_x|² ≥ V−²−wy²−22² >0.

The fixed gate selects positive va_x. Continuity and the strictly positive squared lower bound prevent a sign change; positive ground speed alone would not justify this. Hence

    u=xdot ≥ u−=wx+sqrt(V−²−wy²−22²)>0.

All reported conditions satisfy both strict radical and ground-speed inequalities.

### Coupled airspeed/ground-speed ratio

For u≥u−,

    (V/u)² ≤ 1−2wx/u+(wx²+wy²+22²)/u².

This function has no interior maximum: if wx≤0 it decreases; if wx>0 its only positive critical point is a minimum. Its supremum is therefore bounded by

    Rv=max(1,sqrt((u−−wx)²+wy²+22²)/u−).

Thus ∫V dt ≤ Rv xD. This replaces the parent bound V+ xD/u−, which ignored the dependence between the speeds.

### Mandatory gate-thrust ramp

The zero-acceleration gate has fixed air angle −3.1° and 153 kt EAS. Therefore

    Qg=.5×1.225×541.2×(153k)²,
    Lg=mg cos(3.1°),
    Tg=−mg sin(3.1°)+.08Qg+.045Lg²/Qg.

The slew limit implies T(t)≥max(700000e,Tg−Kt), K=100000(1−e). Put A=max(0,Tg−700000e). Because u≤wx+V+ and Tf≥4,

    t−=max(4,xD/(wx+V+)),
    z=min(t−,A/K),  J=A z−K z²/2.

J is a lower bound on ∫₀^Tf max(A−Kt,0)dt. Using V≥V−, the excess thrust contributes at least V−J to work.

The air-relative energy identity gives the necessary inequality

    U²−2wx U ≥ R−wx²−C xD+B(xD),
    R=Vgate²+2g×15.24−wy²−.7²,
    C=2 max(0,D+−700000e) Rv/m,
    B(x)=2 V−J(x)/m.

Equivalently U≥max(U0,wx+sqrt(max(0,R−Cx+B(x)))), where U0 is the original family/terminal speed floor. If the radical argument is negative, the zero replacement remains a valid lower bound because the already-proved air branch implies U>wx.

`strong_bound.exclusion` partitions the entire admissible xD interval [200+500e,700−500e]. Outward-rounded interval arithmetic checks

    xD+2U+U²/(2a)−2636(1−e)>0

on all 4096 cells. No scalar optimizer or sampled residual is used as the exclusion certificate. Exclusion at e excludes every larger margin by nesting of the ORIGINAL feasible sets, without needing monotonicity of the algebraic bound itself.

Baseline e=0.181970215 is excluded, with outward lower residual 0.9678323903 m. Calm e=0.095800781 and tailwind5 e=0.060058594 are also excluded. Tailwind5 at e=0 is **not** excluded by this relaxation. The first unresolved cell is evidence of relaxation weakness, not a feasible trajectory and not a proof that stronger bounds cannot work.

## 2. Actual limiting flare active system

Let p=(Tf,xD,U,fx,fz). The baseline approach variables can be held fixed while the flare-only relaxed problem is solved. Six active margins are observed:

1. Stop margin.
2. Absolute thrust-slew margin at the gate.
3. Absolute thrust-slew margin at touchdown.
4. Absolute thrust-slew margin at an interior time sS.
5. Upper-load margin at interior time sL.
6. Lower-thrust margin at interior time sT.

Solve the nine equations g_i(p,s;wx)=η (i=1,…,6), together with ∂s g4=∂s g5=∂s g6=0. All other constants, including wy, are held fixed. The executable `active_branch.py` solves this system, differentiates the resulting Jacobian and reports the numerical multipliers; it does not substitute generic KKT equations for evaluated results.

At wx=−4.876589552990943 m/s, wy=9.64006667211232 m/s:

    η ≈ .152360764301861,
    p ≈ (4.140834462862,302.126459392734,72.512142316831,
         −.054163922082,−.014824733206),
    dη/dwx ≈ −.0180031316887,
    dp/dwx ≈ (−.110664524450,−3.935299293324,1.001891357489,
               .018454391225,−.228425025747).

The active multipliers in the order above are approximately

    (.856064452,.000965821,.004509405,.008791721,.051442623,.078225977).

Their sum is one and all are numerically positive. The augmented active-gradient matrix has minimum numerical singular value .0654992; the nine-equation system condition number is about 56882. This is numerical regularity evidence, **not interval validation of a root or Jacobian nonsingularity**. Centered re-solves at ±.01 m/s agree with dη/dwx within 10⁻⁶. Re-solves on the listed points in [−.1,+.1] m/s relative to baseline retain positive multipliers. A solve at −.2 m/s reaches an equality branch with a negative multiplier; its equality residual alone is not an optimality certificate. No continuous active-regime domain is inferred by interpolating these points.

### Exact local theorem and its unverified premise

If an exact root exists nearby, the active-time extrema remain valid, all omitted constraints are slack, and the active-gradient simplex contains zero in its strict interior, then the finite active constraints give a strict local max-min optimum. Indeed, for every nonzero direction d, at least one active gradient has negative inner product with d. Compactness of the unit sphere gives a uniform first-order decrease, dominating the O(|d|²) remainder. Since full feasibility implies the finite active inequalities, this is a sufficient LOCAL upper-support argument, not merely necessary KKT conditions. The implicit-function derivative is −F_z⁻¹F_wx on a nonsingular branch.

The present root/gradient evaluation is numerical. It does not establish these exact premises by an interval Newton/Krawczyk proof, nor does it prove global flare optimality. It also does not identify a unique full 12-dimensional primary path: the approach can remain slack. These are retained gaps.

## 3. A genuinely condition-dependent, continuously certified feasible domain

Define δ=wx−wx0. Use the real-decimal center q0 from `active_branch.json` and the real-decimal derivatives above for the five flare coordinates; set the other seven derivatives to zero:

    q(δ)=q0+q′δ,  wind(δ)=(wx0+δ,wy0,0).

For each δ the endpoint velocities are recomputed from that wind by the original Hermite construction. This is an explicit parameter-dependent trajectory family, not interpolation of controls. Its approach duration and bump coordinates are fixed but the approach coefficients still respond to the wind-dependent endpoint velocities.

`box_certifier.py` plus `parameter_taylor.py` proves all-time force, whole-body geometry and analytic rollout inequalities for every δ in each CLOSED interval:

| Domain, m/s | Certified operating margin |
|---|---:|
| \|δ\|≤.001 | .149 |
| \|δ\|≤.002 | .147 |
| \|δ\|≤.005 | .14 |

These are feasibility lower bounds for the explicit affine family, not the unknown condition-dependent optimum or a proof of secondary optimality. The widest radius is only about .00972 kt: a small mathematical neighborhood, not operational gust robustness. Each wind is known and constant for the corresponding trajectory; this is not one causal feedback law.

The checker uses first-order interval automatic differentiation in δ and the mean-value enclosure r^(k)(s,δ) ∈ r^(k)(s,0)+[−d,d] ∂δr^(k)(s,[−d,d]), k=0,…,3. Derivatives include duration denominators. Every derivative is enclosed analytically with outward arithmetic; finite differences are only regression diagnostics. Polynomial-time intervals cover both closed flight phases; factored gear contact and exact rollout follow the parent checker. The actual q(δ) correlations are preserved in this mean-value enclosure; any remaining independent interval hulls only enlarge the set. All parameter boxes stay inside the unchanged original bounds.

Initial independent-coefficient interval boxes failed even at small radii because of dependency inflation. The mean-value checker resolves three smaller domains; |δ|≤.01 at margin .13 remains interval-unresolved near flare s≈.91249. Neither failure excludes a physical or mathematical path. No larger domain is claimed.

## 4. Continuous secondary-retention proof

For a fixed local primary path choose any time/constraint, using a dense scan only to choose a tight point. Evaluate that constraint with interval arithmetic. Its upper endpoint, rounded upward, is an upper bound ηP,U on the TRUE continuous minimum of that primary path. Then certify the delivered secondary path at ηP,U−.0001. This proves

    η(primary path)−η(secondary path) ≤ .0001

without treating a sampled minimum as a lower bound. It is a comparison of two delivered local paths, not a comparison to the unknown global primary optimum. All eight original paths pass this stronger check. Their bytes and coefficients are unchanged.

The baseline lower certificate is now .15225866725206007. Combined with §1:

    .15225866725206007 ≤ η*family ≤ .181970215.

Gap .02971154774793993 remains. The full-class terminal bound is unchanged; neither new family bound nor local active-system computation applies as a global full-class optimizer proof.

## 5. Targeted continuation and exact remaining obstruction

Warm-start wind continuation: 2.5,3,3.5,4,4.5,5 kt. Warm-start urban-height continuation: 56,…,65 m, always retaining the exact urban-exit one-sided clearance constraint. Follow with 1201-point target re-solves and 20001-point diagnostics; urban65 also receives a second seed from urban60. Negative-margin points are continuation diagnostics, never accepted landings.

The tailwind5 dense retry has margin about −.01711 and a non-success stopping flag; its mesh margin is about −.01680, exposing additional between-mesh loss. Urban60 converges to about −.06295 with urban-exit clearance .2 m and the original vertical odd-bump upper bound active. Urban65 reaches two poor negative-margin branches, not a global exclusion. The energy relaxation at zero margin cannot exclude tailwind5 and is independent of the urban blanket, so it cannot settle the tall cases.

Optimizing the condition itself at η=0 gives local mesh boundary estimates 3.50319 kt and 58.32087 m. The 20001-point minimum margins are slightly negative (about −8.5×10⁻⁶ and −5.9×10⁻⁶); these values are explicitly NOT certified feasibility thresholds. They localize the loss of this branch, not all branches. Neighboring positive paths at 3 kt and 58 m are instead verified continuously with independent Newton replay and local secondary stages.

Remaining work: rigorous global search/dual enclosure using the actual five-variable flare limits; interval validation of local active roots/regularity and event domains; other-branch existence or sound exclusions for tailwind5/urban60/urban65; global secondary minimization. No mathematical impossibility claim is made.
