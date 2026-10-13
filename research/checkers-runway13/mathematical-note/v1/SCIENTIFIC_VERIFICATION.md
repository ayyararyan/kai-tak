# Scientific verification

## Verdict and scope

The note establishes the four stated local theorems for the declared A1 model: unique root in the exact box, strict five-variable primary sufficiency, continuous-time feasibility, and non-strict twelve-parameter local transfer. Analytical necessary bounds and the global-family exclusion remain unmatched. Secondary retention is certified; effort optimality is not.

Source freeze: `78a9ce1c627f917c94306af5529d5e9ebeb743e8`. All prior repository artifacts are preserved. No optimizer, new model assumption, public push or release change was used for this task.

## What was independently reconstructed

- The CG/virtual-reference transformation, polynomial endpoint identities, moving-basis force/rate equations, conservative body/gear/obstacle predicates and hybrid stopping law.
- Monotonic stopping-speed restriction, terminal branches/quartic sign selection, exact 69 m/s floor regime and distinction between relaxed and attainable optima.
- Exact-rational polynomial derivative bounds, force regularity and compact-family attainment with the canonical **nonnegative** forward-speed hard condition.
- Airspeed/ground-speed coupling, drag convexity, mandatory gate-thrust ramp and the energy inequality used in the family exclusion.
- Exact-decimal Krawczyk contraction, residual/Neumann simplex validation and uniform first-order decrease plus Taylor remainder.
- Whole-time proof from stationary/endpoint neighborhoods plus a gap-free cover; factorized contact; the approach-independent necessary-constraint transfer.
- Correct upper-primary/lower-secondary retention comparison and parameter-AD mean-value feasibility proof.

These are actual independent mathematical derivations and source-code reviews. They are not claimed as formal proof-assistant verification or human aerospace peer review.

## Fresh executable evidence

The accepted read-only run is in `verification/accepted/run.json`; exact matrices are in `verification/final/local_matrices.json`.

| Check | Actual result |
|---|---|
| Public tests | 102 numerical/core/proof +15 geometry =117 passed |
| Unavailable-source exclusions | 5 restricted historical-source tests and2 original-workspace tests, not passes |
| Root/simplex/events | Freshly reproduced; exact stored root offsets and multiplier strings match |
| Root path | 398 accepted cells (32 approach,366 flare),786 processed |
| Secondary retention | Freshly certified at upper root endpoint−0.0001;4020 processed cells |
| Family exclusion | All4096 cells excluded at0.181970215; displayed residual0.9678323903412959m |
| Wind domains | All3 closed parameter intervals passed |
| Accepted condition paths | All10 whole-time certificates and independent numerical replays passed |
| Legacy synthetic witnesses | Both separately reproduced; calm2502 accepted cells, wind376 |
| Finite-object export | Full Jacobians, preconditioners, residuals and exact binary endpoints exported and checked |
| Independent stronger positivity diagnostic | All398 root-path cells have forward-speed lower bounds>45m/s |

The matrix exporter verifies safe directed bounds root norm<2e−14, K-offset<2e−34, simplex norm<2.5e−14 and every multiplier>0.0009658. The original sharper displays and directed endpoint audit support the narrower summaries printed in the paper. The analytical reviewer separately checked every family-exclusion residual>.9678m with exact decimal comparison.

## Discovered failures and repairs

1. **Sealed derivation prose:** touchdown slew called negative. Code, saved sign vector and independent interval evaluation show positive. Corrected in manuscript/audit; original untouched.
2. **Publication-ledger integrity:** old checker expects the pre-V5 complete ledger. Current public main contains legitimate appendages. New additive verifier checks historical exact prefix plus current pinned hash; original failure retained.
3. **Transient snapshot construction:** first closure omitted legacy manifest dependencies, causing real FileNotFoundError test failures. Expanded the public pinned closure, preserved failure logs, reran unchanged tests successfully. No missing test was relabelled a pass.
4. **Cache-sensitive old integrity check:** shared-source imports created untracked bytecode. Clean snapshot plus PYTHONDONTWRITEBYTECODE=1 avoids changes; original caches were not deleted to manufacture a pass.
5. **Draft corrections:** forward condition≥0 restored to canonical meaning; exact binary64 corridor cloud distinguished from ideal analytic samples; root vector renamed to avoid altitude ambiguity; endpoint derivative notation and unused smooth-envelope implication corrected. Independent review checked the repairs.

## Limits

No global primary optimizer, global or local secondary-effort minimum, full-class local optimum, unique12D path, quantified local-optimality radius, rigorously enclosed sensitivity number, broad active-regime partition or feedback/gust policy is proved. Tailwind5kt/urban60m/urban65m remain unresolved. Historical source restrictions remain genuine exclusions. Root/geometry results are conditional on A1, not calibrated aircraft accuracy.
