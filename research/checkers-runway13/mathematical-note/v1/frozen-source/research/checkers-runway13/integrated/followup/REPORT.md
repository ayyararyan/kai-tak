# Threshold semantics and primary-survey follow-up — 13 October 2026

**Overall INCOMPLETE. No accepted historical registration, historical clearance or closed-form optimum.** The 1993-11-04 epoch, aircraft, 2,786 m LDA, frozen braking law, margin/effort objective and geometry-first gate are unchanged. This report supplements, not replaces, the canonical `../SPEC.md` and `../../PROJECT_STATE.md`.

## New diagnosis

The earlier “77.6–81.5 m threshold-registration discrepancy” is a discrepancy between **one image-derived threshold and a back-projection from an interpreted pavement endpoint**, not between two surveyed threshold positions. The latter calculation assumed that the selected pavement end was the declared landing-distance endpoint. That semantic link was never established.

Using the unchanged northern/southern fit outputs:

| Diagnostic | Result |
|---|---:|
| Fitted north-threshold to selected southeast pavement endpoint | 2,863.276 m |
| Smallest possible mismatch over **any** runway bearing with 2,786 m LDA | **77.276 m** |
| Mapped-axis residual, along runway / right | −77.267 m / +7.429 m |
| Mapped-axis norm, no endpoint offset | 77.623 m |
| Mapped-axis norm **conditional on a 61 m paved extension** | **17.883 m** |
| Short-photo-axis norm conditional on the same extension | 30.922 m |

The bearing-free lower bound follows exactly from the reverse triangle inequality:
`min_{||u||=1} ||N − (S − Lu)|| = abs(||S−N||−L)`.
It concerns supplied fitted points, not ground truth. Changing direction alone cannot close the original mismatch.

### A primary-source endpoint hypothesis, not a correction adopted as fact

Fresh inspection of CAD Report 1/95 found:

- Appendix 9, PDF page 143: southeastern concrete section labelled **152 m**.
- Section 1.10.1, printed page 27 / PDF page 34: the **last 91 m of runway 13** is concrete.
- Appendix 9: runway 13 strip length **3,392.5 m**; the report's runway/TORA length is **3,331.5 m**.

Both differences are 61 m. If the first two statements describe the same concrete section, and if the picked outer pavement endpoint is its downstream end, the declared runway endpoint would lie 61 m upstream of that pick. That hypothesis substantially explains the longitudinal residual. **The scan does not supply an explicit surveyed tie proving these endpoint identities.** Strip length is not automatically usable landing distance, and discrepancies between drawing and text could instead reflect reference conventions, editions or error. No 61 m offset is accepted, no endpoint is fitted to force agreement, and no physical uncertainty bound is manufactured.

The independent official CAD history page says the runway was extended to 3,390 m in 1975. That historical summary differs from the accident-specific declared distance. It reinforces the need to distinguish physical development length, runway declarations and pavement limits; it does not license replacing the frozen LDA.

### Camera-control weakness remains

A fresh leave-one-fit-control-out diagnostic retains the original fit/holdout roles. Removing the northern seawall control raises held-out RMS to about **111.6 m** and the uncorrected threshold mismatch to about **216.1 m**. Removing individual grass-island controls leaves approximately 75–79 m mismatches. The northern control layout depends strongly on its one off-strip seawall point. This is evidence of sensitivity, not grounds to delete that point or a calibrated confidence interval.

The new producer and seven tests are [diagnose_threshold.py](diagnose_threshold.py), [test_diagnosis.py](test_diagnosis.py), [threshold_diagnosis.json](threshold_diagnosis.json), and [tests.log](tests.log). Existing producers and the previous 36-test suite were not rerun.

## New exact primary-survey lead for the datum

Appendix 14, PDF page 160, is a **Photogrammetric Unit, Lands Department** drawing of the accident wheel tracks. Its title/control block explicitly states:

| Field | Source reading |
|---|---|
| Drawing number | **115-93 A** |
| Folder number | **404 Part II** |
| Plates | **72998, 72999, 73000, 73001** |
| Date of photography | **5 November 1993** |
| Control coordinates | **H.K. 1980 Metric Grid** |
| Control heights | **H.K. Principal Datum** |

See [full drawing](page160_full.png), [control block](appendix14_controlblock.png), and [title block](appendix14_titleblock.png). “Folder” is not relabelled a camera film identifier. Photography is after the accident, not proof of an unchanged November 4 scene. The drawing notes that plotted aircraft positions were supplied by the Civil Aviation Department; they are not calibrated in-flight envelopes.

This establishes that an accident-specific survey used HKPD, but **the published drawing does not print numerical control heights or a tie between those controls and the aviation 15 ft AMSL value**. Consequently `AMSL_to_HKPD_offset_m` remains null. The 1965–83 mean-sea-level relation in the Lands datum notes and current AIP's 2016-based relation do not identify which realization was used in the 1993 aerodrome declaration.

### Public archive check performed, with scope limits

The existing local AOI index contained 14,927 records and no matching date or plate identifier. Two direct targeted query formulations returned HTTP-service error 400; those failures are not interpreted as absent records. A simple year-count query succeeded. The follow-up then obtained the complete ID set and all **5,637 public layer-2 records for 1993**, without an AOI restriction, and checked actual `DATEFLIGHT` and `PHOTONO` fields. No November 5 record or matching plate identifier was present. Exact counts, saved chunk hashes and no-match result are in [survey_archive_check.json](sources/survey_archive_check.json); acquisition code is [query_survey_archive.py](query_survey_archive.py).

This is a bounded negative result for that public index, **not proof that the special-survey photographs or controls no longer exist**. The drawing's plate numbering need not match the public A-series naming convention.

## Obstacle-height investigation

No numerical historical roof/equipment top or hard height bound was newly accepted. The original approach chart, airport plan and wheel-track drawing were inspected; they do not provide a complete approach obstacle-top schedule. An enlarged checkerboard annotation remains unsuitable as an independently verified complete object-top bound. A 2014 IVAO chart contains readable coordinates/labels, but is prominently marked simulation-only and is not treated as primary historical evidence.

The official Buildings Department route was recovered from its raw online-tools HTML when lightweight text extraction omitted the links. Its [BRAVO information page](https://www.bd.gov.hk/en/resources/online-tools/BRAVO-online-building-records/index.html) explicitly requires a registered account to inspect/order private building records. The page was saved as [bravo_access.json](sources/bravo_access.json). No account was created, no login supplied, and no order or spending occurred. This route is relevant to private structures such as the Regal Airport Hotel and Po Sing Court; it does not establish coverage for public-housing blocks, government facilities or demolished structures. Approved plans would still need dated alterations and rooftop-equipment reconciliation.

### Routes actually tried

- Direct local primary report, source maps, original image-fit controls and inherited datum notes: inspected.
- Direct CAD history and report index: accessible; historical length context recovered, no 1993 control schedule.
- Current AIS home and GEN 2.1: accessible, not a 1993 realization statement.
- Geodetic control-network page: accessible, routes to the current map service; no historical airport control table obtained.
- Guessed geodetic height/level routes: application error pages despite HTTP 200; not counted as evidence.
- HKO tide landing page accessible; guessed datum page returned 404.
- Google lightweight retrieval returned a search shell; Bing returned irrelevant results; DuckDuckGo yielded chart leads before a human-verification challenge. No challenge bypass attempted.
- IVAO PDFs downloaded and inspected as **nonprimary discovery leads only**.
- Old EPD EIA report-directory route returned the revamped-site 404, not a historical height source.
- HKMS webpage retrieval had a certificate-chain failure; the already-established official API route succeeded without disabling TLS checks or changing configuration.
- Buildings Department official HTML and BRAVO information page: accessible; record inspection requires registered access.

No exhaustive internet or local-map-extraction claim is made.

## Exact missing input and minimum external action

The highest-value external input is the **control coordinate/level schedule and original georeferenced plan for Lands Department Photogrammetric Unit drawing 115-93 A, folder 404 Part II, plates 72998–73001, 5 November 1993**, together with the contemporaneous aerodrome declared-distance/end-light plan identifying the LDA endpoint and its benchmark tie to the published 15 ft AMSL. The published reduced scan lacks those numerical controls; the queried public aerial layer did not expose the identified survey.

Minimum action: obtain an existing copy from CAD/Lands archival holdings, or authorize a narrowly scoped custodian enquiry for those exact records. **No enquiry was sent.** One such schedule could resolve a datum/endpoint dependency but would not by itself supply all approach obstacles or aircraft calibration.

For the existing 15 mapped structure identities, the required input is dated roof and equipment elevations with reference datum, geometry and survey/alteration uncertainty, including vanished/changed structures. The private-building route requires BRAVO access; Housing Authority/government records are a separate dependency. Modern polygon heights and regulatory height limits are not substitutes for observed 1993 tops.

No model-meaning decision is required to preserve the current task. Accepting a scenario datum, statistical tolerance, changed epoch or reduced flight model would be a different decision and has not been done. The full derivation/proof requirements remain open behind the geometry/physical calibration gate.

## Verification and continuity

Seven new tests pass: synthetic reverse-triangle bound, offset sign/lateral invariance, coordinate-rotation invariance, inherited numerical residual reproduction, non-acceptance/null propagation, orthogonal decomposition and control-influence retention. Primary observation hashes, public-index completeness, unchanged inherited outputs and frozen inputs are recorded in [verification.json](verification.json). The previous verification receipt remains historical and unchanged.

Scientific completeness remains **16 requirements: 1 implemented, 10 partial, 5 blocked**. Zero accepted new complete obstacle volumes; zero new hard height bounds. No historical condition cell or optimum was enabled. The canonical ledger receives an append-only entry; no publication, outreach, spending, extra agents or inter-session coordination occurred.
