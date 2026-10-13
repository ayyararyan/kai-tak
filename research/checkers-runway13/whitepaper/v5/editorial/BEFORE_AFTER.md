# Substantive prose transformations

Stage 3 main rewrite completed 13 October 2026. The source excerpts below are V4; the replacement excerpts are the new V5 manuscript, not aspirational samples. Equations and scientific meanings remain subject to the separate claim/source verification. The complete audit and destination map are `CAVEAT_AUDIT.csv` and `NARRATIVE_MAP.md`.

## 1. Begin with the physical puzzle

**V4 (`sections/part1.tex`):**

> From the ground, a large aircraft turning above a city looks like a contest between scale and space. At Kai Tak the setting made that impression unusually vivid.

**V5 (`sections/act1.tex`):**

> At Kai Tak, an aircraft established on the instrument localiser was still approaching along a direction that did not lead down the runway. The localiser pointed along 088° magnetic. Runway 13 lay along 135°.

The new opening makes the contradiction specific before interpreting it. It describes the localiser direction, not the aircraft's wind-dependent heading. Geography follows immediately, with the full-landing question in view.

## 2. Explain the two jobs of lift before writing the equation

**V4 (`sections/part3.tex`):**

> In a steady, coordinated, level turn in still air, lift must support weight and provide centripetal acceleration.

**V5 (`sections/act2.tex`):**

> In straight, level flight, lift supports the aircraft's weight. Tilt that lift vector by banking the wings and it acquires a horizontal component. The horizontal component bends the velocity; the vertical component must continue to support the aircraft. A turn is the simultaneous performance of those two jobs.

The model conditions remain directly before the equation. The added physical construction tells a reader what to look for in the force-vector illustration.

## 3. Let the worked example reveal the role of time

**V4 (`sections/part3.tex`):**

> The example explains how a visually substantial direction change can accumulate under a moderate bank, provided enough space and time are available. It does not show that this particular arc fits the historical approach.

**V5 (`sections/act2.tex`):**

> Fifteen degrees of bank does not produce fifteen degrees of total turn. It produces a turning rate. Here the rate persists long enough to accumulate the much larger change in direction.

The ideal-turn conditions and nonregistered benchmark status remain in the caption. The body gives the reader the mechanism instead of explaining the example's editorial purpose.

## 4. Derive stopping distance visually

**V4 (`sections/part3.tex`):**

> Let x_D be touchdown distance beyond the usable threshold, u forward ground speed, d a delay before braking and a>0 constant deceleration thereafter. The stipulated full-stop station is ...

**V5 (`sections/act3.tex`):**

> In a speed–time diagram the delay contributes a rectangle of area ud. Braking contributes a triangle with height u and base u/a, hence area u²/(2a). Adding the touchdown station gives ...

All variables and domains are still defined. The equation becomes a geometric calculation that a reader can reconstruct. This supports the scaled runway illustration and the later CAL605 discussion.

## 5. Replace a source-count opening with an archival question

**V4 (`sections/part2.tex`):**

> The project acquired 227 valid survey-map archives across 93 core sheet locations and 48 full aerial frames. These are substantial source holdings, but counts do not measure coverage of every obstacle.

**V5 (`sections/act4.tex`):**

> A current map cannot show a vanished building simply by being more detailed. For an approach in 1993, that absence matters: the object missing from today's image may be the object the aircraft had to pass.

The inventory remains in the technical source appendix. The narrative now creates a reason to inspect historical maps before reporting holdings.

## 6. Explain why incomplete geometry is visible

**V4 (`sections/part2.tex`):**

> Connecting points does not discover hidden building walls or fill an occlusion with evidence.

**V5 (`sections/act4.tex`):**

> Closing a hole with a plausible wall would make the scene easier to recognize, but the new wall would come from the illustrator. It would add no observation.

The scientific limitation is unchanged. The revised passage makes the distinction concrete enough to guide a reader's interpretation of the open surface, without reciting a general historical-clearance warning.

## 7. Introduce verification through an observable failure mode

**V4 (`sections/part4.tex`):**

> The project uses outward-rounded interval arithmetic. Instead of evaluating a state at one instant, the checker encloses its possible values over a closed time interval under the fixed source expressions.

**V5 (`sections/act5.tex`):**

> Between two accepted samples, a margin could briefly become negative. A curve can look smooth and a plot can look feasible while missing the very interval that matters.

The technical explanation follows and the exact two certificates are retained. The reader encounters the problem first, then the method that answers it. The illustrative curve is explicitly distinct from the certified landing references.

## 8. Let the official finding turn the historical story

**V4 (`sections/part6.tex`):**

> The official investigation supplies an unusually rich historical record, but also a warning against attributing an accident to the most visually dramatic part of the approach.

**V5 (`sections/act6.tex`):**

> The touchdown was controllable, and its parameters were not causal in the accident. The most conspicuous part of the approach was not, in the investigation's account, the part that determined the outcome.

The report's finding now carries the transition to rollout. Its official causes are retained, and the fixed-braking calculation remains clearly conditional rather than an accident-prevention claim.

## 9. Replace the public-archive prospectus with an engineering conclusion

**V4 (`sections/part8.tex`):**

> The immediate contribution of this project is an inspectable connection between source documents, dated geometry, a transparent mathematical model and reproducible calculations.

**V5 (`sections/act7.tex`):**

> Bank redirects lift; sustained turning accumulates direction; descent changes the energy balance; wind separates air motion from ground motion; touchdown commits the remaining pavement to delay and braking. Each stage constrains the next.

Rights, licence status, archive counts, file structure and invalidated-run history remain accessible in appendices/reports. The reader's final subject is the landing itself.

## Meaning clarification surfaced during rewriting

Parent verification of the frozen configuration found that V4's phrase “lateral route” could be read too narrowly. V5 now calls it a “400 m three-dimensional tube” around a fixed synthetic reference cloud, matching the existing three-dimensional nearest-distance calculation. This clarifies the inherited model's description; it does not alter the corridor, constraints, coefficients or certified results. The parent technical appendix retains the exact envelope and objective.

## Relocation ledger for parent integration

The `NARRATIVE_MAP.md` C01–C51 table is the complete requirement map. Main-text counts retained include 171,307/3,780/1,318 stereo points, 5.754 m RMS, 86,061 boundary edges, 24 readings/12sites, 190+35 digitization anchors, 225wind pairs,8,360annual subset and8,285/17/58rank. Technical appendices must retain:

- 227survey archives,93locations,48frames;404assignments/202templates,531regions,397overlaps;45dated forms/15names.
- 155,891vertices/225,371triangles;49-point correction and invalidated predecessor exclusion.
- 3,390m historical runway length distinct from3,331.5m runway and2,786mLDA;15ftAMSL=4.572m unaligned withHKPD.
- Full aircraft constants and numeric envelope;12parameter ranges;normalized margins; exact-decimal certificate binding versus rounded coefficients.
- All corrected calm/wind bound derivations;withdrawn0.10/0.05/0.04/0.03972 exclusions and checker repairs.
- NOAA8,549annual/24event-day rows;source/clock/raster conventions;source-specific touchdowns2300/2250/2210/2306m.
- Fixed-law CAL605 remainder decomposition166.51+249.69m relative to calm, not actual causation.
- Exact Cartesian-box stop/remainder/time extrema and assumptions;uncertainty categories and causal-policy quantifier distinction.
- Source rights/attribution/no blanket licence;build scope;AI-assistance acknowledgement;unfulfilled historical/operational programme components.

## Stage-3 editorial self-check

The abstract is approximately202words and the author-review foreword approximately235 words excluding its heading/label. The seven acts have been rewritten as continuous narrative, not rearranged V4 paragraphs. The full main text plus captions, formulas and LaTeX tokens is about6,900word-like tokens; the narrative itself is shorter. Seven numbered insight boxes, the executive-summary repetition and the main-text administrative flowchart are absent. The exact results and local measurement distinctions remain. Figure caption semantics still require integration against the actual new exports; final page pacing and an independent editorial read are not claimed complete at this stage.

## Final stage-3 tightening

Act VII was reduced to approximately 510 word-like tokens, concentrating on synthesis, a short attainment statement and two focused open-research paragraphs. The following passages were removed from its main-text draft for parent relocation into Appendix H, preserving C48/C49/C51 and the uncertainty distinctions:

**Related methods (retain citations):** Steady-wind Dubins-airplane planning studies geometry under restricted motion; richer six-degree-of-freedom landing models represent additional aircraft states; tracking frameworks such as FaSTrack explicitly connect planning to error bounds (`wu`, `kim`, `fastrack`). Each addresses a particular part of the problem. Adapting those ideas here would require checking their assumptions against this aircraft, these observations and this historical setting. Their algorithms/guarantees have not been reproduced or transferred by the present paper.

**Uncertainty:** A raster-reading range, a horizontal registration residual and an objective bound describe different objects. None supplies a prediction interval for a landing. The scalar stopping law admits exact extrema over a specified joint box of inputs, as Appendix F shows. The unresolved work is to justify such an input set physically and connect it to the full flight. A conditional outcome distribution requires validation; mean/parameter confidence intervals and marginal endpoint coverage are distinct from whole-flight joint coverage.

The figure05caption no longer repeats the numerical difference decomposition immediately given in ActV. Figure12caption retains source/category interpretation while the body supplies the quantitative progression. The first-person foreword's self-editing remark was removed. The geographic opening now describes three separate historical frames, including dated CN4581/CN4589, following the parent's verified source acquisition; it does not present them as a stitched panorama.
