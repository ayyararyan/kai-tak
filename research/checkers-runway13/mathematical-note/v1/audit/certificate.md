# Independent computer-assisted and optimization audit

Audit date: 2026-10-14. Scientific source frozen at repository commit
`78a9ce1c627f917c94306af5529d5e9ebeb743e8`. This is an additive review;
no sealed source or certificate has been changed. The complete workspace working
agreement was read before this review. The parent is responsible for the separate
full reproduction record and final manuscript acceptance.

## Verdict and repair register

The local-certificate implementation supports existence and uniqueness of one
active-system root in the stated nine-dimensional box, strict local primary
optimality in the five flare coordinates, complete-path feasibility, and
non-strict local primary optimality in the twelve-parameter family. The five to
twelve dimensional implication is valid for this particular model because all
six upper-bounding active margins are independent of all seven approach
parameters. It must be proved using this independence, not asserted merely by
embedding a five-dimensional optimum.

One definite source-prose error was found: `local_certificate/DERIVATION.md`
says thrust slew is negative at both gate and touchdown. The actual certificate
and the correctly implemented signed branches give **negative at the gate,
positive at touchdown, positive at the interior slew event**. The source file
must remain preserved; the new note must explicitly record the corrected sign.
This does not change any sealed calculation or theorem value.

Additional presentation repairs required for a rigorous article:

1. Distinguish the exact decimal box from its outward machine hull. The proof
   below shows why the existing strict-inclusion check proves the intended
   decimal-box statement despite the extra interval-input ulps.
2. Treat `_display` fields as rounded diagnostics, not as exact directed
   enclosures. Use coarse, safely outward bounds or the interval-string fields.
   In particular the equal displayed endpoints for stopping position and some
   trajectory coordinates do not mean these quantities are singleton intervals.
3. State the full-family dependence argument and the uniform Taylor-remainder
   argument explicitly.
4. Airborne rate constraints hold phasewise with both one-sided junction values.
   At the gate position, velocity and acceleration agree, so thrust and bank are
   continuous even if their derivatives jump. Contact is a separately stipulated
   hybrid reset, not an airborne acceleration satisfying these same force bounds.
5. The root radius, proof-event intervals, unquantified optimality neighborhood,
   and certified wind domain are four different objects.

## Scope and source inspection

Read in full: local-certificate `interval_root.py`, `validate.py`,
`test_local_certificate.py`, `retention_replay.py`, `verify.py`, `DERIVATION.md`,
`REPORT.md`; parent `conditional_model.py`, `forces.py`, `certify.py`, amendment
A1 and assumption register; refinement `box_certifier.py`; underlying
`counterfactual/continuous.py`. Inspected source certificate contents, event and
cover records, active-branch parameter records and current project-state entries.

The baseline is the unchanged A1 model with constant exact real-decimal wind
`(-4.876589552990943, 9.64006667211232, 0)` m/s. It does not use the unrounded
trigonometric wind vector from the earlier synthetic model. Flight altitude in
the force calculation is CG altitude, whose gate value is 21.24 m and touchdown
value 6 m relative to the adopted runway plane. The seven fixed approach
parameters are the exact decimal renderings of the `baseline.q` entries at
indices `0,4,5,6,7,8,9` in refinement `active_branch.json`.

## 1. The finite root object

Let `p=(Tf/5,xD/300,U/75,fx,fz)` and
`z=(p,eta,sS,sL,sT)`. Write thrust along the flare as `T(p,s)`, upper-load margin
as `(1.4-n(p,s))/.9`, and lower-thrust margin as `T(p,s)/700000`. A physical-time
thrust slew is `T_s/Tf`, not `T_s`.

In the isolated box the six smooth active-margin functions are, in order,

```
g0 = (2636-xD-2 U-U²/(2*1.4709975))/2636,
g1 = 1 + T_s(p,0)/(Tf*100000),
g2 = 1 - T_s(p,1)/(Tf*100000),
g3 = 1 - T_s(p,sS)/(Tf*100000),
g4 = (1.4-n(p,sL))/.9,
g5 = T(p,sT)/700000.
```

The nine equations are `gi-eta=0` for `i=0,...,5`, followed by
`∂s g3=∂s g4=∂s g5=0`. The signs in `g1,g2,g3` above agree with the original
absolute-slew margins on the isolated box and their certified time neighborhoods.
These are analytic inverse-dynamics equations; numerical optimizer convergence
is not a premise of their proof.

The exact decimal center is:

| Coordinate | Exact center string |
|---|---|
| Tf/5 | 0.828166892572350798346132239036969796434284587227 |
| xD/300 | 1.00708819797578277757988923079646312157494318537 |
| U/75 | 0.966828564224417027917923697606192868395258198399 |
| fx | -0.0541639220816773321011413707558375035064437706277 |
| fz | -0.0148247332056131376799362505546836506035492894573 |
| eta | 0.152360764301861701918625206455836893973748530913 |
| sS | 0.763520832037558933983831253901580196263121832139 |
| sL | 0.742524712666685897431892059100460080408671780144 |
| sT | 0.367159602316114440267379742208002318715902381307 |

Define `X=c+[-10^-20,10^-20]^9` using these exact decimals as rational numbers.
The physical coordinate radii are respectively `5e-20 s`, `3e-18 m`,
`7.5e-19 m/s`, `1e-20 m`, `1e-20 m`; event times have normalized-time radius
`1e-20`. They are not error bars on the aircraft model.

The resulting rigorously justified eta enclosure is

```
[0.152360764301861701908625206455836893973748530913,
 0.152360764301861701928625206455836893973748530913].
```

Thus the manuscript's convenient lower endpoint
`0.15236076430186170190` is strictly below the root-box lower endpoint.

### Interval-AD and jet implementation

The dual-number type carries all nine partial derivatives. Normalized-time jets
store coefficients `f^(k)/k!`, through order three. Differentiation through
product, reciprocal, square-root and exponential Taylor recurrences produces
interval enclosures of mixed derivatives as well as values. In particular the
slew stationarity equation uses `-sign*2*T_jet[2]/(Tf*100000)`, and its second
normalized-time derivative uses `-sign*6*T_jet[3]/(Tf*100000)`. The factors two
and six are correct.

The centered polynomial evaluation is an exact finite Taylor identity. Its
center is held fixed during dual differentiation; this is legitimate since the
polynomial identity holds for every constant center. Jet truncation omits only
unrequested higher derivatives and does not approximate any requested lower
coefficient. No finite difference is part of the proof.

### Root proof, including decimal-hull distinction

Let `Xhat` be the outward mpmath interval hull constructed by the program, so
`X ⊂ Xhat`. Let `C` denote the *fixed real matrix whose entries are the exact
decimal strings* obtained by rounding a high-precision numerical inverse.
Its interval hull is used in every computation; treating that hull as a varying
preconditioner is unnecessary. The computed interval matrix `Jhat` encloses
every `DF(z)` for `z` in `Xhat`, hence for `z` in `X`.

The validated checks give

```
||I-C DF(z)||∞ < 1.964e-14 < 1             for every z in X,
K(X)-c ⊂ [-1.964e-34,1.964e-34]^9 ⊂ int([-1e-20,1e-20]^9),
K(X)=c-C F(c)+(I-C Jhat)(X-c).
```

Here the displayed coarse bounds are deliberately wider than the saved values;
the saved maximum offset is below `1.963985900734e-34`. The program verifies
the offset against `rad.a`, the **lower** endpoint of the interval enclosure of
the exact decimal radius. Thus its inclusion check is stronger than inclusion
in the intended exact box, not merely inclusion in a slightly enlarged box.

The mean-value formula implies that `H(z)=z-CF(z)` maps the exact closed box `X`
strictly into itself and is a contraction. Banach's theorem supplies a unique
fixed point in `X`. From `||I-CDF||∞<1`, `CDF` is nonsingular; because it is square,
both `C` and `DF` are nonsingular. A fixed point therefore satisfies `F=0`.
The root is unique in `X`; this does not show uniqueness outside `X` or uniqueness
of a complete twelve-coordinate trajectory. The same argument proves every
actual enclosed Jacobian nonsingular.

The exact interval preconditioner and Jacobian are regenerated from the explicit
code and input center; they are not stored as arrays in `certificate.json`.
The certificate stores strict-inclusion and nonsingularity checks, full offset
interval strings and a float contraction diagnostic. Reproduction is therefore
necessary for an independent executable proof check, not merely a JSON flag test.

## 2. Strict local max-min sufficiency

At the exact root fix `sS,sL,sT` at their exact root values. In this section the
functions `gi(p)` are evaluated at these fixed **normalized** times. They remain
smooth functions of `p` in an open neighborhood because their slew signs and
all inverse-dynamics denominators are separated there.

Let `G` have rows `Dgi(p*)`, a 6 by 5 matrix, and let
`A=[G^T;1^T]`. The interval computation validates
`||I-C_A A||∞ < 2.484e-14 < 1` throughout the root box. Hence `A` is nonsingular
and `rank(G)=5`. The enclosure is for the actual derivatives with event-time
coordinates held fixed, as required, not derivatives along a numerically fitted
event branch.

For `b=(0,0,0,0,0,1)^T`, the exact solution of `A lambda=b` is enclosed by a
Neumann residual estimate. If `lambda_hat=C_A b` and
`r=||I-C_A A||∞<1`, then

```
||lambda-lambda_hat||∞ <= ||C_A (b-A lambda_hat)||∞/(1-r).
```

The six saved enclosures lie inside the following safely enlarged decimal
intervals (all lower endpoints are strictly positive):

| Active margin | Outward summary enclosure for its multiplier |
|---|---|
| stop | [0.8560644515753778, 0.8560644515753782] |
| gate slew | [0.0009658211277946, 0.0009658211277950] |
| touchdown slew | [0.0045094051150227, 0.0045094051150231] |
| interior slew | [0.0087917210360731, 0.0087917210360735] |
| upper load | [0.0514426236725329, 0.0514426236725333] |
| lower thrust | [0.0782259774731976, 0.0782259774731981] |

For every nonzero vector `d`, at least one `Dgi(p*)d` is negative. If all were
nonnegative, their positive weighted sum would be zero, forcing every one to
vanish; the full column rank of `G` would then force `d=0`. On the compact unit
sphere the continuous function `d -> min_i Dgi(p*)d` has a strictly negative
maximum. Thus there is `c0>0` such that

```
min_i Dgi(p*) h <= -c0 ||h||.
```

By smoothness and finiteness of the six functions, choose a common neighborhood
and `M<infinity` such that all six Taylor remainders obey
`|gi(p*+h)-eta*-Dgi(p*)h| <= M ||h||²` there. Consequently

```
min_i gi(p*+h) <= eta* - c0||h|| + M||h||² < eta*
```

for every sufficiently small nonzero `h` (take `||h||<c0/M` when `M>0`). The
true continuous flare max-min value is no larger than these six fixed-event
values. At `p*` complete feasibility below proves it equals `eta*`. This proves
strict local primary optimality, not merely stationarity or KKT necessity.
Neither `c0`, `M`, nor a numerical local-optimality radius has been certified.

## 3. Complete-time proof and the meaning of 398 cells

For the three interior active events, the certificate verifies strictly positive
second derivatives of the corresponding margin throughout a closed interval
containing the exact stationary point. Endpoint slew margins have the correct
one-sided derivative signs on closed endpoint intervals. The five intervals are
the following **exact decimal intervals**, not binary-float domains:

| Margin | Normalized-time interval | Safe derivative statement |
|---|---|---|
| interior slew | [0.7535208320375588,0.773520832037559] | margin second derivative >13.33 |
| upper load | [0.7325247126666857,0.752524712666686] | margin second derivative >6.58 |
| lower thrust | [0.3571596023161144,0.37715960231611445] | margin second derivative >0.869 |
| gate slew | [0,0.01] | margin first derivative >3.78 |
| touchdown slew | [0.99,1] | margin first derivative <-2.31 |

The margins equal `eta*` at the exact active root events. Strict convexity plus
stationarity proves the entire corresponding interior intervals have margin at
least `eta*`; monotonicity proves the endpoint cases. Only these local stationary
minima need isolating. There is no claim that all stationary points of every
function over the entire phase have been enumerated.

`validate.full_path` retains the seven approach coordinates, replaces the five
flare coordinates by interval root coordinates, and checks both complete closed
phases. All remaining operating margins are required to exceed the **upper** eta
box endpoint. On one of the five special intervals, it omits only the margin
already proved there analytically; all other margins remain checked, including
the other two active interior functions. The accepted partition is:

| Coverage statistic | Count |
|---|---:|
| Approach cells | 32 |
| Flare cells | 366 |
| Total accepted cells | 398 |
| Total processed cells, including rejected parents | 786 |
| Accepted cells without any special omission | 347 |
| Cells omitting upper-load margin inside its proved zone | 45 |
| Cells omitting slew inside proved slew zones | 5 |
| Cells omitting lower-thrust margin inside its proved zone | 1 |

For each phase the first endpoint is 0, the last is 1, and every pair of adjacent
accepted cells shares exactly the same stored endpoint. Their interpretation as
decimal rationals therefore gives a gap-free cover even when subdivisions are
selected in floating point. Event checking and ordinary checking both construct
interval inputs from the same decimal renderings. The largest bisection depth
is 12. These are **time enclosures**, not 398 sample evaluations. The smallest
ordinary operating slack is greater than `6.86e-7`; this does not describe the
minimum of all constraints, whose active margins equal `eta*`.

### Hard inequalities and structural identities

The full-path checker encloses the forward-speed and positive upward-lift hard conditions, the
inverse-dynamics force quantities, the exact declared corridor cloud, object and
urban clearance, non-gear ground clearance and gear nonpenetration. Its use of a
nearest-point data structure is not trusted for a sharp distance computation:
any selected point of the frozen cloud gives an upper bound on distance to the
cloud. The distance to that selected point is recomputed in interval arithmetic.
The cloud's binary64 coordinates themselves are the exact declared finite data.

Whole-aircraft clearance uses a sufficient axis-separation predicate: either a
whole-body horizontal bounding radius separates the aircraft from an obstacle
rectangle or its lowest vertical support exceeds the obstacle top plus buffer.
The maximum/disjunction interval operation is inclusion monotone; it can lose
sharpness but cannot turn a violated pointwise condition into a proved one.
The assumed box and gear set, not an unmodelled detailed aircraft surface, are
the objects certified. The 55 m horizontal radius covers the assumed set under
the declared roll/yaw closure.

The flare lateral polynomial is identically zero. At touchdown its accelerations
are zero by the Hermite/bump identities, and lateral position, track and bank
are structural equalities. Gear contact is also structural. To avoid trying to
prove a cancellation-prone interval zero, write

```
zCG(s)-6=(1-s) H(s),   ax(s)=(1-s) A(s).
```

Since `ay=0`, `sin(phi)=m*wy*ax/(H_air*L)`. With `cos(phi)<=1`, the gear
clearance is bounded below by

```
(1-s) [ H(s)-6.0579*m*|wy*A(s)|/(H_air*L) ] + 6(1-cos(phi)).
```

The bracket is enclosed nonnegative and the last term is analytically
nonnegative. This proves pre-contact nonpenetration including exact contact at
`s=1`, not a tolerance allowance for penetration. The distinct symbols `H(s)`
and `H_air` here denote a factored height polynomial and horizontal airspeed.

The touchdown-coordinate and sink margins are strictly above eta; the stop
margin equals eta by the first root equation. After ideal contact the model
resets vertical velocity from -0.7 to zero, uses a straight level pose, coasts
for two seconds, then brakes at 1.4709975 m/s². Rollout geometry is enclosed on
the entire line segment from `xD` to `xD+2U+U²/(2a)`. Gear contact on that segment
is exact by assumption, so the checker replaces its cancellation residual by
zero. It does not claim an aerodynamic certificate for the impact impulse,
tyre authority, struts or physical brake deployment dynamics.

The baseline complete path is a valid witness. It establishes neither
historical obstacle clearance nor aircraft-model calibration.

## 4. Full twelve-parameter transfer, without a dimensional leap

Reorder the original family as `(a,p)`, where `a` comprises approach duration and
the six approach bump coefficients and `p` comprises the five flare coordinates.
The gate position, ground velocity and acceleration are fixed by the family and
the known constant wind. `coeff` builds the flare solely from these gate data,
`Tf,xD,U,fx,fz`, and fixed touchdown data. Thus it is independent of all seven
components of `a`. Stop distance likewise depends solely on `xD,U`.

Let `J(a,p)` be the complete-path continuous primary margin on its feasible
domain, and let `psi(p)=min_i gi(p)` use the six root-normalized active times.
For every admissible approach `a`,

```
J(a,p) <= psi(p).
```

The gate-slew term here is the **flare-side** derivative, present regardless of
the approach derivative at the same junction. Varying approach duration shifts
the absolute gate time but does not remove any normalized flare time from the
constraint domain. At the root `psi(p*)=eta*`; near the root
`psi(p)<eta*` if `p!=p*`. Therefore for every complete feasible `(a,p)` with `p`+sufficiently close to `p*`, `J(a,p)<=eta*`, with strict inequality whenever the
flare coordinates differ. This proves non-strict local optimality at the
certified `(a*,p*)`, and indeed a cylindrical upper bound uniform in admissible
approach coordinates.

No statement that approach perturbations preserve feasibility is needed for
this upper-bound argument. The complete path at `(a*,p*)` does need feasibility,
and that is supplied independently by the 398-cell proof. Approach-only changes
may preserve eta, lose feasibility, or lower the margin. The theorem does not
prove a unique full trajectory or strict twelve-dimensional optimality.

## 5. Retention and sensitivity boundaries

Let `Ueta` be the exact decimal upper root-box endpoint above and let the
unchanged delivered secondary path be `qS`. The separately executed continuous
checker certifies

```
J(qS) >= Ueta - 0.0001
      = 0.152260764301861701928625206455836893973748530913.
```

Because `eta*<=Ueta`, subtraction yields
`eta*-J(qS)<=0.0001`. The direction of comparison is correct: an upper bound on
the primary optimum and a lower bound on the secondary minimum are needed.
No lower bound on `eta*-J(qS)` is implied, and no effort-optimality conclusion
follows. The 4020 count in that receipt is processed cells, not accepted cells.

The reported `deta/dwx=-0.018003131684724366` is in the numerical active-branch
record, not an interval enclosure. The baseline Jacobian certificate gives
local implicit-function regularity for the smooth extended active equations,
but it does not certify that decimal sensitivity, the width of a continuation
domain, or persistence of the active regime at other winds. Separately certified
parameter-dependent feasible trajectories at radius 0.001, 0.002, and 0.005 m/s
provide lower bounds 0.149, 0.147, and 0.140 under a *known constant* wind. Such
construction is not a shared feedback policy for unobserved gusts.

## 6. Dependency and conclusion table

| Result | Premises actually required | Certificate or proof | Supported conclusion |
|---|---|---|---|
| Root | Exact A1 inverse dynamics; nonsingular force domain; correct signed equations | Interval AD, Krawczyk strict inclusion, contraction | One exact active-system root, unique only in the stated box |
| Five-coordinate optimum | Positive six weights; nonsingular augmented gradient matrix; local smoothness; value attainment | Simplex enclosure plus uniform Taylor proof above | Strict local primary max-min optimum in flare coordinates |
| Continuous path | Root equations; signed extrema; gap-free interval partition; hard geometry; structural endpoint/contact identities | Event checks and 398 accepted cells | Complete A1 approach, flare, contact and analytic rollout witness |
| Twelve-coordinate optimum | Complete feasible witness; exact seven-coordinate independence of all six upper-bounding margins | Explicit coefficient dependence plus cylindrical upper-bound argument | Non-strict local optimum in the fixed twelve-parameter family |
| Secondary retention | Primary upper endpoint; secondary continuous lower bound | Separate retention receipt | Primary loss at most 1e-4, not effort-optimality |
| Family lower bound | Certified complete witness and exact eta enclosure | Feasible witness | Family supremum at least 0.15236076430186170190 |

The inherited upper bound `0.181970215` has a separate analytical/domain proof;
it is not supplied by the local certificate. This review does not replace that
audit. No local proof closes the global-family gap or proves global primary,
secondary, unrestricted-class, historical or operational optimality.

## 7. Fresh diagnostic execution

The separate numerical-reproduction pass owns the complete test counts and
continuous certificate reruns. This local source audit does not relabel saved
test logs as fresh successful tests.

Fresh read-only execution completed at `2026-10-13T18:52:54.028471+00:00`
(2026-10-14 in Asia/Kolkata), using Python 3.12.13, NumPy 2.5.4, SciPy 1.18.1,
mpmath 1.3.0 and Matplotlib 3.11.2. The command imported `validate`, loaded the
saved exact center and radius, then called `krawczyk` and `simplex` directly;
it did **not** run either source file's artifact-writing main entry point.
Both checks passed. Each returned root/simplex dictionary was identical to its
saved certificate counterpart. Reconstructing the interval matrices additionally
gave the following upper-endpoint scalars before any float display conversion:

```
root Jacobian norm upper endpoint:
0.00000000000001963985900728542858591246456702956498556949786549251291

simplex matrix norm upper endpoint:
0.00000000000002483435599521030486346876813710605014680928884042551404
```

Directed interval comparisons against `1.964e-14` and `2.484e-14` both returned
true. These decimal displays summarize the actual interval-endpoint objects;
the coarser inequalities in the article are the intended outward statements.

A separate fresh endpoint/active-time evaluation established the following
deliberately enlarged real-decimal slew enclosures, in N/s:

| Event | Enclosure |
|---|---|
| gate | [-84763.923569813833,-84763.923569813827] |
| touchdown | [84763.923569813780,84763.923569813880] |
| interior slew | [84763.923569813802,84763.923569813858] |

Setup history: the initial temporary execution environment lacked Matplotlib,
an import dependency of the existing model module. That attempt ended at import
and supplied no proof result. Adding the dependency resolved the setup failure.
An initial successful diagnostic used mpmath 1.4.1; the accepted final rerun above
explicitly pinned the original certificate's mpmath 1.3.0 and reproduced the
stored root and simplex records exactly. Neither setup attempt altered sealed
artifacts or led to a mathematical repair.

For the complete source-checking execution route, run the note's reproduction
script once provided. For a read-only narrow check from the repository root,
after installing the pinned environment, execute the following Python body:

```python
import json, sys
from pathlib import Path
base = Path("research/checkers-runway13/integrated/assumption_solution/refinement/local_certificate")
sys.path.insert(0, str(base))
from validate import krawczyk, simplex
saved = json.loads((base / "certificate.json").read_text())
root, box, margins = krawczyk(saved["root"]["center"], saved["root"]["radius"])
weights = simplex(margins)
assert root["certified"] and weights["certified"]
assert root == saved["root"] and weights == saved["simplex"]
```

This is a narrow fresh certificate check, not the full numerical reproduction or
final manuscript audit. The final prose/caption cross-check remains a separate
review against the completed manuscript.

## 8. Separate optimization-validity manuscript pass

This pass independently checks the *written theorem logic*, rather than using
the interval-code pass as an optimization approval. Initial reviewed files:
`sections/model.tex`, `sections/active.tex`, `sections/local.tex`,
`sections/attainment.tex` and the regularity argument in `sections/analytical.tex`.
The later continuous/transfer/conditional sections are to be reviewed when
written. This is not yet final manuscript acceptance.

### Conclusions checked

| Logical issue | Initial manuscript result |
|---|---|
| Objective distinguishes operating margins from hard geometry | Correct: geometry is not assigned an arbitrary objective normalization |
| Stationary system versus optimum | Correct: root theorem only establishes the root; a separate simplex sufficiency proof is supplied |
| Strict five-variable sufficiency | Correct: positive weighted dependence, rank five, compact sphere, uniformly bounded Hessians and fixed-time upper support establish a sharp local maximum |
| Local radius versus root radius | Correct: theorem explicitly declines a numerical optimality radius |
| Parameter scaling | Mathematically consistent; explicit definition of the five-vector xi requested for clarity |
| Root isolation versus global uniqueness | Correct: uniqueness restricted to the exact isolation box |
| Whole-time feasibility dependency | Properly a distinct premise, referenced forward rather than inferred from the root or KKT equations |
| Attainment | Supported by compact parameter box, closed hard predicates and uniform nonsingularity on nonnegative-margin paths; not presented as computing a global optimizer |
| Twelve-dimensional transfer | Pending review of the written transfer section; its sufficient proof is in Section 4 of this audit |
| Secondary retention versus minimization | Pending review of the written conditional section; the required comparison direction is in Section 5 of this audit |

### Initial manuscript corrections communicated to the authoring agent

1. `local.tex` said stationarity makes fixed-event gradients coincide with
   derivatives of a smooth local envelope. Stationarity alone does not establish
   existence of that smooth envelope: nondegenerate time curvature and the
   implicit-function theorem are required. Since the actual proof only uses
   fixed times, remove that unnecessary assertion or explicitly cite the later
   positive-curvature result. **Presentation-level justification gap; no change
   to the sufficient proof or certificate.**
2. Replace “a singular G” by “rank(G)<5”: `G` is 6 by 5, not a square matrix.
3. Define one unambiguous flare-thrust symbol before the active equations;
   `dot T_f` is easily confused with a derivative of flare duration. Define the
   physical-time derivative as `Tf^-1 * partial_s` explicitly.
4. Define `xi=(Tf/5,xD/300,U/75,fx,fz)` explicitly.
5. State that the corridor reference comprises the exact stored binary64 values
   in `reference_cloud.npy`. Ideal analytic samples and stored coordinates are
   not exactly the same finite object, although their difference is tiny. The
   certificate uses the latter without relying on float nearest-distance
   accuracy.
6. Avoid simultaneously using scalar `z` for CG altitude and vector `z` for the
   nine root variables; a distinct root symbol removes an unnecessary global
   notation overload.

No fatal optimization defect was found in the initial active/root/simplex/
strict-local sections. Final disposition of these editorial repairs and the
remaining theorem sections must be recorded after inspecting the completed
files, not inferred from their being requested.

## 9. Continuous, transfer and conditional manuscript pass

Freshly read the complete `sections/continuous.tex`, `sections/conditional.tex`
and `sections/discussion.tex`, then cross-checked their conclusion with the
introduction and the already-reviewed active/local argument. The theorem chain
is **not circular**: root and event equations establish the special margins;
independent interval coverage establishes feasibility; local Taylor sufficiency
uses feasibility only to identify its attained objective value; the transfer
uses the fixed-event upper support, not an assumption that the approach is
stationary or that approach perturbations remain feasible.

### Theorem-by-theorem conclusion table

| Written result | Established premises | Proof/evidence checked | Conclusion and residual limit |
|---|---|---|---|
| Validated root theorem | Exact A1 constants, isolated signed branches, regular domain, interval Jacobian | Krawczyk strict inclusion and norm <1, including exact-box versus outward-hull bridge | Unique active-system root in the declared box; no global root uniqueness |
| Positive-simplex lemma | Six actual fixed-event gradients, exact decimal preconditioner, positive residual enclosures | Neumann residual bound; all six weight lower bounds positive; augmented matrix nonsingular | Origin is interior to a full-dimensional gradient simplex |
| Strict local-primary theorem | Positive simplex, local C2 regularity, six active equalities, independent continuous feasibility | Compact-unit-sphere argument and uniform quadratic Taylor remainder | Sharp strict local maximum in five flare variables; unquantified neighborhood |
| Local time-minimum lemma | Stationary root equations; curvature positive throughout each closed event zone; signed endpoint slopes | Correct factors 2 and 6 in interval jets and explicit closed zone endpoints | Whole assigned zones satisfy margin ≥eta; no need to enumerate all global stationary points |
| Whole-time-feasibility theorem | Exact root flare, frozen seven approach decimals, gap-free partition, event lemma, structural endpoint and hybrid laws | 32+366 accepted cells; correct omission counts; independent interval geometry/contact; exact stop equation | One feasible complete A1 path with objective exactly eta; no physical/historical certification |
| Twelve-parameter-transfer theorem | Six upper supports depend only on flare parameters and fixed wind/gate data; complete witness feasible | Explicit polynomial dependence and normalized-time invariance when approach duration varies | Uniform cylindrical upper bound near the flare optimum; non-strict full-family local optimum |
| Retention proposition | Primary upper endpoint, unchanged secondary path's certified continuous lower endpoint | Exact decimal comparison at 0.152260764301861701928625206455836893973748530913 | Loss at most 1e-4 relative to the exact local-primary value; no effort-optimality result |
| Known-wind-neighborhood proposition | Explicit decimal affine decision vectors, wind-dependent recomputed endpoint data, whole-box containment | `parameter_taylor.py` derivative of physical-time derivatives including duration denominators; mean-value inclusion and time coverage | Complete feasible known-constant-wind paths on three stated intervals; not feedback or optimality |

The values in the secondary retention proof, rounded secondary touchdown/stop
positions, and the global bracket gap agree with their source records. The
discussion maintains the distinction between family-global, full-class,
secondary, historical and operational conclusions. The ten-row condition table
and full exact coefficient/root appendices were not yet present at this pass;
their numerical bindings remain to be read after generation.

One new notation repair was requested: the event table differentiates `g2` and
`g3` with respect to normalized time, although the active equations initially
defined them only as fixed-endpoint functions of `p`. Introduce the signed
time-extended margins on the gate/touchdown neighborhoods, or explicitly define
`g2(p,s)=1+dotT(p,s)/100000` and `g3(p,s)=1-dotT(p,s)/100000` before using their
time derivatives. The numerical derivative bounds and underlying proof are
correct; the notation must refer to the actual functions differentiated.

### Additional fresh evidence for strict forward speed of the witness

The model requires only `dot x>=0`, whereas the manuscript states that the
delivered witness has strictly positive forward speed. A fresh read-only
interval-polynomial check supports that stronger statement: over every one of
the stored accepted cells, with the full root-parameter hull, it evaluated
`poly(deriv(cs[phase][0]),left,right)/Tphase`. At
`2026-10-13T18:57:55.287687+00:00`, its smallest lower endpoints were

```
approach: 46.91345312522361085926825426112774217599525231109287237 m/s
flare:    72.51177641931492990280783426562592806525126711302492028 m/s.
```

The directed comparison that both are greater than 45 m/s passed. This used the
same pinned narrow-check environment recorded above; it changed no source
artifact. Thus no strict-forward-speed assumption has been silently added to
the feasible domain.

Status of this pass: all principal theorem implications in the main text are
supported, subject to the communicated notation repairs and later inspection of
the generated exact-input appendices and table. This does not yet accept a
rendered final PDF or final package.

## 10. Final mathematical, table and reproducibility-source audit

Read the completed appendices, abstract, all exact-input tables, condition table,
matrix exporter and public replay wrapper. Checked the abstract/introduction/
discussion against the four principal theorem statements. The RFS class gives
theorem environments an independent counter: the root, strict five-variable,
whole-time-feasibility and twelve-parameter transfer results are Theorems 1–4.

### Exact new finite checks

An independent Python check used `Fraction` arithmetic on the matrix export's
exact binary endpoints and `Decimal` arithmetic for table rounding. It passed:

| Check | Verified count |
|---|---:|
| Root-table exact center strings equal source/export | 9/9 |
| Printed widened Krawczyk component bounds strictly contain exact binary endpoints | 9/9 |
| Fixed approach decimals equal baseline input | 7/7 |
| Wind-family center coordinates equal baseline numerical branch input | 12/12 |
| Nonzero wind-family derivatives equal source branch derivatives | 5/5 |
| Condition-table margins equal downward rounding of certified values to six decimals | 10/10 |
| Condition touchdown and stopping positions round correctly to three decimals | 20/20 |

The stopping values in the last row were independently recomputed from exact
decimal `xD,U` using `xD+2U+U²/(2*1.4709975)`, not copied from the displayed
source stop fields. The baseline condition row deliberately uses its earlier,
weaker certified bound; this does not conflict with the stronger separate
local-primary retention proof for the same unchanged secondary path.

The `verification/emit_matrices.py` implementation exports the actual interval
matrices, both exact decimal preconditioners, residuals, Krawczyk offsets and
multiplier enclosures. Its exact endpoint encoding is correctly documented as
`(-1)^sign * mantissa * 2^exponent`, with the stored bit count an auxiliary
representation field. Exact offsets and multipliers are asserted equal to the
sealed source records. The actual output is
`verification/final/local_matrices.json`.

The public replay wrapper's `--source-root` and `--output-dir` flags are correct.
It runs stages in separate processes, preventing mutable interval-wind globals
from leaking between proof stages. Matrix export is a separate command, not a
side effect of the replay's `all` stage. The corrected source manifest path is
`frozen-source/PUBLIC_SOURCE_MANIFEST.json`; ordinary fresh proof receipts are
under `verification/accepted/`. The publicly selected test receipt reports 102
core/proof plus 15 geometry tests, with five historical-source tests and two
original-workspace preservation tests excluded rather than counted as passes.
Those are independently executed reproduction-agent results, not new full-suite
executions by this proof reviewer.

### Five distinct review domains

| Required review domain | Evidence and disposition |
|---|---|
| Analytical validity | Separate `audit/analytical.md` reconstructs stopping, regularity/attainment and energy exclusion; this pass checked their use by the local theorem and appendix identities, without relabeling those results as a new global solution |
| Computer-assisted validity | This report Sections 1–3 and 7: interval AD/jet algebra, exact decimal inputs, hull distinction, Krawczyk and matrix nonsingularity, positive simplex, event neighborhoods and time-cover semantics checked; narrow root/simplex reproduction exactly matched sealed records |
| Optimization validity | Separate pass in Sections 8–9: strict five-coordinate sufficiency proved by uniform directional decrease; twelve-coordinate transfer proved by parameter independence; secondary retention not upgraded to effort optimality |
| Physical-model consistency | Separate analytical/model review plus this report's hard-geometry/contact inspection: CG versus virtual reference, phasewise control rates, factored gear nonpenetration and ideal hybrid reset retained as A1 assumptions |
| Numerical reproducibility | Public replay receipts, matrix export and exact table checks inspected; full-suite and condition/domain reruns are credited to the separate reproduction pass; omitted restricted tests stay explicit exclusions |

### Final correction disposition

Observed repairs in manuscript source: gate/touchdown sign error corrected with
sealed source preserved; unsupported local-envelope statement removed; rank
language corrected; scaled five-vector explicitly defined; root vector renamed
`zeta` while restoring all physical vertical subscripts `z`; flare thrust and
its physical-time derivative defined unambiguously; endpoint margins extended
as functions of time before differentiation; corridor binary64 inputs identified
as the finite object; Newton replay described as integration of Newton's equation;
manifest filename and matrix-export command corrected.

The root-vector rename briefly changed physical bump subscripts to `zeta` in
`active.tex`. Review caught the editing regression and the parent restored
`b_z,c_z,f_z`; no scientific input or certificate changed.

Figure-caption/source review found no unsupported historical or global-optimality
claim. Captions explicitly identify schematic geometry, numerical-center curves,
true interval-cover data and distinct condition-specific witnesses. Two last
presentation checks were requested: use the manuscript's `zeta` symbol in the
certificate diagram; label the retention inset as a tolerance magnitude (or a
one-sided ray) so the graphic does not imply an unproved upper bound on
`eta(qS)-eta0`. The active diagram's positions are normalized event-time
positions, not a spatial flight path. The figure-production pass owns visual
inspection and regeneration.

Mathematical verdict: **the four principal theorem implications and the stated
conditional retention/wind claims are supported at their declared A1 scope.**
No reduction of the principal conclusions is needed. The remaining checks are
production/presentation acceptance, not an unresolved mathematical proof
dependency. This review does not certify human aerospace validation, historical
flight clearance, a global optimum or a formal proof-assistant derivation.
