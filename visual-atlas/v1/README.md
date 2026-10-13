# Checkers with Runway 13 · Visual atlas v1

**Prepared for Aryan Ayyar's author review. GitHub publication explicitly authorized on 2026-10-13.**

[Open the exhibition gallery](gallery/index.html) · [A4 atlas PDF](renders/print/Kai-Tak-Visual-Atlas-A4.pdf) · [Contact sheet](qa/contact-sheet.jpg) · [Source and rights audit](metadata/SOURCE_AUDIT.md) · [QA and limitations](qa/REPORT.md)

## What this atlas delivers

Twelve 3840 × 2160 plates, each with annotated and unannotated PNGs, web previews and A4 print layouts. Seventeen Blender views supply source-linked 3D surfaces, modern building masses, historical map boards and separate modern terrain context. Editable `.blend` files and full camera records accompany every base render. Selected square/vertical crops and a transparent evidence legend are included.

The gallery's **Evidence-led** and **With disclosed context** controls change the hill, alignment and signature plates. Context includes explicitly later hill terrain, schematic magnetic-course arrows and a separately framed airport map. Historical source geometry is unchanged. Other plates retain their source-bound views. An illustrative camera is not a documented aircraft pose.

## Recommended white-paper selection

1. **08 — November 1993, in fragments:** strongest source-derived 3D hero. [Warm light](renders/annotated/08-november-1993.png) · [Matched architectural daylight](renders/annotated/08-daylight.png).
2. **11 — From photograph to spatial evidence:** strongest explanation of the method and its traceability. [Plate](renders/annotated/11-evidence-chain.png).
3. **10 — The airport landscape, then and now:** matched-camera airport-area comparison. [Plate](renders/annotated/10-then-and-now.png).
4. **07 — Kowloon, October 1989:** legible historical sheet and accepted height-unknown faces. [Plate](renders/annotated/07-kowloon-1989.png).
5. **06 — Forty-seven degrees:** accessible magnetic-course diagram, explicitly separate from grid-oriented geography. [Plate](renders/annotated/06-final-alignment.png).
6. **03 — The city beneath the aircraft:** closer source-surface view with a 100 m horizontal scale reference. [Plate](renders/annotated/03-city-beneath.png).

The full storyboard, interpretive objectives, alternatives and limitations are in [storyboard.json](storyboard/storyboard.json). The signature synthesis (12) is available, but 08 is the stronger image when the paper needs to emphasize actual recovered geometry.

## Scientific limits that stay visible

- The 1993 surface contains **155,891 vertices and 225,371 original triangles**, not solid historical buildings. Unsupported holes are retained. The closer core contains **52,230 original triangles**, selected without inventing new faces.
- Stereo heights are **relative to a fitted park/road plane**, not HKPD. Nominal camera calibration and control extrapolation remain limitations; only 3,780 of 171,307 dense points are inside the local map-control hull.
- Forty-five reviewed historical map faces retain **unknown heights**. Three map editions have distinct evidence, not artificially equal city models.
- The broad map mosaic spans **1986–1993**, including July 1986 sheet 11-NE-16D. It is not a single-date survey. Mapped runway registration still has unresolved threshold discrepancies. No complete historical coastline or terrain was fabricated.
- The modern airport view uses **3,546 valid polygon components** from the 21 September 2026 inventory, with approximate HKPD base/top elevations. **167 records** with invalid geometry or missing/inconsistent heights are omitted explicitly. Modern buildings are never transferred into 1993.
- The hill context uses the existing **2014–2015 photography-derived DTM**. It is separately shown, never called a 1993 terrain survey. The painted checkerboard's exact surveyed face/position is unresolved.
- The 088°/135° arrows are **magnetic directions**, not a plotted historical flight path. The mapped runway-edge bearing is about 134.02° **grid**. A virtual camera carries no flown-trajectory claim.
- The A36143 date-reading discrepancy remains documented: an earlier ambiguous reading was corrected to **2 November 1993** after original-image/catalogue inspection.

## Organization

| Folder | Contents |
|---|---|
| `storyboard/` | Twelve-subject plan, narrative objectives, epochs and evidence-limited alternatives |
| `scenes/` | Seventeen editable packed Blender scenes; source-pinned JSON render jobs |
| `scripts/` | Preparation, Blender rendering, composition, gallery and acceptance checks |
| `assets/` | Derived display textures, hole-safe modern roofs, geography and separate hill context |
| `renders/master/` | Base 4K renders + camera/source records; unannotated finished plates |
| `renders/annotated/` | Twelve finished plates, evidence variants, daylight variant and transparent legend |
| `renders/web/` | WebP previews and caption/provenance sidecars |
| `renders/print/` | A4 300-dpi layouts and the atlas PDF |
| `renders/crops/` | Selected native-resolution-derived square and vertical crops |
| `comparisons/` | Matched-date, then/now and source-chain plates |
| `metadata/` | Input hashes, rights/source register, restoration receipt and dependency versions |
| `qa/` | Acceptance evidence, visual inspection, review decisions and regeneration results |
| `gallery/` | Static HTML exhibition with no CDN/runtime dependency |

Large original datasets remain at their existing repository/archive paths. `assets/` contains necessary derived preparation, not another copy of the original archive.

## Reproduce

From the **repository root**, restore the original archived data through the existing helper. It verifies archive/member hashes and refuses conflicting local files:

```sh
python3 scripts/fetch_data.py
python3 -m venv visual-atlas/v1/.venv
visual-atlas/v1/.venv/bin/pip install -r visual-atlas/v1/metadata/requirements.txt
```

Install **Blender 4.5.3 LTS** or a compatible 4.5 build. Set `BLENDER` to its executable, or have `blender` on PATH. The verified local run uses the checksum-verified official 4.5.3 macOS ARM64 distribution. Newer versions may change lighting/pixels and require fresh visual acceptance.

```sh
PY=visual-atlas/v1/.venv/bin/python
$PY visual-atlas/v1/scripts/prepare.py
$PY visual-atlas/v1/scripts/make_jobs.py
$PY visual-atlas/v1/scripts/render_all.py
$PY visual-atlas/v1/scripts/assemble.py
$PY visual-atlas/v1/scripts/build_gallery.py
$PY visual-atlas/v1/scripts/verify.py
$PY visual-atlas/v1/scripts/inventory.py
```

**Moving the checkout:** rerun `prepare.py` and `make_jobs.py` before rendering. Generated job paths are machine-local absolute paths; they are regenerated from the new repository root, not manually edited. Packed `.blend` scenes can be opened directly. Blender X/Y/Z are east/north/source-specific height in metres, origin E837500/N821000 in EPSG:2326; vertical exaggeration is 1.

Composition uses Baskerville/Arial on macOS, DejaVu Serif/Sans on Linux. Override `ATLAS_SERIF_FONT` and `ATLAS_SANS_FONT` with installed font files for another platform. Different fonts change typography and need fresh visual inspection. Source images are not upscaled as recovered detail; display map grading only changes existing ink contrast.

For one view, pass its job ID, for example `render_all.py 08-november-surface`. Unknown IDs fail explicitly. `assemble.py` refuses changed original sources, prepared assets, render pixels or stale job records. The gallery can be opened normally in a browser or served locally. No separate website deployment is included.

## Rights and attribution

Source data: **Lands Department and Buildings Department, Government of the Hong Kong Special Administrative Region; CSDI Portal; DATA.GOV.HK**. Original data ownership retained; supplied as-is without endorsement. Included historical images are the audited **open-data DAP-L0 and Old Survey Sheets** routes, not paid imagery or excluded accident-report/Boeing scans. See [DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions), [CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC), [source audit](metadata/SOURCE_AUDIT.md) and the repository's `DATA_SOURCES.md`/`NOTICE.md`.

Original research and visualization © 2026 Aryan Ayyar. GitHub publication authorized for this version; no outreach, peer-machine sync or automatic future publication authorized.

Only `.blend` files in `scenes/` are current editable deliveries. Superseded `.blend1` backups are preserved in `qa/superseded-scenes/` and excluded from the final artifact inventory.

## GitHub downloads

All finished images, PDF, web previews, gallery source and scripts are tracked in this directory. [Editable Blender scenes and prepared assets](https://github.com/ayyararyan/kai-tak/releases/tag/visual-atlas-v1) are a separate checksum-verified release download. Original research datasets still use the existing repository restoration process.

Restore the scene bundle into the checkout without overwriting conflicting local files:

```sh
python3 visual-atlas/v1/scripts/restore_scene_bundle.py
```

This restores all 17 packed `.blend` files and derived assets. Regenerate machine-local JSON jobs with `make_jobs.py` before rerendering on another computer. Original render metadata preserves the source-run paths and hashes; they are provenance, not portable execution instructions.
