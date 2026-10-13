# Independent final editorial read — Version 5

**Status: revised content accepted.** The final disposition at the end supersedes
the initial draft findings below, which remain as the audit trail.

## Review basis

Read after the first complete production build passed the technical gate (37 pages,
14 references, embedded fonts, no reported typesetting defects). The reviewer read
the complete abstract, foreword, seven-act main text and captions, and inspected
actual rendered PDF pages 1–12 and 20–21 at page size. All 15 figure-generating
masters were also read; figure source/geometry checks are separately recorded in
`qa/science_figure_semantics.json`. This is an independent agent editorial review,
not an independent human aerospace or historical peer review.

The following findings concern the reviewed production draft. They are proposals
for the production owner, not edits silently made by the reviewer. Final acceptance
requires checking their disposition and the regenerated pages.

## Verdict

**The strongest passages now read as a compelling, authored engineering
investigation, not a generic technical report. The manuscript is not yet uniformly
at that level.** The force-balance calculation, speed-squared stopping argument,
wind projection and “slower, yet with a harder stop ahead” passage create interest
through reasoning. The CAL605 account remains measured and causally disciplined.

The chief remaining weakness is Act IV. It offers a good historical opening and a
substantially better illustration, but the prose moves from generic stereo method
directly into control counts, residuals, datum distinctions and missing geometry.
The reader learns much more about what the reconstruction cannot establish than
about the actual roof features recovered. Several closing sentences elsewhere
still explain the exposition's value or announce its lesson. Those are localized,
correctable remnants of technical-report prose; passing the build cannot settle
this editorial judgment.

## Prioritized findings and concrete corrections

### E1 — Put one recovered historical object into the prose (high priority)

**Evidence:** Act IV, “Depth from a displacement,” PDF pages 11–12. The figure
already identifies Kowloon City Market and displays R = 10.77 m and S = 19.20 m.
The prose never follows those features through the two photographs. Instead it
immediately recites 1,318/171,307/3,780 points and then spends successive paragraphs
on horizontal/vertical error, open boundaries and incompatible datums.

**Proposed change:** replace the generic first paragraph of this subsection with
an actual feature correspondence, retaining the following explanation of camera
assumptions, point counts and support. A scientifically supported draft is:

> At Kowloon City Market, the roof feature marked R can be picked out in both
> photographs; S marks a rooftop service structure. Their displacement between
> the two images provides depth information. Once the camera geometry and metric
> scale are fixed, the corresponding sight lines constrain each feature's position
> in three dimensions. In the fitted-plane reconstruction, R lies 10.77 m above the
> local park/road plane and S lies 19.20 m above it. Both examples lie outside the
> map-control hull, a limitation that becomes visible when the reconstructed
> features are placed beside the controls.

These numbers and classifications are already accepted inputs (tracks 26 and
1135), not new reconstruction. Keep the local-plane/outside-hull qualification.
The following paragraph can broaden from those two concrete observations to the
1,318 sparse and 171,307 dense points. This gives the later limitations a physical
object to qualify instead of letting them dominate an abstract methods account.

### E2 — Repair two figure-induced sentence interruptions (high priority)

**Evidence:** page 2 ends “the accumulated result”; page 3 opens with the aerial
figure and its caption before continuing “of turning over time.” Page 11 ends
“A common vertical transformation”; page 12 opens with the stereo figure and
caption before “still has to be justified.” The important visual is physically
between the two halves of an unrelated sentence.

**Proposed change:** constrain the relevant float placement after Figures
`fig:place` and `fig:stereo`, or make equivalent local page-flow adjustments. The
stereo illustration should appear immediately after the concrete correspondence
and count paragraph, before the extended control-support discussion. Avoid
solving this by shrinking the imagery or its labels. Inspect the regenerated
pages; a float barrier alone is not evidence that the page flow improved.

### E3 — Define the first aviation term at first use (medium priority)

**Evidence:** the first narrative sentence, page 2, assumes the reader understands
“established on the instrument localiser.” The intended reader may know almost
nothing about aviation. A numerical bearing should follow a physical referent.

**Proposed change:** introduce the localiser as the radio-guidance beam, for example:
“At Kai Tak, following the localiser—the radio beam that supplied lateral
approach guidance—did not bring an aircraft straight down the runway.” Then retain
the 088°/135° magnetic directions and the visual-turn requirement. This defines
an object already used in the source; it does not imply guidance through the turn.

### E4 — Remove a small set of editorial self-commentaries (medium priority)

The explanation is generally strong enough without these lead-ins or justifications:

| Location | Current language | Proposed disposition |
|---|---|---|
| Act II after worked arc calculation | “The distinction is decisive.” | Delete; start with the concrete fifteen-degree distinction. |
| Act II, penultimate paragraph | “Its value is to replace an impression of impossibility with quantities that can be inspected…” | Delete this sentence. The calculation has already done that work. |
| Act IV, photograph date paragraph | “Keeping that small disagreement visible is part of keeping the source intact.” | Delete; preserve the date discrepancy itself. |
| Act IV, mesh paragraph | “The open surface is itself informative.” | Delete; start with the conservative mesh and its gaps. |
| Act V, final paragraph | “The gain from the certificates is specific…” and “With that mathematical object defined…” | State the established full-time constraints directly, then move to what the historical flight record contains. |
| Act VI, closing paragraph | “The engineering lesson is concrete.” | Delete; start with what touchdown passes to the ground system. |

These are prose cuts, not reductions in technical scope. Equations, numerical
claims, local scientific assumptions and source rights should remain untouched.

### E5 — Tighten the conclusion's last paragraph (medium priority)

**Evidence:** page 21 already has a complete synthesis and a focused account of
remaining research. The last paragraph revisits the dated city/calibrated
model/uncertainty list, restates the mathematical scope, then uses three successive
“ends/after” clauses. The final thought is sound, but its rhythm is overworked.

**Proposed change:** retain the positive result and its conditional domain once;
shorten the final movement. For example:

> Under the declared constraints, turn, descent and stop fit within one continuous
> mathematical construction. Connecting that construction to a historical landing
> requires the dated city and a calibrated aircraft. Kai Tak drew the eye to the
> turn. The calculation keeps following the aircraft until it stops.

This is an editorial option, not a required imitation of the reviewer. The final
sentence should end with the physical completion of the landing, not another
inventory of missing inputs.

## Scientific/display corrections found in this review lane

- **Corrected and source-rechecked:** Fig. 03 originally paired a right-bank front
  view with a left-turn plan arc. The plan now turns clockwise, with an exactly
  tangent exit arrow; force balance and the 47° angle agree.
- **Corrected and source-rechecked:** A1 used a three-dimensional velocity norm
  labelled ground speed. It now plots the horizontal norm and names it explicitly.
- **Corrected and source-rechecked:** Fig. 08 now labels the positive component
  “rightward wind,” avoiding confusion with wind *from* the right.
- **Corrected and visually rechecked:** Fig. 07 has positive camera-up direction,
  preserved open mesh geometry and an explicit outside-control-hull statement for
  both labelled roof examples. Fig. 02's previous label overlap is gone.
- **Needs disposition/recheck at this review timestamp:** A3's x-axis ended at
  18 m/s although the retained subset contains observations at 19.0 and 20.1 m/s.
  The axis must include the complete empirical support; no observation or count
  should change. The in-memory independent figure check detected this clipping.

## What should not be changed

Do not replace the clear stopping derivation with a qualitative summary; its
rectangle/triangle geometry is one of the strongest passages. Retain the
non-monotone rise, the two distinct certificates, the uncertainty categories and
the local noncausal interpretation of the scenario comparison. Do not dramatize
CAL605 or invent a personal experience to enliven the foreword. The foreword's
approval label is appropriate. No remaining issue here calls for new simulations,
an altered model or stronger historical claims.

## Initial acceptance boundary

Editorial acceptance is **pending targeted dispositions and regenerated-page
inspection**, not blocked on new research. The source arithmetic and interval
proof findings retain their separate tested status. Authorship cannot be inferred
from prose style; the assessment above answers how the document reads, and the
manuscript's AI-assistance acknowledgement remains explicit.

## Final disposition after revision — accepted

The production owner accepted E1–E5 and implemented them. The reviewer reread the
changed source passages and inspected the regenerated actual pages 2–3, 11–13,
22 and 37. The final inspected PDF has **38 pages**, SHA256
`9dc2957599405b9070741904f11074e12614d69ccb32c8b60c07a2a8836dc634`.

| Finding | Disposition and observed evidence |
|---|---|
| E1 — specific historical recovery | Closed. Page 11 follows Market features R and S through their image correspondences and names the accepted fitted-plane heights, retaining the outside-hull qualification. The subsequent support discussion now has actual objects to explain. |
| E2 — interrupted sentences | Closed. Pages 2–3 now place the aerial illustration between complete passages. The stereo float is bounded after the complete RMS paragraph: page 11 ends at a paragraph boundary, page 12 carries the intact illustration and open-mesh paragraph, and the datum explanation continues without an inserted figure. Some deliberate space remains before this full-width illustration; no imagery was shrunk to force it onto a crowded page. |
| E3 — first-use terminology | Closed. The opening defines the localiser through its radio beam and lateral-guidance function before stating the bearings. |
| E4 — editorial self-commentary | Closed. The identified generic lead-ins/justifications were removed or replaced by the physical/mathematical claim itself. The scientific conditions remain. |
| E5 — final paragraph | Closed. The conclusion retains the conditional positive result, then ends with following the aircraft to its stop. The repeated ending clauses and redundant research inventory are gone. |
| A3 empirical support | Closed. The x-axis now extends to 21 m/s and includes the observations at 19.0 and 20.1 m/s. Page 37 was inspected. No evidence values or counts changed. |

The separate scientific figure audit now passes **74 checks for all 15 masters**.
All 26 baseline displayed mathematical blocks and the byte-identical coefficient
table remain preserved. The 198-word abstract states the positive results and
scope without a catalogue of failed objectives.

**Final editorial answer:** the revised main manuscript reads as a compelling,
coherent engineering investigation, not predominantly as an AI-generated
technical report. Its best explanations let the mathematics produce the interest;
the historical section now follows a recovered object instead of only classifying
evidence. The technical appendices appropriately remain more documentary. This is
a critical reading judgment, not a claim that style proves human authorship or
that a human specialist has reviewed the paper.

**Acceptance:** the reviewed editorial/scientific content is accepted for this
V5 production scope. Final delivery remains conditional only on the production
owner's clean-package rebuild and matching-artifact checks. The personal foreword
still awaits Aryan's approval, as explicitly marked; independent human aerospace
and historical peer review has not occurred. Those are honest review boundaries,
not missing editorial implementation.
