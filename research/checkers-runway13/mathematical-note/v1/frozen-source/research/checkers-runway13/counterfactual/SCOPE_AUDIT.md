# Counterfactual landing: full-scope audit

13 October 2026. Latest instruction: calculate the landing that should have happened. Accident reconstruction alone is not the requested object. This continuation calculates a new complete candidate, conditional on evidence-labelled assumptions, while retaining the outstanding historical requirements.

## Unchanged decision object

Primary: maximize minimum normalized operating margin across approach, flare and stop. Secondary: minimize integrated squared normalized control demands while retaining primary margin within 1e-4. Not minimum landing time, minimum stopping distance, imitation of CAL605, or a newly chosen strongest-braking strategy.

Aircraft configuration and physical/scenario envelope remain fixed. Scene and state uncertainty cannot be removed by making an optimizer run.

## Requirement reconciliation

| Existing requirement | Present evidence | Counterfactual work / unresolved dependency |
|---|---|---|
| Complete approach, flare and stop | Nominal calm candidate exists | Newly optimize a mean-wind case and export full reference/controls. |
| Actual historical entry state | Selected recorder graphs, not registered full state | Synthetic initial position remains explicit; no historical same-state improvement claim. |
| Dated obstacle geometry | Latest stereo handoff is local relative-height reconstruction | No absolute runway/datum or comprehensive obstacle scene. Historical clearance remains blocked. |
| Whole-aircraft/tracking clearance | No calibrated swept-volume/tracking tube | Point mass cannot certify actual aircraft clearance. |
| Wind conditions | CAD 070 true / 21 kt; NOAA 070 true /10.8 m/s | Declared constant mean scenario, not actual time-varying aircraft-local wind. Chart 1990 variation remains scenario conversion. |
| Aircraft/braking calibration | Report identifies type/config/mass; simplified envelope | Preserve .15g and 2 s; no unapproved stronger brake assumption. Physical applicability unresolved. |
| Explicit solution | Existing endpoint-constrained polynomial family | Export newly calculated case coefficients; a single case is not the full condition-to-coefficient map. |
| Feasibility and numerical bounds | Exact-rate/replay/interval machinery available | Fresh wind-aware validation required. No zero-wind certificate transfer. |
| Near-optimality | Prior calm upper bounds only | Multistart search not global proof. A wind-valid necessary upper bound, if derived, must identify its domain and achieved gap. |
| Prediction intervals | No physical input/model/tracking error calibration | Null coverage and physical CI/PI, not invented distributions. |
| Go-around viability / causal controller | Not implemented or calibrated | Cannot conclude landing was preferable to go-around or prescribe a robust executable pilot procedure. |
| Historical improvement | Actual report says touchdown was recoverable | No claim actual turn/touchdown caused overrun or proposed path would have prevented accident. |

## Completion rule

The conditional calculation may pass all its numeric checks while the requested historical solution remains incomplete. Report both. Conditional means a precisely stated computable case, not permission to omit terrain or uncertainty from the full agreed goal.

## Sources inspected

Original model and approximation specifications; original model/evaluator and exact polynomial/rate evaluator; nominal interval checker; historical evidence report and chart; NOAA event-day metadata; `reconstruction/block_matching/HANDOFF.json` generated 13:41 UTC, reporting local relative-height geometry, null hard-height intervals, unreconciled absolute datum and clearance_certified=false.

No source model, terrain, or reconstruction artifact is modified by this audit.


## Conditional calculation closure — 13 October 2026

| ID | Status | Implementation / output | Acceptance evidence |
|---|---|---|---|
| INPUT-01 | Implemented | inputs.json; this audit | Frozen source/config/reference-cloud identities checked |
| SOLVE-01 | Implemented | calculate.py; selected.json; search_checkpoint.json | Four deterministic primary starts, refinement and secondary stage; all six successful |
| OUT-01 | Implemented | formula.json; path_controls.csv; result.json; landing.png/pdf | Coefficient reconstruction, full stop, visual inspection and two identical numeric exports |
| VAL-01 | Implemented | test_counterfactual.py; verification.json | 37 passing tests; independent replay; source tampering and failed-search rejection |
| CERT-01 | Implemented | continuous.py; continuous_check.json | Parent reproduced all 376 interval boxes; model-only lower bound 0.1507934696816132 |
| OUT-02 | Implemented | REPORT.md; parent project-state append | Three independent reviews, repaired failure paths, current verification and explicit wider gaps |

Conditional case: 6/6 implemented and verified; no unapproved scope reductions or proxy substitutions. Full historical/uncertainty solution: INCOMPLETE. The valid terminal-relaxation upper bound is 66656817/307536544; the resulting gap is too loose to claim near-optimality. The 20,001-point parent check is supplementary numerical evidence, not a substitute for the interval proof. Full ledger above and the approximation specification retain every outstanding requirement.
