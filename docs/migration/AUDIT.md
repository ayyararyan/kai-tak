# Repository architecture audit

Read-only discovery completed 13 October 2026, before implementation. Authoritative
baseline: `516bba9537f856d58a4cb440ad57e658dcd2bfcf`, freshly fetched GitHub `main`.
The browser's cached repository page lagged behind GitHub's API and fetched Git refs;
it was not used to decide publication status.

## Inventory and responsibilities

The baseline has **2,439 tracked files, 643,722,593 bytes**. Full path/size/SHA256
inventory: [initial-baseline.json](initial-baseline.json). Counts exclude restored external data,
ignored environments and private material.

| Existing top-level directory | Files | Responsibility and boundary |
|---|---:|---|
| `archive/` | 130 | Independent research-data catalogue, nine collections, rights, schemas, immutable v1.0.0 manifests, preservation/audit records |
| `assets/` | 1 | Existing illustrated cover, not source photography |
| `data/` | 5 | Dated CAL605/source-acquisition inventory, not the universal destination for all restored data |
| `publication/` | 11 | Original snapshot delivery manifests and later publication receipts, not manuscript authorship |
| `research/` | 2,089 | Scientific sources, observations, experiments, accepted and invalidated evidence; includes 638 manuscript-package files |
| `scripts/` | 14 | Shared restoration, archive validation, local candidate building and audit tooling |
| `tests/` | 3 | Archive metadata, policy and hostile-input/no-clobber tests |
| `visual-atlas/` | 181 | Released v1 plates/gallery/source registers/jobs; packed scenes remain external release assets |

Five root files provide homepage, citation, source rights, notice and exclusions.
No CI workflows, project-wide documentation hub or publication index existed.
Local cache/environment directories are not additional architectural pillars.
Three existing worktrees were inspected without changes: main and archive clean;
the separate editorial worktree contains untracked v5 material. Its draft PDF does
not establish publication. See [worktree summary](worktrees-before.json).

## Scientific and publication subsystems

Within `research/checkers-runway13/`:

| Subsystem | Tracked files | Object and consumer |
|---|---:|---|
| `foundations/` | 3 | Finite-roll identities and verification |
| `analytical/` | 40 | Turn/landing derivations, coupled witness certificates, bounds and failed exclusion attempts |
| `approximation/` | 12 | Explicit nominal reference formulas and regression checks |
| `model/` | 7 | Scenario configuration, trajectory dynamics, solver and tests |
| `counterfactual/` | 74 | Separate declared steady-wind landing, certificate and stable delivery aliases |
| `evidence/` | 81 | CAL605 manual readings, clock alignment and NOAA observations; not raw DFDR data |
| `geospatial/` | 22 | Separately dated modern terrain/building comparison and GIS tooling |
| `reconstruction/` | 1,004 | Historical source chronology, obstacle investigation, registration, stereo and scene workbench |
| `integrated/` | 149 | Source-bound geometry, clearance prerequisites, rejected registration, survey and archival follow-ups |
| `literature/` | 4 | Prior-work and contribution assessment |
| `outputs/` | 34 | Retained scientific run outputs, not a disposable cache |
| `reviews/` | 9 | Research criticism and dispositions |
| `whitepaper/` | 638 | Version-specific manuscripts, source packages, frozen evidence, figures and QA |

Other laboratory files hold the canonical model specification, equations,
traceability, changelog, verification, dependency lock and chronological ledger.
The dependency map and ownership rules belong in the new documentation layer;
these scientific authorities remain at their original paths.

## Publication and preservation boundaries

**Latest published paper: v4**, a 35-page formatting-only successor to v3.
`publication/v4_verification.json` pins the publication and accepted PDF hash;
v3 and v4 each contain 104 hash-pinned scientific inputs, all matching during audit.
V1 remains a historical working draft; v2, v3 and v4 retain their published packages.
The local v5 worktree is neither incorporated nor labelled accepted.

All five tags and 22 release assets were inspected through the live GitHub API.
[Release identities, sizes and server digests](releases-before.json) record the exact
boundary. This is metadata inspection; later restoration checks separately test bytes.

| Tag | Commit |
|---|---|
| `snapshot-2026-10-13` | `fd0c0d85b6c514fc7f919542192f18b747f4e092` |
| `update-2026-10-13` | `6178eed1de49f66ac658acf5f5d26fa7e754b9ba` |
| `integration-2026-10-13` | `128f7006e8c929a878bd80bdf84521a97c45ee30` |
| `archive-v1.0.0` | `9f4f7b0cc47b2db0933bd4d20b4e3698f43a465d` |
| `visual-atlas-v1` | `c39008bbdb400e5a0ca25bfb480af85f1b0e6047` |

Archive v1.0.0 has 3,268 catalogue artifacts, 44 datasets, nine collections and
418 permitted-data files in five bundles. Catalogue membership is not permission
to redistribute. Its scientific acquisition boundary predates later manuscripts.
Atlas v1 contains twelve principal 4K plates and seventeen views, with 27 external
scene/asset members. Job absolute paths and source hashes describe the original run.

## Duplication: evidence versus waste

[Initial exact-byte scan](initial-duplicates.json): **220 duplicate groups, 481 additional copies**.
This is a content identity measure, not a finding that 481 files can be deleted.
Most repeated scientific files sit inside self-contained manuscript snapshots;
v4 also retains accepted v3 formatting baselines. Counterfactual stable aliases are
intentional ordinary files. Historical `prior_checkpoint/`, rejected geometry and
invalidated runs preserve failed hypotheses and verification history.

No safe, meaningful active-code consolidation was established that outweighs the
published path/hash coupling. Do not delete these copies or replace them with symlinks.
Consolidate **changing public navigation and version pointers**, not historical
source bytes. New mutable work should use documented ownership and dependencies.

## Path coupling and hidden dependencies

The [path scan](path-risks.json) records 644 line-level candidates: machine paths
and deep relative references, not 644 proven defects. Scientific scripts commonly
assume subsystem CWDs or `Path(__file__).parents[n]`. Shared restoration selects the
historical publication manifest by default, but selects the independent archive
only with `--release v1.0.0`. These are different contracts.

- Manuscript source packages embed evidence and generate QA/PDF/figures in place.
  Rebuild extracted packages, never overwrite accepted trees.
- `foundations/verify_finite_roll.py` writes its verification JSON; run in a copy.
- Atlas jobs contain original absolute paths. Reprepare inputs/jobs in a disposable
  copy before rendering. `verify.py` writes `qa/acceptance.json`; it is not read-only.
- Modern GIS, historical stereo and nominal dynamics require different dependency
  environments. The numerical lock is not a universal installation specification.
- Integrated source checks depend on intentionally excluded originals. Missing
  inputs must not be replaced by empty obstacles or newly generated hashes.
- `archive_package_review.py` creates a private mixed-rights Git-history bundle.
  It is a local preservation tool, not a public-release uploader.

## Documentation and broken-reference audit

[Baseline local-link scan](baseline-links.json) found **337 absent targets among
794 Markdown file references** in a metadata-only checkout. This scan tests paths,
not network URLs or heading anchors. The follow-up validator classifies each
missing path against actual release manifests and publication exclusions.
Examples include restorable meshes/images, restricted scan overlays, unpublished
enquiry drafts, historical copied reports referring to siblings, and a missing
`integrated/HANDOFF_TASK.md`. They are not all repairable by renaming directories.

Current navigation has genuine stale status: the README opens with v4 but later
recommends building/citing v3; `DATA_SOURCES.md` describes v3 as unfinished at its
historical integration checkpoint; v3's frozen README says unpublished. Earlier
ledger sections retain superseded title/publication statements. Preserve frozen
records and explain their date in the new current-status/source-rights pages.
Root `CITATION.cff` is specifically the archive citation, not a paper citation.

The 1,744-line root ignore file largely enumerates release-only and restricted paths.
Its verbosity is intentional protection, not permission to replace it with broad
ignores that conceal new evidence. Add only narrowly defined future working caches.

## Baseline verification and design decision

Before structural implementation: 59 archive tests plus 43 subtests passed;
89 model/counterfactual tests passed; 32,912 metadata checks passed with 2,739
retained provenance/authorship warnings. Initial system-Python attempts lacked
pytest/jsonschema; an isolated validation environment resolved that dependency
problem. Passing metadata does not resolve provenance or prove flight safety.

**Blueprint:** retain every existing scientific/release path. Add `papers/` as the
publication index, a `visual-atlas/README.md` edition selector, `research/README.md`
as the laboratory map, and `docs/` for audience navigation, architecture, status,
reproduction and contribution rules. Keep the already substantial `archive/` as
the fourth product's independent authority. Add an inexpensive validation/command
interface, separate science and release workflows, and a manually requested render
lane. No empty future-version folders, source moves, licence changes or symlinks.

The [per-file migration map](MIGRATION_MAP.csv) covers every baseline path, including
retained paths, immutable status, dependency impact and verification procedure.
No file was moved or deleted during this audit.


## Concurrent upstream publication: second audit, 14 October IST

The first audit above records what actually existed at its timestamp. Before final
handoff, a fresh remote check found four new upstream commits ending at
`78a9ce1c627f917c94306af5529d5e9ebeb743e8`. They publish the assumption-conditional
scientific package and white paper **v5**, then record their public verification.
V5 is now the latest published paper, not a future draft.

The implementation was carried onto a new isolated local branch at that exact
upstream commit. No published branch was merged, rebased, reset or rewritten.
The earlier architecture branch remains available. All 530 added upstream files
were inventoried before incorporating them into navigation; only the upstream
README, ignore rules and append-only laboratory ledger differed among the original
2,439 paths. The migration did not author those scientific/ledger changes.

[Reconciliation record](upstream-reconciliation.json) lists every addition and the
three changed upstream paths. The scientific-publication checkpoint pinned **2,969
files / 768,860,190 bytes** (the final README-only checkpoint is recorded below). The preservation gate protects all 2,967 current originals
except the intentionally redesigned root README and additive ignore rules.
All five release tags and 22 release assets remain unchanged.

### Added scientific and publication boundaries

- `whitepaper/v5/`: 38-page narrative/visual edition, fifteen redesigned figures,
  278-member published source ZIP. Its unchanged foreword retains author-review
  status. Two documentation-only public-package path normalizations are recorded
  in its own publication inventory. Original v1–v4 packages remain unchanged.
- `integrated/aircraft_followup/`: conditional aircraft prerequisites and explicit
  missing-source boundaries, not newly acquired aircraft calibration.
- `integrated/assumption_solution/`, `refinement/`, `local_certificate/`:
  assumption-conditional trajectories and certificates, including strict local
  five-variable / non-strict local twelve-parameter primary optimality. Global
  primary/secondary optimality, full condition coverage and historical clearance
  remain unresolved. Failed attempts and earlier claims retain checkpoint meaning.
- `publication/scientific-results-20261013/`: 235 source/public mappings, 224 sealed
  scientific entries, three original manifests and an explicitly scoped 117-test
  public-copy runner. Normalized public copies are not misrepresented as original
  source bytes. Restricted inputs, private correspondence and runtime material
  remain excluded.

The new current tree has 23 publication-record files and 2,607 research files;
other top-level counts above are unchanged. The [updated duplicate scan](duplicates.json)
finds **235 groups / 609 extra copies**, chiefly frozen evidence across editions.
No copies were deleted. The refreshed [path scan](path-risks.json) records 640
absolute-path/deep-relative candidate lines under its explicit string heuristic;
these are inspection leads, not 640 verified defects. It is not a claim of reduced
path risk relative to the first scan's different candidate rule.

### Newly observed reproducibility issue

V5's later ledger append makes the earlier science publication's exact ledger hash
fail when its original verifier is invoked directly from current main. This is a
real inherited snapshot-boundary mismatch. The strict published verifier and map
remain unchanged. The new science wrapper restores the recorded scientific artifact
commit in a disposable tree, requires current mapped scientific bytes to match
(except the explicitly append-only ledger), and runs the original tests there.
The receipt distinguishes current-tree regressions from historical snapshot proof
reproduction. Future scientific changes cannot silently inherit that old pass.

V5's copied historical evidence adds inherited broken references. They are pinned
to exact frozen upstream source hashes, not exempted because they are new to this
architecture branch. New navigation remains subject to ordinary strict link checks.


### Final README-only upstream checkpoint

A further remote commit `125ebac16dc52a86998e2f6c4893e116bfca67d8` changed only the
root homepage. Its newer 47-degree headline and grand-overview hero are retained in
the architecture proposal; long technical sections are routed to the new guides.
The effective baseline and local review branch now begin at that commit. All 2,967
protected non-homepage/non-ignore originals are identical to the scientific
publication checkpoint, so no scientific rerun was triggered by this prose-only update.
