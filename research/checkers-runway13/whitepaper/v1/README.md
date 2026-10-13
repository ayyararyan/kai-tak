# Checkers with Runway 13 — first white-paper draft

Author: Aryan Ayyar. Version 1, 13 October 2026. 23 pages, five figures. **Private working draft; not published or peer reviewed.**

## Read or edit

- `checkers-with-runway-13-white-paper-v1.pdf`: fixed-layout reading copy.
- `main.tex`: document setup, title, executive summary and inclusion order.
- `manuscript.tex`: main argument and results.
- `appendices.tex`: dynamics, model domain, restricted proofs, provenance and contribution statement.
- `references.tex`: primary-source references with hyperlinks.
- `figures/`: five original, reproducible manuscript figures in PDF and PNG.
- `evidence_manifest.json`: timestamped hashes of the frozen source evidence.
- `CLAIMS_AND_GAPS.md`: claim-to-source map and unfinished research sections.
- `qa/`: numerical figure checks, document checks, extracted PDF text and rendered pages.

This is a prose manuscript, not an outline. It preserves the proposed white-paper scope while explicitly leaving historical validation, terrain-aware feasibility, calibrated uncertainty and the improved-approach claim unfinished. The final drafting check incorporated the settled CAL605 benchmark and corrected dense geometry after verifying 98 flight-delivery hashes and 30 geometry-handoff hashes. The frozen source reports are evidence for claims at their stated level, not a new independent peer review.

The package rebuilds the **manuscript and its five figures**. It is not the complete landing solver or full historical-reconstruction pipeline. Those remain in the parent project, with their separate dependencies, original data and validation records. No aircraft configuration, research model or active reconstruction artifact was changed to make this paper.

## Build

Requirements: Python 3.14 (tested), Tectonic on PATH, and Poppler `pdftotext` and `pdffonts` on PATH. Tectonic resolves TeX Gyre Termes regular/bold/italic/bold-italic and TeX Gyre Termes Math from its TeX bundle. Its first build may need network access to retrieve TeX packages/fonts. No proprietary system font is required or bundled.

From this folder:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
```

The builder creates `figures/` and `qa/`, verifies frozen hashes, reproduces the plots, compiles the PDF, checks content with PyMuPDF and Poppler, checks embedded fonts and links, and renders all pages for visual inspection. Source fonts and rasterized plot labels are embedded in the delivered PDF; no claim about DOCX/Word rendering is made, because LaTeX is the editable source.

`make_figures.py` checks the exact 8,360-observation weather subset and its below/tie/above counts, recomputes scalar stopping quantities, and checks trajectory endpoint consistency. These checks do not re-prove the historical reconstruction or the original continuous certificate. `check_pdf.py` leaves visual inspection pending by design; the delivery record documents the actual rendered-page review.

## Evidence and rights

Primary report: Hong Kong CAD Report 1/95. Geospatial sources: Lands Department and, in the wider chronology, Buildings Department, Government of the Hong Kong SAR. Weather: NOAA NCEI ISD. Citations and source reports retain dates, coordinate meanings and source routes.

The source ZIP includes authored text, code, frozen project reports and limited derived numerical plot inputs. It excludes third-party report PDFs, historical map images, aerial photographs and full raw geospatial archives. Derived materials still retain applicable source terms; the ZIP is a private research handoff, not a public-data licence. No outreach, public upload or institutional endorsement occurred.

## Next revision

1. Extend the selected CAL605 benchmark into identifiable state/model diagnostics without forcing clock or geometry alignment.
2. Integrate defensible historical corridor geometry and datum/tracking assumptions into the landing comparison.
3. Add a condition-dependent rule, useful performance-gap evidence and calibrated outcome uncertainty when supported.
4. Complete broader literature/comparator checks and author/specialist review before any public research claims.

The canonical wider-project ledger remains `../../PROJECT_STATE.md`. This file describes the frozen draft package, not a second scientific project ledger.
