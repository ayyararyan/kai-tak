# Version 4 visual diagnosis

Read and inspected 13 October 2026. This is the stage-1 design review, not the stage-6 acceptance result.

## Inspection record

All 35 pages of the actual V4 PDF were rendered with `pdftoppm -r 60 -png` and visually viewed, not merely inferred from LaTeX. Review renders: `qa/v4-visual-review/page-01.png` through `page-35.png`. All sixteen figures were inspected in their manuscript context; figure source and data paths were read. Original A36143 was additionally inspected at original-image detail. Supplemental source photographs A36142, A36144, CN4581 and CN4589 were viewed and SHA-256 checked against the committed aerial manifest. The settled open mesh's bytes were checked against the V4 HANDOFF, not selected from later experimental reconstruction.

## Verdict and ranked priorities

1. **The paper does not yet make the physical place legible.** Figure 1 shows important real evidence, but box labels hide part of it; Checkerboard Hill and the bay are missing from the visual argument. Figure 2 discards geography entirely. Readers first need to see why the runway and neighbourhood form a problem.
2. **The complete-landing scene conceals scale.** Figure 9 is a line in a perspective cage, with substantial vertical exaggeration and a compressed secondary plan. Neither threshold nor the physical interval consumed by braking has enough visual weight. Its plot title substitutes for a spatial explanation.
3. **Stopping distance has no runway.** Figure 8's separated bars prevent the eye from adding the distances. Figure 12's runway strip partly solves that, but puts it between two unrelated miniature plots. One scaled, continuous runway allocation should become the signature comparison.
4. **Photogrammetry is shown as a diagnostic output, not evidence of a place.** Figure 4's two tiny plan clouds cannot connect roofs and open ground to the original photographs. The copper supported region is barely legible. An authentic open-surface oblique view plus source crops can disclose both shape and incomplete support.
5. **The turning mechanism is invisible.** Figure 5 gives two families of curves before the reader has seen a banked wing, lift or centripetal acceleration. One physical diagram can earn the equations and the 2.32 km / 24.35 s result.
6. **Verification shows machinery instead of the idea.** Figure 10's interval-width stairs do not explain how a sampled path can fail. Use a named analytic teaching example with a between-sample violation and interval enclosures; retain the actual cover statistics in text/documentation.
7. **Figure/paragraph pacing is uneven.** The reconstruction discussion fills page 7, followed by a small reconstruction on page 8 and an almost half-empty remainder; Figure 12 is an isolated island at the top of page 19. Do not preserve old float barriers mechanically.
8. **There is too much small graphic type.** Plot fonts at V4 text width are substantially smaller than main text; six-panel Figure 11 and three-part Figure 12 need hierarchy. Source-heavy captions often have more visual mass than the figure's message.

## Figure-by-figure disposition

| V4 | Page | What works | What fails | V5 decision |
|---|---:|---|---|---|
| 01 Historical airport | 4 | Real dated aerial; proximity legible | Box labels; frame dominates without orientation/overview; no hill/bay link | New historical image composition with outside labels and separate, explicitly unregistered source views |
| 02 Approach geometry | 5 | Correct common magnetic bearings | Isolated rays plus generic process list; geography absent | Geographic-relations schematic and restrained bearing construction, no exact turn-site claim |
| 03 Dated maps | 6 | Same extent and three useful landmarks | Too small to inspect roof/street forms; numbered circles disconnected from evidence | One larger survey field plus matched detail windows, dates and source-bound landmark labels |
| 04 Reconstruction | 8 | Shows control-support asymmetry honestly | Dense cloud has no physical depth; evidence origin invisible | Source-photo pair, actual open mesh oblique view, separate control-footprint inset |
| 05 Turn physics | 10 | Checked radius and time curves | Two plots express the same formula; no force mechanism | Banked-aircraft force construction and equal-scale turning arc; small radius/speed cue only if needed |
| 06 Wind vectors | 11 | Correct vectors and signs | Awkward labels; component plot disconnected from aircraft direction | Two top-down aircraft orientations with identical wind arrow and component projections |
| 07 Calm profiles | 12 | Brief rise preserved | Generic stack and plot title lead; no connection to trajectory | Compact altitude ribbon and vertical-speed zero crossing beside/full local landing figure; retain speed if needed |
| 08 Stopping | 13 | Accurate decomposition and feasibility boundary | Separate bars are not spatial runway allocation | Replace with scaled common-axis runway graphic and concise speed-squared worked comparison |
| 09 Complete calm | 14 | Full path to stop; no historical false overlay | Empty cube, exaggerated height, tiny plan | True-scale projected local runway scene without cage; threshold/entry/touchdown, plan shadow and ground run |
| 10 Certificate | 16 | Actual accepted subdivisions | Main idea opaque to ordinary reader | Single sampled-curve versus enclosed-interval illustration; statistics separately sourced |
| 11 Wind profiles | 18 | Shows actual controls and limits | Six equally weighted mini-plots; too little hierarchy | Four aligned control strips or an appendix figure retaining all six quantities with readable typography |
| 12 Scenario comparison | 19 | Correct separate problem bounds | Three unrelated scales, cramped path, causal ambiguity unless caption read | Absorb physical comparison into stopping graphic; make bounds a lean dot-and-span plot or table |
| 13 Recorder | 21 | Source-linked manual observations; intervals retained | Three charts too uniform; raw-data impression from line density | Directly labeled traces with observed symbols prominent and thin joining lines; sensitivity key |
| 14 Weather | 22 | Sensor difference and selected annual sample | Two different clocks/evidence objects visually equal | Sensor evidence chart plus compact annual rank strip/CDF sidebar; clocks explicit |
| 15 Rollout | 23 | Strong counterintuitive necessary-deceleration result | Arbitrary equally spaced events feel time-indexed | Landmark table/paired aligned slope diagrams explicitly indexed by narrative event, not time |
| 16 Evidence synthesis | 26 | Honest distinctions | Generic process boxes; repeats much prose; no discovery | Remove as main-text figure; preserve all distinctions in scope/appendix record |

## Source and epistemic hazards found

- The original A36143 handwritten border visibly reads `3.11.93`; catalogue says `1993-11-02`. V4 correctly preserves this discrepancy. An older archive `VISUAL_OBSERVATIONS.md` says the dates agree; this statement must **not** be imported. Additional A36142/A36144 visibly read `2.11.93`.
- A36143 original scan has runway direction down-left; it is not north-up. Approximate frame catalogue bounds do not provide an orthophoto transformation. Do not place exact bearing vectors or the synthetic flight into this scan as if registered.
- CN4581 visibly contains the painted checkerboard. It is colour photography dated 8 October 1993, not the date of CAL605. CN4589 provides genuine bay/runway-end setting from the same October date; it is not an image of the accident.
- The full accepted mesh is available in the original archive and matches the V4 HANDOFF SHA-256. It is **open**, unclassified and referenced to a fitted local plane. Do not cap gaps, extrude roofs into solid buildings, flatten negative heights, or call its Z coordinate HKPD.
- The small control hull must be visible. Do not recolour the whole mesh as equally map-supported. A separate plan inset can show the full reconstruction and true supported region without swamping the main view.
- Use original public-data source attribution and ownership, not a new blanket licence. CAD report pages/images remain excluded; mathematical diagrams and manual numeric replotting are distinct from reproducing restricted report scans.

## Layout implication

Keep V4 RFS page geometry and Times body. Figures should be designed for the **actual text measure**, with sans-serif lettering at a readable final size; no dominant in-plot title. Figure labels identify physical objects; captions supply the question, interpretation and local source condition. Source legal prose should be concentrated into an adjacent rights note/appendix while retaining explicit source attribution in each affected caption.
