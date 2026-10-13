---
title: Four-pillar research repository architecture
type: chore
created: 2026-10-13
status: done
baseline_commit: 125ebac16dc52a86998e2f6c4893e116bfca67d8
context: []
---

<frozen-after-approval reason="Aryan explicitly requested the full attached architecture and implementation; no second scope approval required">

## Intent

Make **Checkers with Runway 13** easy to discover, investigate, reproduce and extend
without changing its science or preservation identities. The complete
[authorized request](AUTHORIZED_REQUEST.md) is normative. This is one coordinated
architecture migration, not a scope-limited README redesign.

Organize four pillars: research papers, historical research archive, visual atlas,
and active scientific laboratory. Public entry points can be new indices while
accepted files stay in their canonical historical locations. Inspect the actual
latest GitHub tree, local work, branches, tags and releases before implementation.

## Boundaries

Always preserve all existing scientific bytes, immutable manifests, source hashes,
rights, attribution, accepted PDFs/source packages, historical failures and release
references. New metadata must distinguish published versions from local drafts and
catalogued evidence from permitted downloads. Establish a complete prechange hash
baseline and compare after implementation. Protect unrelated worktrees.

Never rewrite history, force-push, merge, alter release assets/tags, grant a licence,
publish private sources/correspondence, or replace missing evidence with fabricated
inputs. Do not move path-coupled science merely for aesthetics. No symlink-based
deduplication. No new historical clearance, optimality or aviation-safety claims.

Implement phases in order: audit/blueprint; public navigation; maintained-code
interfaces; generated/preservation boundaries; automated and representative actual
validation; final visitor/review acceptance. Record material dependencies and
untested workflows, including blockers that cannot be cured by reorganization.
The deliverable is a locally committed, reviewed migration branch; external
publication and merge await Aryan's authorization.

## Failure behavior

| Input/state | Expected behavior |
|---|---|
| Clean metadata-only clone | Navigation, metadata/schema, path, syntax and lightweight tests work without bulk downloads |
| Missing frozen/restorable input | Explain restoration or restricted-source boundary; never change recorded hash |
| Stale navigation/version pointer | Fast validation fails and identifies the affected path |
| New broken link/private path/blanket licence | Fast validation fails; historical exceptions require exact documented identities |
| Source-preservation mismatch | Fail migration acceptance; restore original bytes before handoff |
| Expensive numerical/scene work | Explicit separate command/workflow, outputs outside accepted trees |
| Local v5 or concurrent main advance | Do not infer publication or silently absorb unrelated work; report divergence |

</frozen-after-approval>

## Code map

- `../../README.md`, `../../papers/README.md`, `../../visual-atlas/README.md`,
  `../../research/README.md`: curated entry points; original product trees retained.
- `../project-status.json`: one machine-readable current public-product index.
- `../START_HERE.md`, `../RESEARCH_MAP.md`, `../ARCHITECTURE.md`,
  `../REPRODUCIBILITY.md`, `../VERSIONING.md`, `../SOURCE_AND_RIGHTS.md`,
  `../CONTRIBUTING.md`: nonduplicated public and technical navigation.
- `../../scripts/`: additive repository validation, navigation generation and
  command interface; existing archive/science algorithms stay untouched.
- `../../tests/`, `../../.github/workflows/`: bounded fast, science, release and
  manually requested visual verification lanes.
- This directory: audit, migration map, baseline, scope traceability, validation
  receipts, preservation comparison, review and final handoff.

## Tasks and acceptance

- [x] A: Complete read-only inventory, release/branch audit, duplicates/dependencies,
  rights/status assessment, baseline and per-file retained/migrated map.
- [x] B: Implement homepage, publication index, four pillar entry points, five-minute
  guide, actual dependency diagram and authoritative current-status metadata.
- [x] C: Clarify all shared scripts and subsystem responsibilities; add a consistent
  safe command interface without mathematically sensitive refactoring.
- [x] D: Define canonical ownership for new mutable work, frozen/generated boundaries
  and precise temporary exclusions. Retain all historical intentional duplicates.
- [x] E: Implement link/anchor/asset/metadata/schema/navigation/licence checks,
  lightweight tests and separate workflow cost tiers; run migration acceptance.
- [x] F: Review reader journeys, preservation and requested coverage; commit a clean
  local migration branch and deliver an explicit remaining-gap report.

Given the baseline, when compared after changes, all protected paths must retain
identical bytes and all five tags/22 release assets must keep their identities.
Given a visitor, when opening the homepage, paper/archive/atlas links must be visible
immediately, with research and reproduction routes one level away. Given status
metadata, generated version navigation must match it and resolve to verified files.
Given duplicate evidence, only changing navigation facts are consolidated; frozen
packages remain self-contained. Given each old restoration mode and atlas bundle,
actual clean restoration must verify exact members/hashes and refuse conflicts.
Given representative scientific tests/builds, before-and-after behavior must match
within the tested domain; an unrun computation must remain unverified, not passed.

## Design notes

The audit establishes that file moves create risk without solving the core problem:
products share source identities but lack distinct navigation and maintenance rules.
Therefore all original paths remain (2,439 initially; 2,969 after verified concurrent upstream publications). Existing root homepage/ignore rules may
change; all other baseline files remain protected for this migration. New files
carry the organization and automation. Historical documentation exceptions remain
dated, exact and inspectable; no broad ignore of new errors.

## Verification

Run repository fast checks; compare every baseline hash; rerun original archive
tests, model/counterfactual and explicit-reference tests; execute two clean data
restorations and packed-scene restoration; run archive metadata/installed checks,
NOAA replay and representative certificate/package build checks. Record commands,
runtime dependencies, exit statuses and unavailable inputs. Inspect existing hero
image and final navigation. Review new automation independently before acceptance.

## Spec change log

Initial implementation scope follows the full explicit request. No scientific
scope changes or exclusions have been authorized.


Concurrent-upstream reconciliation is an implementation correction within the original
latest-repository requirement. The original baseline remains in initial-baseline.json;
the effective baseline now includes actual v5 and scientific-result publication.
No scientific meaning changed. Review repairs strengthen the existing acceptance
conditions for version evidence, exception identity, public paths, inventory roles,
tag preservation, browser/atlas receipts and multi-block navigation updates.

## Suggested Review Order

**Reader experience and meaning**

- Start with the three public products and distinct reader journeys.
  [README.md:1](../../README.md#L1)
- Inspect current evidence and the limits of the conditional theorem.
  [PROJECT_STATUS.md:1](../PROJECT_STATUS.md#L1)
- Follow concrete producer and manifest dependencies.
  [RESEARCH_MAP.md:1](../RESEARCH_MAP.md#L1)

**Preservation and maintenance**

- Review retained locations and ownership boundaries before considering moves.
  [ARCHITECTURE.md:1](../ARCHITECTURE.md#L1)
- Check initial versus reconciled upstream and unchanged scientific bytes.
  [PRESERVATION.md:1](PRESERVATION.md#L1)
- Separate payload role, scientific disposition and publication boundary.
  [INVENTORY_ROLES.md:1](INVENTORY_ROLES.md#L1)
- Inspect fail-closed metadata, link and byte-identity guards.
  [repository_checks.py:1](../../scripts/repository_checks.py#L1)
- Understand current-tree versus historical-snapshot science checks.
  [repo.py:1](../../scripts/repo.py#L1)

**Evidence and supporting checks**

- Read actual workflow results and unrun verification limits.
  [VALIDATION.md:1](VALIDATION.md#L1)
- Inspect regressions for the independently discovered failure modes.
  [test_repository_checks.py:1](../../tests/test_repository_checks.py#L1)
- Confirm cheap checks do not download bulk data or render scenes.
  [repository-fast.yml:1](../../.github/workflows/repository-fast.yml#L1)


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
