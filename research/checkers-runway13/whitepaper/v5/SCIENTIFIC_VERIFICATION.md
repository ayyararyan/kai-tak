# Scientific claims and source verification — Version 5

## Scope and verdict

The accepted numerical evidence has been preserved and freshly checked. The two
fixed-witness continuous-time checks pass; 89 portable model/counterfactual tests
pass; independent V5 arithmetic and source-integrity checks pass. No trajectory
search, parameter change or new historical reconstruction was performed. These
checks do not establish aircraft calibration, historical clearance or optimality.

**Manuscript integration status:** seven-act text and Appendices A–H scientifically
audited. All 51 baseline claim IDs are mapped: 50 scientific/source claims are preserved,
and author-context C01 is condensed without invented experience. All 26 baseline
displayed mathematical blocks survive; the coefficient table is byte-identical.
All 14 references are cited. The complete abstract and all 15 figure masters pass
source/semantic review; 74 independent in-memory figure checks pass.
Two additional ledger rows trace existing archival inputs newly illustrated in
V5: October source-photo dates (C52) and labelled conditional stereo heights (C53),
bringing the active ledger to 53 rows. They introduce no new reconstruction.
The independent final reader review has been performed after technical checks;
its five targeted findings were accepted and revised. The revised page flow has been reinspected and accepted. The final clean-package build and artifact comparison passed as separately recorded in REPRODUCIBILITY.md; the final layout-only changes preserve the audited prose and mathematics exactly (qa/final_layout_delta.json).

The original 51-row ledger is preserved byte-for-byte in
`editorial/V4_CLAIMS_AND_EVIDENCE.csv`. The active `CLAIMS_AND_EVIDENCE.csv` records
V5 manuscript locations and actual new verification routes, not inherited V3
checks relabelled as fresh.
[The V5 preservation map](editorial/SCIENTIFIC_CLAIM_MAP.md) routes every claim to
the new narrative and records where its essential scope must remain.

## Fresh checks and exact receipts

| Check | New result | Receipt |
|---|---|---|
| Fixed calm witness, original outward-rounded checker | Certified `η ≥ 0.0397`; 2,502 closed intervals; exact saved cover reproduced | `qa/fresh_calm_certificate.json` |
| Fixed wind witness, separate original checker | Certified `η ≥ 0.1507934696816132`; 376 intervals; exact saved cover reproduced | `qa/fresh_wind_certificate.json` |
| Frozen portable regression suites | **89 passed**, 2.43 s; negative paths and mocked search failures included | `qa/science_tests.json` |
| Independent V5 science checker | **287 standard checks; 288 including fresh calm bound**, including frozen hashes, polynomial/CSV derivatives, supplementary image/mesh inputs and independently calculated scalar outcomes | `qa/science_checks.json`; `qa/science_checks_fresh_bound.json` |
| Independent figure-semantic checker | **74 checks passed across all 15 masters**, constructing the actual plots in memory without writing published figures | `qa/science_figure_semantics.json` |
| Original calm-family bound/regularity functions | Fresh outward-rounded result matches the retained bound and full-box regularity lemma | `qa/science_fresh_calm_bound.json` |
| Historical source and reference audit | Primary CAD sections re-read; relevant primary references checked; access fallbacks recorded | `qa/science_sources.json` |

Receipts contain UTC timestamps. `qa/science_certificates.json` summarizes the two
proof runs without conflating them. The original checker and calculator remain
unchanged. The proof reruns reconstruct exact real-decimal parameters; the V5
display checker evaluates floating coefficient exports. The latter is a useful
independent arithmetic check, not another continuous-time certificate.

The portable test command uses the frozen model and counterfactual tests. Calls to
search in negative-path tests mock the numerical solver and use pytest temporary
paths: they neither optimize a new trajectory nor overwrite source results.

## Manuscript-level scientific audit

Receipt: `qa/science_manuscript.json`. Every new act, caption and technical appendix
was read against the original 51-row ledger and frozen parameter specification.
The normalized equation audit finds all 26 original displayed blocks; merging the
two objective brackets changes a terminal period to a comma, not the mathematics.
The stopping-box bounds, policy quantifiers, source counts, uncertainty distinctions
and related methods have moved into the appendices with their domains intact.

Two precision improvements clarify existing meanings: bank-angle rate is explicitly
the rate in the moving flight-path frame, not the full angular velocity of the lift
vector; the corridor is described as a three-dimensional distance to the fixed
reference cloud. Neither changes the model. The new envelope table reproduces the
configuration, and both brief rises remain.

Figures 4 and 5 were inspected visually and at source level. The local landing
projection has orthonormal camera rows and no vertical exaggeration; no historical
city or terrain is inserted. Both runway rows use the same 2786 m scale, correct
delay/braking lengths and the common 150 m reserve boundary. Their difference is
labelled a separately optimized scenario comparison.

The historical opening and bearing diagram were also inspected. The source views
remain separate photographs, not an invented stitched city; the 47-degree inset
uses magnetic directions, not aircraft bank. Eleven supplementary visual inputs
are hash-verified. CN4581 and CN4589 retain their 8 October 1993 catalogue dates.
The mesh uses accepted open triangles, with no reconstructed walls or gap filling.
Two labelled roof examples retain heights 10.7694316303 m and 19.1954909125 m
relative to the fitted plane; both lie outside the map-control hull. The camera
orientation correction and explicit local statement of that support condition
have been source-checked and visually reinspected.

The complete mechanics suite now has a consistent right-bank/right-turn geometry,
exactly tangent turn arrows, correctly signed rightward wind components and
horizontal (not three-dimensional) ground speed. The pedagogical quadratic's
eight interval rectangles contain its true extrema. The controls retain their
sampled/one-sided-join interpretation. The recorder preserves all 123 final-phase
anchors and negative radio-height readings; its clock stays separate from the
ground-wind plot. All 30 values in the two selected A-field series are retained.
The four rollout landmarks keep categorical source order and their conditional
deceleration formula. The annual CDF includes its full support through 20.1 m/s:
an initially clipped two-observation tail was detected and corrected by extending
the displayed axis, with no data or rank changes.

The proposed recorder ground-indication band was checked independently against
the retained pixel calibration: 1012 pixels, with 566 pixels at Datum B zero and
1573 pixels at 70 seconds, gives 31.002979146 seconds. Independent ±3-pixel reading
and calibration-endpoint allowances give [30.585898709,31.420059583] seconds.
This is a declared raster-reading range, not exact physical touchdown timing or
sensor uncertainty; it must retain that label if plotted.

## Numerical and mathematical invariants

| Quantity | Calm | Steady-wind scenario |
|---|---:|---:|
| Touchdown station, m beyond usable threshold | 313.492181158 | 302.114052038 |
| Stop station, m beyond usable threshold | 2531.321117620 | 2233.230845017 |
| Runway remaining, m | 254.678882380 | 552.769154983 |
| Entry-to-stop time, s | 96.286902270 | 96.644053677 |
| Certified normalized lower margin | 0.0397 | 0.1507934696816132 |
| Necessary family upper bound | strictly below 0.1559772 | at most 66656817/307536544 |

Display values above are rounded; the JSON records remain authoritative. Both
stopping calculations use two seconds of delay followed by `0.15g`, with
`g=9.80665 m/s²`, `LDA=2786 m` and a stipulated 150 m reserve. The independent
calculation includes delay travel and braking travel, not merely distance after
brakes activate. The wind/calm difference decomposes into touchdown-position and
ground-travel differences, but remains a comparison between separately optimized
scenarios.

The force-balance turn example remains a constant-speed, coordinated, level-turn
benchmark: at 78 m/s and 15° bank its radius is 2315.347 m, 47° takes 24.3499 s,
arc length is 1899.29 m, and load factor is 1.03528. Mass cancels from the radius
equation but not from the aircraft's force capacity. The 47° is a difference of
published magnetic directions, not bank angle.

The calm compactness argument establishes attainment in the bounded twelve-parameter
polynomial family, with positive durations and nonsingular inverse dynamics. It
does not locate the optimizer. The lower/upper bounds remain unmatched; withdrawn
tighter bounds are not reinstated. The wind upper bound is independently reproduced
using exact fractions; the exact remaining gap is
`1584555818464679384939/24026292500000000000000`.

Phase position, velocity and acceleration agree at the join. The exported wind
position/velocity samples agree with polynomial evaluation; EAS is recomputed from
air-relative velocity and density. The brief positive climb remains in each
trajectory. It was not removed to create a more conventional-looking descent.

## Primary historical sources

The actual retained 226-page CAD Report 1/95 was located, not inferred from a
secondary summary. Its SHA256 is
`f7cb59925ab0ac5fe06216f7d011050183c7131130517ede997bf2152795c87a`.
Relevant extracted text was read and the original page images at physical PDF pages
32, 92 and 126 inspected. The report itself is not copied into the V5 package.

The source supports the following V5 invariants:

- §1.8.1 gives 088° magnetic localizer direction, 3.1° glidepath and a visual-flight
  requirement at the middle marker, 1.7 NM from touchdown. §1.10 gives 135° magnetic,
  3331.5 m runway length, 61 m width and 2786 m LDA. The general airport history's
  extension-era 3390 m is a different source quantity.
- §1.11 records 269 DFDR parameters, omits thrust-lever angle and describes the
  final track as integrated from accelerations. Published plot anchors must not be
  relabelled raw flight data or independent surveyed positions.
- §§2.2.5–7 support the four approximate speed/distance landmarks, forward-thrust
  movement, autobrake disarming, spoiler retraction and delayed reverse/braking.
  The stopping-frontier calculation measures a conditional requirement, not the
  actual applied brake force.
- §2.6.5 judges the touchdown acceptable and its parameters noncausal; §3.2's four
  findings concern thrust-lever handling, monitoring/communication, co-pilot
  rollout skill/experience and missing clearly defined crosswind technique.
  The rewritten paper must preserve that account without implying accident
  prevention by the synthetic path.

The [official CAD history](https://www.cad.gov.hk/english/kaitak.html) was freshly
read for the 1974 IGS introduction and extension-era runway quantity. The retained
[CAD Link 75](https://www.cad.gov.hk/reports/CADLink/Issue75.pdf), May 2025, was
read for the Kowloon/visual-turn and closure history after the web reader refused
the PDF's size. This is source review, not a new historical observation.

## Imagery, reconstruction and weather

The [Old Survey Sheets collection](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-old-survey-sheets)
describes scanned, georeferenced historical maps and limits their positional use.
The [Digital Aerial Photo collection](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-aerial-photo)
identifies DAP-L0 as compressed 300 dpi photographs. Neither pixel spacing nor
image resolution is measurement accuracy. A36143's retained catalogue/scan-date
discrepancy remains unresolved; no new date was selected for convenience.

Reconstruction counts are preserved: 171,307 dense points, 3,780 inside the
control hull, 155,891 mesh vertices, 225,371 triangles and 86,061 boundary edges.
The 2.20656% control-hull share does not measure an accuracy percentage. Stereo
height is relative to the fitted local park/road plane. There are still zero
complete historical obstacle volumes and zero physical obstacle upper bounds.
HKPD, AMSL and radio altitude are distinct. A rendered gap is not an inferred wall.

The [building metadata](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html)
was freshly inspected: 21 September 2026 is its revision date, while the metadata
stamp is 22 September. V5 refers to the retained modern snapshot, not 1993 presence.
The original DTM features HTML was read after a fresh web timeout; it specifies
2014–2015 source photography and March 2019 revision. That modern surface remains
separate from the historical model.

The V5 checker counts 190 retained approach/final anchors and independently checks
225 ground-wind pairs, the declared 8,360-row NOAA routine subset of 8,549 annual
rows, 24 event-day records, rank counts 8,285/17/58, and the two event-hour gusts.
The retained NOAA format documentation, 12 January 2018, was read for true-from
wind direction, m/s scale and quality fields. The annual raw archive was not
reacquired or reparsed in this audit; the frozen derived CSV and its original
verification record are preserved. The weather and flight clocks remain unaligned.

## Bibliography and rights

The primary version-specific records for [Wu and Chen](https://arxiv.org/abs/2412.04797v1),
[Kim and coauthors](https://arxiv.org/abs/2405.16680v1), and
[FaSTrack](https://arxiv.org/abs/2102.07039v2) were freshly read. They support the
limited methodological comparisons: steady-wind Dubins planning, six-degree-of-freedom
landing optimization and planning/tracking separation. No algorithm was reproduced
and no guarantee transferred to a historical 747. The six Kim and eight FaSTrack
author names are preserved; Kim's 2024 v1 is not silently changed to the later v2.

[DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions) and
[CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC) were freshly inspected.
The former remains version 1.2, dated 26 May 2025. Source attribution, ownership,
as-is and nonendorsement conditions remain in the rights record and relevant
figure captions. No blanket license, institutional endorsement or redistribution
permission for accident-report/scholarly scans is inferred.

## Reproduction commands

From `whitepaper/v5`, in the pinned Python environment:

```sh
python scripts/verify_v5_science.py --fresh-bound
python scripts/verify_v5_figures.py
python verify_certificates.py
PYTHONPATH=evidence python -m pytest evidence/model/test_model.py evidence/model/test_review_solver.py evidence/model/test_review_trajectory.py evidence/counterfactual/test_counterfactual.py -q -p no:cacheprovider --basetemp=qa/science_pytest_tmp
```

Correctness, manuscript completeness and visual/editorial readiness are separate.
These receipts establish the first for their stated objects; the production audit
must establish the latter two. No original evidence, Version 4 file or accepted
scientific result was changed by this lane.
