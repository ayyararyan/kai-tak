# 05 — Weather and Meteorological Records

Ayyar, Aryan (2026). Weather and Meteorological Records. The Kai Tak Historical Research Archive, candidate v1.0.0, collection 05. **Unpublished candidate; no DOI assigned.**

35 catalogued artifacts; 1 verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.

[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/05.json)

## NOAA 1993 historic Kai Tak observations

**ID:** `kt-noaa-raw`. Retained unchanged compressed ISD archive

- Quantity: {"records": 8549, "event_day_records": 24}; 1 catalogued files.
- Epoch: 1993-01-01/1993-12-31.
- Processing: downloaded.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Station-history datum not independently reconciled; Surface observations do not identify aircraft-local wind
- Source links: [source 1](https://www.ncei.noaa.gov/pub/data/noaa/1993/450070-99999-1993.gz)
- Reuse: source-specific; consult artifact decisions. New candidate includes 1 matched permitted files.

## Decoded NOAA weather and quality-control tables

**ID:** `kt-noaa-decoded`. Source-order records with raw fields, flags and missingness

- Quantity: {"rows": 8549, "event_rows": 24, "routine_rank_subset": 8360, "missing_calendar_hours": 215, "gust_group_present": 519, "partial_rows": 19}; 3 catalogued files.
- Epoch: 1993-01-01/1993-12-31.
- Processing: derived.
- Verification: fresh isolated decoder replay and 12 tests passed; both CSV hashes match original, receipt noaa_replay.json; no new station-history verification.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Preserves suspect calm/partial row; no imputation; Rank is descriptive, not population percentile or accident probability; NOAA/CAD agreement may share originating observations
- Source links: [source 1](https://www.ncei.noaa.gov/pub/data/noaa/1993/450070-99999-1993.gz), [source 2](https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf), [source 3](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## CAL605 five-sensor wind printout transcription

**ID:** `kt-wind-printout`. 225 direction/speed pairs and source-preserving extrema

- Quantity: {"timestamps": 15, "sensors": 5, "pairs": 225, "numeric_cells": 450}; 7 catalogued files.
- Epoch: 1993-11-04 wind-system clock, offsets unresolved.
- Processing: manual transcription/derived arithmetic.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: A/B/C have different averaging windows; LYM A360/32 retained; no smoothing correction; Not aircraft-local wind or independent repeated observations
- Source links: [source 1](https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf), [source 2](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Weather and Meteorological Records — supporting and unclassified artifacts

**ID:** `kt-support-05`. Ancillary reports, scripts and outputs; consult file-level provenance gaps.

- Quantity: {}; 24 catalogued files.
- Epoch: not established.
- Processing: mixed/unclassified.
- Verification: Not independently verified.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Directory classification is navigational, not a verified source or transformation chain.
- Source links: 
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

