# Kai Tak flight-data acquisition — 13 October 2026

## Result: partial recovery, requested BA dataset still unavailable

Downloaded the complete 226-page Hong Kong Civil Aviation Department Aircraft Accident Report 1/95 for CAL605, Boeing 747-409B B-165, 4 November 1993. This is an actual Kai Tak runway 13 approach, but an accident case, not a successful expert demonstration or the BA collection.

## Delivered

- `sources/CAD_1-95_CAL605_wayback.pdf`: full report, 7,653,178 bytes.
- `extracts/CAL605_DFDR_and_trajectory.pdf`: original PDF pages 150–159 (Appendices 11–13), 10 pages.
- PNG previews: figures 1–4; figure 3 contains column, wheel and rudder-pedal traces.
- `sources/CAD_1-95_CAL605.txt`: searchable OCR text; OCR errors remain.
- `published_summary.csv`: seven published aggregate facts, not individual BA flights.
- `REQUEST_DRAFTS.md`: unsent archive requests and verified contact routes.
- `manifest.json`: SHA-256 hashes and provenance.

## What the recovered report contains

Appendix 11 has approximately three-minute approach plots and 72-second detail with synchronized cockpit annotations. Variables include attitude, altitude, airspeed, heading, accelerations, control column/wheel, rudder pedals and engine indicators. The full recorder held 269 parameters; the published plots are only a selection. Thrust-lever angle was explicitly not recorded (PDF page 95). Figure 6 is the previous landing at Taipei, NOT Kai Tak. The approach track is on PDF page 158.

No raw binary recorder file or machine-readable synchronized time-series export was recovered. These are scanned plots; converting curves to numbers would produce approximate digitized measurements with calibration uncertainty, not recover original samples. No curves have been digitized or invented. This accident case must not silently become a normal-flight imitation-learning dataset.

## British Airways lead

Holtom's abridged article reports 1,079 approaches, 18 above 30 degrees and none above 35 degrees; all bank angles above 11 degrees were associated with Kai Tak runway 13. It does not establish that the entire 1,079-flight sample was Kai Tak. The bank-angle figure is explicitly absent. Full 1999 proceedings are catalogued, but no downloadable full paper or data attachment was located.

Article: https://theairlinepilots.com/forumarchive/flightsafety/foqaflightdataanalysis.php
Proceedings: https://ci.nii.ac.jp/ncid/BA54241467

## Acquisition provenance and search limitations

Report downloaded from: https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf
Original HKU endpoint timed out; the cited ASN mirror failed DNS. A BAAA mirror found in search returned 404 through web retrieval. Internet Archive download succeeded and PDF structure/text plus plotted figures 1–4 were inspected.

Targeted searches covered BA MaxVals/SESMA/Holtom, proceedings, Cathay, accident reports, GitHub-indexed sources and dataset catalogues. Dataset helper returned irrelevant Zenodo records; its Figshare/Hugging Face entries were fallback links, NOT successful API searches. Follow-up indexed searches found text corpora rather than relevant recorder datasets. This is not proof that no dataset exists.

LANTEX/NCAR is an additional archive lead, not acquired Kai Tak approach data: https://www.eol.ucar.edu/field_projects/lantex . Its public page concerns Chek Lap Kok atmospheric measurements, so it is not treated as a substitute.

Public availability of reports does not establish an open-data redistribution/training license. No commercial training rights are asserted. No emails or requests have been sent. No acquisition process is running in the background.

## Next acquisition step

Seek custodian confirmation/release for BA's historical MaxVals/SESMA records; separately seek the decoded CAL605 DFDR export from the current Hong Kong investigation authority and referral to the original UK AAIB readout archive. The drafts make these requests concrete without claiming archive survival or entitlement to release.
