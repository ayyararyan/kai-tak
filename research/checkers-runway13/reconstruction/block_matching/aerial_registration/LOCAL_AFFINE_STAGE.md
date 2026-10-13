# A36143: measured local photo-to-survey registration

**13 October 2026. Local matching diagnostic produced and inspected. Full photo orthorectification and height reconstruction remain incomplete.**

[See the actual registered comparison](local_registration_comparison.png), [picked photo controls](picked_road_controls.png), [numeric controls](control_points.csv) and [measured residuals/transform](registration.json).

## What was measured

The actual 2 November 1993 photograph A36143 was matched to the actual October 1989 survey sheet 11-NE-11A, using **ten identifiable ground-level street-centre junctions** along Carpenter Road and Nga Tsin Wai Road. Cross-streets are Nga Tsin Long, Nam Kok, Lung Kong, South Wall and Tak Ku Ling. These are manually interpreted street-centre intersections, not new surveyed monuments. Temporal persistence of this local street layout is directly consistent with both images; it does not establish historical identity of all buildings in those blocks.

The Lands Department TIFF's accompanying original TFW supplies the metric reference. The TIFF itself has no embedded CRS; the source survey's printed 1980 Grid and source metadata provide **HK1980 Grid / EPSG:2326**. Published sheet/index boundaries were **not** turned into photograph controls. Geographic overlap was **not** used as evidence of content alignment.

A six-parameter affine model was estimated using six controls. Four intersections on the intervening Nam Kok/South Wall cross-streets were reserved **before fitting**, not selected for small residuals. No subsequent point tuning or holdout fitting was performed.

| Set | Points | Horizontal residual RMSE | Largest residual |
|---|---:|---:|---:|
| Fit | 6 | 3.716 m | 5.171 m |
| Held out | 4 | 2.418 m | 3.692 m |

The controls cover approximately **231 × 200 m**, spanning four Kowloon City blocks between Nga Tsin Long and Tak Ku Ling Roads. `local_control_support.geojson` is their convex hull, not the full image footprint. The diagnostic GeoTIFF has an explicit internal mask outside that support hull. Its 0.5 m output grid is resampling spacing, **not 0.5 m accuracy**.

**Interpretation:** the result supports local block comparison. The residuals measure disagreement with manually picked map locations; they are **not independently surveyed absolute accuracy**, a confidence region, a maximum error bound, or roof-level precision. Both rows of controls follow two parallel roads, limiting spatial independence. High buildings lean and occlude ground in the aerial photograph; roof position cannot be substituted for ground footprint. This model has no terrain correction and must not be extrapolated to the Walled City, Checkerboard Hill, runway, or full aerial frame.

## New camera evidence

The actual film label is retained in [A36143_camera_label.jpg](A36143_camera_label.jpg). It reads:

> WILD 15/UAGIA — Nr 6098 — 152.12

The catalogue `FOCAL_LENGTH` field is `"0"`, but the film itself retains a nominal focal-number clue. We record the inscription exactly rather than interpreting zero as proof that there is no nominal information. **This is not a camera calibration report.** Principal point, radial/decentring distortion, calibrated fiducial coordinates, scan deformation and exterior orientation remain unavailable. Nominal focal information alone does not authorize height recovery.

Adjacent acquired November frames exist (A36141–A36146; A36171–A36172), enabling a future stereo tie-point investigation. Mere overlap or successful stereo correspondence would still not supply independent metric height accuracy. No stereo heights, calibrated camera model or bundle-adjusted scene are claimed here.

## Produced artifacts

- `control_points.csv`: all ten manual measurements, exact original-photo pixel coordinates, reference easting/northing, immutable fit/holdout role and residual vectors.
- `registration.json`: source hashes, affine coefficients, residuals, local bounds/support and limitations.
- `A36143_local_affine_diagnostic.tif`: EPSG:2326 RGB diagnostic, 0.5 m sampling, control-support mask; no height band.
- `local_control_support.geojson`: geographic control hull with non-certification properties.
- `local_registration_comparison.png`, `reference_local.png`, `picked_road_controls.png`: inspected evidence illustrations. Other `*_grid`/inspection images preserve the measurement context.
- `measure_registration.py`, `finalize_diagnostic.py`: repeatable fit, residual computation, warp, support mask and display generation. Source images/maps remain unchanged.
- `verification.json`: numerical/source-hash/mask integrity checks, not a reconstruction-completeness certificate.

Run from workspace root using the existing geospatial environment:

```sh
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/aerial_registration/measure_registration.py
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/aerial_registration/finalize_diagnostic.py
```

## Precise remaining registration/3D gaps

1. Additional spatially distributed ground controls and genuinely independent checks across the full scene; inspect and preserve temporal changes rather than force them into a transform.
2. Camera/fiducial calibration and scan-coordinate correction, or independently validated self-calibration with sufficient multi-view geometry; the film inscription alone is inadequate.
3. Terrain-aware orthorectification with historical terrain/shoreline changes explicit; the existing 2014–2015 DTM is not 1993 truth.
4. Stereo/bundle geometry with checks against independently supported heights, surface semantics and datum. No extrapolated metre-level accuracy from these planar holdouts.
5. Building-by-building identity, footprint, roof level and changed/demolished structure verification. This local affine supports comparison, not that completed inference.

These remain required for the requested most accurate reconstruction. No model configuration, source original, shared project ledger, external service or live aircraft procedure was modified.

## Conditional height-recovery feasibility

[height_feasibility.json](height_feasibility.json) records algebraic sensitivity, **zero measured roof/base pairs, zero recovered heights and null height bounds**. The four road-centre cells are in [four_road_control_blocks.geojson](four_road_control_blocks.geojson), for parent blockwise matching only. They include street portions; they are not parcel/building boundaries or evidence that every structure in each cell has been checked.

For an ideal vertical, distortion-free camera with known height **H above a flat ground plane**, let R denote a base point's radial ground distance from the nadir and d denote the roof's outward displacement after ground-plane scaling. A roof point vertically above that base at height h has

`d = h R / (H − h)`, so `h = H d / (R + d)`.

At small h/H, a relative roof/base position error Δd amplifies to roughly `Δh = (H/R) Δd`. Near the nadir R approaches zero: a single vertical image supplies essentially no relief-displacement height information there. Camera tilt, lens/scan distortion and misidentified base/roof edges can imitate relief displacement.

**Scenario sensitivity, not measurements:** if 4000 ft were camera height above the relevant ground (1219.2 m), at R = 500 m each 1 m of relative base/roof error becomes about 2.44 m of height error. At R = 100 m the amplification is about 12.19. The measured local affine's area-equivalent original-image scale is about 0.65 m/pixel; one original pixel would then imply roughly 1.59 m height sensitivity at R = 500 m, before calibration, pose, terrain or interpretation errors. Neither the one-pixel pick error nor the 500 m radius nor the altitude datum is established. These examples cannot become confidence intervals.

The frame centre in the index is an acquisition aid, not an identified optical nadir. `4000 ft` has not been reconciled to camera elevation/AGL/sea-level convention. The film label's `152.12` cannot resolve that convention. Required inputs remain calibrated principal point/fiducial geometry and lens/scan distortion; metric scale and camera pose/altitude datum; historically valid ground elevation; genuine corresponding base/roof edges or well-conditioned stereo tracks; and independent height checkpoints. Nominal focal length plus approximate flight height and a street-plane affine are insufficient to separate camera/scan geometry from building height.
