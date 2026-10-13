# V5 narrative architecture and complete result map

Stage 2 proposal, preserving the authorized seven-act sequence and V4's scientific meaning. This map covers all 51 rows of V4 `CLAIMS_AND_EVIDENCE.csv`; a move to an appendix is a presentation change, not deletion of the result. The main text has no executive-summary recapitulation and no numbered “Insight” boxes. Full source locators remain in the claim ledger and bibliography.

## The narrative sequence

| Act | Question and discovery | Mathematics / evidence | Visual role | Exit into next act |
|---|---|---|---|---|
| I. A runway in a different direction | Why does a correctly established approach still require a substantial visual turn? | 088°/135° magnetic; 3.1° glidepath; visual acquisition; middle marker; runway/LDA distinction | Original historical aerial + geographically intelligible direction figure | A 47° direction change does not tell us the bank angle. |
| II. How a modest bank accumulates a turn | What does the lift vector have to do, and how long must it do it? | Force balance; radius 2.315 km, 24.35 s, 1.899 km arc, load 1.0353 at 78 m/s and 15° | Aircraft force geometry + overhead arc | The turn solves direction; descent and stopping still compete for the motion. |
| III. Landing continues after the turn | What must fit between approach entry and a full stop? | Descent/energy, flare, stopping law and sensitivities, inverse dynamics, min-margin objective, calm construction | Physically scaled local 3D scene + signature runway allocation | These are local-model coordinates. What would be needed to place the calculation in the dated city? |
| IV. Recovering the city around the approach | What can old images reveal, and where does geometry run out? | Dated maps, stereo mechanism, 171,307 points, 3,780 inside control hull, relative datum, open mesh and obstacles | Readable map pair + photographs/surface/interpreted forms | Even a fixed landscape is crossed through moving air. |
| V. The air moves; the constraints must hold | How does unchanged wind change its role through a turn, and how is the complete path checked? | Wind decomposition, separate optimized case, exact paired certificate bounds, interval idea and necessary family bounds | Two orientations in one steady wind + continuous-check illustration + paired runway readout | A constructed reference lets us ask better questions of an actual record. |
| VI. The landing after touchdown: CAL605 | What did the actual accident record reveal about runway and braking? | Official causal conclusions, selected recorder anchors, unaligned ground weather, required deceleration and conditional benchmark | Source-defined statistical graphics + rollout landmarks | The distinction between an equation and a calibrated system is now concrete. |
| VII. What the landing requires | What has the mathematics explained, and which empirical connection remains? | Physical synthesis; attainment/upper-bound significance; historical calibration, clearance, causal tracking, routine validation, go-around | No administrative flowchart | Return to the initial question: the turn uses space and time; the landing must also preserve speed, height and runway budgets. |

## Result-by-result preservation map

| V4 claim | V5 destination | Required meaning and supporting source |
|---|---|---|
| C01 | Foreword, marked for author review | Supplied personal background only; no invented flight/memory. |
| C02 | Act I | IGS introduced 1974; `cadhistory`. |
| C03 | Act I + bearing diagram | 088° localiser, 135° runway, 47° difference, 3.1° glidepath; CAD §1.8.1/App.1; magnetic/track/heading/bank distinctions. |
| C04 | Act I | Middle marker 1.7 NM from touchdown, missed approach without visual acquisition; CAD §1.8.1. |
| C05 | Act I/III + technical source note | CAD §1.10: 3331.5 m, 61 m, 2786 m LDA; history's 3390 m is a different source quantity. |
| C06 | Act I | Kowloon visual turn; Checkerboard not Victoria Peak; July 1998 closure/Chek Lap Kok distinct; `cadlink`. |
| C07 | Aerial caption + historical source note | A36143 catalogue 2 Nov / apparent scan label 3 Nov 1993 discrepancy unresolved. |
| C08 | Act IV technical source appendix | 227 archives, 93 locations, 48 frames; chronology report; holdings do not equal coverage. |
| C09 | Act IV technical source appendix | 404 assignments/202 templates, 531 regions, 397 overlaps; matching candidates, not accepted buildings. |
| C10 | Act IV + stereo figure | 1318 sparse, 171307 filtered dense, 3780 in hull; sparse/dense reports. |
| C11 | Act IV | 2.2066% measures control support, not city accuracy. |
| C12 | Act IV | 5.754 m held-out horizontal RMS; registration README; not vertical error. |
| C13 | Act IV + technical note | 155891 vertices/225371 triangles/86061 boundary edges; mesh report; open surface. |
| C14 | Technical reconstruction note | 49-point support correction; preserved verification history. |
| C15 | Act IV + technical evidence inventory | 24 approximate HKPD readings at 12 sites; 45 forms; zero accepted volumes/bounds; readiness record. |
| C16 | Technical reconstruction note, cited from Act IV | Modern DTM 2014–15/2019 and buildings Sept 2026; no 1993 substitution; `dtm`,`buildings`. |
| C17 | Act II | Exact worked turn quantities; reduced constant-speed coordinated level benchmark. |
| C18 | Act V + wind appendix | From 070° true, 21 kt, runway 133°10′ true convention; vector (-4.87659,9.64007,0). |
| C19 | Act V | Entry (-10.3761,3.0080), runway (-4.8766,9.6401) m/s components; geometry, not gust evidence. |
| C20 | Act III | Still-air sink -4.2181 m/s; stipulated touchdown -0.7 m/s. |
| C21 | Act III + dynamics appendix | Energy derivative `(thrust-drag)V`; still-air model identity. |
| C22 | Act III/V + polynomial appendix | C2 join, one-sided rates, touchdown ground transition, brief rise retained. |
| C23 | Act III | Fixed-deceleration 10% speed → 21% braking distance; conditional algebra. |
| C24 | Act III | Delay155.776 m, braking2062.053 m, local speed/delay sensitivities -54.949 and -77.888. |
| C25 | Act III + polynomial appendix | Synthetic entry/threshold/EAS and 12-parameter family; no historical registration. |
| C26 | Act III + constants appendix | Estimated 525718 lb → exact conversion 238461.67357166 kg; no exact-mass claim. |
| C27 | Act III + parameters appendix | Force/rate limits, scales and secondary effort; research envelope and declared metric. |
| C28 | Act III | Calm touchdown313.492181, stop2531.321118, reserve254.678882, total96.286902. |
| C29 | Act V + certificate appendix | Calm exact-decimal certificate ≥0.0397/2502 intervals; separate original checker. |
| C30 | Act V + certificate appendix | Wind ≥0.1507934696816132/376 intervals; no uncertain-wind guarantee. |
| C31 | Act V | Wind touchdown302.114052, stop2233.230845, remainder552.769155, total96.644054. |
| C32 | Act V | Ground140.909 kt versus EAS151.558 kt; threshold41.223 s/TD45.365 s. |
| C33 | Act V + paired runway caption | 298.090273=11.378129+286.712143 m; separate optimization, not causal wind effect. |
| C34 | Act V/VII + bounds appendix | Calm strict upper0.1559772; root bracket0.1559771–0.1559772; invalidated stronger limits excluded. |
| C35 | Act V + wind-bound appendix | Exact wind upper66656817/307536544; gap0.0659509085084467; necessary relaxation. |
| C36 | Act VI | CAD touchdown controllable/not causal; four official rollout/context causes; no prevention counterfactual. |
| C37 | Act VI + source appendix | 269 parameters; no lever angle; track acceleration-integrated; no independent raw stream. |
| C38 | Act VI + recorder caption/source appendix | 190 plot anchors/35 speed-distance anchors; manual selected readings and sensitivity. |
| C39 | Act VI source note | Distinct2300/2250/2210/2306 m remaining conventions; no forced average. |
| C40 | Act VI + weather source note | 225 pairs, A1-second max in5 seconds; B2-minute/C10-minute; event-triggered and separate clock. |
| C41 | Act VI | NW37/23/19kt at03:35:30; NW12/LYM37 at03:38; ground sensors. |
| C42 | Act VI + source appendix | 8549annual/24day/8360routine;8285lower/17ties/58higher; archive rank not return period. |
| C43 | Act VI | 0300/0400UTC070°/10.8m/s;gust17.5/20.6; retained rounded21kt input and possible shared observation source. |
| C44 | Act VI + rollout figure | Required deceleration0.150g→0.255g;2s final delay→0.300g; conditional calculation. |
| C45 | Act VI |480m/160kt with fixed2s/.15g gives -161.521789m; not actual water-entry reconstruction. |
| C46 | Act VII + bounds appendix | Compactness/regularity attainment of calm primary and secondary; not optimizer identification. |
| C47 | First model scope / focused Act VII limitations | Calibrated historical flyability, whole-aircraft clearance and operational safety remain separate. |
| C48 | Ground-bounds appendix, referenced in Act VII | Exact Cartesian-box extrema and stop-time bounds with positive deceleration/nonnegative speed-delay; no fabricated input box. |
| C49 | Act VII short explanation + robust-policy appendix | One causal policy for all winds is stronger than separately optimized known-wind paths. |
| C50 | Rights appendix + captions + RIGHTS_AND_PROVENANCE | Source ownership/attribution/as-is; restricted scans not redistributed; original-work licence unset. |
| C51 | Focused Act VII next-research passage + notes | Wu/Chen steady-wind Dubins; Kim6DoF; FaSTrack tracking; methods not reproduced/transferred. |

## Mathematical preservation and appendix interface

Keep equation labels `eq:turn`, `eq:wind`, `eq:stop`, `eq:objective`, `eq:required` in the main text so existing appendices retain their cross-references. Preserve all dynamics, endpoint constraints, parameter domains, rounded coefficient warnings and exact proof numbers in the appendices. Move `eq:box` to the ground-bounds appendix with its assumptions, along with joint-coverage versus marginal-interval distinctions. Keep `app:dynamics`, `app:polynomial`, `app:bounds`, `app:windbound`, `app:coefficients`, `app:ground`. Add compact historical-source and limitations records if needed; the complete audit must remain accessible.

## Caption policy

Each caption first says what the reader sees and how to read it. Then give source and the one or two definitions needed to interpret that visual independently. Photo date/orientation/rights, relative height datum, synthetic coordinates, digitization sensitivity and noncausal paired comparisons remain local. Repeated generic “not safety/not global/not reconstruction” catalogues disappear when the relevant model scope has already been defined. Technical source paths are in the figure provenance/report rather than typographically prominent labels.

## Editorial acceptance questions

Read only the first sentence of each paragraph: do they continue a physical investigation, or sound like a checklist? Read only the figures and captions: can a nonpilot distinguish the direction change, bank, flight phases, runway allocation and historical evidence? Read the conclusion after the opening: does it answer the same question without promising an unproved historical optimum? These are reader tests, not a substitute for numerical/source checks.
