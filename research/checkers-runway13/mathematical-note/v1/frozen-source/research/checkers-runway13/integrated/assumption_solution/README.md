# Assumption-conditional Kai Tak landing study

Start with [REPORT.md](REPORT.md), [assumptions](ASSUMPTIONS.md), [derivation and proof domains](DERIVATION.md), and [condition table](conditions.csv). This branch implements Aryan's instruction to proceed using existing evidence and explicit assumptions. It does not change the historical evidence or claim historical clearance.

From the canonical research root:

```sh
.venv/bin/python -m pytest -q integrated/assumption_solution/test_solution.py
.venv/bin/python integrated/assumption_solution/evaluate.py mean 20
.venv/bin/python integrated/assumption_solution/evaluate.py urban55 30
```

The evaluator accepts only solved, certified named cases and times within entry-to-stop; at phase joins `--side left`/`right` exposes one-sided controls and the touchdown reset. It does not interpolate conditions or supply flight guidance.

Reproduction order: `build_scene.py` (using geospatial/.venv because pyproj/shapely are already installed there); `search.py`; `search_extra.py`; `refine_tall.py`; `repair_exit.py`; `secondary_polish.py`; `regularity.py`; `certify.py`; `export.py`; `verify_package.py`. Search may take minutes and floating-point optimizers need not reproduce exactly the same numerical stationary point. Existing `cases/*/result.json` and certificates bind the delivered values. Preserve existing runs before intentionally rerunning searches; the scripts append attempts in repair stages, but the first search script is a producer, not an archive manager.

All airborne references have explicit polynomial formulas, force inversion and exact stopping regimes. The full condition-to-global-optimum closed form has NOT been obtained. Global terminal-relaxation bounds and a finite-family existence proof are not a global optimizer. Physical prediction intervals and a causal gust/go-around controller are absent.

`scene.json` contains assumed solids with source provenance; their new heights are NOT observations. The original source GeoJSON and its unknowns are unchanged. In particular, the blanket urban height is an assumption over missing coverage, not a recovered historical building height.

No new acquisition, outgoing enquiries, publication, paid services or agents were used after the correction. Third-party aircraft-source images remain in the separate local aircraft_followup directory; do not infer redistribution permission.
