# Historical Reconstruction and Flight Mathematics

[Home](../README.md) · [Research map](../docs/RESEARCH_MAP.md) · [Current status](../docs/PROJECT_STATUS.md) · [Reproduce](../docs/REPRODUCIBILITY.md)

The laboratory is the scientific foundation of the paper, archive and atlas.
Start with the object you want to investigate, not the chronology of past runs.

| Question | Canonical starting point | State |
|---|---|---|
| What exactly is the accepted scenario model? | [Specification](checkers-runway13/MODEL_IMPLEMENTATION_SPEC.md), [model guide](checkers-runway13/README.md) | Implemented and tested within declared scenario assumptions |
| Which mathematical results are established? | [Foundations](checkers-runway13/foundations/MATHEMATICAL_FOUNDATIONS.md), [coupled results](checkers-runway13/analytical/coupled/RESULTS.md) | Restricted identities, feasible witness, bounded finite family; invalid exclusions retained |
| How explicit is the landing formula? | [Approximation status](checkers-runway13/approximation/STATUS.md) | Implemented nominal reference; historical requirements remain blocked |
| What changes in the declared wind scenario? | [Counterfactual report](checkers-runway13/counterfactual/REPORT.md) | Separate certified fixed-model witness, not causal identification |
| What is now proved under explicit geometry and aircraft assumptions? | [Local certificate](checkers-runway13/integrated/assumption_solution/refinement/local_certificate/REPORT.md), [public reproduction](../publication/scientific-results-20261013/README.md) | Strict local five-variable / non-strict local twelve-parameter primary optimum; global and historical claims remain unresolved |
| What do recorder and weather sources show? | [CAL605 evidence](checkers-runway13/evidence/cal605_reconstruction/REPORT.md) | Source-dependent observations and uncertainty |
| What can dated maps and aerials establish? | [Chronology](checkers-runway13/reconstruction/chronology/REPORT.md), [block matching](checkers-runway13/reconstruction/block_matching/REPORT.md) | Acquired evidence and partial conditional reconstruction |
| Are historical obstacle volumes known? | [Obstacle report](checkers-runway13/reconstruction/obstacles/REPORT.md) | Incomplete; mapped readings are not complete clearance solids |
| What modern geography is available? | [Geospatial guide](checkers-runway13/geospatial/README.md) | Separately dated modern comparison, not 1993 geometry |
| Can these be integrated into historical clearance? | [Integration](checkers-runway13/integrated/REPORT.md), [traceability](checkers-runway13/integrated/TRACEABILITY.md) | Blocked on explicit evidence/calibration dependencies |
| What is the contribution relative to prior work? | [Literature and comparison](checkers-runway13/literature/LITERATURE_AND_COMPARISON.md) | Source-bound assessment, not an endorsement |

## Working states

Accepted references are identified by their specification, configuration, certificate
and validation receipt. Active or incomplete investigations retain their own ledger.
Rejected registrations, invalidated dense blends, failed global-exclusion attempts
and earlier checkpoints are retained for diagnosis; their presence is not acceptance.

The [chronological project ledger](checkers-runway13/PROJECT_STATE.md) preserves
decisions. The [short current status](../docs/PROJECT_STATUS.md) is the cross-project
entry point. For manuscripts use the [publication index](../papers/README.md), not
the laboratory's working-history headings.

Before extending a subsystem, read its specification and tests, then follow
[ownership](../docs/OWNERSHIP.md) and [contribution rules](../docs/CONTRIBUTING.md).
