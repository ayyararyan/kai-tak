# Independent analytical and physical-model audit

**Scope:** A1 analytical bounds and physical-model consistency.  
**Source snapshot:** `78a9ce1c627f917c94306af5529d5e9ebeb743e8`.  
**Review/reproduction date:** 2026-10-14.  
**Reviewer:** independently delegated analytical-review agent; not a human referee.  
**Output ownership:** this report and `analytical_derivations.tex` only. No sealed source, result, or certificate was edited. No optimization was run.

## Verdict

The A1 stopping/terminal arguments, compact-family attainment argument, and coupled airspeed–energy–gate-thrust-ramp exclusion are mathematically valid on their declared domains. The baseline exclusion at the exact decimal `0.181970215` was freshly reproduced over all 4096 touchdown-position cells, with displayed smallest interval lower residual `0.9678323903412959 m`. It is a global exclusion within the stated polynomial family, not a global optimal trajectory and not an unrestricted-class bound.

No fatal analytical gap was found in that exclusion. Several qualifications need explicit proof-level treatment in the note:

1. The original synthetic, calm, lumped-reference model and A1 are different mathematical models. Their coefficients, altitude arguments, certified values, and family bounds cannot be pooled.
2. A positive ground speed does not generally select the positive air-relative longitudinal branch. A1's flare-wide lower bound and continuity supply the missing implication; it must be stated.
3. Compactness of the parameter box alone does not establish attainment when inverse dynamics has potential singularities. The exact vertical-speed bounds, gear/bank lower-height implication, load lower bound, and positive-up branch repair this possible presentation gap.
4. The surplus gate thrust must be integrated as positive work, while the worst drag contribution uses an **upper** bound on air-relative path length. Reversing either inequality would invalidate the upper bound.
5. The numerical value of the smallest interval lower endpoint, converted to binary float for display, is not itself a rigorously outward-rounded decimal bound. The verifier's interval comparison is rigorous. A fresh additional all-cell interval comparison in this audit proved that every lower endpoint exceeds the exact decimal `.9678 m`; that weaker inequality can safely be printed. Call `0.9678323903412959` a display value.
6. A1's geometry test is a sufficient bounding-volume separation test and, by stipulation, the exact definition of the conservative admissible set. Its failure does not prove intersection of the actual aircraft and obstacle shapes.

The central local root/simplex/whole-time claims are audited in a separate delegated pass. This report independently checks their model premises but does not claim to replace that proof audit.

## Sources actually inspected

Paths below are relative to `research/checkers-runway13/`; line references bind this snapshot.

| Source | Inspected mathematical role |
|---|---|
| `MODEL_IMPLEMENTATION_SPEC.md` | Frozen original model, point-reference height, nominal objective, envelope, delayed braking |
| `PROJECT_STATE.md`, latest accepted local-certificate entries | Authority and current scientific state; old results not mistaken for current scope |
| `integrated/SPEC.md` | Historical branch and unresolved physical calibration/registration |
| `integrated/assumption_solution/SPEC_AMENDMENT.md:8–20` | A1's assumed scene, virtual-to-CG shift, contact closure, retained box |
| `integrated/assumption_solution/ASSUMPTIONS.md:7–23` | Complete explicit assumption register |
| `integrated/assumption_solution/DERIVATION.md:5–166` | Hermite family, geometry, hybrid law, terminal relaxation, attainment, parent energy bound |
| `integrated/assumption_solution/refinement/DERIVATION.md:5–71` | Coupled speed ratio and gate-thrust-ramp proof |
| `model/trajectory.py:94–148,196–206,241–285` | Density/endpoint convention, original polynomial family and bounds, ground law and normalized margins |
| `integrated/assumption_solution/conditional_model.py:14–84,100–118` | A1 curve construction, conservative hard geometry, structural constraints, numerical terminal evaluator |
| `integrated/assumption_solution/forces.py:4–30` | Moving-basis derivatives and exact inverse rates |
| `integrated/assumption_solution/regularity.py:5–13` | Exact rational shape-derivative bounds |
| `integrated/assumption_solution/analysis_tools.py:7–26` | Outward terminal brackets |
| `integrated/assumption_solution/energy_bound.py:10–65` | Parent energy relaxation and scalar candidate regimes |
| `integrated/assumption_solution/refinement/strong_bound.py:7–39` | Actual full-cell validated stronger exclusion |
| `integrated/assumption_solution/test_solution.py` | Physical checks, preserved disjunction-alias failure, terminal and energy negative controls |
| `integrated/assumption_solution/refinement/test_refinement.py` | Ratio/ramp and invalid-domain tests, unresolved-condition semantics |
| `analytical/FULL_LANDING_ANALYSIS.md` | Original nominal model's exact formulas and terminal proof domain |
| `analytical/coupled/existence_and_bounds.py:7–52`, `RESULTS.md` | Earlier calm-model existence and upper bound; independent rerun |
| `analytical/coupled/global_exclusion_attempt.py`, affected `global_*.json` | Historical invalidations and branch-safe search's nonconclusion |
| `whitepaper/v5/references.bib` | Existing primary-reference inventory, not a substitute for mathematical proof |

## Reconstructed mathematical conclusions

### 1. Hybrid stopping and terminal restrictions

For touchdown coordinate `x`, nonnegative speed `U`, delay `τ=2`, and braking acceleration `a=1.4709975`, integration gives

\[
S(x,U)=x+\tau U+\frac{U^2}{2a}.
\]

The derivatives are `∂S/∂x=1` and `∂S/∂U=τ+U/a>0`. Thus the reserve margin `1−S/2636` is strictly decreasing in each variable. The admissible speed at required margin `e` is exactly

\[
0\le U\le -a\tau+\sqrt{a^2\tau^2+2a\{2636(1-e)-x\}},
\]

provided the braces are nonnegative. At zero available distance the only allowed speed is zero. A1's positive-speed family excludes that boundary automatically. The stop model is stipulated, not inferred from brake/tyre physics; no aerodynamic force/rate constraints are imposed after the ideal reset.

At A1 touchdown, CG height is `6 m` above the model runway, lateral ground velocity is zero, and vertical velocity just before reset is `−σ`, `σ=.7`. For known horizontal wind, define

\[
\Delta(e)=\{k e^{6/17000}(135+40e)\}^{2}-w_y^2-\sigma^2,
\quad U_-(e)=w_x+\sqrt{\Delta(e)},\qquad k=1852/3600.
\]

On the positive longitudinal air branch with `Δ>0`, `U_->0`, the EAS lower margin gives `U≥U_-`. The touchdown-position lower margin gives `x≥200+500e`. Monotonicity of stopping gives the necessary inequality

\[
F(e)=200+500e+2U_-(e)+U_-(e)^2/(2a)-2636(1-e)\le0.
\]

Here `U_-'=40 k² exp(12/17000)(135+40e)/sqrt(Δ)>0`, so `F'=3136+(2+U_-/a)U_-'>0`. Fixed endpoint EAS gives `e≤.45`. Therefore the terminal-relaxation regimes follow from endpoint signs and the unique root. With the exact floor `U≥69`, replace `U_-` by `max(69,U_-)`; `F` remains strictly increasing although it need not be differentiable at the switch.

For baseline wind, fresh outward arithmetic gives:

| Domain | Exact certified bracket / value |
|---|---|
| Terminal relaxation without family speed floor | `1258200404569269/5629499534213120 < ηT < 629100202284639/2814749767106560` |
| Decimal upper display | `0.2235012893992799` |
| Speed-floor-binding family terminal relaxation | `η69 = 66656817/307536544 ≈ 0.2167443781900599` |
| Stronger energy/ramp family exclusion | exact trial decimal `0.181970215` excluded |

The terminal root is attained **in the relaxation** by its lower-bound terminal position/speed. This is not a landing construction. If a squared quartic is used, retain the unsquared equation `Q+B sqrt(Δ)=0`; `B=2+w_x/a` is negative for the baseline headwind. Squaring without its sign condition introduces spurious roots. The lower endpoint of a root bracket is not a feasible-flight lower bound.

### 2. Uniform regularity and attainment

The A1 endpoint vertical speeds have absolute values strictly below `5 m/s`; fresh 60-digit interval evaluation bounds them by the displayed `4.293256992989995` and `4.261864869074666`. Wind does not enter these vertical endpoint speeds because vertical wind is zero and endpoint EAS/air-angle are fixed.

Let `H,A,B` be the Hermite displacement/initial-velocity/final-velocity polynomials and `b,o` the even/odd endpoint-null bumps. Exact rational Bernstein subdivision over 128 dyadic cells yields

\[
\|H'\|_\infty\le15/8,\quad
\|A'\|_\infty,\|B'\|_\infty\le1,\quad
\|b'\|_\infty\le288141339/83886080,\quad
\|o'\|_\infty\le2.
\]

The unchanged parameter box therefore implies

\[
|v_{z,A}|\le\frac{33792275107}{1258291200}<26.856,
\qquad
|v_{z,F}|\le\frac{719106075}{33554432}<21.432<22.
\]

These are global box bounds, not empirical speed limits. Gear nonpenetration and `|φ|≤25°` imply

\[
z_C\ge6\cos\phi+6.0579|\sin\phi|\ge6.
\]

For `θ∈[0,25°]`, the derivative of `6 cosθ+6.0579 sinθ` is positive, so its minimum is its value `6` at zero. Hence any nonnegative-margin feasible sequence has `V≥135k`, and the horizontal airspeed satisfies the convenient exact lower bound `H_air>64 m/s`. In fact

\[
(135k)^2-\left(\frac{33792275107}{1258291200}\right)^2-64^2
=\frac{9617823244026244151}{1583296743997440000}>0.
\]

Also `L≥.5mg` and `l_u=L cosφ≥.5mg cos25°>0`. Thus no denominator or angle branch in the force/rate formulas becomes singular along the closure of the feasible set. Positive phase durations give uniform convergence of polynomials and their derivatives under parameter convergence. Position/force/control margins, distance to a fixed finite reference cloud, max/min clearance functions, terminal margins, and interval ground-segment geometry are continuous on that closure. Each all-time inequality passes to the limit. A certified nonempty superlevel set in the compact box is therefore compact; its primary objective attains its maximum. The exact normalized-time effort integral is continuous on that set, so its primary-retaining secondary minimum is also attained.

This does **not** identify either optimizer, prove uniqueness, or establish unrestricted-path compactness. It is useful to state this proof in the note rather than merely invoke the parameter box.

### 3. Stronger family exclusion: independently reconstructed proof

**Height bound.** With `H=10s³−15s⁴+6s⁵`, `A=s−6s³+8s⁴−3s⁵`, `B=−4s³+7s⁴−3s⁵`, the flare height is

\[
z_C=21.24-15.24H+T_f v_{g,z}A-.7T_f B+f_zb.
\]

On `[0,1]`, `H∈[0,1]`, `A≥0`, `B∈[-.2,0]`, `b∈[0,1]`. Since `v_g,z<0`, `T_f≤12`, and `f_z≤10`, this is at most `21.24+12(.7)(.2)+10=32.92<34`. Thus feasible flare trajectories have `z_C∈[6,34]` and `|v_z|≤22`.

**Forward branch.** Since `y≡0`, `V²=(u−w_x)²+w_y²+v_z²`. EAS/height bounds give `(u−w_x)²≥V_-²−w_y²−22²>0`. The fixed gate has `u−w_x>0`; continuity prevents its sign changing. Consequently `u≥u_-:=w_x+sqrt(V_-²−w_y²−22²)>0`. This is stronger reasoning than inferring forward airspeed from positive ground speed.

**Drag.** Set `v_-=k(135+40e)`, `v_+=k(175−40e)`, `V_-=v_-exp(6/17000)`, `V_+=v_+exp(34/17000)`, `Q±=.5ρ0S v±²`, `L+=mg(1.4−.9e)`. Dynamic pressure times area is exactly `.5ρ0S EAS²` in SI units. The function `.08Q+.045L²/Q` increases with `L²` and is convex in positive `Q`, hence the valid common drag bound is

\[
D_+=\max_{Q\in\{Q_-,Q_+\}}\left(.08Q+.045L_+^2/Q\right).
\]

Omitting the simultaneous lift-coefficient cap only enlarges this relaxation.

**Air-relative distance.** For `u≥u_-`,

\[
(V/u)^2\le f(u)=1-2w_x/u+(w_x^2+w_y^2+22^2)/u^2.
\]

Writing `c=w_x²+w_y²+22²`, `f'=2(w_xu−c)/u³`. If `w_x≤0` it decreases; if `w_x>0` the only positive critical point is a minimum. Its supremum on the half-line is at the left endpoint or infinity. Therefore

\[
\int_0^{T_f}Vdt\le R_vx,\qquad
R_v=\max\left(1,\sqrt{(u_--w_x)^2+w_y^2+22^2}/u_-\right).
\]

**Mandatory thrust ramp.** At the fixed zero-acceleration gate,

\[
T_g=-mg\sin3.1^\circ+.08Q_g+.045(mg\cos3.1^\circ)^2/Q_g,
\quad Q_g=.5\rho_0S(153k)^2.
\]

Let `T_-=700000e`, `K=100000(1−e)>0`, `A=max(0,Tg−T_-)`. The rate cap and thrust floor imply `T(t)≥T_-+max(A−Kt,0)`. Moreover `u≤w_x+V_+`, so `T_f≥t_-:=max(4,x/(w_x+V_+))`. With `z=min(t_-,A/K)`, the nonnegative excess-thrust work is at least `V_-J`, where `J=Az−Kz²/2`.

**Energy.** For constant horizontal wind, `v_a'=a` and `v_a,z=v_z`. Taking the tangential component of Newton's law therefore gives

\[
\frac d{dt}(V^2/2+gz_C)=(T-D)V/m.
\]

The force model need not be conservative; this identity follows directly from its power equation. Combining the preceding bounds,

\[
V_D^2\ge V_g^2+2g(15.24)
-\frac{2\max(0,D_+-T_-)R_v}{m}x+\frac{2V_-J(x)}m.
\]

Use `V_D²=(U−w_x)²+w_y²+.7²`, `R=V_g²+2g(15.24)−w_y²−.7²`, `C=2max(0,D_+−T_-)Rv/m`, `B(x)=2V_-J(x)/m` to obtain

\[
U\ge U_b(x):=\max\{69,U_-(e),w_x+\sqrt{\max(0,R-Cx+B(x))}\}.
\]

The zero replacement remains valid by the already-proved forward-air branch. Stopping is increasing in `U`. Thus a feasible path at level `e` requires at least one `x∈[200+500e,700−500e]` for which

\[
x+2U_b(x)+U_b(x)^2/(2a)\le2636(1-e).
\]

The actual certificate partitions this **entire** interval, evaluates every displayed expression outward, and obtains strictly positive lower residual on each cell at `e=.181970215`. Feasible sets of the original max-min problem are nested in `e`, so all higher margins are excluded without assuming that the relaxed algebraic residual is itself monotone.

### 4. Model consistency requirements for the manuscript

| Object | Correct A1 interpretation |
|---|---|
| `r` and `rC` | Virtual point and CG satisfy `rC=r+(0,0,6)` by a constant inertial translation. A rotating material gear point does not satisfy this acceleration identity. |
| Density height | Evaluated at `zC`, measured above the model runway. The assumed `6 m HKPD` runway datum enters obstacle conversion, not an additional density-height offset. |
| Endpoints | Virtual heights `140,15.24,0`; CG heights `146,21.24,6`. Endpoint velocities must be recomputed at the CG heights, so A1 is not obtained by shifting old coefficients alone. |
| Wind | Baseline exact decimal vector `(-4.876589552990943,9.64006667211232,0) m/s`; negative along-axis component means headwind. Ground-track and air-heading differ. |
| Bank | Inverse-dynamics lift bank and stipulated body roll; pitch zero and yaw ground-track are additional pose assumptions, not six-degree-of-freedom dynamics. |
| Body/gear | CG-fixed body box and ideal point gear; lower supports `zB=zC−4cosφ−32.7|sinφ|`, `zG=zC−6cosφ−6.0579|sinφ|`. |
| Obstacles | Assumed rectangular source forms, assumed heights/datum/urban blanket. `max(horizontal_gap,vertical_gap)≥0` is a conservative clearance predicate, not a calibrated terrain result. |
| Contact | At touchdown zero bank and ideal simultaneous wheel contact. Vertical speed and angular motion reset ideally; strut loads and angular impact mechanics are not certified. |
| Ground | Flat `zC=6`, `y=0`, assumed lateral tyre authority, fixed delay/deceleration; no uncontrolled reinterpretation of the airborne rate cap across the reset. |
| Corridor | Fixed finite synthetic reference cloud translated by `+6 m`; it is not reoptimized, historical, or a continuous reference curve. The exact certificate uses `iv.mpf(float(component))`, hence the exact stored binary64 value for each component of the sealed `.npy` array, not the exact real-number evaluation of the original polynomial at those sampling times. The nearby historical comment mentioning “float repr” is stale and does not describe the conversion actually executed. |
| Hard constraints | Obstacle/ground clearance and inverse-domain constraints do not acquire arbitrary objective normalizations. The `.2 m` search-only obstacle guard is not part of the mathematical objective or final acceptance threshold. |
| Structural equalities | Hermite endpoint and C2 joining identities, flare `y≡0`, fixed sink and zero endpoint acceleration imply touchdown lateral/track/bank margins exactly one; contact equality is allowed. |

The original synthetic zero-wind family has separately certified `|vz|<14`, a witness margin `.0397`, and family upper bound `<.1559772`. Those values concern the old height/density/reference/wind model. Their relationship to A1 is historical progression, not a bound comparison on a common feasible set.

### 5. Preserved invalidations and explicit nonconclusions

* `analytical/coupled/global_exclusion_attempt.json` and `global_exclusion_10000.json`: a lower enclosure of corridor margin was incorrectly usable as an exclusion upper bound. They are marked invalidated. Distance to one reference point provides a sufficient feasibility test, not an exclusion certificate.
* The `global_upper_003972.json`, `_004.json`, `_005.json`, `global_exclusion_corrected.json`, and `global_exclusion_endpoint_exact.json` tight bounds are invalidated: interval `atan2` at zero numerator with a denominator spanning zero failed to enclose the branch. No `.03972/.04/.05/.10` global bound may be resurrected from them. The branch-safe surviving-box run is incomplete, not a proof of exclusion.
* The A1 `cases/urban55/pre_exit_limit_repair/result.json` candidate passes its sampled upstream disjunction with minimum `+0.045035446184471084 m`, but its exact urban-exit one-sided clearance is `−0.037838837736877906 m` on fresh evaluation. It is an invalidated mesh-acceptance precursor, not an accepted continuous construction. The source retains it and explicitly tests rejection.
* Tailwind `5 kt` at `e=0` remains unexcluded by the stronger relaxation: fresh run reports `excluded:false`, first unresolved cell `0`. No feasibility or infeasibility conclusion follows.
* Urban `60/65 m` failed numerical searches are unresolved. The energy bound does not use those obstacle heights, so it cannot by itself classify them.

## Fresh execution evidence

All calls were read-only function calls or in-memory exact arithmetic; all executable `__main__` writers were avoided. `python -B` avoided source bytecode writes. Runtime: Python environment under the authorized reproduction workspace, NumPy `2.5.4`, SciPy `1.18.1`, mpmath `1.3.0`.

| Check rerun | Actual result |
|---|---|
| `strong_bound.exclusion(Case(),'0.181970215',4096)` | `excluded:true`, 4096 cells, residual lower display `0.9678323903412959` |
| Same 4096-cell calculation with comparison to exact `.9678` instead of zero | Every interval lower endpoint strictly exceeds `.9678 m` |
| `strong_bound.exclusion(Case(wind=(5*KT,0,0)),'0',2048)` | `excluded:false`, first unresolved cell 0; correctly no infeasibility claim |
| Exact Bernstein derivative bounds, reconstructed directly from `polynomial_range` | Matched all five saved rational shape bounds and both saved rational vertical-speed bounds exactly |
| Endpoint vertical-speed bound with mpmath interval precision 60 | Both strict `<5` comparisons pass |
| `analysis_tools.terminal_interval_bound(Case())` | Full and family root brackets have strict opposite-sign interval residuals; values above |
| `analysis_tools.fixed_gate(Case(frame_dx=80,frame_dy=-50,runway_level=4))` | Negative `urban_side_1=-10 m`; a fixed-gate exclusion for the conservative assumed scene |
| Old `existence_and_bounds.vertical_bound()` | Both 128-cell phase checks pass; display maxima `11.645983141916668`, `13.949332088876938`; horizontal speed `>68` in old nominal domain |
| Old `existence_and_bounds.stronger_bound()` | Root bracket `[.1559771,.1559772]`, lower residual upper display `−.00013125194352436916`, upper residual lower display `+.0002464956673745526` |
| Preserved urban55 pre-repair path | One-sided negative gap reproduced, despite positive sampled gap |

A convenient nonmutating reproduction of the principal bound, from repository root, is:

```sh
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import sys
sys.path.insert(0,'research/checkers-runway13/integrated/assumption_solution/refinement')
from strong_bound import Case,exclusion
print(exclusion(Case(),'0.181970215',4096))
PY
```

The pinned project dependencies must already be installed. No unit-test total is asserted by this audit; the separate numerical-reproducibility pass owns the full-suite result.

## Citation recommendations verified against primary sources

No external source is needed to replace the self-contained stopping, compactness, simplex, or energy proofs. For the validated-numerics method, two precise sources were checked on 2026-10-14:

* R. Krawczyk, “Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken,” *Computing* **4** (1969), 187–201, [publisher record / DOI](https://doi.org/10.1007/BF02234767).
* S. M. Rump, “Verification methods: rigorous results using floating-point arithmetic,” *Acta Numerica* **19** (2010), 287–449, DOI `10.1017/S096249291000005X`, [author-hosted corrected manuscript](https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf), [institutional bibliographic record](https://tore.tuhh.de/entities/publication/dee47218-ca2f-4cfa-9ada-0c60b14a9097).

These are primary method references, not attestations of this implementation. Existing V5 aviation references can provide provenance context, but the note should not cite a general Boeing/CAD source as evidence for A1's invented hard geometry, aerodynamic calibration, or gear-impact sufficiency.

## Acceptance boundary

**Analytical logic:** independently reconstructed and accepted within the documented assumptions.  
**Executable bounds:** fresh nonmutating reproductions pass at the precise scopes recorded above.  
**Physical consistency:** A1 is internally coherent as a conditional reduced model, provided the coordinate/contact distinctions in this audit are retained. It is not physically calibrated or historically certified.  
**Global and secondary optimality:** remain open; existence and upper exclusion do not identify the optimizers.  
**Manuscript integration:** the parent must verify that the final theorem statements retain these domains; this report is not an audit of a future unseen manuscript revision.

## Draft-section review and disposition

The initial `sections/model.tex`, `sections/analytical.tex`, and `sections/attainment.tex` were inspected after this source audit. The following concrete corrections were sent to the parent:

* **Accepted, must be incorporated:** Define the canonical hard forward predicate as `vx≥0`. Both the original and A1 evaluators use this closed inequality. A strict interval `vx>0` check proves a stronger property of the witness; it does not change the mathematical admissible class. Once the manuscript uses the canonical inequality, there is no reason for the attainment theorem to introduce a different “closed variant” problem or a strict-class caveat. `Lu>0` is already uniformly implied by the load/bank bounds.
* **Accepted, must be incorporated:** Define the corridor's exact finite coordinates using the certifier's exact binary64 point-cloud values. Its generating procedure is provenance, not a substitute exact definition. The reviewer initially inferred decimal conversion from a stale inline comment; parent inspection of the actual `iv.mpf(float(x))` conversion corrected that inference, and this report has been reconciled to the executable line.
* **Notation:** Define `ρ0=1.225` and `VG=153k exp(21.24/17000)` before their first use; use `exp` where the trial margin is also named `e`; resolve the two-/three-dimensional dot product `w·d` by using horizontal wind or a zero-padded direction.
* **Reviewed and accepted:** Terminal-relaxation sufficiency on `e≤.45`, provided only the retained terminal constraints are meant. The upper touchdown-position margin and both fixed-sink margins allow that choice; additional force/path constraints remain omitted.
* **Reviewed and accepted:** The energy proof's zero-radicand replacement is justified by the already-proved positive air branch. It is not an unsupported square-root substitution.
* **Reviewed and accepted:** The uniform force-regularity and compactness proof, after the forward-predicate correction, supplies the necessary closure argument.

This appendix records a review of those particular draft sections, not acceptance of later or unseen manuscript versions.
