# Historical-map content correspondence candidates

This lane produces **review candidates, not a certified building census**. Actual historical
TIFF ink content is compared with present-day polygons. This goes beyond the earlier
index-footprint overlap joins, but does not establish continuous survival or historical
height. The full reconstruction remains incomplete.

## Inspect

- `index.html`: per-sheet overlay contact sheets and CSV links.
- `all_candidates.csv`: every screened modern-template/source pair, including rejected
  and clipped cases. Repeated epochs or sheet edges are not independent buildings.
- `review_work_units.geojson`: 200 m grid cells containing current-template candidates.
  These are **review work units, not traced street blocks**. Empty cells and vanished-only
  sites are not covered by this file; see the map regions and full parent coverage masks.
- `SHEET_MONTH/ranked_candidates.geojson`: **modern matching templates**, not historical
  footprints. Historical identity, geometry, query-date presence and heights are unresolved.
- `SHEET_MONTH/map_regions.geojson`: image-derived white connected regions; includes
  objects with no substantial modern-polygon correspondence. These can be buildings,
  gardens, road enclosures, label artifacts or omitted areas. They are not automatically
  demolished buildings. Coverage-edge regions are explicitly flagged.
- `validation.json`, `run_summary.json`, `manifest.json`: counts, reproducibility and checks.

## Reproduce

From the workspace root:

```sh
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/candidates/extract_candidates.py --core-pre1993
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/candidates/repair_export_topology.py
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/candidates/validate_and_summarize.py
```

Without `--core-pre1993`, extraction processes the October 1989 and July 1994
11-NE-11A sheets only. With the flag it also processes the latest acquired edition
strictly before November 1993 at each core sheet location. This is an acquisition-based
selection, not a claim that the sheet is the latest actual survey before the flight.

## Method

1. Read the official TIFF and its TFW **inside the original archive**, preserving source
   hashes. Convert the TFW pixel-centre origin to raster corner coordinates. Assign the
   documented survey grid EPSG:2326; independent printed-grid accuracy checks belong to
   the parent registration report. No image alignment adjustment is fitted here.
2. Average-resample to approximately 0.25 m pixels; threshold grey values below 200 as
   ink. The analysis pixel size is not an accuracy claim. Survey index bounds only clip
   map margins; they are not used to register the image.
3. Transform present-day polygons to EPSG:2326. Sample exterior boundaries at 0.5 m
   intervals. Record distance-to-ink median, 95th percentile and fraction within 0.75,
   1.5 and 3 m. These are image-content distances, not independent survey residuals.
4. Find connected white regions without closing ink gaps. Restrict candidate regions to
   12–25,000 m² pixel area to remove most text holes and large open backgrounds. For
   each modern polygon choose the maximum raster intersection-over-union (IoU) region.
   All current-template candidates remain, including those with no eligible region.
5. Rank using `0.65 × boundary_fraction_within_1.5m + 0.35 × best_region_IoU`.
   Strong-screen candidates require boundary support ≥0.75 and IoU ≥0.50; ambiguous
   candidates have boundary support ≥0.50 or IoU ≥0.25. Other cases are low-support
   screen rejections. Partly clipped templates are a separate review class. These
   thresholds are engineering review heuristics, **not calibrated probabilities**.
6. Export map regions as pixel-derived external contours, simplified at 0.25 m.
   Interior text/ink holes are filled in the vector contour; pixel-area and contour-area
   therefore need not agree exactly. These are candidate outlines, not survey-grade
   digitized walls. `screened_modern_matches` counts modern templates with IoU ≥0.25.
7. Contact sheets show the top 12, six middle and six bottom ranked examples. Red is
   the modern outline; black is historical ink. These are audit samples, not a record
   that every row has been visually reviewed.

## Evidence boundaries and failure modes

- Roads, labels, grids and buildings all create ink. High boundary proximity alone is
  insufficient; the region-overlap check helps but does not prove identity.
- Open/partly broken outlines, subdivision lines and text crossing walls can produce
  false negatives. White-region extraction misses filled/hatch-filled buildings.
- Split/merge and shape changes need actual human interpretation. A single map region
  can have multiple current correspondence candidates; no one-to-one join is imposed.
- Low support or no current match never establishes historical absence or demolition.
  The 1989 Walled City blank is a known map omission; no extraction recovers its dense
  building geometry from that blank. Modern park structures there remain rejected/
  unresolved, not proof the historical city was empty.
- Regions below 12 m², above 25,000 m², and unenclosed map features are not exhaustively
  digitized. The complete parent uncertainty mask remains necessary.
- Dates are **edition-month intervals**. Neither an edition date nor a current polygon's
  creation date is a dated observation of unchanged historical structure geometry.
- Source date, modern-template date, historical identity and height fields remain
  independent. No modern roof/base heights are copied or exported as historical values.
- Modern geometry repairs are recorded per row; originals remain unchanged.
- Export validation identified 36 region self-intersections after coordinate conversion.
  `repair_export_topology.py` repairs only these derived contours, preserving original
  invalid features beside each output and recording each operation in
  `topology_repairs.json`. The largest measured grid-area change is below 0.000002 m²;
  this is numerical topology repair, not evidence of physical accuracy.
- No optimizer/configuration, source archive or chronology deliverable is modified.

The useful next acceptance step is to inspect strong named-object candidates, trace the
actual historical outlines, resolve identity and map height notation, and retain rejected,
changed and disappeared structures in the parent scene ledger.

**Attribution:** Lands Department and Buildings Department, Government of the Hong Kong
Special Administrative Region. Original source terms apply. Source URLs and retrieval
records remain in `../../chronology/sheets/maps/*.json` and the geospatial source package.
