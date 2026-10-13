# Four road-control cells: dated content assignments

Open **[the comparison index](index.html)** for four legible October1989/July1994
map-overlay pairs. These are the exact supplied road-centre control cells, which include
parts of surrounding streets. The cell geometry is not a parcel boundary or a verified
inventory boundary. Source: `../../aerial_registration/four_road_control_blocks.geojson`.

This additive package changes no stable 94-sheet screening output or original source.
Only the two existing 11-NE-11A source epochs are used.

## What is assigned

Each cell directory contains:

- `1989-10_templates.geojson`, `1994-07_templates.geojson`: **modern matching templates**
  clipped to the cell, retaining original candidate status and source provenance. They
  are not historical footprints, even when the underlying screen status is strong.
- `1989-10_regions.geojson`, `1994-07_regions.geojson`: unclassified map regions clipped
  to the cell. Text/ink holes remain; some regions represent roads or other non-buildings.
- `memberships.csv`: every positive-area assignment, with actual intersection area and
  fraction of original source geometry within the cell.
- `across_dates.csv`: same modern CSUID used as a template in each map epoch, joined
  within this cell. Labels in the PNG refer to its cell-local row numbers. This is **not
  accepted historical identity, unchanged footprint, or survival between dates**.
- `region_overlap_across_dates.csv`: all positive-area overlaps between the two epochs'
  cell-clipped unclassified regions, with IoU and fractions of each clipped region.
  These are many-to-many spatial correspondence candidates, not temporal identities.
- `two_date_overlay.png`: equal survey-grid extent and scale for both dates. Black is
  the historical map, blue the exact supplied cell, green a strong unverified modern
  template, and copper other screening statuses. Overlapping labels can represent
  separate current substructure records; they are not independent historical buildings.

Assignment uses intersection in EPSG:2326. Strictly positive area above **1e-6m²** is
retained; this is a numerical tolerance, not a physical accuracy bound. Tangential-only
contacts are excluded. Features can belong to multiple cells when they overlap them;
no centroid-only or maximum-overlap assignment silently drops boundary cases.

The source map edition is a month, not each object's observation date. Current template
epoch stays **2026-09-21**. Historical presence and roof elevation stay **null**; historical
identity acceptance and full-contents verification stay **false**. A missing row or low
screen score never proves a historical building was absent.

## Bounded counts

| Road-control cell | Current-template across-date rows | Map regions1989 /1994 | Across-date region-overlap candidates |
|---|---:|---:|---:|
| 01: Nga Tsin Long–Nam Kok |46|77 /73|105|
| 02: Nam Kok–Lung Kong |41|57 /59|75|
| 03: Lung Kong–South Wall |53|59 /60|79|
| 04: South Wall–Tak Ku Ling |62|74 /72|138|

Totals: **202 cell/template rows**, **404 dated template assignments**, **531 dated map-region
assignments**, and **397 geometric cross-date region-overlap candidates**. These counts
measure different objects and must not be added as historical buildings.

## Reproduce and verify

Run `assign_road_cells.py` using the project's `geospatial/.venv/bin/python`. It verifies
the four candidate inputs against the stable parent manifest, checks original archive
hashes using the read-only source reader, validates geometry/null semantics and overlap
fractions, decodes the four PNGs, and verifies the parent inputs/manifest remain unchanged.
`validation.json` records the exact checks and source hashes; `manifest.json` hashes this
additive package. Parent visual review of all four cells remains a separate acceptance
step; neither a generated PNG nor these checks establish complete historical contents.

Attribution: Lands Department and Buildings Department, Government of the Hong Kong
Special Administrative Region. Original source terms remain applicable.
