"""Build dated map-point evidence; deliberately NOT a historical clearance surface.

Run with geospatial/.venv/bin/python. Inputs are manually inspected, hash-pinned
observations and a separate inspection receipt. Rebuild never edits source data,
aircraft configuration, prior geometry, or published snapshots.
"""
from __future__ import annotations

import argparse
import calendar
import copy
from datetime import date, datetime, timedelta
import hashlib
import json
import math
from pathlib import Path
import re

from PIL import Image
from pyproj import Transformer

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
FACES_PATH = "reconstruction/block_matching/historical_faces.geojson"
FACES_SHA256 = "f866def637ad2c3495e9a9463a6abfc1b04cbf600b8b52b6ed5ee503bd749ef7"
CORE = [114.16, 22.30, 114.22, 22.35]
TO_WGS84 = Transformer.from_crs(2326, 4326, always_xy=True)
TO_GRID = Transformer.from_crs(4326, 2326, always_xy=True)
CLASSES = {"terrain_spot", "elevated_platform_spot"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path):
    def invalid(value):
        raise ValueError(f"Nonfinite JSON constant: {value}")
    return json.loads(Path(path).read_text(), parse_constant=invalid)


def finite(value, name):
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value), f"{name} must be a finite number")
    return float(value)


def resolved_input(root, relative):
    require(isinstance(relative, str) and relative, "Missing input path")
    path = Path(relative)
    require(not path.is_absolute(), f"Input must be project-relative: {relative}")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()), f"Input escapes project: {relative}")
    require(resolved.is_file(), f"Missing input: {relative}")
    return resolved


def verify_file(root, relative, expected):
    require(isinstance(expected, str) and re.fullmatch(r"[a-f0-9]{64}", expected),
            f"Missing/invalid SHA256 pin for {relative}")
    path = resolved_input(root, relative)
    require(sha256(path) == expected, f"SHA256 mismatch: {relative}")
    return path


def verify_hash_fields(root, record):
    """Every explicit hash must have a corresponding file path; no ignored pins."""
    verified = {}
    for key, digest in record.items():
        if key != "sha256" and not key.endswith("_sha256"):
            continue
        stem = "path" if key == "sha256" else key[:-7]
        candidates = [stem, stem + "_path", stem + "_image"]
        if stem == "datum_evidence":
            # datum_evidence itself is interpretation prose, never a file path.
            candidates = ["datum_evidence_image", "datum_evidence_path"]
        found = [name for name in candidates if name in record]
        require(found, f"Hash {key} has no paired file path")
        for name in found:
            relative = record[name]
            verify_file(root, relative, digest)
            verified[relative] = digest
    return verified


def source_period(source_month, query_date):
    require(isinstance(source_month, str) and re.fullmatch(r"\d{4}-\d{2}", source_month),
            "Source date must have YYYY-MM precision")
    year, month = map(int, source_month.split("-"))
    start = date(year, month, 1)
    end = date(year, month, calendar.monthrange(year, month)[1])
    query = date.fromisoformat(query_date)
    relation = "before_query" if end < query else "after_query" if start > query else "query_month_ambiguous"
    return {"edition_period_start": start.isoformat(), "edition_period_end": end.isoformat(),
            "source_period_relative_to_query": relation,
            "date_precision": "month", "query_date_presence": "unknown",
            "individual_object_survey_date": None}


def validate_source(root, source, query_date):
    for key in ("id", "path", "sha256", "source_date", "sheet", "registered_png",
                "registered_png_sha256", "registered_metadata", "registered_metadata_sha256"):
        require(key in source, f"Source missing {key}")
    require(source.get("vertical_datum") == "HKPD", "Unsupported/unknown source vertical datum")
    require(source.get("units") == "metres", "Source metric elevations require printed metre units")
    datum_paths = [key for key in ("datum_evidence_image", "datum_evidence_path") if source.get(key)]
    require(datum_paths, "Source missing datum evidence image/path")
    for key in datum_paths:
        require(key + "_sha256" in source or "datum_evidence_sha256" in source,
                "Source missing paired datum evidence hash")
    datum_text = source.get("datum_evidence")
    require(isinstance(datum_text, str) and len(datum_text.strip()) >= 20 and
            re.search(r"principal\s+datum|\bHKPD\b", datum_text, re.I) and
            re.search(r"\bmet(?:re|er)s?\b", datum_text, re.I),
            "Source missing substantive datum evidence text describing datum and metric units")
    for key, value in source.items():
        if key.endswith("_accuracy_m"):
            require(value is None, f"Unidentified source accuracy must remain null: {key}")
    period = source_period(source["source_date"], query_date)
    verified = verify_hash_fields(root, source)
    meta = read_json(resolved_input(root, source["registered_metadata"]))
    for field, expected in (("source_id", source["id"]), ("source_sha256", source["sha256"]),
                            ("source_date", source["source_date"]),
                            ("png_sha256", source["registered_png_sha256"]), ("crs", "EPSG:2326")):
        require(meta.get(field) == expected, f"Registration metadata {field} does not bind source")
    if "tif_sha256" in meta:
        tif = str(Path(source["registered_png"]).with_suffix(".tif"))
        verify_file(root, tif, meta["tif_sha256"])
        verified[tif] = meta["tif_sha256"]
    if "sheet" in meta:
        require(meta["sheet"] == source["sheet"], "Registration sheet mismatch")
    require(meta.get("date_precision") == "month", "Registration date precision mismatch")
    for field in ("width", "height"):
        require(isinstance(meta.get(field), int) and not isinstance(meta[field], bool)
                and meta[field] > 0, f"Invalid registered {field}")
    affine = meta.get("affine_pixel_edges")
    require(isinstance(affine, list) and len(affine) == 6, "Missing pixel-edge affine")
    a, b, _, d, e, _ = [finite(v, "affine coefficient") for v in affine]
    require(abs(a * e - b * d) > 1e-15, "Singular pixel-edge affine")
    with Image.open(resolved_input(root, source["registered_png"])) as image:
        require(image.size == (meta["width"], meta["height"]), "Registered image dimensions mismatch")
        image.verify()
    return meta, period, verified


def point_feature(observation, source, meta, period, root):
    for key in ("id", "source_id", "site_id", "surface_class", "description", "pixel_edge_col",
                "pixel_edge_row", "elevation_m", "source_symbol", "digitization_pick_tolerance_px",
                "evidence_crop", "evidence_crop_sha256", "evidence_crop_bounds_pixel_edges"):
        require(key in observation, f"Observation missing {key}")
    require(observation.get("accepted") is True, "Unaccepted observation cannot be exported")
    require(observation["surface_class"] in CLASSES, "Unresolved/unsupported surface class")
    require(observation["source_symbol"] == "spot_height_cross", "Ambiguous source symbol")
    for key in ("id", "site_id", "description"):
        require(isinstance(observation[key], str) and observation[key].strip(), f"Missing {key}")
    # Reject attempts to override datum/time/upper-bound semantics in a manual record.
    for key, expected in (("vertical_datum", "HKPD"), ("units", "metres"),
                          ("source_date", source["source_date"])):
        if key in observation:
            require(observation[key] == expected, f"Observation {key} conflicts with source")
    for key in ("historical_top_hkpd_m", "historical_upper_elevation_hkpd_m", "upper_bound_m", "physical_upper_bound_m"):
        require(observation.get(key) is None, "Point is not a physical obstacle upper bound")
    for key in ("presence_on_query_date", "query_date_presence"):
        if key in observation:
            require(observation[key] in {"unknown", "unresolved"}, "Query-date presence remains unknown")
    for key, value in observation.items():
        if key.endswith("_accuracy_m"):
            require(value is None, f"Unidentified observation accuracy must remain null: {key}")
    x = finite(observation["pixel_edge_col"], "pixel_edge_col")
    y = finite(observation["pixel_edge_row"], "pixel_edge_row")
    require(0 <= x <= meta["width"] and 0 <= y <= meta["height"], "Digitized point outside image")
    height = finite(observation["elevation_m"], "elevation_m")
    tolerance = finite(observation["digitization_pick_tolerance_px"], "digitization_pick_tolerance_px")
    require(tolerance >= 0, "Negative digitization tolerance")
    verified = verify_hash_fields(root, observation)
    with Image.open(resolved_input(root, observation["evidence_crop"])) as image:
        image.verify()
    if "evidence_crop_bounds_pixel_edges" in observation:
        bounds = observation["evidence_crop_bounds_pixel_edges"]
        require(isinstance(bounds, list) and len(bounds) == 4 and
                all(isinstance(v, int) and not isinstance(v, bool) for v in bounds), "Invalid crop bounds")
        left, top, right, bottom = bounds
        require(0 <= left < right <= meta["width"] and 0 <= top < bottom <= meta["height"],
                "Evidence crop outside registered image")
        require(left <= x < right and top <= y < bottom, "Accepted point outside its evidence crop")
        with Image.open(resolved_input(root, observation["evidence_crop"])) as crop_image, \
                Image.open(resolved_input(root, source["registered_png"])) as registered_image:
            expected_crop = registered_image.crop(bounds).convert("RGB")
            actual_crop = crop_image.convert("RGB")
            require(actual_crop.size == expected_crop.size and actual_crop.tobytes() == expected_crop.tobytes(),
                    "Evidence crop pixels do not match registered source")
    a, b, c, d, e, f = meta["affine_pixel_edges"]
    east, north = a*x + b*y + c, d*x + e*y + f
    lon, lat = TO_WGS84.transform(east, north, errcheck=True)
    require(all(math.isfinite(v) for v in (east, north, lon, lat)), "Invalid transformed coordinates")
    require(-180 <= lon <= 180 and -90 <= lat <= 90, "Invalid WGS84 coordinate")
    re, rn = TO_GRID.transform(lon, lat, errcheck=True)
    error = math.hypot(re - east, rn - north)
    require(error < 0.01, "Coordinate roundtrip exceeds 1 cm numerical check")
    # Only manual evidence fields enter output; arbitrary raw assertions cannot
    # survive next to the derived unknown-presence/accuracy/upper-bound semantics.
    manual_fields = {"id", "source_id", "site_id", "surface_class", "description", "pixel_edge_col",
                     "pixel_edge_row", "elevation_m", "source_symbol", "digitization_pick_tolerance_px",
                     "accepted", "evidence_crop", "evidence_crop_sha256", "evidence_crop_bounds_pixel_edges",
                     "physical_upper_bound_m", "survey_accuracy_m", "presence_on_query_date", "interpretation"}
    props = {key: copy.deepcopy(value) for key, value in observation.items() if key in manual_fields}
    props.update(period)
    props.update({"source_date": source["source_date"], "source_sheet": source["sheet"],
                  "source_archive": source["path"], "source_sha256": source["sha256"],
                  "registered_metadata": source["registered_metadata"],
                  "registered_metadata_sha256": source["registered_metadata_sha256"],
                  "registered_png": source["registered_png"],
                  "registered_png_sha256": source["registered_png_sha256"],
                  "vertical_datum": "HKPD", "units": "metres", "grid_crs": "EPSG:2326",
                  "easting_m": east, "northing_m": north, "geometry_crs": "EPSG:4326",
                  "geometry_has_vertical_coordinate": False,
                  "pixel_coordinate_convention": "pixel_edges_no_half_pixel_offset",
                  "horizontal_position_category": "derived_from_manually_digitized_registered_map",
                  "elevation_category": "manually_transcribed_map_spot_observation",
                  "source_elevation_status": "approximate_printed_spot_height_verify_before_use",
                  "ground_horizontal_accuracy_m": None, "vertical_accuracy_m": None,
                  "digitization_tolerance_is_ground_accuracy": False,
                  "digitization_grid_axis_tolerance_m": [tolerance*(abs(a)+abs(b)), tolerance*(abs(d)+abs(e))],
                  "coordinate_roundtrip_error_m": error, "historical_upper_elevation_hkpd_m": None,
                  "is_local_maximum": False, "is_full_structure_top": False,
                  "physical_upper_bound_known": False, "usable_for_historical_clearance": False,
                  "survey_date_is_edition_date": False,
                  "aviation_amsl_conversion_verified": False})
    return {"type": "Feature", "id": observation["id"],
            "geometry": {"type": "Point", "coordinates": [lon, lat]}, "properties": props}, verified


def unresolved_features(faces, input_sha, query_date, faces_path):
    require(faces.get("type") == "FeatureCollection", "Footprints must be FeatureCollection")
    features = []
    for face in faces["features"]:
        item = copy.deepcopy(face)
        require(item.get("type") == "Feature" and item.get("geometry", {}).get("type") in
                {"Polygon", "MultiPolygon"}, "Invalid historical footprint geometry type")
        props = item["properties"]
        for field in ("historical_top_hkpd_m", "historical_base_hkpd_m", "historical_upper_elevation_hkpd_m"):
            require(props.get(field) is None, f"Unreviewed historical footprint height: {field}")
        props.update({"obstacle_evidence_role": "unresolved_historical_mapped_footprint",
                      "historical_upper_elevation_hkpd_m": None, "query_date": query_date,
                      "query_date_presence": "unknown", "unknown_obstacle_mask": True,
                      "usable_for_historical_clearance": False, "physical_upper_bound_known": False,
                      "footprint_input": faces_path, "footprint_input_sha256": input_sha})
        features.append(item)
    west, south, east, north = CORE
    features.append({"type": "Feature", "id": "whole_approach_acquisition_core_unknown",
                     "geometry": {"type": "Polygon", "coordinates": [[[west, south], [east, south],
                         [east, north], [west, north], [west, south]]]},
                     "properties": {"obstacle_evidence_role": "approach_acquisition_core_unknown_coverage",
                         "bounds_wgs84": CORE, "is_navigation_corridor": False,
                         "coverage_status": "incomplete_unknown_not_clear",
                         "unknown_obstacle_mask": True, "query_date": query_date,
                         "query_date_presence": "unknown", "historical_upper_elevation_hkpd_m": None,
                         "physical_upper_bound_known": False, "usable_for_historical_clearance": False,
                         "note": "Acquisition work area only, not a certified approach corridor. Point readings and mapped faces do not remove any area from this unknown mask."}})
    return features


def build(project=PROJECT, observations_path=None, receipt_path=None,
          faces_path=FACES_PATH, expected_faces_sha256=FACES_SHA256):
    project = Path(project).resolve()
    observations_path = Path(observations_path or HERE / "observations.json")
    receipt_path = Path(receipt_path or observations_path.with_name("inspection_receipt.json"))
    raw = read_json(observations_path)
    receipt = read_json(receipt_path)
    require(receipt.get("observations_sha256") == sha256(observations_path),
            "Manual inspection receipt does not bind current observations")
    require(isinstance(receipt.get("reviewer"), str) and receipt["reviewer"].strip(),
            "Receipt missing reviewer identity")
    require(isinstance(receipt.get("reviewed_utc"), str), "Receipt missing reviewed_utc timestamp")
    try:
        reviewed_at = datetime.fromisoformat(receipt["reviewed_utc"])
    except ValueError as error:
        raise ValueError("Receipt invalid reviewed_utc timestamp") from error
    require(reviewed_at.tzinfo is not None and reviewed_at.utcoffset() == timedelta(0),
            "Receipt reviewed_utc must be explicitly UTC")
    require(isinstance(receipt.get("inspection_evidence"), dict) and receipt["inspection_evidence"],
            "Receipt requires nonempty inspection_evidence mapping")
    require(isinstance(receipt.get("accepted_count"), int) and not isinstance(receipt["accepted_count"], bool),
            "Receipt missing integer accepted_count")
    require(isinstance(receipt.get("accepted_reading_ids"), list) and
            all(isinstance(value, str) for value in receipt["accepted_reading_ids"]),
            "Receipt missing accepted_reading_ids list")
    inspection_inputs = {}
    for relative, digest in receipt["inspection_evidence"].items():
        inspected = verify_file(observations_path.parent, relative, digest)
        require(inspected.is_relative_to(project), "Inspection evidence escapes project")
        inspection_inputs[str(inspected.relative_to(project))] = digest
    require(raw.get("schema_version") == 1, "Unsupported observation schema")
    query_date = raw["query_date"]
    date.fromisoformat(query_date)
    require(query_date == "1993-11-04", "Frozen historical query date changed")
    sources, metadata, periods, inputs = {}, {}, {}, inspection_inputs
    for source in raw["sources"]:
        require(source["id"] not in sources, "Duplicate source id")
        meta, period, files = validate_source(project, source, query_date)
        sources[source["id"]], metadata[source["id"]], periods[source["id"]] = source, meta, period
        inputs.update(files)
    require(sources, "Empty accepted source catalogue")
    features, seen = [], set()
    for observation in raw["observations"]:
        require(observation["id"] not in seen, "Duplicate observation id")
        seen.add(observation["id"])
        sid = observation["source_id"]
        require(sid in sources, "Observation refers to unknown source")
        feature, files = point_feature(observation, sources[sid], metadata[sid], periods[sid], project)
        features.append(feature)
        inputs.update(files)
    require(features, "No accepted point observations")
    require(receipt["accepted_count"] == len(features), "Receipt accepted count mismatch")
    require(len(receipt["accepted_reading_ids"]) == len(features) and
            set(receipt["accepted_reading_ids"]) == seen, "Receipt accepted IDs mismatch")
    faces_file = verify_file(project, faces_path, expected_faces_sha256)
    faces = read_json(faces_file)
    unresolved = unresolved_features(faces, expected_faces_sha256, query_date, faces_path)
    inputs[faces_path] = expected_faces_sha256
    collection_meta = {"query_date": query_date, "vertical_coordinates": "properties_only_HKPD_metres",
                       "historical_clearance_ready": False, "sources": list(sources.values()),
                       "limitations": raw.get("limitations", [])}
    evidence = {"type": "FeatureCollection", **collection_meta, "features": features}
    unknown = {"type": "FeatureCollection", "query_date": query_date,
               "historical_clearance_ready": False, "features": unresolved}
    site_count = len({o["site_id"] for o in raw["observations"]})
    readiness = {"schema_version": 1, "query_date": query_date,
                 "historical_clearance_ready": False, "complete_obstacle_volumes": 0,
                 "physical_upper_bounds_available": 0, "accepted_source_observations": len(features),
                 "distinct_digitized_sites": site_count, "dated_source_count": len(sources),
                 "unresolved_historical_footprints": len(unresolved)-1,
                 "unknown_coverage_polygons": 1, "approach_acquisition_core_wgs84": CORE,
                 "query_date_presence_established": False,
                 "obstacle_surface_completeness": "incomplete",
                 "aviation_amsl_to_hkpd_relation": "unverified",
                 "required_remaining_evidence": ["Historical roof tops and rooftop equipment/antennas",
                     "Terrain upper surface between isolated spot observations",
                     "Exact-date structure presence and alteration history",
                     "Vertical and ground positional accuracy of historical measurements",
                     "Historical obstacle coverage throughout approach and beyond acquisition core as required",
                     "Aviation vertical reference reconciled to HKPD and whole-aircraft clearance"],
                 "limitations": raw.get("limitations", []),
                 "sources": list(sources.values()), "verified_input_files": inputs}
    verification = {"schema_version": 1, "status": "data_export_verified_not_clearance_ready",
                    "observations_sha256": sha256(observations_path),
                    "inspection_receipt_sha256": sha256(receipt_path),
                    "verified_input_files": inputs, "verified_input_file_count": len(inputs),
                    "observation_count": len(features), "unresolved_footprint_count": len(unresolved)-1,
                    "max_coordinate_roundtrip_error_m": max(f["properties"]["coordinate_roundtrip_error_m"] for f in features),
                    "manual_acceptance_binding": "whole observations file SHA256 matches separate inspection receipt",
                    "source_archive_png_metadata_crop_hashes": "passed",
                    "source_metadata_identity_links": "passed",
                    "date_datum_and_unknown_surface_semantics": "passed",
                    "historical_clearance_ready": False, "complete_obstacle_volumes": 0,
                    "tests": "Run test_obstacles.py separately; build success is not a test-suite claim"}
    return {"obstacle_evidence.geojson": evidence, "unresolved_footprints.geojson": unknown,
            "readiness.json": readiness, "verification.json": verification}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path, default=HERE / "observations.json")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    outputs = build(observations_path=args.observations, receipt_path=args.receipt)
    # Validate all inputs before replacing any generated file.
    encoded = {name: json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
               for name, value in outputs.items()}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in encoded.items():
        destination = args.output_dir / name
        temporary = destination.with_name(destination.name + ".tmp")
        temporary.write_text(content)
        temporary.replace(destination)
    print(json.dumps({"outputs": list(outputs), "observations": outputs["readiness.json"]["accepted_source_observations"],
                      "historical_clearance_ready": False}))


if __name__ == "__main__":
    main()
