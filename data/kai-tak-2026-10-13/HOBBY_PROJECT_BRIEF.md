# Kai Tak: The Geometry of the Last Turn

## User direction — 2026-10-13
Aryan explicitly wants to pursue this kind of flight-mechanics/mathematical-control work as a serious hobby project. His supplied discussion explores analytical feasibility for the Checkerboard Turn, finite roll rates, descent, wind, obstacles, numerical control and later learning-based controllers. This is an exploratory direction, not approval of every assumption or a frozen implementation specification.

## Proposed deliverables
A reproducible simulation/analysis repository, a visual recoverability map and a technical note distinguishing established results, derived bounds and unverified novelty. No public repository, publication or institutional outreach is authorized yet.

## Recommended first milestone — proposed, not frozen
For a specified reduced aircraft model and terminal landing gate, construct a feasible/infeasible/unresolved map across entry speed, cross-track offset and altitude, fixing or explicitly conditioning on heading and initial bank. Include finite roll rate, bank limit and descent constraints. Begin with the supplied still-air circular construction as a regression benchmark; incorporate wind and obstacles in subsequent explicitly specified model stages. This is sequencing, not removal of the longer-term scope.

A verified admissible trajectory demonstrates model-relative feasibility. Failure of a local numerical solver does not prove impossibility. Use analytical outer bounds for exclusion and constructive inner bounds for feasibility; retain the gap as unresolved. With uncertain wind, distinguish a single feedback policy working for every allowed disturbance from a separately chosen trajectory for each known wind realization.

## Decisions before implementation
Aircraft/parameter envelope; coordinate frame and historical geometry; terminal gate vs touchdown; speed and descent dynamics; roll authority; time horizon; obstacle clearance and wind class. No aircraft type is selected merely because CAL605 used a 747-400. Operational limits and stall/load-factor constraints cannot be inferred solely from a bank cap.

## Data relationship
See README.md for verified acquisition state. BA raw QAR collection remains unlocated; full CAL605 report and plotted recorder extracts were recovered. Historical records can inform plausibility and validation but are not a prerequisite for model-relative analytical work. The accident plots are not successful expert demonstrations. Do not silently turn them into imitation-learning training data.

## Literature checked this turn
Wu and Chen, arXiv:2412.04797, abstract checked 2026-10-13: minimum-time Dubins planning in steady wind; four candidate families and nonlinear root solving for some families. https://arxiv.org/abs/2412.04797 . Full theorem assumptions and relevance to the proposed constrained model require review. No novelty claim established.

## Status
Project direction captured; no simulator or theorem implemented. Requests to BA, AAIA and FSF remain unsent. Next substantive step is a precise reduced-model specification and literature comparison, not an unsupported claim of a universal closed-form solution.

## Clarified question — 2026-10-13, 14:21 IST
Aryan's central question is comparative optimization: can an analytical/closed-form approach for the same aircraft and Kai Tak runway 13 improve on a defined historical approach and demonstrate its suboptimality? Recoverability mapping is a possible supporting method, not a replacement for this objective. Immediate request is to check possibility, not implement a controller.
A valid comparison must hold aircraft/configuration, initial state, terminal conditions, historical obstacle geometry and operational/information constraints fixed, or explicitly identify changed technology/constraints. One feasible strictly better solution proves a baseline suboptimal for the stated objective; global optimality and real-world safety require stronger evidence. Closed form is desirable, not itself an optimality certificate. Safety objective remains to be selected; proposed candidate is maximizing tolerable disturbance magnitude while maintaining constraints and a viable go-around option.
Literature refinement: Wu–Chen section 2 explicitly uses altitude-hold, constant airspeed and steady wind with terminal position/heading constraints; it is not a complete descending airliner landing solution.
