# Publication-readiness checklist

Version 1 · 14 October 2026 · prepared locally for author review.

## Scientific acceptance

- [x] Current main inspected before source freeze and checked again before final packaging.
- [x] All 15 authorized requirements traced in `REQUIREMENTS_TRACEABILITY.md`.
- [x] A1 assumptions, frame, geometry, contact and polynomial domain stated without mixing V5 coefficients.
- [x] Analytical results reconstructed; all principal claims have proofs or identified computer-assisted proofs.
- [x] Exact root box, nonsingularity, positive simplex and uniform-remainder sufficiency checked.
- [x] Continuous 398-cell coverage and the twelve-parameter dependency argument audited.
- [x] Secondary retention distinguished from effort optimality; sensitivity distinguished from a rigorous enclosure.
- [x] Three wind domains and ten condition certificates reproduced; three unresolved cases retained as open.
- [x] All seven public replay stages passed; 117 tests passed, seven unavailable/inapplicable tests excluded explicitly.
- [x] Failures and repairs recorded without altering sealed results.
- [x] Independent analytical, interval, optimization, physical-model and numerical review completed.

## Production acceptance

- [x] Finished 36-page PDF, editable LaTeX, bibliography and exact V5 production styles.
- [x] Six reproducible figures, vector PDF/SVG and PNG exports, input/provenance manifests.
- [x] All mathematical labels, references, units, numerical rounding and figure-caption claims checked.
- [x] No unresolved references, missing characters, overfull boxes or physical-page overflow.
- [x] Times 12 pt / NewTX / 14.4 pt baseline and V5 page geometry verified against the reference PDF.
- [x] All 36 rendered pages individually inspected; identified page-break/command-wrap defects repaired and rechecked.
- [x] Clean source extraction and fresh Python environment build completed; page text/pixels and figure exports compared.
- [x] Frozen-source hash validation, source ZIP member verification and deterministic packaging completed.
- [x] Copyright notices retained; no installable proprietary fonts or restricted originals packaged.

## Publication boundary and remaining science

The manuscript and package are ready for the author's publication decision. No push, tag, GitHub release, existing-release change or external communication has been performed by this task. These remain subject to the author's explicit final approval, as requested in the assignment; no additional technical work is being withheld pending that decision.

The unmatched global-family gap, secondary-effort optimality, quantitative local radius, rigorously enclosed sensitivity, active-regime partition and unresolved conditions are open mathematical questions, not failed production requirements. Formal-kernel verification and human specialist peer review are not claimed.

Suggested release title: **Mathematical Note v1 — Certified Local Optimality in a Constrained Landing Model**. Draft release text is in `RELEASE_NOTES.md`. Actual asset hashes are in `DELIVERY_MANIFEST.json`; this file does not itself authorize publication.
