# Reproducibility and clean build — Version 5

## Reproduction contract

This edition is built from the editable manuscript, frozen numerical evidence and original historical visual inputs in this directory. The build regenerates all 15 illustrations; it does not rerun an optimizer, reconstruct a new city, reacquire historical sources or calibrate an aircraft.

The ordinary command is `python build.py --figures`. It checks the original 104 frozen input hashes, the 11 supplemental historical input hashes, 287 science assertions and 74 independent figure-semantic assertions; it runs four XeLaTeX passes and BibTeX, verifies the resulting PDF and renders every page. `python verify_certificates.py` separately reruns both original fixed-witness certificates. `python scripts/verify_v5_science.py --fresh-bound` includes the additional fresh calm-bound check (288 total).

## Dependencies

The clean environment uses Python 3.14.6 and the exact versions in requirements.txt: NumPy 2.5.4, Matplotlib 3.11.2, PyMuPDF 1.28.2, Pillow 12.3.0, SciPy 1.18.1, mpmath 1.3.0 and pytest 9.1.1. XeLaTeX/BibTeX from TeX Live 2026 and Poppler are host tools. `XELATEX` and `BIBTEX` may select executable locations; no particular workspace path is required.

Locally licensed Times, Arial and Courier New are required. The final PDF embeds font subsets; installable proprietary font files are not redistributed. Exact pagination and pixels are verified only for the recorded host/font versions. Other environments may yield typography differences even with identical mathematics. FORMAT_PROVENANCE.md records the academic style.

## Package contents and exclusions

`python package_sources.py` writes a deterministic ZIP with fixed member timestamps and checks every member against its source bytes. It includes the manuscript, style/dependencies, scripts, historical inputs, frozen proof evidence, all vector and screen figures, 600 dpi exports, editorial records and compact JSON receipts. It excludes virtual environments, compiler intermediates, rendered-page images, restricted original CAD report scans and proprietary fonts. The source package is a local mixed-rights research deliverable, not a new blanket licence or external publication. RIGHTS_AND_PROVENANCE.md controls reuse.

The frozen CAD-derived digitizations remain reproducible as retained inputs; this package does not claim to redistribute every original source publication. Source availability and restrictions remain explicit.

## Clean-build acceptance

A new source ZIP was extracted into a fresh directory and built with a separately created Python environment on 13 October 2026. The ordinary `build.py --figures` command exited successfully. All 287 science checks and 74 figure checks passed inside that extraction. No original checkout or existing figure output was used as the build directory.

Results: **38/38 page texts and RGB pixel arrays match**, and **60/60 figure exports are byte-identical** (15 PDF, 15 SVG, 15 screen PNG, 15 presentation PNG). The two manuscript PDF byte hashes differ; byte-identical PDFs are not claimed. The final accepted PDF is `328f848d805df1e5bac5fd6aff6f28363112bea3acd9a5fcb71c33ec16842939`. Its clean-build counterpart is `a11fa31cdd01c2d841f5373042a276750ee559fed7bd7e7a48224e69e68c3d26`. The matching text and pixels establish content/layout reproduction on the tested toolchain.

Receipt: `qa/clean_build_verification.json`, including per-page/per-export hashes and 150 build-sensitive input hashes. The tested staging archive is identified there. Final packaging adds completed reports and acceptance receipts. The packaging script was separately finalized to include the font receipt and exclude machine-local/circular delivery records; it is tested by the final deterministic ZIP replay. the delivery check confirms the final archive retains all clean-tested build inputs and exact deliverable bytes. `qa/delivery_acceptance.json` records that bridge, so the final archive is not silently substituted for the tested one.

All 38 pages were separately inspected as images. The independent editorial review followed the mathematical/source checks; its accepted repairs and final layout-only delta are recorded. No automated result is used to infer prose quality.

The clean Python environment is not a fresh operating system: the existing host TeX, Poppler and licensed fonts were used. Rebuilding on another operating system is documented but not tested. The 89 regression tests and both exact certificates were freshly run during V5 production; they were not repeated inside this final ordinary-build command. Their distinct run receipts are retained.
