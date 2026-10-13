# Data and code ownership

[Architecture](ARCHITECTURE.md) · [Source rights](SOURCE_AND_RIGHTS.md)

Ownership here means **which file is authoritative for maintenance**, not a new
copyright or licence claim. Existing paths remain unchanged. The [per-file role audit](migration/INVENTORY_ROLES.md)
and [migration map](migration/MIGRATION_MAP.csv) separate role, scientific disposition
and preservation boundary for every original file.

| Artifact class | Existing authority / home | Rule for new mutable work |
|---|---|---|
| Original source evidence | Dated acquisition manifests in `data/`, chronology, evidence and geospatial lanes | Acquire once in the responsible subsystem; record source ID, product/channel, date, rights and checksum |
| Immutable archival data | `archive/releases/<version>/` manifests and exact release bundles | New version for changed data; never overwrite a published member or hash |
| Canonical processed data | Subsystem derived outputs, linked to input manifests | One producer-owned result per configuration; consumer records its path/hash rather than making an untracked copy |
| Scientific model source | `model/`, `analytical/`, `approximation/`, `counterfactual/` and reconstruction producers | Keep algorithms beside their specification and tests; shared helpers only after semantic equivalence is demonstrated |
| Derived output | Existing scientific `outputs/`, reconstruction products and atlas renders | Label producer, inputs, parameters, environment and status; generated does not mean disposable |
| Publication snapshot | `whitepaper/v*/`, `visual-atlas/v1/`, published archive metadata | Freeze a complete, ordinary-file package; duplicated evidence can be necessary for independent reproduction |
| Verification receipt | Existing QA/review directories and new migration receipts | Append a new run record; do not retroactively edit an accepted receipt |
| Temporary working artifact | Ignored `.work/`, `.cache/`, virtual environments and existing download caches | Keep outside accepted products; move only reviewed outputs into maintained paths |
| Superseded/invalidated artifact | Existing invalidated/rejected/checkpoint directories | Preserve and label cause, affected claim and successor; never use as an accepted result |

## New experiments

Create a descriptively named workstream under the appropriate laboratory subsystem
only when it has actual work. Its README or specification declares the question,
input identities, assumptions, output roles, state and reproduction command. Use
one state ledger. Keep exploratory and accepted outputs distinguishable in names
and metadata, and record the acceptance decision before a public product consumes them.

Do not create empty `active/accepted/archive/` hierarchies throughout the existing
tree. Existing meanings live in explicit manifests and research state, not merely
directory names. The [laboratory index](../research/README.md) routes those states.

## Copies and dependencies

Prefer stable archive dataset/artifact IDs where available, a canonical path and
SHA256 otherwise. A dependent experiment records the exact identity consumed.
If an immutable publication needs a copy, its source manifest explains the copy.
Never deduplicate across frozen boundaries or use symlinks in release packages.

No scientific duplicate files were deleted or consolidated in this migration.
Only mutable navigation/version references are consolidated into the current-status
index and its generator. The [duplicate inventory](migration/duplicates.json) is
evidence for future decisions, not a deletion list.
