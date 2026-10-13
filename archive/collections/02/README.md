# 02 — Historical Buildings and Urban Geography

Ayyar, Aryan (2026). Historical Buildings and Urban Geography. The Kai Tak Historical Research Archive, candidate v1.0.0, collection 02. **Unpublished candidate; no DOI assigned.**

358 catalogued artifacts; 133 verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.

[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/02.json)

## Modern building footprints and local subset

**ID:** `kt-modern-buildings`. Source building polygons with approximate HKPD base/top elevations

- Quantity: {"whole_hk_features": 342195, "local_features": 69915, "invalid_geometries": 83, "local_invalid_geometries": 13, "top_height_missing": 104847, "base_height_missing": 106249}; 2 catalogued files.
- Epoch: Source revision 2026-09-21; not a 1993 building census.
- Processing: downloaded/transformed.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:4326 export / HKPD.
- Limitations: TopHeight is absolute elevation above HKPD, not height to add to terrain; DateCreate denotes database polygon creation, not construction; Original invalid geometries/nulls retained
- Source links: [source 1](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html), [source 2](https://portal.csdi.gov.hk/csdi-webpage/file-api?dataset_id=landsd_rcd_1637211194312_35158&format=geojson&layer_name=Building)
- Reuse: source-specific; consult artifact decisions. New candidate includes 2 matched permitted files.

## Building documentary chronology source tables

**ID:** `kt-building-chronology-source`. Complete four-table current-source relationship graph

- Quantity: {"works": 168042, "building_structure_relationships": 53349, "structure_permit_links": 54505, "permits": 24469}; 123 catalogued files.
- Epoch: Historical documentary events accessed in modern source.
- Processing: downloaded.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: 52,552 works OP-date entries in 2019/2020; 52,202 CSUIDs conflict with linked permit dates; No silent repair; both source values retained
- Source links: [source 1](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1000), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1002), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1003), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1004)
- Reuse: source-specific; consult artifact decisions. New candidate includes 123 matched permitted files.

## Date-specific building documentary classifications

**ID:** `kt-building-date-classification`. Queries retain event provenance and uncertainty

- Quantity: {"classified_current_features": 342195, "local_current_features": 69915, "resolved_evidence_paths": 221383, "additional_vanished_identities": 0}; 11 catalogued files.
- Epoch: 1993-11-04 and 1985-01-01 query dates; modern source universe.
- Processing: derived.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Completion evidence does not prove unchanged shape or target-date survival; Zero additional vanished identities; not a demolished-building census
- Source links: [source 1](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1000), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1002), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1003), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer/1004), [source 5](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html), [source 6](https://portal.csdi.gov.hk/csdi-webpage/file-api?dataset_id=landsd_rcd_1637211194312_35158&format=geojson&layer_name=Building), [source 7](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Visually inspected historical mapped faces

**ID:** `kt-historical-map-faces`. Hash-bound interpreted faces across three map editions

- Quantity: {"faces": 45, "named_forms": 15, "modern_component_joins": 72}; 5 catalogued files.
- Epoch: 1989-10, 1994-07, 1997-04.
- Processing: derived/interpreted.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:4326 exports and EPSG:2326 source grid / No heights identified.
- Limitations: Faces may be aggregates/partial outlines, not whole buildings; Historical base/top elevations and volumes remain null; No presence certification on 1993-11-04
- Source links: [source 1](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1631584892859_72892/FeatureServer), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1639990901210_47291/FeatureServer), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047202071_61921/FeatureServer), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047456225_68329/FeatureServer), [source 5](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1671592436814_1059/FeatureServer), [source 6](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Historical map content matching queue

**ID:** `kt-map-matching-candidates`. Automated template/source-region correspondence candidates

- Quantity: {"pairs": 23801, "strong_unverified": 10955, "unclassified_map_regions": 61893, "nonempty_review_cells": 1333, "road_control_cells": 4, "across_date_cell_joins": 202}; 201 catalogued files.
- Epoch: 94 editions at 93 sheet locations.
- Processing: derived/unvalidated candidates.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: EPSG:2326 local matching / not applicable or unresolved.
- Limitations: Every automated pair still requires identity interpretation; Map regions include text, roads and courtyards; not automatically vanished buildings
- Source links: [source 1](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1631584892859_72892/FeatureServer), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1639990901210_47291/FeatureServer), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047202071_61921/FeatureServer), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047456225_68329/FeatureServer), [source 5](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1671592436814_1059/FeatureServer), [source 6](https://portal.csdi.gov.hk/csdi-webpage/metadata/landsd_rcd_1637211194312_35158/html), [source 7](https://portal.csdi.gov.hk/csdi-webpage/file-api?dataset_id=landsd_rcd_1637211194312_35158&format=geojson&layer_name=Building), [source 8](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Dated historical source observations and obstacles

**ID:** `kt-historical-observations`. Evidence-linked partial terrain/building observations

- Quantity: {"chronology_visual_observations": 52, "named_sites": 17, "obstacle_observations": 24, "obstacle_sites": 12, "complete_obstacle_volumes": 0}; 4 catalogued files.
- Epoch: Mixed historical dates; target 1993-11-04.
- Processing: interpreted/approximate digitization.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: No complete historical obstacle envelope; Unknown is not empty/clear space
- Source links: [source 1](https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1631584892859_72892/FeatureServer), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1639990901210_47291/FeatureServer), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047202071_61921/FeatureServer), [source 5](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047456225_68329/FeatureServer), [source 6](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1671592436814_1059/FeatureServer), [source 7](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA), [source 8](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Historical Buildings and Urban Geography — supporting and unclassified artifacts

**ID:** `kt-support-02`. Ancillary reports, scripts and outputs; consult file-level provenance gaps.

- Quantity: {}; 106 catalogued files.
- Epoch: not established.
- Processing: mixed/unclassified.
- Verification: Not independently verified.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Directory classification is navigational, not a verified source or transformation chain.
- Source links: 
- Reuse: source-specific; consult artifact decisions. New candidate includes 8 matched permitted files.

