# Terrain-owner handoff for approximate landing analysis

13 October 2026. Parent-owned interface request; not a claim the terrain owner has delivered these fields. Coordinate with `reconstruction/chronology/SPEC.md`. Do not change chronology outputs just to pass this interface.

## Current handoff evidence

Stable `reconstruction/chronology/HANDOFF.json`, `REPORT.md` and validation have now been received and inspected. On 13 October 2026 the approximation lane freshly verified the size and SHA256 of all nine artifacts listed in HANDOFF. Source-package acceptance is complete; historical clearance acceptance is not. A map that omits a building is not evidence of its absence.

| Contract field | Received evidence | Integration status |
|---|---|---|
| Identity/coverage | Nine hashed handoff artifacts; local WGS84 AOI [114.10,22.27,114.25,22.40] | Accepted as documentary/source package, not a flight corridor |
| Epoch | 1993-11-04 documentary example; 2014–15 terrain; 2026-09-21 current buildings | Mixed epochs preserved; historical scene not reconstructed |
| Coordinates | EPSG:4326 footprints/indexes, EPSG:2326 terrain, HKPD elevations | Aviation datum transform and historical runway registration absent |
| Runway/entry | No new registered runway/entry state in handoff | Synthetic start/axes cannot be relabelled historical |
| Terrain | Local 5 m raster; source ±5 m at 90% statement | No hard height envelope or verified 1993 surface |
| Structures | Documentary classifications and current polygons; zero historical footprints verified; 10,026 local top heights missing | Historical occupied volumes unavailable |
| Unknowns | AOI-wide historical uncertainty mask now delivered | Epistemic non-certification, not physical occupancy or proof of infeasibility |
| Quality/provenance | Stable report, validation and source matches | Package integrity verified; geometric registration remains absent |
| Aircraft/tracking | Not a terrain-owner deliverable | Whole-aircraft geometry and justified tracking error still required |
| Statistical calibration | No relevant landing-error/wind/braking distributions | Prediction intervals unavailable independently of scene completion |

Do not turn the whole-AOI mask into an obstacle wall or treat unknown cells as free space. Both would change the problem. No new terrain-aware solution can be certified from this package alone. No solver/configuration/certificate was changed during reconciliation.

## Required input groups before terrain-aware certification

| Group | Required information | Treatment when missing |
|---|---|---|
| Identity | Immutable scene ID, file hashes, producer, verification date, dataset version | Do not issue a certificate tied only to a mutable filename. |
| Epoch | Intended scenario date; actual observation/capture/edition dates; temporal validity intervals per feature | Do not merge years or interpolate building presence silently. |
| Coordinates | Horizontal CRS; grid/true/magnetic north conventions; vertical datum; units; transform and validation residuals | Do not compare geographic HKPD heights directly with runway-relative z. |
| Runway | Historical threshold position, bearing, usable distance, elevation/profile and geometry; sources and uncertainty | Keep runway registration blocked. Current redeveloped Kai Tak is not the historical landing surface. |
| Approach entry/procedure | Source-backed entry fix or declared counterfactual entry state, navigation/visual-turn constraints and allowed airspace for the selected epoch | The synthetic (-2500,1000,140) m start and 400 m tube are not automatically historical constraints. |
| Terrain | Raster/mesh, resolution, spatial coverage, interpolation semantics, error description, surface-versus-bare-ground classification | Preserve unknown cells; no default flat ground/sea or automatic hard ±5 m buffer. |
| Structures | Geometry, base/top elevations or bounds, presence classifications and validity dates, stable historical IDs and evidence | Missing heights/presence remain unknown. Modern height is not historical height without evidence. |
| Uncertainty | Distinguish guaranteed/conservative intervals from statistical accuracy statements and unresolved alternatives | Do not convert confidence statements into deterministic limits or assign probability to unresolved alternatives. |
| Coverage | Known, unknown and unresolved areas/objects, including possible omitted/demolished features | A blank/modern-only region cannot certify historical clearance. |
| Quality | Geometric validity, spatial registration checks, date conflicts, manually inspected vs automatic classification | Keep confidence/evidence categories available downstream; do not silently repair. |
| Rights | Attribution and reuse terms | Retain with derived scenes. |

The acquisition AOI is not an approved flight corridor or a completeness certificate. The landing lane will determine whether the full candidate and required recovery/go-around region are covered; incomplete coverage is an explicit dependency.

## Responsibilities after receipt

The approximation lane must validate the dated scene, register the historical runway, and construct conservative clearance constraints for the **whole aircraft**. Scene data describe the world; they do not supply aircraft geometry, tracking error or operational clearance standards. Those inputs must be sourced and declared separately. A representative point clearing a roof does not establish wingtip/tail clearance in bank.

Let S(t) be the aircraft occupied volume for a candidate attitude and position. Let E(t) be a justified tracking/registration uncertainty set. Terrain/obstacle feasibility requires the swept set S(t) expanded by E(t) to avoid the applicable obstacle envelope throughout the path. Unknown obstacles intersecting that expanded path cannot be certified clear. This is a mathematical interface, not a chosen numerical clearance margin.

Scene acceptance and statistical calibration are separate gates. A useful visual scene may be delivered before a clearance-ready scene; retain both statuses. No hypothetical `verified=true` field alone may waive source coverage or uncertainty gaps.
