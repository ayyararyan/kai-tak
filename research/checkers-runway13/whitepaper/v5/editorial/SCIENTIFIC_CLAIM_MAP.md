# Version 5 scientific-claim preservation map

Audit owner: independent scientific lane. Updated 13 October 2026. The original 51-row ledger is preserved byte-for-byte as `editorial/V4_CLAIMS_AND_EVIDENCE.csv`. The active `CLAIMS_AND_EVIDENCE.csv` now records V5 locations and fresh verification routes. All 50 scientific/source claim IDs survive; author-context C01 is condensed for the authorized foreword rewrite, with residence detail omitted and no new experience invented. The seven-act source audit, abstract and all15 figure-semantic checks are complete; final editorial dispositions and clean-build evidence are separate.

The active ledger contains 53 rows: 51 preserved baseline IDs plus two traceable
facts newly illustrated from existing sources, C52 and C53. No source-derived
height is promoted to a surveyed or physically bounded quantity.

Qualification placement: **A** essential locally at first use; **B** methodological assumption/definition; **C** conclusions or open problems. Redundant repeats can be removed, but the listed essential meaning cannot.

| ID | V5 destination | Immutable finding / object | Qualification class and retained scope | Evidence |
|---|---|---|---|---|
| C01 | Foreword | Author-supplied childhood aviation interest, Hong Kong studies and personal connection, condensed for V5 | A: Personal context not independently authenticated; not historical evidence | sections/foreword.tex; whole text |
| C02 | Act I | IGS introduced in 1974 | C: Instrument guidance does not complete visual turn | references.bib; cadhistory |
| C03 | Act I; fig:bearings (02_bearings) | 088 magnetic localiser; 135 magnetic runway; 47-degree difference; 3.1-degree glidepath | A: Direction change not bank angle; diagram not surveyed | references.bib; cad §1.8.1 and Appendix 1 |
| C04 | Act I | Middle marker 1.7 NM from touchdown; missed approach without visual acquisition | A: Not a zero-visibility final turn | references.bib; cad §1.8.1 |
| C05 | Acts I and III; Appendix G | 3331.5 m runway; 61 m width; 2786 m LDA | A: Distinct from CAD general history 3390 m extension-era length | references.bib; cad §1.10 |
| C06 | Act I | Visual turn over Kowloon; closure July 1998; Chek Lap Kok distinct | C: Checkerboard Hill not Victoria Peak | references.bib; cadlink Issue 75; cadhistory |
| C07 | fig:place (01_place); Act IV; Appendix G | A36143 catalogue 1993-11-02; scan label appears 3-11-93 | A: Unresolved date; no re-dating | inputs/A36143_product.json;inputs/A36143.jpg; catalogue and printed margin |
| C08 | Appendix G | 227 valid survey archives; 93 core locations; 48 frames | B: Acquisition not complete obstacle coverage | evidence/reconstruction/chronology/REPORT.md; acquisition counts |
| C09 | Appendix G | 404 dated template assignments; 202 templates; 531 map-region assignments; 397 overlaps | B: Not 935 buildings or unchanged historical identities | evidence/reconstruction/block_matching/REPORT.md; road-cell comparisons |
| C10 | Act IV; Appendix G | 1318 sparse;171307 dense;3780 inside control hull | A: Relative-plane geometry; no roof confidence interval | evidence/reconstruction/block_matching/aerial_registration/sparse_stereo_report.json;evidence/reconstruction/block_matching/aerial_registration/dense_stereo_report.json; retained counts |
| C11 | Act IV; Appendix G | 3780/171307=2.2065648 percent | A: Control support share not accuracy share | qa/science_checks.json; control_hull_share |
| C12 | Act IV; Appendix G | 5.754 m held-out horizontal RMS | A: Not vertical error or physical maximum bound | evidence/reconstruction/block_matching/aerial_registration/README.md; registration diagnostic |
| C13 | Appendix G | 155891 vertices;225371 triangles;86061 boundary edges | B: Non-watertight; no hidden walls inferred | evidence/reconstruction/block_matching/aerial_registration/observed_surface_mesh_report.json; mesh counts |
| C14 | Appendix G | 49-point interpolation-support correction retained | B: Invalidated predecessor not used | evidence/reconstruction/block_matching/aerial_registration/observed_mesh_verification.json; support correction |
| C15 | Act IV; Appendix G | 24 approximate readings at 12 sites;45 dated forms;0 volumes;0 bounds | A: Bracketing map editions not exact 1993 presence; HKPD/AMSL unresolved | evidence/reconstruction/obstacles/readiness.json;evidence/reconstruction/obstacles/REPORT.md; readiness fields |
| C16 | Act IV; Appendix G | Modern DTM uses 2014–2015 photography;2019 revision;modern buildings Sept2026 | B: Not historical 1993 obstacles | references.bib; dtm; buildings |
| C17 | Act II; fig:turn (03_turn) | 78 m/s at15deg: radius2315.347m;47deg in24.3499s;1899.29m arc;load1.03528 | A: Constant-speed level coordinated turn; no roll-in or historical fit | qa/science_checks.json; values.turn |
| C18 | Act V; Appendix D | Wind070true21kt;runway133deg10min;vector(-4.87659,9.64007,0)m/s | A: 1990 chart variation convention; not surveyed historical wind field | evidence/counterfactual/inputs.json;qa/science_checks.json; wind components |
| C19 | Act V; fig:wind (08_wind) | Entry wind projections(-10.3761,3.0080)m/s;runway projections(-4.8766,9.6401) | A: Same constant wind; different track | qa/science_checks.json; values.wind_projection |
| C20 | Act III; Appendix B | 78sin(-3.1deg)=-4.2181m/s; touchdown target-0.7m/s | B: Straight still-air benchmark | qa/science_checks.json;evidence/model/config.json; descent and touchdown |
| C21 | Act III; Appendix A | Energy rate=(thrust-drag)*V in still-air coordinated point-mass model | B: No variable-wind extension implied | appendices.tex;evidence/MODEL_EQUATIONS.md; equations19–20 and PartIII |
| C22 | Acts III and V; Appendices B and H | Position velocity acceleration continuous; one-sided rates; brief climb retained | B: No monotonic-descent constraint added | evidence/approximation/reference_formula.json;evidence/counterfactual/formula.json; phase polynomials |
| C23 | Act III | 10percent speed increase gives21percent greater braking distance | B: Fixed deceleration; not an approach-speed recommendation | qa/science_checks.json; quadratic_braking_ratio |
| C24 | Act III; fig:runway (05_runway) | Delay155.776m; braking2062.053m; sensitivities-54.949m/(m/s),-77.888m/s | A: 2s delay and0.15g are assumed | qa/science_checks.json; values.calm |
| C25 | Act III; Appendix B | Synthetic entry(-2500,1000,140); threshold15.24m;153kt EAS;12-parameter family | A: Not CAL605 initial position or middle-marker registration | evidence/model/config.json;evidence/analytical/coupled/solve_coupled.py; boundary and family definitions |
| C26 | Act III; Appendix A | 525718lb estimated mass converted to238461.67357166kg | A: Exact conversion not exact measured mass | evidence/model/config.json;references.bib; cad aircraft data; config mass |
| C27 | Act III; Appendix A envelope table | Lift drag force/rate limits; margin normalization; secondary effort | B: No Boeing performance calibration or natural safety metric | evidence/model/config.json;evidence/analytical/coupled/solve_coupled.py;evidence/MODEL_IMPLEMENTATION_SPEC.md; configuration and objective |
| C28 | Act III; fig:landing (04_landing) | Calm touchdown313.492181m;stop2531.321118m;remainder254.678882m;time96.286902s | A: Frozen synthetic calm case | evidence/approximation/reference_formula.json;evidence/approximation/reference_outcomes.json; endpoints and ground law |
| C29 | Act V; Appendices D and H | Calm eta>=0.0397 over2502 intervals | A: Specified model only; mpmath not proof assistant | evidence/analytical/coupled/continuous_certificate_refined.json;qa/fresh_calm_certificate.json; real-decimal vector and complete cover |
| C30 | Act V; Appendices D and H | Wind eta>=0.1507934696816132 over376 intervals | A: No uncertain-wind policy or physical tracking bound | evidence/counterfactual/continuous_check.json;qa/fresh_wind_certificate.json; real-decimal vector and complete cover |
| C31 | Act V; fig:runway (05_runway) | Wind touchdown302.114052m;stop2233.230845m;remainder552.769155m;time96.644054s | A: Different optimization from calm | evidence/counterfactual/result.json;evidence/counterfactual/formula.json; outcomes |
| C32 | Act V | Touchdown ground140.909kt;EAS151.558kt;threshold41.223s;TD45.365s | A: Airspeed not ground speed | evidence/counterfactual/path_controls.csv;evidence/counterfactual/result.json; phase endpoints |
| C33 | Act V; fig:runway (05_runway) | 298.090273m difference=11.378129m touchdown+286.712143m ground travel | A: Not causal effect of wind alone | qa/science_checks.json; values.scenario_difference |
| C34 | Acts V and VII; Appendix C | Calm optimum strictly below0.1559772;root bracket0.1559771–0.1559772 | A: Not attained optimum; withdrawn stronger claims excluded | evidence/analytical/coupled/existence_bounds.json;qa/science_fresh_calm_bound.json; family_upper_bound |
| C35 | Act V; Appendix D | Wind upper66656817/307536544;gap0.0659509085084467 | A: Necessary relaxation; not near-optimality criterion | evidence/counterfactual/result.json;qa/science_checks.json; upper bound and exact gap |
| C36 | Act VI; Appendix H | CAL6054Nov1993;touchdown controllable and not causal;four major rollout/context causes | A: No new causal conclusion or prevention counterfactual | references.bib; cad Synopsis;§2.6.5;§3 |
| C37 | Act VI; Appendix G | 269 recorder parameters;no thrust-lever angle;integrated track not independent GPS | A: Cockpit controls not surface deflections | evidence/evidence/cal605_reconstruction/REPORT.md;references.bib; cad §1.11;Appendix12 |
| C38 | Act VI; fig:recorder (10_recorder); Appendix G | 190 approach/final anchors;35 speed-distance anchors;final subset shown | A: Raster sensitivity not physical confidence intervals | evidence/evidence/cal605_reconstruction/flight/flight_summary.json;evidence/evidence/cal605_reconstruction/flight/flight_anchor_readings.csv; anchor counts;Figure13 |
| C39 | Act VI; Appendix G | Distinct touchdown distance conventions2300/2250/2210/2306m remaining | A: No forced alignment or averaging | evidence/evidence/cal605_reconstruction/REPORT.md;evidence/evidence/cal605_reconstruction/analysis.json; touchdown comparisons |
| C40 | Act VI; Appendix G | 225 windpairs=15times*5sensors*3fields;A1secmax/5sec;B2min;C10min | A: Event-triggered; clocks not aligned | evidence/evidence/cal605_reconstruction/wind/wind_records.csv;evidence/evidence/cal605_reconstruction/wind/README.md; A/B/C meanings |
| C41 | Act VI; fig:weather (11_weather) | 03:35:30NW37/23/19kt;03:38NW12/LYM37kt | A: Ground sensors not aircraft-local wind | evidence/evidence/cal605_reconstruction/wind/wind_records.csv; specified timestamps |
| C42 | Act VI; Appendix G | 8549annualrows;24eventday;8360routine;8285lower17tie58higher | A: Not return period or risk probability | evidence/weather_plot_data.csv;evidence/evidence/cal605_reconstruction/noaa/verification.json; selection/counts |
| C43 | Act VI | 0300/0400UTC070true10.8m/s;gust17.5/20.6m/s | A: Rounded21kt not silently replaced; shared source possible | evidence/weather_plot_data.csv;evidence/evidence/cal605_reconstruction/noaa/verification.json; event values |
| C44 | Act VI; fig:rollout (12_rollout) | Required deceleration rises0.150g→0.255g;2s delay last0.300g | A: Not actual brake force measurement | evidence/evidence/cal605_reconstruction/analysis.json; report_landmark_stopping_frontier |
| C45 | Act VI; Appendix H | 480m160kt with2s0.15g gives-161.521789m remainder | A: Extrapolated scalar outcome; not actual overrun reconstruction | evidence/evidence/cal605_reconstruction/analysis.json; fixed_formula |
| C46 | Act VII; Appendix C | Restricted calm primary and secondary extrema attained | C: Does not identify optimizers or extend to actual aircraft | evidence/analytical/coupled/RESULTS.md;appendices.tex;qa/science_fresh_calm_bound.json; regularity/compactness argument |
| C47 | Act VII; Appendix H | Model feasibility does not establish historical clearance or operational safety | C: Historical flyability and robustness unidentified | evidence/reconstruction/obstacles/readiness.json;evidence/MODEL_IMPLEMENTATION_SPEC.md; missing coverage/calibration |
| C48 | Appendix F | Monotone stopping box extrema and full-stop-time bounds | B: Requires positive deceleration/nonnegative speed-delay; no calibrated box supplied | appendices.tex; stopping-box/stop-time bounds;AppF |
| C49 | Act VII; Appendix H | One causal robust policy differs from separate known-wind solutions | C: Neither robust-policy existence nor full wind set demonstrated | appendices.tex; exists-policy forall-wind |
| C50 | Appendix H; RIGHTS_AND_PROVENANCE.md | Open-data reproduction terms with attribution; no blanket original-work licence | A: No permission generalized to restricted scans | RIGHTS_AND_PROVENANCE.md;references.bib; dataterms;csditerms;root NOTICE |
| C51 | Appendix H | Related work: Dubins steady wind;6DoF landing;FaSTrack tracking guarantees | A: Algorithms not reproduced; guarantees not transferred | references.bib; wu v1;kim v1;fastrack v2 |
| C52 | fig:place (01_place); Act I; Appendix G | CN4581/CN4589 catalogue date 8 October 1993; compressed DAP-L0 imagery | A: Separate source views; not exact 4 November state or a stitched geographic model | inputs/historical/SOURCE_MANIFEST.json; inputs/historical/aerial_fullframe_manifest.json |
| C53 | Act IV; fig:stereo (07_stereo) | Tracks 26/1135 have relative-plane heights 10.7694316303/19.1954909125 m; both outside control hull | A: Not absolute elevation, own-ground building height or vertically bounded error | inputs/historical/sparse_stereo_points.csv; inputs/historical/manual_stereo_labels.json; qa/science_checks.json |

## Non-negotiable mathematical objects

- Calm and wind witnesses are different fixed real-decimal parameter constructions. Their exports are floating evaluation copies, not proof inputs.
- Calm lower margin `0.0397`; 2,502 accepted closed intervals. Wind lower margin `0.1507934696816132`; 376 intervals. A lower normalized margin is not a probability, a physical prediction error or a tracking guarantee.
- Calm optimum is strictly below `0.1559772`; the root bracket is `[0.1559771,0.1559772]`. Wind upper bound is exactly `66656817/307536544`; the exact candidate gap is `1584555818464679384939/24026292500000000000000`. Keep the calm/wind feasible families separate.
- The attainment proof applies to the frozen zero-wind 12-parameter polynomial family; compactness plus regularity gives existence, not an identified optimizer. It does not establish unrestricted optimality. Withdrawn tighter checker bounds remain invalid.
- Ground law: `S=x_D+u d+u²/(2a)`, `a=1.4709975 m/s²`, `d=2 s`, `LDA=2786 m`, reserve `150 m`. Speed is forward ground speed; distance is threshold-to-stop, including the airborne flare above runway.
- Position, velocity and acceleration meet at the approach/flare join. Rates are one-sided where needed. Contact switches to the separate ground rule and resets vertical motion. Both brief climbs remain in plots and prose.
- The 400 m corridor is a fixed synthetic reference cloud. Its geometry must not be implied to represent the actual instrument procedure, middle marker or dated obstacles.
- One known-wind reference for each wind has quantifiers `forall w exists reference_w`; it cannot prove one causal feedback policy `exists policy forall w`.

## No fresh scientific result introduced

V5 changes exposition and illustrations. New arithmetic is re-evaluation of accepted inputs. It adds no optimized trajectory, historical observation, calibration, obstacle-clearance claim, confidence interval, accident counterfactual or source-rights grant. Missing empirical data remain missing.

## Initial diagnosis and disposition

No material numerical conflict was found in the V4 main text/appendices versus frozen evidence. The substantive risks are editorial: local scope can disappear when a result is lifted out of context; historical and synthetic frames can be conflated in prettier scenes; aircraft silhouettes can imply a calibrated swept-volume model; the point-cloud support mask can be hidden by shading. These are controlled by local labels and source-bound rendering, not repeated apologies.

The preserved V4 ledger C01 mentions a 471-word foreword check, and several original verification paths refer to V3 QA. Those are baseline history. The active V5 ledger now cites the actual source-level review and new numerical/proof receipts instead. Modern-data dates are retained historical snapshot descriptions, not claims of present completeness.
