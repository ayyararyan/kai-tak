# Authorized-scope traceability

The full [request](AUTHORIZED_REQUEST.md) remains normative. IDs correspond to its
numbered sections; no section has been removed or redefined as an optional phase.

| ID | Requirement | Implementation / evidence | State |
|---|---|---|---|
| ARCH-01 | Complete coherent research architecture, not merely a README | Four pillar entries, docs/ARCHITECTURE.md, ownership and maintenance lanes | Implemented; independently reviewed |
| ARCH-02 | Audit latest tree, history, all branches/releases, sources, duplicates, dependencies, rights and local files before edits | AUDIT.md, baseline.json, releases-before.json, worktrees-before.json, duplicates.json, path-risks.json, baseline-links.json | Verified |
| ARCH-03 | Four distinct pillars and protected scientific meaning | papers/README.md, archive/README.md unchanged, visual-atlas/README.md, research/README.md | Implemented |
| ARCH-04 | Simple top-level architecture; preserve canonical locations when safer | ARCHITECTURE.md, per-file MIGRATION_MAP.csv; zero relocated paths | Implemented |
| ARCH-05 | Separate public/research/developer entry routes | Root Discover/Investigate/Reproduce navigation; START_HERE, research map, script index | Implemented |
| ARCH-06 | Restrained homepage, real project image, direct public-product links | Root README; inspected atlas plate 08; browser-acceptance.json | Verified locally |
| ARCH-07 | Actual research dependencies; no false historical-integration claim | RESEARCH_MAP.md diagram and ten source/script/manifest edges; blocked gate output | Implemented and gate verified |
| ARCH-08 | Classify ownership/data/code; preserve intentional snapshots | OWNERSHIP.md, MIGRATION_MAP.csv, duplicates.json; no deleted evidence or symlinks | Implemented |
| ARCH-09 | Independent histories; exact old tags/assets preserved | VERSIONING.md, releases-before/after.json, preservation baseline | Verified |
| ARCH-10 | Short current status and machine-readable index; historical ledgers retained | PROJECT_STATUS.md, project-status.json; v5 latest after verified concurrent publication | Implemented |
| ARCH-11 | Concise docs for start, architecture, reproduction, versions, rights, status, contributions | docs/README.md routes all authorities; frozen docs not duplicated or retroactively edited | Implemented |
| ARCH-12 | Cost-separated automation, tests, metadata/rights/link checks; no false CI claims | scripts/repo.py, repository checks, navigation generator, tests, separate workflows | Implemented and locally tested |
| ARCH-13 | Preserve rights/provenance/privacy, no blanket licence or private uploads | SOURCE_AND_RIGHTS.md, original NOTICE/rights registry unchanged; private correspondence/backup not copied | Implemented and checked |
| ARCH-14 | Controlled audit→navigation→maintenance→boundaries→validation→review | SPEC.md and STATE.md; isolated branch, read-only audit then additive changes | Implemented and reviewed |
| ARCH-15 | Before/after baseline, selected tests, both restoration modes, atlas recovery | Initial 2439/current 2969-file baselines; restoration-results.json; v3/v4/v5 rebuilds; two proofs; 25 atlas sources/27 members | Verified |
| ARCH-16 | Discover/Investigate/Reproduce journey usable by new reader | Root/START_HERE; real local Chromium desktop/mobile checks | Verified locally, not deployed |
| ARCH-17 | Architecture/docs/implementation/validation/handoff artifacts | This directory, four entries, docs, automation, immutable baseline and exact receipts | Implemented, tested and reviewed |
| ARCH-18 | Discoverability, integrity, reproducibility, preservation, sustainability | Browser checks, unchanged science, actual workflow reruns, ownership/versioning/CI boundaries | Locally verified; hosted CI not run |

## Engineering decisions, not scope reductions

- All original file paths are retained because their source/hash/CWD coupling is
  demonstrated in the audit. No compatibility redirects are necessary.
- No safe duplicate scientific/helper consolidation was identified. New shared
  maintenance interfaces and generated navigation consolidate active responsibilities;
  frozen package duplicates remain intentional.
- The user requested appropriate expensive checks and explicit unrun-validation
  disclosure, not every full optimizer and seventeen Blender rerenders on a
  repository-organizing change. These are separated and named in VALIDATION.md.
- Existing scientific/provenance blockers remain open; architecture completion does
  not claim completion of the historical model or all source rights.


## Completion audit

Required sections: 18. Implemented: 18. Partial/not implemented/blocked architecture
requirements: 0. Unapproved scope reductions or scientific substitutions: 0.
Scientific unidentified quantities and unperformed expensive checks are explicitly
retained, not converted into architecture failures or silently marked passed.
Correctness evidence, specification coverage and end-to-end reproduction are recorded
separately in VALIDATION.md. Publication/merge remains a separate author decision.
