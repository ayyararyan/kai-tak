# Atlas v1 — requirements traceability

The full supplied sixteen-section brief remains controlling. These eight requirement groups cover it; the twelve subject-level alternatives are specified in `storyboard/storyboard.json` and visible on the plates. No scope or historical meaning was changed during implementation.

| ID | Requirement | Status | Implementation/output | Verification / limits |
|---|---|---|---|---|
| DATA-01 | Repository inventory, restoration, source hashes and rights | Implemented | `metadata/input_manifest.json`, `restore_receipt.json`, `rights.json`, `SOURCE_AUDIT.md`, `reconstruction_register.json`; `scripts/prepare.py` | 1,254 archive members restored/verified; 25 declared original hashes current; route-specific photo rights gate; missing scientific quantities recorded |
| DESIGN-01 | Complete twelve-subject public storyboard and source-limited alternatives | Implemented | `storyboard/storyboard.json`; captions and README shortlist | All twelve subjects represented, including explicit bounded alternatives for wide geography/approach/signature |
| SCENE-01 | Reproducible source-linked Blender scenes, coordinate/datum integrity | Implemented | `scripts/render_scene.py`, `make_jobs.py`; 17 `.blend` scenes/jobs; `metadata/cameras.json` | Original full mesh/triangle order preserved, GLB mapping independently checked; compatible coordinate/datum objects only; two representative fresh-process rebuilds |
| RENDER-01 | Twelve outputs, styles/lights/modes/cameras and publication formats | Implemented | 12 annotated and 12 clean 4K plates; 17 base 4K views; 3 evidence variants; daylight variant; WebP, 12 A4 layouts/PDF, 6 square/vertical crops, transparent legend | Dimensions/metadata and view matching checked; all principal plates visually inspected. Artistic quality is submitted for author review, not independently certified |
| COMP-01 | Matched historical and modern comparisons | Implemented | `comparisons/`; plate09 (1989/1993/1994/1997); plate10 (historical/2026); triptych11 | Fixed camera/extent records; map-edition versus photo dates and relative/HKPD differences retained; no construction dates inferred |
| OUT-01 | Static exhibition gallery, downloads, explanation and recommendations | Implemented | `gallery/index.html`; `README.md` | Static links and JavaScript syntax pass; 12 logic checks pass with DOM stub. Actual browser interaction remains unverified under VAL-01 |
| VAL-01 | Geographic/historical/visual/reproducibility verification | Partially implemented | `qa/acceptance.json`, `reproducibility.json`, `REPORT.md`, review decisions, contact sheets | 157 acceptance checks pass; two regenerated scenes match decoded RGB pixels; checksum rejection succeeds; image inspection completed. Browser layout/interaction verification blocked by navigation policy |
| OPS-01 | Canonical state, versions, output hashes and reproducibility handoff | Implemented | `PROJECT_STATE.md`, this file, README, environment/requirements, `metadata/artifact_manifest.json` | Local source and delivered output inventory; GitHub publication subsequently authorized; no peer sync; original scientific files preserved |

**Coverage:** 8 requirement groups: 7 Implemented, 1 Partially implemented, 0 Not implemented. All 12 requested image subjects have delivered source-bounded alternatives. Overall: **implemented/rendered for local author review; final browser acceptance incomplete**.

## User-brief coverage map

| Brief section | Requirement groups |
|---|---|
| 1 Existing evidence and archive recovery | DATA-01, SCENE-01 |
| 2 A/B/C hierarchy and selectable modes | DESIGN-01, SCENE-01, RENDER-01, OUT-01 |
| 3 Visual design and two styles | DESIGN-01, RENDER-01 |
| 4 Twelve-image storyboard | DESIGN-01, RENDER-01 |
| 5 Camera variations and registration | SCENE-01, COMP-01 |
| 6 Reproducible stack and coordinates | DATA-01, SCENE-01, OPS-01 |
| 7 Materials and two lighting rigs | SCENE-01, RENDER-01 |
| 8 Accessible images, captions and provenance | DESIGN-01, RENDER-01, OUT-01 |
| 9 Historical safeguards | DATA-01, SCENE-01, VAL-01 |
| 10 Resolution and formats | RENDER-01 |
| 11 Versioned directory and original-source preservation | OPS-01 |
| 12 Standalone local gallery | OUT-01, VAL-01 |
| 13 Science, presentation and reproduction QA | VAL-01 |
| 14 Deliverables and white-paper shortlist | All; README shortlist |
| 15 Source-led priority order | PROJECT_STATE execution record |
| 16 Public accessibility, truth and author review | All; author aesthetic acceptance remains human review |
