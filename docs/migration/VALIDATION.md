# Migration validation

Initial baseline: `516bba9537f856d58a4cb440ad57e658dcd2bfcf`.
Reconciled upstream baseline: `125ebac16dc52a86998e2f6c4893e116bfca67d8`; see [preservation](PRESERVATION.md).
Execution began 13 October UTC / continued 14 October 2026 Asia/Kolkata.
Checks below are **newly executed locally**, not claims of hosted CI execution.

## Observed results

| Workflow | Before / after evidence | Outcome |
|---|---|---|
| Original archive + new maintenance regressions | Baseline 59 tests + 43 subtests; after review repairs 98 tests + 43 subtests | Passed, including 39 new infrastructure regression cases |
| Core model/counterfactual | 89 tests before and after implementation | Passed |
| Explicit reference approximation | 30 tests | Passed |
| Archive metadata | 32,912 checks before implementation | Passed, 2,739 retained provenance warnings |
| Dated snapshot restoration | Original helper, ordinary verified local bundle cache, empty destination; 1,254 exact members | Passed |
| Archive v1.0.0 restoration | Original helper, five public cached bundles, empty destination; 418 exact members | Passed |
| Installed permitted-data validation | 33,330 checks on the newly restored archive | Passed, same 2,739 warnings |
| NOAA replay | 12 decoder tests; two regenerated annual/day tables | Passed, byte-identical outputs |
| Geospatial source checks | 13 checks on the newly restored data | Passed; 83 original invalid geometries retained |
| Atlas scene restoration | Original helper, checksum-verified public ZIP, empty destination; 27 members | Passed |
| Atlas source dependencies | 25 source hashes checked against fresh restored data and tracked evidence | Passed |
| Representative scene rebuild | Preparation of 25 sources and 17 jobs in disposable tree; fresh Blender render of `08-november-surface` | Passed, 3840×2160 decoded RGB pixels identical |
| Paper v3 clean source build | Extracted 199-member accepted package; all 104 frozen inputs checked | Passed; all 33 pages text/pixel-identical at 100 dpi |
| Paper v4 clean source build | Extracted 235-member accepted package; all 104 frozen inputs checked | Passed; all 35 pages text/pixel-identical at 100 dpi |
| Paper v5 clean source build and figures | Extracted 278-member published package; `build.py --figures` | Passed; all 38 pages text/pixel-identical at 100 dpi, all 60 figure exports byte-identical |
| Published conditional scientific proof | Original 91ff740 artifact snapshot; 234 current scientific files and append-only ledger prefix checked first | 102 numerical/proof + 15 geometry tests passed; 224 source-seal bindings and 235 mapped public files checked |
| Fixed-witness certificates | Fresh execution in extracted v4 package | Calm: 2,502 cells, margin 0.0397; wind: 376 cells, margin 0.1507934696816132; both passed |
| Historical integration gate | Original `integrated/evaluate.py`, no output argument | Expected exit 2; 13 frozen inputs unchanged, historical integration remains blocked |
| Real browser acceptance | Chromium desktop 1440×1100 and mobile 390×844; 15 checks | Passed; no JavaScript errors, image/variant/modal/navigation checks passed |

## Inspectable receipts

- [Restoration results](restoration-results.json): exact bundle/member counts and
  initial symlink-cache refusal; source hashes were not changed to allow restoration.
- [Atlas source/scene dependencies](atlas-dependencies.json), [representative rebuild](atlas-rebuild.json).
- [Public HTTP readback](public-readback.json): accepted v4 PDF and archive weather bundle fetched anonymously and checksum-matched.
- [V3/v4 rebuild comparison](paper-rebuild-comparison.json), [v5 rebuild/figure comparison](v5-rebuild-comparison.json): all 106 pages across three editions.
- [Calm certificate](fresh_calm_certificate.json), [wind certificate](fresh_wind_certificate.json).
- [Weather replay](weather.json), [geospatial checks](geospatial.json),
  [historical gate output](historical-gate.json).
- [Browser acceptance](browser-acceptance.json): exact checked behavior and browser version.
- [Release comparison](releases-final.json): fresh API identities/digests, not merely old receipts.
- [Science command results](science-results.json), [maintenance results](maintenance-results.json).
- [Baseline archive validation](baseline-archive.json), [all baseline files](baseline.json).

The full temporary run logs, extracted build packages, restored data and screenshots
are outside Git in the local migration working directory. Bulky source data and
duplicate build products are not new repository artifacts. All byte comparisons
use accepted originals without rewriting them.

## Environment and failures repaired

System Python 3.14 initially lacked pytest/jsonschema. An isolated Python 3.12.13
environment installed the pinned maintenance and manuscript packages. Original
scientific environments were reused read-only for baseline model/GIS checks.

The original local legacy download cache consisted of symlinks. The existing
fail-closed extractor refused them. Ordinary copies of the actual files were placed
in a new cache and independently compared with the published archive SHA256 values;
the original unchanged restore helper then restored all five groups successfully.

V4 initially stopped because XeLaTeX was not on PATH. An existing local TinyTeX
installation was located and supplied through the documented `XELATEX`/`BIBTEX`
variables; no fallback font, TeX source or scientific content was substituted.
V3 used the installed Tectonic. All three builds used the available production fonts
and Poppler/PyMuPDF checks. PDF file hashes can differ because of build metadata;
the accepted PDFs themselves remain unchanged.

The browser test first attempted to decode an unset modal image and then waited
on lazy images; the test harness was corrected to load actual preview images
explicitly. No gallery code was changed. Real Chrome checks subsequently passed.
The homepage preview used local CommonMark/table rendering, not a claim of GitHub
production CSS or a deployed website. Desktop/mobile screenshots were inspected. After upstream reconciliation, all fifteen
checks were repeated against v5 navigation; the receipt binds exact gallery and homepage bytes.

## Remaining verification scope

- Hosted GitHub Actions are configured but have not been run from this unpushed branch.
- Full numerical/global-search reruns, every reconstruction experiment and all
  seventeen Blender rerenders are not part of this migration acceptance.
- Source-dependent historical computations needing restricted originals remain
  unavailable to an unaided public clone; no evidence gates were bypassed.
- Existing provenance warnings, inherited v1 manifest discrepancies and unresolved
  historical calibration remain scientific/data limitations, not repaired by layout.
- No cross-platform pixel equivalence, independent aerospace review, historical
  clearance, global optimum or operational safety is established.

## Final repository acceptance

Final fast run: **302 Python files, 1,117 JSON files and 1,775 local references**;
**98 tests plus 43 subtests passed**. The 701 exact link-exception records cover
760 inherited occurrences. Evidence: [maintenance-results.json](maintenance-results.json).
All 2,967 protected original files retained both SHA256 and Git blob identity, and
all five historical tag targets matched. All 22 release asset identities/server
digests remain unchanged. Public v4/v5 PDF and weather-bundle readbacks matched hashes.
There are zero new link errors; inherited exceptions remain exact and hash-bound.

The scientific command lane passed 89 model/counterfactual tests, 30 explicit-reference
tests, the expected blocked historical gate and the 117-test published scientific
snapshot. The latter is explicitly historical reproduction after confirming current
scientific bytes, not a claim that a later ledger is the old one. Initial direct-run
failure and its cause are preserved in the audit; no frozen check was weakened.

Navigation generation is idempotent, including two stale blocks in one file. Thirty-nine
new infrastructure cases exercise the actual review failure modes. Independent acceptance
and edge reviewers rechecked repairs, including the final multi-block reproducer.
[Review dispositions](REVIEW.md) record the full repair scope. Hosted workflows remain unrun.

**Correctness:** specified regression, integrity and build checks passed locally.
**Completeness:** all 18 architecture requirements covered by traceability.
**End-to-end readiness:** both restoration modes, atlas recovery/one render, three
manuscript builds, current model tests and historical proof reproduction verified.
This does not establish full scientific completeness, source rights resolution,
all-platform reproducibility or publication/merge approval.
