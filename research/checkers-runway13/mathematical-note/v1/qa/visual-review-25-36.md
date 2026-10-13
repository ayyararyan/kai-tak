# Visual review: pages 25–36

**Method:** each of the twelve individual PNG pages was opened with `view_image` and visually inspected at the supplied rendered resolution; this was not a text-only or contact-sheet review. No LaTeX/source edits and no mathematical/proof reruns were performed.

Final reviewed PDF SHA-256: `24965a9e628ce7f845870b0774e77d07911021e5a366dd8bf8fc033982dfda28`. Initial review PDF: `8d1acbe45f2641f29781aecd304900c9f88ac8c25851b44f7545c05c1211d8ed`.

**Final verdict: PASS, pages 25–36.** Page 34 was visually reopened after the shell-continuation repair; all other page PNG hashes remain byte-identical to the individually reviewed originals.

Review recorded UTC: `2026-10-13T19:08:46.220220+00:00`.

## Page-by-page record

| Page | Content seen | Verdict | Observation |
|---:|---|---|---|
| 25 | Proposition 6; wind-domain table; proof and condition-section opening | PASS | Table 5 is legible; displayed enclosure formula and proof-ending square fit; section7.3 does not strand a heading. |
| 26 | Table 6 and Figure6 condition results | PASS | All ten rows and bars are distinguishable; values, units, axis ticks and unresolved-case labels are readable. Chart has no invented frontier or numerical bounds for unresolved cases. Caption fits. |
| 27 | Frame-shift qualification and discussion | PASS | Dense prose remains readable; heading and all paragraphs fit without footer collision. Global-gap decimal is intact. |
| 28 | Appendix A polynomial construction and rational bounds | PASS | Hermite/Bernstein formulas, binomial notation and long rational numbers fit. No equation-label collision or clipped denominator. |
| 29 | Appendix A close and Appendix B inverse dynamics | PASS | Long rational inequality and two-column derivative displays fit. Subscripts, overdots and signs remain clear; appendix heading is well separated. |
| 30 | Appendix C exact root and fixed-approach data | PASS | All nine long root-box centers and seven approach entries visible. Both long primary-box endpoints fit on one line each. Monospaced table is small but readable; no lost sign/digit. |
| 31 | Appendix D interval AD and Taylor jets | PASS | Reciprocal/square-root/exponential recurrences have clear fraction bars and summation limits. Concluding matrix-export paragraph is intact. |
| 32 | Appendix E algorithm and Appendix F introduction | PASS | Five numbered algorithm steps are aligned and readable. Lower whitespace arises because the long coefficient table begins next page; no isolated heading. |
| 33 | Table A2 and Appendix G chronology | PASS | Exact wind-family q and q-prime decimals are readable and stay within columns. Commit hash wraps without clipping. Bottom paragraph continues coherently onto34. |
| 34 | Appendix H object/path table and reproduction commands | PASS after repair | Individually re-viewed current page-34.png. Both commands now have deliberate short lines, explicit backslashes on every nonfinal line, readable paths and no clipping. |
| 35 | Appendix H verification-scope close | PASS | Exclusions and executed checks are readable. Substantial lower white space precedes separately forced reference page; optional layout choice, not a clipping/readability defect. |
| 36 | References | PASS | Four references and their DOI/repository URLs fit. Wrapped monospaced URLs are legible; no clipped bibliography item, footer conflict or unresolved placeholder visible. |

## Resolved production issue

**P34 — command wrapping (production, not a mathematical failure).** The displayed `verify_all.py` command wraps after `frozen-source`, placing `--output-dir` on a new line with no shell-continuation marker. The `emit_matrices.py` command wraps after `--source-root`, before the existing explicit backslash. The underlying LaTeX uses a normal wrapping typewriter paragraph. A reader copying visual lines into a shell could therefore run incomplete commands. The package README already supplies correct invocation details.

Repair verified: both displayed commands now use deliberately short lines with a literal backslash at each nonfinal shell line. Current page 34 was individually reopened using `view_image`; the commands and all surrounding content fit cleanly. No remaining actionable issue in pages 25–36. No equation, proof or source certificate was changed by this reviewer.

**Optional only:** p35 is short and p36 contains the bibliography because `main.tex` explicitly clears the page before references. Keeping this academic section break is acceptable; no change is required for legibility.

## Documentation consistency check

Read-only inspection confirms `reproduce.py` now lists seven `all` stages, including `legacy`; `scripts/verify_all.py` accepts `legacy`; `verification/README.md` describes that seventh stage and the separate matrix-export command. The documented scope is consistent. No proof execution was repeated.

## Render bindings

- `page-25.png`: `a14a49438aae8655683ddb35be18446e7cb2e7e3be82af29b7097f67ce9f3c23`
- `page-26.png`: `7fbeadd88ca20886a6569443f80aabeb308ce74b5c2fab57f9777837512666c2`
- `page-27.png`: `97aaba054d0b54d2983a4c31dc327428f3bb696b0ede4c8ca8bc7bcbcdf0426c`
- `page-28.png`: `f6dd6ebb99b08dbed5c84a1383559992854f647fd104a8fe165b1d1ad2fef56e`
- `page-29.png`: `b2bd64c7b6f318b8c4ab455a54e950c7a8b1b36712d0e0873d6548896c0d8682`
- `page-30.png`: `b9c837389845b615597fbdc10e51ab807888e7d3df697808df658f1ee6d7fb62`
- `page-31.png`: `7212e88fcbdbc62313ab0c043b0233d3c11dc089c70823bf1dcb1be6e09b7a96`
- `page-32.png`: `aef598d55be4477dfa7f90916cdd3366276758e02bea1d0143005f40660faa08`
- `page-33.png`: `13fcc2db0b4e056a80dd3c87c110f2f8e68f05e5bb39d8c5679053ff5747582d`
- `page-34.png`: `3d49daeb0b6cda40ad0b2610459da88f4281717dc4db12cf18591f9a2837b037`
- `page-35.png`: `814104f32477f944608e7dcefb25093087bd00cf4d8fd213d9349e7d41ed4202`
- `page-36.png`: `0167a3ee5a509132272b2ca6df0b40c680db1496a4018bb663a138e688700862`

## Final clean-build comparison

Independently compared the production and clean-extraction PDFs: all 36 unnormalized page texts, all 36 full RGB pixel arrays at 100 dpi and all 36 page rectangles match exactly. All 18 figure exports are byte-identical. PDF file hashes differ only through CreationDate and document ID; the one differing object stream differs only in its embedded CreationDate. Detailed per-page and per-figure hashes are in [clean-build-comparison.json](clean-build-comparison.json). No proof rerun or manuscript/figure edit was performed.

Final reinspection/comparison recorded UTC: `2026-10-13T19:13:56.634110+00:00`.
