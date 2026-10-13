# Independent grayscale visual and preservation review

Checked at **2026-10-13T19:34:38Z** against published commit `01ccec8c3c982fbfe9352be3c43b693d41d01ba5`.
Current PDF SHA-256: `10ac658ffa41e7fad5cd7da3a4be5e2ad013a0b9b27ac2d37100a45171d6c98f`.

**Result: PASS.** All six figures and their six affected manuscript pages were
individually opened with `view_image` and inspected. No new clipping, overlap,
unreadable label, or loss of mathematical distinction was observed. This review
is limited to the author-requested grayscale conversion; no scientific proof
was rerun or changed.

## Preservation evidence

- The eight replacement colors exactly match the stated weighted grayscale rule.
- All eleven non-entry-point functions in `make_figures.py` have identical ASTs;
  the entry-point difference is only truthful palette metadata.
- `inputs/figure_data.json` is byte-identical to the published input.
- All six SVGs are identical after normalizing only color literals and
  color-dependent generated IDs together with their references. Thus their
  paths, dimensions, text, transforms, line styles, and opacity are unchanged.
- All six figure PDFs preserve text, font names, sizes, bounding boxes, and canvas.
- All six PNGs have exactly equal R/G/B channels at every pixel. SVG colors are
  likewise neutral. PDF color-setting operators are DeviceGray `g`/`G`.
- All 36 manuscript pages preserve extracted word strings and bounding boxes.
  Exactly pages **8, 13, 15, 19, 22, 26** change rendered pixels; the other
  **30 pages are pixel-identical** at the production rendering scale.
- Every inspected page PNG matches a fresh rendering from the current PDF.

## Individually inspected figures and pages

| Figure | Manuscript page | Visual result |
|---|---:|---|
| Landing | 8 | Solid CG and dashed virtual paths remain distinguishable; phase names, contact/reset notation and caption are readable. |
| Bracket | 13 | Bound endpoints, point/bar markers, separate retention scale and rightward lower-bound ray remain clear. |
| Active | 15 | Six labelled rows, event positions and terminal diamond distinguish constraints without relying on hue. |
| Certificate | 19 | Root, sufficiency and feasibility boxes, directed arrows and non-strict full-family qualification remain readable. |
| Continuous | 22 | Separate margin panels, solid curves, dashed primary line, shaded event zones and accepted-cell strips remain distinguishable. |
| Conditions | 26 | Ten labelled bars and values remain legible; unresolved cases remain text-only, with no invented frontier. |

The equal grayscale intensities for BLUE and SLATE are not an ambiguity: the
landing paths retain different line styles, while other mathematical objects
have explicit labels or separate positions/panels. No layout adjustment was
required or made. Figure captions and surrounding manuscript text remain in
their original positions.

Detailed hashes, palette values, SVG checks, PDF comparisons and page records
are in `grayscale-independent-checks.json`. This reviewer modified only these
two QA reports, not source code, figures, manuscript, data or certificates.
