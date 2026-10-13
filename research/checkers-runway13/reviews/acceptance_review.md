# Independent acceptance audit

Reviewed 2026-10-13 against MODEL_IMPLEMENTATION_SPEC.md v1, after reading the full working agreement. Read-only review except this report. Snapshot and actual source reviewed; no source edits or additional agents. Findings refer to the pre-repair source at review time.

## Verdict

The default delivered candidate has credible sampled nominal feasibility evidence, but closeout is not yet complete. No fatal force-balance or default stop-distance error found. Three correctness/provenance details need repair, and OPS-01 remains unfinished. This is not historical feasibility, gust robustness, or operational safety evidence.

## Prioritized findings

### P2: phase-junction rate check substitutes a smoothed derivative for the actual one-sided rates

`model/trajectory.py:204` and `:205` fit a single cubic spline through both flight phases. Position is C2, not C3, at the threshold: jerk, and consequently bank/thrust rates, can have a jump. The spline invents a single intermediate derivative, which does not check either physical one-sided limit. Finite differentiation of each underlying polynomial at the delivered candidate's threshold gives bank rates -2.2850363 and 0 degrees/s, while the 1201-point global spline gives -0.2717157 degrees/s. Thrust-rate limits are likewise -15329.45 and -58947.48 N/s versus the reported -53744.20 N/s. This does not itself invalidate this candidate: these actual junction rates are below its limits, and the reported overall roll maximum is 3.5633 degrees/s. It is a general STATE-01/VAL-02 validator defect that finite-grid caveats do not remove. Check both phase endpoints separately using analytic derivatives or phase-local rate reconstruction; regress a binding one-sided limit.

### P2: configurable optimization mesh can be denser than its purported dense validation

`model/solve.py:100` fixes validation at 1201 points per phase; `:141` accepts an arbitrary optimization `--samples`. A valid `--samples 2401` run would be validated on fewer points than the optimization mesh. The same issue affects reported mesh comparison (`:120`) and the README's 10-times-denser claim. Choose a validation mesh strictly denser than the supplied optimization mesh, e.g. max(1201, 10*(n-1)+1), and propagate it consistently to sensitivity/output metadata. Default n=121 is not affected.

### P2: source-estimated mass is labeled observed without preserving the estimation qualifier

`model/config.json:13–17` labels the accident-report estimated landing mass `observed`, while the source string does not explain that it is an estimate. The exact pounds-to-kilograms conversion is correct; it cannot make the input mass exact or directly measured. Preserve machine-readable source-estimated status and describe `mass_kg` as a deterministic conversion of that estimate. The fixed scenario value need not change. Parent independently identified this provenance issue; I verified the affected config fields, not a fresh reading of the original CAD report.

### Closeout gap, not a runtime bug: OPS-01 missing final state/validation

`MODEL_VALIDATION_REPORT.md` is absent at audit time. `MODEL_REQUIREMENTS_TRACEABILITY.md` still says implementation is underway and tests/replay not implemented, despite existing verified artifacts. `PROJECT_STATE.md` likewise retains the pre-verification next step. Populate final evidence and accepted/rejected review dispositions before claiming completion. Do not mark broader STUDY requirements complete.

## Requirement-by-requirement acceptance

- DATA-01: all specified numerical choices and categories present; mass provenance qualifier needs repair.
- STATE-01: constant-wind inverse-force decomposition, density, finite lift/load/CL/thrust envelopes, C2 flight join, touchdown impulse, fixed delay and deceleration implemented. Rate checks need phase-junction repair above.
- OPT-01: sampled dimensionless minimum margin, hard altitude/forward-motion constraints, fixed baseline and corridor, secondary effort/eta-retention and honest unresolved status implemented. Default output records both solver stages succeeding. No global-optimality claim found.
- VAL-01: 27 tests passed freshly, including force balance, wind heading, C2/endpoints, stop calculation, invalid configurations, nonconstant wind rejection, historical gate, and negative force/obstacle/control-corruption cases.
- VAL-02: independent Newton replay genuinely recomputes forces from its own state; default dense check and four sensitivity cases produced. Rate-junction and configurable dense-mesh issues above prevent unqualified acceptance.
- OUT-01: CSV/JSON/PNG/provenance/manifest, README and dependency lock present. Fresh checksum and CSV semantic checks passed. Plot-generating code inspected; no fresh visual-image review in this lane.
- OPS-01: partially implemented; final audit/state artifacts need update.

## Fresh numerical/output evidence

Using current `.venv`, `python -m pytest model/test_model.py -q`: **27 passed**. Independently recomputed candidate diagnostics from its stored decisions. Manifest hashes and source hashes all match. Both CSVs contain approach, flare and rollout, strictly increasing time and a final zero speed; each has 2502 rows. Historical artifact says `blocked`; intentional search-failure artifact says `unresolved`.

Delivered candidate: eta 0.0270552992; no dense nominal violations; threshold-to-touchdown sequence ends at x=394.53037 m; stop x=2564.57449 m, leaving 221.42551 m of runway (71.42551 m beyond the required reserve). Maximum bank 13.29295 degrees; maximum sampled roll 3.56327 degrees/s; EAS 136.08221–153.00378 kt. Replay reports maximum position error 0.00015650 m, velocity error 0.00003159 m/s and stop error 0.00031401 m, with terminal/stop checks passing. These output values are pre-repair and must be refreshed after numerical changes.

Baseline stops at 2669.29914 m, exceeding the usable 2636 m stop bound; successful replay of that baseline is correctly distinct from feasibility. Four fixed-path sensitivity records exist: +5 m/s crosswind eta 0.02710, -5 m/s crosswind eta -0.05478, +5% mass eta 0.00690, 10% weaker braking eta -0.05788. Replay fidelity passing in all four cases does not make the two negative-margin cases feasible.

Six-case finite-roll artifact was inspected and records passed; I did not rerun its writer under this read-only scope. No full optimizer rerun performed in this bounded lane.

## Explicitly not bugs or grounds to rewrite the model

The uncalibrated 747 force envelope, exponential density, 400 m synthetic corridor, fixed start, 50-ft gate, constant mass, touchdown gear-reference height, inelastic contact and 0.15g delayed braking are fixed scenario choices. They are not certified historical facts. Allowing a temporary climb is consistent with the current one-sided descent constraint; imposing monotonic descent would change the agreed feasible set. The deterministic eta objective is explicitly not universal gust tolerance. Wind-conditioned inverse controls are properly described as fixed-path diagnostics, not a common causal policy. Missing historical obstacles, routine-flight records, aircraft calibration, robust feedback synthesis and go-around viability remain open full-study requirements, not defects that can be patched by inventing inputs.
