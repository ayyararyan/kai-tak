# Review findings and decisions

Two independent native reviewers inspected code without inherited implementation context: blind defect review and edge-case review. The edge reviewer subsequently performed the source/artifact acceptance review against SPEC.md. It was not a third independent reviewer. `implementation.diff` preserves the pre-repair reviewed snapshot; current code and manifest are authoritative.

All substantive findings accepted as correctness repairs within the evidence contract; no model-meaning changes or new permission required.

| Finding | Repair and evidence |
|---|---|
| Null structure/permit keys could falsely join | Exclude empty keys, preserve raw records and explicit join issues; synthetic end-to-end fixture |
| Demolition followed by permit could falsely certify absence | Unresolved chronology/identity; regression tests |
| Last current status overwrote alternatives | Aggregate statuses and flag conflict; regression tests |
| Overlapping partial dates falsely conflicted | Interval comparison; exact day corroboration distinct from interval compatibility |
| Compact ISO date could miscompare lexically | Normalize query date before comparisons and output names |
| Missing geometry could crash classification/indexing | Retain unlocated rows and explicit flags; synthetic fixture |
| November edition could count as before November 4 | Month-end versus query; retain same-month candidates; five genuinely preceding editions added, total 227 |
| Cache receipt could claim deleted/changed archive valid | Recheck file existence and SHA; preserve invalidated files and acquisition attempts |
| Source matching could crash on null dates/geometries or zero output | Unresolved-input issue ledger and header-only empty CSV handling; seven matching tests |
| Tiny positive fractions rounded to zero | Preserve full floating-point area/fractions; final all-row positive-fraction invariant |
| Two key aerial transitions omitted from central CSV | Integrated A23632 and CN4581 observations; added Checkerboard landmark observation; 52 observations / 17 objects/sites |
| Same-month map editions tied | Coverage candidate selection uses edition and source-ID tie breaks, consistent with selected latest prior edition; test accepts exact-date alternatives |
| Comparison figure used false colours for single-channel images | Convert source display to RGB; visually re-inspected grayscale maps/photo. Source bytes unchanged |

The first parent selection regression failed because two map editions share June 1989: it demanded one particular ID rather than an acquired edition at the correct latest month. Source records were inspected; test now checks temporal evidence without inventing uniqueness. Matching uses edition tie-breaks. This was not a source acquisition failure.

The documentary agent rebuilt the complete database and both date exports. `structures/review_repair_impact.json` reports zero changes to prior classification fields for all 342,195 objects at both dates; the bugs matter for unsupported input combinations exercised by the new fixtures. Parent independently reran all 39 documentary tests and seven matching tests and reconciled final artifact counts. Acceptance limitations remain prominent in REPORT.md: current polygon count is not historical building coverage; no registered historical geometry, per-building heights or clearance certification.
