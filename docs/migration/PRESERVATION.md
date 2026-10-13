# Before-and-after preservation

## Two observed upstream checkpoints

The task began at `516bba9537f856d58a4cb440ad57e658dcd2bfcf` with 2,439 tracked
files. The [initial baseline](initial-baseline.json) remains unchanged. Concurrent
publications added the scientific-results package and v5 while the architecture
work was in progress. The final branch starts at freshly fetched
`125ebac16dc52a86998e2f6c4893e116bfca67d8`, with 2,969 tracked originals.

[Upstream reconciliation](upstream-reconciliation.json) identifies all 530 added
paths and exactly three upstream modifications: README, ignore rules and the
append-only research ledger. Of the original 2,439 paths, 2,436 remained byte-identical
across those upstream commits. Those publication changes are not architecture edits.
No upstream files were deleted. The new effective [baseline](baseline.json) preserves
those authorized publications, rather than rolling them back to the initial tree.

## Migration invariants

| Boundary | Before / after |
|---|---|
| Current scientific/publication/source originals | All 2,967 protected files match both recorded SHA256 and baseline Git blob |
| Original locations | Zero moves; zero deleted files; no symlink replacements |
| Intended existing-file edits | Root README redesign and additive local scratch exclusions only |
| Historical tags | All five exact tag commits retained; independently pinned validator |
| Published assets | Five releases / 22 asset IDs, names, sizes and server digests unchanged |
| Papers | All accepted v1–v5 PDF/source bytes retained; v3/v4/v5 builds run externally |
| Archive | Original v1.0.0 manifests, 418 permitted members, rights and attribution unchanged |
| Atlas | Original 25 input identities, 27 packed members, camera/job definitions and source hashes unchanged |
| Historical research | Failed attempts, invalidations, reports and ledgers remain; no failed hash regenerated |
| Other local work | Original main/archive/editorial/publication worktrees not reset or edited |

[Final release readback](releases-final.json) is newly observed API evidence.
[Public artifact readback](public-readback.json) includes actual anonymous downloads
of v4/v5 PDFs and the archive weather bundle. Full legacy/archive/scene restores used
verified ordinary cached bundles, not mocked metadata. [Validation](VALIDATION.md)
records the exact computation and build boundaries.

The per-file [migration map](MIGRATION_MAP.csv) is the old-to-new mapping: retained
locations are deliberate compatibility decisions, not omitted migration work.
