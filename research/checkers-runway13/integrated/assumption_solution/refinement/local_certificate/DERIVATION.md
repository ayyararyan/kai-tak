# Validated local primary optimum under unchanged A1

## Exact object and constants

This proof concerns the baseline constant real-decimal wind
`(-4.876589552990943, 9.64006667211232, 0)` m/s in the unchanged assumed scene.
All physical, family, endpoint, hard-geometry and rollout constants remain those of
amendment A1. It is not a certificate for a real aircraft or historical terrain.

Let `z=(Tf/5,xD/300,U/75,fx,fz,eta,sS,sL,sT)` and retain the seven approach
coordinates exactly as the real-decimal `baseline.q` entries in the sealed
`../active_branch.json`. The new center and radius below define an exact root
implicitly; rounding that root to a printed vector is not the proof.

The six active margins, in order, are stop, gate slew, touchdown slew, interior
slew at sS, upper load at sL, and lower thrust at sT. Each equals eta. Three more
equations set the normalized-time derivative of each interior margin to zero.
Slew absolute-value signs are rigorously separated: negative at gate and
touchdown, positive at the interior active time. The smooth signed equations
therefore agree with the original absolute-value margins throughout the root box.

## 1. Analytic interval derivatives, not finite differences

`interval_root.py` implements outward interval dual numbers with nine independent
coordinates, nested inside normalized-time Taylor jets of order three. Jet
coefficients are `f^(k)/k!`. Product, reciprocal, square-root and exponential
recurrences follow by equating Taylor coefficients in their defining identities.
For example, `b=sqrt(a)` obeys

    b0=sqrt(a0),
    bn=(an-sum_{k=1}^{n-1} bk*b(n-k))/(2*b0).

Dual differentiation through these recurrences provides the mixed derivatives
needed for the nine-equation Jacobian. Thrust-slew is `T_s/Tf`, interior slew
stationarity uses `T_ss/Tf`, and its margin curvature uses `T_sss/Tf`.
Load and thrust use their corresponding first/second time derivatives. The
physical thrust and load formulas are the unchanged inverse force law. Position,
velocity and acceleration are differentiated Hermite/bump polynomials; centered
polynomial algebra reduces time dependency without approximation or truncation
of the underlying polynomial. Jet order truncates only derivatives not requested.

All constants and box centers enter as real-decimal interval inputs. Computation
uses mpmath outward arithmetic at 50 decimal digits. Floating-point linear algebra
is not part of the proof: a high-precision approximate inverse is rounded to
explicit real-decimal interval entries, and every use is enclosed outward. Numerical
Newton refinement only selects the center. Finite-difference comparisons and the
independent NumPy force evaluator are regression diagnostics only.

## 2. Root existence, uniqueness and Jacobian nonsingularity

The nine center strings in `certificate.json:root.center`, with radius `1e-20`
in every **scaled z coordinate**, define the closed box X. Its eta center is

    0.152360764301861701918625206455836893973748530913.

Let c be the exact decimal center, C the approximate inverse, and J(X) the
interval-AD enclosure of every Jacobian on X. The checked Krawczyk image is

    K(X)=c-C F(c)+(I-C J(X))(X-c).

Every component lies strictly inside X. The infinity-norm bound
`||I-C J(X)||∞ < 1.964e-14 < 1` proves nonsingularity of every enclosed actual
Jacobian (and C). The map `x -> x-C F(x)` maps X strictly into itself and is a
contraction. Thus a unique exact root z* exists in X; this is not merely a small
residual. The maximum absolute Krawczyk offset is below `1.964e-34`, far smaller
than the `1e-20` box radius. The receipt stores the full enclosures; displayed
float values are explanatory only.

## 3. Strict active-gradient simplex

Let G have six rows of gradients of the six active margins with respect to the
five scaled flare coordinates, holding the active times fixed. Form

    A = [G^T; 1^T],       A lambda = (0,0,0,0,0,1)^T.

For every z in X, `||I-C_A A||∞ < 2.484e-14`. Invertibility is therefore proved,
not inferred from a numerical singular value. A Neumann residual enclosure gives

    lambda in lambda_hat + [-epsilon,+epsilon]^6,
    epsilon >= ||C_A (b-A lambda_hat)||∞/(1-||I-C_A A||∞).

Every lower endpoint is strictly positive. Rounded values are

    (0.856064451575378, 0.000965821127795,
     0.004509405115023, 0.008791721036073,
     0.051442623672533, 0.078225977473198).

The smallest weight is greater than 0.0009658211277946. The exact weights sum to
one and G^T lambda=0. A nonsingular augmented matrix and positive weights imply
that zero is in the strict interior of the five-dimensional gradient simplex.

## 4. Checked stationary-time and endpoint extrema

For each interior event the root time is strictly within its closed neighborhood
of radius 0.01 in normalized flare time. Interval third-/second-derivative checks
prove positive margin curvature everywhere in that neighborhood. Safe outward
summary bounds, weaker than the stored enclosures, are:

| Active margin | Curvature lower bound |
|---|---:|
| Interior slew | 13.33 |
| Upper load | 6.58 |
| Lower thrust | 0.869 |

Because its time derivative is exactly zero at the root and its value is eta*,
each margin is at least eta* throughout its entire neighborhood. There is a
unique stationary minimum within each such neighborhood. No assertion that these
are the only stationary points of every margin on [0,1] is needed or made.

On [0,0.01], the gate-slew margin derivative is >3.78; on [0.99,1], the
touchdown-slew margin derivative is <−2.31. Their endpoint values equal eta*,
so those entire neighborhoods also satisfy the margin inequality. Slew signs
are checked across all three slew neighborhoods. Every time boundary in the
force and event check denotes the **same real-decimal number**; event intervals
are rounded outward around those decimal endpoints.

## 5. Omitted constraints and complete hybrid path

The seven fixed approach coordinates plus the five interval-enclosed root
coordinates define the complete two-phase Hermite/bump path. All remain strictly
inside the original parameter box. `validate.full_path` checks the entire
closed approach and flare with 398 accepted time cells (786 processed).

On active neighborhoods only the corresponding already-proved active margin is
removed from ordinary interval comparison. All other operating margins are
strictly greater than the root's eta upper endpoint. Outside those neighborhoods
**all** operating margins are checked. The smallest ordinary-force slack lower
bound is >6.86e-7. The interval proof also checks positive forward speed/lift-up,
whole-body object and urban clearances, non-gear ground clearance, and factored
gear nonpenetration. It reuses the sealed checker at the CG reference with
`parameter_kin=None`; there is no parameter-box interpolation or grid acceptance.

Touchdown distance and sink margins are strictly slack. Lateral position,
track, bank, and endpoint acceleration are structural equalities in the exact
polynomial construction. The stop margin equals eta* by the first root equation;
all other terminal and straight-rollout geometry constraints are checked.
The structural ideal gear contact is handled analytically, not by tolerating
floating-point penetration. The fixed two-second delay, 1.4709975 m/s² braking,
150 m reserve and ideal 0.7 m/s vertical impact reset are unchanged.

At the exact root, rounded values are:

    Tf = 4.140834462861754 s,
    xD = 302.1264593927348 m,
    U  = 72.51214231683128 m/s,
    stop x = 2234.377025300292 m,
    runway remaining = 551.622974699708 m.

The exact definitions are the root box and polynomial formulas, not these
rounded numbers. Independent Newton replay of the rounded numerical center
has position error about 1.14e-11 m and velocity error about 1.73e-12 m/s.
Replay is a consistency diagnostic; the interval certificate establishes the
exact implicit-root path's feasibility.

## 6. What the local theorem now proves

Fix the six active times at their exact root values and write their margins as
smooth functions g_i(p) of the five flare coordinates. For every nonzero d,
some gradient satisfies `grad g_i(p*) dot d < 0`: otherwise positive multipliers
and `G^T lambda=0` force all inner products to vanish, contradicting the rank
proved above. By compactness of the unit sphere there exists c>0 such that

    min_i grad g_i(p*) dot d <= -c ||d||.

Smoothness gives a uniform quadratic remainder. Therefore for all sufficiently
small nonzero h,

    min_i g_i(p*+h) < eta*.

The full all-time margin is bounded above by those six fixed-time values; at p*
it equals eta* by the feasibility proof. Consequently p* is a **strict local
primary max-min optimum of the five-variable flare relaxation**. This is a
sufficient result, not just necessary KKT conditions. No numerical radius for
the neighborhood of this optimality statement is claimed.

The connected complete path is a **local primary optimum of the original
12-parameter family**, generally non-strict: changing only the seven slack
approach coordinates can leave the same optimal flare margin. No unique full
12-dimensional path or full-class local optimum is asserted. The Krawczyk radius
is a root isolation box, NOT an optimality-domain radius or a wind domain.

The existence result strengthens the primary family lower bound to the safe
rational-decimal `0.15236076430186170190`. The existing global family upper bound
remains `0.181970215`. Their gap is still positive. No global optimum follows.

## 7. Secondary retention against the proved local primary

`retention_replay.py` continuously certifies the original, unchanged delivered
baseline secondary path at

    root_eta_center + 1e-20 - 0.0001.

Because eta* is no larger than center+radius, this proves loss ≤1e-4 relative to
the **proved local primary optimum**, not just the old sampled primary path.
It passes with 4020 processed time cells. This does not prove global or local
secondary-effort minimality; the prior successful numerical secondary search
retains that status, with a now stronger primary-retention comparison.

## 8. Limits retained

No global flare/family/full-class optimum, global secondary optimum, complete
active-regime or wind-domain partition, or resolution of tailwind5/urban60/urban65.
Historical certification remains false. The known-wind mathematical paths are
not a common causal gust policy, go-around viability proof, or calibrated
operational aircraft procedure. No fresh external data or altered assumptions.
