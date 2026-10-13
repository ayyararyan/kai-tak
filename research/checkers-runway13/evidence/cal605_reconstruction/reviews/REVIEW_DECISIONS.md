# Review decisions

13 October 2026. Three independent lanes: blind code/analysis hunt, edge-case hunt, acceptance audit. These reviews are evidence checks, not physical aviation certification.

| Finding | Decision and repair | Verification |
|---|---|---|
| Final-coordinate interval reaches runway end; upper required deceleration unbounded | Accepted. Added explicit unbounded/domain status, not an unexplained blank. | Actual last-anchor regression test. |
| Figure band omits x sensitivity | Accepted. Label now says vertical reading sensitivity only; horizontal intervals remain in CSV. | Figure regenerated and inspected. |
| Parent producer ignores anchor calibration metadata | Accepted. Axis, provenance and sensitivity fields are read from anchor JSON. | Axis tests, inspected code and regenerated outputs. |
| Required-deceleration accepts nonfinite inputs | Accepted. Finite-domain guard; deliberate infinity only for exhausted distance after delay. | NaN and exhausted-distance tests. |
| Wind documented null input crashes derivatives/plots | Accepted. Independent null propagation, dynamic counts, sparse/all-missing behavior and prewrite staging. | Eleven tests; original actual observations unchanged. |
| NOAA changed source/station/year can enter ranks | Accepted. Pinned archive identity plus all-record station/year/header validation before writes. | Twelve tests; both CSVs unchanged after repair. |
| Clock called explicitly unsynchronized | Accepted wording correction. Separate internal clock with unknown offset, not proved nonzero offset. | Report wording changed; clock ledger preserves available approximate ATC event anchor without a sample join. |
| Flight source replacement with unchanged hardcoded pixel anchors | Parent extension of source-identity audit. Pin inspected PDF/rasters before regeneration. | Final flight test receipt records source-substitution checks. |

Acceptance reviewer found no blocking scope/numerical issue in the selected benchmark. It independently checked source overlays, consequential narrative/wind values, all 34 explicit segments, and 10,000 anchor-perturbation distance integrals. That sampling is a diagnostic, not a theorem of physical accuracy. Its 39-test count describes the pre-final-flight-source-guard run; final total is in `../verification.json`.

No finding required changing aircraft configuration, the nominal objective, braking parameters, terrain work or the meaning of a CI. No review finding was hidden by widening physical error bars or claiming a source discrepancy had been resolved.
