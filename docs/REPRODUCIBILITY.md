# Reproduce the work

[Project guide](README.md) · [Scripts and side effects](../scripts/README.md) · [Latest checks](migration/VALIDATION.md)

Choose the workflow you need. A metadata-only clone is sufficient for reading and
fast checks. Data restoration, scientific calculations, manuscript builds and
rendering are separate operations with different environments.

## Fast repository checks

Use Python 3.12 or later on macOS/Linux. Archive extraction relies on POSIX directory
descriptors; native Windows support is not claimed. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-repository.txt
.venv/bin/python scripts/repo.py fast
```

This lane checks maintained navigation, local links/anchors/assets, metadata/schema
consistency, Python syntax, preservation/rights boundaries and lightweight tests.
It downloads no research data, performs no numerical optimization and renders no scenes.
Historical link exceptions remain itemized in the migration record; new broken
references fail. Network availability is checked separately from local links.

After an accepted publication, edit `docs/project-status.json`, then regenerate
the marked navigation blocks with `python scripts/update_navigation.py`.
`--check` verifies without rewriting. Do not infer publication from a local PDF.
The root README is author-maintained: this generator never rewrites it. Update its
public-product links by an explicit editorial change when a new version is published.

## Mathematical models and scientific smoke checks

The original model environment is independent of the archive/maintenance environment:

```sh
python3 -m venv .science-venv
.science-venv/bin/python -m pip install -r publication/scientific-results-20261013/requirements.txt
.science-venv/bin/python scripts/repo.py science
```

The scientific lane runs model/counterfactual tests and explicit-reference tests
with their required working directories. It checks expected historical-mode refusal.
It also runs the [published scientific-result checks](../publication/scientific-results-20261013/README.md),
including the local-root proof and geometry tests reproducible from public inputs.
That runner documents restricted-source and original-workspace exclusions explicitly.
The wrapper runs it in a disposable checkout of its recorded artifact commit, because
later publication entries changed its hash-bound ledger. It first compares current
mapped scientific bytes; only the explicitly append-only ledger is exempt. Do not
weaken the frozen verifier or treat a historical snapshot pass as new-model acceptance.
It does not rerun the global search, photogrammetry or every continuous certificate.
Consult the [model guide](../research/checkers-runway13/README.md),
[approximation status](../research/checkers-runway13/approximation/STATUS.md) and
[counterfactual report](../research/checkers-runway13/counterfactual/REPORT.md).

For fixed-witness proof verification, use an extracted accepted manuscript source
package and run `verify_certificates.py` there. Proof wrappers generate receipts;
never run them over accepted frozen publication trees.

## Rebuild a white paper

Use the [publication index](../papers/README.md) to select the exact edition.
Extract its source ZIP into a **new directory outside the accepted tree**.
Install its own pinned `requirements.txt` and follow that edition's build guide.

- **v5:** the latest published editorial/visual edition, with its own Python 3.14
  production dependency record, XeLaTeX/BibTeX, Poppler and licensed Times, Arial
  and Courier New. `build.py --figures` regenerates the fifteen-figure suite.
  Consult its publication record for two documentation-only path normalizations;
  the original frozen README's local-only wording is a historical checkpoint.
- **v4:** XeLaTeX/BibTeX (recorded TeX Live 2026), Poppler and licensed Times,
  Arial and Courier New fonts. Set `XELATEX`/`BIBTEX` if needed. `build.py` checks
  104 source hashes before compiling and validates layout after compilation.
  `--figures` also regenerates scientific figures and their scalar checks.
- **v3:** Tectonic and Poppler; its portable package includes the frozen evidence,
  figure scripts and proof checkers. Use its own instructions, not v4's TeX command.
- **v2:** retain its documented dependency on the wider original layout for some
  archived proof code; do not claim that every legacy solver is standalone.

PDF byte identity is not generally expected from a fresh TeX run. Compare extracted
text, pagination and rendered pixels where the recorded platform supports that test.
Never replace the accepted PDF with a freshly built one just to make hashes match.

## Rebuild or verify the mathematical companion

The independent [mathematical note v1](../research/checkers-runway13/mathematical-note/v1/README.md)
has its own [source package](../research/checkers-runway13/mathematical-note/v1/certified-local-optimality-v1-sources.zip),
pinned environments and complete public proof closure. It does not supersede V5.
Extract the package into a new directory outside the accepted tree, then follow
its README for `build.py` and `scripts/verify_all.py`. Supply a fresh output directory
for verification receipts; do not regenerate accepted certificates in place.
The note records 117 public tests and seven excluded tests (not passes), with
scientific replay and grayscale production evidence kept distinct.

Its copied historical reports retain source-identical missing links. Fast checks
inherit only existing historical exceptions whose exact source bytes and pinned
snapshot manifest match; new links and changed copies still fail.

## Restore research data

Both established modes use the unchanged helper and refuse conflicting local files:

```sh
# Original dated research snapshot: five groups, including their historical exclusions.
python3 scripts/fetch_data.py

# Independent permitted-data archive release.
python3 scripts/fetch_data.py --release v1.0.0

# A small collection only; no full imagery download.
python3 scripts/fetch_data.py --release v1.0.0 --collection 05
```

The default selection is defined by [publication/release_assets.json](../publication/release_assets.json).
The versioned archive uses [archive/releases/v1.0.0/manifest.json](../archive/releases/v1.0.0/manifest.json).
These inventories and redistribution boundaries are not interchangeable.

For clean restoration acceptance, supply an empty real-path destination and a new
report filename. `--archive-dir` points to a verified bundle cache; `--offline`
forbids download. `--verify-only` checks bytes without extracting.

```sh
python3 scripts/fetch_data.py --offline --archive-dir /absolute/cache \
  --destination /absolute/new-legacy-root --report /absolute/new-legacy-report.json
python3 scripts/fetch_data.py --release v1.0.0 --offline \
  --archive-dir /absolute/public-archive-cache \
  --destination /absolute/new-archive-root --report /absolute/new-archive-report.json
```

Use actual nonsymlink paths, including ancestors. On macOS use `/private/tmp`
instead of the `/tmp` symlink if working there. Expect 1,254 legacy members or
418 archive members, not the catalogue's total research inventory.

## Validate archive metadata and reproduce weather

```sh
.venv/bin/python scripts/archive_validate.py
.venv/bin/python scripts/archive_validate.py --data-root /absolute/new-archive-root
python3 scripts/archive_reproduce.py --data-root /absolute/new-archive-root \
  --report /absolute/new-weather-report.json
```

Archive metadata validation requires its pinned jsonschema/PyYAML dependencies.
Weather replay runs the retained NOAA decoder and compares annual/day tables; it
does not reconstruct a complete along-flight wind field. Geospatial checks have
the separate [geospatial environment](../research/checkers-runway13/geospatial/README.md).
Provenance warnings are not suppressed by passing integrity tests.

## Recover the visual atlas

```sh
python3 visual-atlas/v1/scripts/restore_scene_bundle.py
```

This verifies the exact ZIP and its 27 scene/asset members. It is independent of
restoring the original research sources. For an isolated test use `--archive`
with a verified local ZIP and `--destination` with a new real-path directory.

Original sources must also match [input_manifest.json](../visual-atlas/v1/metadata/input_manifest.json).
Packed scenes can be opened directly; original render jobs include machine-local
paths. For rerendering, make a disposable checkout, restore its inputs, and rerun
`prepare.py` and `make_jobs.py` there before rendering. **Do not rewrite published
job/source hashes in the canonical v1 tree.**

The [atlas guide](../visual-atlas/v1/README.md#reproduce) gives the complete pipeline,
Blender 4.5.3 LTS requirement, fonts and single-view selection. Rendering and
`verify.py` write outputs. macOS/Linux font differences and Blender upgrades can
change pixels and require fresh visual review. Seventeen-view rendering is never
part of a README-change check.

## Verification tiers

| Lane | Trigger | What it establishes |
|---|---|---|
| Fast repository | Ordinary changes / pull requests | Navigation, schema, syntax and bounded infrastructure correctness |
| Scientific | Relevant scientific-source changes or manual request | Specified regression tests and expected gate behavior |
| Release integrity | Explicit request | Frozen bytes, source/asset identities; optional data/scene restoration using real bundles |
| Visual rebuild | Explicit manual request | A selected scene's actual regeneration in disposable space; not automatic acceptance of all views |

CI configuration is not a CI result. The [validation report](migration/VALIDATION.md)
records locally observed execution separately from unrun hosted workflows, full
scientific recalculation and visual acceptance.
