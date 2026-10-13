# Archive task state

Canonical specification: ARCHIVE_SPEC.md; full normative request: requirements/AUTHORIZED_REQUEST.md.
Branch: archive/v1.0.0-preparation. Audited baseline: 128f7006e8c929a878bd80bdf84521a97c45ee30.
Authorization: local audit, implementation, testing and local versioning only. No push, release, DOI/deposition, license activation or outreach.

## Current verified state

Local catalogue: 3,268 canonical artifacts, 44 datasets, 16 sources, nine collections. Five deterministic permitted-data bundles: 418 files, 824,753,872 compressed bytes. Final clean HTTP restore and isolated NOAA replay passed; installed validation 33,328 checks; 2,739 provenance warnings retained. 58 archive tests and 13 geospatial checks passed. All 12 old release assets verified, original three tags unchanged. Full report: PUBLICATION_READINESS.md.

## Honest remaining scope

Full acceptance INCOMPLETE: 2,739 incomplete item-level provenance/authorship records; mixed-rights and permission-dependent sources; incomplete frozen-source versions and three inherited manifest discrepancies. Original-work grants and external publication require author approval. Newer work advanced the separate original checkout (v3/v4); this candidate remains baseline-pinned. Reconcile current main before any merge/public release, without silently overwriting its research or changing this release's identities.

## Local handoff

Large final bundles, acceptance checkout and review package live outside Git in the task's local handoff directory. The local review package manifest records the exact final archive commit and hashes. Its Git-history bundle is PRIVATE preservation, not a proposed public upload. Repository files and code are locally committed only; consult git HEAD and the package manifest for exact identity.

Next authorized step after this handoff: none requiring external action. Await concrete author license/publication decisions; missing source permissions/provenance remain evidence-dependent blockers, not automatic approvals.
