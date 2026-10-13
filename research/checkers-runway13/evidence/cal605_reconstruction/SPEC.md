---
title: Matched CAL605 flight and weather reconstruction benchmark
type: feature
created: 2026-10-13
status: done
baseline_commit: NO_VCS
context: []
---

<frozen-after-approval reason="Aryan: Let’s make that and then see what surprising results we get; accepted matched historical reconstruction and exploratory comparison, 13 October 2026">

## Intent

Build the uncertainty-aware CAL605 flight/weather reconstruction proposed in the preceding conversation, then compare observations with the existing landing equations and investigate discrepancies. Deliver reusable numerical evidence, readable figures and an evidence-qualified findings report. The object is a historical reconstruction benchmark, not a completed historical optimum or operational procedure.

Use the already-held CAD Report 1/95, especially Appendices 5–7 and 11–12, together with the acquired NOAA 1993 station-year archive. Work in a separate evidence directory so ongoing terrain reconstruction and frozen model sources remain untouched. Preserve numerical evidence and failed hypotheses, not just interesting-looking findings.

## Boundaries and constraints

Always distinguish report-stated numbers, manual image readings, computationally digitized traces, reconstructed quantities and assumed counterfactuals. Every observation needs source page/figure or raw record, units, time reference, method and uncertainty semantics. Plot-derived precision must reflect raster resolution, trace thickness, ambiguous intersections and axis calibration. Such bounds are digitization sensitivity bounds, not physical 95% confidence intervals. Raw DFDR measurement errors remain unavailable unless documented. Flight trace time and wind-system clock are distinct; no arbitrary alignment presented as observed synchronization.

Preserve the existing aircraft, objective, fixed braking model and source artifacts. Comparisons may evaluate that formula at observed inputs, clearly labeled conditional diagnostics. Do not tune the frozen solver or infer control, aerodynamic parameters and local wind simultaneously from position alone. Do not use mean surface weather as flight-path gust truth. No causal population claim from one accident, and no generic prediction interval or accident probability. Do not reinterpret radio height as AMSL or map trace integration as independent position truth.

External contact, paid acquisition, publication and model-meaning changes require separate authorization; none is needed for this approved local evidence work. Do not duplicate terrain-owner geometry reconstruction or claim its active outputs as stable. Routine-flight validation remains a wider-project gap; it is not silently replaced by the accident case.

## I/O and edge cases

| Input | Expected behavior |
|---|---|
| Readable published flight curve | Calibrate axes, preserve actual pixel anchors and extract trace samples; show image overlays and ranges attributable to reading precision. |
| Overlapping/indistinct trace | Mark ambiguous or missing; no forced invented sample. Interpolation explicitly labeled. |
| Published narrative flight events | Separate source-stated event table; compare with graph without treating them as independent measurements. |
| Wind A/B/C fields | Decode present/2-minute/10-minute semantics separately; preserve sensor and own-clock labels. Missing scheduled record is not zero wind. |
| NOAA missing/quality flags | Retain raw fields, null sentinels, documented quality filtering and report types; no imputation. |
| Unknown UTC offset or datum | Maintain separate relative times and report identifiability limit; sensitivity scenarios cannot certify alignment. |
| Historical/model disagreement | Report mismatch and conditional decomposition, without claiming matched controls or historical superiority. |

</frozen-after-approval>

## Code map

- `../../../../data/kai-tak-2026-10-13/sources/`: immutable primary report PDF and searchable transcription (workspace-root resolution is authoritative).
- `../weather_feasibility_2026-10-13/`: acquired NOAA archive and acquisition evidence.
- `../../approximation/reference_outcomes.json` and `../../model/config.json`: read-only nominal comparator.
- `source_pages/`: rendered source evidence and annotated extraction overlays.
- `noaa/`: separately owned reproducible NOAA decoding and QC.

## Tasks and acceptance

- [x] SRC-01 `manifest.json`: source hashes and page/figure index; preserve input identity.
- [x] WX-01 `wind/wind_records.csv`, `wind/wind_extraction.json`: visually verified five-sensor printout transcription and field semantics with missing/ambiguous fields explicit.
- [x] FLT-01 `flight/flight_traces.csv`, `flight/trace_anchors.json`, `flight_events.csv`, `rollout_trace.csv`: reconstruct readable approach/rollout variables with provenance, uncertainty, independent narrative checks and source overlays.
- [x] WX-02 `noaa/`: documented decoder, year/event tables, quality/missingness summary and tests.
- [x] COMP-01 `reconstruct.py`, `analysis.json`: derive observed timing/runway diagnostics, compare frozen reference and conditional stopping formulas, retain assumptions and unidentifiable quantities.
- [x] OUT-01 `REPORT.md`, standalone figures: distinguish achieved extraction, findings, limitations and wider-project blockers.
- [x] VAL-01 `test_reconstruction.py`, `verification.json`: test axis transforms, bounds, chronology, units, cross-source consistency and scalar distance calculations; independently review extraction and consequential findings.

Given the retained raw inputs and manual anchors, when the script runs, then derived tables and figures reproduce without network access. Given uncertain anchors, when propagated, then output ranges enclose declared digitization inputs without statistical labels. Given a clock offset not identified by evidence, when joining sources, then no exact synchronization is asserted. Given each final numerical finding, when traced backward, then its source and calculation are inspectable. Given comparison to the synthetic model, then unmatched entry state, control history and environment remain explicit.

## Verification

Use the project's existing Python virtual environment, numerical libraries and local Poppler rendering tools. Inspect overlays against primary PDF pages and cross-check published narrative numbers. Run meaningful reconstruction/decoder tests, verify source hashes and inspect report/figure contents. Final status separates benchmark implementation from historical 3D/optimality/prediction completeness.

## Spec change log

2026-10-13: Initial benchmark scope records explicit authorization; no renewed approval gate for accepted work. Workspace BMAD config is absent; use project-local paths and existing frozen model conventions.

## Suggested Review Order

- Start with the substantive findings and their interpretation limits.
  [REPORT.md](REPORT.md#L1)
- Inspect actual source anchors before reading interpolated curves.
  [flight/README.md](flight/README.md#L1)
- Distinguish sensor location, aggregation window and unknown clock offset.
  [wind/README.md](wind/README.md#L1)
- Inspect closed-form reconstruction and conditional stopping arithmetic.
  [reconstruct.py](reconstruct.py#L1)
- Review accepted defects, repairs and final evidence.
  [REVIEW_DECISIONS.md](reviews/REVIEW_DECISIONS.md#L1)
  [verification.json](verification.json)
