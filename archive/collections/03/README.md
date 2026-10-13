# 03 — Terrain and Geospatial Data

Ayyar, Aryan (2026). Terrain and Geospatial Data. The Kai Tak Historical Research Archive, candidate v1.0.0, collection 03. **Unpublished candidate; no DOI assigned.**

47 catalogued artifacts; 3 verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.

[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/03.json)

## 5m DTM original and lossless raster derivatives

**ID:** `kt-dtm5-original`. Whole Hong Kong elevation raster and Kowloon subset

- Quantity: {"columns": 12751, "rows": 9601, "cells": 122422351, "subset_rows": 2880, "subset_columns": 3092, "source_nodata_cells_observed": 0}; 3 catalogued files.
- Epoch: 2014–2015 photography; published 2017; revision 2019-03.
- Processing: downloaded/transformed.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:2326 / HKPD.
- Limitations: 2014–2015, not 1993 terrain; Includes some vegetation/bridges, not strict bare earth; ±5m at 90% is source specification, not hard clearance bound; Populated water cells are not a land mask
- Source links: [source 1](https://www.landsd.gov.hk/en/spatial-data/open-data/kf_dtm.html), [source 2](https://www.landsd.gov.hk/landsd_psi_data/SMO/data/Whole_HK_DTM_5m.zip)
- Reuse: source-specific; consult artifact decisions. New candidate includes 3 matched permitted files.

## Coordinate/datum documentation and diagnostics

**ID:** `kt-geodetic-frame`. Official transform and project registration gates

- Quantity: {"historical_aviation_datum_tie_established": false}; 14 catalogued files.
- Epoch: Mixed historical and current reference documents.
- Processing: downloaded/derived.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:2326 / geographic / runway-relative distinctions / HKPD versus historical aviation AMSL unresolved.
- Limitations: Numerical transform checks do not validate historical runway placement; 77.62–81.54 m discrepancy concerns direct threshold vs pavement-end back-projection, not two surveyed thresholds; 61 m endpoint offset is an unaccepted hypothesis
- Source links: [source 1](https://www.geodetic.gov.hk/common/data/parameter/7P_ITRF96_HK80_V1.pdf), [source 2](https://www.ais.gov.hk/eaip_20261001/2026-10-01-000000/html/eAIP/VH-GEN-2.1-en-US.html), [source 3](https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf), [source 4](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Terrain and Geospatial Data — supporting and unclassified artifacts

**ID:** `kt-support-03`. Ancillary reports, scripts and outputs; consult file-level provenance gaps.

- Quantity: {}; 30 catalogued files.
- Epoch: not established.
- Processing: mixed/unclassified.
- Verification: Not independently verified.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Directory classification is navigational, not a verified source or transformation chain.
- Source links: Not established; see unresolved source record.
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.
