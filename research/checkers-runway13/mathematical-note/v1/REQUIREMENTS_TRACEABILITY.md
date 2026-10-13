# Requirement acceptance traceability

Authority: `SPEC.md`, transcribing the full author assignment. All 15 requirements are implemented and verified within the stated public-input scope. Excluded historical tests are not passes. Publication is a separate, unperformed action.

| ID | Requirement | Status | Manuscript / artifact | Acceptance evidence |
|---|---|---|---|---|
| M01 | Complete A1 model; distinguish V5 | Implemented | Section 2; Appendix A–B; `sections/model.tex` | `audit/analytical.md`, `audit/certificate.md`; canonical nonnegative forward predicate and exact stored corridor cloud |
| M02 | Analytical stopping, terminal, attainment and coupled bounds | Implemented | Section 3; Lemmas 1–2, Propositions 1–4; Appendix A–B | Independent derivations; fresh `verification/accepted/analytical-bounds.json`; all 4,096 exclusion cells |
| M03 | Exact root and nonsingularity | Implemented | Theorem 1; exact box in Appendix C; Appendix D | Fresh root certificate and full matrices in `verification/final/local_matrices.json`; printed decimals independently checked |
| M04 | Strict five-variable sufficiency | Implemented | Lemma 3, Theorem 2 and complete uniform-remainder proof | Positive simplex weights, augmented-matrix residual; independent optimization audit |
| M05 | Whole-time connected feasibility | Implemented | Lemma 4, Theorem 3; Appendix E | 398 accepted cells, 786 processed; event neighborhoods, omitted inequalities, geometry/contact audit |
| M06 | Non-strict twelve-parameter transfer | Implemented | Theorem 4 and dependence-based proof | Independent gate/flare dependency and uniform-in-approach review |
| M07 | Certified secondary retention only | Implemented | Proposition 5, equation (44) | Fresh lower evaluation at upper root endpoint minus 0.0001; no effort-optimality claim |
| M08 | Sensitivity, explicit wind family, conditions/open cases | Implemented | Section 7; Proposition 6; Appendix F | Three wind-domain certificates, ten condition certificates/replays; numerical derivative explicitly unvalidated |
| M09 | Complete research article and bibliography | Implemented | 36-page PDF, full LaTeX, eight appendices, bibliography | Theorem and citation audits, 47 automated source-consistency checks, independent manuscript review |
| M10 | Exact V5 format and notices | Implemented | Five byte-identical class/style files; `RIGHTS_AND_PROVENANCE.md` | `qa/format-comparison.json`, embedded-font checks; no installable proprietary fonts |
| M11 | Reproducible mathematical figures | Implemented | `make_figures.py`; six PDF/SVG/PNG figures | `FIGURE_PROVENANCE.md`; 18 export comparisons; visual/caption audit |
| M12 | Five distinct review domains and repairs | Implemented | `INDEPENDENT_REVIEW.md`; three detailed reviewer reports | Analytical, interval, optimization, physical-model and numerical passes; original failures retained |
| M13 | Fresh public checks; sealed-source preservation | Implemented | `verification/accepted/`, `frozen-source/` | 117 tests; all seven replay stages; 487 exact source files; seven explicit exclusions |
| M14 | Complete publication package | Implemented | PDF, sources, pins, reports, claim ledger, provenance, README, source ZIP | `PACKAGE_MANIFEST.json`, `DELIVERY_MANIFEST.json`; final ZIP member checks |
| M15 | Clean build and exhaustive production review | Implemented | `REPRODUCIBILITY.md`, `qa/` | Fresh environment/extraction build; 36-page text/pixel comparison, 18 figure exports, all 36 pages visually inspected |

Correctness: independently derived logic and fresh executable evidence, not merely successful compilation. Completeness: 15/15 required components. End-to-end readiness: local build, reproduction and package verified; external publication intentionally not performed. Unapproved model changes and scope reductions: zero.
