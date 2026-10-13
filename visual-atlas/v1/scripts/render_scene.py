#!/usr/bin/env python3
"""Reproducible evidence-only geometry adapter for Blender 4.5+.

blender -b --python render_scene.py -- --atlas /path/visual-atlas/v1 --job job.json
All coordinates: local EPSG:2326 east/north metres, origin E837500/N821000.
Z remains source-specific. A display board is never a terrain reconstruction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ORIGIN = [837500, 821000]
SOURCE_RECORDS = {}
EXPECTED_HASHES = {}
REQUIRE_HASH = False
PALETTE = {
    "ivory": (0.66, 0.60, 0.49, 1),
    "roof": (0.82, 0.78, 0.66, 1),
    "approximate": (0.34, 0.48, 0.53, 1),
    "accent": (0.64, 0.26, 0.12, 1),
    "water": (0.15, 0.34, 0.36, 1),
    "terrain": (0.38, 0.43, 0.30, 1),
    "asphalt": (0.18, 0.21, 0.22, 1),
    "board": (0.75, 0.77, 0.74, 1),
    "ink": (0.12, 0.19, 0.20, 1),
}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path, expected=None):
    path = Path(path).resolve()
    sha = digest(path)
    expected = expected or EXPECTED_HASHES.get(str(path))
    if REQUIRE_HASH and not expected:
        raise ValueError(f"Input has no pinned checksum: {path}")
    if expected and sha != expected:
        raise ValueError(f"Input checksum mismatch: {path}")
    SOURCE_RECORDS[str(path)] = sha
    return json.loads(path.read_text())


def material(name, color, roughness=0.8, emission=0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = color
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = color
    return mat


def tag(obj, **props):
    for k, v in props.items():
        obj[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) or v is None else v
    return obj


def mesh_object(name, vertices, faces, mat, **props):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return tag(obj, **props)


def line_object(name, points, mat, radius=0.6, closed=False, **props):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 1
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for p, xyz in zip(spline.points, points):
        p.co = (*xyz[:3], 1)
    spline.use_cyclic_u = closed
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return tag(obj, **props)


def image_plane(name, path, bounds, z=0, **props):
    path = Path(path).resolve()
    sha = digest(path)
    expected = EXPECTED_HASHES.get(str(path))
    if REQUIRE_HASH and not expected:
        raise ValueError(f"Image input has no pinned checksum: {path}")
    if expected and expected != sha:
        raise ValueError(f"Image input checksum mismatch: {path}")
    SOURCE_RECORDS[str(path)] = sha
    image = bpy.data.images.load(str(path), check_existing=True)
    mat = bpy.data.materials.new(name + " · archival texture")
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = image
    texture.interpolation = "Linear"
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Strength"].default_value = 0.85
    diffuse = nodes.new("ShaderNodeBsdfDiffuse")
    mix = nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 0.2
    output = nodes.new("ShaderNodeOutputMaterial")
    links.new(texture.outputs["Color"], emission.inputs["Color"])
    links.new(texture.outputs["Color"], diffuse.inputs["Color"])
    links.new(emission.outputs[0], mix.inputs[1])
    links.new(diffuse.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs["Surface"])
    x0, y0, x1, y1 = bounds
    obj = mesh_object(name, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [(0, 1, 2, 3)], mat, **props)
    uv = obj.data.uv_layers.new(name="Source registration")
    for loop, xy in zip(uv.data, [(0, 0), (1, 0), (1, 1), (0, 1)]):
        loop.uv = xy
    return obj


def stereo_scene(source, mats, job):
    data = source["observed_mesh"]
    if data["vertical_datum"] != "relative_ground_plane" or not data["available"]:
        raise ValueError("Stereo source must retain relative-ground-plane semantics")
    source_vertex_rows = data["vertices"]
    source_indices = list(range(len(source_vertex_rows)))
    faces = [f[:3] for f in data["faces"]]
    if job.get("stereo_bounds") is not None:
        x0, y0, x1, y1 = job["stereo_bounds"]
        if not (x1 > x0 and y1 > y0):
            raise ValueError("Invalid stereo subset bounds")
        inside = [x0 <= v[0] <= x1 and y0 <= v[1] <= y1 for v in source_vertex_rows]
        faces = [f for f in faces if all(inside[i] for i in f)]
        if not faces:
            raise ValueError("Stereo subset contains no complete source triangles")
        source_indices = sorted({i for f in faces for i in f})
        index_map = {old: new for new, old in enumerate(source_indices)}
        faces = [[index_map[i] for i in f] for f in faces]
        source_vertex_rows = [source_vertex_rows[i] for i in source_indices]
    vertices = [v[:3] for v in source_vertex_rows]
    obj = mesh_object("November 1993 · partial observed surfaces", vertices, faces, mats["ivory"],
                      evidence_level="B", source_epoch=data["source_epoch"], vertical_datum=data["vertical_datum"],
                      source="scene.json#/observed_mesh", complete_buildings=False, watertight=False,
                      nominal_camera_calibration=True, outside_control_hull_extrapolation=True,
                      source_vertices=len(data["vertices"]), source_triangles=len(data["faces"]),
                      retained_vertices=len(vertices), retained_triangles=len(faces),
                      subset_bounds=job.get("stereo_bounds"),
                      subset_policy="Retain complete original triangles only when all three original vertices lie inside bounds; no clipping or new triangles" if job.get("stereo_bounds") else "Full source mesh",
                      vertical_exaggeration=1.0)
    index_attr = obj.data.attributes.new(name="Original source vertex index", type="INT", domain="POINT")
    index_attr.data.foreach_set("value", source_indices)
    # Preserve topology and original per-vertex source intensities. No smoothing,
    # remeshing, extrapolation, hole filling, solidification or invented walls.
    if job.get("vertex_intensity", True):
        attr = obj.data.color_attributes.new(name="Source photograph intensity", type="FLOAT_COLOR", domain="POINT")
        values = []
        for v in source_vertex_rows:
            gray = sum(v[3:6]) / 765.0
            lum = 0.22 + 0.64 * gray
            values.extend((lum, lum * 0.94, lum * 0.82, 1.0))
        attr.data.foreach_set("color", values)
        mat = mats["ivory"].copy()
        mat.name = "Archival luminance · restrained ivory tint"
        vertex = mat.node_tree.nodes.new("ShaderNodeVertexColor")
        vertex.layer_name = attr.name
        mat.node_tree.links.new(vertex.outputs["Color"], mat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"])
        obj.data.materials[0] = mat
    return {"vertices": len(vertices), "triangles": len(faces), "source_vertices": len(data["vertices"]), "source_triangles": len(data["faces"]), "retained_vertices": len(vertices), "retained_triangles": len(faces), "subset_bounds": job.get("stereo_bounds"), "subset_policy": obj["subset_policy"], "objects": 1}, "relative_ground_plane"


def modern_scene(source, mats, job, atlas):
    modern = source["modern"]
    if modern["vertical_datum"] != "HKPD":
        raise ValueError("Modern scene requires explicit HKPD elevations")
    roofs = read_json(job.get("modern_roofs_path", atlas / "assets/modern_roofs.json"))
    if "features" in roofs:
        roofs = roofs["features"]
    if isinstance(roofs, list):
        roofs = {f["id"]: f for f in roofs}
    roof_count = wall_count = 0
    for f in modern["features"]:
        lower, upper = f["base_hkpd_m"], f["top_hkpd_m"]
        if lower is None or upper is None or not (math.isfinite(lower) and math.isfinite(upper)) or upper < lower:
            raise ValueError(f"Invalid source elevations {f['id']}")
        if f["id"] not in roofs:
            raise ValueError(f"Missing courtyard-safe roof triangles: {f['id']}")
        entry = roofs[f["id"]]
        triangles = entry["triangles"] if isinstance(entry, dict) else entry
        vertices, faces = [], []
        for tri in triangles:
            offset = len(vertices)
            points = [(p[0], p[1], upper) for p in tri]
            cross = (points[1][0] - points[0][0]) * (points[2][1] - points[0][1]) - (points[1][1] - points[0][1]) * (points[2][0] - points[0][0])
            if cross < 0:
                points.reverse()
            vertices.extend(points)
            faces.append(tuple(range(offset, offset + 3)))
        roof_faces = len(faces)
        for idx, ring in enumerate(f["rings_local"]):
            ring = [list(p[:2]) for p in ring]
            if ring[0] == ring[-1]:
                ring = ring[:-1]
            area = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))
            if (area > 0) != (idx == 0):
                ring.reverse()
            for a, b in zip(ring, ring[1:] + ring[:1]):
                offset = len(vertices)
                vertices.extend([(a[0], a[1], lower), (b[0], b[1], lower), (b[0], b[1], upper), (a[0], a[1], upper)])
                faces.append(tuple(range(offset, offset + 4)))
                wall_count += 1
        obj = mesh_object(f"2026 · {f['id']} · {f['name']}", vertices, faces, mats["roof"],
                          source_id=f["id"], source_epoch=f["epoch"], vertical_datum="HKPD", evidence_level="B",
                          source=modern["source_path"], base_hkpd_m=lower, top_hkpd_m=upper,
                          courtyard_rings=len(f["rings_local"]) - 1, available_terrain_dataset_epoch="2014–2015; not rendered",
                          height_transfer_to_historical=False)
        obj.data.materials.append(mats["ivory"])
        for poly in obj.data.polygons:
            poly.material_index = int(poly.index >= roof_faces)
        roof_count += roof_faces
    return {"components": len(modern["features"]), "roof_triangles": roof_count, "walls": wall_count}, "HKPD"


def map_scene(source, mats, job, scene_path):
    epoch = job["epoch"]
    registered = next(m for m in source["maps"] if m["epoch"] == epoch)
    path = scene_path.parent.parent / registered["source_path"]
    if digest(path) != registered["sha256"]:
        raise ValueError(f"Registered map checksum mismatch: {path}")
    if job.get("map_texture", True):
        image_plane(epoch + " survey edition · registered reference", job.get("map_image_path",path), [0, 0, 750, 600],
                    source=str(path), source_epoch=epoch, evidence_level="A", vertical_datum="display_plane_not_terrain",
                    distribution="Local author review; source imagery rights must be checked before distribution")
    count = 0
    for f in source["historical_faces"]:
        if f["source_epoch"] != epoch:
            continue
        if f["height_m"] is not None or f["physical_volume"] is not None:
            raise ValueError("Historical mapped outlines must remain height-unknown")
        line_object(f["name"] + " · height unknown", [(p[0], p[1], 0.15) for p in f["outer_local"]],
                    mats["accent"], job.get("outline_width", 0.55), closed=True,
                    source="scene.json#/historical_faces/" + f["id"], source_epoch=epoch, evidence_level="B",
                    height_m=None, display_offset_m=0.15, physical_volume=False, vertical_datum="display_plane_not_terrain")
        count += 1
    return {"registered_map_planes": int(job.get("map_texture", True)), "height_unknown_outlines": count}, "display_plane_not_terrain"


def geography_scene(mats, job, atlas):
    path = Path(job.get("geography_path", atlas / "assets/geography.json"))
    data = read_json(path)
    if data.get("origin_epsg2326", ORIGIN) != ORIGIN:
        raise ValueError("Geography origin mismatch")
    count = omitted = 0
    for f in data["features"]:
        interpretive = f.get("interpretive", False) or f.get("contextual", False) or f.get("illustrative", False)
        if job["mode"] == "evidence" and interpretive:
            omitted += 1
            continue
        if interpretive and not (f.get("label") or f.get("name")):
            raise ValueError("Interpretive context must have an explicit name/label")
        props = {k: f[k] for k in ("source", "evidence_level", "epoch", "label", "vertical_datum", "interpretive", "contextual", "illustrative") if k in f}
        props["display_is_historical_terrain"] = False
        name = f["name"]
        mat = mats.get(f.get("material", "approximate"), mats["approximate"])
        if f["type"] == "image_plane":
            a, b = f["coordinates"]
            image_plane(name, f["image_path"], [a[0], a[1], b[0], b[1]], a[2] if len(a) > 2 else 0, **props)
        elif f["type"] == "polyline":
            coords = [list(p) if len(p) == 3 else [*p, 0] for p in f["coordinates"]]
            line_object(name, coords, mat, f.get("width", 2), f.get("closed", False), **props)
        elif f["type"] == "mesh":
            mesh_object(name, f["vertices"], f["faces"], mat, **props)
        elif f["type"] == "polygon":
            # Concave outlines must be triangulated upstream; a raw ngon is not
            # accepted because implicit tessellation could conceal courtyard gaps.
            if "triangles" in f:
                verts = [p if len(p) == 3 else [*p, 0] for tri in f["triangles"] for p in tri]
                mesh_object(name, verts, [list(range(i, i + 3)) for i in range(0, len(verts), 3)], mat, **props)
            else:
                coords = [list(p) if len(p) == 3 else [*p, 0] for p in f["coordinates"]]
                line_object(name, coords, mat, f.get("width", 2), True, **props)
        else:
            raise ValueError(f"Unsupported geography primitive {f['type']}")
        count += 1
    return {"features": count, "interpretive_features_omitted": omitted}, data.get("vertical_datum", "display_plane_not_terrain")


def display_board(bounds, z, mats, job):
    x0, y0, x1, y1 = bounds
    # No fabricated thickness: a flat exhibition support, explicitly identified.
    mesh_object("Exhibition support · NOT geographic terrain", [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [(0, 1, 2, 3)], mats["board"],
                evidence_level="presentation_only", physical_geography=False, purpose="Neutral missing-evidence display support", z_is_display_choice=True)
    line_object("Evidence display boundary · not a coastline", [(x0, y0, z + 0.05), (x1, y0, z + 0.05), (x1, y1, z + 0.05), (x0, y1, z + 0.05)],
                mats["approximate"], max(x1 - x0, y1 - y0) * 0.0006, True, physical_geography=False)
    if job.get("unknown_hatching", False):
        step = max(x1 - x0, y1 - y0) / 45
        for i in range(1, 45):
            x = x0 + i * step
            if x < x1:
                line_object("Missing-evidence display hatch", [(x, y0, z + 0.03), (x, y1, z + 0.03)], mats["hatch"], step * 0.012, physical_geography=False)


def setup_camera(job):
    cfg = job["camera"]
    data = bpy.data.cameras.new("Recorded virtual camera")
    camera = bpy.data.objects.new("Recorded virtual camera", data)
    bpy.context.collection.objects.link(camera)
    camera.location = cfg["location"]
    direction = Vector(cfg["target"]) - camera.location
    if direction.length < 1e-6:
        raise ValueError("Camera and target must differ")
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    data.type = cfg["projection"]
    data.lens = cfg.get("lens", 50)
    data.ortho_scale = cfg.get("ortho_scale", 1000)
    data.sensor_width = cfg.get("sensor_width", 36)
    data.shift_x = cfg.get("shift_x", 0)
    data.shift_y = cfg.get("shift_y", 0)
    data.clip_start = cfg.get("clip_start", 0.1)
    data.clip_end = cfg.get("clip_end", 100000)
    data.dof.use_dof = False  # Evidence must not be hidden by selective defocus.
    bpy.context.scene.camera = camera
    tag(camera, source="Virtual artistic viewpoint; not an historical aircraft pose", **cfg)
    return camera


def setup_lighting(job, extent, center):
    scene = bpy.context.scene
    world = bpy.data.worlds.new("Exhibition ambience")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.73, 0.79, 0.82, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.65
    # Separating the exhibition backdrop from environment illumination changes
    # presentation only: it never introduces haze or hides source geometry.
    nodes, links = world.node_tree.nodes, world.node_tree.links
    light_path = nodes.new("ShaderNodeLightPath")
    backdrop = nodes.new("ShaderNodeBackground")
    backdrop.inputs["Color"].default_value = ((0.045, 0.065, 0.075, 1) if job["kind"] == "stereo" else (0.72, 0.74, 0.71, 1))
    backdrop.inputs["Strength"].default_value = 1.0
    mix = nodes.new("ShaderNodeMixShader")
    links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
    links.new(nodes["Background"].outputs[0], mix.inputs[1])
    links.new(backdrop.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], nodes["World Output"].inputs["Surface"])
    scene.world = world
    warm = job["lighting"] == "warm"
    sun = bpy.data.lights.new("Warm artistic afternoon" if warm else "Clear artistic daylight", "SUN")
    sun.energy = 2.2 if warm else 2.0
    sun.angle = math.radians(12 if warm else 18)
    sun.color = (1.0, 0.79, 0.60) if warm else (1.0, 0.97, 0.91)
    obj = bpy.data.objects.new(sun.name, sun)
    bpy.context.collection.objects.link(obj)
    obj.rotation_euler = (math.radians(58 if warm else 35), math.radians(-20), math.radians(-35))
    tag(obj, historical_weather=False, artistic_choice=True)
    area = bpy.data.lights.new("Large soft exhibition fill", "AREA")
    area.energy = extent * extent * 4.0
    area.shape = "DISK"
    area.size = extent * 1.4
    fill = bpy.data.objects.new(area.name, area)
    bpy.context.collection.objects.link(fill)
    fill.location = (center[0] - extent * .4, center[1] - extent * .1, extent * 1.4)
    fill.rotation_euler = (Vector((*center, 0)) - fill.location).to_track_quat("-Z", "Y").to_euler()


def main():
    global REQUIRE_HASH
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", required=True, type=Path)
    parser.add_argument("--job", required=True, type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    started = time.time()
    atlas = args.atlas.resolve()
    job = read_json(args.job)
    manifest_path = atlas / "metadata/input_manifest.json"
    manifest = read_json(manifest_path)
    for item in manifest["files"]:
        if item.get("available") and item.get("sha256"):
            EXPECTED_HASHES[str((atlas.parents[1] / item["path"]).resolve())] = item["sha256"]
    # Generated derivative inputs must also be pinned; never trust the newest
    # local roof/geography file merely because its path exists.
    for path, sha in job.get("asset_hashes", {}).items():
        p = Path(path)
        if not p.is_absolute():
            p = atlas / p
        EXPECTED_HASHES[str(p.resolve())] = sha
    REQUIRE_HASH = True
    for field, allowed in [("kind", {"stereo", "modern", "map", "geography"}), ("style", {"cinematic", "architectural"}), ("mode", {"evidence", "interpretive"}), ("lighting", {"daylight", "warm"})]:
        if job[field] not in allowed:
            raise ValueError(f"Invalid job {field}: {job[field]}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1
    scene.render.engine = job.get("engine", "BLENDER_EEVEE_NEXT")
    if scene.render.engine == "CYCLES":
        scene.cycles.samples = job.get("samples", 64)
        scene.cycles.use_denoising = True
    elif hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = job.get("samples", 64)
    scene.render.resolution_x = job.get("width", 3840)
    scene.render.resolution_y = job.get("height", 2160)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA" if job.get("transparent", False) else "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = job.get("transparent", False)
    scene.render.image_settings.compression = 30
    scene.view_settings.view_transform = "AgX" if job["style"] == "cinematic" else "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = job.get("exposure", 0)
    scene.view_settings.gamma = 1
    mats = {k: material(k, v) for k, v in PALETTE.items()}
    if job["kind"] == "stereo":
        mats["board"] = material("Dark slate exhibition support", (0.055, 0.085, 0.095, 1))
    mats["hatch"] = material("Faint unknown-region hatch", (0.63, 0.67, 0.64, 1))
    default_source = atlas.parents[1] / "research/checkers-runway13/reconstruction/block_matching/scene/scene.json"
    scene_path = Path(job.get("scene_path", default_source)).resolve()
    if job["kind"] != "geography":
        source = read_json(scene_path, job.get("scene_sha256"))
        if source["origin_epsg2326"] != ORIGIN:
            raise ValueError("Scene coordinate origin mismatch")
        if job["kind"] == "stereo":
            counts, datum = stereo_scene(source, mats, job)
        elif job["kind"] == "modern":
            counts, datum = modern_scene(source, mats, job, atlas)
        else:
            counts, datum = map_scene(source, mats, job, scene_path)
    else:
        counts, datum = geography_scene(mats, job, atlas)
    bpy.context.view_layer.update()
    geometry = [obj for obj in scene.objects if obj.type in {"MESH", "CURVE"}]
    points = [obj.matrix_world @ Vector(c) for obj in geometry for c in obj.bound_box]
    if not points:
        raise ValueError("No source geometry rendered")
    bounds = job.get("board_bounds", [min(p.x for p in points) - 20, min(p.y for p in points) - 20, max(p.x for p in points) + 20, max(p.y for p in points) + 20])
    board_z = job.get("board_z", min(p.z for p in points) - 3.0)
    if job.get("display_board", True):
        display_board(bounds, board_z, mats, job)
    center = [(bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2]
    extent = max(bounds[2] - bounds[0], bounds[3] - bounds[1])
    setup_lighting(job, extent, center)
    camera = setup_camera(job)
    scene["atlas_job"] = json.dumps(job)
    scene["origin_epsg2326"] = ORIGIN
    scene["axis_mapping"] = "Blender X=east, Y=north, Z=source height. No GLB transformation applied: original ENZ scene JSON used."
    scene["vertical_datum"] = datum
    scene["vertical_exaggeration"] = 1.0
    scene["reconstruction_type"] = job["mode"]
    scene["historical_epoch"] = job["epoch"]
    scene["lighting_is_historical_weather"] = False
    bpy.context.view_layer.update()
    output = Path(job["output"])
    if not output.is_absolute():
        output = atlas / output
    output.parent.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(output)
    if job.get("save_blend"):
        blend = Path(job["save_blend"]) if isinstance(job["save_blend"], str) else atlas / "scenes" / (job["id"] + ".blend")
        if not blend.is_absolute():
            blend = atlas / blend
        blend.parent.mkdir(parents=True, exist_ok=True)
        # Packed registered images keep the editable scene usable offline.
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)
    cfg = job["camera"]
    delta = Vector(cfg["target"]) - Vector(cfg["location"])
    record = {
        "id": job["id"], "epoch": job["epoch"], "kind": job["kind"], "style": job["style"], "mode": job["mode"],
        "lighting": job["lighting"], "lighting_historical_weather": False,
        "blender_version": bpy.app.version_string, "python_version": sys.version,
        "engine": scene.render.engine, "samples_requested": job.get("samples", 64),
        "origin_epsg2326": ORIGIN, "horizontal_crs": "EPSG:2326", "vertical_datum": datum,
        "axis_mapping": "X=east, Y=north, Z=source height", "vertical_exaggeration": 1,
        "source_counts": counts, "source_sha256": SOURCE_RECORDS,
        "camera": {**cfg, "location_epsg2326": [cfg["location"][0] + ORIGIN[0], cfg["location"][1] + ORIGIN[1], cfg["location"][2]],
                   "target_epsg2326": [cfg["target"][0] + ORIGIN[0], cfg["target"][1] + ORIGIN[1], cfg["target"][2]],
                   "world_matrix": [list(row) for row in camera.matrix_world],
                   "rotation_euler_radians": list(camera.rotation_euler), "sensor_width_mm": camera.data.sensor_width,
                   "grid_azimuth_degrees": math.degrees(math.atan2(delta.x, delta.y)) % 360,
                   "elevation_angle_degrees": math.degrees(math.atan2(delta.z, math.hypot(delta.x, delta.y))),
                   "bearing_note": "Grid-north camera direction, not true/magnetic aircraft heading",
                   "view_frame": [list(v) for v in camera.data.view_frame(scene=scene)]},
        "display_board": {"bounds": bounds, "z": board_z, "is_terrain": False},
        "width": scene.render.resolution_x, "height": scene.render.resolution_y,
        "render_seconds": round(time.time() - started, 3), "output": str(output), "output_sha256": digest(output),
        "objects": [{"name": o.name, "type": o.type, "metadata": dict(o.items())} for o in scene.objects],
        "landmark_pixels": {},
        "projected_marks": [],
    }
    for landmark in job.get("landmarks", []):
        p = world_to_camera_view(scene, camera, Vector(landmark["position"]))
        record["landmark_pixels"][landmark["name"]] = {"x": p.x * scene.render.resolution_x, "y": (1 - p.y) * scene.render.resolution_y, "camera_depth": p.z}
    for mark in job.get("marks", []):
        p = world_to_camera_view(scene, camera, Vector(mark["point"]))
        record["projected_marks"].append({"label": mark["label"], "point": mark["point"], "x": p.x * scene.render.resolution_x, "y": (1 - p.y) * scene.render.resolution_y, "camera_depth": p.z})
    output.with_suffix(".render.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"ATLAS_RENDER_COMPLETE {job['id']} {output} {record['render_seconds']}s", flush=True)


if __name__ == "__main__":
    main()
