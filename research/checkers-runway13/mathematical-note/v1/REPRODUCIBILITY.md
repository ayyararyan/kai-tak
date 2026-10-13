# Reproducibility and clean-environment record

## Scope

The source package builds the note and replays its public mathematical certificates without the rest of the repository. It includes 487 exact public source files (34,184,693 bytes), pinned to `78a9ce1c627f917c94306af5529d5e9ebeb743e8`. The source subset is a proof/test dependency closure, not a copy of the historical archive. Restricted originals, private enquiries, credentials and installable proprietary fonts are absent.

Latest-main reinspection is recorded in `qa/upstream-freshness.json`: the later changes concern the repository README and presentation assets, not the frozen scientific sources or V5 production files.

## Build

Use a new Python environment and an installed XeLaTeX/BibTeX toolchain:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python build.py --figures --render
```

The tested production interpreter is Python 3.14.6 on macOS arm64. Exact package versions are in `requirements.lock`; TeX and PDF tool versions are recorded in `qa/toolchain.txt`. The unchanged V5 style requires locally licensed Times, Arial and Courier New, with NewTX mathematics. See `FORMAT_PROVENANCE.md`. A clean Python environment was created and packages installed afresh; the host TeX installation and licensed fonts were reused. This is not a claim to have tested a fresh operating-system image or another platform.

Place `xelatex` and `bibtex` on `PATH` or set `XELATEX` and `BIBTEX`. Poppler is optional for additional font reporting; PyMuPDF performs the page checks and renders. No local workspace path is needed by the build.

The clean extracted package regenerated all six figures and compiled the manuscript. `qa/clean-build-comparison.json` records the comparison of all 36 pages' extracted text and 100 dpi pixels, and all 18 PDF/SVG/PNG figure exports. PDF container hashes may differ because build metadata changes; page content and rendering, not just file existence, are compared. The accepted PDF hash is in `DELIVERY_MANIFEST.json`.

## Mathematical reproduction

For the independently tested proof environment (Python 3.12.13):

```sh
python3.12 -m venv .venv-verify
.venv-verify/bin/python -m pip install -r verification/requirements.lock
.venv-verify/bin/python scripts/verify_all.py \
  --source-root frozen-source --output-dir verification/new-run
PYTHONDONTWRITEBYTECODE=1 .venv-verify/bin/python verification/emit_matrices.py \
  --source-root frozen-source --output verification/new-run/local_matrices.json
```

Use a new output directory to preserve earlier results. The runner executes stages in separate processes and prevents bytecode writes to the sealed source subset. Do not execute old certificate-producing main functions in their source directories: some replace historical outputs.

All seven stages were freshly run: public tests, local root/simplex/events/path, secondary retention, analytical bounds, wind domains, ten conditions and legacy synthetic witnesses. `verification/accepted/run.json` records actual commands, durations and return codes. The matrix export is a separate executed check. The fresh production environment additionally reran all 117 public tests from the extracted source package; its retained receipt is under `verification/clean-package/`.

The checks are proof replays, not new optimization experiments. Five restricted historical-source tests and two original-workspace preservation tests are unavailable or inapplicable to the normalized public subset. They are explicitly excluded, never counted as successful tests. See `verification/README.md` and `audit/reproduction.md` for exact exclusion names and failure chronology.

## Integrity and package

`frozen-source/PUBLIC_SOURCE_MANIFEST.json` binds all 487 files. The additive integrity checker preserves the sealed checker and validates its exact historical ledger prefix, then validates the full newer ledger separately. The inherited direct checker failure remains in the package.

```sh
.venv/bin/python package_sources.py
```

The packager validates all frozen-source hashes, creates a fixed-order/fixed-timestamp ZIP, and verifies every archived member. It excludes caches, virtual environments, page renders, TeX intermediates and its own ZIP/manifest. Two final invocations are compared for deterministic identity. `qa/final-package-checks.json` also binds the final package's build/proof inputs to the tested clean extraction; later-added review documents do not change the mathematical or production inputs.

## Evidence boundaries

The certificate implementation and interval arithmetic backend are part of the trusted computational base; no proof-assistant kernel or independent interval library was used. The manuscript supplies analytical arguments and finite interval objects so these assumptions can be inspected. No human aerospace peer review, historical calibration, operational landing certification, global primary solution, secondary-effort optimum, or unobserved-gust policy is implied.
