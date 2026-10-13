# Hong Kong geospatial data for the Kai Tak project

Acquired and inspected 13 October 2026. **Data downloaded; not integrated into the landing model.**

Aryan authorized acquisition from another documented period if exact 1993 data are unavailable. This package preserves two distinct vintages. It is not a 1993 reconstruction or a single-date city model. The frozen scenario configuration is unchanged.

## Files to use

| File | Contents |
|---|---|
| `raw/Whole_HK_DTM_5m.zip` | Original Lands Department whole-territory ArcInfo ASCII elevation grid; 28,706,079-byte ZIP, CRC checked. |
| `derived/Hong_Kong_DTM_5m_HK1980.tif` | Lossless compressed GeoTIFF of that grid, EPSG:2326, elevations in metres above Hong Kong Principal Datum (HKPD). |
| `raw/Building_20260921.geojson` | Original whole-territory building footprint release; 397,075,244 bytes, 342,195 features. |
| `derived/Kowloon_KaiTak_DTM_5m_HK1980.tif` | Smaller 5-metre raster subset for Kowloon, Kai Tak and nearby hills/harbour; no resampling. |
| `derived/Kowloon_KaiTak_buildings_20260921.geojson` | 69,915 building features intersecting the local acquisition rectangle. |
| `metadata/validation.json` | Raster extent, values, full-cell equality check, counts and height completeness. |
| `metadata/building_quality_flags.json` | Invalid polygon IDs and building status counts. |
| `manifest.json`, `SHA256SUMS` | File sizes, local SHA-256 integrity hashes and source provenance. |

Local acquisition rectangle: longitude **114.10–114.25**, latitude **22.27–22.40** (WGS84). This is a convenience subset, not an approved flight corridor. Entire intersecting building polygons are retained. The raster is the corresponding approximately aligned projected bounding rectangle. Full-territory originals remain available outside this subset.

## Dates, coordinates and accuracy

**Terrain:** the [official product specification](https://www.landsd.gov.hk/en/spatial-data/open-data/kf_dtm.html) describes 2014–2015 aerial photographs, publication in 2017 and revision in March 2019. The [catalogue](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-5m-grid-dtm/resource/620c4f4f-eac4-472f-9074-dffa2ad596fd) reports a July 2024 resource update; the download server reports September 2023 modification. These are different metadata dates, not evidence that the terrain was surveyed in 2024. Preserve the documented photography epoch and this uncertainty. Resolution is 5 m; stated accuracy is ±5 m at 90% confidence, **not a guaranteed worst-case clearance bound**. Vegetation and some bridges/elevated roads are included. This is not strictly bare-earth terrain or a complete obstacle surface.

Raster: 12,751 columns × 9,601 rows; 122,422,351 cells; observed range −26 to 958 m HKPD. Source declares −9999 nodata, but no such cells occur in this file. A populated cell is not proof of surveyed land: this rectangle includes water/offshore space. It is **not a land/water mask**. Every GeoTIFF cell was compared to the source and matched exactly. EPSG:2326 was attached from official documentation, not inferred from arbitrary coordinates.

**Buildings:** [official release metadata](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html) specifies revision **2026-09-21**. The downloaded GeoJSON is longitude/latitude (WGS84 export); the source service uses HK1980 Grid. `BaseHeight` and `TopHeight` are approximate **elevations above HKPD**, not height above local ground. Do not add TopHeight to the terrain. `DateCreate` is creation of the database polygon, not necessarily construction of the building. All downloaded statuses are Active, as reported by the source.

## Verification and limitations

- Complete GeoJSON parsed; 342,195 records match the live service's count; no duplicate OBJECTIDs.
- Whole territory: 104,847 missing TopHeight values and 106,249 missing BaseHeight values.
- Local subset: 10,026 missing TopHeight and 10,233 missing BaseHeight values. Missing values remain null, never zero or imputed from storeys.
- 83 source polygons are geometrically invalid under Shapely; 13 lie in the local subset. IDs are recorded, and original geometry is preserved rather than silently repaired.
- Footprint plus approximate roof/base elevation supports coarse extruded obstacles, not a complete roof mesh, antennas, cranes or aircraft swept-volume clearance.
- Terrain/building epochs differ. A modern building layer cannot establish historical clearance; modern development on the former runway cannot be silently removed to make a counterfactual landing work.
- Hills may be useful across dates only after checking cuts/quarries/earthworks. Shoreline and reclamation changes require their own layer. No verified shoreline geometry was downloaded in this acquisition. An official iB1000 tile inventory for the immediate Kai Tak area is retained as an acquisition lead, not a downloaded map: 49 tiles; one inspected FGDB tile was about 43 MB. The portal's whole-layer Shoreline file route returned 404; no error page is counted as data. The third-party shoreline item metadata is a lead only.
- HKPD is not automatically the aviation height datum. Runway placement, elevation, north conventions, terrain uncertainties and collision margins still require reconciliation before simulation use.

## Provenance and reuse

Source and intellectual-property attribution: **Lands Department, Government of the Hong Kong Special Administrative Region; DATA.GOV.HK and Common Spatial Data Infrastructure (CSDI) Portal**. Download/use is available under the [DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions) and [CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC), with attribution and their stated conditions/disclaimers. Snapshots and the official building data specification are under `metadata/`. No account, API credential, purchase, publication or external outreach was used.

The broad dataset-search helper produced several irrelevant hits and failed NASA/data.gov/UCI/OpenML queries; those results were not used as acquisition evidence. The actual data were obtained directly from official Hong Kong endpoints.

## Reproduce local preparation

Use the separate geospatial environment (`requirements.lock`), not the numerical-model environment:

```sh
.venv/bin/python prepare_and_verify.py
shasum -a 256 -c SHA256SUMS
```

The script reads the original downloaded files and recreates the GeoTIFFs, local building subset and primary validation report. It never changes the landing simulator. Local hashes establish integrity of this acquired snapshot, not publisher-signed authenticity or geospatial accuracy.
