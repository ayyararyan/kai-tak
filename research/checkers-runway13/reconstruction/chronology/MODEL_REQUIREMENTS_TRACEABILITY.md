# Historical reconstruction evidence: requirement audit

13 October 2026. **7 requirements implemented; 1 partially implemented. Overall historical reconstruction: INCOMPLETE.** These statuses concern the source/evidence specification, not the aircraft model or completion of all historical structures.

| ID | Status | Implementation and artifacts | Verification / remaining gap |
|---|---|---|---|
| DATA-01 | Implemented | `sheets/acquire_indexes.py`; 72,691 whole-HK / 18,440 local index editions | Complete family counts, unique IDs, cached-response hashes |
| DATA-02 | Implemented | `sheets/acquire_sheets.py`; 227 selected editions at 93 locations, previews | All hashes and CRCs; cited image contents inspected. Selected set, not every indexed map |
| DATA-03 | Implemented | `aerial/`; 14,927 frames indexed, 48 fullframes and 47 previews acquired | Complete index count/IDs; image decode/hashes; date annotation inspection |
| JOIN-01 | Implemented | `match_sources.py`; 69,915 current-feature candidates, 16,968 sheet/frame pairs | Month/date boundaries, exact index-polygon intersections, positive fractions; coverage matching only |
| CLASS-01 | Implemented | `structures/chronology.py`; all 342,195 current polygons, 71,382 linked to records | 39 semantic tests; source count/ID audit, two dates, full snapshot repair comparison; no vanished identities recovered from this graph |
| CLASS-02 | Partially implemented | `historical_visual_observations.csv`; 52 observations, 17 named objects/sites | Three sheet editions and three fullframes inspected by parent; source-backed vanished-site changes. Comprehensive image interpretation, historical identities and footprints missing |
| OUT-01 | Implemented | `REPORT.md`, `coverage.png`, `source_comparison.png`, CSVs, `HANDOFF.json`, uncertainty mask | Counts reconciled, figures visually inspected, paths/hashes verified. Delivered evidence package, not a reconstructed city |
| VAL-01 | Implemented | `validate_delivery.py`, `test_matching.py`, structure tests, review repairs | 46 regression tests; archive/image/source/export checks; independent code and artifact review. Historical geometry/clearance unverified |

No unapproved aircraft/model change or missing-data proxy substitution. Arbitrary-date documentary queries work within evidence support. Source matching exports are explicitly the 1993 example. No complete arbitrary-date city, historical heights or reconstructed 3D mesh exists. Missing full scene and identity work is not waived.
