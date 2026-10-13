# Independent acceptance audit

**Audited 2026-10-13, 13:31 UTC. Verdict: useful, evidence-linked partial reconstruction; full frozen request INCOMPLETE.**

Read the entire canonical working agreement and `SPEC.md`. Reviewed actual registration records, accepted geometry, match records, screening totals, sparse/dense CSVs, scene data, producer and viewer code, verification records and the newly written report/traceability. This is an acceptance audit, not a second implementation or independent survey. No source or implementation files were changed by this reviewer.

## Prioritized findings

### A1 — High: blockwise identity reconstruction remains incomplete

`MATCH-01` is not discharged by 23,801 screening pairs or 45 inspected source faces. The latter are 15 named cartographic forms repeated across three map editions; the former explicitly contain zero verified historical-building identities. The 72 current-component joins remain spatial candidates. Changed, vanished and split/merge structure histories are not comprehensively resolved.

All four road-control cells have `contents_verified=false`. Independently intersecting their actual polygons with the 15 October-1989 accepted forms finds only the Lok Sin school face inside those cells; the other 14 are elsewhere. Thus the four cells and 15 forms are useful but largely different subsets, not four completed block inventories.

**Action:** keep MATCH-01 partial; continue explicit cell-to-structure assignment and source/date/identity acceptance, including unmatched historical map forms. Do not treat automated screening or modern absence as historical presence/absence. The current report already states overall incompleteness and should retain that distinction.

### A2 — High: historical height/scene completeness and accuracy remain unresolved

The delivered 171,307 dense points and 225,371 triangles are actual conditional image reconstruction, not invented building extrusions. Nevertheless, the mesh is unclassified, incomplete surface patches; it cannot stand in for complete historic buildings, terrain or the whole approach. All 45 accepted cartographic faces retain null historical base/top heights. Two interpreted roof tracks measure elevation relative to a fitted park/road plane, not their own building bases or HKPD.

Only 3,780 dense points and 14 sparse points are inside the local map-control hull. Independent CSV inspection also finds dense relative Z from approximately −19.00 to 121.54 m; these values must remain observations under the stated model, not silently reclassified or clipped into a flat-ground city. Internal consistency and nominal-intrinsic sensitivity are not independent physical error bounds.

**Action:** retain HEIGHT-01/SCENE-01 partial; continue available additional-view/control, building-surface interpretation and coverage work, with datum/calibration dependencies explicit. Do not call a functioning viewer or nonwatertight surface a completed historical reconstruction. Current wording correctly preserves these limitations.

### A3 — Medium: browser acceptance remains genuinely unverified

The static preview is legible and the delivered HTML contains the claimed modes and controls. Code inspection shows modern HKPD walls are isolated from relative-plane stereo, historical faces are display-plane outlines only, sparse rejection flags are respected, and modern inner rings are retained. These facts do not establish actual Plotly/WebGL rendering or click/orbit/selector behaviour in a browser.

**Action:** retain `browser_interaction_verified=false` and VAL-01 partial until the real delivered interaction can be tested through an allowed browser path. Parent reports navigation-policy failures; this reviewer did not attempt a bypass. A Node stub test is not a browser test.

### A4 — Low, reparable documentation issue: unsupported estate grouping

The initially reviewed `REPORT.md` calls Shing Tung, Mau Tung, On Tung and Hong Tung the “four Mei Tung blocks.” The inspected map supports those individual names, not that estate grouping; nearby Mei Tung Road is not evidence for it.

**Action:** use the four source-backed house names explicitly unless an authoritative estate attribution is supplied. Parent was notified during review. This wording issue does not alter accepted geometry.

**Resolved during audit:** fresh reread confirms the unsupported “four Mei Tung blocks” phrase is absent from the updated report. No remaining geometry impact.

## Seven-requirement acceptance coverage

| ID | Acceptance assessment | Evidence and limit |
|---|---|---|
| REG-01 | Implemented for the audited archive inventory and accepted digitization subset | Inventory records 227/227 archive/transform checks; independent printed-grid records cover 12 points across the three accepted map editions. The other 224 sheets remain independently unchecked. Broader screening geometry must not inherit those three sheets' grid validation. |
| REG-02 | Implemented bounded registration/diagnostic | Actual road content controls, six fit/four holdout points, distinct 2.418 m affine and 5.754 m stereo holdout RMS. No full-image orthorectification or calibrated height claim. |
| MATCH-01 | Partially implemented | 45 faces/15 forms, recomputable cross-map IoU, 72 modern spatial joins, screening work units and unresolved records. A1 prevents full acceptance. |
| HEIGHT-01 | Partially implemented | Genuine conditional stereo, inspected roof tracks and full-area unknown mask. A2 prevents full height/geometry acceptance. |
| SCENE-01 | Partially implemented | Portable embedded scene, source-linked machine-readable outputs and separate dates/datums. Not full physical buildings or whole-approach terrain; interaction unverified. |
| VAL-01 | Partially implemented | Strong integrity/reproducibility evidence and inspected static imagery. Browser interaction, independent absolute 3D accuracy and full geographic/semantic completeness remain unverified. |
| OUT-01 | Reporting requirement implemented in report/traceability; final package assembly pending at audit time | Report is readable and explicitly incomplete; geometry/provenance exports inspected. Parent was still producing aggregate `validation.json` and `HANDOFF.json`; those final files were not accepted by this reviewer before creation. |

No requirement is waived. The three implemented reporting/registration components do not make the full scope complete.

## Fresh evidence obtained by this reviewer

- Independently loaded all 45 accepted source geometries: valid and nonempty; historical base/top heights null; geometry hashes match their reviewed manifest entries.
- Recomputed all 45 stored cross-map IoUs from actual polygons; all agree numerically.
- Recomputed scene source-file hashes and every mesh-input hash; all agree with their recorded bindings.
- Read the actual sparse and dense CSVs: 1,318 and 171,307 rows; counted 14 and 3,780 control-hull flags respectively.
- Reconciled the scene's 155,891 mesh vertices and 225,371 faces, and its 45 historical faces, against producer counts.
- Independently checked the uncertainty-mask bounds: 114.10–114.25 E, 22.27–22.40 N. It preserves broader acquisition-area uncertainty rather than implying the small reconstructed core is complete.
- Inspected the actual October-1989 digitization overlay and final static 3D preview. The overlay provides legible source-linked forms while visibly retaining omitted/unreviewed city areas. The mesh preview visibly consists of patches and missing areas, not complete solids. This was sampled visual review, not reinspection of every historical object or a browser screenshot.
- Inspected current verification artifacts: candidate checks 944/944, sparse/dense checks 24/24 plus 25 guardrail tests, mesh checks 24/24, and scene semantic tests 11. These are producer/parent recorded runs, not claimed as fresh reviewer reruns.

## Audited artifact identities

| Artifact | SHA-256 |
|---|---|
| `SPEC.md` | `ca5253b96712b4d5fd98d40bf30d09e64d4fb06549cdcfb691a9ec5d247d5621` |
| `scene/scene.json` | `734ca0e43995571686de9a43cc7b0522a1cf55d1c97d868f66fb2ed7ca1e34e8` |
| `scene/index.html` | `74089d5c20c3abd7faf8476c0af35e8a84969f956aeaab98ebe521e9cce9bfc5` |
| `historical_faces_hk1980.geojson` | `ababd2644f766efb29a79eb02d4a73ffd09893f74190c1e5f464e75627c3bb2e` |
| `aerial_registration/dense_stereo_points.csv` | `634aa4f28a4d7e80014c48eae199ce829a72d0b5461aaf7e7beeb9a1c8a0dba9` |
| `aerial_registration/observed_surface_mesh.ply` | `49866bd77fd74a04f8ba18e8a734d05ee169b2ddd9bc7d74b6039800869a8323` |

**Correctness:** inspected invariants and current artifacts agree; no additional delivered-geometry defect established by this audit. **Completeness:** incomplete. **End-to-end readiness:** bounded source-to-surface output verified; browser interaction and full historical reconstruction not accepted.

## Final assembly audit — 2026-10-13, 13:34 UTC

Fresh read-only inspection now includes the completed `HANDOFF.json`, aggregate `validation.json`, updated report and updated specification. This supersedes the earlier OUT-01 assembly-pending note: **the reporting/export handoff is now assembled and its stated partial status is consistent**. It does not supersede A1–A3 or complete the reconstruction.

Independent checks performed after final assembly:

- **30/30 handoff artifact byte sizes and SHA-256 bindings match the actual files.**
- **489/489 candidate-manifest file sizes and SHA-256 bindings independently recomputed and match.**
- Handoff, scene and producer counts agree: 171,307 dense points, 3,780 inside the control hull, 225,371 surface triangles, 155,891 surface vertices, 45 mapped faces and 15 distinct named forms. Screening remains 23,801 unverified pairs.
- Every exported historical scene face still has null physical volume, relative building height, base HKPD and top HKPD. Handoff hard-height intervals and height-error confidence intervals are null, not zero or invented bounds.
- Handoff flags explicitly deny query-date presence certification, absolute-datum reconciliation, verified screening identities, completed road-cell contents, watertight/building-classified surfaces, clearance certification and browser verification. Report, scene, specification status and aggregate validation all say the full reconstruction remains incomplete.
- Photo date (1993-11-02), example query date (1993-11-04) and three map edition months remain distinct. Modern comparison remains a separate epoch and vertical datum.
- The aggregate Python count reconciles to **21 + 10 + 25 + 11 = 67**. The recorded 944 candidate checks and 24 stereo/24 mesh checks agree with their underlying verification records. These test-run records were reconciled, not rerun in this bounded final audit. Node UI logic remains explicitly stubbed, not browser/WebGL verification.
- Updated report uses the four source-backed house names and explicitly states that only the school face overlaps the four road-control cells; A4 is resolved without changing geometry.
- The specification now records `incomplete-verified-partial-delivery` and adds a suggested review order. Its reviewed scope and seven requirements remain intact.

Final assembly identities:

| Artifact | SHA-256 |
|---|---|
| `HANDOFF.json` | `9311455a95ff9912a59138fcccc8a6cdf120a632f7923b80355d5bcd1cb36aff` |
| `validation.json` | `c441ec85ae1d44c48527d9083d6d6b04e0b1ee4c674491f9f676e110bbaeb349` |
| Updated `SPEC.md` | `4c66de2cb65902c9e706856ff933bf73c9f08fa2c399d365786a259e9446ecdf` |
| Updated `REPORT.md` | `7777a06d303c56a49aba38827320b88d515f1bee52eaff67fdb125cc75a39ae6` |

**Final bounded verdict:** assembled partial handoff passes the inspected integrity/semantic checks; no new discrepancy found. Full scope remains incomplete, and actual browser interaction remains unverified.
