# Kai Tak: block matching and photograph-derived 3D

**Verified partial reconstruction, 13 October 2026. Full historical reconstruction: INCOMPLETE.**

[Open the offline 3D workbench](scene/index.html) · [Static preview](scene/overview.png) · [Download GLB](aerial_registration/observed_surface_mesh.glb) · [Browse sheet matching](candidates/index.html)

Actual 2 November 1993 photographs now supply a three-dimensional observed-surface model. Registered historical maps supply inspected structure outlines and a much wider matching queue. These are useful reconstructed geometry, but not yet a complete, independently accuracy-calibrated historical city. No modern building height has been passed off as a historical measurement.

## What was built

| Component | Delivered evidence |
|---|---|
| Survey registration | All 227 original map archives audited; three core maps registered and independently checked against printed grid intersections |
| Broad content matching | 94 editions across 93 sheet locations; 23,801 source/current-template pairs; 10,955 strong **unverified** candidates |
| Named source geometry | 45 visually inspected mapped faces for 15 named forms across October 1989, July 1994 and April 1997 |
| Local block work | Four road-centre matching cells; wider screening organized in 1,333 nonempty 200 m review cells, not claimed street blocks |
| Actual historical stereo | 1,318 sparse and 171,307 dense points from overlapping A36142/A36143 photographs dated 2 November 1993 |
| Observed-surface mesh | 225,371 triangles / 155,891 vertices; source image colour, unsupported holes retained |
| Viewer | Separate historical stereo, dated maps/matches and 2026 comparison views; no invented historical building extrusion |

The surface is nonwatertight: 86,061 boundary edges and zero nonmanifold edges. It contains observed roof, ground, vegetation and potentially erroneous image matches, not automatically classified buildings. No unseen backwalls, missing roofs or occluded ground were filled. The full dense correspondence mask retains failures; unknown does not mean empty space.

## Matching: what is accepted and what is only a candidate

[Reviewed faces](historical_faces.geojson), [source-grid faces](historical_faces_hk1980.geojson), [structure matches](structure_matches.json), [review decisions](manual_review_decisions.json), [modern spatial correspondences](modern_correspondences.json).

The inspected forms include four Mei Tung blocks, the market podium, Tung Tau Blocks 22/23, Lee Kau Yan School, Ng Wah College aggregate, Regal Airport Hotel, Po Sing Court, Kowloon City Market, a partial Lok Sin Tong Primary School face, the maternity home and Lee Kee dispensary. These are depicted faces or aggregates, not necessarily one complete footprint per physical building. The clinic seed returned an adjacent cartographic subdivision and was rejected. The school symbol/outline changes remain ambiguous rather than being forced into unchanged identity.

Each accepted face is pinned to the exact geometry, full candidate record, source archive and inspected overlay hashes. A modified label, date, height or geometry cannot inherit visual approval. The 72 modern-component spatial joins are correspondence evidence, not 72 historical buildings. All historical face base/top elevations and asserted volumes remain null. Matching an outline across map editions does not certify survival or exact geometry on 4 November 1993.

The broad screen compares current outline templates with actual historical raster ink and enclosed regions. It produces 10,955 strong-unverified, 7,055 ambiguous-content, 234 truncated-region, 2,936 low-support and 2,621 clipped pairs. There are 22,072 distinct current template IDs; multiple components/editions are not independent structures. It also exports 61,893 unclassified map regions, including 49,045 without substantial modern correspondence. Text, roads, courtyards and other symbols can form regions: none is automatically a vanished building. All 23,801 pairs still require identity interpretation beyond automated screening.

## Coordinate meaning and accuracy

| Quantity | Measured result | Interpretation |
|---|---:|---|
| Printed-grid registration RMS, three maps | 0.427 / 0.147 / 0.308 m | Raster-to-printed-grid consistency, not ground survey accuracy |
| Single-image local affine holdout RMS | 2.418 m | Four withheld ground road controls, local planar model |
| **Stereo metric alignment holdout RMS** | **5.754 m**, maximum 7.859 m | Four withheld survey-road controls; applicable check for this 3D alignment |
| Rectified stereo residual RMS | 0.341 pixels | Internal pair alignment, not absolute height accuracy |
| Dense points inside map-control hull | 3,780 / 171,307 | Most of the cloud is horizontal extrapolation beyond local control |
| Two inspected market roof features | 10.77 / 19.20 m above reference plane | Conditional estimated surface elevations, not height above each building's base |

Horizontal coordinates use diagnostic HK1980 grid alignment, EPSG:2326. **Vertical coordinates are metres relative to a fitted local park/road plane, not HKPD or mean sea level.** Four inspected ground tracks fit that plane. One withheld ground track has a −0.028 m residual but is not an independent camera/vertical calibration check. Do not use that number as a vertical accuracy bound.

The nominal camera uses the film-label 152.12 mm focal length, assumed 300 dpi metric scan scale and approximate principal point. Full film/fiducial/lens calibration is unavailable. A declared focal/principal-point sensitivity gives approximately 10.21–11.33 m and 18.19–20.20 m for the two roof features. These are **sensitivity ranges, not confidence intervals or hard error bounds**. They omit other matching, calibration and ground-reference uncertainty. The current surface is a conditional estimate, not a certified obstacle map.

PLY retains diagnostic E/N/relative-Z. GLB uses standard Y-up local coordinates `(E−837600, relative-Z, −(N−821200))`, with datum/origin in metadata. WGS84 face exports correctly identify EPSG:4326 and separately retain source-grid provenance.

## Use the viewer

Open [scene/index.html](scene/index.html) in a normal browser. Its required code, map images and scene data are embedded; no CDN is required. Keep the surrounding project for downloadable full-resolution assets and source links.

- **1993 stereo:** observed-surface patches by default; switch to points or wider coverage. The map-core view is not the whole approach. Grey map faces on the display plane are reference outlines, not ground or roof elevations.
- **Maps & matches:** select 1989, 1994 or 1997 and inspect the source-backed forms. Changing the map does not change the photograph's 1993 date.
- **2026 comparison:** 464 modern polygon components displayed with their own approximate HKPD base/top data and courtyard rings; ten invalid/missing/inconsistent components omitted explicitly. This view is never merged vertically with the historical relative-plane cloud.

Browser interaction is **unverified**: OpenClaw navigation policy rejected both the file URL and localhost preview. No bypass was attempted. Semantic tests, JavaScript syntax/UI-logic tests and a separately generated static preview are distinct checks and are recorded as such.

## Review and verification

See [validation.json](validation.json), [review decisions](reviews/DECISIONS.md), [requirement coverage](MODEL_REQUIREMENTS_TRACEABILITY.md), [stereo verification](aerial_registration/stereo_verification.json) and [mesh verification](aerial_registration/observed_mesh_verification.json).

Review led to substantive repairs: reject unsupported palette/nodata inputs; fail closed on changed archives; bind manual inspection to exact data; use true source coverage and raster-cell edges; refuse artificial clipping closures as strong outlines; gate sparse observations; retain modern courtyards; and require every contributing right-disparity interpolation pixel to be valid. The last defect removed 484 accepted image correspondences and 49 exported points. Old affected outputs remain under clearly named invalidated directories. The corrected cloud/mesh and current manifests are authoritative.

Correctness evidence is separate from completeness. Parent reran the delivered tests and artifact checks; exact counts/timestamps are in validation.json. All original sources and the aircraft model/configuration remain unchanged. No Git commit, push, publication, peer sync, purchase or external communication occurred.

## Remaining work, without reducing the agreed scope

Full block-by-block identity interpretation is still missing outside the inspected named forms; even those forms do not constitute complete building solids. Vanished/changed structures require further explicit geometry and date resolution. The broad matching queue is not completed matching. The reconstructed photo pair does not cover or validate the entire approach, runway or historical terrain.

Additional overlapping frame reconstruction and broader map controls can extend coverage with current sources. Reliable absolute heights and quantified spatial accuracy still need camera/scan calibration or validated self-calibration plus independent horizontal/vertical checkpoints and datum reconciliation. Roof/ground interpretation, occlusion repair supported by other views, and historical terrain/runway changes remain unresolved. These dependencies are not replaced by modern extrusions, guessed storeys, gap-filling or invented confidence intervals.

The overall request remains **INCOMPLETE**. The useful deliverable now is an auditable partial 1993 observed-surface reconstruction, dated inspected map geometry and a broad content-matching inventory. Nothing here changes or certifies the landing solution.
