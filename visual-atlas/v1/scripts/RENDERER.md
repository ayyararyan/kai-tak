# Blender scene renderer

Run from any directory with Blender 4.5 LTS:

```sh
blender -b --python-exit-code 1 --python /path/to/visual-atlas/v1/scripts/render_scene.py -- \
  --atlas /path/to/visual-atlas/v1 --job /path/to/job.json
```

`--python-exit-code 1` is important: Blender otherwise may return exit status zero after a Python exception. Only an image **and** its adjacent `.render.json` constitute a completed render. Visual acceptance is a separate check.

## Job contract

Required: `id`, `kind` (`stereo`, `modern`, `map`, `geography`), `epoch`, `style` (`cinematic`, `architectural`), `lighting` (`daylight`, `warm`), `mode` (`evidence`, `interpretive`), `camera`, `output`.

`camera` supplies `location`, `target`, `projection` (`ORTHO`, `PERSP`), plus `ortho_scale` and/or `lens`. Optional parameters: `sensor_width`, `clip_start`, `clip_end`. Coordinates are metres in the local east/north/source-height frame, origin E837500/N821000, EPSG:2326. Cameras are virtual exhibition viewpoints; the recorded azimuth is clockwise from **grid** north, not a magnetic aircraft heading.

Other parameters: `width`/`height` (default 3840/2160), `samples` (64), `engine` (`BLENDER_EEVEE_NEXT` or `CYCLES`), `transparent`, `exposure`, `save_blend` (false, true for default path, or path), `board_bounds`, `board_z`, `display_board`, `unknown_hatching`, `vertex_intensity`, `map_texture`, `outline_width`. Optional `marks=[{"label":"…","point":[x,y,z]}]` becomes `projected_marks` in metadata, with top-left-origin pixel coordinates and camera depth.

Overrides: `scene_path`, `scene_sha256`, `modern_roofs_path`, `geography_path`. Job `asset_hashes` maps absolute or atlas-relative derivative paths to SHA-256. Every geometry JSON and texture must match either a job-pinned checksum or the original source manifest at `metadata/input_manifest.json`; absent pins and mismatches fail closed. Job and manifest hashes are recorded too. Output paths may be absolute or atlas-relative. Input override paths should be absolute.

## Scientific geometry rules

- Stereo consumes **all** original `observed_mesh.vertices` XYZ and `observed_mesh.faces` triangle indices by default. Optional `stereo_bounds=[xmin,ymin,xmax,ymax]` selects only complete original triangles whose three vertices fall within the rectangle; it never cuts triangles or adds geometry. Original vertex indices, original/retained counts, bounds, and subset policy are retained. No smoothing, remeshing, hole filling, walls, solidification, or geometric scaling is applied. Photo-derived luminance can be ivory-tinted for display. The original source remains linked and hashed.
- Stereo Z is `relative_ground_plane`. Modern Z is `HKPD`. A job never combines them. Modern roofs require courtyard-safe pretriangulated `modern_roofs.json`, keyed by component ID. Rings retain inside walls. Invalid/missing heights or missing roof triangulations fail the render; they are not guessed.
- Map planes are geographically registered at a display Z, not terrain. Historical outlines stay flat and height-unknown. A 0.15 m line lift only avoids coplanar render artifacts and is recorded as display offset.
- Geography accepts source `image_plane`, `polyline`, `mesh` and `polygon` primitives. Filled polygons require upstream triangles; polygons without them remain outlines. `interpretive`, `contextual`, or `illustrative` features are omitted in evidence mode.
- Neutral exhibition boards and boundary strokes are tagged non-geographic. They are not land, terrain, coastline, water levels, or proof that missing regions were historically empty.
- Materials, sun angle, and lighting are artistic choices, not recovered facades or historical weather. There is no selective depth-of-field or generated facade detail.

## Outputs

PNG, optional editable packed `.blend`, and adjacent `.render.json` with camera matrix, lens/projection, grid azimuth, source frame, source hashes, source object counts, per-object provenance, output hash, software versions and elapsed render time. PNG annotation, publication metadata/captions, composites, gallery, source-rights gating and full-resolution visual acceptance belong to the parent atlas pipeline.

## Implementation verification

Blender 4.5.3 LTS on this workstation rendered 960×540 smoke views of stereo, modern core, 1989 registered map, historical geography mosaic and sparse hill observations. Those previews were inspected: topology holes remain visible; modern courtyard outlines are preserved; maps and hill evidence remain explicitly non-solid. These smoke checks establish renderer operation, **not** publication-quality acceptance of every final camera or four-kilopixel image.
