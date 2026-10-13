# Visual atlas source, rights and coverage audit

Audit date: 2026-10-13. Scope: bounded inspection of canonical project records, source schemas and local files; no source geometry or original metadata changed. Paths below are relative to `research/checkers-runway13/` unless explicitly marked repository-root. This document supplements, not replaces, per-render input hashes and source manifests.

## Rights, source ownership and attribution

Public source pages and terms were freshly accessed on 2026-10-13. Repository-root `DATA_SOURCES.md` and `NOTICE.md` record the settled publication scope.

- [DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions), version 1.2, updated 26 May 2025, allow commercial/non-commercial distribution and reproduction subject to their conditions, source identification and acknowledgement of Government/relevant organisations' intellectual-property ownership. They also contain indemnity and as-is provisions. Do not describe the data as public domain or invent a Creative Commons licence.
- [CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC) similarly permit distribution/reproduction subject to attribution, retained ownership and the stated conditions. Identify Government and CSDI as sources; do not imply Government endorsement.
- [Digital Aerial Photo catalogue](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-aerial-photo) identifies Lands Department DAP-L0 as compressed 300 dpi JPEG imagery. Repository `reconstruction/chronology/aerial/README.md` documents the public OpenData requestQueue/queueStatus acquisition route and its CSDI terms link. `fullframe_manifest.json` records product, original source, exact acquired bytes and hashes. This route-specific permission is not permission for every Lands Department photograph or paid high-resolution product.
- [Old Survey Sheets catalogue](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-old-survey-sheets) identifies the open historical map product. Original sheet receipts are under `reconstruction/chronology/sheets/`; source ZIP/TFW/TIFF hashes and registrations are in `reconstruction/block_matching/registered/sheet_registration_inventory.json`.
- [Official terrain product specification](https://www.landsd.gov.hk/en/spatial-data/open-data/kf_dtm.html), [terrain catalogue](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-5m-grid-dtm/resource/620c4f4f-eac4-472f-9074-dffa2ad596fd), and [building metadata](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html) identify the modern products. These URLs are retained from the locally audited geospatial report; the terrain/building pages were not independently fetched in this bounded audit.

Use on images/gallery: **Source data: Lands Department, Government of the Hong Kong Special Administrative Region; CSDI Portal and DATA.GOV.HK. Government and relevant organisations retain intellectual-property ownership. Reconstruction and rendering: Aryan Ayyar. Data and derivatives are supplied as-is; no Government endorsement.** Add Buildings Department where documentary chronology is used. Link both terms pages in the gallery/source register. The original research/code has no additional open-source licence in repository-root `NOTICE.md`.

The initial atlas was prepared locally for author review. Aryan subsequently explicitly authorized pushing this atlas to GitHub on 2026-10-13. Source rights and attribution obligations remain unchanged. CAD accident-report/chart scans, Boeing manuals/drawings, paid imagery, private state and unsent correspondence remain excluded. Factual derived observations can cite them without reproducing restricted pages. Earlier broad restrictions in `reconstruction/SOURCE_REPORT.md` predate the settled open DAP-L0 route and must not be incorrectly applied to all included open imagery.

## Historical maps and footprints

Use `reconstruction/block_matching/registered/11-NE-11A_1989-10_core.png`, `_1994-07_core.png`, and `_1997-04_core.png` with their `.json` sidecars. These three present local files have matched bounds `[837500,821000,838250,821600]` metres EPSG:2326, image size 3000 x 2400, and 0.25 m raster sampling. Pixel-edge transform is E=837500+0.25*x, N=821600-0.25*y. Raster sampling is not ground accuracy. Individual object survey dates remain unknown.

`reconstruction/block_matching/historical_faces_hk1980.geojson` contains 45 reviewed depicted faces: 15 per edition. `source_epoch`, `source_id`, `source_sha256`, `source_archive`, `geometry_role`, `review_status` and `height_status` preserve provenance. All historical base/top heights are null. Render these as footprint/outline overlays, never arbitrary-height solids. `modern_correspondences` are candidate identities, not authorization to transfer 2026 heights backward. Blank Walled City map coverage is a cartographic omission, not historical emptiness. Source-map edition differences alone do not date construction/demolition.

For the wider airport, `integrated/geometry/runway_map_mosaic.png` and `map_mosaic_manifest.json` are already present. The latter supplies pixel-edge transform `[2,0,837500,0,-2,821600]` in EPSG:2326 and every source sheet/edition/hash. Label the mosaic as mixed historical editions, latest acquired before November 1993, not a single target-day survey.

## Airport, coastline and bearings

`integrated/geometry/mapped_runway_edges.geojson` gives two partial opposing mapped edge segments. GeoJSON is geographic display geometry; projected metre coordinates are `properties.EN_m`. The long-edge diagnostic gives approximately 134.02 degrees grid bearing and 61 m separation. These are genuine partial lines, not a full runway perimeter. Reference `integrated/geometry/mapped_runway_axis_check.json` and `integrated/REPORT.md`.

`integrated/geometry/historical_seawall.geojson` contains 14 digitized vertices from August 1993 sheet 11-NE-22D, source `1980_1990:1011`. Its `EN_m` and WGS84 geometry describe a partial southeastern seawall only. Top height, complete coastline, landmask and water-level law are unknown. Do not close this line to invent a verified peninsula.

`integrated/registration.json` explicitly has null threshold E/N, true/grid 1993 runway bearing and runway HKPD elevation, and `accepted_historical_registration=false`. Diagnostics disagree by approximately 77.62/81.54 m. The conditional 61 m pavement/declaration endpoint hypothesis is not accepted registration. Keep published physical runway length separate from 2786 m LDA; do not use LDA to silently construct pavement endpoints.

The historical chart gives 088 degrees magnetic localizer direction and 135 degrees magnetic runway direction, hence 47 degrees difference. A 1990 variation-derived true bearing is only a labelled scenario, not surveyed 1993 grid orientation. Any curved approach arrow is illustrative, not a recovered aircraft track or optimal-flight result.

## Checkerboard Hill: what can actually be placed

`integrated/geometry/historical_hill_terrain.geojson` has two partial November 1989 contours at 60 and 80 m HKPD, eight readable ground spots, and one unreadable spot. `properties.EN_m`, `elevation_HKPD_m`, `source_archive`, `source_tiff_sha256`, `source_pixel_edge_pick` / `core_pixel_edge_picks` and source-crop hashes link observations. The 60 m trace runs approximately E837142–837171/N821989–822018; the 80 m trace approximately E837104–837127/N822033–822069. These are labelled source observations, not a closed hill surface. A hill label may point to this evidenced region without claiming to mark the painted checkerboard face.

No exact surveyed painted-checkerboard face position/height was found. `reconstruction/chronology/record_visual_observations.py` records its visible presence in CN4581 on 1993-10-08 but explicitly no measured slope/elevation. Acquisition anchors are not survey: `aerial/acquire_previews.py` uses (114.185,22.337), whereas `chronology/render_report.py` uses (114.1832,22.335). Do not silently promote either to verified landmark coordinates. `integrated/followup/REPORT.md` also rejects a simulation-only chart as primary historical location evidence.

## Modern terrain, buildings and evidence classes

`geospatial/derived/Kowloon_KaiTak_DTM_5m_HK1980.tif` is locally present and uses EPSG:2326/HKPD metres. Photography is 2014–2015, publication 2017, product revision March 2019; later catalogue/server dates are not a new terrain survey. The acquisition rectangle is WGS84 [114.10,22.27,114.25,22.40]. The DTM contains offshore values and some vegetation/infrastructure: it is not a coastline mask or guaranteed bare earth. Any historical use is distinctly labelled context; unknown earthworks/reclamation cannot be assumed away.

`geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson` is the 2026-09-21 current inventory. BaseHeight and TopHeight are approximate HKPD elevations, not height above ground. Do not add TopHeight to the DTM. Missing/inconsistent heights and invalid geometry must remain omitted/flagged. Current buildings cannot populate 1993. The existing smaller modern adapter in `reconstruction/block_matching/scene/scene.json` is suitable for matched local extent and records omissions.

Directly supported mapped observations may have strong visual presence but still carry map accuracy limitations. Nominally calibrated stereo and approximate modern heights are conditional/approximate (Level B), not surveyed certainty. Unsupported regions are unknown (Level C); blank scene regions never mean historically empty land.

## Triptych: photograph to observed surface to interpretation

Use actual source originals `reconstruction/chronology/aerial/fullframes/A36142.jpg` and `A36143.jpg`, not a separate visually similar photograph. Both are 3000 x 3000 DAP-L0 images from 1993-11-02. Stable catalogue previews: [A36142](https://www.hkmapservice.gov.hk/OneStopSystem/map-search/productPreview?itemId=DAP&sheetNo=A36142), [A36143](https://www.hkmapservice.gov.hk/OneStopSystem/map-search/productPreview?itemId=DAP&sheetNo=A36143). Acquisition catalogue: `reconstruction/chronology/aerial/fullframe_manifest.json`; source interface: [HKMS aerial search](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA).

Date discrepancy remains recorded in `reconstruction/chronology/aerial/date_annotation_audit.json`: the latest independent inspection reads handwriting and stamp as 2.11.93, correcting the older 3.11.93 reading. Source metadata and accepted reconstruction use November 2; the correction must not disappear.

Source hashes pinned by `manual_stereo_labels.json`:

- A36142: `42da43eebfa6eae39597ea16d917f900986d80f7c069b909ebbe3563fc074767`.
- A36143: `e8439e24ffd7acbbaf7b5247b2fddbd7a52fd079e3c986481771efe204eaf289`.
- Original matched-track NPZ: `55af21bc665c3b95a26b9a6b1557751498844e97904377734862963f13d91081`.

Correspondence authority: `reconstruction/block_matching/aerial_registration/sparse_stereo_points.csv`. Each row links original `frame42_x/y`, `frame43_x/y`, `track_id`, EPSG:2326 E/N, and `z_above_fitted_local_park_road_plane_m`. `manual_stereo_labels.json` associates track IDs with inspected semantic labels and pins source hashes; never assign labels using row number after regeneration. `sparse_stereo_report.json` describes nominal camera K/R/t, fitted ground plane and map control. `sparse_stereo_transform.npz` is authoritative; `stereo_metric_cloud.npz` is rejected. Do not use invalidated dense files under `invalidated_dense_lr_blend/`.

Recommended linked marks below are copied from the actual CSV. Coordinates have storage precision, not corresponding physical accuracy. Z is NOT HKPD. These are sparse observed points to overlay on the same dense scene, not claims that each is an exact mesh vertex:

| Track | Inspected feature | A36143 original pixel x,y | E,N metres | Relative Z metres | Reprojection RMS px |
|---|---|---|---|---:|---:|
| 26 | municipal market north roof feature | 2313.100586, 734.276917 | 837508.976841, 821228.099284 | 10.769432 | 2.649546 |
| 708 | Carpenter Road visible ground point | 2352.135742, 939.580688 | 837634.943232, 821270.860498 | -0.028010 | 2.897164 |
| 788 | park paved-path intersection | 2393.859375, 733.630371 | 837500.477000, 821284.283609 | 0.165132 | 2.898231 |
| 1135 | municipal market south rooftop service structure | 2162.846924, 733.552246 | 837519.099115, 821129.257736 | 19.195491 | 2.414064 |

Photo pixels use the unchanged original image orientation. Any crop, rotation or resize must transform marks using the same image affine and record it. Do not flatten the perspective photograph onto the map rectangle; relief displacement matters. For the middle/right panels, overlay identical track IDs at their actual E/N/relative-Z and project through the recorded Blender camera. A small locator diagram or consistent north arrow can communicate differing photo/render orientations. Matching landmarks establishes source linkage, not exact viewpoint equivalence.

The accepted dense surface is `reconstruction/block_matching/aerial_registration/observed_surface_mesh.ply` / `.glb`, described by `observed_surface_mesh_report.json`; per-face/grid provenance is linked there. It contains 225371 triangles and 155891 vertices, deliberately nonwatertight. The 171307-point dense cloud is separate. No gaps are filled, roofs completed or back walls inferred. Standard Y-up GLB mapping is (x,y,z)=(E−837600,relative_height,−(N−821200)); PLY uses global E/N/relative-Z. Blender should use east/north/up consistently after explicit conversion.

Nominal calibration uses a 152.12 mm label, approximate principal point (1460,1440), no calibrated film/scan distortion and a locally fitted park/road reference plane. Map-control held-out RMS is 5.754 m, not a hard spatial bound. Sparse roof tracks 26/1135 are outside the map-control hull; disclose this when interpreting them. Absolute HKPD heights must not be mixed with relative stereo in one metric scene.

## Availability and checks in this bounded audit

The three map-core PNGs, A36142/A36143 originals, wide runway map mosaic, south runway map, DTM and the metadata/vector files discussed above were present locally when inspected. Large-data restore and exhaustive input checksum verification belong to the parent pipeline; presence alone is not an integrity verdict. The frame bytes were independently checked below against the source-pinned hashes while writing this audit. This source investigation did not revalidate every raw archive, inspect every render or certify broad reconstruction completeness.

- Fresh A36142 SHA-256 match: **passed** (`42da43eebfa6eae39597ea16d917f900986d80f7c069b909ebbe3563fc074767`).

- Fresh A36143 SHA-256 match: **passed** (`e8439e24ffd7acbbaf7b5247b2fddbd7a52fd079e3c986481771efe204eaf289`).

## Atlas review correction: full mosaic date range

Fresh inspection of all `map_mosaic_manifest.json` records identifies sheet **11-NE-16D, July 1986**. The full wide mosaic range is therefore **1986–1993**, not 1989–1993. The three matched core editions remain October 1989 / July 1994 / April 1997. Atlas captions, jobs and exported metadata use the corrected wide range. Contrast-graded display copies modify raster ink tones only, with no recovered-detail or new-geometry claim.
