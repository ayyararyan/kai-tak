# Public mathematical reproduction

Run these commands from the mathematical-note `v1/` directory. They need Python
3.12, an ordinary writable output directory, and the included `frozen-source/`.
No Git checkout, private source scan, original workspace, optimizer run, or
undocumented machine path is required.

```sh
python3.12 -m venv .venv-verify
.venv-verify/bin/python -m pip install -r verification/requirements.lock
.venv-verify/bin/python scripts/verify_all.py \
  --source-root frozen-source --output-dir verification/new-run
.venv-verify/bin/python verification/emit_matrices.py \
  --source-root frozen-source --output verification/new-run/local_matrices.json
```

Choose a new output directory to retain earlier receipts. The wrapper sets
`OPENBLAS_NUM_THREADS=1` and `PYTHONDONTWRITEBYTECODE=1` and removes an inherited
`PYTHONPATH`. Source proof scripts have module-level interval wind state; each
stage runs in its own process. Do not run the old producer mains against the
sealed source directories: several overwrite their certificates and manifests.

## What is executed

1. All 117 public tests, with the original explicit seven exclusions and an
   additive, append-aware input-integrity check.
2. The accepted exact root box, Krawczyk inclusion, nonsingularity, positive
   multiplier simplex, five active neighborhoods, and full-path coverage.
3. Baseline delivered-secondary retention relative to the exact local primary
   optimum, and independent Newton replay of the numerical root center.
4. The 4,096-cell family exclusion at `0.181970215`, terminal interval signs,
   and failure to exclude zero margin for the unresolved 5 kt tailwind case.
5. All three accepted continuous known-wind affine-trajectory domains.
6. Ten complete-path condition certificates and independent numerical Newton
   replays; the eight original cases also reproduce their continuous retention
   comparison with the stored numerical primary paths.
7. The legacy synthetic calm/wind witnesses and legacy coupled vertical-speed
   and family-bound functions, explicitly separated from A1.
8. The separate matrix-export command records the full interval Jacobians,
   exact decimal preconditioners, residual operators, Krawczyk offsets and
   augmented active-gradient matrix. Exact binary endpoints accompany the
   original directed interval strings.

These are proof replays and regression checks, not a new optimization search.
They do not establish historical/operational validity, global primary
optimality, global secondary optimality, or a gust-feedback policy.

## Frozen inputs and the inherited checker defect

The included subset contains **487 exact public files, 34,184,693 bytes**, from
Git commit `78a9ce1c627f917c94306af5529d5e9ebeb743e8`. It includes the original
scientific seals, the publicly available preservation dependencies and the
legacy input-manifest dependencies needed by the unchanged tests. The
[source manifest](../frozen-source/PUBLIC_SOURCE_MANIFEST.json) pins every byte.
It does not include restricted originals or runtime caches. The root
`NOTICE.md` remains part of the subset; no new license is granted.

The inherited `run_public_tests.py` fails before collecting tests on the pinned
current main: its 13 October mapping expects the then-current
`PROJECT_STATE.md`, but later V5 publication entries were appended. The entire
102,013-byte historical ledger prefix still has its exact mapped hash. Our
additive [checker](verify_public_inputs.py) verifies that prefix **and** the
complete 106,014-byte current ledger against its pinned hash. Every other
mapping and original seal is checked exactly; no scientific-byte exception is
made. The inherited checker and its failed log remain unchanged/preserved.

Generated `__pycache__` entries also violate that historical checker's explicit
exclusion list. Running from the clean source subset with bytecode disabled
avoids this without deleting caches or weakening the exclusion check.

## Accepted receipts

- [Stage commands, return codes and elapsed times](accepted/run.json).
- [Fresh public test log](accepted/public-tests.log), [test counts](accepted/public-tests.json).
- [Input integrity](accepted/public-input-integrity.json), [final preservation](accepted/preservation.json).
- [Local certificate](accepted/local-certificate.json).
- [Actual proof matrices](final/local_matrices.json).
- [Secondary retention](accepted/secondary-retention.json).
- [Analytical bound evaluations](accepted/analytical-bounds.json).
- [Wind domains](accepted/wind-domains.json).
- [Ten conditions](accepted/conditions.json), with per-condition proof files.
- [Legacy model checks](accepted/legacy-summary.json).
- [Numerical audit and repair record](../audit/reproduction.md).

The accepted run used a freshly created Python 3.12.13 environment with the
fully pinned [dependency lock](requirements.lock). Platform and package versions
are in [environment.json](accepted/environment.json). Reproduction was performed
on macOS arm64; no claim is made that another OS was tested in this delivery.

## Recreate the source subset from Git

The archive is already self-contained. To independently recreate its input
subset from a repository containing the pinned commit:

```sh
python3.12 verification/make_source_snapshot.py \
  --repository /path/to/kai-tak --destination /path/to/new-frozen-source
```

The extractor uses `git archive` at the fixed commit, never arbitrary workspace
bytes. Existing destinations are refused unless `--extend` is explicitly used
for a draft closure; extension verifies every existing byte and never replaces
a copied source file. The complete accepted subset needs no extension.
