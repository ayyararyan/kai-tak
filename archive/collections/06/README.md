# 06 — Three-Dimensional Reconstruction

Ayyar, Aryan (2026). Three-Dimensional Reconstruction. The Kai Tak Historical Research Archive, candidate v1.0.0, collection 06. **Unpublished candidate; no DOI assigned.**

1098 catalogued artifacts; 6 verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.

[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/06.json)

## A36142/A36143 historical stereo points

**ID:** `kt-stereo-points`. Sparse and dense conditional triangulated cloud with QC

- Quantity: {"sparse_points": 1318, "dense_points": 171307, "dense_points_inside_control_hull": 3780, "holdout_rms_m": 5.754}; 8 catalogued files.
- Epoch: 1993-11-02 photographs.
- Processing: estimated reconstruction.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: Diagnostic EPSG:2326 alignment / Fitted local park/road plane, NOT HKPD/AMSL.
- Limitations: Most points outside control hull; 152.12 mm label focal, 300dpi scan scale and principal point assumptions; No independent absolute-height accuracy calibration; Sensitivity ranges are not confidence intervals
- Source links: [source 1](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA), [source 2](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1631584892859_72892/FeatureServer), [source 3](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1639990901210_47291/FeatureServer), [source 4](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047202071_61921/FeatureServer), [source 5](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1640047456225_68329/FeatureServer), [source 6](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1671592436814_1059/FeatureServer), [source 7](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Observed historical surface mesh

**ID:** `kt-stereo-mesh`. Nonwatertight source-coloured triangulated patches

- Quantity: {"triangles": 225371, "vertices": 155891, "boundary_edges": 86061, "nonmanifold_edges": 0}; 3 catalogued files.
- Epoch: 1993-11-02.
- Processing: derived reconstruction.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: Diagnostic HK1980/local GLB / Relative fitted plane.
- Limitations: Not complete city or classified buildings; Holes retained, no invented backwalls/occluded roof; GLB axes local Y-up (E-837600,z,-(N-821200))
- Source links: [source 1](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA), [source 2](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Invalidated reconstruction evidence

**ID:** `kt-invalidated-reconstructions`. Preserved pre-repair outputs with explicit invalidation records

- Quantity: {"removed_dense_exported_points": 49}; 527 catalogued files.
- Epoch: Research generation 2026-10-13; source historical dates separate.
- Processing: superseded/invalidated.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Must not be displayed as accepted current geometry; Preserve diagnostic history and source dependencies
- Source links: [source 1](https://github.com/ayyararyan/kai-tak), [source 2](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Three-Dimensional Reconstruction — supporting and unclassified artifacts

**ID:** `kt-support-06`. Ancillary reports, scripts and outputs; consult file-level provenance gaps.

- Quantity: {}; 560 catalogued files.
- Epoch: not established.
- Processing: mixed/unclassified.
- Verification: Not independently verified.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Directory classification is navigational, not a verified source or transformation chain.
- Source links: 
- Reuse: source-specific; consult artifact decisions. New candidate includes 6 matched permitted files.

