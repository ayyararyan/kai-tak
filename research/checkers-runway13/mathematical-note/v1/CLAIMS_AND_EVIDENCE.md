# Claims and evidence ledger

Complete machine-readable inventory: CLAIMS_AND_EVIDENCE.csv (20rows). Source paths are relative to research/checkers-runway13/integrated/assumption_solution unless otherwise stated. All are pinned by frozen-source/PUBLIC_SOURCE_MANIFEST.json.

For a stage in the ledger run `python scripts/verify_all.py --source-root frozen-source --output-dir verification/replay --stage STAGE`. Analytical implications are proved in the indicated manuscript sections, not inferred solely from test passes. Additional full matrix reproduction: `python verification/emit_matrices.py --source-root frozen-source --output verification/replay/local_matrices.json`.
