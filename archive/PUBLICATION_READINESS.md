> **Verified publication:** [v1.0.0 is public and immutable](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0). All nine assets passed public readback and all 418 data members restored cleanly. [Exact verification receipt](reports/publication_verification.json). The full historical completeness limitations below remain.

# Publication update — 2026-10-13

Aryan explicitly authorized publication of the reviewed archive. **[Data Release v1.0.0](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0) publishes the 418-file permitted-data subset with its limitations intact.** Original-work license drafts remain inactive, and no Zenodo deposition or DOI is claimed. Current main's accepted v3/v4 packages have been merged unchanged; they do not redefine the original data-catalogue boundary. Private enquiries and private source-history backups are excluded. Remote delivery verification is recorded separately after upload.

The following report is the retained **pre-publication acceptance audit**. Its prior authorization/URL/concurrent-main blockers describe that checkpoint, not the current publication authorization. Its unresolved provenance, rights and scientific limitations still apply.

---

# Publication readiness — v1.0.0 candidate

**Verdict: local permitted-data candidate implemented and verified; full archive acceptance remains incomplete. Nothing was pushed, released, deposited or newly licensed.**

## 1. What was reorganized

An additive archive layer on branch `archive/v1.0.0-preparation`, based on `128f7006e8c929a878bd80bdf84521a97c45ee30`, provides nine stable collections, a concise homepage and explicit source/rights/scientific metadata. Original research paths, evidence and old release tags are retained. [Final audit](audit/FINAL_AUDIT.md) · [old-path mapping](audit/old_to_catalogue.csv).

## 2. What exists and in what quantity

The audit hashed **34,645 local entries**. The public catalogue identifies **3,268 canonical artifacts, 44 datasets and 16 source records**; it is not a count of independent historical observations. The new data candidate has **418 files in five bundles**, **824,753,872 compressed bytes** and **1,305,783,427 uncompressed bytes**.

| Collection | Included files | Content |
|---|---:|---|
| 01 Historical maps/aerial photography | 275 | 227 survey ZIP editions and 48 full DAP-L0 photographs |
| 02 Buildings/urban geography | 133 | Source acquisitions, modern feature data and four verified assembled tables |
| 03 Terrain/geospatial | 3 | Permitted terrain/geospatial source and derived records |
| 05 Weather | 1 | Pinned NOAA ISD 1993 source gzip |
| 06 Reconstruction | 6 | Source/output-bound registered rasters; not survey-grade certification |
| 04 / 07 / 08 / 09 | 0 bundled | Catalogue entries, existing Git research and explicit restrictions/approval gates |

The catalogue also records 47 aerial previews separately from full photographs. Modern buildings total 342,195 features, not a complete 1993 reconstruction. More counts and epochs: [catalogue](CATALOGUE.md).

## 3. What has been verified

- **58 automated archive tests:** safe paths/symlinks, collisions, interruptions, policy tampering, transactional candidate rebuilds, schema/reference failures, provenance cycles, published-state guards, dates and scientific invalidation labels.
- **32,910 metadata checks**, then **33,328 installed-data checks**, passed. **2,739 provenance warnings remain**; a passing integrity check does not erase them.
- All five real bundles downloaded via loopback HTTP into a clean baseline checkout, restored **418 exact files**, survived repeat restoration, and passed verify-only nonmutation. [Receipt](reports/clean_restore.json).
- Two independent builds produced identical SHA-256 hashes for every final bundle. [Determinism](reports/deterministic_rebuild.json).
- NOAA decoder: **12 tests**, annual **8,549** and event-day **24** rows; both derived CSVs reproduced byte-for-byte. Three additional analytical producers reproduced their saved values after excluding generation timestamps; their theorem/model scopes are unchanged.
- **13 geospatial checks** matched source counts, CRS, raster coverage and missing values. **83 invalid source geometries remain unchanged**. CFF passed the official 1.2.0 schema.
- All **12 old release assets** matched full-download hashes; seven tar member sets reconciled. Legacy default restoration produced **1,254 files**.

These are local integrity/reproducibility checks, not operational aviation validation or public-host delivery checks. [Reports](reports/) · [review dispositions](reports/REVIEW_DISPOSITION.md).

## 4. What can be redistributed

The 418 included files have exact source/channel bindings to verified Lands OpenData survey/DAP-L0, CSDI building, terrain or NOAA terms. Reuse must retain each recorded attribution, ownership acknowledgment, disclaimer and restriction. There is **no unrestricted repository-wide license**. Source permission does not authorize this agent to publish. [Rights matrix](licensing/rights_matrix.csv) · [attribution](licensing/ATTRIBUTION.md).

## 5. What remains restricted or unresolved

**2,850 catalogue artifacts are not included in the new bundles:** 2,525 rights-unresolved, 308 original-authorship/license proposals and 17 permission-required classifications. Some are already in inherited Git/history; that does not establish a new grant.

Genuine unresolved work includes exact lineage/authorship for 2,739 entries, CAD/AIS/Boeing/BRAVO restrictions, historical HKMS index/preview rights, source-version bytes missing from frozen-paper chains, and three inherited v1 manifest discrepancies. Only 13/24 probed source routes were reachable; 11 failed or remained unverified. Restricted inputs prevent full historical integration/photogrammetry reproduction from these bundles alone. Approval cannot substitute for absent evidence or establish survey accuracy/global optimality.

Separate work advanced the original checkout during this task, including white-paper v3 and untracked v4. This candidate is **not a snapshot of that newer moving state**. [Concurrent-work audit](audit/concurrent_work.json) and [preservation check](reports/preservation_verification.json) record the divergence. Reconcile the branch with current main before publication, without silently changing this candidate's source identities.

## 6. Existing releases preserved

`snapshot-2026-10-13`, `update-2026-10-13` and `integration-2026-10-13` remain unchanged. Their assets were verified, not replaced. GitHub reported immutable protection disabled; no Zenodo preservation was verified. No historic tag was reused for the new archive version.

## 7. Files and tools created

[Catalogues/provenance](catalogue/), [nine collection pages](collections/), [schemas](schemas/), [audits](audit/), [license drafts](licensing/drafts/), [v1 manifests/checksums/notes](releases/v1.0.0/), [CITATION.cff](../CITATION.cff), [preservation drafts](preservation/), [55-row traceability](TRACEABILITY.md), automated tests and `archive_*` build/validation/reproduction/review-package tools. The existing `fetch_data.py` retains historical defaults and adds release/collection selection, verification-only and integrity reports. [Usage](DOWNLOAD.md).

## 8. Can it download and restore cleanly?

**Locally, yes, for the exact permitted candidate and specified replay. Publicly, not yet:** candidate asset URLs intentionally remain null. Complete historical reconstruction is not established. Metadata-only checks need the source checkout and lightweight validation requirements, not the entire data archive. A collection can be fetched independently.

The local review package contains the five data bundles, a metadata/tooling support tar and a verified **private** Git-history bundle pinning the exact archive commit. Support code requires author licensing approval; mixed-rights history must not be uploaded wholesale. Its external `REVIEW_PACKAGE_MANIFEST.json` records exact package hashes and source commit, avoiding a self-referential Git manifest. [Packaging command](../scripts/archive_package_review.py).

## 9. What is ready for publication review?

The catalogue, safe tooling, five source-permitted bundles, exact manifests/checksums, limitation notices, source-specific rights records, CFF and concept/version Zenodo metadata drafts are ready to inspect. They are **not an assertion that all 15 acceptance sections are complete**. Of 55 requirements, 44 local components are implemented, six are partial, one is blocked, three require approval and one historical scientific quantity remains unidentified. [Traceability](TRACEABILITY.md) retains the full scope.

## 10. What requires author approval or further evidence?

1. Confirm original authorship and exact license scope. Recommended: **MIT** for eligible original code; **CC BY 4.0** for eligible prose/figures/data. Apache-2.0 and CC0 remain alternatives, not selected grants. White-paper licensing is separate.
2. Confirm any contribution/image rights; keep unclear material metadata-only unless permission is evidenced.
3. Reconcile concurrent main changes and approve the exact proposed public branch/release set after final review.
4. Separately authorize GitHub publication and, if desired, Zenodo deposition. No DOI is invented or reserved.

Further provenance recovery/source permissions require evidence, not merely an approval tick. [Publication checklist](PUBLICATION_CHECKLIST.md) lists these gates. **Correctness: tested. Local subset restoration: verified. Specification completeness/publication readiness: incomplete.**
