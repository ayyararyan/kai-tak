# Checkers with Runway 13 — white paper v2

Aryan Ayyar · 13 October 2026 · 30 pages, seven figures. Working research paper, not peer reviewed.

**Read [the PDF](checkers-with-runway-13-white-paper-v2.pdf).** Version 2 adds a complete wind-conditioned landing, its own continuous-time model-feasibility certificate, a valid but loose optimality-gap bound, and the final blockwise reconstruction supplement. The calm-air result from v1 remains a separate benchmark.

The new case touches down at 302.11 m and stops at 2,233.23 m, leaving 552.77 m, under the declared steady 070° true / 21 kt wind and unchanged 2-second / 0.15g braking. Synthetic entry/corridor and uncalibrated aircraft assumptions remain explicit. This is not a historically validated landing, an accident-prevention claim, a near-optimality proof, or flight guidance. Physical prediction intervals remain unavailable.

## Edit and rebuild

Canonical text: `main.tex`, `manuscript.tex`, `wind_results.tex`, `appendices.tex`, `wind_appendix.tex`, `wind_coefficients.tex`, `references.tex`. Seven original figures are generated from frozen numerical evidence. `CLAIMS_AND_GAPS.md` and `VERSION_CHANGES.md` map what changed and what remains open.

Requirements: Python 3.14 (tested), Tectonic, Poppler `pdftotext` and `pdffonts` on PATH. Tectonic resolves TeX Gyre Termes and Termes Math from its bundle; first use may need network access. No proprietary fonts are required.

From this folder:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
```

The builder creates its figure/QA directories, checks snapshot hashes, recalculates stopping and exact gap arithmetic, reconstructs polynomial states/velocities and EAS against the exported control table, checks certificate source identity and closed time coverage, generates seven figures, compiles the PDF, and verifies both text extractors, embedded fonts, links and page bounds. It renders pages for separate visual inspection. Do not use optimized Python (`-O`); the builder rejects it because document checks use assertions.

This is a **manuscript reproduction package**, not a standalone end-to-end historical-data acquisition or landing-solver distribution. Files under `evidence/` are frozen research evidence, including archival counterfactual code for inspection; their original relative imports expect the wider project layout. A document rebuild does not rerun the interval proof or establish aircraft calibration. Final source checks and the separate 37-test conditional-case rerun are recorded in `qa/` and `DELIVERY_RECORD.md`.

## Provenance and publication

`evidence_manifest.json` records both original source hashes and public-snapshot hashes. Only host paths and internal-session identifiers in prose/metadata were normalized. Numeric inputs, proof code, coefficients and certificates are unmodified. Historical v1 evidence statements describe their recorded stage; this README and the version ledger describe v2.

The PDF and editable source are prepared for the explicitly authorized GitHub push to `ayyararyan/kai-tak`. The exact verified commit and remote status are reported in the handoff, not inferred from a local build. Version 1 is preserved locally. No website publication or third-party outreach is part of this task.

Source attribution: Hong Kong CAD; Lands Department/Buildings Department, Government of the Hong Kong SAR; NOAA/NCEI; cited research authors. The package excludes original accident-report PDFs, scholarly PDFs, survey rasters and aerial photographs. It includes authored reports/code and limited derived numerical figure inputs with their source terms retained. Public access does not relicense third-party material. No new blanket licence or institutional endorsement is claimed.
