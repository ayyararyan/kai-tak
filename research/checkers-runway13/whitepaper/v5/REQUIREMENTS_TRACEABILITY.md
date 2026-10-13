# Version 5 requirements traceability

Authority: [SPEC.md](SPEC.md) and [the authorized request](editorial/AUTHORIZED_REQUEST.md). No scientific scope reduction or proxy substitution was authorized or made.

**Status convention:** All 19 requirements are implemented and their acceptance evidence is closed in `VERIFICATION.md`. Correctness, completeness and delivery readiness remain separate findings. The final clean extraction reproduced every page and figure export; all 38 actual pages have artifact-bound visual acceptance.

| ID | Status | Implementation and acceptance evidence |
|---|---|---|
| V5-01 | Implemented | `editorial/DIAGNOSIS.md`; inspection of all 35 baseline pages; `editorial/CAVEAT_AUDIT.csv`; `qa/caveat_audit_checks.json`. |
| V5-02 | Implemented | Seven-act narrative; `editorial/NARRATIVE_MAP.md`; four compared openings in `editorial/OPENING_ALTERNATIVES.md`; baseline claim map. |
| V5-03 | Implemented | Complete rewrite of `sections/act1.tex` through `act7.tex`; `editorial/BEFORE_AFTER.md`; final independent reader review. |
| V5-04 | Implemented | `abstract.md`; new introduction in Act I; concise, author-review-marked `sections/foreword.tex`. |
| V5-05 | Implemented | `01_place` and `02_bearings`; original source frames and map; provenance records and explicit nonregistration labels. |
| V5-06 | Implemented | Act II force balance and worked example; `03_turn` links force vectors, clockwise turning arc and radius curve. |
| V5-07 | Implemented | `04_landing`: equal-metric orthographic scene, flare detail and unaltered height profile. |
| V5-08 | Implemented | `05_runway`: common 2,786 m scale; exact touchdown, delay, braking, stop and remainder allocations. |
| V5-09 | Implemented | `07_stereo`: original-photo correspondences, retained open mesh, mapped Market and support hull; conditional heights and outside-hull qualification. |
| V5-10 | Implemented | `08_wind`: one wind vector viewed from two track frames; Act V explanation and separate-scenario qualification. |
| V5-11 | Implemented | `10_recorder`: 123 anchors and reading sensitivities; `11_weather`: irregular independent clock; `12_rollout`: report-stated landmarks; `A3_weather_context`: full empirical support. |
| V5-12 | Implemented | `09_certificate`: exact pedagogical interval enclosures; the two actual fixed-witness proofs reproduced separately. |
| V5-13 | Implemented | `CLAIMS_AND_EVIDENCE.csv`: 53 rows, including all 51 baseline IDs; source/manuscript checks; 26 retained mathematical blocks; unchanged coefficient tables. |
| V5-14 | Implemented | Preserved RFS style and class; `FORMAT_PROVENANCE.md`; embedded-font and page-geometry checks. |
| V5-15 | Implemented | Named PDF, editable sources, 15 PDF/SVG/PNG figure masters, 15 high-resolution presentation exports, scripts and evidence-linked inputs. Portable source ZIP built, extracted and reproduced in a fresh Python environment. |
| V5-16 | Implemented | `VERSION_CHANGES.md`, `editorial/BEFORE_AFTER.md`, `FIGURE_REDESIGN.md`, `SCIENTIFIC_VERIFICATION.md` and `EDITORIAL_ASSESSMENT.md` present. Completed `REPRODUCIBILITY.md` and `VERIFICATION.md` bind the clean-build and delivery checks. |
| V5-17 | Implemented | PDF font/reference/layout checks and individual actual-page reviews performed on the production builds. Final float pages reinspected; all 38 page texts/pixels and 60 figure exports match a clean rebuild. `qa/visual_inspection.json` and `qa/clean_build_verification.json` bind the accepted artifacts. |
| V5-18 | Implemented | `editorial/FINAL_INDEPENDENT_REVIEW.md`: post-technical-gate review, E1–E5 dispositions and revised-content acceptance. Final production-page checks remain separate. |
| V5-19 | Implemented | All 238 V4 files checksum-checked; separate `editorial/v5` worktree; no external publication; author-review label retained on the foreword. |

All **19 requirements** remain represented. Mathematical/source checks establish correctness of the retained objects; row coverage establishes the specification's accounting; clean source-package reproduction and artifact-bound page inspection establish delivery readiness. None establishes historically calibrated flight performance, unaided human authorship or human specialist peer review.
