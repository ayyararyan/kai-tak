# Versioning and preservation

[Architecture](ARCHITECTURE.md) · [Current status](PROJECT_STATUS.md)

| History | Meaning | Change rule |
|---|---|---|
| White-paper v2, v3, v4, v5… | A manuscript edition with its claims, figures, PDF and source package | New accepted edition; retain every previous package and version-change record |
| Archive v1.0.0… | A data distribution with fixed member identities and rights decisions | New semantic version for corrections/additions; published manifests/assets remain immutable |
| Visual-atlas v1… | A visual edition with cameras, sources, plates and editable scenes | New edition or explicitly versioned correction; preserve original visual/source identities |
| Scientific models | Exact configuration, implementation and accepted result snapshot | Specification/change control for meaning changes; rerun relevant scientific validation |
| Dated snapshots | Historical assembled research state | Preserve original tags, manifests, exclusions and restoration paths |

Never synchronize these version numbers artificially. A paper may consume earlier
data and a visual edition may expose evidence that is not yet clearance-ready.

## Frozen references

The historical tags `snapshot-2026-10-13`, `update-2026-10-13`,
`integration-2026-10-13`, `archive-v1.0.0` and `visual-atlas-v1` are preserved.
Their exact commits/assets are recorded in the [migration release baseline](migration/releases-before.json).
The first three may not be GitHub-enforced immutable releases; this project still
treats their published bytes and identities as preservation boundaries.

Do not rewrite Git history, replace release assets, regenerate failing frozen hashes,
deduplicate evidence across publication boundaries, or move accepted packages.
An error in an old result receives a new correction record with its affected scope;
the old record remains inspectable. Restricted/private sources do not become public
merely because an old manifest names them.

## Preparing a new version

1. Specify the changed object and scope; preserve independent histories.
2. Record source IDs, acquisition channels, rights, hashes and missing dependencies.
3. Prepare a new candidate outside frozen directories; freeze its exact file set.
4. Run fast checks, relevant scientific/build checks, source/asset integrity and
   clean restoration. Inspect figures/PDFs as actual delivered artifacts.
5. Record what was tested and what remains unresolved. Obtain author authorization
   for external publication, licence changes and scientific meaning changes.
6. After authorized publication, verify remote tag, asset bytes and restoration.
   Only then update [status metadata](project-status.json) and regenerate navigation.

For this migration the branch is local and reviewable; no merge, push or release
mutation is implied by completed local checks.
