# Architecture

[Project guide](README.md) · [Research map](RESEARCH_MAP.md) · [Ownership](OWNERSHIP.md)

Four pillars share evidence, but have different audiences and release contracts.

| Pillar | Public entrance | Canonical implementation | Responsibility |
|---|---|---|---|
| Research papers | [papers/](../papers/README.md) | `research/checkers-runway13/whitepaper/` | Versioned argument, results, manuscripts and self-contained evidence snapshots |
| Historical archive | [archive/](../archive/README.md) | `archive/` plus shared restoration tools | Dataset catalogue, permitted distributions, provenance and rights |
| Visual atlas | [visual-atlas/](../visual-atlas/README.md) | `visual-atlas/v1/` and versioned external scene bundle | Finished visual interpretation, gallery, cameras, rendering and figure provenance |
| Scientific laboratory | [research/](../research/README.md) | `research/checkers-runway13/` | Active mathematical and historical investigations, accepted references and failed hypotheses |

The public indices are intentionally light. A physical move of accepted packages
would break their relative paths and source identities without improving the
scientific system. **No original path is relocated in this migration.**

## Supporting directories

| Directory | Owns | Does not own |
|---|---|---|
| `docs/` | Audience guides, architecture, current public metadata, migration record | Scientific claims or duplicate source catalogues |
| `scripts/` | Shared operational interfaces and archive/repository maintenance | Subsystem scientific algorithms |
| `tests/` | Infrastructure regression/security tests | All mathematical proof verification |
| `publication/` | Historical delivery manifests and publication receipts | Latest paper selection or editable manuscript source |
| `data/` | Original dated acquisition inventory retained at its published path | A forced new home for every restored source |
| `assets/` | Existing project-level cover illustration | Historical source authority or a duplicate atlas library |
| `.github/workflows/` | Cost-separated automated checks | Release uploads, publishing approval or automatic rendering on prose edits |

## Maintenance interfaces

Ordinary edits use repository fast checks: link/asset references, navigation metadata,
Python syntax, archive schemas/policy and lightweight tests. Scientific tests are a
separate lane; the newer source-bound public proof is replayed from its recorded
publication snapshot, with current scientific bytes compared first. Release acceptance adds preserved-byte checks and explicit restored
inputs. Rendering is manually requested and runs in a disposable copy. Detailed
commands and mutating tools are identified in the [script index](../scripts/README.md).

`docs/project-status.json` is the only new mutable cross-product status authority.
Generated marked sections in entry pages eliminate competing “latest” pointers.
The root README is author-maintained and excluded from generation, as explicitly
requested for the main-branch merge. Its links remain subject to read-only checks.
Canonical rights stay in existing rights records; canonical science stays in
specifications and source-bound results. No new universal project configuration
replaces the independently pinned scientific environments.

## Compatibility

The [migration map](migration/MIGRATION_MAP.csv) lists all original paths, retained
destinations, roles, immutable status and validation. There are no redirects or
symlink shims because there are no moves. The old restoration commands, manuscript
ZIP roots, archive collection IDs and atlas scene URLs remain valid.

Historical missing links are itemized rather than made invisible by broad exclusions.
Public readers enter through maintained guides. Researchers can still reach the
original reports and inspect why a source is missing, restricted or unresolved.

For the prior design and evidence behind these choices, see the
[read-only audit](migration/AUDIT.md). For future changes, follow
[versioning](VERSIONING.md) and [contribution rules](CONTRIBUTING.md).
