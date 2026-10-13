# Data sources, attribution and publication scope

This is an initial public research snapshot, not a complete backup of the workstation. A separate publication manifest records every included source file and explicit file exclusions. The live research directories were not moved or modified by packaging, apart from publication entries appended to their project ledger.

## Included open data and derived research

**Lands Department and Buildings Department, Government of the Hong Kong Special Administrative Region; CSDI Portal and DATA.GOV.HK.** The Government and relevant organisations retain intellectual-property ownership of their data. These data and derivatives are provided as-is, without endorsement or a warranty of accuracy or suitability.

- [DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions) and [CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC) permit distribution/reproduction with source attribution and their stated conditions.
- [Old Survey Sheets](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-old-survey-sheets): historical sheets downloaded through the open-data route, including GeoTIFF/world-file archives. Their georeferencing is for general reference, not precision work.
- [Digital Aerial Photo, DAP-L0](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-aerial-photo): 300-dpi compressed open-data photographs, not paid high-resolution products. The inspected OpenData download page links directly to CSDI terms. This permission must not be generalized to all Lands Department photographs or paid products.
- Modern terrain/buildings: source and epoch details are in [the geospatial report](research/checkers-runway13/geospatial/README.md). Modern data are not represented as historical ground truth.
- Building chronology source metadata and conflict flags are retained; documentary dates do not establish historical footprints/heights.

**NOAA/NCEI:** source attribution for the retained 1993 ISD station-year observations and format documentation. See [ISD](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database). Recorded weather is not an along-flight gust field; flags, station-history limitations and missing values are preserved in the research outputs.

**CAD Report 1/95:** derived factual/manual-reading tables cite the report, page/figure and uncertainty. They are not raw DFDR samples. The full primary report, rasterized pages, source overlays and the simulation-chart reproduction remain outside this public package. The source inventory and [acquisition report](data/kai-tak-2026-10-13/README.md) identify the originals and archive URLs. Reproducing scan-dependent analyses requires independently obtaining the specified original bytes; existing source-hash checks are not bypassed.

## Deliberate exclusions

- Python environments, third-party installed packages, bytecode and test caches.
- Private download queue/session state, saved dynamic web-app pages/scripts, HTTP headers and correspondence drafts.
- Third-party scholarly PDFs, accident-report PDFs/scans and source-image overlays without verified redistribution permission. Citations, source references, authored analysis and numerical results remain included.
- Cached third-party website pages that are not needed to understand the research; source URLs remain in inventories.

These files remain in the original local project. No research evidence was deleted. The JSON publication manifest lists file-level exclusions and delivery lanes; excluded environment directories are listed separately.

## Publication versus source hashes

The original scientific manifests record the original local artifacts. Some documentation/output metadata has local workspace paths or internal session references normalized in the public copy. The publication manifest records both `source_sha256` and the actual public-copy `sha256`, and lists these normalizations. Mathematical model/configuration sources were not changed for publication. Historical source inventories can refer to excluded files; they are provenance inventories, not promises that every third-party item is mirrored here.

Large files are distributed as release archives instead of Git blobs. Restore them with `python3 scripts/fetch_data.py` from the repository root. The helper checks release hashes and paths and refuses to overwrite conflicting files. The public release is a fixed snapshot; new work in other research sessions is not automatically synchronized.
