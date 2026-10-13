"""Evidence-integrity and scientific-semantic regression tests using isolated files."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

import build_obstacles as builder


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "archive.zip").write_bytes(b"synthetic original source fixture")
        Image.new("RGB", (100, 80), "white").save(self.root / "registered.png")
        Image.new("RGB", (20, 20), "white").save(self.root / "crop.png")
        Image.new("RGB", (20, 20), "white").save(self.root / "datum.png")
        self.meta = {"source_id": "fixture:1", "source_sha256": builder.sha256(self.root / "archive.zip"),
                     "source_date": "1989-10", "date_precision": "month", "crs": "EPSG:2326",
                     "png_sha256": builder.sha256(self.root / "registered.png"), "width": 100, "height": 80,
                     "affine_pixel_edges": [0.25, 0, 837500, 0, -0.25, 821600]}
        self.write("registered.json", self.meta)
        self.source = {"id": "fixture:1", "path": "archive.zip", "sha256": self.meta["source_sha256"],
                       "source_date": "1989-10", "sheet": "11-NE-11A", "vertical_datum": "HKPD",
                       "units": "metres", "registered_png": "registered.png",
                       "registered_png_sha256": self.meta["png_sha256"],
                       "registered_metadata": "registered.json",
                       "registered_metadata_sha256": builder.sha256(self.root / "registered.json"),
                       "datum_evidence_image": "datum.png", "datum_evidence_sha256": builder.sha256(self.root / "datum.png"),
                       "datum_evidence": "Printed legend: heights in metres above Principal Datum; approximate spot heights."}
        self.observation = {"id": "spot-1", "source_id": "fixture:1", "site_id": "site-1",
                            "surface_class": "terrain_spot", "description": "synthetic point",
                            "pixel_edge_col": 10, "pixel_edge_row": 20, "elevation_m": 17.3,
                            "source_symbol": "spot_height_cross", "digitization_pick_tolerance_px": 2,
                            "accepted": True, "evidence_crop": "crop.png",
                            "evidence_crop_bounds_pixel_edges": [0, 10, 20, 30],
                            "evidence_crop_sha256": builder.sha256(self.root / "crop.png")}
        self.raw = {"schema_version": 1, "query_date": "1993-11-04", "sources": [self.source],
                    "observations": [self.observation], "limitations": ["Fixture only"]}
        self.face = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [
            [[114.19, 22.33], [114.191, 22.33], [114.191, 22.331], [114.19, 22.33]]]},
            "properties": {"id": "face-1", "historical_top_hkpd_m": None,
                           "historical_base_hkpd_m": None, "original_property": "retained",
                           "modern_correspondences": [{"modern_top_hkpd_m": 48.2, "height_transfer_to_historical": False}]}}
        self.write("faces.json", {"type": "FeatureCollection", "features": [self.face]})
        self.face_sha = builder.sha256(self.root / "faces.json")
        self.accept()

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value))

    def accept(self):
        self.write("observations.json", self.raw)
        self.write("inspection_receipt.json", {"observations_sha256": builder.sha256(self.root / "observations.json"),
                                               "reviewer": "synthetic fixture reviewer",
                                               "reviewed_utc": "2026-10-13T14:00:00+00:00",
                                               "accepted_count": len(self.raw["observations"]),
                                               "accepted_reading_ids": [o["id"] for o in self.raw["observations"]],
                                               "inspection_evidence": {"datum.png": builder.sha256(self.root / "datum.png")},
                                               "acceptance_statement": "Synthetic fixture acceptance"})

    def run_build(self):
        return builder.build(self.root, self.root / "observations.json", self.root / "inspection_receipt.json",
                             "faces.json", self.face_sha)

    def test_deterministic_build_keeps_no_clearance_claim(self):
        first = self.run_build()
        self.assertEqual(first, self.run_build())
        readiness = first["readiness.json"]
        self.assertFalse(readiness["historical_clearance_ready"])
        self.assertEqual(readiness["complete_obstacle_volumes"], 0)
        self.assertEqual(readiness["physical_upper_bounds_available"], 0)
        self.assertEqual(readiness["aviation_amsl_to_hkpd_relation"], "unverified")
        point = first["obstacle_evidence.geojson"]["features"][0]
        self.assertEqual(len(point["geometry"]["coordinates"]), 2)
        p = point["properties"]
        self.assertEqual(p["elevation_m"], 17.3)
        self.assertEqual(p["query_date_presence"], "unknown")
        self.assertIsNone(p["historical_upper_elevation_hkpd_m"])
        self.assertIsNone(p["vertical_accuracy_m"])

    def test_pixel_edge_affine_not_pixel_centre(self):
        p = self.run_build()["obstacle_evidence.geojson"]["features"][0]["properties"]
        self.assertEqual(p["easting_m"], 837502.5)
        self.assertEqual(p["northing_m"], 821595)
        self.assertEqual(p["digitization_grid_axis_tolerance_m"], [0.5, 0.5])
        self.assertLess(p["coordinate_roundtrip_error_m"], 0.01)
        self.assertFalse(p["digitization_tolerance_is_ground_accuracy"])

    def test_rotated_affine(self):
        self.meta["affine_pixel_edges"] = [0.25, 0.02, 837500, -0.01, -0.25, 821600]
        self.write("registered.json", self.meta)
        self.source["registered_metadata_sha256"] = builder.sha256(self.root / "registered.json")
        self.accept()
        p = self.run_build()["obstacle_evidence.geojson"]["features"][0]["properties"]
        self.assertAlmostEqual(p["easting_m"], 837502.9)
        self.assertAlmostEqual(p["northing_m"], 821594.9)

    def test_stale_input_files_fail_closed(self):
        for filename in ("archive.zip", "registered.png", "registered.json", "crop.png", "datum.png", "faces.json"):
            with self.subTest(filename=filename):
                path = self.root / filename
                original = path.read_bytes()
                path.write_bytes(original + b" ")
                with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
                    self.run_build()
                path.write_bytes(original)

    def test_changed_manual_values_cannot_inherit_acceptance(self):
        for field, replacement in (("elevation_m", 200), ("pixel_edge_col", 30),
                                   ("surface_class", "elevated_platform_spot")):
            with self.subTest(field=field):
                raw = copy.deepcopy(self.raw)
                raw["observations"][0][field] = replacement
                self.write("observations.json", raw)
                with self.assertRaisesRegex(ValueError, "inspection receipt"):
                    self.run_build()
        self.accept()

    def test_changed_source_metadata_cannot_inherit_acceptance(self):
        for field, value in (("source_date", "1994-07"), ("id", "another:1"), ("vertical_datum", "AMSL")):
            with self.subTest(field=field):
                raw = copy.deepcopy(self.raw)
                raw["sources"][0][field] = value
                self.write("observations.json", raw)
                with self.assertRaisesRegex(ValueError, "inspection receipt"):
                    self.run_build()

    def test_metadata_identity_links_even_when_hash_is_refreshed(self):
        for field, value in (("source_date", "1994-07"), ("source_id", "wrong"),
                             ("source_sha256", "0"*64), ("png_sha256", "0"*64), ("crs", "EPSG:4326")):
            with self.subTest(field=field):
                original = self.meta[field]
                self.meta[field] = value
                self.write("registered.json", self.meta)
                self.source["registered_metadata_sha256"] = builder.sha256(self.root / "registered.json")
                self.accept()
                with self.assertRaisesRegex(ValueError, "metadata"):
                    self.run_build()
                self.meta[field] = original

    def test_date_precision_and_query_month(self):
        cases = [("1993-10", "before_query"), ("1993-11", "query_month_ambiguous"),
                 ("1993-12", "after_query")]
        for month, relation in cases:
            p = builder.source_period(month, "1993-11-04")
            self.assertEqual(p["source_period_relative_to_query"], relation)
            self.assertEqual(p["query_date_presence"], "unknown")
            self.assertIsNone(p["individual_object_survey_date"])
        for month in ("1993-11-01", "1993-13", "1993-00", "bad"):
            with self.assertRaises(ValueError):
                builder.source_period(month, "1993-11-04")

    def test_bracketing_editions_do_not_establish_presence(self):
        second = copy.deepcopy(self.source)
        second.update(id="fixture:2", source_date="1994-07", registered_metadata="second.json")
        second_meta = {**self.meta, "source_id": second["id"], "source_date": second["source_date"]}
        self.write("second.json", second_meta)
        second["registered_metadata_sha256"] = builder.sha256(self.root / "second.json")
        self.raw["sources"].append(second)
        self.raw["observations"].append({**self.observation, "id": "spot-2", "source_id": second["id"]})
        self.accept()
        outputs = self.run_build()
        self.assertEqual(outputs["readiness.json"]["distinct_digitized_sites"], 1)
        for feature in outputs["obstacle_evidence.geojson"]["features"]:
            self.assertEqual(feature["properties"]["query_date_presence"], "unknown")

    def test_invalid_nonfinite_and_unaccepted_points(self):
        cases = [("elevation_m", float("nan")), ("elevation_m", float("inf")), ("elevation_m", True),
                 ("pixel_edge_col", -1), ("pixel_edge_row", 81), ("pixel_edge_col", "10"),
                 ("digitization_pick_tolerance_px", -1), ("accepted", False),
                 ("surface_class", "storey_count"), ("source_symbol", "address_number"),
                 ("historical_upper_elevation_hkpd_m", 20), ("source_date", "1994-07")]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                previous = self.observation.get(field)
                self.observation[field] = value
                self.accept()
                with self.assertRaises(ValueError):
                    self.run_build()
                if previous is None:
                    del self.observation[field]
                else:
                    self.observation[field] = previous

    def test_unknown_footprints_preserve_original_geometry_and_properties(self):
        features = self.run_build()["unresolved_footprints.geojson"]["features"]
        self.assertEqual(len(features), 2)
        self.assertEqual(features[0]["geometry"], self.face["geometry"])
        for key, value in self.face["properties"].items():
            self.assertEqual(features[0]["properties"][key], value)
        for feature in features:
            self.assertIsNone(feature["properties"]["historical_upper_elevation_hkpd_m"])
            self.assertTrue(feature["properties"]["unknown_obstacle_mask"])
        mask = features[1]
        self.assertFalse(mask["properties"]["is_navigation_corridor"])
        self.assertEqual(mask["geometry"]["coordinates"][0],
                         [[114.16, 22.30], [114.22, 22.30], [114.22, 22.35], [114.16, 22.35], [114.16, 22.30]])

    def test_new_historical_footprint_height_is_not_silently_promoted(self):
        self.face["properties"]["historical_top_hkpd_m"] = 50
        self.write("faces.json", {"type": "FeatureCollection", "features": [self.face]})
        self.face_sha = builder.sha256(self.root / "faces.json")
        with self.assertRaisesRegex(ValueError, "footprint height"):
            self.run_build()

    def test_unsupported_datum_or_units_rejected(self):
        for key, value in (("vertical_datum", "AMSL"), ("vertical_datum", None), ("units", "feet")):
            original = self.source[key]
            self.source[key] = value
            self.accept()
            with self.assertRaises(ValueError):
                self.run_build()
            self.source[key] = original

    def test_all_explicit_hashes_checked(self):
        self.source["additional_evidence_sha256"] = "0"*64
        self.accept()
        with self.assertRaisesRegex(ValueError, "no paired file"):
            self.run_build()

    def test_missing_or_escaped_source_rejected(self):
        for path in ("missing.zip", "../outside.zip", "/tmp/outside.zip"):
            self.source["path"] = path
            self.accept()
            with self.assertRaises(ValueError):
                self.run_build()

    def test_duplicate_observations_and_empty_evidence_rejected(self):
        self.raw["observations"].append(copy.deepcopy(self.observation))
        self.accept()
        with self.assertRaisesRegex(ValueError, "Duplicate observation"):
            self.run_build()
        self.raw["observations"] = []
        self.accept()
        with self.assertRaisesRegex(ValueError, "No accepted"):
            self.run_build()

    def test_inspection_collage_hash_and_reading_ids_are_bound(self):
        receipt = builder.read_json(self.root / "inspection_receipt.json")
        receipt.update(accepted_count=1, accepted_reading_ids=["spot-1"],
                       inspection_evidence={"datum.png": builder.sha256(self.root / "datum.png")})
        self.write("inspection_receipt.json", receipt)
        self.run_build()
        receipt["inspection_evidence"]["datum.png"] = "0"*64
        self.write("inspection_receipt.json", receipt)
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            self.run_build()
        receipt["inspection_evidence"]["datum.png"] = builder.sha256(self.root / "datum.png")
        receipt["accepted_reading_ids"] = ["wrong"]
        self.write("inspection_receipt.json", receipt)
        with self.assertRaisesRegex(ValueError, "accepted IDs"):
            self.run_build()

    def test_crop_content_matches_registered_source_and_contains_point(self):
        self.observation["evidence_crop_bounds_pixel_edges"] = [0, 10, 20, 30]
        Image.new("RGB", (20, 20), "grey").save(self.root / "crop.png")
        self.observation["evidence_crop_sha256"] = builder.sha256(self.root / "crop.png")
        self.accept()
        with self.assertRaisesRegex(ValueError, "crop pixels"):
            self.run_build()
        Image.new("RGB", (20, 20), "white").save(self.root / "crop.png")
        self.observation["evidence_crop_sha256"] = builder.sha256(self.root / "crop.png")
        self.accept()
        self.run_build()
        self.observation["pixel_edge_col"] = 21
        self.accept()
        with self.assertRaisesRegex(ValueError, "outside its evidence crop"):
            self.run_build()

    def test_registered_tiff_pin_when_present(self):
        Image.new("RGB", (100, 80), "white").save(self.root / "registered.tif")
        self.meta["tif_sha256"] = builder.sha256(self.root / "registered.tif")
        self.write("registered.json", self.meta)
        self.source["registered_metadata_sha256"] = builder.sha256(self.root / "registered.json")
        self.accept()
        self.run_build()
        (self.root / "registered.tif").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            self.run_build()

    def test_singular_affine_and_image_dimensions_rejected(self):
        self.meta["affine_pixel_edges"] = [0, 0, 837500, 0, 0, 821600]
        self.write("registered.json", self.meta)
        self.source["registered_metadata_sha256"] = builder.sha256(self.root / "registered.json")
        self.accept()
        with self.assertRaisesRegex(ValueError, "Singular"):
            self.run_build()
        self.meta["affine_pixel_edges"] = [0.25, 0, 837500, 0, -0.25, 821600]
        self.meta["width"] = 99
        self.write("registered.json", self.meta)
        self.source["registered_metadata_sha256"] = builder.sha256(self.root / "registered.json")
        self.accept()
        with self.assertRaisesRegex(ValueError, "dimensions mismatch"):
            self.run_build()

    def test_missing_crop_bounds_cannot_bypass_source_pixel_check(self):
        del self.observation["evidence_crop_bounds_pixel_edges"]
        self.accept()
        with self.assertRaisesRegex(ValueError, "missing evidence_crop_bounds_pixel_edges"):
            self.run_build()

    def test_datum_evidence_fields_are_mandatory(self):
        for field in ("datum_evidence_image", "datum_evidence_sha256", "datum_evidence"):
            with self.subTest(field=field):
                value = self.source.pop(field)
                self.accept()
                with self.assertRaisesRegex(ValueError, "datum evidence"):
                    self.run_build()
                self.source[field] = value
        for text in (None, "", "   ", "checked", "I checked this document and it seems acceptable."):
            with self.subTest(text=text):
                self.source["datum_evidence"] = text
                self.accept()
                with self.assertRaisesRegex(ValueError, "datum evidence text"):
                    self.run_build()

    def test_datum_evidence_path_alias_is_hash_bound(self):
        self.source["datum_evidence_path"] = self.source.pop("datum_evidence_image")
        self.accept()
        self.run_build()
        self.source["datum_evidence_sha256"] = "0"*64
        self.accept()
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            self.run_build()

    def test_receipt_required_fields_cannot_be_omitted(self):
        original = builder.read_json(self.root / "inspection_receipt.json")
        for field in ("inspection_evidence", "accepted_count", "accepted_reading_ids", "reviewer", "reviewed_utc"):
            with self.subTest(field=field):
                receipt = copy.deepcopy(original)
                del receipt[field]
                self.write("inspection_receipt.json", receipt)
                with self.assertRaisesRegex(ValueError, "Receipt"):
                    self.run_build()
        for field, value in (("inspection_evidence", {}), ("accepted_count", 0),
                             ("accepted_count", True), ("accepted_reading_ids", []),
                             ("accepted_reading_ids", ["spot-1", "spot-1"]), ("accepted_reading_ids", "spot-1"),
                             ("reviewer", "  "), ("reviewer", None), ("reviewed_utc", "bad"),
                             ("reviewed_utc", "2026-10-13"), ("reviewed_utc", "2026-10-13T10:00:00+05:30")):
            with self.subTest(field=field, value=value):
                receipt = copy.deepcopy(original)
                receipt[field] = value
                self.write("inspection_receipt.json", receipt)
                with self.assertRaisesRegex(ValueError, "Receipt"):
                    self.run_build()

    def test_alternate_footprint_path_is_correctly_recorded(self):
        target = self.root / "alternate"
        target.mkdir()
        (target / "faces.json").write_bytes((self.root / "faces.json").read_bytes())
        result = builder.build(self.root, self.root / "observations.json", self.root / "inspection_receipt.json",
                               "alternate/faces.json", self.face_sha)
        properties = result["unresolved_footprints.geojson"]["features"][0]["properties"]
        self.assertEqual(properties["footprint_input"], "alternate/faces.json")
        self.assertEqual(properties["footprint_input_sha256"], self.face_sha)
        self.assertIn("alternate/faces.json", result["verification.json"]["verified_input_files"])

    def test_contradictory_observation_semantics_rejected(self):
        for field, value in (("presence_on_query_date", "established"), ("query_date_presence", "present"),
                             ("survey_accuracy_m", 0.01), ("map_ground_accuracy_m", 0.01),
                             ("map_vertical_accuracy_m", 0.01), ("physical_upper_bound_m", 200)):
            with self.subTest(field=field):
                self.observation[field] = value
                self.accept()
                with self.assertRaises(ValueError):
                    self.run_build()
                del self.observation[field]
        self.observation["unreviewed_claim"] = "historical clearance established"
        self.accept()
        properties = self.run_build()["obstacle_evidence.geojson"]["features"][0]["properties"]
        self.assertNotIn("unreviewed_claim", properties)

    def test_unidentified_source_accuracy_cannot_be_asserted(self):
        self.source["map_ground_accuracy_m"] = 0.01
        self.accept()
        with self.assertRaisesRegex(ValueError, "source accuracy"):
            self.run_build()


if __name__ == "__main__":
    unittest.main()
