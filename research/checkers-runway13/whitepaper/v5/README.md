# Checkers with Runway 13 — Version 5

Aryan Ayyar · local editorial and visual edition. This directory is the self-contained production source; V4 remains unchanged in its sibling directory. No external publication is part of this task. The personal foreword is explicitly a draft for the author's approval.

## Build

Requires Python 3.14, the pinned packages below, XeLaTeX/BibTeX (TeX Live 2026 tested), Poppler `pdftotext`/`pdffonts`, and locally licensed Times, Arial and Courier New. The PDF embeds font subsets; installable proprietary fonts are not redistributed. Other operating systems/font versions may paginate differently. The RFS author style and original class/dependency notices are preserved.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py --figures
```

Set `XELATEX` and optionally `BIBTEX` to executable paths if needed. The builder creates output/QA directories, verifies the original 104 frozen source hashes and 11 supplemental visual inputs, runs independent science/figure checks, regenerates all V5 figures from the master scripts, compiles the paper, checks fonts/references/layout and renders every page. `abstract.md` is the editable source for the generated `abstract.tex`.

To recheck the exact original fixed witnesses without optimization:

```sh
.venv/bin/python verify_certificates.py
.venv/bin/python scripts/verify_v5_science.py --fresh-bound
```

The first command reruns both continuous-time proofs. The second independently checks scalar results, curve/CSV relations, source counts, the exact wind bound and (with the flag) the calm regularity/upper-bound calculation. These do not reconstruct a historical flight, reacquire the archive or re-estimate aircraft performance. See SCIENTIFIC_VERIFICATION.md for checks actually performed.

## Editable masters and evidence

- `main.tex`, `sections/`, `abstract.md`, `appendices.tex`, `coefficients.tex`, `references.bib`: complete editable manuscript.
- `RFS.cls`, `rfs-workingpaper.sty`, `rfs.bst`, `crop.*`: academic typography and dependencies.
- `make_figures.py`, `scripts/`: new reproducible illustration system.
- `figures/`: vector PDF/SVG masters and screen PNGs; `presentation/`: matching 600 dpi PNG exports.
- `inputs/`, `evidence/`: immutable V4 input snapshot. Additional historical originals/accepted mesh are under `inputs/historical/`, bound by a separate provenance manifest.
- `CLAIMS_AND_EVIDENCE.csv`, `SCIENTIFIC_VERIFICATION.md`: claim routes, mathematical scope and source checks.
- `editorial/`: diagnosis, seven-act map, caveat audit, alternative openings and before/after examples.
- `SPEC.md`, `STATE.md`, `REQUIREMENTS_TRACEABILITY.md`: approved scope and current acceptance evidence.
- `FIGURE_REDESIGN.md`, `VERSION_CHANGES.md`, `REPRODUCIBILITY.md`, `EDITORIAL_ASSESSMENT.md`: visual, narrative, build and final editorial records.

Use `python package_sources.py` to construct the portable ZIP after acceptance. The source package deliberately excludes virtual environments, TeX intermediates, full-page renders, unpermitted original CAD scans, local paths in compiler logs and previous-version packages. The delivery manifest binds the reviewed outputs; a successful compile is not a substitute for the separately recorded visual/editorial review.

## Scientific and source boundaries

The model and evidence meanings are unchanged. Calm and known-wind references have separate certificates; their difference is not a causal wind estimate. Historical surfaces remain incomplete and unregistered to the synthetic landing. The full technical scope and source conventions are in Appendices G–H. Lands Department/CSDI/DATA.GOV.HK attribution and retained Government ownership accompany historical imagery. No blanket licence is newly granted.
