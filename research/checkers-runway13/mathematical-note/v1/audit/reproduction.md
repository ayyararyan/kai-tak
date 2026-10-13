# Independent public numerical reproduction

**Result:** the unchanged 117 public tests and all requested latest numerical
certificate lanes were freshly reproduced. The exact finite root/simplex
objects were also exported, and the two legacy synthetic witnesses were checked
separately. No numerical optimizer was run, no assumption was changed, and no
inherited scientific artifact or manifest was overwritten.

The scope here is executable verification. It does not replace the manuscript's
analytical reconstruction or the separate adversarial mathematical reviews.

## Source, environment and evidence

- Scientific source commit: `78a9ce1c627f917c94306af5529d5e9ebeb743e8`.
- Accepted source subset: 487 exact files, 34,184,693 bytes, all from that public
  Git commit; [manifest](../frozen-source/PUBLIC_SOURCE_MANIFEST.json).
- Fresh environment: Python 3.12.13, macOS 26.5.2 arm64, with twenty pinned
  packages; [environment receipt](../verification/accepted/environment.json).
- Accepted run began at `2026-10-13T18:54:33.034308+00:00` (14 October IST).
- Final source preservation: all 235 mapped public records (one append-only
  ledger treatment), 224 original source-manifest bindings and three unchanged
  seals; all 610 preservation paths classified as in the public mapping.
- Commands, exit codes and actual durations are recorded in
  [run.json](../verification/accepted/run.json). The legacy stage ran in a
  separate process while the six other stages were executing; summed stage
  durations are not presented as wall-clock duration.

The source subset is intentionally more than the few files needed by the local
root solver: the unchanged public test suite verifies prior source bindings and
preservation history. Its extra files are public provenance dependencies, not
new measurements or restricted originals.

## Verification results

| Lane | Fresh outcome | Exact scope |
|---|---|---|
| Public numerical/core/proof tests | 102 passed; 6 deselected | Original tests unchanged |
| Public geometry tests | 15 passed; 1 explicitly excluded | Original tests unchanged |
| Krawczyk root and Jacobian | Passed | Nine-dimensional scaled box, radius `1e-20` |
| Active-gradient simplex | Passed | Six strictly positive validated multiplier enclosures |
| Active extrema | Passed | Three strictly convex interior margin neighborhoods and two one-sided endpoint neighborhoods |
| Complete exact-root path | Passed | 398 accepted cells, 786 processed cells, plus analytical contact/rollout treatment |
| Baseline secondary retention | Passed | 4,020 processed cells; loss at most `0.0001` relative to the proved local primary optimum |
| Global-family exclusion | Passed | 4,096 spatial cells at `eta=0.181970215` |
| Known-wind parameter domains | 3 passed | Closed along-wind radii `0.001`, `0.002`, `0.005` m/s |
| Condition cases | 10 passed | Fresh all-time operating/geometry certificates and independent numerical replays |
| Legacy synthetic witnesses | 2 passed | Calm and constant-wind V5-model certificates, not A1 |
| Full proof-matrix export | Passed | Interval objects match original offsets and weights exactly |

No selected test was skipped. The seven exclusions are **not passes**:

1. `test_parent_snapshot_unchanged` and `test_preserved_packages` require the
   original complete workspace and unnormalized original bytes.
2. Four source tests in `integrated/followup/test_diagnosis.py` require restricted
   originals: `test_control_influence_not_silently_deleted`,
   `test_hypothesis_remains_unaccepted`, `test_pythagorean_residual_decomposition`
   and `test_source_residual_reproduction`.
3. `test_source_observations_hashes_and_unknown_fixdatum` requires restricted
   source inputs.

No restricted-input test was rerun with a private fixture in this assignment.
The historical 124-test original-workspace count is not the public test count.

## Principal quantitative objects

The exact local root is specified by the accepted nine decimal centers and the
scaled-coordinate radius `1e-20`, not by a rounded candidate vector. Its outer
objective box is

```text
0.152360764301861701908625206455836893973748530913
0.152360764301861701928625206455836893973748530913
```

The stated family lower bound `0.15236076430186170190` is below the first
endpoint. The freshly reproduced exclusion at `0.181970215` has a displayed
minimum residual of `0.9678323903412959` m. This is an unmatched global-family
bracket, not a global optimizer certificate.

The complete-path partition contains **32 approach cells and 366 flare cells**.
“398” counts accepted leaf cells, not point evaluations, not the 786 processed
nodes, and not 398 separate landings. The closed cells cover each normalized
phase interval from zero to one with no gaps. Active neighborhoods omit only
their separately proved active margin; all remaining margins and geometry
predicates are interval-checked. The ideal contact transition and straight
rollout are handled analytically by the source proof.

The unchanged baseline secondary path is newly certified at

```text
0.152260764301861701928625206455836893973748530913
```

Subtracting this value from the certified **upper** endpoint of the local
primary box gives exactly `0.0001`. This establishes a retention property,
not secondary-effort optimality. Independent Newton replay of the rounded root
center passed; the numerical replay is not a representation of the exact root.

### Full interval matrices

[local_matrices.json](../verification/final/local_matrices.json) contains the
entire interval Jacobian at the center and over the root box, exact 48-digit
decimal preconditioner inputs, `I-CJ`, center residual and Krawczyk offset, the
6-by-6 augmented gradient matrix, its preconditioner and residual, and all
multiplier intervals. The original `bounds()` strings are retained. Exact binary
endpoint tuples are included to avoid treating rounded decimal displays as
exact machine interval endpoints.

The exporter checks these additional conservative decimal inequalities directly
in interval arithmetic:

```text
||I-C J(X)||_infinity < 2e-14
max |Krawczyk offset| < 2e-34
||I-C_A A||_infinity < 2.5e-14
min multiplier > 0.0009658
```

They are new verification records for existing finite objects, not new roots,
optimization experiments, or larger local-optimality neighborhoods. Root
isolation radius, Taylor-sufficiency neighborhood, active-time neighborhoods
and certified wind domain must remain distinct.

### Wind domains and sensitivity

| Radius of known along-wind perturbation (m/s) | Certified margin | Accepted cells | Processed cells |
|---:|---:|---:|---:|
| 0.001 | 0.149 | 262 | 522 |
| 0.002 | 0.147 | 243 | 484 |
| 0.005 | 0.140 | 182 | 362 |

These are interval certificates for the explicit affine decision rule with
endpoint velocities recomputed for the prescribed constant wind. They are not
a feedback policy for unobserved gusts. The source sensitivity
`deta/dwx = -0.018003131684724366` per m/s is **numerical**, checked by the
published centered re-solves but not rigorously enclosed. No new sensitivity
root solves were conducted here. The unsuccessful wider `0.01` m/s domain
attempt remains unresolved; it was not rerun or relabelled infeasible.

### Ten accepted condition points

The entries below reproduce the stronger delivered-secondary certificates in
the refinement package. They are feasible-path lower bounds. The separate
baseline local-root and stronger baseline-retention results above are not
silently substituted for the delivered trajectory in this comparison.

| Condition | Exact certified margin string | Accepted cells | Processed cells |
|---|---:|---:|---:|
| Baseline mean wind | 0.15225866725206007 | 1,989 | 3,976 |
| Calm | 0.039021289592747265 | 1,564 | 3,126 |
| 10 kt headwind | 0.1462028910807011 | 1,636 | 3,270 |
| 2 kt tailwind | 0.016768057530118538 | 1,598 | 3,194 |
| 3 kt tailwind | 0.00554748408841633 | 1,571 | 3,140 |
| 15 m horizontal buffer | 0.1522586672517442 | 1,989 | 3,976 |
| 45 m urban blanket | 0.1522586672517442 | 1,992 | 3,982 |
| 50 m urban blanket | 0.1522499864636599 | 1,986 | 3,970 |
| 55 m urban blanket | 0.09943667248032322 | 122 | 242 |
| 58 m urban blanket | 0.011876478604716387 | 1,476 | 2,950 |

The eight original retention comparisons evaluate an upper bound on the
continuous minimum of each stored numerical primary path and a continuous lower
bound for its delivered secondary path. They do not prove that those stored
numerical primary paths are optimizers. Only the separate baseline local-root
certificate supplies the corresponding local primary theorem.

The 5 kt tailwind, 60 m urban and 65 m urban targets remain unresolved. Freshly
checking the stronger bound at zero margin for the 5 kt tailwind does not
exclude it. A failed bound or a failed local optimizer is not infeasibility.

## Failures discovered, diagnosis and repair

| Finding | Effect | Additive repair and evidence |
|---|---|---|
| The inherited public runner rejects current `PROJECT_STATE.md` | No tests collected in the first attempt | Original ledger prefix has the exact old hash; full current ledger separately pinned. `verify_public_inputs.py` makes this explicit, leaves all source code/seals unchanged. [Original failure](../verification/initial-public-runner-failure.log). |
| Generated bytecode occurs in the shared checkout | Historical exclusion list rejects a runtime cache path | Clean Git-derived source subset plus `PYTHONDONTWRITEBYTECODE=1`; no caches deleted and no exclusion waived. [Failure](../verification/initial-cache-presence-failure.log). |
| Initial subset omitted the old counterfactual input-manifest dependencies | 7 tests failed with missing-file errors; 95 passed | Included every public `counterfactual/inputs.json` source binding from the fixed Git commit. All 117 public tests subsequently passed unchanged. [Failed attempt](../verification/initial-subset-failure.log). |
| Initial new legacy wrapper lacked the counterfactual module search path | Legacy wind replay failed to import `calculate`; calm passed | Corrected only the additive wrapper's path initialization. Both original certificates now reproduce. [Failed attempt](../verification/initial-legacy-import-failure.log). |

The first defect is inherited publication orchestration, not a mathematical
certificate failure. The last two are preparation defects in this new
reproduction package. None was repaired by editing an old proof, reducing a
constraint, changing a certificate target, or counting an omitted test as a pass.

## Reproduction and remaining boundaries

Use the commands in [verification/README.md](../verification/README.md).
The frozen subset makes the result reproducible without the original private
workspace. The old unrestricted source verifiers still correctly refuse the
incomplete public tree; this delivery does not pretend otherwise.

These checks verify the declared computational enclosures and their source
bindings. The local-optimality implication, compactness/domain qualifications,
and transfer to twelve variables require the written mathematical arguments and
their separate reviews. Physical calibration, historical scene validity,
unrestricted-class optimality, global family optimality, global secondary
optimality and the unresolved conditions remain outside the positive result.
