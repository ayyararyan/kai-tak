# Seven explanatory insights: equation, calculation and scope

These are explanations of established mechanics and the project's evidence, not claims of novelty. All paths below are relative to this package; claim IDs refer to `CLAIMS_AND_EVIDENCE.csv`.

| Insight | Equation / logical object | Verified calculation or evidence | Correct interpretation |
|---|---|---|---|
| 1. Dense imagery can contain sparse knowledge | control-support share = 3780 / 171307 | 0.0220656482 (`qa/v3_claim_checks.json`, C10–C11) | Only about 2.21% of retained dense points are inside the map-control hull. This is neither an accuracy fraction nor a clearance probability. |
| 2. Direction change accumulates | R=V²/(g tanφ); Δψ=∫g tanφ/V dt | V=78 m/s, φ=15°: R=2315.347 m; 47° takes 24.3499 s (`qa/insight_calculations.json`, C17) | Modest bank can accumulate a substantial turn given space/time; mass still affects force and performance requirements. |
| 3. Steady wind changes its role through the turn | w_parallel=w_x cosχ+w_y sinχ; w_cross=−w_x sinχ+w_y cosχ | χ:−47°→0° gives parallel−10.376→−4.877 m/s and cross3.008→9.640 m/s (C18–C19) | The decomposition changes without any gust. It is not a measurement of pilot workload. |
| 4. Speed costs stopping distance nonlinearly | braking distance=u²/(2a) | (1.1u)²/u²=1.21; calm dR/du=−54.949 m/(m/s) (C23–C24) | Fixed-deceleration conditional sensitivity; not an operational speed recommendation. |
| 5. Plot samples do not cover all time | min_{t∈I}g_j(t)/s_j≥η, verified by an interval enclosure | Full phase covers:2502 calm intervals at η=.0397;376 wind intervals at η=.1507934696816132 (C29–C30) | The enclosure establishes a model inequality over each entire interval; a sampled positive value does not. |
| 6. Slowing down can coexist with worsening stopping margin | a_req=v²/[2(R−vτ)], R>vτ | Report landmarks:160→129kt but necessary no-delay a rises.150→.255g; last point with 2 s delay ≈.300g (C44) | Runway is being consumed faster than speed-squared falls. This is not measured actual braking. |
| 7. A model certificate is not a safety certificate | q∈F_model does not imply q∈F_historical; physical clearance needs swept aircraft volume∩bounded obstacles=∅ | Both model certificates pass while historical_clearance_ready=false, complete volumes=0, physical upper bounds=0 (C15,C29,C30,C47) | Unmeasured buildings, uncertain dynamics and tracking cannot be certified by numerical accuracy inside the reduced model. |
