# Independent review decisions — 13 October 2026

Three context-separated reviews examined the code. Reports are evidence to evaluate, not proof of correctness. All retained items below are implementation/reporting repairs within the fixed model; none changes the chosen aircraft, envelope, landing target or nominal objective.

| Finding | Decision | Reason / repair | Model-meaning change / approval |
|---|---|---|---|
| Narrow runway obstacle missed by fixed rollout samples | Accept | Exact minimum distance across the straight ground segment; airborne checks still explicitly sampled | No / not needed |
| Wind stress replaces nominal headwind/vertical wind | Accept | Add/subtract 5 m/s only in nominal crosswind component; label modified parameter scenario-based | No / not needed |
| Validation can be coarser than custom solver mesh | Accept | At least 10x intervals, minimum 1201 points per phase | No / not needed |
| Phase-join spline averages one-sided control derivatives | Accept | Piecewise derivatives with adverse one-sided join value; retain finite-grid limitations | No / not needed |
| NaN margin can evade feasibility flag | Accept | Nonfinite diagnostics fail closed | No / not needed |
| Nonphysical flight-path angles accepted | Accept | Reject out-of-domain angles instead of silently changing endpoint | No / not needed |
| Numerical residual at zero-sink endpoint mislabelled as physical violation | Accept | Distinguish boundary-unresolved from passed or clearly violated; no relaxed physical constraints | No / not needed |
| Replay checks closeness but not all path inequalities | Parent audit: accept | Re-evaluate operating/hard constraints from independently integrated state and forces | No / not needed |
| Estimated source mass labelled observed without qualifier | Accept | Preserve source-estimation uncertainty through exact unit conversion | No / not needed |
| Missing final validation/traceability closeout | Accept | Parent completes reports after repaired run | No / not needed |
| Initial candidate includes a brief climb | Record limitation | Fixed model only bounds maximum descent; no monotone-descent constraint was specified. Do not silently change feasible set | Changing this requires a new model decision |

Pre-review source snapshots and outputs retained under reviews/ and outputs/scenario-pre-review/. They are superseded numerical evidence, not the authoritative final run. The pre-review saved 19/19 artifact checks did not cover the newly exposed edge cases.
