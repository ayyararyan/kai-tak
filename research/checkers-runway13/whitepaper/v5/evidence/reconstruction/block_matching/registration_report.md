# Survey-sheet registration — REG-01

Verified 2026-10-13. Scope: all 227 already downloaded archives; independent content checks and clipped digitization rasters for sheet 11-NE-11A, October 1989, July 1994 and April 1997. Originals and chronology outputs were not changed.

## Delivered and checked

All **227/227** ZIPs pass CRC, current SHA256 against original download receipts, one-TIFF/one-TFW pairing, finite invertible affine, world-file versus rasterio transform consistency, and official index core containment. All TIFFs lack embedded CRS; EPSG:2326 is assigned from HK1980 Grid source documentation and the printed sheet legend, not inferred solely from coordinate magnitudes.

The complete per-source record is [registered/sheet_registration_inventory.json](registered/sheet_registration_inventory.json). It retains archive, TIFF and TFW SHA256; original world-file text; pixel-edge affine; raster dimensions; nominal sampling; raster bounds; official sheet core bounds; margins; metadata checks; and a separate printed-grid status. Original nominal raster sampling spans **0.063343–0.063581 m/pixel**. This is scan sampling, **not ground accuracy**.

Official WGS84 index polygons transform back to integral-metre HK1980 sheet grids within 0.01 m; that round-trip discrepancy is preserved, and core extents are snapped only under the stated tolerance. For the selected sheet the core is **[837500, 821000, 838250, 821600]** metres. All 227 scans include borders/legends extending beyond core extents; individual side margins range **39.90–114.95 m**. Those margins are not geographic mapping coverage.

## Ready-to-digitize rasters

| Edition | Registered RGB GeoTIFF | RGB PNG / coordinate sidecar |
|---|---|---|
| 1989-10 | [GeoTIFF](registered/11-NE-11A_1989-10_core.tif) | [PNG](registered/11-NE-11A_1989-10_core.png) · [transform](registered/11-NE-11A_1989-10_core.json) |
| 1994-07 | [GeoTIFF](registered/11-NE-11A_1994-07_core.tif) | [PNG](registered/11-NE-11A_1994-07_core.png) · [transform](registered/11-NE-11A_1994-07_core.json) |
| 1997-04 | [GeoTIFF](registered/11-NE-11A_1997-04_core.tif) | [PNG](registered/11-NE-11A_1997-04_core.png) · [transform](registered/11-NE-11A_1997-04_core.json) |

Each is **3000 × 2400**, sampled at **0.25 m**. Pixel-edge coordinates obey `E = 837500 + 0.25 x`, `N = 821600 − 0.25 y`. Pixel-index centres add 0.5 to x/y. Palette values, where present, are decoded to RGB before area averaging. PNG and GeoTIFF pixels are verified identical. Edition dates have month precision; they do not certify an object's survey date or continuing presence.

## Independent printed-grid inspection

The actual source scan content was inspected at four visible, labelled 100 m grid crossings for each edition: (837600,821500), (837700,821500), (837700,821400), (838000,821100). The first pair lies in/near the historically omitted Walled City area; the last lies near the airport circulation road. Crossings are dotted grid lines, not physical ground controls.

Crop origins were calculated to locate the neighbourhood. The **observed crossing locations were then manually recognized in the actual scan** and refined by dark-pixel projection within manually selected nine-pixel strips. They were not assigned the expected transform positions. Pixel centres, raw crop origins, independently observed coordinates and residuals are retained. Reading uncertainty is estimated at ±2 source pixels (roughly ±0.127 m per axis), not a calibrated confidence interval. No transform was fitted, corrected or forced through those checks.

| Edition | Visible crossings | 2D RMS residual | Maximum residual | Inspected evidence |
|---|---:|---:|---:|---|
| 1989-10 | 4 | 0.427 m | 0.736 m | [Source crops](registered/grid_crops_678.png) |
| 1994-07 | 4 | 0.147 m | 0.175 m | [Source crops](registered/grid_crops_679.png) |
| 1997-04 | 4 | 0.308 m | 0.342 m | [Source crops](registered/grid_crops_680.png) |

[Printed-grid validation and all measurements](registered/printed_grid_validation.json).

These results support use of the supplied world-file placement for cartographic digitization. They measure **scan/world-file agreement with the printed grid only**. Four internal crossings do not establish edge-wide deformation, original survey accuracy, building identity, roof displacement, or historical ground accuracy. All 224 other sheets remain `not_independently_checked`, not silently promoted from metadata audit. A sheet newly used for geometry extraction requires the same content check.

## Verification and reproduction

Nine tests passed (including two new fail-closed checks): TFW centre-to-edge convention; rotated affine/inverse; invalid transform refusal; all 227 original archive hashes; exact three output CRS/core/hash/pixel equivalence; independently recorded residual recomputation; and preservation of uninspected status.

From workspace root:

```sh
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/register_sheets.py
research/checkers-runway13/geospatial/.venv/bin/python -m unittest discover -s research/checkers-runway13/reconstruction/block_matching -p test_registration.py -v
```

**Correctness:** tests pass. **REG-01 completeness for these three digitization editions:** complete. **Whole reconstruction readiness:** not implied; historical geometry extraction, matching and height validation belong to subsequent requirements. Metric physical accuracy remains null. No model or optimizer changes, original-source edits, publication or peer synchronization.

## Fail-closed review repair

The independent review identified that `main` previously rendered selected sheets even if the recorded integrity checks failed. Rendering is now gated on successful hashes, transform and core checks for the entire batch; a failed audit is saved and the run raises before rendering any new raster. Direct `render` calls independently enforce the same record gate. A synthetic ZIP with appended tamper bytes retains a valid CRC but fails its receipt hash: the regression verifies a preserved failure inventory and zero rendering calls. Existing 227 originals pass; prior delivered geometry is unaffected.
