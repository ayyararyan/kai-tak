# Historical-integration publication — 13 October 2026

This is a dated publication of settled prerequisite research, not completion of the historical landing problem. It adds the integration package and its verified endpoint/datum follow-up. The newly settled archival-record checkpoint is also included. The unfinished v3 manuscript and unsent correspondence remain outside this snapshot. Catalogue metadata identify leads, not acquired drawing/photo contents.

## What changed

- 155 new/changed source files: 150 compact research files in Git and five larger open-data-derived imagery files in a new 14.19 MB archive.
- 88 source-bound scene features, registration and datum diagnostics, whole-body enclosure primitives, physical-calibration audit, 16-row requirement traceability and prerequisite derivations.
- The endpoint interpretation, conditional 61 m extension diagnostic, exact survey identifiers and the complete 5,637-record public 1993 aerial-index query.
- The final archival report, relative-height analysis, 14 exact record identities and a 50-retrieval hash inventory. Publisher independently rechecked all 50 source hashes, all 14 record identities and eight exact-rational algebra checks.
- A catalogue of 61 acquisition records with URLs and recorded checksums, plus file-level exclusion reasons. Counts describe the captured inventory, not an exhaustive search or number of independently validated documents.

The accepted scientific status is still 1 implemented, 10 partial and 5 blocked requirements. No historical clearance, complete obstacle model, hard height bounds or closed-form global optimum is asserted. V1 and V2 manuscript bytes and frozen numerical model remain unchanged.

## Reproduction and tests

Publisher reran the 36 integration tests and seven follow-up tests against the isolated public code copy, with the original excluded primary files supplied locally and the documented numerical dependencies available. All 43 passed. The historical evaluator returned the intended blocked status / exit 2, with all 13 frozen inputs unchanged. This verifies refusal semantics, not historical feasibility.

The initial bare public-copy attempts correctly exposed missing `mpmath` and excluded source-file dependencies. No checks were disabled. The prerequisites were supplied, and the full relevant suites rerun successfully. To reproduce:

1. Install the geospatial dependencies from `research/checkers-runway13/geospatial/requirements.lock`, plus `mpmath==1.4.1` for the new interval primitives. The source README lists additional packages needed by drawing/figure producers.
2. Restore published bulk data with `python3 scripts/fetch_data.py`.
3. For source-bound tests, independently obtain the exact primary bytes identified by `integrated/primary_source_manifest.json` and source observations. The CAD PDF and specified page crops, Boeing manual, current AIP HTML and transformation document are not licensed by this repository. The publication catalogue records their exclusions; original source-hash checks remain intact.
4. From `research/checkers-runway13`, run `python -m unittest discover -s integrated -p 'test_*.py' -v`, then the same command with `-s integrated/followup`. `python integrated/evaluate.py --output /tmp/kai-tak-evaluation.json` is expected to exit 2 until historical prerequisites are established.

The 30 geometry/frame fixture tests do not require restricted source originals; the six source-geometry tests and seven diagnostic tests depend on source evidence. Original source manifests are preserved, including references to files not redistributed. Full source-dependent producer replay is not claimed for an unaided public clone.

All five release archives were read completely and checked for exact membership, safe paths, byte sizes and member SHA-256 values: 1,254 files in total. The four earlier archives are unchanged. Only the new independent integration group needs a new upload.

## Exclusions and continuity

Downloaded originals are not automatically redistributable. Third-party report/manual/chart scans, extracted full text, cached web bodies, detailed aircraft-drawing reproductions, private correspondence drafts, local environments and runtime state remain local. Open Lands Department survey-map/aerial derivatives retain the attribution and terms in `DATA_SOURCES.md` and `NOTICE.md`.

The original local project and the dirty v3 manuscript checkout were left intact. Publication was prepared in an isolated Git worktree. Source and public-copy hashes are recorded separately when local paths/session identifiers were normalized. This snapshot is not automatic ongoing synchronization.
