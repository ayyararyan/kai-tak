# Initial repository audit — before archival implementation

Audit date: 2026-10-13. Target: ayyararyan/kai-tak. Remote baseline: 128f7006e8c929a878bd80bdf84521a97c45ee30. No source evidence has been moved, renamed, normalized or deleted. A separate archive/v1.0.0-preparation worktree was created from the remote baseline; the original dirty main checkout remains untouched.

## Scope and evidence

Inspected README.md, DATA_SOURCES.md, NOTICE.md, publication/snapshot_manifest.json, release_assets.json, integration_source_inventory.json, INTEGRATION_UPDATE.md and scripts/fetch_data.py. Enumerated every file in both local checkouts and the source research/data workspace, excluding Git's internal object database; inspected Git's complete seven-commit reachable history, three tag references, branch state, contributors and all three GitHub release records. Git history remains the preservation source for earlier README/artifact versions.

The initial machine inventory contains 34,645 entries: remote-baseline checkout 1,669; dirty local checkout 1,764; research workspace 31,189; acquisition workspace 23. This includes 27,991 environment/cache entries and 20 symbolic links. No read errors. Symlink hashes explicitly hash the link text, not the referenced bytes. Filesystem modification times are not acquisition dates. Unknown creator/date/rights/transformation fields are null or explicitly unclassified, not guessed.

Current snapshot manifest: 2,907 research files, comprising 1,653 Git-delivered files and 1,254 files in five selected archives. All 1,653 Git-delivery sizes/hashes match the baseline checkout. Manifest logical bytes: 4,117,281,199. Root project/publication files are additional to that research manifest. Original v1/v2 manuscripts exist. Unfinished v3 and a dirty project ledger exist only in the other local checkout and are not publication-approved.

## Releases and history

All three release records and their assets exist on the live GitHub API: snapshot-2026-10-13, update-2026-10-13, integration-2026-10-13. Three tag targets verified via git ls-remote. GitHub marks all three releases immutable=false. They must not be modified or reused; future archive-series immutability requires publication configuration and persistent deposition, not merely a tag name.

Full remote-byte downloads and archive-member hashing are underway in a separate audit cache. This initial report does NOT yet certify every remote asset's bytes; the final existing_release_verification.json will report completion/failures per asset. Existing local archive copies and their symlink selections have been enumerated. The latest five-group manifest composes chronology/geospatial from the initial snapshot, reconstruction/supporting from the update, plus the independent integration group. The integrated-data asset alone is not a complete snapshot.

## Dependencies, duplication and integrity

Content duplicates are recorded by SHA-256 across storage roots; none are deleted. Frozen white-paper evidence intentionally duplicates some research outputs. There are 1,158 Python import records, one machine-absolute path literal, and 193 Markdown references unresolved in the metadata-only checkout; these are candidate issues, not all broken links (bulk/restricted dependencies are absent by design). Multiple separate environment locks exist. mpmath versions differ among historical lanes. The user must not be told one numerical environment reproduces the whole reconstruction.

The existing downloader validates archive/member hashes and rejects unsafe members, but lacks collection/release discovery, a local integrity report, complete upfront destination-conflict validation and explicit restricted-dependency reporting. Legacy five-group behavior should be retained while adding a separately versioned archive mode. Strengthen temporary-file and symlink handling and test adversarial archives.

## Provenance and scientific distinctions

1993 is the intended reconstruction epoch, not the vintage of every dataset. Modern building/terrain files cannot certify historical geometry. Aerial index records are not acquired full photographic frames. Manually digitized CAD traces are not raw recorder samples. Conditional stereo geometry is not survey-grade HKPD geometry. The synthetic flight results do not establish historical obstacle clearance, global optimality or operational safety. Preserve invalidated analytical/stereo results with explicit status.

A fresh isolated NOAA decoder replay reproduces the 8,549-row annual table and 24-row event table byte-for-byte and passes 12 tests. This is bounded reproducibility evidence, not validation of other scientific lanes. Further source-specific catalogue records and dependencies are being assembled before release selection.

## Rights and privacy

No original-work blanket license exists. Git records two contributor identities: Aryan Ayyar and Induj1; the latter changed the README photograph. Photograph provenance/permission cannot be inferred from contribution or public visibility. No new license may cover it automatically. Original-code authorship and dependency scope need explicit approval before a grant.

Fresh official-term inspection confirms specific open-data distribution routes for historical survey sheets, DAP-L0 compressed photographs, DTM and CSDI buildings, subject to source terms/attribution. This is not permission for every government file. CAD/AIS, Boeing, scholarly PDFs and private building records remain restricted/link-only; API index/preview routes need separate decisions. Detailed verified source scope belongs in the rights register.

Private queue/session state, drafts/correspondence, local environments, machine paths and third-party source documents remain in the original workspace. Detailed private audit inventory is kept outside Git. Public catalogue entries will redact operational/private values, retain source identifiers/checksums where appropriate, and default unresolved rights to metadata-only. New draft licenses must explicitly say they are not grants.

## Migration decision and gate

Proceed with a non-destructive archive/ layer: stable nine collection IDs, source/dataset/artifact IDs, schema-validated catalogues, file-level rights decisions, explicit provenance links, scoped draft licenses, release manifests and deterministic collection bundles. Preserve existing research paths and all old publication manifests. Replace only the archive-facing README and extend fetch_data.py compatibly. Do not modify scientific calculations or source bytes.

Initial audit gate satisfied by this report and the machine inventory; outstanding verification is explicitly recorded above. The final audit supplement must reconcile remote bytes, source rights, missing references and publication exceptions before any readiness claim. Public push/release/deposition and new licensing grants remain unauthorized.
