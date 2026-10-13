# Version 2 claim audit

All paths below are relative to the wider `checkers-runway13` project and have frozen snapshots under this draft's `evidence/` directory unless noted.

| Manuscript claim | Source | Permitted interpretation |
|---|---|---|
| 47-degree magnetic offset; 2,786 m LDA | `evidence/EVIDENCE_REPORT.md`; CAD §§1.8–1.10 | Dated historical procedure/runway information; not arbitrary-wind heading change |
| 227 survey archives; 48 full aerial frames | `reconstruction/chronology/REPORT.md` | Acquired sources, not complete historical obstacle geometry |
| 171,307 dense points; 3,780 within control hull | stereo reports and verification | Filtered image-derived surfaces; local support only |
| Relative roof features 10.77 / 19.20 m | sparse stereo report and README | Conditional relative-plane estimates; not HKPD or complete accuracy bounds |
| Horizontal stereo holdout RMS 5.754 m | sparse stereo report | Particular local-control check; not vertical uncertainty |
| Candidate minimum margin at least 0.0397 | `analytical/coupled/continuous_certificate_refined.json`; `RESULTS.md` | Existing computer-assisted certificate for exact-decimal synthetic nominal model |
| Stop 2,531.32 m; remaining 254.68 m | `approximation/reference_outcomes.json` | Deterministic scenario outputs, freshly recomputed for draft |
| Finite-family optimum below 0.1559772 | `analytical/coupled/RESULTS.md` | Necessary upper bound; no near-optimality or historical clearance claim |
| Existence in finite family | `analytical/coupled/RESULTS.md` | Attainment conditional on source regularity lemma and fixed domain; no identified optimizer |
| Speed/delay stopping derivatives | Direct derivatives of frozen stopping law | Local conditional model sensitivities, not empirically estimated effects |
| 8,285 below / 17 tied / 58 above 10.8 m/s | NOAA CSV and verification | Declared 8,360-record routine subset; correlated selected records, not landing population |
| No physical prediction interval | `approximation/reference_outcomes.json`, uncertainty nulls | Preserved explicit absence, not a statement that future identification is impossible |
| Historical touchdown diagnostic: −161.52 m under fixed law | Settled CAL605 `analysis.json` and CAD §2.6.5 | Conditional model substitution, not historical path superiority |
| Required braking rises as reported speed falls | CAD §§2.2.5–2.2.7; `analysis.json` | Four rounded source landmarks; diagnostic, not measured continuous deceleration |

## New v2 claims

| Claim | Frozen source | Interpretation |
|---|---|---|
| Touchdown 302.114 m; stop 2233.231 m; remaining 552.769 m | `counterfactual/result.json`, `formula.json`, `path_controls.csv` | Fixed steady-wind scenario, synthetic entry/corridor, unchanged braking |
| Constant wind [-4.87659, 9.64007, 0] m/s | `counterfactual/inputs.json`; CAD chart convention | 21 kt FROM 070 true; 133°10′ chart-based runway axis, not recovered aircraft-local gusts |
| All-time margin ≥0.1507934696816132 | `counterfactual/continuous_check.json` | Own wind-aware real-decimal certificate, 376 closed intervals |
| Upper 66656817/307536544 and gap ≤0.0659509085084467 | `counterfactual/result.json`; direct rational derivation | Loose necessary finite-family bound; not near-optimality |
| Final workflow checks | `counterfactual/reviews/DISPOSITION.md`, `parent_final_verification.json` | 37 tests; all known lifecycle findings repaired; scientific gaps retained |
| 298.090 m greater remainder | Independent subtraction and stopping decomposition | Two differing scenario outputs, not causal wind effect or historical improvement |
| 404+531 dated assignments; 397 overlaps | `reconstruction/block_matching/road_cell_parent_verification.json` | Geometry/matching candidates, not accepted building identity or exact 1993 presence |

## Claims excluded

- Global near-optimality, including withdrawn bound 0.03972.
- Historical obstacle clearance from the empty-obstacle synthetic result.
- Independent vertical accuracy from a reprojection residual or a ground-plane fit.
- New control-theory novelty from using a new airport case.
- An accident-prevention effect, population accident probability or typical-flight result.
- A completed condition-to-policy map or gust-rejecting controller.
- External adoption, specialist endorsement or completed peer review. Public GitHub release is authorized, but is not evidence of any of those claims.

## Unfinished sections retained in scope

Complete georeferenced historical flight/model confrontation; terrain-aware solve; condition-dependent explicit approximation; calibrated uncertainty; equivalent-conditions improvement comparison; go-around/causal-policy robustness in the wider study. The revised manuscript describes the questions and evidence gates without invented findings or placeholder numbers.

## Review boundary

The drafting pass checked claim-to-source consistency, figure inputs, scalar calculations, formulas' endpoint identities, references and document rendering. It did **not** conduct a new independent audit of the entire aircraft model, interval arithmetic implementation, photogrammetric pipeline or published control literature. The PDF states that boundary.
