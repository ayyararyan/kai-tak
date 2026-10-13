# Artifact-role audit

The migration map separates **what a file is**, **what is scientifically established**,
and **why its bytes are preserved**. A generated result is not an original observation;
a verification receipt about an invalidated package is not itself an invalidated result.

## Method and limits

The inventory includes the upstream scientific-results snapshot and v5 paper newly
published during the migration; it is not limited to the initial 2,439-file tree.
Every inventory row was reassigned using payload type, subsystem semantics, inspected
producer calls, acquisition records and explicit invalidation declarations. The previous
catch-all `maintained source / technical record` class is removed. Role is navigational:
`processed research data` does not declare a result accepted, accurate or canonical.
An item inside a frozen paper is a `publication snapshot` in the compatibility
classification column, with its actual payload role recorded separately.

- `artifact_role`: source evidence, processed evidence/data, source code, derived output,
  publication document/package, verification record, configuration, documentation or metadata.
- `scientific_disposition` and `scientific_status_basis`: explicit invalidation and
  candidate boundaries where evidenced; otherwise no new acceptance is inferred.
- `recorded_outcome`: selected literal status/certified fields, where present; failures
  remain failures and mixed-domain certificates retain both true and false counts.
- `preservation_boundary`: publication/release/run boundary independent of role. Every
  original path retains its prior migration decision, immutable flag and compatibility rule.
- `producer_or_authority` and `lineage_basis`: exact inspected output calls are distinguished
  from documentary responsibility pointers and catalogue-associated scripts. The archive
  often lists scripts at **dataset level**; those associations are not exact per-file lineage.
- `catalogue_provenance_status`: copies the existing qualified provenance status without
  upgrading it. The map does not make rights, authorship or redistribution decisions.

This is a repository artifact-role audit, not a new scientific validation of every
computation. No tracked historical artifact is labelled disposable simply because it is
a log, failed run, duplicate, intermediate or generated file. There is no deletion list.

## Coverage

**2,969 unique paths classified; zero catch-all roles; zero relocations.**

| Artifact role | Files |
|---|---:|
| configuration / dependency source | 24 |
| configuration / model inputs | 36 |
| derived output | 995 |
| documentation / scientific record | 296 |
| infrastructure source | 15 |
| original source evidence | 6 |
| original source evidence / acquisition metadata | 78 |
| presentation asset (origin unresolved) | 1 |
| presentation source / generated page | 7 |
| processed research data | 315 |
| processed source evidence | 100 |
| provenance / catalogue metadata | 172 |
| publication build source | 35 |
| publication document | 6 |
| publication manuscript / typesetting source | 73 |
| publication source package | 4 |
| schema / contract source | 8 |
| scientific disposition record | 2 |
| scientific model / processing source | 199 |
| scientific status record | 17 |
| verification receipt | 525 |
| verification source | 46 |
| visualization source | 9 |

## Verified semantic spot checks

| Artifact | Evidence and classification |
|---|---|
| `evidence/cal605_reconstruction/explicit_rollout_samples.csv` | `reconstruct.py:87` writes computed samples: derived output, not observed source evidence. |
| `evidence/cal605_reconstruction/findings.png` and `.pdf` | `reconstruct.py:203` saves the figure: derived output. |
| `evidence/cal605_reconstruction/flight/flight_traces.csv` | `flight/build_flight.py:86` writes interpolated rows; the flight README distinguishes 273 interpolated rows from 123 manual anchors. |
| `evidence/cal605_reconstruction/wind/manual_readings.txt` | Wind README identifies checked manual transcription; processed source evidence, not raw telemetry. |
| `reconstruction/block_matching/candidates/invalidated_archive_integrity.json` | Receipt reports 508 matching entries and one explained log mismatch; checks preservation of an invalidated package, not algorithm acceptance. |
| `reconstruction/block_matching/candidates/invalidated/pre_B1_B7_B8_B9/` | Explicit `INVALIDATED.md` governs run disposition; logs/manifests remain records of that run rather than acquiring a different physical role. |
| `reconstruction/block_matching/aerial_registration/invalidated_dense_lr_blend/` | `INVALIDATED.json` explains the invalid disparity interpolation; the declaration itself is a disposition record and the old verification files are historical receipts, not current acceptance. |
| `whitepaper/v4/evidence/model/config.json` | Frozen publication snapshot containing model input configuration, not original source evidence. |
| `integrated/assumption_solution/refinement/branch_domain.json` | Three false certificate flags; unsuccessful enclosure, not a proof of infeasibility. |
| `integrated/assumption_solution/refinement/taylor_domain_refined.json` | Three true and one false flags; preserves mixed condition-domain outcomes. |
| `integrated/assumption_solution/refinement/local_certificate/` | Sealed strict local five-variable / non-strict local twelve-parameter theorem; not a global or historical certificate. |
| `archive/releases/v1.0.0/collections/01.json` | Published archive release metadata, not the distributed raw data payload. |

Paths in this table are relative to `research/checkers-runway13/` except the final
archive row. These examples are checks of the global rules, not the complete audit.

## Mechanical assertions executed

The task-local classification script checked unique complete row coverage, nonempty
role/disposition/boundary fields, existence of the first producer/authority reference,
unchanged original path/action/immutability/dependency/validation decisions, exact current
baseline path coverage and SHA-256 equality for every protected baseline file, seven exact
producer-output assignments, and the invalidated-package integrity receipt distinction.
All assertions passed before writing this report. Scientific source bytes were not edited.

For future new files, assign the independent fields at creation. Unknown lineage should
remain documentary or unresolved until an actual producer/input/output binding is verified;
never borrow acceptance, rights or authorship from a parent directory name.
