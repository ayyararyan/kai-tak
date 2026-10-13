# Certified Local Optimality in a Constrained Landing Model

Aryan Ayyar · Independent mathematical research note · Version 1 · 14 October 2026

This is a standalone companion to *Checkers with Runway 13*, V5. The exact A1 local root, strict five-variable max-min sufficiency, whole-time feasible connection and non-strict twelve-parameter transfer are proved in the manuscript. The global family bracket remains unmatched. This is a conditional mathematical model, not a historical or operational aircraft certificate.

## Read

- `certified-local-optimality-v1.pdf`: finished manuscript.
- `main.tex`, `sections/`, `appendices.tex`, `references.bib`: editable sources.
- `SCIENTIFIC_VERIFICATION.md`: checked claims and actual execution.
- `INDEPENDENT_REVIEW.md`: five review domains, findings and disposition.
- `CLAIMS_AND_EVIDENCE.csv`: theorem/premise/source/command ledger.
- `PUBLICATION_READINESS.md`: acceptance and author-approval boundary.

## Clean build

The directory and its source ZIP are self-contained. Create a new Python environment (tested Python 3.12.13 for proof checks and 3.14.6 for production), then:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python build.py --figures --render
```

Host tools: XeLaTeX and BibTeX with the V5 TeX packages, and optionally Poppler `pdffonts`/`pdftotext`. Put the TeX bin directory on `PATH`, or set `XELATEX` and `BIBTEX`. No workspace-specific default is embedded. Locally licensed **Times**, **Arial**, and **Courier New** are required by the unchanged V5 style. NewTX supplies mathematics. Installable proprietary fonts are deliberately excluded; the delivery PDF embeds subsets. `FORMAT_PROVENANCE.md` records the exact reference and comparison.

`build.py` verifies frozen build inputs and 47 source-consistency assertions, optionally regenerates six vector figures, runs four XeLaTeX passes plus BibTeX, and checks page geometry, fonts, references and visible text. `--render` produces one PNG per page in `qa/pages/`. It does **not** rerun mathematical certificates; a successful build is not proof of mathematical correctness.

## Fresh public mathematical verification

No optimizer or source-producing script is invoked. Run:

```sh
.venv/bin/python scripts/verify_all.py \
  --source-root frozen-source --output-dir verification/replay
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verification/emit_matrices.py \
  --source-root frozen-source --output verification/replay/local_matrices.json
```

`--stage` can select `public-tests`, `local`, `retention`, `bounds`, `domains`, `conditions` or `legacy`. The first command reruns 117 publicly available tests, exact root/simplex/event/full-time checks, secondary retention, analytic/global bounds, three wind domains, ten condition certificates and numerical forward replays. The legacy stage separately checks original synthetic-model certificates; their values are not substituted into A1. The second exports full interval Jacobians, exact decimal preconditioners and binary interval endpoints. It is a separate computation, not silently included in the first command.

The frozen public-source subset is pinned to Git commit `78a9ce1c627f917c94306af5529d5e9ebeb743e8`. `frozen-source/PUBLIC_SOURCE_MANIFEST.json` checks every included file against that source. The original publication checker assumes an earlier project-ledger byte length; V5 added legitimate ledger text. The additive verifier checks the historical prefix and current full hash separately and records the original failure. No sealed checker, old certificate or original manifest was rewritten.

Five historical-source tests and two original-workspace preservation tests are excluded because their inputs are unavailable or intentionally normalized in the public tree. They are **not passes**. The conditional mathematical certificates here do not require those restricted originals. See `audit/reproduction.md` and `verification/accepted/` for actual logs, and the preserved `verification/initial-*.log` files for failures and repair chronology.

## Package, rights and release

`python package_sources.py` creates the deterministic compact source ZIP after validating the source snapshot. It includes the frozen public proof closure, authored figures and sources, PDF and verification records; excludes environments, page renders, TeX intermediates and caches. The package does not duplicate the entire repository or historical archive. Existing RFS/crop notices and repository `NOTICE.md` are retained; `RIGHTS_AND_PROVENANCE.md` specifies scope. No new license is granted.

Prepared locally for a versioned release. **No push, release creation, publication or modification of an existing release is authorized by this package.** Author approval is the remaining publication gate.
