# Kai Tak evidence-linked 3D workbench

Open [index.html](index.html) directly in a browser. Plotly and all maps/data required by the viewer are embedded; no CDN or server is required. Keep the surrounding project folder for source/download links. [overview.png](overview.png) is a separately generated static core-area 3D preview, not a browser screenshot.

## Three distinct views

1. **1993 stereo · 3D:** default conservative observed-surface patches, with a selector to return to genuine image-triangulated points from A36142/A36143, 1993-11-02. The 171,307-point dense export is the full producer artifact; the embedded browser preview keeps every third exported point (57,103 total) and defaults to the 750 × 600 m map core. “Wider stereo coverage” reveals its wider observed footprint. The thinning is display-only; complete CSV/PLY downloads retain the producer data. The surface mesh connects only producer-accepted neighbouring image-grid observations; it is non-watertight, contains no hole filling or unseen building faces, and is not a complete building solid. Sparse manually interpreted ground/roof points are overlaid for evidence inspection. Map outlines lie on a labelled display reference plane, not a terrain/roof model.
2. **Maps & matches:** selected 1989-10, 1994-07 or 1997-04 survey sheet, 15 mapped forms / 45 reviewed source faces, and four road-centre blockwise work cells. Click a face for source, date, review and unresolved height/presence. A date selector changes the map evidence, not the 1993 photo epoch.
3. **2026 comparison:** 464 current-source polygon components, with observed approximate base/top HKPD elevations, displayed as walls and top outlines, preserving courtyard rings and their interior walls. Ten invalid/missing/inconsistent components are explicitly listed as omitted. No historical footprint is extruded using those modern heights. No relative-height photo points are combined with absolute HKPD elevation in this view.

## Semantics preserved

- Historical face metric heights and volumes remain **null**. All 45 faces have null height and no physical solid.
- Stereo Z is relative to a fitted park/road plane, **not HKPD**. Camera calibration is nominal. The local map-control stereo holdout RMS is **5.754 m**, distinct from the separate single-image planar registration result.
- Only **3,780 / 171,307** dense points lie inside the map-control hull. Outside-hull points are explicitly extrapolated, not equally controlled observations.
- Dense points are unclassified image surfaces, potentially including ground, roofs, trees and erroneous correspondences. They are not automatically buildings. No watertight building mesh, complete roof inventory, terrain surface, height interval, clearance or whole-city completeness is asserted.
- Source coordinates and SHA256 values are included in [scene.json](scene.json). Complete producer coordinates remain in linked original CSV/PLY exports; browser preview coordinates are local EPSG:2326 offsets from E837500/N821000.

## Build and verification

```sh
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/scene/build_scene.py
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/block_matching/scene/render_snapshot.py
research/checkers-runway13/geospatial/.venv/bin/python -m unittest discover -s research/checkers-runway13/reconstruction/block_matching/scene -p test_scene.py -v
```

Eleven semantic tests pass. Acceptance covers: exact historical source geometry/null heights; separate modern epoch/datum; relative sparse semantics; all displayed dense coordinates matched to source CSV; current input hashes; and bundled offline viewer/control structure. JavaScript passes `node --check`. A Node test with DOM/Plotly stubs also passes default mesh construction, points switch, courtyard ring traces, separate modern datum, source epoch switching and click-detail construction. Stubs do not verify browser rendering or WebGL. Static overview visually inspected. **Browser interaction remains unverified:** parent attempted both file and localhost navigation through OpenClaw; navigation policy blocked both. No bypass was attempted. This is an actual inspection blocker, not a successful browser test.

A working viewer does not complete the full historical reconstruction.

## Review repairs

Sparse regeneration now requires `passes_diagnostic_5px_filter=True` and `positive_depth_both_views=True` explicitly; rejected rows are omitted with counts/IDs. A fixture verifies rejected and blank-flag rows cannot reappear as accepted roofs. The modern comparison retains interior rings, tested against component `3810921432T20050430:0`. The observed-surface adapter checks all producer-input hashes and refuses a mesh whose point/report/QC inputs changed.

## Corrected final geometry

After the dense interpolation-support repair, the final source export has **171,307 points** and the conservative observed surface has **225,371 triangles / 155,891 vertices**. The scene was rebuilt only after the producer confirmed corrected outputs stable; stale affected geometry was not reused. Source-file hashes and all mesh-input hashes pass the adapter/tests. Full surface GLB and PLY downloads are linked in the viewer; browser points are a clearly labelled 57,103-point display sample.
