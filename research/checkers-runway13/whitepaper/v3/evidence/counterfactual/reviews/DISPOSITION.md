# Review disposition and final acceptance

13 October 2026. Three independent reviews: blind.md, edge.md, acceptance.md. Duplicates reconciled below. All findings concern implementation failure paths inside the existing specification; no model-meaning change or new approval was required.

| Finding | Classification | Decision / repair | Verification |
|---|---|---|---|
| Terminal and delivery gates disappear under Python -O | patch | Accept; replace runtime assertions with unconditional exceptions | Optimized-Python terminal rejection; inspected unconditional verifier gates |
| Failed or interrupted search leaves consumable stale selection | patch | Accept; run identity, state and selection hash gate; preserve archive | Failed/interrupted search regression; new completed run identity |
| Higher-margin refinement can violate hard constraints | patch | Accept; shared eligibility predicate preserves feasible incumbent | Injected bad-refinement/failing-secondary regression |
| Rejected or failed export partly overwrites old artifacts | patch | Accept; validate first, stage complete bundle, atomically switch pointer | Stale-certificate, generation-failure and bundle-switch regressions |

Related boundary checks: malformed real-decimal certificate inputs rejected, current search generation rechecked before delivery, no physical-confidence or historical-clearance inference. No remaining demonstrated blocker for this conditional case. Wider empirical and optimality gaps remain unresolved, not rejected or silently deferred.

Parent fresh evidence: 37 tests passed; verify_delivery.py completed two producer/replay reruns with byte-identical formula and controls; independently reproduced interval cover at the saved target; 20,001-point-per-phase dense check; all 22 manifest hashes matched; final plot visually inspected. Exact hashes and time in parent_final_verification.json. Successful source-bound numerical candidate unchanged by repair. No new scientific peer-review claim.
