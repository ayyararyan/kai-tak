# Scientific figure provenance

Six figures, each exported as vector PDF, editable-text SVG, and 240 dpi PNG. The masters have exactly the manuscript's 373.2 TeX-point text width (`373.2/72.27` inches); no automatic bounding-box crop changes their dimensions. `figures/manifest.json` binds the figure input and all 18 exports by SHA-256.

## Visual architecture

The actual V5 production entry point and `whitepaper/v5/scripts/figure_style.py` were inspected. These figures retain its Arial labels, STIX mathematical symbols, open axes, light rules and vector-first export. On 14 October 2026, the author requested grayscale while keeping the figures otherwise identical. Each original RGB colour is converted using `round(0.2126 R + 0.7152 G + 0.0722 B)` and repeated equally in all channels: ink `#393939`, slate `#737373`, copper-role `#6C6C6C`, sage-role `#7C7C7C`, pale `#F1F1F1`, light `#E0E0E0`, grid `#DADADA`, blue-role `#737373`. The role names remain in the source to preserve every plotting call. Data, geometry, labels, line styles, alpha, dimensions and typography are unchanged.

The production build used the installed Arial font. No installable font files are copied or bundled. On systems without Arial, the script selects Liberation Sans, then DejaVu Sans; the selected font is recorded in the manifest. The supplied vector figures preserve the production typography irrespective of the reader's installed fonts. Rebuilding on a fallback font may change text metrics slightly.

## Reproduction

From this directory, in the pinned production environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python make_figures.py
```

The default build reads only `inputs/figure_data.json`; it requires no repository imports, private data, optimization or undocumented local paths. To recreate the plotting arrays from the bundled frozen evaluator and certificate records:

```sh
PYTHONDONTWRITEBYTECODE=1 python make_figures.py --refresh-data
```

The latter reads `inputs/local_certificate.json`, `inputs/active_branch.json`, `verification/condition-values.json` and the A1 numerical evaluator under `frozen-source/research/checkers-runway13/`. It makes no writes to those sources and runs no optimizer. All numerical source identities and hashes are recorded in `inputs/figure_data.json`.

## Figure-by-figure contract

| Figure | Source object and meaning | Deliberate limits |
|---|---|---|
| `landing` | Conceptual side-elevation drawing of approach, flare, contact, two-second delay and fixed `0.15g` braking. CG and virtual reference are offset vertically; the ideal vertical reset is labelled. | Explicitly not to scale; not a geographic map, obstacle-clearance drawing or calibrated aircraft illustration. Flare track is straight, not constant-altitude flight. |
| `active` | Six active margins from the actual root system. Interior event coordinates are `sS≈.7635208320`, `sL≈.7425247127`, `sT≈.3671596023`; gate and touchdown slew are at 0 and 1. The root centre's flare duration is displayed. | Event coordinates are rounded plotting values, not exact roots. Stopping is marked as a terminal hybrid equation, not an interior flight event. No high-dimensional geometry is projected. |
| `certificate` | Logical implication diagram: validated root `F(ζ*)=0`; positive simplex and nonsingular augmented matrix; whole-time feasibility; strict flare optimum; transfer through necessary flare constraints. | This is a proof-dependency diagram, not a geometric projection of a simplex. The `10^-20` label refers only to scaled root isolation, not an optimality or wind neighborhood. The final twelve-parameter conclusion is explicitly non-strict. |
| `continuous` | Three critical flare margin curves, evaluated at the numerical root-box centre with the sealed A1 `forces.phase`. The plotting grid has 2001 equally spaced points plus the three root-centre interior events. The five certified event zones are shaded for their applicable constraint. All 32 approach and 366 flare accepted interval cells are drawn at their actual normalized-time widths. | Curves are binary64 plotting evaluations, not interval lower bounds or proof by sampling. The dashed level is the plotting value of the certified root's primary coordinate. Entire-time proof comes from the accepted cell records plus analytical extrema bounds, not the appearance of the curve. |
| `bracket` | Exact input decimals `0.15236076430186170190` and `0.181970215` specify the displayed global-family bracket; width is approximately `.02960945`. A rightward ray on a separate scale depicts only `ηS−ηloc≥−10^-4`. | Not a root-uncertainty interval, confidence interval, local optimality radius or identified global optimum. The retention ray has no upper endpoint; it does not assert `ηS≤ηloc`. Rounded bracket-endpoint labels are illustrative; full decimal inputs are preserved. |
| `conditions` | Ten individually certified secondary-path lower bounds, read from `verification/condition-values.json`, organized by wind changes and geometry changes. Text labels are rounded downward to six decimals. Each bar starts at zero and represents its own path. | No interpolation, common policy, frontier or joint uncertainty statement. Tailwind 5 kt and urban 60/65 m are listed without invented zero bars. The baseline secondary bar is not the separately certified exact primary-root trajectory. |

## Exact input versus numerical illustration

The scaled decimal root centre is preserved verbatim. To make the plotting vector, its first three entries are multiplied by the exact scales 5, 300 and 75, and the corresponding five flare coordinates replace the approximate active-branch coordinates. The other seven approach entries come from the fixed branch record. The resulting vector is converted to binary64 solely for visual evaluation. The exact implicit root remains defined by its certificate box, not by this plotted vector.

`inputs/figure_data.json` stores all plotted arrays, all accepted cell rows, all event zones, all ten original condition records, both bracket endpoints and the root-centre decimal strings. It records which quantities are certified source data, rounded plotting coordinates or conceptual constructions. No sampled optimization output is silently promoted into a certified object.

## Visual inspection and export checks

All six PNG masters were inspected at full rendered resolution. An initial layout pass found overlapping title/subtitle baselines and overly long certificate-box text; both were repaired. Final independent review then corrected the root-vector label to `ζ` and replaced the retention segment by a one-sided rightward ray, avoiding an unsupported upper bound on the secondary margin. The two corrected figures were regenerated and inspected again. The final figures have unclipped labels at the fixed text width. The arrow/box logic of the certificate, separate close event times, actual interval-cell strip, distinct retention scale and explicitly unresolved conditions were checked visually.

The automated export inspection is recorded in `figures/export_checks.json`: one page per PDF; the exact intended PDF width; no embedded raster images in the vector PDFs; no SVG raster-image tags; all extracted PDF text boxes lie within the page; and a second default source-data build reproduces all 18 export hashes. The source-data-only run is the portable figure-build check; the parent separately owns clean-environment manuscript and proof reproduction.

The grayscale revision additionally verifies equal RGB channels in every PNG pixel and grayscale fill/stroke colours in every SVG. `qa/grayscale-independent-checks.json` and `qa/grayscale-visual-review.md` compare the updated figures and manuscript with the prior public commit; `qa/grayscale-clean-build.json` records the clean-extraction rebuild. The scientific arrays and manuscript LaTeX are unchanged.
