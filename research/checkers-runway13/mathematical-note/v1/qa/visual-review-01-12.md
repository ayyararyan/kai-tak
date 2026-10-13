# Visual review — rendered pages 01–12

Reviewed 14 October 2026 by the independent analytical/figure review agent.
Scope: actual rendered page images `qa/pages/page-01.png` through
`qa/pages/page-12.png`, each individually opened with `view_image` and visually
inspected. This is a rendering review, not a substitute for the separate proof
and certificate audits.

PDF: `certified-local-optimality-v1.pdf` (36 pages, as supplied for review).
SHA-256: `8d1acbe45f2641f29781aecd304900c9f88ac8c25851b44f7545c05c1211d8ed`.

**Result: 12/12 assigned pages inspected; no blocking visual defect found.**
One nonblocking pagination observation appears below. No manuscript source was
edited during this pass.

## Page-by-page record

| Page | Content actually seen | Visual finding |
|---|---|---|
| 01 | Title, author, abstract, version/date and independent-note designation | Title wraps cleanly over two lines. Abstract and quantitative result are readable; no clipping, missing symbols or overlap. Lower whitespace is appropriate to a title page. |
| 02 | Introduction and displayed family bracket (1) | Running header, prose, citations and long decimal bracket fit the text measure. Both bounds and inequality signs are clear. |
| 03 | Frame, wind, CG/virtual transformation, basis and inverse dynamics, equations (2)–(8) | All formulae and equation numbers are distinct and readable; density reference is visibly defined. No edge collisions. |
| 04 | Polynomial family, Table 1, Hermite construction (9), endpoints (10) | Parameter table and endpoint arrays fit. The three-component direction definition is clear. Corridor paragraph continues normally to page 5. |
| 05 | Corridor continuation, Table 2, objective (11) | Exact-binary64 cloud description is legible. Margin table is readable and not cramped. Closed forward predicate is visibly nonnegative, not strictly positive. |
| 06 | Secondary objective (12), occupied geometry, support (13), obstacle constraint (14), contact subsection opening | Integral and geometric expressions remain inside margins with separated equation numbers. Contact heading has following text, not a stranded heading. |
| 07 | Ground law (15), stopping formula (16), V5/A1 model distinction | Formulae and prose are readable. Nonblocking cosmetic observation: approximately the lower two-fifths of the page are blank before the deferred Figure 1 on page 8. No content loss or stranded heading. |
| 08 | Figure 1 landing schematic and caption; analytical section, Lemma 1, (17)–(18) | Integrated figure labels are small but legible at the page width. CG/virtual paths and ideal reset are distinct; flare is labelled “straight track.” Caption and mathematical text do not collide. |
| 09 | Terminal Proposition 1 and proof, derivative, quartic, family-floor bound (20) | Formulae, signs and proof ending are clearly rendered. No clipping or crowding. |
| 10 | Regularity (21), Lemma 2, attainment Proposition 2 and proof | Long bounds fit. The hard forward predicate remains nonnegative. Proof-ending square on its own final line is visible and within the measure. |
| 11 | Coupled energy bounds (22)–(26) | Constants, forward-speed inequality, ratio bound, gate thrust and ramp are legible; long formulae have no overlap with equation numbers. |
| 12 | Work inequality Proposition 3, (27)–(29), global exclusion Proposition 4 | Displayed bounds and proof text are readable. Continuation to page 13 is natural, without a stranded heading or clipped last line. |

The graphical family-bracket figure and certificate-flow figure do not occur
within pages 1–12; this page-range report does not claim their inspection in
the assembled PDF. Their final corrected standalone exports were separately
visually reviewed during figure production: the root uses `F(ζ*) = 0`, and
retention is a rightward lower-bound ray rather than an asserted two-sided
interval. The family bracket in equation (1), which does occur on page 2,
was inspected here.

## Inspected image hashes

```text
page-01.png 28a5b6443219443992417628e010319586a7e6ebc7cff4af892fbce010d0a9d1
page-02.png 70ed6ce8d4271d1ee8d5e6a826055e22fb4ff48791b204b044fea2916045812c
page-03.png e77de056126f2b106f30f89b7f6372f3da72b56a02f37d8e621f8b138e71f49c
page-04.png e5159c8e955845d092ac80078a7b18cd2930252131c47feca8a7b9c63d49c716
page-05.png a02b70dba01e548a474c2493b4b19a7164d49da9403760637399b8e6e8449823
page-06.png 0f8828b795f44aa29a57f9e9654299d946f7805f88500fc3aa6ec4fa29384e41
page-07.png 7c825008ae3d30bf502099444bb46c3d3cd792beefba3374faeb4c72755a5b53
page-08.png 396a7f17464be23633e1cd8cec42e0cee0c84f265b7106240b3b43ec11e99583
page-09.png 1be96104ee1de9fd5e52370f207eda08bb953136271fb0a59f23461364bd3858
page-10.png 0498bee4565130b6e46d9fc632d8591d8ae68ed4e96a9729124bd1aa2ce9afad
page-11.png 52174bd5c3926fa6559b93473f071ecfea765278c35fcdab705274a00812ff22
page-12.png bf6692b1e00712aefe4618847fbc65044816f26dde0e64d412dd9728bfe4f00e
```

## Hash bridge to final PDF

At 2026-10-13T19:14:45Z, the current PDF had SHA-256
`24965a9e628ce7f845870b0774e77d07911021e5a366dd8bf8fc033982dfda28`. All twelve current
page PNGs were byte-identical to the hashes recorded above. A fresh in-memory
render of each corresponding page directly from that PDF, using PyMuPDF
1.28.2 with `Matrix(1.4, 1.4)`, also produced those same hashes.
Thus the visual findings above apply unchanged to pages 1–12 of this PDF.
Full comparison evidence is recorded in `upstream-freshness.json`.
