# Kai Tak provenance and scientific-semantics audit

Date: 13 October 2026. Scope: read-only research/source audit; output written only in this scratch directory. The original research trees, data, and public checkout have not been edited by this lane. Licensing and remote-release verification are separate parent-owned tasks. This report does not make redistribution grants or certify external URL availability.

## Delivered records

- `datasets.json`: 35 significant dataset records across all nine requested collections, with stable proposed IDs, path globs/exact paths, source IDs, dependency IDs, producer scripts, evidence records, dates, counts, CRS/datum distinctions, and limitations. All matched paths and named producer scripts exist.
- `sources.json`: 15 source-family records. These are provenance records, not completed rights decisions.
- `artifacts.json`: 1,074 actual local artifacts, totaling 2,328,127,703 bytes by unique local path, with fresh SHA256, size, existing-public-checkout presence, historical snapshot identity and dataset membership. This is a significant-dataset subset, **not** the parent's comprehensive repository inventory; overlaps between collection views are intentional and do not imply duplicated release payloads.
- `source_accessions.json`: each of 227 historical map editions and 48 acquired DAP-L0 frames. All 275 original acquisition size/hash identities freshly match local bytes. The map accessions include fresh hashes and sizes for 454 extracted TIFF/TFW members; no source archive was extracted over evidence or altered.
- `structure_acquisitions.json`: 119 metadata/count/ID/page artifacts from four official tables; source endpoint, table, original acquisition timestamp, expected and actual hash/size. All 119 match.
- `publication_usage.json`: eleven dataset-to-white-paper-v2 section/figure relations with actual LaTeX labels. Frozen v1 and v2 evidence are separate datasets, not treated as current project-state copies.
- `verification.json`: observed counts and scoped checks.
- `noaa_replay.json`: fresh isolated replay and test evidence; `replay/` is disposable audit scratch, not a proposed public artifact.

## Data quantities and meaning

| Collection | Significant evidence | Interpretation boundary |
|---|---|---|
| 01 | 72,691 whole-HK survey-index rows; 18,440 AOI entries; 227 acquired editions over 93 sheet locations | A map edition date is not each depicted object's survey date |
| 01 | 14,927 AOI aerial-index rows (1985–1998), including 1,277 in 1993; separate all-HK 1993 query has 5,637 entries | Index records are not downloaded photographs; separate scopes must never be summed as unique frames |
| 01 | 48 acquired full DAP-L0 frames; 47 additional previews recorded | DAP-L0 compressed 3000px images are not calibrated high-resolution film scans |
| 02 | 342,195 modern building polygons, 69,915 local; release revision 2026-09-21 | Not a complete 1993 census or historical roof model |
| 02 | Four documentary tables: 168,042 / 53,349 / 54,505 / 24,469 records; 221,383 resolved evidence paths | Multiple links are not independent historical buildings; no additional vanished identities beyond modern universe |
| 02 | 45 inspected faces / 15 named forms; 23,801 automated matching pairs | Faces may be partial/aggregate; all broad candidates remain identity-unverified |
| 03 | 122,422,351 5m DTM cells (12,751 × 9,601), source photography 2014–2015 | HKPD elevations, not 1993 terrain; some vegetation/bridges included |
| 04 | 226-page accident report; 123 final-phase and 67 approach chart anchors; 273 interpolated trace rows | Not raw DFDR or routine successful-flight data; A/B/UTC clocks distinct |
| 05 | 8,549 annual NOAA records / 24 event-date rows; 225 wind-printout direction/speed pairs | Preserves missing/suspect fields; station wind is not recovered aircraft-local gust history |
| 06 | 1,318 sparse / 171,307 dense stereo points; 225,371 mesh triangles and 155,891 vertices | Conditional 2 Nov 1993 surface, not survey-grade complete geometry; only 3,780 dense points inside map-control hull |
| 07 | Synthetic scenarios, restricted proofs, calm-air and steady-wind interval certificates | Feasibility within declared model, not global optimum or operational safety |
| 08/09 | Seven v2 figures, 30-page v2 paper, preserved v1 and frozen evidence | Working research, not peer reviewed; manuscript rebuild is not full data/solver reproduction |

Fresh CSV row counts independently match the survey index, AOI frame index, annual/event NOAA, sparse/dense stereo and wind-pair totals. Other totals above are scoped recorded reports/metadata, not newly replayed scientific derivations.

## Fresh reproducibility result

Copied only the NOAA decoder, tests, source-format PDF and pinned 1993 gzip to an isolated scratch layout. Ran `python3 decode_noaa.py` and `python3 -m unittest -v test_decode_noaa.py`: exit 0; twelve tests pass. Both regenerated CSVs are byte-identical to the retained research outputs:

- Annual: `104b2fc2e2e7cdf3ebb2cda338dfebac948a76f95630595242ececf0ce14ef4c`
- 4 November: `ee619b6c154678b69b197e0ad5205704255d28682f5904aefe08f84093abc01b`

This proves the selected deterministic decode from these local source bytes. It does not newly validate historical station siting, meteorological truth, all other research pipelines, or remote clean-checkout delivery. The source-format PDF is a runtime dependency even though the decoder is stdlib-only, because the producer hashes it in its report.

## Required distinctions and preserved failures

1. **Modern versus historical geometry.** `BaseHeight` and `TopHeight` are elevations above HKPD; adding TopHeight to DTM is wrong. There are 104,847 missing tops / 106,249 missing bases and 83 invalid source geometries. Null and invalid geometry evidence must remain visible. The source `DateCreate` is not construction date.
2. **Date conflict remains raw.** 52,552 works records labelled OP Date fall in 2019/2020; 52,202 CSUIDs disagree with linked permit-table dates. The source audit inspected individual official responses. Both values and contradictions remain; this archive must not "clean" them by choosing a convenient date.
3. **Stereo vertical datum.** Stereo Z is relative to a fitted local park/road plane, not HKPD, MSL or each building's base. RMS alignment 5.754m is a local horizontal holdout diagnostic, not hard absolute XYZ error. Camera/scan assumptions and extrapolation prevent survey-grade claims. Focal/principal-point ranges are sensitivities, not confidence intervals.
4. **Invalidated outputs are useful evidence.** Keep `invalidated_dense_lr_blend/` and global-exclusion failures clearly marked. The stereo repair removed 49 exported dense samples. Bounds 0.10, 0.05, 0.04 and 0.03972 from invalidated global-search runs cannot enter accepted scientific summaries. The current calm-air bracket is 0.0397 ≤ eta* < 0.1559772 for the finite family, not an identified optimum.
5. **Flight digitization is not raw recorder data.** The report-derived images/anchors and interpolation require their original hashes and chart calibration. A 273-row derived trace is not 273 independently observed recorder points. A/B clock datums and wind-clock alignment must remain explicit.
6. **Synthetic certificates remain synthetic.** Current geometry/aircraft/physics inputs do not establish complete historical obstacle clearance, causal accident prevention, universal gust robustness, global near-optimality or aviation safety. The integrated owner retains 16 requirements: 1 implemented, 10 partial, 5 blocked; optimum is null.
7. **Runway discrepancy meaning.** 77.62–81.54m compares directly imaged threshold to LDA back-projection from a selected physical pavement endpoint; it is not disagreement between two surveyed thresholds. The possible 61m offset remains an unaccepted endpoint hypothesis.
8. **Archival lead ≠ acquired evidence.** Drawing 115-93A/folder 404 Part II/plates 72998–73001, photography 5 November 1993, are identified in the report but control schedule and original plates are not acquired. GRS finding-record titles identify potential evidence, not its numerical content or target-day presence.

## Reproducibility gaps and dependencies

- Original CAD PDF and 16 derivative extract files exist in local source tree but are absent from public checkout and prior included manifest. Flight/rollout/wind reconstruction therefore needs separately permitted pinned source bytes; do not promise all pipelines from metadata-only clone.
- Full map and photo sources live in existing chronology release bundle, not compact Git checkout. New per-collection bundles must preserve dependency relationships (maps → registration → faces/stereo), independent of display collection placement.
- The historical science is incomplete even if packaging is correct: no complete target-date obstacle solids; unknown heights/datum tie and calibrated aircraft envelope unresolved; no raw normal-flight comparison dataset.
- The white-paper package is a frozen manuscript reproduction, whose nested original imports may expect wider paths. Keep frozen source hashes and frozen-public hashes distinct; never substitute current ledger for frozen evidence silently.
- Counterfactual stable files in the original tree may resolve through `current_bundle` symlinks. Proposed archive extraction should not create arbitrary links. Resolve only audited contained targets for packaging, pin bytes, and preserve an explicit logical-path map; do not alter original link structure.
- Original scripts use separate dependency locks for numerical and geospatial environments; stereo also carries `requirements_stereo.txt` and local `python_deps/`. Virtualenvs, vendored compiled binaries and caches are runtime material, not automatically original research or portable dependencies.

## Publication/privacy hazards

- Unsent `REQUEST_DRAFTS.md`, `LANDS_ENQUIRY_DRAFT.md`, `CAD_ENQUIRY_DRAFT.md`, session/download response caches and internal review scratch are not publication artifacts. Preserve private originals; omit from proposed new release bytes.
- Existing ledger records an obstacle `reviews/change_snapshot.txt` previously committed, later removed from current tree. Do not promise erasure from Git history; history rewrite is not authorized.
- Current snapshot still lists counterfactual `reviews/change_snapshot.txt` and numerous logs. Those need explicit content review before inclusion; a log filename alone is not evidence of a credential leak. Existing `A36143_l0_download_result` is binary JPEG despite extensionless name, not a JSON session response; classify by file content, not its name alone.
- A targeted current-checkout text scan found no `/Users/<name>/`, `agent:main:`, common private-key header, bearer-header or token-pattern hits in scanned .json/.md/.txt/.html/.py files up to 10MB. This is bounded screening, not a full secret-clearance claim; large/binary/extensionless artifacts and all Git history were not covered by this scan.
- Embedded source pixels in plots/viewers retain their source rights; "authored HTML/figure" must not be used to launder image redistribution. The local report PDF, Boeing source documents, scholarly PDFs, portal HTML/previews and official open-data channels require distinct source-specific decisions.
- No license approval is implied by these records. The archive can catalogue restricted items as metadata/link-only while clearly marking unavailable reproduction inputs. Author grants remain pending.

## Integration guidance

Prefer the supplied exact paths and globs over directory-name-only classification. Resolve frozen `whitepaper/v1/evidence/` and `whitepaper/v2/evidence/` first, before matching generic underlying subject categories. A file can legitimately serve multiple collection views but should have one immutable artifact identity. `source_accessions.json` is the strongest available granular source mapping for maps/photos; `structure_acquisitions.json` covers raw table pages; producer manifests and `publication_usage.json` complete the source → derived → claim chain without inventing independent scientific validation.
