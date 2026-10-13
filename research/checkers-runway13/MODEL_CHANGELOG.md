# Model changelog

## 2026-10-13 — v1 baseline and implementation authorization

Aryan requested: “fix the aircraft, landing target and optimization objective, then build the constrained trajectory model.” This delegates baseline selection; it does not grant historical facts or operational authorization.

- Selected the documented CAL605 747-409B configuration: flaps 30, gear down, four PW4056, published estimated landing mass converted from pounds. Aircraft dynamics remain reduced-order and uncalibrated.
- Fixed threshold capture, flare, touchdown and full stop as the landing target. Pre-flare capture alone is not reported as a full landing.
- Selected dimensionless nominal minimum constraint slack, then control effort, for executable scenario optimization. This differs explicitly from the eventual universal gust-tolerance objective; the latter remains open rather than being claimed implemented.
- Wrote scenario initial state, tolerances, force/rate envelope, synthetic corridor and braking assumptions before implementation. No historical geometry or performance value is fabricated to fill missing evidence.
- Preserved all three research aims and unavailable historical-data/calibration/go-around/robust-policy requirements.
- Canonical executable specification: MODEL_IMPLEMENTATION_SPEC.md. Earlier PROJECT_SPEC_DRAFT.md remains the research-scoping record.
- No public repository, outreach, publication or operational aircraft guidance authorized or performed.

## 2026-10-13 — review repairs and verified closure

Accepted review defects repaired without loosening physical limits. Added phase-side rate handling, exact straight-rollout obstacle checks, full replay-state constraints, nonfinite/domain gates, conservative boundary status, custom-wind perturbations and dynamic dense meshes. Source-estimated mass remains qualified. Default local solver cap increased to 600; secondary solver-grid eta loss budget tightened to 5e-5 to satisfy 1e-4 dense retention. All 52 tests and 29 artifact checks pass. Final scenario result differs from the pre-review run; both evidence records retained. Full study incomplete.

## 2026-10-13 — analytical-first research instruction

Aryan asks to try deriving an exact analytical/closed-form optimum, grounded in historical terrain and procedures. New research brief preserves that objective. Numerical v1 is unchanged and becomes supporting verification. Reduced minimum-bank/path-length theorems must identify their restricted family and cannot replace the full landing/nominal-margin problem. Historical source acquisition and analytical tractability investigation are active; a full solution is not claimed.

## 2026-10-13 — analytical investigation handoff

ANALYTICAL_FINDINGS.md reconciles exact restricted-family geometry, altitude-coupled cubic optimum, parent checks and independent proof review. Synthetic verification passed 80 cases plus boundary/descent checks; full analytical landing remains incomplete. Reconstruction report and inventory document retrieved official sources and datum mismatch, not completed terrain. All 29 acquisition-artifact checksums verified; raw routine-flight acquisition remains unresolved. Preserved numerical v1 unchanged. Review qualifications accepted without changing model meaning. No historical superiority, novelty, global full-model optimality or operational safety claimed.

## 2026-10-13 — coupled candidate and all-time certificate

Latest explicit request: jointly construct approach/flare/speed choices with fixed
braking, then derive the required proofs. Added analytical/coupled/ without changing
numerical v1 sources/config, model meaning or constraints. Exact-rate local search
and a real-decimal witness produced; all-time interval certificate proves margin
>=0.0397, including both join sides and exact stopping. Compactness/regularity
establishes optimizer existence in the finite family, not its identity.
Valid necessary scalar family upper bound is 0.1559772. Global interval searches
with a corridor-bound-direction error and a library atan2 branch-cut defect were
invalidated and retained; tight upper-bound claims from those runs withdrawn.
Branch-safe rerun leaves 7,071 unresolved boxes after 15,000 checks at eta=0.10.
Fresh feasible-witness certificate, 180 point/enclosure comparisons, 24 endpoint
identities, 130 ancestor-box negative controls, five rejection/regression cases
and forward replay pass. Exact global primary/secondary and unrestricted solution
remain incomplete. No publication, operational use or background monitor.
