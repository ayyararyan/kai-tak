# Checkers with Runway 13 — Version 3

A complete 33-page research white paper by Aryan Ayyar, with eight narrative parts, 16 scientific figure composites, seven explanatory insights and mathematical appendices. The 471-word first-person foreword is explicitly for author review. This edition is a local deliverable: it has not been pushed or published.

## Read

- `checkers-with-runway-13-white-paper-v3.pdf`: finished manuscript.
- `abstract.md`, `executive-summary.md`: public-facing companion text.
- `VERIFICATION.md`: mathematical checks, document acceptance and scientific limits.
- `CLAIMS_AND_EVIDENCE.csv`: claim-by-claim evidence and interpretation.
- `RIGHTS_AND_PROVENANCE.md`, `SOURCE_MANIFEST.json`: attribution and immutable inputs.
- `VERSION_CHANGES.md`, `REQUIREMENTS_TRACEABILITY.md`: changes and scope audit.

## Build from this directory

Requirements: Python 3.12 or 3.14, Tectonic 0.17.0, Poppler (`pdftotext`, `pdffonts`). Tectonic may download its public TeX bundle on first use. No project credentials or parent-directory data are required. On macOS the system tools can be installed with `brew install tectonic poppler`; other systems should use their package manager or official binaries.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
.venv/bin/python verify_certificates.py
```

Do not use Python `-O`: original research verifiers contain scientific assertions. `build.py` verifies 104 immutable input hashes, independently recalculates displayed results, regenerates 16 PDF/PNG figures, rechecks the calm-family regularity and upper bound, compiles LaTeX, checks references/fonts/text bounds and renders every page under `qa/pages/`. `verify_certificates.py` separately recomputes the two fixed-witness continuous-time interval certificates; it takes longer than typesetting. It never reruns optimization or overwrites the original evidence.

`qa/fresh_*` are fresh receipts; `evidence/` contains frozen original artifacts. `evidence_manifest.json` is the inherited V2 67-file subset, while `SOURCE_MANIFEST.json` is the full V3 104-file freeze. Both are checked. Changes to source evidence must be deliberate and justified; do not regenerate manifests merely to silence a mismatch.

For an independent rerun of the supplied model/counterfactual test collection:

```sh
.venv/bin/python -m pytest evidence/model evidence/counterfactual/test_counterfactual.py -q
```

The source archive contains all files needed for these commands, including the original corridor dependency. `main.tex`, `sections/`, `appendices.tex`, `coefficients.tex` and `references.bib` are editable. Scientific plots are created by `make_figures.py`; captions and equations are in the LaTeX. `check_pdf.py` is automated acceptance, not a substitute for visually reviewing the rendered pages after an edit.

## Reproduction scope

The supplied package reproduces figures, manuscript, scalar/endpoint checks, fixed witnesses and the retained family bound. It does **not** reacquire the complete historical archive, rerun dense photogrammetry, repeat optimizer searches or re-digitize all recorder plots. Their original methods, larger datasets and manifests belong to the wider `ayyararyan/kai-tak` repository and releases. Report scans and scholarly PDFs whose redistribution permission is not established are linked, not bundled.

No aircraft-performance calibration, historical clearance, robust feedback policy, global near-optimality or historical procedural superiority is established. The two wind scenarios are different optimization problems. Exact source-decimal certificate constructions, floating-point plotting exports and rounded printed coefficients are distinguished.

## Rights

See `RIGHTS_AND_PROVENANCE.md`. Government imagery/data retain source-specific ownership and attribution terms. This task does not select a blanket licence for original research/code. Public availability must not be read as permission to relicense all inputs. Version 2 and the frozen research artifacts remain unchanged.
