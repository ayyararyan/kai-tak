# The Kai Tak Visual Atlas

[Home](../README.md) · [Paper](../papers/README.md) · [Historical archive](../archive/README.md)

Historical photographs, mapped evidence and three-dimensional surfaces, presented
with their dates, sources and uncertainty intact.

<!-- atlas-current:start -->
**Published edition: v1.** 12 principal 4K plates, 17 Blender views.

[Read the atlas PDF](v1/renders/print/Kai-Tak-Visual-Atlas-A4.pdf) · [Plate and methods guide](v1/README.md) · [Download editable scenes](https://github.com/ayyararyan/kai-tak/releases/tag/visual-atlas-v1)
<!-- atlas-current:end -->

## Selected plates from edition v1

| Begin with | What it shows |
|---|---|
| [November 1993, in fragments](v1/renders/annotated/08-november-1993.png) | Conditional stereo-derived surface; original holes retained |
| [From photograph to spatial evidence](v1/renders/annotated/11-evidence-chain.png) | Observations, reconstruction and interpretation |
| [The airport landscape, then and now](v1/renders/annotated/10-then-and-now.png) | Separately dated historical and modern evidence |
| [Kowloon, October 1989](v1/renders/annotated/07-kowloon-1989.png) | Historical map faces without invented building heights |

<!-- atlas-gallery:start -->
## Open the gallery

GitHub displays the [gallery HTML source](v1/gallery/index.html); it does not host
this directory as a live exhibition. After cloning, open that file in a browser,
or serve the checkout locally:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
# Open http://127.0.0.1:8000/visual-atlas/v1/gallery/index.html
```
<!-- atlas-gallery:end -->

The gallery offers evidence-led and explicitly contextual variants, captions,
provenance and full-resolution downloads. No website deployment is implied.
The original v1 delivery did not include browser acceptance. A later [local Chromium
check](../docs/migration/browser-acceptance.json) verified v1 desktop/mobile interaction;
this is not a deployed-site check.

## Recover and reproduce edition v1

The edition guide documents [scene restoration and rendering](v1/README.md#reproduce).
The [scene manifest](v1/metadata/scene_bundle.json) binds seventeen packed Blender
files and ten prepared assets to the separate release ZIP. Original research inputs
are pinned in the [input manifest](v1/metadata/input_manifest.json).

Use a disposable checkout when rebuilding: preparation regenerates machine-local
job paths, and verification writes QA records. Preserve the released cameras,
source hashes and images. See the [safe reproduction guide](../docs/REPRODUCIBILITY.md).

Relative stereo heights are not HKPD elevations; modern buildings do not fill gaps
in 1993 geometry. [Source rights](v1/metadata/SOURCE_AUDIT.md) ·
[Scientific and visual limitations](v1/qa/REPORT.md).
