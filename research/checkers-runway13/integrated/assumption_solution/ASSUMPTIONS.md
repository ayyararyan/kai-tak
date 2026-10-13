# Assumption register A1

Every row is an assumption unless explicitly called an observed source dimension. Nothing here overwrites original unknowns. Parameter sweeps are deterministic scenarios, not confidence/prediction intervals. Baseline physical constants and original artifacts remain frozen.

|ID|Assumption/value|Rationale and sensitivity/domain|
|---|---|---|
|A01|Threshold EN838277.9926795285,820320.961097593; grid134.02°|Adopt existing northern interpreted pick and mapped axis despite failed historical registration. Frame scenario +80m along/−50m lateral is tested, not a hard error bound. True bearing133°10′ remains a separate wind-direction convention.|
|A02|Runway HKPD6m|Convenient common datum hypothesis;4m alternative tested. It is NOT a found AMSL conversion.|
|A03|All45dated source forms retained, with45mHKPDtops|Union across source editions deliberately conservative in footprint, NOT target-day verification. Roof_delta is a parameter. Duplicates are distinct source objects; no claim of45independent buildings.|
|A04|Hill observed extent plus50m expanded rectangle,140mHKPDtop|120m terrain+20m equipment assumption; spot observations are not maxima.|
|A05|Mapped light points expanded to4m×4m,12mHKPDtops|Shape and tops invented transparently as model assumptions, not data.|
|A06|Unknown urban area25m above runway;endsx=−600m;nearer cleared strip±100m|Makes finite complete assumed scene. Tests45/50/55/60/65mblankets. No obstacle-free historical corridor inferred.|
|A07|CG6m vertically above virtual reference; actualdensity evaluated atCGaltitude|Virtual point is not a body-fixed gear point. Constant inertial translation preserves force acceleration. Start/threshold CG146/21.24m; touchdown6m.|
|A08|Nongear bodyboxx[−40.8,30.2],y±32.7,z[−4,13.8] relativeCG|Planning dimensions motivate extent; precise in-flight geometry is assumed. Gear point plan fromBoeing7-5; CG22m aftnoseaxle, all contactz=−6m. No suspension flexibility.|
|A09|Pitch0; yawground-track; bodybank=liftbank|Explicit reduced pose closure. No calibrated AoA/sideslip/moment/control-surface dynamics.|
|A10|55mhorizontal boundingradius;+5mpositionbuffer;+3mverticalobstaclebuffer|Sufficient axis-separation test; source-independent engineering margins. Buffer15m tested. These are not probability intervals.|
|A11|Flat runway, nongroundbodyclearance≥.5m, ideal simultaneous wheel contact|CGsink−.7m/s is reset plastically; staticpose thereafter. Unlimited ideal contact impulse/adequate tyre authority assumed. No validated strut loads.|
|A12|Successfullandingmode, spoiler/brake availability, no disarm|CAD logic recorded separately; frozen2sdelay/.15g groundlaw remains stipulated. Engine6–10sresponse is not used to change it.|
|A13|Original mass,flaps30,gear-down,CD0/.045polar and all original force/rate limits|Promoted ONLY to assumed conditionalphysics, not empirical calibration. Mass/config domains beyond baseline are not solved by these cases.|
|A14|Constant knownwind suppliedpercase;zeroverticalcomponent|Calm; reportmeanvector;10ktheadwind;2/5kttailwind. Independent paths, NOT one causal gust policy.|
|A15|Syntheticentry(−2500,1000,140)virtual,−47°track; original400mcorridor|Explicit entryclass, mapped into assumed frame. Published IGS alternatives are not exhaustively solved. Corridor is an inherited objective constraint, not a surveyed restriction.|
|A16|Inherited12dimensional polynomialfamily, unchangedbounds|A computational restriction, not proof unrestrictedoptimum belongs to it. Fullclass and family upperbounds reported separately.|
|A17|Newsearches impose0.2mextra obstacle-only numerical guard|Conservative search margin introduced for tall-obstacle refinement; not included in objective. Acceptance/certification use original assumed hardgeometry≥0. Older candidate examples are validated against same targetgeometry.|

Uncertainty ranges are not distributions. Additional assumptions can be supplied through Case parameters, but a new condition requires fresh solution/validation; interpolation of example coefficients is not certified. Current loops use one process at a time for interval wind state.
