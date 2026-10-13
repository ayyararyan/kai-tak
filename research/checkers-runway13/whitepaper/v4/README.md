# Checkers with Runway 13 — Version 4

**RFS author-format edition, 13 October 2026.** [Read the PDF](checkers-with-runway-13-white-paper-v4.pdf). Formatting-only successor to the accepted V3: exact title, complete narrative and mathematics, 16 original figures, seven insights, six appendices and 51-claim ledger retained. The previously separate abstract appears on the title page. V2 and V3 remain unchanged in sibling directories.

This is an independent aviation-history/mathematics white paper using Aryan's website **RFS author adaptation**, not an RFS publication or submission. No journal branding, DOI, acceptance date or endorsement is implied. Later historical research in the wider repository has not been merged into this formatting-only edition. The first-person foreword remains marked for author review.

## Build

Extract `checkers-with-runway-13-white-paper-v4-sources.zip` and enter its `checkers-with-runway-13-v4/` directory. Tested with Python 3.14.6, XeLaTeX/BibTeX from TeX Live 2026, Poppler 26.07.0 and the pinned Python packages. Install a current TeX Live/MacTeX with `fontspec`, `newtx`, `mathtools`, `microtype`, `geometry`, `enumitem`, `setspace`, `etoolbox`, `needspace`, `placeins`, `longtable`, `xcolor`, `xurl`, `hyperref` and the standard tools/graphics packages. Put `xelatex`, `bibtex`, `pdftotext` and `pdffonts` on PATH.

The exact website typography requires licensed local **Times, Arial and Courier New** fonts. The production Mac uses `/System/Library/Fonts/Times.ttc` for Times, with its regular/bold/italic faces. Fonts are embedded in the PDF, not included as installable font files. A missing font is an error; the builder does not silently substitute a lookalike. Other operating systems or font releases have not been tested for identical pagination.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
```

Set `XELATEX` and optionally `BIBTEX` to executable paths when they are not on PATH. The script creates QA directories, checks all frozen input hashes, runs XeLaTeX/BibTeX with shell escape disabled, copies the named PDF, checks source preservation, text, fonts, references and geometry, and renders every page. Four XeLaTeX passes are intentional.

To regenerate the scientific figures and recheck their scalar calculations before compiling:

```sh
.venv/bin/python build.py --figures
```

To rerun both original continuous-time fixed-witness proofs separately:

```sh
.venv/bin/python verify_certificates.py
```

The default format rebuild does **not** rerun optimization, the 89-test model suite, photogrammetry, source acquisition or proof searches. Original V3 certificate/test receipts are explicitly archived under `qa/v3-baseline/`; `V3_VERIFICATION.md` describes those earlier checks. `VERIFICATION.md` records what was performed for V4. The optional proof command evaluates the same frozen witnesses, not historical flight safety.

## Inspectable sources

- `main.tex`, `rfs-workingpaper.sty`: layout and website-style adaptations; official `RFS.cls`/`rfs.bst` unchanged.
- `sections/`, `appendices.tex`, `coefficients.tex`: editable complete content.
- `baseline/`: accepted V3 TeX/BibTeX for independently reproducible content comparison, not a second build target.
- `figures/`, `make_figures.py`, `inputs/`, `evidence/`: original reproducible scientific figures and frozen inputs.
- `CLAIMS_AND_EVIDENCE.csv`, `SOURCE_MANIFEST.json`: unchanged scientific evidence ledger and 104 input hashes.
- `FORMAT_BASELINE.json`, `check_pdf.py`: source/figure identity and layout checks.
- `FORMAT_PROVENANCE.md`, `RIGHTS_AND_PROVENANCE.md`: typography authority and retained image/data attributions.
- `package_sources.py`: reproducible source selection, ZIP creation and exact-member verification.

Run `python package_sources.py` after completing visual review. Generated TeX intermediates, full-page renders, local paths in compile logs and Python caches are not publication files. The delivered PDF is the visual authority. Two legacy NewTX symbol fonts lack explicit ToUnicode maps; all fonts are embedded and body fonts are Unicode-mapped. Mathematical copy/paste is not promised to be lossless; editable equations remain authoritative.
