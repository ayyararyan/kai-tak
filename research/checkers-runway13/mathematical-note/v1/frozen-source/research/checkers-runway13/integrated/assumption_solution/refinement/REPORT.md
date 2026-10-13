# Conditional landing: additive mathematical refinement

## Result

The baseline **polynomial-family** optimum is now rigorously bracketed by

**0.15225866725206007 ≤ η*family ≤ 0.181970215.**

The gap is **0.029711548**, down from the delivered gap of about 0.042299306. The lower improvement comes from a tighter continuous certificate for the **unchanged delivered baseline path**. The upper improvement comes from coupled speed/energy and mandatory gate-thrust-ramp inequalities. **Global optimality remains unproved.** The full-class terminal bound is unchanged; the stronger family bound does not apply to arbitrary smooth paths.

Two additional complete landings are continuously verified:

| Condition | Certified margin | Touchdown (m) | Stop (m) | Runway remaining (m) |
|---|---:|---:|---:|---:|
| 3 kt tailwind | 0.005547484 | 319.660 | 2621.245 | 164.755 |
| 58 m urban blanket | 0.011876479 | 694.037 | 2593.470 | 192.530 |

Both retain the original two-second delay, .15g braking and 150 m reserve. Both pass independent Newton replay and continuous ≤10⁻⁴ retention of their local primary benchmark. The urban58 secondary search initially hit its iteration limit; its smaller-step restart converged and was re-certified. The failed stage is preserved.

There are now **ten verified condition points across the parent and additive packages**. This is not a complete condition-domain solution. Original delivered paths and reports remain byte-for-byte unchanged.

## Requested unresolved cases: new work, unchanged status

Warm continuation used the nearest accepted tailwind2 and urban55 paths, rather than restarting blind multistarts. Exact urban-exit geometry remained enforced. Target re-solves used 1201 optimization points and 20001-point diagnostics; urban65 received two different continuation seeds.

| Target | Best fresh dense diagnostic | Conclusion |
|---|---:|---|
| 5 kt tailwind | margin about −0.01711; optimizer did not converge | Unresolved. Stronger energy relaxation excludes η≥0.060058594, but not η=0. |
| 60 m urban blanket | margin about −0.06295; exit clearance .2 m, vertical odd-bump bound active | Unresolved. This local branch cannot furnish a feasible path. |
| 65 m urban blanket | two negative-margin branches, about −0.78060 and −1.67741 | Unresolved. Poor local branches do not establish global infeasibility. |

Optimizing the condition itself at zero margin locates local mesh transitions near **3.50319 kt** and **58.32087 m**. Dense rechecks are slightly negative, so these are **uncertified local boundary estimates**, not feasibility or exclusion thresholds. Their useful outcome is to locate where this continuation branch loses feasibility and to motivate the separately certified 3 kt/58 m paths.

## Evaluated local sensitivity and a verified domain

The actual limiting flare system has six active margins: stop, gate slew, touchdown slew, interior slew, upper load and lower thrust. Solving these six equalities plus three interior-time stationarity equations gives baseline numerical η≈0.1523607643. The five-variable flare sensitivity to along-runway wind, holding the crosswind fixed, is

**dη/dwx ≈ −0.01800313 per m/s.**

The evaluated parameter derivatives and positive numerical multipliers are in [active_branch.json](active_branch.json). Centered re-solves confirm the derivative. Numerical regularity is not an interval root-existence proof; a more distant equality solution has a negative multiplier and is not accepted as an optimal branch.

An explicit affine trajectory rule q(δ)=q0+q′δ, with endpoint velocities recomputed for wx=wx0+δ, is continuously certified over three closed domains:

| Along-wind radius | Certified margin of the affine family |
|---|---:|
| ±0.001 m/s | 0.149 |
| ±0.002 m/s | 0.147 |
| ±0.005 m/s | 0.140 |

These are genuine parameter-domain feasibility results, proved using interval automatic differentiation and all-time checks. They are **not** optimized condition-domain margins, secondary optima or a causal gust policy. The widest radius is only about 0.00972 kt, so this is a small mathematical neighborhood, not operational robustness. A wider ±0.01 m/s enclosure remains unresolved because of interval overestimation.

See [DERIVATION.md](DERIVATION.md) for the complete inequalities, branch equations, evaluated coefficients, local sufficiency theorem and unverified premises, failed approaches and exact remaining gaps.

## Verification and preservation

- **97 core/refinement tests pass**, plus **16 geospatial tests**. Exact commands are in [README.md](README.md); integrity counts are in [verification.json](verification.json).
- All eight original secondary paths now have **continuous** ≤10⁻⁴ local primary-retention proofs; this is stronger than a dense-grid retention check.
- Both additional paths have continuous flight/rollout certificates, independent replay and local secondary completion. Replay position errors are below 9×10⁻¹² m.
- Parent package: all **136 manifested artifacts**, plus its manifest, unchanged. Its **397 prior artifacts and 13 frozen inputs** are independently checked again.
- This additive directory has its own manifest; the sole canonical PROJECT_STATE is appended, not replaced. No old artifact is regenerated.

Parent read-only QA provenance is recorded separately: 136/397/13 hash checks, 85 core tests, 16 geospatial tests, a fresh baseline certificate and the previous 0.191605 exclusion check. Those checks concern the original snapshot; they are not counted as new refinement tests or attributed to this owner.

## Completeness

A-01/02/03/06/07 remain implemented. **A-04 and A-05 remain partial**. The following are still not proved:

- Existence or exclusion of a nonnegative-margin path for tailwind5, urban60 or urban65.
- A matching global family optimum, unrestricted full-class optimizer, or global secondary minimum.
- Exact interval validation of local active-system roots/regularity and a complete active-regime parameter partition.
- The broader historical/feedback/go-around requirements retained in the original study.

Historical certification remains **false**. These are assumption-conditional mathematical results. No new acquisition, login, enquiry, mail, publication, spending, peer sync or agents occurred.

## Deliverables

- [New condition metrics](new_conditions.json)
- [Tailwind3 formula](tailwind3_formula.json), [controls/rollout CSV](tailwind3_path_controls.csv), [verification](tailwind3_verified.json)
- [Urban58 formula](urban58_formula.json), [controls/rollout CSV](urban58_path_controls.csv), [verification](urban58_verified.json)
- [Global family exclusion](strong_bound.json), [continuous wind domains](taylor_domain_refined.json)
- [Coverage](TRACEABILITY.md), [reproduction guide](README.md), [artifact manifest](artifact_manifest.json)
