# Version 3 — mathematical claims and publication verification

**Status: complete local manuscript package.** Verified 13 October 2026, final checks at 16:56 UTC. Exact title **Checkers with Runway 13**. The publication assignment is complete; the broader programme of historically calibrated optimal landing research remains incomplete.

## What was delivered

33-page PDF: eight narrative parts, seven explanatory insights,16 scientific figure composites, six technical appendices and14 references. Editable LaTeX/bibliography, scripts and frozen figure inputs,51-row claims/evidence ledger, figure attribution, build instructions, abstract, executive summary and V2→V3 changelog accompany it. The471-word first-person foreword is explicitly for Aryan's review. There are no placeholder sections/images.

Final PDF SHA256:
`c517517899088cb72a82be5f76e73767846aab3925fd0d418a6f13cf14959ea3`

## Correctness: fresh checks performed

| Check | Result | Evidence |
|---|---|---|
| Existing model/counterfactual suite |89 passed in 2.71 s, original repository context | `qa/model_counterfactual_tests.log` |
| Portable copy of same collection |89 passed in 3.67 s in newly installed Python 3.14 environment | `qa/portable_tests.log` |
| Immutable evidence |104 full-package input hashes and inherited67-file V2 subset match | `SOURCE_MANIFEST.json`, `evidence_manifest.json`, build logs |
| Calm scalar outcomes and polynomial endpoints | Touchdown313.492181158m;stop2531.321117620m;remaining254.678882380m;time96.286902270s | `qa/figure_checks.json`; `verify_v2_inputs.py` |
| Wind formula/CSV, density/EAS and ground outcome | Touchdown302.114052038m;stop2233.230845017m;remaining552.769154983m;time96.644053677s | `qa/figure_checks.json`; source-bound formula andCSV |
| Calm fixed-witness interval proof | Certified η≥0.0397;2,502 intervals; exact original cover reproduced | `qa/fresh_calm_certificate.json` |
| Wind fixed-witness interval proof | Certified η≥0.1507934696816132;376 intervals; exact original cover reproduced | `qa/fresh_wind_certificate.json` |
| Clean-folder proof reruns | Both certificates pass again from portable source-only staging | `qa/clean_calm_certificate.json`, `qa/clean_wind_certificate.json`, `qa/clean_certificates.log` |
| Calm regularity lemma and family upper bound | Full-box vertical speed<14 m/s; feasible horizontal speed>68 m/s; root bracket[.1559771,.1559772]; exact stored result reproduced | `qa/fresh_existence_bounds.json`; `verify_v3_claims.py` |
| Wind necessary upper bound and gap | Exact fraction66656817/307536544; gap1584555818464679384939/24026292500000000000000 | `qa/figure_checks.json`; exact rational recomputation |
| Explanatory calculations | Bank/radius/time, wind projection, descent, quadratic braking sensitivity and ground decomposition agree | `qa/insight_calculations.json`, `qa/v3_claim_checks.json` |
| Historical derived values | Weather count/rank/event values and conditional stopping arithmetic recomputed | `qa/figure_checks.json` |
| Source/provenance scope | Original reports and metadata read; evidence categories, image terms,14 citations checked | `CITATION_VERIFICATION.md`, `RIGHTS_AND_PROVENANCE.md`,51-row ledger |

The two certificate reruns use the original source-bound proof code, not an independently authored second verifier. Scalar calculations and formula/CSV checks provide complementary checks but are not independent human peer review. A certificate checks the exact real-decimal parameter construction. Floating polynomial exports and printed rounded coefficients are not silently promoted to that exact object.

### Diagnosed issues retained, not concealed

The first wind-proof run stopped because the initial compact package lacked the source-bound original corridor replay dependency. The required source file was restored byte-for-byte, its hash retained, and the unchanged checker passed. `qa/certificate_rerun.log` retains that initial failure locally; `qa/wind_certificate_rerun.log` records success. This was packaging incompleteness, not a changed scientific model. No certificate was reported as passing on the failed run.

Visual review corrected an accidental colour map on a grayscale aerial, crowded panel headings, an undersized 3D view, a cover paragraph break, two orphan pages and a crowded scenario legend. The revised final 33 pages were checked. The source-date conflict discovered on A36143 remains disclosed rather than cosmetically repaired.

## Completeness: specification audit

`REQUIREMENTS_TRACEABILITY.md`:10 required components;10 implemented;0 partial;0 missing;0 blocked. Required calm/wind arms both retained. No unapproved model changes, exclusions or proxy substitutions. All 16 figures have reproducible generators, linked inputs, units or an explicit schematic interpretation, source attribution and limitation-bearing captions. Seven insight objects are documented in `INSIGHTS.md`.

The scientific conclusions deliberately **do not** include calibrated historical flyability, complete obstacle clearance, near/global optimality, physically calibrated prediction intervals, a gust-robust causal control policy, or improvement over an equivalent historical baseline. Those are identified limitations, not missing manuscript sections.

## End-to-end readiness: document and portable rebuild

- Tectonic 0.17.0 compiled the complete manuscript. No overfull boxes, missing glyphs or unresolved citations/references remain. PDF title metadata exactly matches the required title.
- PyMuPDF and Poppler both extract readable text. Fonts are embedded with Unicode mapping. Text bounds and 64 links were checked; the existence of links is not a guarantee that every external server remains reachable.
- Every page was rendered and visually inspected. `qa/visual_inspection.json` binds the33-page review to the final PDF hash. Automated geometry checks supplement, not replace, that review.
- A separate source-only staging directory, with no generated figures, TeX intermediates or existing PDF, rebuilt successfully using a new Python 3.14.6 environment. All 33 pages have **identical extracted text and identical rendered pixels** to the delivery PDF. PDF bytes differ between compilations; bit-for-bit PDF reproducibility is not claimed. `qa/clean_rebuild.json` contains both hashes and per-page results.
- The clean run uses the same machine and installed Tectonic/Poppler; cross-platform rendering and an offline first installation were not tested. Exact Python dependency versions are in `requirements.txt` and `qa/clean_environment_versions.txt`.
- `package_sources.py` creates the source ZIP, checks ZIP integrity, and verifies each archived member byte-for-byte against its local source. `DELIVERY_MANIFEST.json` records its count, digest and the included PDF digest. Rendered review images, caches, virtual environments and TeX intermediates are excluded from the portable archive; page renders can be regenerated.

## Preservation and publication state

Baseline repository commit:0798c76. All 1,517 pre-task tracked files were hash-compared. The only changed pre-existing tracked file is the authorized append to `research/checkers-runway13/PROJECT_STATE.md`. Version 2 and all original scientific/source artifacts are unchanged; `qa/preservation_check.json` records this. Version 3 is new work under `whitepaper/v3`.

No commit, push, public release, institution contact, announcement or peer-machine synchronization was performed. The local source ZIP is a delivery artifact, not evidence of publication. No independent peer review or expert endorsement is implied.

## Not rerun / not established

Full optimization searches, historical source reacquisition, dense photogrammetry, new flight-data digitization and a complete obstacle reconstruction were not rerun for this editorial assignment. Existing settled artifacts and their provenance were inspected, then the manuscript's numerical calculations and retained mathematical certificates were recomputed. Underlying historical measurement uncertainty remains uncalibrated. The inherited review documents are historical research records, not a new review of Version 3.

Author review of the first-person foreword remains requested by the brief. Choosing an original-work open licence and authorizing external publication remain separate decisions; neither is necessary to read, inspect or locally rebuild this complete manuscript.
