---
title: Source-backed historical obstacle update
type: feature
created: 2026-10-13
status: in-review
baseline_commit: NO_VCS
context: []
---

<frozen-after-approval reason="Aryan directed accurate obstacle updates; existing historical reconstruction scope already authorized">

## Intent

Replace presentation-only progress with improved historical obstacle evidence for the Kai Tak landing study. Preserve the existing 1993-11-04 query and full approach reconstruction objective. Extract defensible historical terrain/elevated-surface observations from original survey sources, audit aviation elevation context, and package them with unresolved building footprints and explicit coverage. A bounded set of new observations does not complete the full obstacle inventory.

The useful object is a dated, geographically located obstacle surface with defensible vertical reference and uncertainty. A photograph-derived relative-height cloud is not that object. This continuation must improve source-supported observations where possible and explicitly block unsupported clearance calculations rather than relabel existing patches as accurate obstacles.

## Boundaries & Constraints

Preserve original sources, prior reviewed geometry, stereo observations, the frozen aircraft/optimizer configuration, and the published snapshot. Work locally under this directory and append only to the canonical project ledger. 1993 historical presence is not established by bracketing map editions alone. A map edition is month-precision publication/revision evidence, not every object's survey date. Existing source dating and unresolved regions remain visible.

Store horizontal coordinates in EPSG:2326 with WGS84 GeoJSON exports. Extract positions from source-registered imagery, record digitized pixel locations and hashes, and distinguish scan/grid agreement from ground positional accuracy. Use the printed historical sheet's units/datum before recording metric elevations. Modern mapping specifications can explain feature semantics but cannot retroactively certify older surveys. Keep source elevations and exact unit conversions separate from assumptions. HKPD, AMSL, ellipsoid heights and relative stereo Z are different fields, never silently combined.

A terrain spot is a measured map observation at a point, not a roof top, solid, local maximum, or surface bound. A platform observation is not necessarily the maximum structure height. A building outline with unknown height remains an unresolved polygon. Blank, omitted, unreviewed, or missing areas remain unknown, never clear. Do not infer roof elevations from addresses, storeys, modern heights, or a local ground-plane offset. Do not create confidence bounds from sensitivity scenarios. A visually matching map label in two editions is corroborated mapped content, not independent observations or proof of unchanged 1993 geometry.

No aircraft-model meaning changes, live operations, spending, outreach, publishing or peer synchronization. Those are not needed to extract and validate supported data. If original data cannot establish complete accurate obstacle surfaces, report exactly which observations improved and which gates remain blocked; do not claim accurate historical clearance.

## I/O & Edge-Case Matrix

| Input/state | Required behavior |
|---|---|
| Readable historical spot symbol, value, units and datum | Source-bound point observation with manual interpretation and position |
| Address, storey count, or ambiguous elevated/ground surface | Reject as height or retain unresolved interpretation |
| Two map editions agree | Two source observations linked by location, not exact-date survival certification |
| Unverified source hash or changed crop/annotation | Refuse inherited acceptance |
| Historical footprint has no top elevation | Retain null top and an explicit unknown-obstacle mask |
| Historical coverage incomplete | Historical-clearance readiness false, regardless of count or code tests |
| Aviation AMSL figure | Preserve original datum; no automatic HKPD conversion |

</frozen-after-approval>

## Code Map

- `../block_matching/registered/sheet_registration_inventory.json`: original ZIP/TIFF/world-file identities and transforms.
- `../chronology/sheets/maps/`: immutable official historical survey source archives.
- `../block_matching/historical_faces.geojson`: accepted dated 2D mapped forms, heights unresolved.
- `../block_matching/aerial_registration/sparse_stereo_report.json`: existing relative-height limitations, not an absolute-height source.
- `sources/`, `review/`, `aviation_sources/`: interpretation documents and inspection evidence.
- `observations.json`, `build_obstacles.py`, `test_obstacles.py`: manually accepted readings, deterministic exports, semantic checks.
- `obstacle_evidence.geojson`, `unresolved_footprints.geojson`, `readiness.json`, `REPORT.md`: usable local handoff.

## Tasks & Acceptance

- [ ] OBS-01: inspect relevant historical hill/approach maps and printed datum/legend; preserve hash-bound readings and interpretation exclusions.
- [ ] OBS-02: investigate original aviation records for useful absolute elevation and obstacle context; keep unresolved symbols unpromoted.
- [ ] OBS-03: build geographical observation and unresolved-footprint exports, with complete source/date/datum semantics and an approach-coverage unknown mask.
- [ ] OBS-04: verify source/crop hashes, coordinate conversions, null propagation, temporal distinctions and model/source preservation.
- [ ] OBS-05: report new supported evidence and remaining obstacle-readiness gaps; append verified status to the sole project ledger.

Given an accepted reading, rebuilding must reproduce its value and coordinate from the pinned source and digitized location. Given a changed source, export must fail rather than reuse approval. Given unmeasured roofs or unreviewed coverage, no obstacle-clearance-ready flag or invented upper surface may result. Given a different datum or date, observations must remain distinguishable. Given source-supported new elevations, the handoff must identify their physical surface and not merely add a figure. Completion of this implementation does not close the full historical reconstruction specification.

## Spec Change Log

2026-10-13: current instruction prioritizes accurate obstacle evidence over reconstruction presentation. Existing approval covers reversible extraction and validation; no new model decision or redundant approval gate introduced. BMAD config is absent; project-local paths and English are used without creating unrelated configuration.

## Verification

Use the existing geospatial virtual environment. Rebuild the exports and run focused tests for evidence binding, coordinate location, source-time separation, datum handling and fail-closed readiness. Visually inspect every newly accepted source reading and its physical symbol. Compare the frozen model/source hashes before and after. Independent review must distinguish implemented data handling from unfulfilled historical completeness.
