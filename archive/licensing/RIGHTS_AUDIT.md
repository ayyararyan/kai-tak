# Source-specific rights audit — 13 October 2026

Status: **draft rights decisions, no new license grant, no publication**. This is a source-level investigation, not a claim that every repository file has been cleared. The parent audit must associate exact artifact hashes and source chains with these decisions. Copyright ownership, permission, byte availability and scientific verification remain separate fields.

## Decision summary

| Material | Proposed treatment |
|---|---|
| Official Old Survey Sheets acquired via documented OpenData route | Redistribution permitted with original portal conditions and attribution |
| Documented DAP-L0 300-dpi compressed JPEG frames | Redistribution permitted with original portal conditions; not paid scans or arbitrary previews |
| Official 5-metre DTM and traced conversion/subsets | Redistribution permitted with conditions; retain 2014–2015 photography epoch |
| Named CSDI Building service, linked tables and metadata | Redistribution permitted with conditions; modern data are not a complete 1993 model |
| NOAA-compiled ISD station-year observations | Redistribution permitted under dataset-specific constraints and NCEI policy; do not blanket-label all NOAA material CC0 |
| CAD accident reports, AIS charts, Boeing manuals/drawings, BRAVO plans | Permission required for public redistribution; catalogue/source links only |
| Three inspected arXiv paper PDFs | Link-only; displayed license grants distribution to arXiv, not to this archive |
| GRS records | Link-only until actual holdings and item-specific permission established |
| HKMS FlightPaths index/preview route; hkmaps tiles; non-open-lane geodetic PDFs; secondary shoreline lead | Rights unresolved or link-only; not eligible for automatic byte inclusion |
| Original research | Author approval needed for exact scoped open-license grants; current NOTICE still applies |

## Evidence and scope

`rights_registry.json` contains 22 stable source/rights records, and `rights_matrix.csv` is its tabular counterpart. `verification_receipts.json` records 25 attempted authoritative URL checks: 23 captured successfully, two failed. Captured source bodies are in `evidence/` for local audit evidence; these captures are **not automatically public release assets**. A URL returning 200 was not by itself treated as permission: operative text was read through the browser and acquisition channels checked against repository manifests.

The [DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions) are version 1.2, dated 26 May 2025. They permit redistribution and reproduction for commercial and noncommercial uses with identification, attribution and acknowledgement of Government/relevant-organisation IP ownership; the full terms, including indemnification, apply. [CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC) likewise permit these uses and expressly include metadata and APIs in their coverage. Neither is a CC0 dedication or a repository-wide Creative Commons license. Both distinguish external linked websites from their own data.

The [Old Survey Sheets catalogue](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-old-survey-sheets) links named open-data download/API routes. It limits georeferencing to general reference, not precision work. The [DAP catalogue](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-aerial-photo) specifically identifies compressed 300-dpi JPEG DAP-L0. This scope matches `fullframe_manifest.json`; it does not justify labelling higher-resolution scans or unrelated preview bytes open.

The [DTM product](https://www.landsd.gov.hk/en/spatial-data/open-data/kf_dtm.html) distinguishes source photography in 2014–2015, publication in 2017 and March 2019 revision. It specifies HK1980 Grid/HKPD and ±5 m at 90% confidence. These limitations must survive republication. The [Building dataset metadata](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html) is the actual `landsd_rcd_1637211194312_35158` source represented in local acquisitions. No additional redistribution restriction was identified there; modern revision dates and missing heights must remain explicit.

[NOAA ISD C00532 metadata](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00532/html) identifies NOAA as originator and supplies citation/no-warranty constraints. It is now marked superseded: a catalogue update must not replace the archived source bytes or their historical coverage. [NCEI's open-data policy](https://www.ncei.noaa.gov/sites/default/files/2023-12/NCEI%20PD-10-2-02%20-%20Open%20Data%20Policy%20Signed.pdf) distinguishes NOAA-produced data from externally provided material. The audit does not assign CC0 to arbitrary NOAA-hosted publications.

## Explicit restrictions

[CAD's notice](https://www.cad.gov.hk/english/important_notices.html) allows limited personal/internal use but requires prior written permission for public reproduction/adaptation/distribution. [AIS](https://www.ais.gov.hk/) independently displays a corresponding public-reuse restriction. A Wayback/HKU copy of CAD Report 1/95 does not establish broader rights. Preserve numerical readings as attributed, approximate research observations; do not confuse them with raw DFDR or freely redistributable report scans.

[Boeing's site terms](https://www.boeing.com/terms-of-submission-and-privacy-policy/site-terms) require permission for public network posting and modification. [BRAVO](https://bravo.bd.gov.hk/noticeView) limits use to declared purposes and restricts reproduction and adaptation; this is a different rights regime from CSDI building records. [GRS reproduction guidance](https://www.grs.gov.hk/en/use_and_reproduce_our_holdings.html) preserves copyright and donor conditions and asks that holdings be credited to Public Records Office, Government Records Service. Catalogue access is not acquisition or permission to publish underlying holdings.

Current landing pages for [Wu et al.](https://arxiv.org/abs/2412.04797), [Kim et al.](https://arxiv.org/abs/2405.16680) and [Chen et al.](https://arxiv.org/abs/2102.07039) each link to the [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html). None establishes general redistribution rights for this archive. Versionless local acquisition URLs also need exact version reconciliation.

## Unresolved channel distinction: aerial indexes and previews

The repository acquired historical aerial index records from `api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2`, and previews through `OneStopSystem/map-search/getPreviewFile`. These differ from the demonstrated DAP-L0 OpenData frame route. A live API metadata request returned 401. Both local HKMS HTTPS attempts failed normal certificate verification; no TLS bypass was used. Browser access to the HKMS OpenData page also failed. Therefore the registry conservatively leaves **those specific raw indexes/previews** unresolved, while clearing documented DAP-L0 frames. It is legitimate to describe/count index records in original research metadata, but a bulk API dump cannot inherit an unrelated permission by assertion. A later verified channel-specific term or exact mapping to the permitted product may resolve this.

The original `DATA_SOURCES.md` records a previous inspection linking OpenData to CSDI. That historical statement is retained as history but is not fresh validation of every delivery channel. Preserve earlier public releases; changing a future package allowlist does not authorize deleting or rewriting them.

## Original-work licensing recommendation for review

Recommend MIT for verified original code because the present goal is uncomplicated academic/computational reuse. Apache-2.0 is a reasonable alternative if explicit contributor patent licensing is desired; it adds obligations and must not be inferred from dependencies. Recommend CC BY 4.0 for wholly authored explanatory documentation and figures, and for original factual datasets where rights suffice. CC0 is an option for eligible factual tables if Aryan explicitly prefers a waiver over mandatory attribution. Maintain scholarly citation requests separately from legal obligations.

No recommendation applies to third-party scans, mixed figures, source-derived factual compilations with retained upstream conditions, publisher PDFs or installed third-party libraries. Confirm authorship/contributors per file, identify vendored portions, and apply exact file/directory declarations with exclusions. Do not put an unrestricted root LICENSE over the existing mixed-rights tree. Existing `NOTICE.md` expressly grants no additional open-source license; all proposed grants remain drafts for approval.

## Outstanding publication gates

1. Match exact included artifacts and parent source hashes to the permitted scope, including mixed figures and nested archives.
2. Keep CAD/Boeing/BRAVO and unresolved bytes out of new public bundles; retain metadata links, scientific dependency records and original local evidence.
3. Resolve any core reproducibility dependency requiring restricted originals, or state explicitly which public reproductions are possible without them.
4. Obtain author approval for the exact original-work license grants and public release. No external contact was made.

## Follow-up check: open aerial index is a different epoch

The [official open Aerial Photo Flight Index](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-aerial-photo-flight-index) exists. Its [current CSDI service](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1638157809075_22117/FeatureServer?f=json) exposes FlightPoint_2016 through FlightPoint_2024. This does not establish rights for the project's 1985–1998/1993 HKMS historical index bytes; the unresolved decision is deliberately confined to the exact acquired product/channel. The [CSDI FAQ](https://portal.csdi.gov.hk/csdi-webpage/info/FAQ) also confirms that own-design map renderings may credit CSDI and links attribution to the terms. This supports permitted-source derivatives without granting a new blanket license.
