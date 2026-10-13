# Architecture migration state

Objective: complete the [authorized architectural request](AUTHORIZED_REQUEST.md)
without changing science, frozen artifacts or published release identities.

- Status: implemented, locally validated and independently reviewed; local handoff.
- Initial audit: `516bba9537f856d58a4cb440ad57e658dcd2bfcf` / 2,439 files.
- Reconciled upstream: `125ebac16dc52a86998e2f6c4893e116bfca67d8` / 2,969 files.
- Branch: `architecture/four-pillars-review-20261014`, isolated architecture worktree.
- Specification: [SPEC.md](SPEC.md); audit including concurrent publications: [AUDIT.md](AUDIT.md).
- Phases A–F implemented: audit, navigation, maintenance, boundaries, actual workflow
  acceptance and independent review. Local commit identity is the branch tip containing this file.
- Immutable boundary: all 2,967 current-baseline paths except root README and ignore rules.
- Latest published paper v5; separate conditional scientific results correctly scoped.
- Unresolved scientific/provenance issues remain, as recorded in [HANDOFF.md](HANDOFF.md).
- External push/PR/merge/release actions not performed. Await author publication decision.
- Evidence: [VALIDATION.md](VALIDATION.md), [REVIEW.md](REVIEW.md), [PRESERVATION.md](PRESERVATION.md).

No background monitoring or future automatic publication is promised.


## GitHub branch publication — 14 October 2026 IST

Aryan explicitly authorized “push to GitHub.” Architecture commit
`81a3a9edcf6dc89821fd7a91b61e7936305c977e` was pushed to
`architecture/four-pillars-review-20261014`; remote ref identity and anonymous HTTP
README bytes were freshly verified. Earlier local-only statements above describe
the pre-publication handoff. No PR was opened, no merge occurred, and no release
assets or tags were changed. Main had independently advanced to
`a772db4a0198edfdba5cb3e4c351e3259a554ef8`; this push does not replace or merge it.
Hosted workflow results are separate from branch-publication verification.


## Authorized main merge and README ownership — 14 October 2026 IST

Aryan explicitly requested checking and merging the architecture, with the README
from main retained. Main commit `a772db4a0198edfdba5cb3e4c351e3259a554ef8` is the
merge input. Its README and `assets/runway-allocation.svg` are preserved exactly,
including the author's layout, wording and new diagram. This explicit correction
supersedes the proposed architecture homepage above. The root README is no longer
a generated file; a regression test ensures navigation updates cannot rewrite it.
Product links are still checked without edits. Other guides and generated indices
remain in place. [Merge preservation](merge-preservation.json) records exact hashes.

Earlier browser receipts describe the architecture proposal's homepage, not this
author-maintained main README. Atlas gallery bytes and its browser acceptance remain
unchanged. The inherited direct scientific-snapshot command in the preserved README
retains its ledger-hash limitation; `docs/REPRODUCIBILITY.md` documents the working
snapshot-safe `scripts/repo.py science` route. No README change was made to hide it.


A concurrent author update advanced main to
`58f643681d34d17acadd594485de85f3e8426f7c` during merge verification, adding the
cropped overview image. The merge now retains that newer README and
`assets/kai-tak-overview-cropped.webp` exactly, as well as the runway diagram.
The first checkpoint above remains historical; merge-preservation.json identifies
the final protected input. Main was not overwritten by the earlier candidate.
