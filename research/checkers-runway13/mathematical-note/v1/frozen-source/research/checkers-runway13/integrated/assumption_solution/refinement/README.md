# Additive refinement package

Read REPORT.md then DERIVATION.md. Existing parent files are sealed and unchanged. All numerical strategies retain amendment A1 and original parameter bounds. Only this subdirectory and an append to the canonical project ledger are mutated.

From the project root, using the existing environment:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q -p no:cacheprovider counterfactual/test_counterfactual.py integrated/test_integrated.py integrated/followup/test_diagnosis.py integrated/aircraft_followup/test_prerequisites.py integrated/assumption_solution/test_solution.py integrated/assumption_solution/refinement/test_refinement.py
geospatial/.venv/bin/python -m unittest integrated.test_frames_and_gate integrated.test_source_geometry
.venv/bin/python integrated/assumption_solution/refinement/export_refinement.py --case urban58 --time 45 --side right
.venv/bin/python integrated/assumption_solution/refinement/verify_refinement.py
```

The evaluator returns one point of the selected complete hybrid path; it refuses extrapolation. At touchdown, `--side left` returns the airborne pre-impact state; the default right state applies the assumed ideal reset. Ground CL/thrust fields are null because the original ground law stipulates deceleration, not an aerodynamic ground-control synthesis.

## Producer sequence

`continue_cases.py` → `target_polish.py` and `critical_conditions.py`: nearest-path continuation and unresolved-case diagnostics. `verify_frontier.py` → `polish_frontier.py`: continuous verification, independent replay and local secondary stages. The pre-polish urban58 result is retained.

`strong_bound.py`: 4096-cell interval exclusion for the coupled energy/ramp relaxation. `active_branch.py`: evaluated local flare equations and derivatives. `box_certifier.py`/`parameter_taylor.py` → `verify_taylor_domain.py`: condition-domain feasibility. `retention_proof.py`: eight stronger certificates for unchanged original paths. `export_refinement.py`: additive formulas/CSV/evaluator.

Numerical producers write only this refinement directory, but rerunning them changes its current manifest. For forensic replay, copy this additive directory first, preserving its parent-relative position/import access. Never run the parent producers to regenerate sealed parent artifacts.

`verify_refinement.py` is read-only by default; `--write` creates a fresh local verification receipt only. Artifact manifest excludes itself and Python/test caches; it includes the verification receipt. The ledger is outside manifest scope because it is append-only canonical state. Source bindings, parent snapshot and prior/frozen hashes are checked independently.

The failed independent-box and wider-domain experiments/logs are evidence of unresolved enclosure attempts, not infeasibility. `box_certifier_initial.py` preserves the pre-interface-hardening version. The final accepted parameter certificates are **only** in `taylor_domain_refined.json`; `taylor_domain.json`, `branch_domain.json`, and `domain_probe.json` are unsuccessful earlier experiments. No global, historical, or feedback-policy solution is claimed.
