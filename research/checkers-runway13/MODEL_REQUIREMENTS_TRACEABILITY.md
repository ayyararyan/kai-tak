# Requirement coverage

13 October 2026. Implementation status and full-study status are separate. IDs prefixed `MODEL/` belong to executable specification v1; `STUDY/` preserve the earlier research draft. A completed code task does not remove a study dependency.

| ID | Requirement | Status | Evidence / limitation |
|---|---|---|---|
| MODEL/DATA-01 | Parameter provenance and fixed baseline | Implemented | model/config.json; estimated mass qualifier and source categories verified |
| MODEL/STATE-01 | Constrained flight, flare and stop | Implemented | model/trajectory.py; complete scenario sequence, calibrated physics absent |
| MODEL/OPT-01 | Lexicographic margin/effort optimization | Implemented | model/solve.py; both stages succeed and dense eta retention passes |
| MODEL/VAL-01 | Model and negative-path tests | Implemented | 52 pytest cases pass; model/test_model.py and review regression suites |
| MODEL/VAL-02 | Independent replay, denser samples and stresses | Implemented | outputs/scenario/optimization_replay.json; stress violations preserved |
| MODEL/OUT-01 | CSV, JSON, figure, README, dependencies | Implemented | Six run artifacts; 29 artifact checks pass; dependency lock supplied |
| MODEL/OPS-01 | State, changelog, traceability and validation | Implemented | MODEL_VALIDATION_REPORT.md and PROJECT_STATE.md reconciled |
| STUDY/MATH-01 | Finite-roll analytical benchmark | Implemented | Proof and six cases rerun; conditional heading bound only |
| STUDY/MATH-02 | Position/heading/speed/descent/bank with force feasibility | Partially implemented | Reduced scenario model implemented and tested; calibration unavailable |
| STUDY/MATH-03 | Terminal recoverability inner/outer bounds | Not implemented | Sample-feasible numerical paths are not universal certificates |
| STUDY/MATH-04 | Historical terrain, uncertain wind, information and go-around | Blocked | Historical geometry/calibration missing; robust policy and recovery set absent |
| STUDY/DATA-01 | Dated procedure geometry | Partially implemented | Primary chart and relative courses/LDA verified; no surveyed obstacle/corridor model |
| STUDY/DATA-02 | Routine-flight raw numerical records and rights | Blocked | Not acquired; custodian requests unsent |
| STUDY/VAL-01 | Uncertainty-aware CAL605 digitization | Not implemented | Published recorder plots available, not yet digitized |
| STUDY/VAL-02 | Held-out historical consistency checks | Blocked | Historical numerical records/calibration missing |
| STUDY/OPT-01 | Historical baseline, common feasible set and objective | Partially implemented | Executable synthetic baseline fixed; historical baseline not identified |
| STUDY/OPT-02 | Independently verified better historical-condition path | Blocked | Synthetic objective improvement cannot establish historical improvement |
| STUDY/OPT-03 | Robustness/tracking burden and go-around | Not implemented | Steady-wind diagnostics are not causal-policy robustness or recovery |
| STUDY/OPT-04 | Separate modern-guidance/route-redesign arm | Implemented | Interpretation rule retained; no such comparison run |

No missing requirement is marked complete merely because it is difficult or data-dependent.

## Analytical continuation, 13 October 2026

These rows add the expanded analytical request without changing executable v1.

| ID | Requirement | Status | Evidence / limitation |
|---|---|---|---|
| ANALYTIC/MATCH-01 | Finite-roll position matching and proof | Implemented | analytical/FINITE_ROLL_POSITION.md and independent review; implicit equations within restricted family |
| ANALYTIC/PATH-01 | Coupled complete candidate, approach through stop | Implemented | analytical/coupled/continuous_certificate_refined.json; unchanged aircraft/braking/model |
| ANALYTIC/FEAS-01 | All-time candidate feasibility | Implemented | Outward-rounded interval certificate, 2502 closed intervals; margin >=0.0397; nominal real-decimal family only |
| ANALYTIC/EXIST-01 | Existence versus nonexistence | Partially implemented | Compactness/regularity proof of attainment in finite polynomial family; unrestricted control problem not covered |
| ANALYTIC/OPT-01 | Global primary optimum and optimal parameter formula | Partially implemented | Certified lower 0.0397 and strict family upper 0.1559772; bounds do not match, optimizer not identified |
| ANALYTIC/OPT-02 | Global secondary minimum at retained optimum | Not implemented | Existence proof only; local secondary search does not establish the unknown global primary threshold |
| ANALYTIC/OPT-03 | Unrestricted full landing optimum / closed-form policy | Not implemented | No theorem equating unrestricted controls with the polynomial family |
| ANALYTIC/VAL-01 | Independent proof audit of new coupled results | Not implemented | Parent verification and replay passed; earlier independent audit does not cover these new results |
