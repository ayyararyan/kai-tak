# Official documentary structure chronology

**Acquired and run 13 October 2026. CLASS-01 documentary lane implemented and verified; historical image matching and city reconstruction remain incomplete.** This package classifies every one of the **342,195 current building polygons** in the September 21, 2026 source snapshot. The Kowloon/Kai Tak acquisition rectangle contains **69,915** of them. These are polygon/CSUID counts, not counts of independent buildings or historical buildings ever constructed.

## What the example date establishes

Example query: **1993-11-04**. The date is selectable; it is not a restriction to a single historical period.

| Evidence measure | Whole Hong Kong current polygons | Local acquisition rectangle |
|---|---:|---:|
| Current polygons classified, including unresolved | 342,195 | 69,915 |
| At least one linked documentary event | 71,382 | 29,082 |
| Some recorded completion or occupation permit on/before example date | 35,540 | 21,746 |
| Direct CSUID-linked completion on/before date | 35,314 | 21,575 |
| Completion date also agrees with a relational OP date on/before date | 34,387 | 21,066 |
| Only later completion/permit evidence; earlier presence unresolved | 19,588 | 6,562 |
| Administrative/undated evidence only; presence unresolved | 16,254 | 774 |
| No linked chronology; historical presence unresolved | 270,813 | 40,833 |
| At least one date/identity conflict flag, regardless of target date | 52,239 | 26,743 |
| Structure-level historical visual checks in this lane | 0 | 0 |

**Completion by a date does not establish continued presence at that date, or unchanged footprint/roof height.** Every non-demolition 1993 result keeps `presence_at_target_unverified` and every geometry keeps `historical_geometry_status=unverified`. No current polygon is certified as a valid 1993 model merely because an old completion record links to it. The two BD tables agreeing is cross-table corroboration, not two independent historical witnesses.

## Material source conflict discovered

All **52,552** `BuildingWorksHistory` rows labelled `OP Date` have year **2019 or 2020**. For **52,202 CSUIDs**, those dates disagree with the permit dates in the explicitly linked `OP` table. The pipeline preserves both sources and flags this; it does not overwrite or silently repair the publisher's values.

Example: CSUID `0621112353T20050430` has a works completion of **1969-02-01**, a works `OP Date` of **2019-02-01**, and linked permit `NT6/69` dated **1969-02-01**. The raw source records and their IDs are retained. This is evidence of a date-value inconsistency, not evidence that the structure was built in 2019. Its cause is not established.

**Fresh source verification at 2026-10-13 12:36 UTC:** eight exact public records were re-requested individually from CSDI and matched their acquisition snapshots field for field. The discrepancy exists in the raw JSON, before this pipeline parses any date. The official specification defines `WorksDate` as the date of the works, `OP.OPDate` as permit issue date, and separately names geometry/record creation dates; it does **not** document works `OP Date` as a database-creation timestamp or explain the 2019/2020 pattern. Whether this is a publisher encoding/migration error remains unresolved; it is not relabelled as a record timestamp here.

| Public source table / OBJECTID | CSUID or permit | Exact raw value | Parsed Hong Kong date |
|---|---|---|---|
| BuildingWorksHistory / 62779 | `0621112353T20050430`, Completion Date | `01/02/1969` | 1969-02-01 |
| BuildingWorksHistory / 62780 | same CSUID, OP Date | `01/02/2019` | 2019-02-01 |
| OP / 16184 | `NT6/69` | `-28886400000` milliseconds | 1969-02-01 |
| BuildingWorksHistory / 113305 | `3792721212T20050430`, Completion Date | `18/05/1982` | 1982-05-18 |
| BuildingWorksHistory / 113306 | same CSUID, OP Date | `18/05/2019` | 2019-05-18 |
| OP / 21190 | `K23/82` | `390499200000` milliseconds | 1982-05-18 |

Exact URLs, raw responses, retrieval times, hashes and join-path IDs are in `documentation/fresh_anomaly_crosscheck.json`. CSV fields `completion_matches_relational_permit_by_target`, `matching_completion_permit_dates`, `qualifying_completion_providers` and qualifying event IDs preserve the positive support **separately** from `works_op_date_conflict`. Thus a conflicting works OP value need not obscure a specific older completion date that the linked permit also supports.

The near-approach **Regal Oriental Hotel tower**, CSUID `3792721212T20050430`, has completion **1982-05-18**, linked OP **1982-05-18**, and conflicting works OP **2019-05-18**. Its historical form and naming remain unverified. **Mei Yan House**, CSUID `3738621565T20091214`, has HD completion **2010-04-28**; **Mei Tak House** at Mei Tung Estate, CSUID `3763921652T20130422`, has HD completion **2014-09-01**. Later completion alone does not establish absence of construction in 1993. Same-named buildings elsewhere are not substituted: another Mei Tak House has a different CSUID and a 1969 date.

## Files

- `aoi_features_1993-11-04.csv`: all 69,915 local current polygons, names, representative-point coordinates, source heights and documentary classification.
- `current_features_1993-11-04.csv`: all 342,195 whole-territory current polygons with the same fields.
- `objects_1993-11-04.csv`: CSUID-level classifications, including unlocated documentary identities if present. In this snapshot **none** extend beyond the current polygon set.
- `chronology.sqlite`: `features`, `objects`, `events`, `raw_records`, and `join_issues`; indexes support inspection and joins. Raw source records remain queryable without data loss.
- `events.csv`: **221,383** evidence-event paths: 168,042 works rows and 53,341 resolvable permit relationship paths. A path is not necessarily an independent physical event.
- `join_issues.csv`: missing/null permits and one-to-many structure links, never silently discarded.
- `summary_1993-11-04.json`, `validation.json`: counts, semantic audit and source anomalies.
- `examples_1993-11-04.json`: illustrative name-search matches with full event provenance, including unresolved and same-name different-identity cases.
- `demolition_events.json`: all 34 demolition completion records, **2019–2020**, each linked to an `Active` modern polygon and explicitly conflicted. These do not constitute a historic demolished-building catalogue.
- `raw/`: original paginated JSON responses, metadata, counts and OBJECTID lists for all four tables.
- `acquisition_manifest.json`: exact request URLs, retrieval timestamps, response hashes and complete-table count checks.
- `documentation/`: official specification, permit explanation and source provenance.
- `manifest.json`, `input_hashes.json`: integrity hashes for outputs and read-only footprint inputs.

Coordinates in the CSV are **representative points inside the current footprint**, longitude/latitude WGS84, not historical building coordinates, survey control points or calibrated aerial matches. Rejoin exact current geometry using `objectid`/`building_csuid` to the unchanged GeoJSON. The local flag reproduces the prior exact polygon-intersection subset WGS84 `[114.10,22.27,114.25,22.40]`; it is not the immediate visual-turn corridor.

## Source acquisition and joins

Official [CSDI Building service](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer):

| Table | Source ID | Complete retrieved rows |
|---|---:|---:|
| BuildingWorksHistory | 1000 | 168,042 |
| BuildingRelateOPStructure | 1002 | 53,349 |
| OPStructure | 1003 | 54,505 |
| OP | 1004 | 24,469 |

All table counts matched before/after acquisition; every retrieved OBJECTID matched the separately queried complete ID set; no duplicate OBJECTIDs. Pagination is ordered by OBJECTID, at the advertised 3,000-row limit. **119 original response files** were individually hashed and rechecked. No credential or fee was required.

Joins use the documented identifiers, not approximate names:

`Building.BuildingCSUID → BuildingRelateOPStructure.BuildingCSUID → BuildingStructureID → OPStructure.OPNo → OP.OPNo`.

`BuildingWorksHistory.BuildingCSUID` joins directly to the building identity. **2,204 duplicated natural-key works rows are retained**; they do not count as extra buildings. **314 CSUIDs have multiple structure links**; all paths survive. **Eight** relation paths have null/missing permit records. OP support from a linked structure is labelled `linked_scope`, not assumed to establish the completion of every component in a current outline. OPStructure and OP keys were unique in the acquired snapshot. 20,146 of 24,469 permit records link through this current feature graph; the remainder remain stored without invented spatial matches.

## Date and class rules

The [official Building FSDT specification, January 2026 v1.1](https://static.csdi.gov.hk/csdi-webpage/download/common/b3eead8b2d2f167fcf05009502dfc628a77a3ab76a22a52cfbaa405a65cde6e6), pp. 10–13 and 20–21, defines the fields and relationship keys. `DateCreate` and the embedded CSUID date concern database geometry creation; neither is used as construction evidence. `DateStamp` is a record-modification date. Base/roof values remain approximate elevations above HKPD, not AGL heights or historical measurements.

The [Buildings Department's completion/OP explanation](https://www.bd.gov.hk/en/building-works/new-building-works/index.html) supports treating a granted occupation permit as documentary evidence that its building was ready for occupation by issue, not as the construction start date. This source is retained locally. Exemption and compliance certificates are kept as **administrative evidence only**; no unjustified physical-completion inference is made from their dates.

- Works day strings are parsed `DD/MM/YYYY`, including one unpadded day/month string.
- The two ArchSD year-only `2021` records produce `[2021-01-01,2021-12-31]` intervals, not January 1 point dates.
- Two duplicated HD `00/01/2001` records remain invalid/undated: no publisher-verified zero-day convention was found, so January 1 is not imputed.
- Five linked permit paths have null dates; retained as undated evidence.
- ArcGIS OP values are epoch milliseconds. Source metadata specifies **China Standard Time**. They are converted to UTC+08:00 calendar dates. Using the UTC date would move many permits one day earlier.
- Evidence is definitely on/before the query only when its **upper date bound ≤ query date**. A straddling year stays date-sensitive.
- `documented_completion_by_target`: at least one directly linked completion date qualifies; historical survival and shape are still unresolved.
- `documented_permit_by_target_linked_scope`: at least one permit path qualifies, without a qualifying direct completion record.
- `_with_evidence_conflict`: qualifying support exists, but conflicting source values remain; the support and conflict are both exported.
- `later_completion_or_permit_only_presence_unresolved`: no qualifying early evidence; **not absent**.
- `documentary_records_only_presence_unresolved` and `no_documentary_chronology_presence_unresolved`: no supported completion/presence classification.
- Demolition completion by the query can support absence of that documented identity, but contradiction with the current active snapshot triggers unresolved identity/conflict status. A future demolition-completion date does not say whether demolition had started at an earlier query date.

## Reproduce and query another date

From the workspace root, using the already established GIS environment:

```sh
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/chronology/structures/chronology.py --date 1985-01-01
research/checkers-runway13/geospatial/.venv/bin/python -m unittest discover -s research/checkers-runway13/reconstruction/chronology/structures -p 'test_*.py' -v
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/chronology/structures/audit.py
```

`--build` rebuilds the database from retained source tables and the unchanged footprint inputs. `acquire.py` performs a fresh public table acquisition. Neither script changes the analytical/simulator model. A dated query writes date-specific classification exports and reuses the static event graph. A date query cannot create missing historical observations.

## Verification and outstanding limits

**Correctness:** 39 semantic regression tests pass, including later-OP-not-absence, duplicate retention, source conflicts, demolition/active contradictions, year intervals, invalid zero days, nulls, Hong Kong timezone boundaries, corroborated completion despite a works-OP conflict, and proof that the source anomaly exists before parsing. New review regressions cover null-key exclusion, post-demolition permits, overlapping date precision, aggregate current statuses, compact-date normalization and missing/empty geometry, including a synthetic end-to-end database/query fixture. Raw-count/ID/hash validation, database integrity, unique current CSUIDs, full works retention, permit-path counts and both 1993 export reconciliations pass. A second real query for **1985-01-01** produced 24,256 whole-territory / 17,401 local features with some completed/permit-by-date support, with all current polygons retained.

**CLASS-01 completeness:** four complete public tables retained, conservative classification applied to every current feature, event provenance retained, arbitrary-date query implemented, audit and readable report produced. No hidden missing-date imputation or current-footprint historical substitution.

**Historical-reconstruction readiness:** incomplete. This snapshot contains no old identities outside today's footprint universe; historical demolished structures still require dated sheets/photos or other archives. No scan/photo content was visually matched in this lane, no structure was surveyed, no historical mesh was produced, and no aircraft-clearance claim follows. Use this as documentary evidence for the parent historical-matching workflow, not as the finished historical city.

Source attribution: Lands Department and Buildings Department, Government of the Hong Kong Special Administrative Region; CSDI Portal. Existing source terms and the geospatial package's attribution requirements continue to apply. Files are local; nothing was published, committed or synchronized to another machine.

## Independent-review repairs and snapshot impact

All six review findings were accepted after inspection and repaired within the original evidence contract:

1. Null, empty and whitespace-only structure/permit keys never join, including null-to-null. Incomplete records remain in `raw_records`; `join_issues` records the excluded path.
2. A permit dated after demolition completion makes identity/chronology unresolved, even without a direct completion record or an active current snapshot. Overlapping permit/demolition date intervals also cannot certify clean absence.
3. Multiple current-feature statuses for one CSUID are aggregated, not overwritten by the last row. `current_status_evidence` retains all statuses and disagreement is flagged.
4. Overlapping year/day evidence is compatible; disjoint completion intervals are conflicting. OP source checks compare full intervals. Exact cross-table corroboration requires exact matching day intervals, not merely an overlapping year.
5. Accepted compact ISO query dates are normalized before comparisons and filenames: `19931104` means `1993-11-04`, and November 5 is not before that query.
6. Null/empty/unreadable geometries remain as features with null coordinates and an explicit `geometry_status`, not a database-build crash. Invalid nonempty polygons are preserved and flagged.

A rebuilt database, both example-date exports and the complete acquisition/export audit passed again. `review_repair_impact.json` compares the old and repaired classifier for **all 342,195 current features at both dates**: **zero changes to pre-existing classification fields or summary counts** in this actual snapshot. This is not proof that the bugs were harmless generally: the new synthetic end-to-end fixture exercises precisely the previously failing combinations. Current source join keys are populated, all current CSUIDs are unique, and geometry has 342,112 valid / 83 invalid nonempty polygons. Eight links still lack a matching permit record; missing record is distinct from a null key.

The superseded code and prior summaries are preserved under `review_repair_baseline/`, clearly labelled not current. `review_impact.py` reproduces the complete before/after comparison. All original public date values remain unchanged.
