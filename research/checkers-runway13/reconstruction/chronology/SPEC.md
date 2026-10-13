---
title: Evidence-backed historical structure chronology
type: feature
created: 2026-10-13
status: evidence-package-verified-historical-reconstruction-incomplete
baseline_commit: NO_VCS
context: []
---

<frozen-after-approval reason="Aryan explicitly requested matching sheets/photos and classifying as many structures as possible on 2026-10-13; executes that scope without a second approval">

## Intent

Create an auditable, spatially matched historical source collection and structure chronology for the Kai Tak approach reconstruction. Maximise evidence-backed classification, including demolished structures; do not substitute an index of modern buildings for a historical reconstruction. Support dated queries with evidence intervals instead of claiming universal exact-date knowledge.

Begin with the existing local acquisition rectangle WGS84 [114.10,22.27,114.25,22.40], encompassing Kowloon/Kai Tak and context. Prioritise the Checkerboard Hill/Kowloon City turn/airport area for actual image inspection, while retaining broader available coverage. All-territory downloadable documentary tables may be retained and processed where practical. Geographic scope and coverage must be explicit in every summary. The date dimension is historical; use 1993-11-04 as a clearly labelled example, not a newly frozen restriction or a claim of daily observation. Acquire other epochs when useful.

## Boundaries

Always preserve source URL, exact identifier, capture/edition/release date semantics, retrieval timestamp and checksum. Join source geometries in documented coordinate systems. A survey-sheet edition is not proof that all mapped features were surveyed on its publication date. Aerial index positions/estimated footprints are not photos or calibrated orthophotos.

Presence, construction, completion, demolition and occupancy dates are different objects. Modern database creation/update dates are not construction dates. A later occupation permit alone cannot prove absence before that date. Current footprints and heights cannot be projected backwards unchanged solely from a completion date. Match historical identity explicitly and retain conflicts. Unknown height/presence is never zero/absent. Demolished objects need historical evidence, not modern-source absence.

Classifications: directly observed at source epoch; document-supported completed/present by date; date-sensitive construction/demolition; absent supported by explicit evidence; unresolved. Each result carries evidence type and source. Uncertainty must remain available to downstream scene construction. Measurements from scanned maps require registration quality flags; no precision surveying or aviation-clearance claim.

Proceed with public read-only retrieval and local reversible processing. No purchases, outgoing messages, publication, credentials, simulator changes or alteration to analytical objectives. Preserve existing artifacts. Obtain missing paid/gated inputs only after a concrete acquisition option is ready for authorization. No fabricated manual visual review, automatic segmentation presented as verified buildings, or missing-data imputation.

## Inputs and edge cases

| Input | Expected handling |
|---|---|
| Paginated public index/table | Retrieve all matching rows, validate IDs/counts and preserve raw response |
| Geographic intersection | Retain exact overlap, not just name similarity |
| HTTP success containing error HTML | Record failed content validation; not a usable map |
| Source missing date or geometry | Preserve row, flag inability to time/place it |
| Ambiguous building join / multiple dates | Preserve alternatives; do not choose a convenient date |
| Historical image with no readable detail | No building presence/absence certification |
| No historical evidence for modern structure | Unresolved historical status, not absent |

</frozen-after-approval>

## Code map and ownership

- `../../geospatial/raw/Building_20260921.geojson`: existing whole-territory current snapshot, read-only.
- `../../geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson`: existing local subset, read-only.
- `../SOURCE_REPORT.md`, `../APPROACH_CITY_INVENTORY.md`: preceding findings and caveats.
- `sheets/`: historical map indexes, downloaded sheets, previews and matching outputs (parent).
- `aerial/`: exact frame acquisition and coverage investigation (independent acquisition agent).
- `structures/`: official works/permit tables, conservative date classifier and exports (implementation agent).
- `REPORT.md`, `coverage.png`, `manifest.json`: parent synthesis, visible handoff and verification.

## Tasks and acceptance

- [x] DATA-01: `sheets/` — acquire complete AOI indexes for available historical survey families; preserve edition dates and download links, check pagination.
- [x] DATA-02: `sheets/` — retrieve useful dated sheets around the turn and airport; validate formats and visually inspect geographic content.
- [x] DATA-03: `aerial/` — acquire exact dated historical frame records and usable imagery where publicly available; distinguish blocked image acquisition from index success.
- [x] JOIN-01: spatially join sheet/frame coverage, report capture-edition time differences; never call coverage overlap a content match.
- [x] CLASS-01: `structures/` — acquire official historical works/permit evidence and apply conservative structure-level chronology to as many uniquely joinable features as possible.
- [ ] CLASS-02: inspect usable historical images for vanished/changed structures and document source-backed observations; record unresolved coverage, not made-up completeness.
- [x] OUT-01: deliver machine-readable classified inventory, source inventory, visible coverage map and readable report with counts and limitations.
- [x] VAL-01: test date semantics, join multiplicity, nulls, count completeness and source integrity; inspect delivered image/report and reconcile counts.

Given a historical date query, the output must separate documentary support from image confirmation and unresolved structures. Given source overlap, the output must provide source IDs and dates without claiming that contents agree. Given inaccessible imagery, acquisition records must identify the exact blocker and resulting incomplete requirements. Overall historical reconstruction remains incomplete unless evidence actually covers its required objects; a functioning pipeline is not completion of Hong Kong's historical inventory.

## Verification

Verify parsed responses against source counts where supported; detect duplicate IDs, missing join keys and repeated pagination. Store SHA-256 hashes. Exercise classifier boundaries and ambiguous cases. Inspect raster/preview content and a sample of matched source/building records. Report total scoped, documented, visually checked and unresolved separately. Reuse geospatial environment without changing the numerical model environment.

## Spec change log

Initial scoped implementation under current explicit authorization. No frozen aircraft/model meaning changed.

## Verified handoff, 13 October 2026

See MODEL_REQUIREMENTS_TRACEABILITY.md and validation.json. Seven requirements implemented; CLASS-02 remains partial: 52 directly inspected observations for 17 named objects/sites, not a historical building census. Acquisition and documentary classification verified; registered historical outlines, complete vanished structures and heights remain missing. No aircraft/model changes.
