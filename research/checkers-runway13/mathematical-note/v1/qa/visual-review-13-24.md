# Independent rendered-page review: pages 13–24

Reviewed on 2026-10-14 (Asia/Kolkata) by the independent certificate/optimization reviewer.

## Scope and method

All **12 of 12 assigned pages** were individually opened with `view_image`, using the actual 1.4× rendered page images `qa/pages/page-13.png` through `page-24.png`. This was a visual inspection, not an inference from extracted text or compiler diagnostics. The checks covered mathematical legibility, equation numbering and clipping, theorem/proof breaks, figure labels and captions, and consistency with the independently audited mathematical statements.

The inspected 36-page PDF was `certified-local-optimality-v1.pdf`. After two page-break repairs, pages 13, 14, 17 and 18 were individually reopened and visually rechecked. The final reviewed PDF SHA-256 was `24965a9e628ce7f845870b0774e77d07911021e5a366dd8bf8fc033982dfda28`. The final page-13 PNG SHA-256 was `36c6ac74414647d0c559a03f055e81cf069c269fbd641c55d3801e0b8a41af8c`; page-24 was `69f3ad03667fea73d59bbd7af9d72bb34aa530c44cdacc6191e0f5c9a76a2a08`.

## Disposition

**Accepted for visual presentation within the reviewed scope.** No clipped equation, illegible mathematical symbol, overlapping figure label, or new mathematical/caption inconsistency was observed on these pages. Two local page-break defects found in the initial render were repaired by the production agent and independently visually verified in the final render:

1. **Pages 13–14, repaired:** the original single-word “are” orphan was removed. Page 14 now opens with the ordinary paragraph continuation “derivative. The six active margins are” immediately before equation (31). The complete introductory clause stays with its display.
2. **Pages 17–18, repaired:** the original mid-sentence split in the principal Theorem 2 was removed. The complete statement, displayed conclusion and proof now appear together on page 18. Page 17 ends cleanly after Table 3.

No actionable visual defects remain from this pass. No manuscript sources were edited by this reviewer.

## Page-by-page inspection record

| Page | Actual content inspected | Result |
|---:|---|---|
| 13 | Analytical-exclusion conclusion; Figure 2 family-value bracket and separate retention scale; start of Section 4; scaled root coordinates (30). | Figure bounds and caption are readable. Retention is correctly a rightward ray with no asserted upper endpoint. Root symbol and scale are clear. Re-viewed after the page-break repair: ordinary paragraph continuation onto page 14, no isolated active-margin introducer. |
| 14 | Six active margins (31); corrected gate/touchdown/interior slew signs; nine-equation root system (32); event times (33); fixed-time upper-support argument. | All equations, long values and equation numbers are readable and unclipped. Re-viewed after repair: introduction now stays with (31), with no lone-word orphan. |
| 15 | Figure 3 event-time structure; Section 5; exact root box (34); complete Theorem 1 statement and objective enclosure (35); proof opening. | Figure event labels are distinct, caption accurately says event-time positions, and stopping is distinguished as a terminal equation. Theorem statement fits intact. Its proof continues normally on page 16. |
| 16 | Krawczyk proof, equations (36)–(37), mean-value uniqueness argument; beginning of active-gradient simplex section and augmented matrix (38). | Long formulas remain within the text width, integral/matrix symbols are legible, and proof-ending square is correctly placed. No actionable defect. |
| 17 | Lemma 3, simplex certificate and residual bound (39); Table 3 multiplier intervals. | Table intervals and proof formulas are legible. Re-viewed after repair: page ends cleanly after the multiplier table; Theorem 2 is no longer split. |
| 18 | Complete Theorem 2, inequality (40), and full strict-local-sufficiency proof. | Re-viewed after repair: full theorem and proof fit together. Norms, compact-sphere argument and uniform-remainder estimate are clear. Proof terminates cleanly. |
| 19 | Figure 4 certificate proof-dependence diagram; Section 6; endpoint extensions of active margins; Lemma 4. | Diagram labels are readable, use the correct root symbol, and do not suggest a false dimensional projection. Both feasibility and gradient branches feed the final conclusion. Lemma statement is intact; proof follows with its table on page 20. |
| 20 | Table 4 event neighborhoods and derivative enclosures; Lemma 4 proof; interval-cover algorithm. | Two-line interval endpoints in the table are intentional and legible; derivative columns align correctly. Equations and narrative fit. Ordinary paragraph continuation onto page 21 is acceptable. |
| 21 | Corridor proof conclusion; gear-clearance factor (41) and lower bound (42); complete Theorem 3 and its proof. | Factor expressions and symbols are readable. The theorem, coverage counts, geometry/contact argument and proof-ending square fit without clipping. No new scientific inconsistency observed. |
| 22 | Stopping and forward-integration diagnostic; Figure 5 continuous margins and certified partition; Section 6.3 and full Theorem 4 statement. | Margin panels, active-neighborhood shading and objective reference lines are readable. Dense partition stripes are appropriate to the reported 366 flare cells; 32/366 labels are legible. Caption does not misidentify sampled curves as proof. Theorem statement remains intact; proof continues on page 23. |
| 23 | Full twelve-parameter transfer proof; Section 7; Proposition 5 retention statement and proof opening; long retention comparison (44). | Transfer equations and exact-decimal retention value fit within the text measure; equation number does not overlap. Proposition statement is intact. Proof continuation onto page 24 is conventional. |
| 24 | Retention proof conclusion and interpretation; sensitivity equation (45); affine known-wind construction (46). | Mathematical formulas, sensitivity status qualifier and wind-dependence text are readable. No clipping, broken symbol, or contradictory figure/caption claim observed. |

## Limit of this record

This report establishes visual inspection of pages 13–24 of the identified render. Mathematical validity is documented separately in `audit/certificate.md`; full build, font/page-size comparison, all other rendered pages and source-package reproducibility are covered by their own production and review records. A successful visual inspection is not a replacement for those checks.
