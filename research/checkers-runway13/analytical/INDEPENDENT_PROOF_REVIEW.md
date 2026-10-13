# Independent proof review

Reviewed 2026-10-13, fresh numerical rerun at 10:51:21 UTC. Scope: `ANALYTICAL_TRACTABILITY.md` and `verify_scs.py`, checked against the frozen implementation specification and current project ledger. No simulator or derivation changes made.

## Verdict

No fatal mathematical error found in the stated restricted S–C–S theorems. The exact geometry, feasible-radius interval, within-family global monotonicity, descent bank mapping, cubic stationary condition and real hyperbolic root are consistent. This is a valid restricted analytical result, not a solution of Aryan's requested full optimal landing.

## Independent algebra checks

- Integrating heading from −δ to zero gives arc displacement `(R sinδ, R(cosδ−1))`. Solving the two endpoint equations gives the stated unique nonnegative straight lengths and the stated radius upper bounds. `cscδ−cotδ=tan(δ/2)` gives `D=C−BR`.
- `B>0` follows from `tan(δ/2)>δ/2`, so time at fixed horizontal speed and level-flight bank decrease strictly with radius. A positive feasible upper endpoint is the unique optimum in this family, including zero-straight cases.
- At constant descent angle, vertical force balance and coordinated yaw give `tanφ=U²/(g R cosγ)`, not the level formula. The stated load factor and thrust balance are consistent with constant speed and constant flight-path angle in the assumed point-mass model.
- Under fixed altitude loss and selectable constant slope, `cosγ=D/sqrt(D²+H²)`. Differentiating the bank proxy gives sign numerator `CH²−D³−2H²D`; the strictly increasing cubic has precisely one positive root. The displayed sinh/asinh expression is the correct real solution, and clipping its radius to the feasible interval gives the global family minimum.
- Degenerate headings, zero radius, incompatible altitude/slope, and fixed-slope radius uniqueness are correctly distinguished. The theorem does not assert feasibility of other path families when this one is empty.

## Boundary fairness and claims

The report correctly discloses that the fixed-H comparison holds horizontal speed fixed while freeing vertical velocity, total airspeed and endpoint flight-path angle. It therefore does not share the frozen simulator's full boundary state. Instantaneous bank/lift changes also violate that simulator's actuator assumptions. The 47-degree example cannot be presented as a competing feasible landing, a better solution to the frozen margin objective, or a whole-problem lower bound. The current text makes these distinctions explicitly.

The largest scientific gap is not a proof defect: no exhaustive trajectory class, full-model PMP derivation, or sufficient global certificate is supplied. Historical constraints and touchdown/stop are absent from this theorem. The full analytical landing objective remains incomplete, as the report acknowledges.

## Nonblocking precision and validation notes

1. For the δ=0 straight degeneracy, `X=0` is only a zero-duration endpoint coincidence at fixed positive speed, not a positive-duration flight. If any subsequent API requires positive duration, use `X>0` there.
2. `geometry()` deliberately computes signed straight lengths outside the feasible family; it rejects only invalid δ/R domains. Its upper-bound tests detect infeasibility but the function is not a complete admissibility validator. Keep that distinction if reusing it outside this verification script.
3. Floating-point corroboration excludes very small heading angles and extreme H/C ratios. The report already warns about small-angle cancellation; no certified-precision claim is justified. Physical thrust availability, lift limits and altitude-dependent aerodynamic feasibility remain unverified, not consequences of the algebra tests.

## Fresh verification

Called `run()` through `runpy` without executing the artifact-writing main block. All 80 constructed random cases and supplied deterministic/domain tests passed. Worst endpoint residual: `1.0444e-10 m`; length residual: `7.276e-12 m`; normalized cubic residual: `7.357e-16`.

Additional independent dense comparisons exercised an interior stationary point and both endpoint-clamping directions; all passed. These are numerical corroboration, not interval-certified global proofs. `verification_results.json` was not modified.

**Correctness:** restricted algebra checked and synthetic tests passed. **Completeness:** full analytical landing remains incomplete. **Readiness:** no operational or historical feasibility established.
