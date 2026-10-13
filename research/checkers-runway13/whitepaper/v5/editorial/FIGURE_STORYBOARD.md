# Version 5 figure storyboard

Stage-2 design plan; prototype implementation waits for the full main-text rewrite. No scientific inputs are changed.

## Production filenames and ownership

Main suite: `01_place`, `02_bearings`, `03_turn`, `04_landing`, `05_runway`, `06_maps`, `07_stereo`, `08_wind`, `09_certificate`, `10_recorder`, `11_weather`, `12_rollout`. Appendix: `A1_profiles` (complete calm kinematics and all six wind controls), optional `A2_bounds`. Historical lane owns `01_place`, `02_bearings`, `06_maps`, `07_stereo` and source assets. Parent owns remaining figures. This map replaces provisional IDs below without altering their editorial purpose.

Four prototype transformations therefore produce `01_place`, `02_bearings`, `04_landing` + `05_runway`, and `07_stereo`; `06_maps` follows after gate inspection.

## Visual language

Ink `#263D45`, slate `#63777D`, copper `#A65F3D`, sage `#72816A`, pale paper `#F3F1EA`. Assign meaning consistently: ink airborne motion/primary measured series; copper the geometric question or wind; sage stopping/reserve or supported evidence. Colour must never be the sole distinction. Arial/DejaVu Sans final figure type approximately 9–10 pt at document text width; tiny image credits belong in caption or provenance documentation. No generic rounded boxes, stock silhouettes, generative historical imagery or ornamental gradients. Vector PDF + SVG for diagrams, embedded unaltered raster sources for photographs/mesh, 600 dpi PNG presentation masters and 180–200 dpi screen derivatives.

## Four prototype gate

### P1 / GEO — A city, a hill, a runway

**Reader discovery:** the airport sits beside dense neighbourhoods, its turning reference is an actual painted hillside, and its runway reaches into the bay.

**Composition:** strong central A36143 view (airport/city), narrow source-photo inset of actual checkerboard in CN4581, small harbour-end inset from CN4589. Keep the frames separate, with source dates; do not stitch them into an invented seamless orthophoto. Fine leaders originate at manually inspected visible features and end outside image area. Label Kai Tak Airport, Runway 13 threshold, Kowloon City, Checkerboard Hill and Kowloon Bay only where respective frames support them. The airport photograph's original scan orientation stays explicit; no north arrow on unrectified imagery. Trim scan margins in view but retain complete originals and a source-ID/date inset where it aids the historical story.

**Inputs:** existing `inputs/A36143.jpg`; hash-verified archival `CN4581.jpg` and `CN4589.jpg`, with manifest metadata. **Acceptance:** labelled checkerboard visibly real, bay unambiguous, no invented coastlines/registered tracks, final-page labels readable.

### P2 / ANGLE — Two directions, one landing

**Reader discovery:** 47° is the difference between instrument and runway directions on a map, not wing bank.

**Composition:** a restrained geographic-relations plan, using source-bound airport/hill/urban context, plus a mathematically exact small bearing fan with `088° M`, `135° M`, `47°` and magnetic-north arrow. The geographic plan must be marked schematic unless a verified map transform is available. A separately labelled bend conveys visual transition only and must not claim a surveyed turning point/radius. The fan, not an unrectified photo overlay, carries exact angles. Prefer a visible runway strip/threshold over an isolated arrow. A tiny banked-aircraft end view crossed-reference to MECHANICS makes the meaning distinction without a paragraph in the figure.

**Inputs:** CAD Report 1/95 §§1.8.1, 1.10, Appendix 1 factual directions, accepted landmark/source metadata; do not reproduce report page raster. **Acceptance:** common magnetic frame exact; no 47° bank; no zero-visibility completion implied; heading/track equality never asserted in wind.

### P3 / LANDING and RUNWAY — The path ends after touchdown

**Reader discovery:** turn, descent, flare and ground travel are parts of one constrained motion; stopping occupies most pavement.

**Composition LANDING:** orthographic local-model scene, no coordinate cage, no city. True metre scaling in XYZ; runway plane with threshold and centreline, lightly projected ground shadow of the airborne path, sparse vertical drops at entry/threshold, touchdown and stop. Label 140 m entry height and 15.24 m threshold target where verified. Camera should reveal curvature without falsifying height. If true-scale height looks low, retain honesty and add a separately scaled altitude strip rather than exaggerating 3D. A generic aircraft shape may be a schematic orientation cue only, not modeled swept-volume geometry.

**Composition RUNWAY:** two aligned horizontal runway bands on the same 0–2,786 m station axis, calm and steady-wind scenarios. Distinguish threshold→touchdown, 2 s delay, braking and remaining runway, using true lengths; label stop stations and reserve. No independent bars that prevent addition. These are separately optimized examples, not causal wind-effect estimates. A small direct illustration of 10% speed → 21% braking distance can replace an entire extra subplot.

**Inputs:** unchanged `reference_formula.json`, `reference_outcomes.json`, wind `formula.json`, `result.json`; 0.15g, 2 s, 2,786 m. **Acceptance:** all stations regenerate from exact frozen inputs, one common scale, no metric-affecting artistic distortion, calm altitude rise retained in profile.

### P4 / STEREO — Two photographs acquire depth

**Reader discovery:** displacement between real photographs yields surfaces, while gaps and weakly controlled regions remain visible.

**Composition:** top rail of two matched original photo crops from A36142/A36143, with two or three verified corresponding points (existing manual labels, not new automatic identities). Main visual: actual accepted open mesh in a carefully composed oblique orthographic projection, restrained neutral shading/relative-height tint. Outline the small map-control support region in an adjacent plan footprint; omit artificial ground fill/caps. A small mapped inset or a pointer to the municipal-market feature makes the interpreted structure tangible. Never label a generic high patch as a named building without supported correspondence.

**Inputs:** A36142/A36143; `manual_stereo_labels.json`; accepted `observed_surface_mesh.ply` or faithful parsed geometry; `sparse_stereo_report.json` transformation and control hull; `historical_faces.geojson`, dated map. **Acceptance:** 155,891 accepted mesh vertices / 225,371 triangles; gaps remain open; no wall invention; 171,307 / 3,780 counts describe full data rather than plot subsampling; heights explicitly local-plane; photographic date discrepancy stays accessible.

## Remaining family after prototype inspection

| ID | Narrative position | Primary question and new form | Inputs / indispensable condition |
|---|---|---|---|
| MECHANICS | Act II | Why can modest bank accumulate 47°? Banked front silhouette with weight/lift components linked to top-view arc, radius/time numerical callout | `g=9.80665`, `V=78`, `phi=15°`; coordinated level-turn benchmark |
| MAPS | Act IV | Which shape belongs to which year? Enlarged October 1989 map field and aligned July 1994 detail windows at meaningful sites | Unchanged registered map crops and EPSG:2326 metadata; 0.25 m is spacing, not accuracy |
| WIND | Act V | Why does one wind act differently through a turn? Two aircraft/track axes at −47° and 0°, same true wind vector and perpendicular projections | 070° true / 21 kt; runway convention 133°10′ true; along/right signs preserved |
| CONTROL | Act V / appendix | What does the constructed motion demand? Aligned direct-labelled profiles with constraint lines and phase division | All six wind quantities plus calm rise/speed retained across final suite/text; sample plots not certificates |
| VERIFY | Act V | Why are dots insufficient? Clearly named analytic example whose between-sample peak crosses a bound; interval box/range enclosure beside it | Teaching example explicitly separate from actual flight; 2,502 calm and 376 wind interval counts remain exact in text |
| BOUNDS | Act V / appendix | How much has optimization located? Two separate problem brackets with filled achieved lower and open necessary upper ends | 0.0397 to <0.1559772; 0.1507934696816132 to 66656817/307536544; no confidence/global labels |
| RECORDER | Act VI | What does the historical plot actually show? Direct-labelled speed traces and lean altitude/heading aligned strips | Manual anchors and reading sensitivity; datum B; joining lines only guides |
| WEATHER | Act VI | Where and when was wind measured? Sensor sequences with explicit clock, annual distribution as compact separate context | A-field NW/LYM; selected 8,360 NOAA rows; no clock synchronization or aircraft-local wind |
| ROLLOUT | Act VI | How can slowing still leave a harder stop? Narrative-landmark speed/deceleration paired dot graphic, no artificial time spacing | Four report landmarks; zero and 2 s additional delay; necessary deceleration not actual brakes |

## Caption grammar

First sentence says what is visible and the physical relation. Second supplies necessary interpretation/scenario/datum. Final source credit is precise and short; full file/hash/rights chain is accompanying documentation. Do not repeat the entire model-scope disclaimer in each caption. Each first presentation must still correctly identify synthetic versus historical and separate optimized scenarios.

## Inspection gate

Before generalizing style, inspect P1–P4 at manuscript width and high-resolution source detail. Check: visual hierarchy, label collisions, scale, source precision, missing-data visibility and central question answered. Record concrete corrections. Then produce the rest and inspect every final PDF page. The prototype gate is an internal production gate already authorized by the brief, not a new user-approval requirement.
