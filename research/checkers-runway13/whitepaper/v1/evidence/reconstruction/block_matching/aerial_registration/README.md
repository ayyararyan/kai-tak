# Actual-image historical stereo reconstruction

**13 October 2026. A real conditional 3D point cloud has now been recovered from the acquired 2 November 1993 photographs.** This supersedes the earlier conclusion that the current deliverable contained no recovered heights. It does not complete the most accurate historical city reconstruction.

[View the measured 3D evidence](dense_stereo_evidence.png) · [Actual matched image pair](stereo_actual_matches.jpg) · [Inspected ground/roof correspondences](stereo_surface_pair_inspection.jpg)

## What exists now

- **1,318 sparse measured stereo points** from A36142/A36143, not modern-building extrusion or index-corner registration.
- **171,356 filtered dense stereo points**, sampled from 1,541,916 accepted image correspondences. The point cloud contains observed surfaces, including ground, roofs and vegetation; surfaces are not automatically classified as buildings.
- **Two directly inspected municipal-market roof features** estimate approximately **10.77 m and 19.20 m above a fitted local park/road ground plane**. These are different roof features, not two estimates of one flat roof. Their exact height above the building's own base remains unresolved.
- **Four ground-plane fit tracks** and **one separately inspected ground track withheld from that plane fit**; six map road controls and four map controls held out from metric alignment.
- Per-point image coordinates, source dates, reprojection residuals, local-support flags and retained failed-correspondence masks.

Files: [dense PLY](dense_stereo_points.ply), [dense CSV](dense_stereo_points.csv), [dense report](dense_stereo_report.json), [sparse PLY](sparse_stereo_points.ply), [sparse CSV](sparse_stereo_points.csv), [sparse report](sparse_stereo_report.json).

## Coordinate meaning and measured checks

**Horizontal:** diagnostic EPSG:2326 coordinates, anchored to original survey TIFF/TFW and measured ground road junctions. **Vertical:** metres relative to a fitted local park/road plane; **not HKPD**, mean sea level, or an independently surveyed building-base height. No source height is silently set to sea-level zero.

| Check | Measured result | What it establishes |
|---|---:|---|
| Actual sparse content matches passing fundamental fit | 1,318 | Same-scene image correspondences, not certified objects |
| Rectified sparse vertical residual RMSE | 0.341 px | Epipolar alignment of the measured pair |
| Sparse original nominal-camera reprojection RMS, median / maximum | 1.505 / 3.899 px | Internal camera/image fit, not physical height accuracy |
| Held-out survey-road controls, metric 3D alignment | 5.754 m horizontal RMSE; 7.859 m maximum | Local planimetric check against manual survey-image controls |
| Ground-plane fit residual maximum | 0.319 m | Four fitted surface points' internal consistency |
| Withheld ground track 708 | −0.028 m relative-plane residual | One withheld plane check, **not independent calibration or a vertical error bound** |
| Dense minus sparse medians near ground / two roof checks | +0.094 / −0.241 / +0.022 m | Cross-matcher consistency on the same images/calibration |

Only **14 sparse / 3,781 dense** exported points lie within the local map-control hull. Others are explicitly marked horizontal extrapolation. Image coverage and available point density must not be confused with geographically uniform measurement accuracy. Original local-affine registration gave 2.418 m holdout RMSE; the metric stereo alignment is a different model and its **5.754 m** result is the applicable number for this point cloud.

## Reconstruction assumptions, openly retained

1. Film labels on the actual overlapping frames show the same camera `WILD 15/UAGIA Nr 6098 152.12`. We provisionally interpret 152.12 as focal length in mm and the 300 dpi image as metric scan scale, giving **1796.69 px** focal length.
2. Shared principal point is approximated from the corner-fiducial layout at original-image pixel **(1460,1440)**. Full principal-point, fiducial, lens-distortion and film/scan calibration are not available.
3. A robust fundamental matrix is estimated from actual SIFT feature matches. Nominal intrinsics recover relative pose; matching points are triangulated in both original cameras.
4. Four visually inspected park/path correspondences define a **local approximate ground plane**. It is an estimated reference plane, not a statement that the whole city is flat. Road-control image rays intersect that plane; six original survey road coordinates fit metric scale/orientation and four remain held out.
5. The resulting metric baseline is **486.39 m**, versus **525.42 m** between approximate frame-index centres. This mismatch is retained as evidence of unresolved calibration/georeferencing limitations, not hidden by forcing a scale. The metadata's `4000 ft` is not used as a secretly known altitude datum.
6. Dense stereo uses actual fundamental-matrix rectification, SGBM disparity, two-way correspondence consistency ≤0.75 rectified pixels, local texture checks, positive camera depths and original-camera reprojection ≤5 pixels. Failed or untextured pixels mean **unknown**, not empty space. No roof/ground classification, height clipping, hole filling or solid mesh is inferred.

A declared sensitivity experiment varies nominal focal length by ±5% and approximate principal point by ±20 pixels. The two roof estimates vary approximately **10.21–11.33 m** and **18.19–20.20 m** across those choices. **These are sensitivity results, not uncertainty bounds or confidence intervals.** Other calibration, surface, matching and ground-plane errors are not covered by those variations. Estimated heights can support explicitly conditional visualization; independently defensible geometric accuracy remains incomplete.

## Accepted and rejected attempts

The first attempt to track the manually picked road junctions with image patches produced a clear bad correspondence and non-ground drift. Its original `stereo_ground_controls.json`, `stereo_ground_control_patches.jpg` and `stereo_metric_cloud.npz` are retained as **rejected diagnostic evidence**, not the final world solution. Do not consume the latter NPZ as the current cloud.

The authoritative measured-point solution is **`sparse_stereo_transform.npz`** plus **`sparse_stereo_report.json`**. Its ground-plane tracks are visually inspected actual matched surface points. Map controls supply camera-ray/plane intersections, not the rejected patch tracks. The single ground-plane holdout participated in estimating relative pose, but not plane fitting; it is not an independently acquired survey checkpoint.

## Reproduce and inspect

The lane installs OpenCV only into its own `python_deps/`; original source files and the shared geospatial environment were not changed. `requirements_stereo.txt` records versions. The existing project's geospatial Python supplies NumPy/Pillow/rasterio/pyproj.

```sh
PY=research/checkers-runway13/geospatial/.venv/bin/python
LANE=research/checkers-runway13/reconstruction/block_matching/aerial_registration
$PY "$LANE/stereo_probe.py"
$PY "$LANE/build_sparse_stereo.py"
$PY "$LANE/dense_stereo.py"
$PY "$LANE/render_stereo_evidence.py"
$PY "$LANE/verify_stereo.py"
```

Scripts retain source-matched observations and hash-bound provenance. `dense_pixel_qc.npz` preserves disparity, consistency, texture and accepted-correspondence masks. `stereo_verification.json` checks actual CSV/PLY counts, numerical reconstruction, masks, provenance and semantic labels. A passing artifact check does not establish historical-scene completeness.

## Earlier bounded stage and remaining full scope

[LOCAL_AFFINE_STAGE.md](LOCAL_AFFINE_STAGE.md) preserves the earlier street-block registration and pre-stereo height-feasibility assessment. Its `height_feasibility.json` describes that earlier **zero-recovered-height stage**; it is not the current output count. [four_road_control_blocks.geojson](four_road_control_blocks.geojson) supplies four road-inclusive matching cells, not parcel or building boundaries.

For the full requested reconstruction, still required: more frames/views and broader control; better camera/film calibration or validated self-calibration; independent horizontal/vertical checkpoints; historical terrain and datum reconciliation; blockwise building identity and historical outlines; roof/ground interpretation; occlusion and mismatch repair; changed/demolished structures and completeness checks. No certification requirement is imposed as a prerequisite to useful visualization, but unavailable accuracy is not invented. No aircraft model, original source or shared project ledger was modified by this lane.
