# Final archive audit — candidate v1.0.0

## Scope and preservation

The nonmutating [initial audit](INITIAL_AUDIT.md) preceded archive implementation. The dedicated worktree/branch is based on `128f7006e8c929a878bd80bdf84521a97c45ee30`. It retains all original research, data, publication paths and three historical tags. Only root presentation, the compatible downloader and ignore rules are changed; the archive layer, support tools and tests are additive.

The audit hashed 34,645 entries across four locations with zero read errors: 1,669 baseline checkout, 1,764 original checkout, 31,189 research workspace and 23 data workspace entries. The public-safe initial inventory has 6,457 location records; 28,188 runtime/private entries remain outside public metadata. Twenty symlinks were identified; none enter new data bundles. The raw private inventory is retained outside Git. Filesystem modification times are not asserted acquisition dates.

The canonical catalogue has 3,268 distinct path identities and 44 dataset groups. Multiple storage copies, differing checksums and embedded ZIP members are recorded separately. Duplicate content is reported, not deleted. The initial publication snapshot accounts for 2,907 files / 4,117,281,199 logical bytes: 1,653 Git research files plus 1,254 files in the five selected historical bundles.

## Historical releases: actual bytes, not URL inference

All 12 assets from `snapshot-2026-10-13`, `update-2026-10-13` and `integration-2026-10-13` were downloaded in full and matched their GitHub SHA-256 digests. Seven tar member sets were streamed, hashed and reconciled against manifests at their corresponding tags. The default five-bundle composition restored 1,254 files using the improved legacy-compatible downloader. The integration asset alone is not a complete source snapshot. No old release or tag was modified. GitHub reported immutable-release protection disabled; policy alone cannot make those existing assets technically immutable.

## Source coverage and rights

227 acquired survey ZIP editions cover 93 sheet locations. They contain 454 hashed TIFF/world-file identities (virtual members, not fictitious extracted paths). There are 48 acquired full DAP-L0 frames and 47 separate previews. The local aerial index has 14,927 records, including 1,277 local 1993 entries; a separate whole-Hong-Kong 1993 query has 5,637 records. These are distinct populations, not frame counts.

Modern building data contain 342,195 features (69,915 in the recorded subset), with revision 2026-09-21. Four structure tables have 168,042 / 53,349 / 54,505 / 24,469 records. Terrain derives from 2014–2015 photography, with 2017 publication / 2019-03 revision, in HK1980 / HKPD. Neither dataset is complete historical 1993 geometry. NOAA annual/day tables contain 8,549 / 24 observations.

22 source-specific rights investigations plus a generic unresolved record distinguish access, attribution, ownership, permission and scientific validity. 25 official-page attempts produced 23 evidence receipts and two failed checks. Current exact-source terms support the selected Lands OpenData survey/DAP-L0, CSDI building, terrain and NOAA channels. Other Lands archives or third-party diagrams do not inherit that permission. CAD/AIS, Boeing, BRAVO, scholarly PDFs, GRS holdings and historical HKMS indexes/previews retain their individual restrictions or unresolved status. No original-work license was granted.

## New candidate and provenance

Five complete collection bundles contain 418 allowlisted files / 1,305,783,427 uncompressed bytes / 824,753,872 compressed bytes. Collection member counts: 01=275, 02=133, 03=3, 05=1, 06=6. Collections 04/07/08/09 are catalogue-only. 2,850 canonical artifacts remain explicit bundle exceptions. Download receipts add four empty-collection notices; their total exception-message count is therefore 2,854, not an alternate artifact count.

The provenance graph includes 714 recovered transformation/version edges and 464 virtual member/version nodes in addition to catalogue attribution edges. Exact evidence supports 400 source/checksum bindings, 14 registered-raster input/output bindings, four byte-identical table reassemblies, two byte-identical weather replays, three analytical semantic replays, 104 frozen-snapshot bindings and two embedded-input hash records. There remain 2,482 dataset-level-only plus 257 authorship-proposed entries. These 2,739 warnings explicitly prevent a claim of complete provenance; the graph does not infer transformations from directory membership.

Three v1 frozen files disagree with their unchanged inherited evidence manifest; five further frozen-source links lack an original source hash and differ from current source bytes. [Lineage report](../reports/lineage_verification.json) names them. Seven explicit analytical invalidations are now accurately classified, while `unresolved_budget_exhausted` is separately labelled unfinished. Original scientific evidence has not been rewritten.

## Verification and remaining failures

See [publication readiness](../PUBLICATION_READINESS.md) and [machine reports](../reports/). Final candidate download, full restoration, verify-only nonmutation, repeated identical restoration, independent deterministic rebuild, installed file verification, NOAA replay, CFF schema validation and geospatial checks passed. Known 83 invalid building geometries and missing-height values remain unmodified. Pattern/inclusion scanning found no undisposed sensitive matches; it is not proof against arbitrary encoded secrets.

Source reachability is not universal: 13/24 probed registry routes answered; 11 failed or remained unverified, including HTTP 403 APIs. Exact downloaded source bytes can be preserved even when a current provider endpoint is unavailable. Full CAD-dependent reconstruction and all historical source reacquisition are not established.

## Concurrent work discovered during final checks

The original checkout advanced independently to a newer main history with white-paper v3 and untracked v4. [Concurrent-work record](concurrent_work.json) hashes the changed tracked files and records the observed head. [Preservation check](../reports/preservation_verification.json) confirms this branch's pinned research/publication/data bytes and historical tags are unchanged but does **not** falsely claim the external checkout stayed unchanged. No reset, rebase, source overwrite or incorporation of an unreviewed moving target was performed. Before merging the archive branch, reconcile newer main presentation and paper discoveries while keeping this data candidate's baseline explicit.

**Overall:** implemented local archival infrastructure and tested permitted-data candidate; complete historical provenance, rights closure and public-release acceptance remain incomplete. Author approvals alone do not repair missing source lineage or establish historical validity.
