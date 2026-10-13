# Amendment A1 refinement traceability

This is an additive status supplement, not a replacement or reduction of SPEC_AMENDMENT A1. Historical requirements retain their prior status. The parent package is immutable.

| ID | Status | New evidence | Remaining |
|---|---|---|---|
| A-01 | Implemented | Parent source/assumption hashes preserved; no new inputs or changed assumptions | Historical source unknowns remain unknown |
| A-02 | Implemented | Same complete assumed scene and fixed geometry, verified unchanged | No empirical geometry claim |
| A-03 | Implemented | Unchanged CG/occupancy/contact model; two new complete path exports | Reduced pose/contact assumptions remain |
| A-04 | Partially implemented | 16 warm continuation stages, four dense target retries, two condition-boundary searches, two new continuously verified paths and local secondary stages | tailwind5/urban60/urban65 unresolved; no complete feasible-domain map |
| A-05 | Partially implemented | Stronger globally valid FAMILY energy bound, evaluated nine-equation active branch and sensitivity, explicit affine path with three all-parameter/all-time feasible domains | No matching global optimum; no validated exact active-root partition or global secondary proof; no full-class optimizer |
| A-06 | Implemented | Eight stronger continuous retention proofs, two new replay/retention certificates, interval parameter differentiation, 12 new tests and combined regression/integrity checks | Numerical local optimality distinguished from proof; failed enclosures retained |
| A-07 | Implemented | Additive report/derivation/formulas/CSV/evaluator/manifest; canonical ledger append and parent QA provenance | No publication |

Five implemented; two partial. Overall full analytical objective: **INCOMPLETE**. New tests do not close the optimality gaps.
