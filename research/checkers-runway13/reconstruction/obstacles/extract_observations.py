"""Materialize manually read map spots; no OCR acceptance or height interpolation.

Run before review. This does NOT create the independent inspection receipt.
Positions are pixel-edge coordinates in the 0.25m registered source image.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(PROJECT))


# Read from both the original full-resolution source crop and registered raster.
# Values denote the surface at the cross, never the highest obstacle at the site.
# x/y below are relative to review/hill_detail_* crop (900,750,1700,1800).
READINGS = [
    ("hill_latrine_surround", 444, 101, 83.8, "terrain_spot", "Paved surround south of hill latrine; not its roof"),
    ("reservoir_garden_north", 387, 511, 91.9, "elevated_platform_spot", "Northern interior of Lok Fu Service Reservoir Rest Garden, reservoir under"),
    ("reservoir_garden_south", 282, 869, 92.0, "elevated_platform_spot", "Southern interior of reservoir rest garden"),
    ("hill_east_upper_path", 536, 780, 93.8, "terrain_spot", "Upper path immediately east of rest garden"),
    ("hill_east_lower_path", 613, 805, 89.2, "terrain_spot", "Diagonal path east of rest garden"),
    ("hill_east_path_junction", 549, 854, 91.1, "terrain_spot", "Southeastern garden-side path junction"),
    ("hill_east_round_path", 714, 718, 85.7, "terrain_spot", "Rounded eastern path area"),
    ("radar_site_north_ground", 387, 902, 93.3, "terrain_spot", "Open surface north of Radar Station symbol; not radar top"),
    ("radar_site_west_ground", 243, 929, 92.9, "terrain_spot", "Open surface southeast of western Radar Station structure; not its roof"),
    ("radar_site_east_ground", 491, 931, 90.8, "terrain_spot", "Open surface east of square structure in Radar Station site; not its roof"),
    ("radar_site_southeast_ground", 524, 955, 89.2, "terrain_spot", "Southeastern open surface of Radar Station site"),
    ("radar_site_south_ground", 438, 971, 89.6, "terrain_spot", "Southern open surface of Radar Station site"),
]


def main():
    inventory = json.loads((PROJECT / "reconstruction/block_matching/registered/sheet_registration_inventory.json").read_text())
    sources, observations = [], []
    review = HERE / "review"
    for sid, date in [("1980_1990:1292", "1989-11"), ("1980_1990:1293", "1995-06")]:
        original = next(row for row in inventory["records"] if row["source_id"] == sid)
        archive = PROJECT / original["source_archive"]
        if sha(archive) != original["source_sha256"]:
            raise ValueError("Original source changed")
        stem = "11-NW-10D_" + date + "_core"
        png, meta = review / (stem + ".png"), review / (stem + ".json")
        legend = review / ("legend_" + sid.split(":")[1] + ".png")
        source = dict(id=sid, path=rel(archive), sha256=sha(archive), source_date=date,
                      sheet="11-NW-10D", registered_png=rel(png), registered_png_sha256=sha(png),
                      registered_metadata=rel(meta), registered_metadata_sha256=sha(meta),
                      vertical_datum="HKPD", units="metres", datum_evidence_image=rel(legend),
                      datum_evidence_image_sha256=sha(legend),
                      datum_evidence="Original printed HEIGHTS legend: heights in metres above Principal Datum; spot heights are approximate, located by crosses, and should be verified before use.",
                      map_ground_accuracy_m=None, map_vertical_accuracy_m=None,
                      note="Map edition, not per-feature survey date. A repeated value can be carried forward cartography.")
        sources.append(source)
        im = Image.open(png).convert("RGB")
        contact = Image.new("RGB", (960, 4 * 245), "white")
        d = ImageDraw.Draw(contact)
        for i, (site, x, y, z, kind, desc) in enumerate(READINGS):
            px, py = 900+x, 750+y
            # 120px context includes the printed number and surface, without altering it.
            bounds = (px-60, py-60, px+60, py+60)
            crop = im.crop(bounds)
            cp = review / f"{sid.split(':')[1]}_{site}.png"
            crop.save(cp)
            oid = sid.split(":")[1] + "_" + site
            row = dict(id=oid, source_id=sid, site_id=site, surface_class=kind,
                       description=desc, pixel_edge_col=px, pixel_edge_row=py,
                       elevation_m=z, source_symbol="spot_height_cross",
                       digitization_pick_tolerance_px=2, accepted=True,
                       evidence_crop=rel(cp), evidence_crop_sha256=sha(cp),
                       evidence_crop_bounds_pixel_edges=list(bounds),
                       physical_upper_bound_m=None, survey_accuracy_m=None,
                       presence_on_query_date="unresolved",
                       interpretation="Source-map surface observation, not full obstacle height or maximum; digitization tolerance is not ground or vertical accuracy.")
            observations.append(row)
            bx, by = i % 3 * 320, i // 3 * 245
            enlarged = crop.resize((210,210))
            contact.paste(enlarged, (bx,by+30))
            d.text((bx,by), f"{i+1}. {z} m | {site}", fill="black")
            # Red ring marks the selected cross without covering it.
            d.ellipse((bx+99,by+129,bx+111,by+141), outline="red",width=1)
        contact.save(review / f"spot_inspection_{sid.split(':')[1]}.png")
    obj = dict(schema_version=1,query_date="1993-11-04",sources=sources,observations=observations,
               limitations=["Only 12 mapped sites on one historical hill sheet; no complete approach surface.",
                            "1989 and 1995 are bracketing editions, not two independent surveys or proof of exact 1993 presence.",
                            "Point spots do not bound intervening terrain, vegetation, roofs, radar equipment or poles.",
                            "Map printed legend declares approximate heights that should be verified before use.",
                            "No transformation from HKPD to aviation AMSL has been accepted.",
                            "No map spot is used as a stereo vertical checkpoint without a same-surface image correspondence."])
    (HERE / "observations.json").write_text(json.dumps(obj,indent=2)+"\n")
    print(f"Prepared {len(observations)} readings; manual inspection receipt still required.")


if __name__ == "__main__":
    main()
