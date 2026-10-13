# Historical obstacle update

**New evidence: 24 map elevation readings at 12 hill-surface locations, in two dated editions. Full historical obstacle model: INCOMPLETE. No new complete building volume or obstacle upper bound.**

This update moves beyond displaying the relative-height photo cloud: the new geographical point layer contains source-stated **absolute HKPD elevations**. They are useful terrain/platform observations for later reconstruction and cross-source checks, but cannot yet determine aircraft clearance. Nothing was inserted into the aircraft solver.

## What improved

The original Lands Department survey sheet **11-NW-10D**, editions **November 1989** and **June 1995**, shows Lok Fu Service Reservoir Rest Garden, its surrounding paths and the radar-station site. Both printed legends specify metres above Principal Datum and identify crosses as spot heights. Both also explicitly describe those heights as approximate and requiring verification before use.

All 24 selected symbols, printed values and immediate surface contexts were visually inspected. The corresponding twelve locations carry the same values in both editions; this is agreement in the cartographic record, **not proof of two independent surveys or exact 4 November 1993 conditions**. The earliest accepted source is before the target date and the other is after it.

| Mapped surface | Elevation, m HKPD | Meaning |
|---|---:|---|
| Rest garden, northern interior | 91.9 | Surface above the reservoir, not the maximum height of everything on it |
| Rest garden, southern interior | 92.0 | Another mapped surface point, not a flat-roof assumption |
| Surface immediately east of the garden | 93.8 | A spot observation; not the hill's established maximum |
| Open surface north of radar-station symbol | 93.3 | Ground/surface, **not the radar equipment top** |

The other eight mapped sites range from 83.8 to 92.9 m HKPD. Coordinates are digitized using the source-linked HK1980 registration and exported in WGS84. The declared two-pixel pick tolerance corresponds to 0.5 m per grid axis at the selected raster sampling; it is **not measured ground accuracy**. Ground position accuracy and vertical error bounds remain unknown.

The geographical exports preserve all **45 previously reviewed dated map faces for 15 named forms**, with historical tops still null. These are not 45 independent buildings. A separate acquisition-area polygon keeps the entire work area explicitly unresolved. Points do not turn the surrounding land, unreviewed roofs or gaps into clear space.

## Why no building heights were filled in

The available historical sheets provide outlines and spot surface levels, not a complete rooftop-elevation inventory. Addresses beside buildings are not elevations. Modern building heights cannot be assigned to historical outlines merely because names or footprints match. The official [1:1000 Basic Mapping Specifications, version 4.3 (December 2021)](https://www.landsd.gov.hk/doc/en/1_1000_bms.pdf), pp80 and458, also distinguish building roof/base attributes from mapped spot heights and exclude some rooftop equipment from the roof-level definition. That later document is interpretation context, not a retroactive accuracy guarantee for these old maps.

The original CAD CAL605 report was separately inspected. Its runway elevation is **15 ft AMSL (4.572 m in that stated reference)**, but the precise relation of its aviation AMSL to HKPD has not been established. Its approach chart and airport plan do not supply a legible, geographically precise building-obstacle census. The [aviation-source audit](aviation_sources/REPORT.md) adds 14 structured context observations, **zero individual obstacle heights**. No arbitrary mean-sea-level offset was applied.

## Use these files

- [obstacle_evidence.geojson](obstacle_evidence.geojson): 24 dated source-map point elevations, provenance, derived coordinates and limitations.
- [unresolved_footprints.geojson](unresolved_footprints.geojson): 45 existing dated forms plus the unknown-coverage polygon; no manufactured heights.
- [readiness.json](readiness.json): machine-readable gaps; `historical_clearance_ready` remains false.
- [observations.json](observations.json) and [inspection_receipt.json](inspection_receipt.json): exact transcriptions and hash-bound visual acceptance.
- [verification.json](verification.json): reproducible input/coordinate/semantic checks; code checks are distinct from survey validation.

## What is still blocking accurate obstacle constraints

1. **Historical building tops and equipment:** verified heights for structures actually present on the query date, including vanished/changed buildings, tanks, antennas and poles.
2. **Continuous terrain and coverage:** dated contours/surfaces over the approach, not interpolation advertised as a measured upper bound between twelve points.
3. **Independent accuracy and common reference:** horizontal/vertical checkpoints, quantified measurement uncertainty, and registration of terrain, runway and flight paths into consistent coordinates and datum.

The new spots can help future vertical-control work only after establishing same-surface photograph correspondences. Their presence does not calibrate the existing stereo cloud by itself. Wider historical sheets/photographs remain available for continued reconstruction; this small extraction does not discharge that authorized scope. Complete accurate historical obstacles have **not** been achieved by this update.

## Rebuild

From the project directory, using the existing geospatial environment:

```sh
geospatial/.venv/bin/python reconstruction/obstacles/prepare_sources.py
geospatial/.venv/bin/python reconstruction/obstacles/extract_observations.py
geospatial/.venv/bin/python reconstruction/obstacles/build_obstacles.py
geospatial/.venv/bin/python -m unittest discover -s reconstruction/obstacles -p test_obstacles.py -v
```

Unchanged extraction reproduces the inspected readings. Changed observations cannot inherit the old receipt: a new substantive manual inspection is required. No automatic acceptance-refresh command is supplied. Original archives, prior scene geometry and aircraft model/configuration are preserved. This package is local; it has not been published or synchronized to the public snapshot.
