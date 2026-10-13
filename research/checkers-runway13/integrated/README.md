# Historical integration work package

Start with [REPORT.md](REPORT.md). **Incomplete: no historical clearance or closed-form optimum.** Scope: [SPEC.md](SPEC.md); full audit: [TRACEABILITY.md](TRACEABILITY.md); binding request: [HANDOFF_TASK.md](HANDOFF_TASK.md). Project state lives only in `../PROJECT_STATE.md`.

## Reproduce implemented checks

From the canonical research root:

```sh
geospatial/.venv/bin/python -m unittest discover -s integrated -p 'test_*.py' -v
geospatial/.venv/bin/python integrated/check_printed_grid.py
geospatial/.venv/bin/python integrated/check_runway_registration.py
geospatial/.venv/bin/python integrated/check_mapped_axis.py
geospatial/.venv/bin/python integrated/derive_mapped_runway.py
geospatial/.venv/bin/python integrated/digitize_hill.py
geospatial/.venv/bin/python integrated/build_source_ledger.py
geospatial/.venv/bin/python integrated/build_scene.py
geospatial/.venv/bin/python integrated/evaluate.py --output integrated/evaluation.json
```

The last command **must exit 2**, reporting the unresolved historical integration gate. This is not a solver failure or an infeasibility theorem. `check_segments` in `evaluate.py` evaluates supplied geometry and all-time pose intervals; it cannot infer pose, datum, contact or missing roofs.

The existing `geospatial/.venv` provides numerical/geospatial packages. Isolated additional dependencies in `integrated/python_deps` are ezdxf 1.4.4, mpmath 1.4.1, typing_extensions 4.16.0, pyparsing 3.3.3 and fonttools 4.66.1. Existing environments were not modified. PDF inspection used the existing `whitepaper/.venv` PyMuPDF. Scripts rely on locally acquired historical files; acquisition does not imply redistribution permission.

## Artifacts

- `source_manifest.json`: 13 frozen baseline hashes. `primary_source_manifest.json` and `source_observations.json`: 28 primary observations and applicability limits.
- `geometry/`: source features, pixel picks, conditional static aircraft box, rejected tighter shape, diagnostic registrations, printed-grid check and additional hill observations.
- `registration.json`, `conditions.json`, `physical_parameters.json`: known values, labelled scenarios and explicit nulls.
- `clearance.py`, `frames.py`, `evaluate.py`: continuous geometry and frame primitives. Historical acceptance remains unavailable.
- `derivations/`: proved prerequisite identities and identification/sequence gaps, not a full optimality derivation.
- `evidence_gates.png/pdf`, `geometry/airframe_envelope.png/pdf`: exported inspection figures with limitations.
- `verification.json`, `artifact_manifest.json`: verification receipt and hashes. No independent peer review or peer-machine delivery is claimed.

`geospatial/.venv/bin/python integrated/verify.py` runs the producer replay, compares deterministic outputs, checks inherited hashes, tests the expected blocked path and writes the verification/manifest files. Successful verification does not mean the scientific goal is complete.

## Endpoint/datum continuation

[Follow-up report](followup/REPORT.md) records the endpoint-semantic hypothesis, bearing-free residual bound and newly identified HKPD-controlled accident survey. Reproduce the additive diagnostics (no inherited producers rerun):

```sh
geospatial/.venv/bin/python integrated/followup/diagnose_threshold.py
geospatial/.venv/bin/python -m unittest discover -s integrated/followup -p 'test_*.py' -v
```

The source-backed61mextension hypothesis is not an accepted frame or extra usable runway. The original36-test receipt remains historical; the follow-up has7newtests and a separate verification receipt. All scientific gaps and publication exclusions persist.
