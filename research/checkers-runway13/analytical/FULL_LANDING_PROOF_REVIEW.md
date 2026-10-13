# Independent full-landing proof review

Reviewed 2026-10-13, with read-only reruns at 11:44 UTC. Scope: `FULL_LANDING_ANALYSIS.md` and `verify_full_landing_analysis.py`, checked against frozen `MODEL_IMPLEMENTATION_SPEC.md` v1, the research brief/project ledger, configuration, trajectory source and authoritative scenario artifact. This reviewer wrote only this report; parent-owned repairs are identified below. No optimizer, aircraft operation or simulator modification was performed.

## Verdict

**No fatal mathematical defect found in the explicit path/inverse-control identities or the necessary nominal objective upper bound. The complete optimal landing remains unsolved.** The analysis correctly separates explicit evaluation at chosen parameters from optimization of those parameters, sampled diagnostics from continuous-time feasibility, and the polynomial family from unrestricted controls.

The strongest new result is a rigorously bracketed necessary upper bound for the exact stated zero-wind scenario. It is not an attained objective value, a certified continuous optimality gap, a historical reconstruction, or proof of aircraft safety. A second-model audit is evidence, not an exhaustive formal proof.

## Mathematical checks

1. The quintic coefficients invert the endpoint position/velocity/acceleration matrix exactly. The two endpoint-null bumps preserve the stated C2 join. Their degrees and coefficient bounds agree with the implementation. Shared acceleration does not imply shared jerk; keeping both one-sided control rates is necessary and correct.
2. For constant wind, the velocity-basis derivatives, lift projection, bank derivative, dynamic-pressure derivative and thrust derivative follow directly by differentiation. These formulas require positive airspeed, nonzero horizontal airspeed and positive lift. The report states these domains and does not claim arbitrary parameter vectors are admissible. Time-varying wind would need extra derivatives and is outside scope.
3. The delay/braking formula agrees with the stipulated ground model. Removing vertical velocity at contact is an explicit reset, not a landing-gear calculation. The straight ground interval permits the stated exact cylindrical-obstacle clearance calculation.
4. The continuous margin formulation preserves the existing margin conventions and fixed reference point cloud. Exact-rate constraints are properly distinguished from the executable spline-rate approximation. There is no justified general ordering between those two numerical objectives without rate-error control.
5. At touchdown, zero wind, zero lateral speed, height zero and sink 0.7 give EAS = sqrt(u²+0.7²)/κ. The lower EAS and touchdown-location margins imply u ≥ vmin(eta) and xTD ≥ 200+500 eta. Stopping distance is strictly increasing in both xTD and positive u. Substitution therefore gives a necessary inequality, in the correct direction.
6. For eta ≥ 0, vmin is positive and increasing, so F is strictly increasing. Its signs at 0 and 0.45 bracket one root. Negative objective values also lie below the positive root; no feasible negative-eta case contradicts the bound. Extra constraints can only lower the attainable objective.
7. Replacing vmin with κ(135+40 eta)−0.7 gives a valid weaker stopping-distance lower bound because the replacement is positive on this domain. The resulting positive quadratic root is consequently an upper bound, not a feasible construction.
8. The weighted-margin argument in §7 is a valid sufficient-certificate strategy if its proposed global inequality and matching feasible trajectory are actually established. Neither has been established. First-order multipliers alone would not suffice; the report says so.

## Findings and disposition

| Finding | Severity | Disposition |
|---|---|---|
| “Generally not attainable” suggested a nonattainment conclusion that had not been proved. | Wording affecting mathematical scope | Parent replaced it with unknown attainment. Accepted. |
| The original exact bound used hard-coded nominal constants without checking the loaded configuration. A changed wind/braking/envelope could inherit an irrelevant certificate. | Verification/domain gap | Parent added `check_bound_domain` for wind, touchdown sink/location, EAS limits, delay/deceleration, runway/reserve and G/κ, with four changed-domain rejection cases. Inspected and independently rerun successfully. |
| Rational bracketing certifies the exact real nominal constants, not every floating-point operation in the sampled executable. | Precision/evidence qualification | Parent added an explicit precision-domain paragraph in §8; inspected and accepted. No change to the bound or model is needed. |
| Fixed endpoint-margin diagnostic expressions use frozen nominal normalization constants. | Low; future reuse | Valid for current v1. If reusing this verifier with a different envelope, derive those auxiliary diagnostics from configuration or reject all such changes; the main bound's new guard is not a general verifier-domain guarantee. |

The precision qualification matters only to the type of certificate, not the displayed six-decimal result. As a diagnostic, treating the executable's binary κ, deceleration and sink values as exact real inputs shifts the root by approximately −7.72e−17, which exceeds the 3.90e−19 rational bracket width. This is not a proof that floating executable outputs violate the upper bound; it demonstrates why that narrow bracket must not be described as end-to-end floating-point validation. Reported sampled eta remains numerical.

## Fresh verification evidence

Both verifier `run()` functions were imported with bytecode disabled and invoked directly, avoiding their main-program JSON writes.

- Full verifier passed: exact rational Hermite identity; 41 parameter-vector curve comparisons; 50 interior derivative checks; four changed-domain rejection cases.
- Maximum coefficient discrepancy: 5.820766091346741e−11.
- Maximum roll-rate finite-difference discrepancy: 7.96628041310754e−12 rad/s.
- Maximum thrust-slew finite-difference discrepancy: 4.4325167255010456e−4 N/s.
- Maximum Newton reconstruction residual: 7.67420334337097e−15 m/s².
- Sampled exact-rate eta: 0.03889642872930277. This is not an all-time lower certificate.
- Independent 75-digit Decimal bisection, separately coded for the scalar necessary inequality, gave root 0.157694902550945085694119449429119875076344680312774241975675238423348401138.
- Independent F evaluations at the rational certificate endpoints were approximately −4.12994031666e−16 and +1.22401199087e−15, confirming the reported bracket signs. The verifier's Fraction/isqrt enclosures provide the exact-arithmetic certificate; Decimal is an independent numerical corroboration.
- The unchanged simulator SHA-256 was `9b557ce07c7e8f177b0b3cfac1765c1c9aec4997e28b52d3185ad533f7cf3f6a`, matching the authoritative artifact.

### Additional finite-roll repair reviewed

Parent requested review of the endpoint-root repair in `verify_finite_roll_position.py`. Returning lo or hi when its function value equals the target is appropriate: an endpoint target must preserve the endpoint, particularly when the derivative vanishes there and rounded evaluations cease to distinguish nearby arguments. The change does not relax acceptance tolerances or prove quadrature exactness. Fresh rerun passed 30 synthetic cases and five domain rejections; maximum altitude-root bank error was 4.390932062392494e−14 rad, with maximum independent ODE position discrepancy 1.454589213218943e−10 m. The prior finite-roll theorem review remains separate; this extra check addresses the repair, not a new full theorem audit.

## Completion and remaining proof obligations

**Correctness:** the inspected identities and necessary nominal bound are supported by derivation and fresh checks, within their stated domains.

**Specification completeness:** incomplete for Aryan's requested complete analytical optimal landing. Missing are optimal parameter formulas, an all-time feasible witness, a matching global primary certificate, secondary-optimality proof and an unrestricted optimal-control solution. Historical terrain, aircraft calibration and routine-flight evidence are not supplied by this analysis.

**End-to-end readiness:** verifier reproduction is confirmed. Continuous-time or historical landing validity is not certified. No assertion that a complete closed form is impossible is justified by the current investigation.

Next decisive mathematical evidence would be a continuously feasible construction and matching global bound, or a further rigorous bound that narrows the unresolved attainable range. Merely reproducing the sampled eta or adding denser samples would not close these proof obligations.
