# Reproduce the local certificate

Run from `.` with the
existing `.venv`; no installation or network access is needed.

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python integrated/assumption_solution/refinement/local_certificate/validate.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python integrated/assumption_solution/refinement/local_certificate/retention_replay.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q -p no:cacheprovider integrated/assumption_solution/refinement/local_certificate/test_local_certificate.py
.venv/bin/python integrated/assumption_solution/refinement/local_certificate/verify.py
```

The first two commands regenerate **only local_certificate receipts** and will
invalidate this directory's current manifest. Copy this additive directory first
while preserving its relative layout if forensic byte preservation is needed.
Do not run parent/refinement producers: their delivered files are sealed.
`verify.py` is read-only by default. `--seal` deliberately regenerates only this
additive directory's verification receipt and artifact manifest.

## Proof files

- `interval_root.py`: analytic interval dual/Taylor-jet engine and Krawczyk proof.
- `validate.py`: source preservation gate, simplex enclosure, stationary/endpoint
  extrema, all-time operating and hard geometry checks, exact rollout connection.
- `certificate.json`: authoritative root/feasibility proof. `root.center` and
  `root.radius` define X with decimal endpoints; displayed floats are not exact
  coordinate definitions. The seven fixed approach coordinates come from the
  sealed parent `active_branch.json` and are interpreted as real decimals.
- `retention_replay.py` / `retention_replay.json`: unchanged secondary path's
  retention relative to exact local primary; independent numerical center replay.
- `root_attempts.json`: preliminary wider-box Krawczyk experiments, not needed
  for the final smaller-box proof.
- `preserved_snapshot.json`: 610 distinct pre-existing hash/length bindings.
- `test_local_certificate.py`: algebraic AD, independent force comparisons,
  fresh proof reproduction, negative and preservation tests. Finite differences
  appear **only in diagnostic tests**, never as proof derivatives.
- `tests_initial_failure.log`: resolved diagnostic-conversion failures, retained.

Full suite used:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python -m pytest -q -p no:cacheprovider counterfactual/test_counterfactual.py integrated/test_integrated.py integrated/followup/test_diagnosis.py integrated/aircraft_followup/test_prerequisites.py integrated/assumption_solution/test_solution.py integrated/assumption_solution/refinement/test_refinement.py integrated/assumption_solution/refinement/local_certificate/test_local_certificate.py
geospatial/.venv/bin/python -m unittest integrated.test_frames_and_gate integrated.test_source_geometry
```

The proof is a validated numerical local theorem within the declared polynomial
family. It is not a closed-form global solution or a verified flight procedure.
