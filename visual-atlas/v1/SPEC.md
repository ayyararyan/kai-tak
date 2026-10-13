---
title: Evidence-led Kai Tak visual atlas v1
type: feature
created: 2026-10-13
status: in-review
baseline_commit: e4aa7d8
context: []
---

<frozen-after-approval reason="Aryan supplied the complete atlas design and explicitly requested implementation">
## Intent
Create a publication-quality, reproducible 3D visual atlas of Kai Tak and Kowloon for public understanding and author review. The supplied sixteen-section brief is the controlling scope. Deliver actual rendered images, editable/reproducible Blender scenes, camera records, source/rights register, verification and a local static exhibition gallery.

## Boundaries & Constraints
Always preserve source epochs, coordinates, heights and missingness. Use EPSG:2326 east/north to Blender X/Y and the explicitly named vertical datum to Z, with a recorded local origin. Preserve source GLB Y-up mapping if imported. No horizontal distortion or undisclosed vertical exaggeration. Keep relative stereo and absolute HKPD views separate. Use actual archived geometry, restored through the existing hash-verifying process. Preserve unrelated white-paper work and original scientific files.

The image hierarchy is A direct historical observations, B approximate/partial reconstruction, C missing evidence. The stereo is a B conditional reconstruction from historical observations: nominal camera calibration and extensive control extrapolation remain disclosed. Historical footprints without heights stay flat. Unknown regions must not imply historically empty land. Interpretive context is separately selectable and never called verified history. No arbitrary building heights, no invented facades, no modern skyline relabelled 1993. No generative historical architecture. No research trajectory presented as a flown path. Magnetic/grid/true bearings remain distinct. Date discrepancy A36143 retained. Map editions do not establish precise construction dates.

Produce two coordinated styles (cinematic and architectural) and two light rigs (clear daylight and warm late-afternoon), with matched geometry. Lighting is artistic, not evidence of weather. Evidence-led and interpretive modes must be distinguishable. Camera metadata includes position, target, orientation, projection/lens and frame/datum. Comparison cameras match.

Deliver the complete twelve-subject storyboard with images or explicitly evidence-limited alternatives: overview, runway/water, city beneath aircraft, checkerboard/final turn, virtual pilot perspective, alignment, 1989 maps, November 1993 surface, 1989/1994/1997 comparison, historical/2026 comparison, photograph/surface/interpretation triptych, panoramic atlas. Prioritize stereo, modern, dated maps, then wider geography. Image11 may withhold the original photographic panel if redistribution rights cannot be established; document the actual source and local source pointer. This is a source-limited alternative, not a fabricated substitute.

Every finished image has epoch and reconstruction type in image metadata and companion captions. Annotated and unannotated 3840x2160 PNGs where resources allow; web copies, A4-compatible outputs, useful selected vertical/square crops and transparent overlays. At least twelve polished images unless archive coverage justifies a documented subset. Multiple useful angles, historical distinctions and matched comparisons required. Gallery must offer large previews, captions/dates/locations/confidence/attribution/downloads and methods. No external publication or communication authorized.

Ask first only for new model meaning, external publication or material spending. Existing implementation authorization needs no second approval.

## I/O & Edge-Case Matrix
| State | Required behavior |
|---|---|
| Archive/input hash mismatch | Refuse processing affected source; retain diagnostic |
| Height absent or incompatible | No solid or datum merge; explicit omission |
| Unverified coastline/terrain epoch | No claimed historical surface; labelled context or bounded alternative |
| Invalid modern polygon/heights | Explicit omissions, preserve courtyards |
| Photo/map rights unresolved | Local review only; no original-image public distribution |
| Render exists | Inspect pixels, composition, labels and scientific semantics before acceptance |
</frozen-after-approval>

## Code Map
Existing sources: `../../research/checkers-runway13/reconstruction/block_matching/scene/`, its `build_scene.py`, observed PLY/GLB in `aerial_registration/`, reviewed historical faces, chronology, geospatial and integrated geometry. Existing `../../scripts/fetch_data.py` and publication manifests govern restoration.

## Tasks & Acceptance
- [x] DATA-01 `metadata/` — audit file inventory, verify archive/member hashes, record source rights and available/missing files.
- [x] DESIGN-01 `storyboard/` — all twelve subjects, alternatives, captions, evidence levels and recommended views.
- [x] SCENE-01 `scripts/`, `scenes/` — reproducible Blender construction with named source objects and correct coordinate/datum mapping.
- [x] RENDER-01 `renders/` — twelve subject outputs/justified alternatives, two styles/light rigs/modes, multiple angles, 4K annotated/unannotated, web/print/crops/overlays.
- [x] COMP-01 `comparisons/` — matched-date and modern/historical panels with preserved differing evidence depth.
- [x] OUT-01 `gallery/index.html`, `README.md` — local static exhibition, full-resolution links, methods and strongest four-to-six recommendations.
- [ ] VAL-01 `qa/` — numerical/geographic/datum/missingness tests, source hashes, representative regeneration, visual inspection of every output at full and reading size.
- [x] OPS-01 `PROJECT_STATE.md`, `TRACEABILITY.md` — precise completion/limits, dependency versions, artifact hashes and reproducibility commands.

Given restored sources, when prepared, all used inputs must match recorded hashes and unsupported elevations remain absent. Given a source surface, when rendered, original vertices/triangles must not be fabricated or hole-filled. Given comparison panels, camera geometry and extents must match, with incompatible datum panels explicitly separated. Given the completed gallery, every delivered image must resolve locally with captions, provenance and high-resolution download. Given a clean representative rebuild, scene and render must regenerate from documented inputs. Successful rendering alone does not pass visual acceptance.

## Design Notes
Architectural objects on neutral display planes communicate absence without pretending to a complete terrain model. Context geometry only enters a labelled interpretive scene. Clean meshes retain holes and original structure; no smoothing of geometry. Source-linked data and cameras are separate from style/lighting. Build outside the scientific reconstruction.

## Verification
Run atlas acceptance tests, inspect contact sheets and full-size images, regenerate representative scenes, check gallery references and record tools. Report scientific correctness, requested coverage and delivery readiness separately.

## Spec Change Log
Initial specification preserves full user scope; no new approval gate or scope reduction.

## Implementation handoff
All image subjects and source deliverables produced. VAL-01 remains unchecked because browser navigation policy prevented actual gallery interaction/layout verification. See TRACEABILITY.md and qa/REPORT.md; this is not an unconditional completion claim. Review order: README → gallery/index.html or print PDF → qa/REPORT.md → metadata/SOURCE_AUDIT.md → TRACEABILITY.md → scripts/.

## Authorized delivery change — 2026-10-13
Aryan explicitly requested pushing the atlas to GitHub. This supersedes the original local-only delivery boundary for this snapshot. No scientific/model changes; no automatic future publishing or separate website deployment.
