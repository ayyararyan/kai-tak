---
title: Evidence-linked block matching and historical 3D reconstruction
type: feature
created: 2026-10-13
status: in-progress
baseline_commit: NO_VCS
context: []
---

<frozen-after-approval reason="Aryan explicitly instructed block-wise matching then the most accurate 3D reconstruction on 2026-10-13; no second approval required for in-scope implementation">

## Intent

Recover historical structure geometry from the acquired Kai Tak survey sheets and photographs, match structures block by block, and then produce the most accurate evidence-supported 3D reconstruction available from those sources. Preserve the historical date dimension; 1993-11-04 is the existing example scene query, not a restriction on source epochs. Begin in the existing approach core [114.16,22.30,114.22,22.35], retaining the broader acquisition rectangle and unresolved coverage. A finite review batch does not discharge the full reconstruction requirement.

Registration and structure matching precede 3D geometry. Accuracy means traceable source support, validated alignment, correct dates, measured outlines/heights where available and explicit unknowns. Visual realism is not evidence. The deliverables form one reconstruction chain: registered source catalogue, blocks and structure correspondences, historical geometries and uncertainty, then a viewable and machine-readable scene.

## Boundaries & Constraints

Always preserve official downloads and the existing chronology handoff unchanged. Use the supplied survey world files where available, verify printed-grid alignment, assign EPSG:2326 from source documentation, and record that raster pixel resolution is not physical accuracy. Photos need content-based ground control and holdout residuals; index footprint corners are not ground control. Distinguish planar photo registration from orthorectification, especially at tall roofs and slopes.

Block assignments must be labelled: survey tile/subdivision work units are not automatically street blocks. Street blocks require traced roads or matching source geometry. Match historical footprint to current identity only with outline/location/name evidence; document-backed completion alone is insufficient. Preserve split/merge, demolished, changed, omitted and ambiguous objects. Current-source absence never proves historical absence. Unknown height/presence remains null. No guessed storey-height conversion or uniform invented extrusion may appear as historical geometry.

Keep geometry, presence, height and terrain dates separate. Historical map spot elevations may be used only after reading their meaning/units and associating them with a specific object. Storeys are not elevations. Modern HKPD top/base elevations may be offered only as separately labelled modern comparison or proxy layers, not historical measured height. A rendered missing-height marker must not be exported as an obstacle or asserted roof. Existing 2014–15 terrain is a comparison/proxy until historical changes are resolved; do not fill former runway/harbour with today's development.

Proceed with public read-only research and reversible local processing. No paid data, outreach, publication or aircraft/optimizer changes. Ask only for genuinely missing authority, such as purchase of calibrated scans; prepare concrete options first. Complete evidence-supported work before reporting gaps. If full historical height recovery is genuinely unavailable, report the reconstruction incomplete, not 'finished' because a viewer opens.

## I/O & Edge-Case Matrix

| State | Required behaviour |
|---|---|
| Official TFW and sheet grid agree | Registered sheet with measured residuals and original source hash |
| TFW missing or grid inconsistent | Flag unresolved; do not silently infer transform from extent |
| November-only edition vs November 4 | Date-sensitive, not certainly preceding query |
| Matching footprint but different/current height | Identity candidate with independent height-status field |
| Roof displacement in photo | No roof point used as ground control without correction |
| Cartographic blank or illegible building | Unknown/omitted, not open ground |
| Absent historical height | Null metric volume; visibly identified unresolved region |
| Invalid current polygon | Retain original evidence, report repair if a derived operation requires it |

</frozen-after-approval>

## Code Map

- `../chronology/` — immutable source package, manifests, dates and observation ledger.
- `../../geospatial/derived/` — modern footprints and terrain, separate epochs.
- `register_sheets.py`, `registered/` — world-file registration inventory and clipped map rasters.
- `blocks.geojson`, `structure_matches.geojson`, `observations.json` — work units, geometries, independent status/provenance fields.
- `aerial_registration/` — separate investigation, GCP/holdout tables and honest registration results.
- `build_scene.py`, `scene/` — permitted geometry, portable viewer and machine-readable outputs.
- `REPORT.md`, `validation.json`, `MODEL_REQUIREMENTS_TRACEABILITY.md` — measured evidence and complete coverage audit.
- `../../PROJECT_STATE.md` — sole project ledger, append-only updates preserving other session's work.

## Tasks & Acceptance

- [ ] REG-01: audit transforms for every downloaded sheet, then independently inspect printed control grid on used digitization sheets.
- [ ] REG-02: register useful dated aerial imagery with ground points and withheld check points, or identify the exact unresolved inputs.
- [ ] MATCH-01: produce explicit block coverage/work units and source-backed individual footprint/identity matches, including changed and vanished structures.
- [ ] HEIGHT-01: extract defensible historical heights where possible and keep unresolved geometry/height masks complete.
- [ ] SCENE-01: only after matching, build portable evidence-linked 3D output with separate epochs/proxy layers and no invented physical volumes.
- [ ] VAL-01: verify registration, transforms, dates, topology, height semantics, source integrity and visual scene behaviour; retain acceptance evidence.
- [ ] OUT-01: deliver readable results, exported geometries, provenance and a full-scope completeness audit.

Given a depicted structure, its derived geometry must link to the source and digitization method. Given an unresolved height, the exported historical scene cannot contain a non-null asserted building volume. Given a modern comparison layer, its epoch/proxy label must remain visible. Given a source transformation, recorded independent checks must distinguish assignment from positional accuracy. Given a partially reviewed area, every unreviewed region must remain explicit. Given a generated viewer, inspect the delivered interaction or label it unverified.

## Spec Change Log

2026-10-13: new user-authorized reconstruction continuation. Chronology evidence and frozen aircraft model remain unchanged. Workflow checkpoint does not require reapproval of the explicit current instruction.

## Verification

Run regression tests for affine/CRS round trips, month-boundary semantics, null heights, historical-vs-modern separation and invalid geometry handling. Reconcile all geometry/source counts and hashes. Inspect map-overlay figures and the actual viewer. Passing code tests is not full historical reconstruction completeness.
