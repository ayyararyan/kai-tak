# Requirement traceability

The complete authorized request remains binding. Implemented means the named local artifact/capability exists with referenced evidence; it does not promote unknown rights or lineage into verified facts. Final public acceptance is incomplete.

| ID | Request § | Requirement | Status | Evidence | Limitation |
|---|---|---|---|---|---|
| AUD-01 | 1 | Audit before changes; preserve original evidence | Implemented | audit/INITIAL_AUDIT.md | Initial inventory predates archive layer edits. |
| AUD-02 | 1 | Inspect full Git history, tags, contributors and dirty/untracked/ignored files | Implemented | audit/git_history.json; audit/coverage.json | Seven reachable commits, 34,645 local entries; runtime/private metadata omitted from public inventory. |
| AUD-03 | 1 | Verify all existing remote releases and asset bytes | Implemented | audit/existing_release_verification.json; audit/release_member_reconciliation.json | 12 downloads matched; seven tar member sets reconciled to tag-specific manifests. |
| AUD-04 | 1 | 15-field machine-readable source inventory | Implemented | audit/initial_inventory.json; catalogue/artifacts.json | Unknown fields explicit; mtime not acquisition date. |
| AUD-05 | 1 | Duplicates, broken references, dependencies, missing files and inconsistent claims | Implemented | audit/DUPLICATES_AND_DEPENDENCIES.md; reports/lineage_verification.json | Three v1 frozen-evidence discrepancies preserved, no silent repair. |
| ORG-01 | 2 | Stable nine-collection additive archive layer | Implemented | CATALOGUE.md; collections/ | Original research paths retained. |
| ORG-02 | 2 | Collection landing pages and machine metadata | Implemented | collections/01/README.md through collections/09/collection.json | All nine present; catalogue-only collections explicit. |
| ORG-03 | 2 | Old-to-new mapping without unnecessary duplicate data | Implemented | audit/old_to_catalogue.csv | Navigation mapping, not filesystem relocation. |
| PROV-01 | 3 | Stable dataset/source/artifact IDs and schema | Implemented | schemas/; catalogue/ | SHA identifies bytes; stable ID identifies object/path. |
| PROV-02 | 3 | Exact source URLs/identifiers/revisions/date/CRS/datum/rights fields | Partially implemented | catalogue/sources.json; catalogue/artifacts.json | Available exact acquisitions recovered; many inherited items lack documented metadata. |
| PROV-03 | 3 | Every substantive item has complete source-to-transformation-to-result chain | Partially implemented | catalogue/provenance.json; reports/lineage_verification.json | 2,739 dataset-level/authorship-proposed entries remain; unknown recipes are not invented. |
| PROV-04 | 3 | Distinguish historical observations, publication, acquisition and revisions | Implemented | PROVENANCE.md; catalogue/artifacts.json | Verification dates separated; modern buildings and aerial indexes correctly qualified. |
| PROV-05 | 3 | Result/figure/whitepaper use relationships | Partially implemented | catalogue/publication_usage.json | 11 recovered dataset-to-publication uses; exhaustive figure claims not established. |
| RIGHTS-01 | 4 | Official source/channel-specific terms investigation | Implemented | licensing/RIGHTS_AUDIT.md; licensing/rights_registry.json | 22 investigated rights records plus generic unresolved decision; 25 URL attempts. |
| RIGHTS-02 | 4 | Per-artifact six-way publication classification | Implemented | catalogue/artifacts.json | Physical access, validity and permission kept separate. |
| RIGHTS-03 | 4 | All material has affirmative rights or explicit safe exclusion | Implemented | releases/v1.0.0/manifest.json | 418 allowed bytes; 2,850 explicit exceptions; no blanket grant. |
| RIGHTS-04 | 4 | Resolve every essential source right for a fully reusable archive | Blocked | licensing/rights_registry.json | CAD/AIS/Boeing and historical HKMS routes require permission or authoritative evidence. |
| RIGHTS-05 | 4 | Attribution, ownership acknowledgments and no endorsement | Implemented | licensing/ATTRIBUTION.md | Source-specific disclaimers retained. |
| LIC-01 | 5 | Review original authorship/contributions/dependencies and recommend scope | Partially implemented | licensing/proposed_scope.json; preservation/creators.json | Authorship proposed, not proven for every inherited item; supplied photo contributor unresolved. |
| LIC-02 | 5 | Draft code/doc/data licenses without activating grant | Implemented | licensing/drafts/; licensing/README.md | MIT/CC BY recommended; Apache/CC0 evaluated as alternatives. |
| LIC-03 | 5 | Author-approved final license grants | Requires approval | licensing/README.md | No new license activated; whitepaper grant separate. |
| REL-01 | 6 | Independent semantic archive versioning and immutable-release policy | Implemented | VERSIONING.md; releases/version_history.json | Existing tags retained, no tag reuse. |
| REL-02 | 6 | Deterministic independent collection bundles and master/checksums | Implemented | releases/v1.0.0/manifest.json; reports/deterministic_rebuild.json | Five permitted-data bundles outside Git. |
| REL-03 | 6 | Complete snapshot vs increments and exact dependency boundary | Implemented | DOWNLOAD.md; preservation/README.md | New bundles complete per selected allowed member set; old integration asset alone incomplete. |
| REL-04 | 6 | Change log covering corrections/procedures/licenses/claims/schema/known issues | Implemented | CHANGELOG.md; releases/v1.0.0/RELEASE_NOTES.md | Candidate only; initial failed verification retained. |
| CAT-01 | 7 | Human Markdown and machine JSON/CSV catalogue | Implemented | CATALOGUE.md; catalogue/datasets.json; catalogue/datasets.csv | 44 dataset entries, nine collections. |
| CAT-02 | 7 | Dataset purpose/count/period/coverage/format/verification/rights/citation/limits | Implemented | catalogue/datasets.json | Nulls/qualified unknowns explicit; not invented completeness. |
| CAT-03 | 7 | Practical interoperability standards | Implemented | preservation/schemaorg-datasets.jsonld; preservation/datacite-draft.json | No unnecessary STAC assertion for ungeoreferenced frames. |
| IO-01 | 8 | Extend existing fetch tool with compatible old defaults | Implemented | ../scripts/fetch_data.py; reports/legacy_restore.json | Actual five old assets / 1,254 members restored separately. |
| IO-02 | 8 | List releases/collections, selected/all download, verify-only, local reports | Implemented | DOWNLOAD.md; ../tests/test_archive_io.py | Actual HTTP clean-restore test; public candidate URLs deliberately absent. |
| IO-03 | 8 | Safe extraction, collisions/symlink/path controls, atomic/recoverable writes | Implemented | ../scripts/archive_io.py; ../tests/test_archive_io.py | Fail closed; staged member checks, no conflicting overwrite. |
| IO-04 | 8 | Publicly downloadable new release | Requires approval | PUBLICATION_CHECKLIST.md | Local bytes prepared; no upload/public URLs authorized. |
| SCI-01 | 9 | Correct raw/numerical/synthetic/approximate/unvalidated/invalidated distinctions | Implemented | SCIENTIFIC_STATUS.md; catalogue/artifacts.json | Explicit invalidation flags audited; unresolved budget results not certificates. |
| SCI-02 | 9 | Retain evidence, failures, inconsistencies and no safety/global-optimum overclaim | Implemented | SCIENTIFIC_STATUS.md; reports/lineage_verification.json | No source repairs or historical deletions. |
| SCI-03 | 9 | Establish historical obstacle clearance or survey-grade photogrammetry | Unidentified | SCIENTIFIC_STATUS.md | Not an established result; not required to invent one. |
| CITE-01 | 10 | CITATION.cff, individual citations and contributor records | Implemented | ../CITATION.cff; CITATION.md; preservation/creators.json | Official CFF 1.2.0 schema passed; no DOI invented. |
| CITE-02 | 10 | Concept/version long-term preservation metadata and exact-byte boundaries | Implemented | preservation/ | Draft mappings, not an accepted external record. |
| CITE-03 | 10 | External DOI reservation/deposition/publication | Requires approval | PUBLICATION_CHECKLIST.md | Explicitly unauthorized; no external action. |
| HOME-01 | 11 | Concise welcoming homepage, download/reuse/citation/limits and whitepaper | Implemented | ../README.md | Original paper title retained. |
| QA-01 | 12 | Schema, stable IDs, source/rights/provenance links and version consistency | Implemented | ../scripts/archive_validate.py; ../tests/test_archive_metadata.py | Negative regression fixtures as well as positive checks. |
| QA-02 | 12 | Hashes, sizes, counts, collisions, policy, dependencies and backward paths | Implemented | ../scripts/archive_io.py; reports/installed_validation.json | Actual bundle/restore receipts; no directory-based rights inference. |
| QA-03 | 12 | Geospatial CRS/datum/epoch/missing/geometry checks | Implemented | ../scripts/archive_geospatial.py; reports/geospatial_validation.json | Known 83 invalid geometries retained; no repair. |
| QA-04 | 12 | Metadata-only and installed-data checks; deterministic archives | Implemented | REPRODUCIBILITY.md; reports/ | Unknown historic facts remain warnings, not fabricated validations. |
| QA-05 | 12 | Private/generated file scan and broken source route reporting | Implemented | reports/privacy_review.json; reports/source_link_availability.json | Pattern scan plus scoped inclusion review; not proof against arbitrary encoded secrets. |
| SAFE-01 | 13 | Dedicated branch/worktree, preserve main/history/tags/original dirty files | Implemented | STATE.md; reports/preservation_verification.json | Pinned baseline preserved; concurrent original-checkout drift documented. No push or overwrite. |
| SAFE-02 | 13 | Exact reviewable local work before irreversible public action | Implemented | PUBLICATION_READINESS.md; PUBLICATION_CHECKLIST.md | Local source/support preservation; no external publication. |
| OUT-01 | 14 | Deliverable A: audit/migration/rights/releases/mapping | Implemented | audit/; licensing/ | Actual files, not merely proposed structure. |
| OUT-02 | 14 | Deliverable B: homepage/collections/catalogues/provenance | Implemented | ../README.md; catalogue/; collections/ | Full lineage truth remains partial as PROV-03. |
| OUT-03 | 14 | Deliverable C: rights matrix/drafts/restrictions/approval list | Implemented | licensing/ | No grants made. |
| OUT-04 | 14 | Deliverable D: v1 manifests/checksums/notes/available permitted bundles | Implemented | releases/v1.0.0/ | Excluded/missing items explicit. |
| OUT-05 | 14 | Deliverable E: working tools/tests/reproduction/reports | Implemented | ../scripts/; ../tests/; REPRODUCIBILITY.md | Verified selected outputs, not full historical pipeline. |
| OUT-06 | 14 | Deliverable F: citation/Zenodo drafts/checklist/publication summary | Implemented | preservation/; PUBLICATION_READINESS.md | Submission/deposition not performed. |
| OUT-07 | 14 | Deliverable G: ten-point executive handoff | Implemented | PUBLICATION_READINESS.md | Correctness, completeness and readiness separated. |
| ACC-01 | 15 | Independent discovery/verification/citation/reuse/trust | Partially implemented | PUBLICATION_READINESS.md | Discoverability and honest boundaries implemented; exact full provenance/rights closure incomplete. |
| ACC-02 | 15 | Independent public download/reproduce/preserve complete archive | Partially implemented | reports/clean_restore.json; preservation/README.md | Permitted subset tested locally; public publication pending and full historical dependency closure blocked. |

Status counts: Implemented: 44, Partially implemented: 6, Blocked: 1, Requires approval: 3, Unidentified: 1.
