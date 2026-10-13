"""Reproduce map inspection rasters from pinned original ZIPs; no original writes."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import rasterio
from rasterio.transform import Affine
from PIL import Image

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MATCHING = HERE.parent / "block_matching"
sys.path.insert(0, str(MATCHING))
import register_sheets


def main():
    review = HERE / "review"
    review.mkdir(exist_ok=True)
    register_sheets.OUT = review
    inventory = json.loads((MATCHING / "registered/sheet_registration_inventory.json").read_text())
    for sid in ("1980_1990:1292", "1980_1990:1293"):
        record = next(r for r in inventory["records"] if r["source_id"] == sid)
        archive = PROJECT / record["source_archive"]
        if hashlib.sha256(archive.read_bytes()).hexdigest() != record["source_sha256"]:
            raise ValueError("Source changed: " + sid)
        register_sheets.render(record, res=.25)
        suffix, date = sid.split(":")[1], record["edition_date"][:7]
        with rasterio.open("/vsizip/" + str(archive) + "/" + record["tiff_member"]) as dataset:
            array = dataset.read(1)
            try:
                palette = dataset.colormap(1)
                lut = np.array([palette.get(i,(i,i,i,255))[:3] for i in range(256)], dtype="uint8")
                array = lut[array]
            except ValueError:
                pass
            original = Image.fromarray(array)
            original.crop((0,original.height-1300,original.width,original.height)).resize(
                (3000,round(1300*3000/original.width))).save(review / f"legend_{suffix}.png")
            transform = Affine(*record["affine_pixel_edges"])
            upper_left = (~transform)*(836750+900*.25,822200-750*.25)
            lower_right = (~transform)*(836750+1700*.25,822200-1800*.25)
            original.crop(tuple(map(round,(*upper_left,*lower_right)))).save(review / f"raw_hill_{suffix}.png")
            if suffix == "1292":
                original.thumbnail((2400,2400))
                original.save(review / "hill_full_sheet.png")
        registered = Image.open(review / f"11-NW-10D_{date}_core.png")
        registered.crop((900,750,1700,1800)).save(review / f"hill_detail_{date}.png")
    print("Prepared two historical source sheets; inspection receipt is not automatically renewed.")


if __name__ == "__main__":
    main()
