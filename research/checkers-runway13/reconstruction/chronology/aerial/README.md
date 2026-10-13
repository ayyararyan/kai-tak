# Historical aerial evidence acquired for Kai Tak

Acquired and checked 2026-10-13. This directory now contains **actual historical aerial photographs**, not only an index or numeric values. It is source evidence for a dated reconstruction, **not a 3D reconstruction and not a completed building classification**.

## Verified deliverables

- **14,927 unique aerial frame index polygons**, spanning **316 capture dates during 1985–1998**, intersect the project acquisition rectangle WGS84 `[114.10,22.27,114.25,22.40]`. **1,277 are from 1993.** The query count, fetched feature count, unique frame count and CSV count agree. All returned restriction flags were zero.
- **48 full-frame DAP-L0 JPEG images**, each **3000×3000 at 300 dpi**, downloaded through the official free OpenData workflow. These are compressed open-data images, not the paid ≥1800 dpi photogrammetric scans or camera calibration reports.
- **47 watermarked preview JPEGs**, each 1080×1080, retained separately for provenance and quick browsing.
- All **95 image file checksums and JPEG decode checks passed**. See `validation.json` and `SHA256SUMS`.
- `gallery.html` displays the acquired dated imagery. `VISUAL_OBSERVATIONS.md` records limited site-level interpretations and date caveats.

## Most useful immediately

| Frame index ID | Public product ID | Catalogue capture date | Evidence |
|---|---|---|---|
| CN4581 | CN04581 | 1993-10-08 | Colour: Checkerboard Hill and neighbourhood; visible cleared Walled City site and residual structure |
| A36141 / A36142 / A36143 | Same | 1993-11-02 | Kowloon City / approach-end neighbourhood, overlapping views |
| A36144 / A36145 / A36146 | Same | 1993-11-02 | Airport approach end, terminal/apron and adjacent city |
| A36171 / A36172 | Same | 1993-11-02 | Runway-area views |
| A23632 | Same | 1990-11-13 | Earlier dense Walled City roof mass near image margin |
| CN21282 | Same | 1998-10-31 | Airport physical infrastructure after its operating era; not proof of operation |

The source index omits leading zeroes in some CN frame IDs: **CN4581 must become CN04581** for the product/preview/download endpoint. Both identifiers are retained. The 1993-11-02 date on A36143 was independently checked against the original 3000px handwritten annotation and stamp: **2.11.93**, not 3.11.93. Raw epoch is 752198400000 (UTC midnight; Hong Kong 08:00 on the same date). See `date_annotation_audit.json`.

## Files and interpretation

- `frame_catalogue.csv`: all 14,927 IDs, capture dates, native HK1980 frame centres, derived WGS84 centres, approximate index bounds, flying heights/scales, official preview URLs.
- `aerial_footprints_1985_1998.geojson`: source index geometry transformed by the source service to EPSG:4326, with raw attributes and UTC timestamps preserved.
- `landmark_frame_matches.csv`: approximate point-in-index-polygon coverage for Checkerboard, Walled City, threshold and runway anchors; annual/date-proximity ranks. These are acquisition anchors, not surveyed positions or building matching.
- `fullframes/`, `fullframe_manifest.json`: actual compressed full frames; source, IDs, date, local path, hash and image metadata.
- `previews/`, `preview_manifest.json`: source previews, kept distinct from full frames.
- `index_chunk_*.json`, `object_ids_1985_1998.json`, `flightpaths_layer*.json`, `index_provenance.json`: original read-only API responses and schema/acquisition context.
- `acquire_index.py`, `acquire_previews.py`, `acquire_selected_l0.py`: acquisition code. Full-frame script handles product-ID normalization; early probe scripts preserve the route investigation. Preview acquisition's first-pass failures were resolved by normalization; final manifest is authoritative.
- `validate.py`: image/hash/index verification, runnable with the project's geospatial Python environment.

## Source and access route

Primary official sources:

- [HKMS public aerial search](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA)
- [Lands Department DAP-L0 catalogue and 300 dpi description](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-aerial-photo)
- [Lands Department DAP product description](https://www.landsd.gov.hk/en/survey-mapping/mapping/aerial-photo-photogrammetric-products/digital-aerial-photo.html)
- Public map index: `https://api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2/query`, the same layer used by the public HKMS browser application. The public application source defines layer 0 centres and layer 2 coverage polygons.

The new index is distinct from the previously inspected 2016-onward CSDI digital-camera index. The older analogue-era imagery **is publicly available** through HKMS.

Full-frame workflow followed the public interface's `DAP-L0` selection → open-data download page → `requestQueue` → `queueStatus` → returned download URL. The inspected page explicitly had CAPTCHA disabled; no authentication/CAPTCHA bypass, purchase, external message, or public redistribution occurred. Download URLs are transient; stable frame preview URLs and metadata are retained. Cookie/session probe state is not part of the source evidence.

## Unresolved work and bounds

1. **No image has yet been ground-control registered or orthorectified.** The index polygons are approximate frame coverage, not valid corner ground-control points. Terrain and building displacement prevent a naive image-to-polygon stretch from recovering accurate footprints.
2. **No per-building height reconstruction or all-structure classification is complete.** Source availability and geographic overlap are not structure identification.
3. Walled City site is visually a dense compound in the inspected 1990 view, and largely cleared with residual structures in October/November 1993. This does not identify individual remnants or the exact change dates. Survey-sheet blankness cannot establish absence.
4. The selected 48 photos sample four anchor locations and years. They do not constitute complete image coverage of every structure in the bounding box on every date, much less all Hong Kong. The complete 14,927-frame catalogue supports subsequent spatial/date-specific selection.
5. Captures bracket historical states; observations at arbitrary intervening dates remain interval-censored unless supplementary evidence narrows them.
6. 300 dpi compressed images are usable visual evidence but do not substitute for calibrated photogrammetric scans, camera calibration, stereo matching and control points when recovering precise heights.

**Acquisition lane status:** index and selected imagery acquired and verified; source inspection performed on named frames. **Historical city reconstruction status:** incomplete, pending accurate photo/sheet registration and structure-level interpretation.
