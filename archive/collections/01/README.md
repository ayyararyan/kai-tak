# 01 — Historical Maps and Aerial Photography

Ayyar, Aryan (2026). Historical Maps and Aerial Photography. The Kai Tak Historical Research Archive, candidate v1.0.0, collection 01. **Unpublished candidate; no DOI assigned.**

846 catalogued artifacts; 275 verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.

[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/01.json)

## Historical survey-sheet index

**ID:** `kt-survey-index`. Official edition and coverage catalogues

- Quantity: {"whole_hk_entries": 72691, "aoi_entries": 18440}; 104 catalogued files.
- Epoch: Edition years 1922 onward, mixed survey epochs.
- Processing: downloaded/transformed.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:4326 export; native varies by historical series / not applicable or unresolved.
- Limitations: Index polygons are not map raster acquisition; Edition month is not per-object survey date
- Source links: [source 1](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1631584892859_72892/FeatureServer), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1639990901210_47291/FeatureServer), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047202071_61921/FeatureServer), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047456225_68329/FeatureServer), [source 5](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1671592436814_1059/FeatureServer)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Acquired historical survey maps

**ID:** `kt-survey-rasters`. 227 ZIP editions with TIFF/TFW members

- Quantity: {"editions": 227, "sheet_locations": 93}; 228 catalogued files.
- Epoch: Selected 1980s/1990s editions; exact dates in map_downloads.json.
- Processing: downloaded.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: HK1980/printed grid; individually verify source registration / not applicable or unresolved.
- Limitations: TFW/geotag availability does not itself validate historical georeferencing
- Source links: [source 1](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1631584892859_72892/FeatureServer), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1639990901210_47291/FeatureServer), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047202071_61921/FeatureServer), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047456225_68329/FeatureServer), [source 5](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1671592436814_1059/FeatureServer)
- Reuse: source-specific; consult artifact decisions. New candidate includes 227 matched permitted files.

## Historical aerial frame index

**ID:** `kt-aerial-index`. Coverage polygons and frame/capture identifiers

- Quantity: {"frames": 14927, "capture_dates": 316, "frames_1993": 1277}; 32 catalogued files.
- Epoch: 1985–1998.
- Processing: downloaded/transformed.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:4326 / not applicable or unresolved.
- Limitations: These are frame index records, not 14,927 photographs; Index polygon corners are not ground control
- Source links: [source 1](https://api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2/query), [source 2](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Acquired DAP-L0 full frames

**ID:** `kt-aerial-fullframes`. Compressed full-frame JPEG historical aerial photographs

- Quantity: {"full_frames": 48, "pixels_per_side": 3000, "dpi": 300}; 49 catalogued files.
- Epoch: 1985–1998 selected dates; each item retains actual capture date.
- Processing: downloaded.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Not calibrated high-resolution photogrammetric film scans; Not complete Hong Kong photographic coverage
- Source links: [source 1](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA)
- Reuse: source-specific; consult artifact decisions. New candidate includes 48 matched permitted files.

## Additional aerial previews

**ID:** `kt-aerial-previews`. Limited lower-quality preview imagery distinct from full acquired frames

- Quantity: {"previews_recorded": 47}; 48 catalogued files.
- Epoch: Dates per preview record.
- Processing: downloaded.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Preview rights can differ from DAP-L0 channel; classify separately; Not additional calibrated photographs
- Source links: [source 1](https://api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2/query), [source 2](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## All-Hong-Kong 1993 aerial index search

**ID:** `kt-aerial-index-all-hk-1993`. Separate whole-territory query for special-survey record investigation

- Quantity: {"public_layer2_records": 5637, "special_survey_matches": 0}; 13 catalogued files.
- Epoch: 1993.
- Processing: downloaded index metadata.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: Declared in retained query response; inspect response spatialReference / not applicable or unresolved.
- Limitations: Not the 1,277 local-AOI 1993 index records; Not acquired imagery; No November 5/plate match in bounded public layer is not proof of destruction or custodian absence
- Source links: [source 1](https://api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2/query), [source 2](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Historical Maps and Aerial Photography — supporting and unclassified artifacts

**ID:** `kt-support-01`. Ancillary reports, scripts and outputs; consult file-level provenance gaps.

- Quantity: {}; 372 catalogued files.
- Epoch: not established.
- Processing: mixed/unclassified.
- Verification: Not independently verified.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Directory classification is navigational, not a verified source or transformation chain.
- Source links: Not established; see unresolved source record.
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.
