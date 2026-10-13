# Calculated complete landing under the stated wind scenario

**Result:** the new calculation constructs a turn, threshold crossing, flare, touchdown and complete stop. Under steady 070° true / 21 kt wind, the selected candidate touches down **302 m beyond the threshold at 141 kt ground speed**, then stops with **553 m of runway remaining**. This is a fresh optimized candidate, not a fit to the accident trace.

[View the complete landing](landing.png) · [Full coefficients](formula.json) · [Path and controls](path_controls.csv)

## Exactly which landing this is

This solves the approved point-mass research model: synthetic entry (-2500,1000,140) m; fixed original zero-wind reference corridor; declared aircraft envelope; approach and flare polynomial family; fixed 2-second braking delay followed by 0.15g deceleration. It maximizes the minimum normalized operating margin, then reduces integrated control effort within 1e-4 of the primary margin. It does **not** maximize runway remaining, fit the accident, or prove a globally optimal/historically flyable landing.

The CAD report's rounded mean 070° true / 21 kt is imposed as spatially uniform and constant through the trajectory. NOAA's 10.8 m/s (~20.994 kt) corroborates the rounded report value but was not substituted. Runway bearing is 135° magnetic minus chart variation 1°50′ west = 133°10′ true. The 1990 chart variation is a scenario convention, not a surveyed 1993 axis. The resulting wind is [-4.876589552990943, 9.64006667211232, 0.0] m/s in forward/right/up axes.

## The constructed landing

| Event | Seconds after synthetic entry | Result |
|---|---:|---|
| Enter modeled approach | 0 | 140 m above runway, track 47° left of runway, 153 kt EAS |
| Cross threshold | 41.223 | 15.24 m high; 153 kt EAS; 142.281 kt horizontal ground speed |
| Touch down | 45.365 | 302.114 m beyond threshold, 140.909 kt ground speed; 151.558 kt EAS; 0.7 m/s sink |
| Fixed braking begins | 47.365 | 2-second ground delay ends |
| Complete stop | 96.644 | 2233.231 m from threshold; 552.769 m remaining |

Ground distance after touchdown: 1931.117 m. Remaining margin beyond the model's required 150 m reserve: 402.769 m. Maximum sampled bank 10.421°; roll rate 2.351°/s. Groundspeed and airspeed are different quantities: the headwind component contributes to the lower ground speed.

The trajectory includes a shallow leveling/rise during the early approach. The unchanged model bounds steep descent but does not require altitude to decrease monotonically; this optimizer outcome is therefore admissible in the stated family. It should not be described as a standard pilot procedure. Introducing a monotonic descent requirement would be a new model constraint, not an implementation repair.

## Closed form

For each phase, s=(t-t0)/T and r(t)=Σ c[k]s^k. Complete numerical x/y/z coefficients follow; no extrapolation outside the phase. The authoritative machine-readable coefficients are in formula.json.

### Approach: t0=0 s, T=41.2226012073917 s

| k | x coefficient (m) | y coefficient (m) | z coefficient (m) |
|---:|---:|---:|---:|
| 0 | -2500 | 1000 | 140 |
| 1 | 1934.549368102485 | -2074.550210351127 | -176.9167686700667 |
| 2 | 0 | 0 | 0 |
| 3 | 3276.552981362745 | 3383.062356915996 | 2933.950323175728 |
| 4 | -8656.604149696548 | -3364.647218569276 | -8305.2735041548 |
| 5 | 11688.32285604023 | -86.179330521255 | 8399.649065339559 |
| 6 | -7637.663260945988 | 2181.352151193109 | -3255.475138584143 |
| 7 | 1894.842205137074 | -1039.037748667449 | 279.3060228937217 |

### Flare: t0=41.2226012073917 s, T=4.1419425532421 s

| k | x coefficient (m) | y coefficient (m) | z coefficient (m) |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 15.24 |
| 1 | 303.1728580638377 | 0 | -17.64617029808398 |
| 2 | 0 | 0 | 0 |
| 3 | -2.193352217954232 | 0 | -36.77006727416774 |
| 4 | 5.31443492984209 | 0 | 72.66870373969033 |
| 5 | -7.478355627306765 | 0 | -35.33699437918808 |
| 6 | 3.298466889858521 | 0 | 1.844528211749475 |

After touchdown, put h=t−45.3645437606339, u=72.4900358883396, a=1.4709975 and xD=302.114052038277. Then x=xD+uh for 0≤h≤2; x=xD+2u+u(h−2)−a(h−2)²/2 for 2≤h≤2+u/a. Afterward x is constant and speed is zero. The runway lateral/vertical ground coordinates are zero. Airborne controls are the source-bound inverse-force functions of the explicit position derivatives and declared constant wind, not independently fitted splines. The CSV includes both one-sided phase endpoints/rates. Ground aerodynamic control columns are intentionally blank.

## Evidence and mathematical bounds

- Four deterministic primary starts succeeded, followed by denser primary refinement and secondary effort minimization; all six solver records are retained in search_checkpoint.json. Multiple agreeing starts do not prove global optimality.
- 10,001 exact-rate samples per phase: minimum normalized margin 0.152793385166486; primary-to-secondary loss 5.21971487694728e-05, within 1e-4.
- Independent forward Newton integration, recomputing forces from integrated states: maximum position discrepancy 7.29411e-08 m; stop discrepancy 4.3827e-07 m. These are numerical consistency residuals, not physical tracking-error bounds.
- Own wind-aware outward-rounded interval checker at 40 decimal digits covers both closed flight phases in 376 boxes. It establishes **eta ≥ 0.1507934696816132** for the exact declared real-decimal candidate/model, including continuous hard inequalities and the exact ground stopping law. It does not reuse the zero-wind certificate.
- A separate global *necessary* bound for this fixed family is **eta* ≤ 66656817/307536544 ≈ 0.216744378190060**. Derivation: xD≥200+500eta; u≥69; xD+2u+u²/(2a)≤2636(1−eta). This yields 3136eta≤2636−200−138−4761/(2a). Combining the valid lower/upper bounds gives a loose gap <0.065950908509; the exact rational gap is stored in result.json. This is **not near-optimality**.
- 37 targeted tests cover wind signs, invalid values, endpoints, independent scalar/vector analytic rates, finite differences, coefficient reconstruction, dense/replay/stopping checks, interval containment/coverage, source identity and rejection of stale certificates. verify_delivery.py repeats artifact generation/replay and checks byte-identical numerical exports.

## What this does not establish

Historical geometry/datum/whole-aircraft clearance and actual entry state remain unresolved. Uniform surface mean wind is not the aircraft's recovered gust history. The aerodynamic envelope, braking and tracking performance are not calibrated. Therefore no physical confidence/prediction interval, historical clearance, accident-counterfactual causal claim, robust feedback-policy guarantee, go-around decision or global near-optimality is supplied. The original historical-mode gate remains closed. The accident report says actual touchdown was controllable and not causal; this conditional model cannot contradict that by assertion.

This is a time-indexed mathematical reference, **not flight guidance**. It answers what the declared model can construct, while the full requested historical landing and physical uncertainty problem remains incomplete.

## Reproduction and files

From this directory, using ../.venv/bin/python:

```sh
../.venv/bin/python calculate.py
../.venv/bin/python continuous.py
../.venv/bin/python deliver.py
../.venv/bin/python verify_delivery.py
```

inputs.json binds frozen sources and the original corridor. calculate.py contains the exact-rate evaluator and search. continuous.py implements the separately adapted checker and hashes its own source, calculator, inputs, candidate and corridor. deliver.py rejects stale or substituted certificates. formula.json and path_controls.csv contain the complete result; landing.png/pdf show it; result.json, verification.json and delivery_manifest.json record evidence. Source aircraft/configuration and terrain-owner files were not modified. No publication/commit/push/peer sync performed by this calculation. Parent independent review is recorded separately from these producer checks.


## Independent review repairs

Blind and edge-case review found lifecycle gaps, not a demonstrated defect in the current candidate's mathematics. Repairs now use unconditional certificate gates (including under optimized Python), reject malformed real-decimal inputs, enforce one shared hard-feasibility predicate for refinement/fallback, and bind selection/certification/export to a current search run. Failed or interrupted searches leave the current run nonconsumable; previous evidence is copied recoverably under archive/.

Output calculations and plots finish in a staging directory before publication. Stable artifact paths resolve through a single atomically replaced current_bundle link; earlier complete bundles remain under bundles/. Thus stale certificates or generation failures do not partly overwrite a delivered bundle. Regression tests exercise failed/interrupted searches, infeasible refinement fallback, malformed intervals, python -O terminal rejection, stale-certificate preservation and atomic bundle switching. The repaired fresh search reproduced the same decisions and landing metrics; source physics, wind inputs and objective did not change.
