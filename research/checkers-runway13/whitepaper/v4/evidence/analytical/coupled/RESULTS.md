# Coupled landing: feasible witness and existence, not an identified optimum

13 October 2026. The requested full closed-form optimum remains **incomplete**.
This continuation constructs a complete candidate and supplies new all-time
feasibility evidence. It does not rename a numerical candidate an analytical optimum.

## What was solved together

All twelve original parameters remain free in the primary candidate search:
approach/flare durations, touchdown position/speed, six approach-shape parameters,
and two flare-shape parameters. Turning, descent, speed, lift and thrust therefore
interact in one constraint system. Ground delay and deceleration remain fixed.
No aircraft, envelope, boundary state, corridor or safety-margin definition changed.
The search uses the continuous counterpart's exact control derivatives and both
one-sided threshold limits. The old sampled executable and artifacts are preserved.

The contact-height equality is satisfied identically by the Hermite basis. The new
search does not numerically differentiate its roundoff residual as an inequality;
this removes no model constraint. The independent interval proof retains nonnegative
height through touchdown by an exact polynomial factorization.

## Fixed candidate and continuous feasibility proof

The authoritative candidate is the exact real-decimal vector recorded in
`continuous_certificate_refined.json`, not a claim that IEEE execution is exact.
Insert that vector into the explicit formulas in `../FULL_LANDING_ANALYSIS.md`.
Those formulas define the entire flight and the fixed-delay/braking ground phase.

`certify_candidate.py` reconstructs polynomial coefficients directly with
outward-rounded interval arithmetic at 40 decimal digits, including endpoint
trigonometric/exponential expressions. It does not interval-wrap coefficients
already rounded by the numerical optimizer. On each closed time interval it:

1. Encloses position, velocity, acceleration and jerk with centered polynomial
   evaluation; reconstructs lift, bank, thrust and their exact derivatives.
2. Proves every margin is at least the stated lower bound, with positive speed,
   horizontal speed, upward lift, nonnegative height and forward velocity.
3. Covers both sides of the C2 approach/flare join independently.
4. Bounds nearest-point corridor distance from above by distance to one actual
   point of the fixed reference cloud. This is conservative and does not replace
   the corridor by a different reference curve.
5. Uses z(s)=(1-s)g(s), g(s)>=0, in flare. The omitted remainder is identically
   zero by the exact Hermite endpoint identities, not discarded numerical error.
6. Checks terminal margins and the exact stopping expression separately. The
   configured obstacle set is empty; this does not certify historical clearance.

The accepted dyadic intervals form a complete cover of [0,1] in each phase.
Decimal endpoint displays and reported floating lower bounds are only summaries;
the decisions compare outward-rounded interval endpoints internally.
The implementation relies on mpmath 1.3.0 interval elementary functions; this is
a reproducible computer-assisted certificate, not a proof-assistant formalization.

Verified witness: approach 37.33776064 s, flare 4 s, touchdown at 313.492181 m
with horizontal speed 77.888055 m/s. The model stops at 2531.321118 m, leaving
254.678882 m of the 2786 m LDA (104.678882 m beyond its required 150 m reserve).
The all-time certified margin is at least **0.0397**, using 2502 accepted closed
intervals. Independent forward replay passes, with maximum position discrepancy
1.45e-7 m and speed discrepancy 4.04e-8 m/s; these are numerical consistency
checks, not estimates of real-aircraft accuracy. The plot includes a brief climb
permitted by the frozen model; no monotone-descent constraint was silently added.

Fresh checks compare 180 scalar evaluations against the vectorized formulas and
interval enclosures, verify both interval covers, reject an overstated margin and
a changed source, and reproduce the certificate from its saved decimal vector.
No new independent-agent audit has been performed on this continuation.

### Verification corrections retained

Two global-exclusion defects were found and repaired before accepting any global
search bound. First, distance to one reference point gives a lower bound on the
nearest-point corridor margin, not an upper bound usable for exclusion. That
entry is now excluded from global pruning. Second, mpmath 1.3.0 interval atan2
returned only pi for a zero numerator and a denominator interval spanning both
signs. This falsely rejected an ancestor box containing the known feasible
candidate. All affected global-search outputs are explicitly invalidated.
The checker now uses the full [-pi,pi] hull unless the denominator is strictly
positive. A regression follows the feasible witness through 130 enclosing
ancestor boxes; none may be excluded. Candidate certification independently
requires strictly positive upward lift and horizontal speed on every accepted
interval, and is rerun with this repair. The scalar upper bound and vertical-speed
lemma do not use atan2 and are unaffected. Bounds 0.10, 0.05, 0.04 and 0.03972
from the invalidated runs must not be used.

## A best path exists within this finite family

This addresses existence separately from identifying the optimizer.

**Lemma (uniform regularity).** Over the entire original parameter box, both
vertical-velocity polynomials have |vz|<14 m/s. `existence_and_bounds.py` proves
this using interval parameters and 128 closed subintervals per phase, with the
exact Hermite basis. This bound is a consequence of the chosen family, not a new
flight-envelope restriction. At feasible eta>=0 and h>=0, EAS>=135 kt implies
V>=135(1852/3600) m/s. Thus horizontal speed exceeds 68 m/s. The load lower bound
also uniformly bounds lift away from zero.

**Theorem (primary attainment).** In the nominal continuous polynomial family,
the primary maximum is attained.

*Proof.* A certified candidate makes the feasible set with eta at least its
positive certified margin nonempty. q belongs to the original compact box;
eta belongs to a compact interval between that lower bound and the previously
proved upper bound. Take any convergent sequence of feasible (q,eta). Polynomial
states converge uniformly, as do derivatives through jerk because durations stay
positive. Height and EAS inequalities pass to the limit, and the lemma prevents
vertical-flight/zero-speed singularities. The load bound prevents zero lift;
the bank bound keeps the lift projection on the positive-up branch. Inverse
forces, exact control rates and all margins are therefore continuous at the
limit. Minimum distance to a fixed finite point cloud is continuous. Each
inequality at each time passes to the limit, as do terminal/ground constraints.
The feasible set is closed and bounded, hence compact. The continuous projection
onto eta attains its maximum. QED.

**Secondary attainment.** The exact integrated effort is continuous on this
regular compact domain. Intersecting with eta>=eta*−1e−4 leaves a nonempty compact
set, so a minimum exists there as well. This theorem proves existence; it does
not evaluate eta*, locate its maximizer, or identify the secondary minimizer.

Neither theorem extends automatically to unrestricted control functions,
uncertain winds, historical terrain, or a family with different parameter bounds.

## Sharper, still unmatched global upper bound

In flare y=0. The global |vz|<14 bound and EAS>=135+40eta imply

    vx >= sqrt([k(135+40eta)]^2 − 14^2),   k=1852/3600.

Since Tf>=4, integrating vx from the threshold gives the necessary condition

    xTD >= 4 sqrt([k(135+40eta)]^2 − 14^2).

Combine it with touchdown u>=sqrt([k(135+40eta)]^2−0.7^2) and stopping:

    4 sqrt([k(135+40eta)]^2−14^2) + 2u + u^2/(2aB)
        <= 2636(1−eta),    aB=1.4709975.

The difference between left and right is strictly increasing for eta>=0.
Outward-rounded evaluation brackets its unique root between 0.1559771 and
0.1559772. Thus eta*<0.1559772 for this family. The former terminal-only upper
bound remains applicable in its wider stated domain; this new bound uses the
finite family's four-second flare minimum and vertical-speed lemma.

## Why the optimality proof is still missing

The lower and upper bounds do not match. Local first-order solver success and
multiple starting guesses cannot fill that gap. A budgeted global interval
exclusion also tests necessary flare constraints over the whole original flare
box; its saved `complete_exclusion` flag, not a solver status, determines whether
it proves exclusion. Surviving boxes are unknown, not feasible solutions.

To identify the optimum we still need exhaustive global exclusion above an
achievable margin (or an equivalent matching analytical certificate), then a
secondary certificate and an unrestricted-control argument if claiming beyond
the polynomial family. These requirements are not waived. The numerical
parameters and computer-assisted inequalities are not the requested closed-form
optimal-parameter formula.

The repaired branch-safe search processed 15,000 boxes at trial eta=0.10,
excluded 3,965, and left 7,071 unexcluded boxes. It therefore **does not prove**
eta*<0.10. These remaining parameter regions, rather than a failure to construct
a feasible path, are the current concrete global-proof gap. They are not evidence
that a better path exists. The retained rigorous bracket is

    0.0397 <= eta* < 0.1559772

for the continuous polynomial family, an absolute gap below 0.1162772.
The bounded search exited normally; no background search or monitoring remains
active. A stronger exclusion method or matching analytical majorant is still
needed. There is no claim that exact solution is impossible.

## Reproduction

Use the existing project virtual environment; the added interval dependency is
`mpmath==1.3.0`. Numerical v1's dependency lock and sources are unchanged.

    python analytical/coupled/solve_coupled.py
    python analytical/coupled/certify_candidate.py
    python analytical/coupled/existence_and_bounds.py
    python analytical/coupled/global_exclusion_attempt.py

The refined certificate can be independently reproduced from its saved decimal
vector using `certify_candidate.certify(q_real_decimal, eta_lower_real_decimal)`.
The search is not needed to verify a fixed witness.
