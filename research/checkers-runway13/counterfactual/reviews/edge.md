# Independent edge-case review

Reviewed 2026-10-13: four new-file snapshot entries in `change_snapshot.txt`, current counterfactual specification, fixed v1 specification and referenced functions. Read the working contract and used `bmad-review-edge-case-hunter` path enumeration; revisited failure exits, selection/fallback, certificate/domain checks, and export ordering. No source edits. Existing successful artifacts are not invalidated by these findings.

## Findings

1. **P2 — failed re-search leaves a consumable old selection.** `calculate.py:144-146` writes an unresolved result and returns without invalidating or run-binding `selected.json`. `deliver.py:33` and `continuous.py:173` subsequently load that prior selection without checking the latest search outcome. A normal chained rerun can therefore replace the new unresolved result with a feasible label for an older run. Preserve old evidence under its run identity and write a current-run failure/selection manifest that downstream steps enforce.

2. **P2 — stale-certificate rejection happens after output mutation.** `deliver.py:56-63,77-78` overwrites `formula.json` and `path_controls.csv` before validating the certificate. A changed candidate or stale checker hash raises after these writes, leaving the old result/figures beside new controls. Validate before publishing and stage the bundle for atomic replacement; retain the previous complete bundle on failure.

3. **P2 — primary refinement bypasses the hard-feasibility filter.** `calculate.py:151` promotes a successful refinement solely on sampled operating margin, unlike the multistart and secondary branches, which also check `hard_min`. A refinement reported successful with a hard-constraint tolerance violation becomes `best`; if the secondary stage fails, line 155 selects that violating refinement and discards the feasible primary incumbent. Delivery then reports unresolved despite an available feasible fallback. Apply the same hard-feasibility predicate before incumbent replacement and keep the verified incumbent available.

## Verification

All probes ran through the existing project `.venv`, with temporary output directories and in-memory `unittest.mock` substitutions only; canonical sources/artifacts were untouched.

- Forced all four search starts to fail: new result was `unresolved`, while previous `selected.json` remained byte-identical and consumable.
- Ran the real delivery path against a copied certificate with a stale checker hash: raised `stale or substituted certificate: checker_source_sha256`, **after** writing the new formula and CSV; sentinel old result remained.
- Injected successful refinement with higher margin and `hard_min=-1e-5`, followed by secondary failure: selected record retained `hard_min=-1e-5` instead of the feasible incumbent.

No additional demonstrated interval-proof or current candidate-control defect was found. This review did not rerun the full continuous certificate or establish global/secondary optimality.
