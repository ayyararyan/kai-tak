# Local certificate: primary optimality proved, global task still incomplete

Under unchanged assumption amendment A1, the actual baseline nine-equation
flare root now has a rigorous interval certificate. The former unverified
premises of the local sufficiency theorem are checked.

- **Exact root and regularity:** Krawczyk strict inclusion in a scaled-coordinate
  radius `1e-20` box; every enclosed Jacobian is nonsingular.
- **Local sufficiency:** all six active-gradient weights are rigorously positive;
  the augmented gradient matrix is nonsingular. This proves a **strict local
  primary optimum in the five flare variables**.
- **Whole-time feasibility:** stationary minima, endpoint slopes, omitted force
  constraints, hard whole-body geometry and complete approach/flare/stop are
  certified. This gives a **non-strict local primary optimum in the full
  12-parameter family**, not a unique approach path.
- **Local primary value:** `eta ≈ 0.15236076430186170192`. Safe global-family
  bracket: **[0.15236076430186170190, 0.181970215]**. The upper bound is inherited,
  not newly optimized or matched.
- **Secondary retention:** the unchanged delivered baseline secondary path has
  continuous loss ≤`1e-4` relative to this proved local primary optimum.
  Secondary-effort optimality remains numerical, not globally proved.

Rounded root path: touchdown **302.126 m** past the threshold, stop **2234.377 m**,
runway remaining **551.623 m**. These are conditional mathematical-model results.

## Evidence and reproducibility

`certificate.json` contains the exact decimal root center/radius, Krawczyk and
simplex enclosures, stationary-time checks, and the complete 398-cell time cover.
`retention_replay.json` contains the stronger secondary-retention proof and
independent numerical replay. Read [DERIVATION.md](DERIVATION.md) for the theorem
and precise scope, [README.md](README.md) for commands, and
[TRACEABILITY.md](TRACEABILITY.md) for unchanged requirement coverage.

**108 core/certificate tests pass, including 11 new tests; 16 geometry tests pass.**
The new tests freshly reproduce the root, simplex, extrema and all-time path
proof, and reject a displaced non-root and invalid boxes. The 69 refinement
artifacts and its manifest, 136 parent artifacts and its manifest, 397 prior
artifacts and 13 frozen inputs remain unchanged; overlaps give 610 unique
hash-preserved paths. Final receipt and manifest record these checks separately.

During implementation, scalar interval/jet dispatch and two diagnostic-test
conversion issues were repaired. The initial failed test log is retained; neither
failure invalidated a sealed artifact or supplied a proof premise. A decimal-vs-
binary time-boundary mismatch was identified in this new checker during audit and
fixed before the final certificate; final proof uses consistent decimal endpoints.

## What remains incomplete

**A-04 and A-05 remain partial.** No global optimizer, global secondary optimum,
complete active-regime partition, or full-class sufficiency theorem. The 5 kt
tailwind, 60 m urban and 65 m urban cases remain unresolved. No generic continuation
retries were performed. Historical certification remains false; feedback/gust,
go-around and physical calibration gaps are unchanged.

This closes the requested baseline local-proof gap, not the original full
analytical task. No acquisition, login, mail, publication, agents or peer sync.
