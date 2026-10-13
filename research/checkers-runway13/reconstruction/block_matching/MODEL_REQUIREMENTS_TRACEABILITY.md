# Full-scope requirement audit

Frozen scope: [SPEC.md](SPEC.md). No requirement is removed or waived.

| ID | Status | Implementation/output | Verification and remaining gap |
|---|---|---|---|
| REG-01 | Implemented | register_sheets.py; registered/; registration_report.md | 227 archive/transform audits; 12 independent printed-grid checks on three digitization sheets; scan alignment is not ground accuracy |
| REG-02 | Implemented | aerial_registration/registration.json; sparse_stereo_report.json; control_points.csv | Local actual-image controls/holdouts and explicit camera/coverage limitations; no whole-frame orthorectification claim |
| MATCH-01 | Partially implemented | historical_faces.geojson; structure_matches.json; candidates/; candidates/road_cells/; road_cell_visual_observations.json | 45 inspected faces/15 forms, 23,801 screening pairs; four exact road cells with 202 per-cell template joins and eight inspected map observations; comprehensive changed/vanished identity resolution remains missing |
| HEIGHT-01 | Partially implemented | sparse/dense stereo points, inspected roof estimates, historical_3d_unknown_mask.geojson | Conditional relative-plane 3D recovered; historical face absolute heights remain null; independent vertical accuracy and complete geometry unresolved |
| SCENE-01 | Partially implemented | scene/index.html; scene.json; observed_surface_mesh.glb/.ply | Real partial surface, separate epochs and modern comparison; not complete historical physical buildings or approach terrain |
| VAL-01 | Partially implemented | tests, verification JSON, reviews/ | Reproducibility, geometry/date/hash/semantic checks pass; actual browser interaction blocked; independent absolute 3D accuracy/coverage not validated |
| OUT-01 | Implemented | REPORT.md; HANDOFF.json; validation.json; exported geometry and manifests | Reviewable partial result and explicit full-scope audit delivered; this reporting requirement does not discharge missing reconstruction |

**3 implemented / 4 partially implemented / 7 required. Overall INCOMPLETE.**
Correctness: tested outputs. Completeness: incomplete as above. End-to-end readiness: partial source-to-surface artifacts generated and checked; UI interaction unverified; full historical/aviation use not ready.
