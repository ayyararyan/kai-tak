# Checkers with Runway 13

Updated: 2026-10-13. Canonical project ledger; working title selected from Aryan's two suggestions, not a final naming decision. Latest approximation handoff reconciliation is recorded at the end of this ledger; earlier awaiting-handoff entries are historical.

## Authorized objective

Serious hobby project with a possible public project/white-paper output. Aryan explicitly authorized a few agents to investigate what can be assembled and to start the project.

Preserve the three aims in this sequence:
1. Derive landing-feasibility and optimality bounds for Kai Tak runway 13, using historical evidence and applied mathematics.
2. Assess whether actual historical flight paths are consistent with the derived bounds.
3. Investigate an improved approach under a clearly specified objective and equivalent constraints.

Stage 3 is a research question, not an assumed positive result. The historical approach is not established as a unique globally optimal trajectory. Recoverability mapping is supporting methodology, not a replacement objective.

## Latest research direction — 13 October 2026, 16:14 IST

Aryan explicitly prioritizes an analytically solved/closed-form optimal landing, using reconstructed historical terrain, approach instructions and flight evidence. Numerical optimization alone does not fulfill this goal. ANALYTICAL_RESEARCH_BRIEF.md records the current interpreted scope and solution classes. 1993 is the stated reconstruction-date assumption. Numerical model v1 remains preserved as a checked reference, not the final scientific contribution.

Completed bounded lanes: analytical/ (exact position-constrained benchmark and tractability), reconstruction/ (verified historical sources/acquisition), and independent analytical proof review. Full closed-form landing remains an open research question. No new numerical envelope/objective silently substituted. See ANALYTICAL_FINDINGS.md for the reconciled handoff.

Verified analytical evidence: exact straight–circle–straight endpoint geometry and family-optimal radius; fixed-altitude/selectable-slope minimum-bank cubic with explicit hyperbolic expression. Parent rerun and independent reviewer passed 80 synthetic cases plus deterministic/domain/descent checks. Independent review found no fatal restricted-proof error; zero-duration, validator-scope and numerical-stability qualifications accepted. No full-state comparison with numerical v1 or whole-landing bound follows.

Verified acquisition evidence: official historical aerial/product and datum documentation, two substantive datum PDFs, limited nonauthoritative preview tiles; all 29 downloaded/extracted artifact checksums passed. HTTP success counts include excluded error pages. No complete 1993 terrain, exact frame-level acquisition, new airline manual or raw routine-flight records. Source report records date/datum/rights gaps. Delivery package contains authored reports, proof verifier and acquisition references, not third-party imagery.

Next analytical milestone: finite-roll position matching with the same full boundary states; next historical gate: exact dated aerial frame IDs and survey-sheet editions, then datum reconciliation and uncertainty-aware obstacle geometry. Neither has been completed by the restricted theorem.

## Current stage and ownership

New authorization, 17:23 IST: Aryan explicitly requests solving turning, descent and speed together to construct a complete candidate, followed by the required feasibility/optimality proofs. Fixed delay/deceleration remain binding; no stronger brakes or reduced constraints authorized. Active continuation writes under analytical/coupled/, preserving numerical v1 and earlier evidence. First recover the exact continuous-family objective, then coupled candidate construction, all-time verification, and global/secondary proof attempt. Closed form remains a target, not an assumed achievable outcome.

Prior continuation, 17:15 IST: finite-roll derivation and full-landing analytical attempt returned. Parent verification passed after the documented triangular-endpoint bisection repair. Independent full-stage audit found no fatal error within the stated nominal domain; wording, configuration binding and precision qualifications were repaired and accepted. That audit covers the earlier results, not analytical/coupled/. Its handoff is archived in analytical/CONTINUATION_HANDOFF.md; see the coupled continuation below for current status.

Constrained-model implementation authorized 13 October 2026. Aircraft, landing target and nominal objective fixed in MODEL_IMPLEMENTATION_SPEC.md under Aryan’s explicit instruction to select them and build the model. Executable scenario code and verification are complete; no full-fidelity aircraft simulator or validated landing controller claimed. No public repository created, push/publication performed or outreach sent. Future intended release does not fix publishing details or authorize immediate publication.

Parallel native research lanes explicitly requested by Aryan:
- mathematical_foundations: proposed model, analytical benchmark and numerical checks. Exclusive writes under foundations/.
- historical_evidence: geometry, flight-record sources and inspected/downloaded artifacts. Exclusive writes under evidence/.
- literature_and_comparison: primary literature and fair comparative design. Exclusive writes under literature/.

Parent owns this ledger and the synthesis/specification draft. No second-order delegation requested.

## Existing evidence

Acquisition directory: ../../data/kai-tak-2026-10-13/ (README.md, manifest.json, original CAD report, extracted figures and unsent request drafts).

Recovered: complete 226-page CAD Aircraft Accident Report 1/95, CAL605, Boeing 747-409B B-165 at Kai Tak on 4 November 1993. Published DFDR plots and track reconstruction; not raw time-series files or successful expert demonstrations. Relevant control traces span about 72 seconds. Throttle-lever angle was not recorded. Previous-flight engine plot is Taipei, not Kai Tak.

Missing: BA/Cathay raw normal-approach dataset. Holtom's 1,079 sample is not verified as wholly Kai Tak. No archive release guaranteed. Original download task remains partially fulfilled, not cancelled by the new research framing.

Earlier exploratory brief: ../../data/kai-tak-2026-10-13/HOBBY_PROJECT_BRIEF.md. This file now owns ongoing project state; that brief is background, not a second maintained ledger.

## Binding distinctions

- Observed records vs digitized approximations vs simulated paths.
- Feasibility vs objective improvement vs global optimality vs operational safety.
- Failure of numerical search vs proof of infeasibility.
- Closed-form expression vs numerical root solving vs verified numerical certificate.
- Same-technology historical comparison vs explicitly modernized counterfactual.
- Robust feedback policy under uncertain wind vs separately optimized known-wind trajectories.

## Fixed scenario decisions and remaining identification gaps

Executable specification: MODEL_IMPLEMENTATION_SPEC.md v1. Selected 747-409B / 747-400, flaps 30, gear down, estimated mass 525718 lb. Target includes threshold crossing, flare, touchdown and stop within 2786 m LDA with 150 m reserve. Nominal normalized constraint margin is the primary numerical objective; control effort is secondary. Reduced point-mass aircraft envelope, start state, synthetic corridor, touchdown tolerances and braking are explicitly scenario-based, not measured historical constraints.

Still unavailable: calibrated aerodynamic/actuator and braking envelope; historical georeferenced terrain/corridor; raw routine-flight data and reference historical policy; go-around viability and robust causal feedback-policy synthesis. These are not waived. Known-steady-wind stress tests cannot certify universal gust tolerance. Historical mode must refuse to certify feasibility without its missing inputs.

## Prior verified milestone

All three packages collected and reports inspected. Parent reran finite-roll verification: six synthetic cases passed. Combined PROJECT_SPEC_DRAFT.md prepared with all three aims, requirement statuses, assumptions and unresolved choices. Next: source-backed geometry/parameter sheet and explicit aircraft, objective and terminal-target choices before freezing implementation. Full historical-data acquisition remains partial; no improved landing path demonstrated. The earlier runtime collection/write blocker is cleared in this turn.


## Latest verified implementation

MODEL_IMPLEMENTATION_SPEC.md v1 completed as a scenario model. Authoritative run outputs/scenario/optimization_replay.json, UTC 2026-10-13T10:35:26.454179+00:00. Parent reran 52 tests, 29 artifact checks, the six finite-roll cases, historical refusal and intentional search failure. Both nominal optimization stages succeed. Dense and independent replay-state constraints pass. Final illustrative touchdown 330.42 m; stop 2533.06 m, leaving 252.94 m of the 2786 m LDA. Maximum bank 13.33 degrees. Earlier 395 m / 221 m numbers are superseded by the post-review run.

Three review lanes completed; accepted defects repaired. Full report MODEL_VALIDATION_REPORT.md; model/ contains code/config/tests; README.md has reproduction commands and requirements.lock pins dependencies. No Git repository or publication created.

## Next scientific dependency

The requested executable model is built, but the three-aim study remains incomplete. Priority is historical geometry/corridor and aircraft-envelope calibration before interpreting paths as Kai Tak-feasible. Routine-flight acquisition remains blocked; draft custodian requests are still unsent. Go-around viability, causal feedback robustness and full historical comparison remain unimplemented, not waived. The scenario stress tests fail minimum EAS under negative crosswind, thrust slew at +5% mass and runway reserve with 10% less braking. No historical improvement or operational safety claim follows.

## Analytical continuation verification — 13 October 2026

Finite-roll matching: 30 ODE cases and five domain rejections passed on parent rerun at 11:43 UTC after exact-endpoint root repair; previous failure and numerical conditioning are preserved in analytical/CONTINUATION_HANDOFF.md. Full-landing verifier: 41 curve comparisons, 50 derivative checks, exact rational Hermite identity and nominal objective upper certificate passed, plus four changed-domain rejections. The bound is approximately 0.15769490255; it is a necessary bound for the nominal real-decimal model, not a constructed optimum or an IEEE-execution enclosure. Simulator/config unchanged. Still missing: optimal parameters, continuous-time feasibility, primary/secondary global certificates and historical inputs. Next mathematical requirement is a matching feasible/global certificate or a sharper optimum characterization; no result or automatic continuation is promised.

## Coupled continuation — current verified result, 13 October 2026

Supersedes the previous missing-continuous-feasibility status, not the frozen model.
Authoritative witness: analytical/coupled/continuous_certificate_refined.json.
Approach 37.3377606433 s, flare 4 s, touchdown x=313.492181158 m and vx=77.888054960 m/s;
stop x=2531.321117620 m. Real-decimal nominal continuous-family margin >=0.0397
certified by outward-rounded interval arithmetic over 2502 closed subintervals.
Both sides of the phase join, exact control rates, endpoint identities and exact
ground rule are checked. The candidate includes a brief climb allowed by v1.
No historical, calibrated-aircraft or operational-safety claim follows.

Finite-family attainment is proved by compactness and a verified |vz|<14 m/s
bound over the entire parameter box, which rules out inverse-dynamics singularities
on the positive-margin feasible domain. This proves existence, not the optimizer's
identity. Separately, a valid scalar family upper bound is 0.1559772. The broader
terminal-only bound 0.15769490255 retains its prior scope.

Parent checks: 180 scalar/interval comparisons, 24 endpoint identity cases, five
rejection/regression cases, 130 ancestor boxes retaining the feasible witness,
fresh certificate rerun, complete time-cover checks and independent forward replay.
Replay position discrepancy <1.45e-7 m; velocity discrepancy <4.04e-8 m/s. New
proofs have not received a separate agent review. Numerical v1 sources/config unchanged.

Two global-checker defects were found: misuse of a corridor lower enclosure as
an exclusion upper bound; mpmath 1.3.0 interval atan2 at its branch cut falsely
excluded a box containing the feasible witness. All affected exclusion runs are
marked invalidated. Claimed upper limits 0.10/0.05/0.04/0.03972 from those runs
are withdrawn. The safe checker uses a full angle hull at nonpositive-denominator
intervals; the candidate certificate additionally proves strictly positive lift-up
and horizontal speed throughout and passes again. Scalar bound/existence lemma
unaffected. Latest global run and execution disposition are recorded below when settled.

Remaining: identified global primary optimizer, exact optimal-parameter formula,
global secondary effort certificate, unrestricted-control theorem and historical
inputs. Overall expanded request remains INCOMPLETE. See analytical/coupled/RESULTS.md.

Execution disposition, 2026-10-13 12:28 UTC (17:58 IST): branch-safe global run
exited normally after its 15,000-box budget, with 3,965 exclusions and 7,071
unexcluded boxes at eta=0.10. No upper bound of 0.10 follows. The rigorous
finite-family bracket remains [0.0397,0.1559772). Candidate construction and
all-time feasibility are verified; exact primary/secondary global optimality is
unresolved. No solver, delegated worker or durable research monitor remains active
from this continuation. Next technical step is stronger global exclusion/dual
certification; no further user permission is needed for in-scope research.


## Geospatial acquisition — 13 October 2026

Latest explicit scope: Aryan accepts another accurately documented period if exact 1993 geospatial data are unavailable and requests downloading the data into this project. This expands acquisition beyond 1993; it does not authorize treating mixed epochs as a historical reconstruction or silently changing the frozen landing scenario.

Downloaded and verified under `geospatial/`: official Lands Department whole-Hong-Kong 5 m DTM (documented source photography 2014–2015, product revision March 2019; newer catalogue/server dates preserved separately), plus September 21, 2026 whole-territory building footprints/elevations. Original ZIP/GeoJSON retained. 122,422,351 terrain cells; lossless EPSG:2326 GeoTIFF checked against every source value. Building file has 342,195 features, matching the source service count. Local acquisition rectangle WGS84 [114.10,22.27,114.25,22.40] produces terrain and 69,915 building features. 34 file/hash checks pass including manifest. Package about 525 MB excluding its separate Python environment.

Important gaps: 10,026 local building records lack TopHeight; 13 local polygons are invalid (83 whole territory); nulls and geometry retained and flagged. All source building statuses are Active. Heights are HKPD elevations, not AGL; the DTM includes vegetation/some elevated infrastructure and is not a land/water mask or complete obstacle model. No shoreline geometry acquired; official iB1000 tile/source leads retained. Mixed dates, historic runway placement, datum reconciliation, unknown obstacles, whole-aircraft clearance and simulator integration remain unresolved. No existing simulator/config changed, no claim that previous paths clear Hong Kong, no outreach/purchase/publication. See `geospatial/README.md`, `metadata/validation.json`, `manifest.json` and `SHA256SUMS` for exact paths, source attribution and limitations. Historical 1993 reconstruction remains incomplete; geospatial data are no longer wholly unavailable.

## Historical visual reconstruction discussion — 13 October 2026

Aryan requests focusing on the approach area and identifying which buildings existed at a selected time to visualize the historical airport approach. Broad terrain persistence is a starting assumption with local-change checks, not a claim of unchanged terrain everywhere. Initial documentary screening in `reconstruction/APPROACH_CITY_INVENTORY.md` distinguishes four Mei Tung Estate blocks by official completion years and flags the Walled City as date-sensitive demolition geometry. Newly located official Old Survey Sheets collection offers about 72,000 sheets and is distinct from the narrower historical-map catalogue previously checked. Exact area/date sheets and frames still need acquisition; no full inventory or 3D rendering completed. 1993 remains a working example, with earlier authorization to choose another documented period preserved. A dated visual reconstruction and a replay of a specific actual flight are separate evidence targets. No model configuration or analytical objective changed.


## Latest target correction: explicit approximation with outcome uncertainty — 13 October 2026

Aryan explicitly clarifies that an exact symbolic optimum and centimetre accuracy are NOT required. Target: use the other session's dated Hong Kong terrain/building reconstruction to produce an explicit approximately near-optimal landing procedure conditional on specified conditions, predicting path, touchdown, runway consumed/remaining and time with justified uncertainty intervals. Numerical construction may support the explicit approximation; a numerical optimizer alone is not the desired user-facing rule. Preserve nominal margin/secondary-effort objectives and fixed nominal aircraft/braking unless separately changed. Latest target supersedes exact optimal-parameter closed form as a completion gate; terrain, justified approximation/near-optimality and uncertainty remain required.

This session owns `approximation/SPEC.md`, `APPROXIMATION_DESIGN.md`, `scene_contract.md` and reference/output preparation. Terrain owner is dashboard session [local-session-reference], currently assembling `reconstruction/chronology/`. Stable REPORT/validation is awaited; owner confirms no clearance-certified surface/hard obstacle intervals yet. Do not consume changing chronology exports as verified scene input or duplicate acquisition.

Reference preparation preserves existing model/config/certificates. Conditional stopping envelopes are not probabilistic confidence intervals. Individual-outcome prediction intervals and whole-path coverage need explicit calibration, model/tracking uncertainty and a defined condition domain; none is fabricated from the DTM's ±5 m at 90% statement. Historical runway registration, unknown obstacle masks, whole-aircraft geometry/tracking clearance and probabilistic calibration remain dependencies. Full solution remains incomplete.

Correction delivered in results chat: the earlier near-optimality assertion using 0.03972 was wrong because a fresh rerun reproduced a defective interval checker. That limit is withdrawn; valid current synthetic-family bracket remains [0.0397,0.1559772), and the all-time feasible witness remains verified. No claim of near-global optimality is retained.


## Explicit-reference preparation verified — 13 October 2026, 12:42 UTC

`approximation/explicit_reference.py` and formula/outcome exports now reproduce the fixed synthetic continuous-feasible witness without changing the model/configuration/certificate. Parent independently reran 30 tests (30 passed in 0.89 s) and checked nine artifact/source SHA256 values. Tests include independent original-curve evaluation through jerk, joins, ground rollout, all 128 corners of a synthetic scalar interval box, extrapolation/invalid input refusal and source tampering. Statistical prediction fields remain null; no physical uncertainty was invented.

Reference outcomes: touchdown 313.492181158 m; ground roll including delay 2217.828936462 m; threshold-to-stop 2531.321117620 m; remaining 254.678882380 m. Entry-to-touchdown 41.337760643 s; touchdown-to-stop 54.949141627 s; entry-to-stop 96.286902270 s. These are deterministic synthetic-model values, not historical predictions.

Full revised scope audit: 4/10 requirements implemented and verified; scene interface partial (1); historical geometry integration, conditional rule, full feasibility/near-optimality, calibrated predictions and final delivery blocked (5). See `approximation/STATUS.md`, `SPEC.md`, `verification.json`, `parent_verification.json`. Stable terrain-owner chronology REPORT/validation remains the integration gate; documentary evidence alone is not a clearance surface. No approximation solver or durable monitor remains active. Authorization for the full scope persists; no task requirement is waived.

## Historical source matching and chronology — verified 13 October 2026, 12:50 UTC

Latest instruction: match historical sheets/photos and classify as many structures as possible across dates, beginning with the Kai Tak approach area. Canonical evidence spec and handoff: `reconstruction/chronology/SPEC.md`, `REPORT.md`, `HANDOFF.json`, `MODEL_REQUIREMENTS_TRACEABILITY.md`. These files are now stable local deliverables. Overall historical reconstruction is INCOMPLETE; no background acquisition or reconstruction remains active.

Acquired complete official sheet indexes: 72,691 whole-HK editions / 18,440 local intersections. Downloaded 227 valid historical map archives across 93 core sheet locations. Aerial index: 14,927 frames on 316 dates, 1985–1998, including 1,277 in 1993; 48 actual full DAP-L0 frames and 47 previews acquired. Coverage matching produces 16,968 sheet/frame index-polygon pairs and 69,915 current-feature candidate rows. These are not registered image-content matches. Month-precision November editions are not presumed earlier than November 4; five earlier maps were added after review.

Complete official works/permit graph supplies 221,383 evidence paths; conservative arbitrary-date classification covers all 342,195 current polygons, 69,915 local. Linked documentary records: 71,382 whole / 29,082 local. For example 1993-11-04, 35,540 whole / 21,746 local have some completion/permit support, with 34,387 / 21,066 matching completion and relational permit dates. No current polygon is thereby historical-survival/geometry verified. The current graph recovers zero vanished identities outside today's polygons. All 52,552 works OP dates fall in 2019–20 and 52,202 disagree with linked permits; fresh raw-source checks confirm this source anomaly. Both values and conflicts retained.

Visual ledger: 52 observations for 17 named structures/sites, not a building census. Parent inspected three map editions and three full aerial frames. Walled City dense roofscape in 1990-11-13, largely cleared with remnants in 1993-10-08 and 1993-11-02; park mapped April 1997. Blank 1989 sheet interior is map omission, not absence. Chung Tung site construction indicated October 1989, named structure mapped July 1994; precise completion remains unresolved.

Verification: 39 documentary + 7 matching tests passed on parent rerun; 942 final checks including all 227 CRC/hash checks, 95 image hashes/decodes, 170 structure-manifest hashes, 51 sheet-index response hashes, cross-artifact counts and semantics. Root delivery manifest separately verified 93 files. Two independent code reviewers, with one also performing artifact acceptance. Six classifier robustness repairs produced zero changes to old output fields across all 342,195 objects at both 1985/1993 query dates; synthetic fixtures cover previously failing cases. Source comparison and coverage figures visually inspected. No Git commit/push, publication, peer sync or aircraft/config change.

Downstream approximation handoff includes explicit AOI-wide `historical_uncertainty_mask.geojson`: epistemic non-certification, not physical occupancy. EPSG:4326 indexes/current footprints; EPSG:2326 terrain and source sheet grid; modern height elevations HKPD. DTM photo epoch 2014–2015 with ±5m at 90%, not hard bounds. Historical heights, footprints, complete obstacles, shorelines/earthworks and aviation datum reconciliation remain missing. Next work: ground-control registration and structure-level historic identity/geometry interpretation; obtain defensible historical heights before 3D/clearance claims. No scope requirement waived.


## Terrain handoff reconciled; requested closed-form/CI result audited — 13 October 2026, 13:01 UTC

Aryan asks to see the final landing solution with CI/error bounds now that the terrain is assembled. The stable source/documentary handoff has arrived, but its own status is historical_scene_incomplete and clearance_certified=false. Freshly checked all nine handoff artifact sizes/SHA256 values; all match. Inspected REPORT/HANDOFF and reconciled the scene interface. Historical footprint verification remains zero, historical hard height bounds and aviation-datum reconciliation absent; whole-AOI epistemic mask is not a physical obstacle or free-space map. No terrain-aware solve or calibrated prediction interval is present.

Fresh reference verification: 30 tests passed in 1.07 s; formula and outcome objects exactly reproduce saved exports. Model/configuration/certificates unchanged; no new optimum or physical certificate claimed. `approximation/CLOSED_FORM_AND_BOUNDS.md` now gives complete approach/flare coefficient tables, ground path, runway/time expressions, conditional deterministic error-envelope formulas and the surviving synthetic-family objective bracket. `approximation/handoff_reconciliation_verification.json` records fresh evidence. Numerical CIs remain unavailable rather than fabricated.

Updated `approximation/scene_contract.md`, `SPEC.md` and `STATUS.md`: DATA-01 interface reconciliation complete, with geometry limitations preserved under GEO-01. Scope audit now 5 implemented / 5 blocked of 10; final OUT-02 remains blocked. Needed inputs/work are historical runway/scene registration and heights, whole-aircraft/tracking clearance, condition-domain solves and explicit coefficient map, useful valid optimality gap, and calibrated prediction uncertainty. This is not a scope reduction or declaration that the landing is impossible. No solver or background reconstruction was started.

## Block-wise matching and 3D continuation — active 13 October 2026

Aryan explicitly requested block-wise structure matching followed by the most accurate 3D reconstruction. Scope and sequence preserved in `reconstruction/block_matching/SPEC.md`. Original chronology artifacts remain immutable evidence; this continuation owns a separate directory. Work now includes official world-file sheet registration, actual local aerial ground-control measurement, source-outline digitization and content-based matching. Geometry, presence, height and terrain epoch remain distinct; no current roof height is silently made historical. Full reconstruction remains incomplete while per-structure geometry/heights and broad coverage remain unresolved. Aircraft model and approximation owner's files are unchanged. No publication, purchases or outreach authorized by this continuation.


## Flight-record/weather research discussion — 13 October 2026

Aryan asks how historical landing records, weather and multi-date Kowloon reconstruction could help identify an explicit approximate solution and yield mathematical/aviation results. Discussion does not change the frozen aircraft, objective, braking or terrain-owner scope. New evidence note: `evidence/weather_feasibility_2026-10-13/README.md`.

Acquired NOAA legacy ISD 1993 station-year 450070-99999 at 13:07 UTC: gzip 127,633 bytes, SHA256 617c7db4f19c3aaacef91ae8a688c0aab196cdfc7ddfba72857c8e70056d66e0; 8,549 records spanning Jan 1–Dec 31, including 24 dated Nov 4. Re-read checksum/decompression/counts passed. Historical header coordinates differ from current airport inventory; historical station/sensor metadata, variable quality/missingness and synchronization remain to reconcile. These are surface weather observations, not flight-path gusts. CSV endpoint failed schema validation; legacy gzip worked. No calibrated weather model or flight series generated.

Fresh primary-report text inspection identifies CAL605 Appendix 7's matching 03:30–03:40 UTC five-location wind-system printout, with event-dependent recording, averaged/present-wind distinctions, no measured vertical currents and unresolved clock offset against ATC. Existing DFDR graphs and this weather printout provide a matched case but need uncertainty-preserving digitization. Routine-flight QAR archive remains unavailable; BA historical analysis is evidence records existed, not a guaranteed surviving/releasable dataset. HKO has an official potentially paid data-request route; no request, purchase or external communication made.

Proposed scientific direction: identifiable dynamics/discrepancy calibration; dated robust landing-feasibility sets; explicit condition-to-coefficient approximation with separate feasibility, gap and prediction evidence; controlled geometric counterfactuals. Observational pilot traces alone neither identify a unique objective nor prove a closed-form optimum. One accident cannot support normal-flight prediction coverage or accident rates. Immediate recommended benchmark is the already-held matched CAL605 case; broad validation requires routine approaches and go-arounds plus configuration and wind data. No scope reduction or newly proved result implied.


## Public GitHub publication authorized — 13 October 2026

Aryan explicitly requests a public GitHub repository named `kai-tak` and publication of the work assembled so far. This supersedes earlier local-only/no-publication statements for this snapshot; it does not authorize changing scientific model meaning or licensing third-party material beyond its source terms. Verified GitHub account: `ayyararyan`; intended remote `https://github.com/ayyararyan/kai-tak`.

Publication checkout is a separate snapshot at workspace `repos/kai-tak`, preserving the research/data directory layout and the live source work. Code, derivations, reports and research outputs go in Git; large open-data and reconstruction assets go in a versioned release with hashes. Environments/caches, private download-queue state, correspondence drafts, third-party paper PDFs and accident-report scans without verified redistribution permission are excluded explicitly. Original local evidence is retained. Source data from Lands Department/Buildings Department, CSDI, DATA.GOV.HK and NOAA keep their own attribution/terms. No blanket open-source licence is selected on Aryan's behalf. Creation/push/release verification will be recorded after success.
