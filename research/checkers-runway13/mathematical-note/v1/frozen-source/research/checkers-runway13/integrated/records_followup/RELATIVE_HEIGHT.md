# Common-frame relative-height route: dependency assessment

Prerequisite geometry analysis only; no frame adopted, no gate relaxed and no downstream optimum derived.

## What cancels exactly

Let H_i be an obstacle top and H_R the explicitly identified runway reference point, both orthometric heights in the **same realization** at the relevant epoch. Define h_i=H_i-H_R. An unknown *common additive* datum constant c cancels: (H_i+c)-(H_R+c)=h_i. For an aircraft reference path z(t) above R, its world height is H_R+z(t); body/obstacle clearance depends on z(t)-(H_i-H_R) plus the attitude-dependent body support term. A global vertical translation leaves collision geometry invariant.

Thus a supported runway HKPD level plus supported obstacle HKPD tops can establish relative collision geometry without converting the aviation “15 ft AMSL” declaration. The declaration may then serve as an independent cross-check, not the construction's anchor. This is a potentially valid route within the requested common-frame research, **not an accepted replacement frame today**.

## What does not cancel

1. A runway level observed at another point: h_i=(H_i-H_P)-(H_R-H_P). Without the surveyed P-to-R difference, runway slope/position remains unknown. An aerodrome elevation is not automatically the threshold level or a flat-runway elevation everywhere.
2. Different survey realizations: if H_i=Z_i+c_i and H_R=Z_R+c_R, the error contains c_i-c_R. The word “HKPD” alone does not bound monument movement, leveling error or survey epoch changes.
3. Local stereo relative to a fitted road plane: scale, tilt and vertical translation remain to be calibrated. In a simple affine vertical relation H=a*z_stereo+b*E+c*N+d, subtraction removes d only. Scale a and tilt b,c remain, as does the runway's coordinate/height in this model. The existing park-road reconstruction does not include a supported runway tie.
4. Absolute barometric/procedure heights and atmosphere: geometric datum cancellation does not establish the 1993 QNH/AMSL realization, a historical IGS altitude interpretation or a calibrated atmospheric density. Those need separate source support where used. Frozen model density law and thresholds are unchanged.
5. Unknown tops and epoch persistence: a ground spot is not a roof/equipment maximum. A November 5 survey needs a documented link to November 4 geometry; post-accident pavement/objects may differ.

## Uncertainty algebra, not supplied bounds

For genuine source-backed hard intervals H_i in [l_i,u_i], H_R in [l_R,u_R], the conservative relative interval is [l_i-u_R,u_i-l_R]. Shared additive error should be represented jointly and cancels exactly; independent intervals can be unnecessarily wide. If either bound is absent, this expression gives no finite certified interval. RMS residuals do not supply hard intervals. If statistical errors and covariance are justified, Var(H_i-H_R)=Var(H_i)+Var(H_R)-2Cov(H_i,H_R); there is no numerical CI here because the required joint model is absent.

## Minimal observations and exact benefit

| Observation | Resolves | Does not resolve |
|---|---|---|
| Dated threshold/end coordinates plus declared-distance/light plan | Endpoint identity and runway axis; checks the conditional 61m semantics | Vertical datum, obstacle tops |
| Threshold/reference HKPD level tied to stable benchmarks, plus runway profile | Vertical anchor and local runway geometry for same-frame relative construction | Approach roof/equipment heights or aviation altitude realization |
| Survey control schedule for drawing 115-93 A | Original survey coordinates/heights and potential independent control | Automatically the declared-end identity, all approach obstacles or pre-accident persistence |
| Dated obstacle top/profile survey in common frame | Relative height at measured objects, subject to bounds/coverage | Unmeasured roof equipment, missing buildings or aircraft occupancy |
| At least four full-rank control observations for the affine stereo-height example, with independent check points | Identifiability of a,b,c,d in that stated diagnostic model | Camera-model validity, hard error bounds, occluded tops, coverage |

No numerical observation acquired in this continuation closes these rows. The inspected runway_spot_candidates.png contains dot/H-like symbols, not numerical runway elevations. Existing mapped hill levels are approximate and do not anchor the runway. GEO-02 stays Blocked; no certified condition cell is added.
