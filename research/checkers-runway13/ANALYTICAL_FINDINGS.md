# Analytical investigation: what we can now prove

13 October 2026. Research finding, not an operational landing procedure.

**Later full-landing continuation:** see `analytical/coupled/START_HERE.md`.
A complete nominal candidate now has an all-time interval feasibility certificate,
and existence of an optimizer is proved within the fixed polynomial family.
The optimizer itself and a full closed-form optimal landing remain unidentified.
The restricted analytical results below are preserved, not replaced.

## Answer

Yes: the analytical attempt has produced an exact, position-constrained solution in a restricted trajectory family. It is not a numerically fitted curve. It does **not** yet establish the globally optimal Kai Tak landing, historical superiority, or a completed historical terrain reconstruction. The numerical scenario model v1 is unchanged.

## Exact result

Consider a no-wind straight–constant-radius-right-turn–straight path, with instantaneous bank changes, horizontal speed U fixed, heading change δ in (0,π), forward displacement X and initial lateral offset y. Define A=tan(δ/2), B=2A−δ>0 and C=X+yA. Endpoint matching gives

    s(R) = y/sinδ − R A
    ℓ(R) = X − y cotδ − R A
    D(R) = C − B R
    Rgeo = min{y/(1−cosδ), (X−y cotδ)/A}.

Nonnegative straight lengths and an independently specified positive minimum radius require Rlo≤R≤Rgeo. If this interval is empty, this family is infeasible; other families are not thereby ruled out. At fixed horizontal speed, time D/U decreases with R. Level-flight peak bank also decreases with R, so the largest admissible radius is the exact global optimum **within this family** for either criterion.

Descent changes the result. With fixed altitude loss H and fixed descent angle γ<0, D=H/(−tanγ) fixes R uniquely: there is generally no remaining radius to optimize. If H is fixed but constant descent slope is allowed to vary across candidates, the minimum-bank problem has a unique stationary solution:

    D₀³ + 2H²D₀ − CH² = 0
    D₀ = 2H√(2/3) sinh[asinh(3√3 C/(4√2 H))/3]
    Rbank = clip((C−D₀)/B, a, b).

Here H>0 and [a,b] is a nonempty positive-radius interval after geometric and slope restrictions. H=0 uses the level result. This is an explicit expression, not numerical optimization. The full proof, domains, force-balance assumptions and degeneracies are in [the derivation](analytical/ANALYTICAL_TRACTABILITY.md).

The altitude-coupled comparison frees vertical velocity, flight-path angle and total airspeed across candidates. It is **not** a same-initial-state competitor to numerical model v1. Minimum time and minimum bank can disagree. Neither objective replaces v1's full-landing nominal constraint-margin objective. No numerical bank-angle comparison between these different models establishes improvement.

## Verification and independent challenge

The derivation was checked by the parent and an independent proof reviewer. No fatal error was found in the stated restricted results. The verifier passed 80 constructed synthetic cases, two deterministic examples, four explicit domain rejections and additional descent branches. Worst endpoint quadrature residual was about 1.05×10⁻¹⁰ m; normalized cubic residual about 7.36×10⁻¹⁶. These quantify floating-point algebra checks, not aircraft or historical-data accuracy. Proof, not these samples, supplies within-family optimality.

Accepted review qualifications: a zero-distance straight endpoint is zero-duration, not positive-duration flight; the helper geometry function is not a complete feasibility validator; extreme floating-point parameter regimes are not certified. No changes to the frozen simulator were required. No literature novelty is claimed.

## Historical reconstruction: concrete sources, still missing geometry

The [Lands Department aerial archive](https://www.landsd.gov.hk/en/survey-mapping/mapping/aerial-photo-photogrammetric-products/aerial-photo.html) and [digital aerial product documentation](https://www.landsd.gov.hk/en/survey-mapping/mapping/aerial-photo-photogrammetric-products/digital-aerial-photo.html) establish a route to historical film scans and, where available, camera calibration. Exact dated 1993 approach-area frames and full-resolution stereo imagery have not been acquired. Two small third-party 1993-labelled previews were inspected, but are not authoritative terrain or height data.

Two substantive official datum PDFs were downloaded. [Geodetic explanatory notes](https://www.geodetic.gov.hk/common/data/pdf/explanatorynotes.pdf) establish that Hong Kong Principal Datum is not mean sea level. The correct relationship to the 1993 aviation chart's AMSL reference remains to be established; a modern numerical offset must not be silently applied. True, magnetic and grid bearings also remain separate.

The existing CAD Report 1/95 and its approach chart remain the primary historical procedure evidence. No additional raw routine-flight records or contemporary airline landing manual were acquired. Published accident-recorder plots are neither raw records nor representative normal landings. The 1993 reconstruction epoch remains a stated working assumption.

See [source report](reconstruction/SOURCE_REPORT.md), [inventory](reconstruction/source_inventory.csv) and [retrieval ledger](reconstruction/retrievals.json). All 29 locally downloaded/extracted artifacts passed their stored SHA-256 checks. This count includes explicitly excluded error pages and does not mean 29 usable datasets. The delivery archive excludes downloaded third-party imagery and source PDFs; it contains our notes, code and source references.

## What prevents a full closed-form claim

The current family omits finite roll, variable speed, force/slew envelopes, flare, contact/braking, dated obstacle clearance, go-around viability and uncertain-wind feedback. A family restriction is not automatically a relaxation of the full problem, so its optimum is not automatically a full-problem lower bound. Necessary optimal-control equations alone would not establish global sufficiency either.

[Wu and Chen's primary paper](https://arxiv.org/abs/2412.04797) addresses constant-speed, altitude-hold steady-wind planning. Some candidate families reduce to quadratic equations; others require transcendental roots. It is useful precedent for analytic characterization, not a full finite-roll landing solution. Parent web inspection confirmed this distinction; no exhaustive novelty search is claimed.

## Next mathematical and evidence gates

1. Extend position matching to finite roll while holding the same full entry and terminal states. Integrate the displaced turn itself; adding a roll-time penalty to the circular solution is invalid. Distinguish elementary expressions, special-function/quadrature representations and implicit switching equations.
2. Identify exact dated aerial frame IDs and historical survey-sheet editions before purchases or claims of reconstruction. Reconcile datums, retain uncertainty and missing cells, and reconstruct terrain separately from historical roofs/obstacles. Clearance must eventually apply to aircraft swept volume, not just its centre of gravity.
3. Establish a sufficient global certificate for the chosen full-landing objective, or report the precise restricted domain for which one is possible. Use numerical v1 to challenge candidate constructions, not as a substitute for proof. Historical-path confrontation and any superiority claim remain dependent on missing flight evidence.

**Status:** restricted analytical result derived, tested and independently reviewed; source acquisition documented; full analytical Kai Tak landing, historical terrain reconstruction and historical comparison **incomplete**. No proof of impossibility is claimed, and no full closed form is promised.
