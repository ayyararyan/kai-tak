# Visual and scientific QA — atlas v1

Verified 2026-10-13T17:46:08.583641+00:00. **Local author-review delivery.** All twelve plates exist and have been inspected. The atlas is a bounded archaeological/architectural presentation of the surviving evidence, not a complete calibrated historical city or a recovered cockpit scene.

## Verdict: distinguish the three questions

- **Correctness:** 157 automated acceptance checks passed, zero failures. Twelve additional gallery state-logic checks passed using a minimal DOM stub. JavaScript syntax passed `node --check`.
- **Specification completeness:** all twelve subjects have rendered, source-bounded alternatives, with required scenes, scripts, camera/source records, comparisons, formats and gallery. Seven of eight requirement groups implemented; VAL-01 remains partial solely for actual browser acceptance. Historical data gaps are disclosed source limitations, not filled with invented architecture.
- **End-to-end readiness:** real-source preparation, Blender rendering, composition and static gallery generation ran successfully. Two representative fresh-process Blender rebuilds exactly matched decoded RGB pixels. Browser layout and interaction remain **unverified**. Publication-quality aesthetic approval is reserved for the author; no independent museum/exhibition acceptance is claimed.

## Geographic and source checks

Original inputs: 25 current SHA256 matches. Archived restoration: 1,254 members across five existing data bundles, using the repository's archive/member verification workflow. Full mesh: 155,891 vertices / 225,371 original triangles. Independent binary GLB decode compared all coordinates and original triangle indices: maximum coordinate difference 0.00006104 m. The source Y-up convention maps correctly to Blender east/north/up. Close core: 36,108 vertices / 52,230 unmodified source triangles.

Forty-five historical faces retain unknown heights. No historical solid heights were invented. Modern courtyard-safe roof area error was below 3e-12 square metres on the audited data. Airport-wide modern geometry contains 3,546 valid polygon components with 167 explicitly omitted records. No modern skyline is relabelled 1993. Relative stereo and absolute HKPD heights are not fused. Vertical exaggeration is 1.

Mapped runway-edge direction is approximately 134.02° grid, with 61 m edge separation. Magnetic 088° and 135° arrows form a separate educational diagram; they are not map-grid vectors or a flown path. Physical runway total length is not inferred from the 2,786 m landing distance available. Threshold registration discrepancies of 77.62/81.54 m remain unresolved. Wide map editions span 1986–1993. Source dates and rights are recorded in the source register, including the A36143 correction history.

## Image-by-image inspection

Every principal plate was inspected at ordinary reading size; native-pixel source/detail crops were also inspected for source geometry, map registration and render artifacts. Final mode variants, daylight alternative, social crops and an A4 layout were inspected in a derivative sheet. All print/WebP exports are generated from the same inspected plate pixels; their dimensions and metadata are checked programmatically.

| Plate | Inspection result and bounded interpretation |
|---|---|
| 01 Overview | Dated oblique map geography and labelled missing tile, not a fabricated solid Kowloon skyline. Essential landmarks readable. Map ink contrast improved without adding source detail. |
| 02 Runway / water | Source runway edges and partial mapped shoreline remain on map evidence. No arbitrary water elevation or inferred full coastline; LDA distinguished from physical runway length. |
| 03 City beneath | Original broken surface remains visible with 100 m projected horizontal scale. No filled roofs/walls; display support is not historical terrain. |
| 04 Checkerboard Hill | Sparse 1989 contours/spot heights retained. Later terrain context is a separate panel, with a georeferenced locator. Evidence mode removes later terrain. Exact painted checkerboard face remains unresolved. |
| 05 Virtual perspective | Low illustrative camera exposes incomplete surface texture. Framing intentionally extends beyond patch boundaries; no historical aircraft pose, visible runway or recovered cockpit claimed. |
| 06 Alignment | Mapped airport and restrained magnetic-course diagram are separated. Evidence mode removes schematic arrows. No zero-visibility or actual flight-path implication. |
| 07 1989 | Reviewed faces sit on correctly dated, registered map context and remain flat. Linework is legible at publication resolution. |
| 08 November 1993 | Full original mesh shown without remeshing or artificial walls. Warm and daylight views share the camera and geometry. Source holes, disconnected fragments and extrapolation remain visible, not cosmetic defects to conceal. |
| 09 Across the nineties | Four dated panels preserve different evidence depth and matched geographic view. No artificial temporal continuity or demolition date inference. |
| 10 Then / now | Matched geographic camera/extent; modern panel uses modern buildings only. Historical map is visibly a different evidence type. No operational airport shown in the modern panel. |
| 11 Evidence chain | Actual source photograph and corresponding surface/map controls use marks 26,708,1135. Marker visibility improved after panel fitting. Photo is not labelled orthorectified; map has its own epoch. |
| 12 Synthesis | Panorama recomposed to reserve a separate readable map inset without covering the surface. Inset heading contrast corrected. Evidence mode removes inset. It is a framed synthesis, not a seamless calibrated landscape. |

No observed accidental clipping of the intended principal subjects remains, except deliberate close perspective/crop boundaries. No known render-generated floating modern buildings, water-level errors or fabricated terrain seams were found. Broken stereo fragments and sparse hill observations are source limitations. The neutral display plane, shadows and warm light are artistic presentation choices. No historical weather is reconstructed.

The wider historical scenes cannot provide a complete photorealistic skyline under this archive. Their map-board and separately framed alternatives are deliberately explicit about that evidentiary limit. Plate08 is the strongest source-led hero; plate12 should not be sold as a complete geographic reconstruction.

## Reproduction

Blender 4.5.3 LTS, EEVEE, 48 samples, 3840×2160 base renders. Official ARM64 distribution SHA256 verified. External preparation/composition uses Python 3.14.6; Blender embeds Python 3.11.11. Exact library versions are recorded in metadata.

Fresh-process replays of `08-november-surface` and `10-modern-core` returned zero with **all decoded RGB pixels identical** to production. PNG byte containers differed; this is not a cross-platform or cross-version bitwise guarantee. A deliberately incorrect source checksum exited1 without emitting a render. Unknown job IDs fail explicitly. Assembly checks declared original hashes, prepared-asset hashes, render PNG hashes and current job hashes before accepting images.

Independent blind, edge-case and acceptance review findings were assessed and repaired; see `REVIEW_DECISIONS.md`. Review is supporting criticism, not proof of scientific completeness.

## Browser blocker / outstanding acceptance

The available OpenClaw browser rejected file navigation with `unsupported protocol "file:"`; the normal localhost preview then failed with `browser navigation blocked by policy`. No bypass was attempted. Static asset links, JavaScript syntax and mode/download/navigation state logic pass, but these do not establish browser layout, keyboard behavior, focus handling or image decoding. See `browser_verification.json` and `gallery-state-check.json`.

Remaining acceptance: open the local `gallery/index.html` in an authorized ordinary browser, inspect desktop/mobile layout, exercise both modes and full-size viewer/downloads. No external hosting is required. At the original QA boundary nothing had been published or pushed. GitHub publication was subsequently authorized; this does not resolve the browser acceptance gap. No peer-machine sync is included.

## Evidence files

`acceptance.json`, `reproducibility.json`, `gallery-state-check.json`, `REVIEW_DECISIONS.md`, `contact-sheet.jpg`, `full-resolution-details.jpg`, `derivatives-contact.jpg`; per-render camera/source metadata; `../metadata/artifact_manifest.json`.
