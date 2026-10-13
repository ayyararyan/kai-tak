# Version 4 verification

## Scope

Formatting-only edition of accepted V3. No changed scientific model, new historical acquisition, new optimization or claim of independent peer review. The inherited scientific record is `V3_VERIFICATION.md` and `qa/v3-baseline/`; current format checks are distinct.

## Performed for V4

- Downloaded the actual website Queue Priority PDF and inspected fonts, page geometry and rendered title/body pages; matched the approved author-style sources. Unchanged official class/BST/crop hashes recorded.
- Compared all twelve body/appendix/coefficient TeX files against accepted V3 after a small explicit set of layout transformations. Paragraph blocks, emphasis, mathematical expressions, captions and citation keys retained. The previously separate abstract is included verbatim. Six missing-date labels and the explicit CAD report type are bibliography metadata clarifications, not new sources.
- Verified all 104 frozen input hashes, all original scientific figure-file hashes and the unchanged 51-claim evidence ledger. No new mathematical claim is introduced.
- Native XeLaTeX/BibTeX compilation: 35 pages, 16 numbered figures, seven insights, 14 bibliography entries and 93 resolved links. No overflowing boxes, missing-character warnings or unresolved citations/references. Checked text with PyMuPDF and Poppler and inspected visible text bounds.
- All fonts embedded; Times body/title faces and 12 TeX-pt body verified. Two legacy NewTX symbol fonts lack explicit ToUnicode mappings; see `FORMAT_PROVENANCE.md`. Equations visually checked; mathematical copy/paste is not certified.
- All 35 pages rendered and visually inspected. Corrections include avoiding isolated foreword/summary continuation pages, breaking long identifiers, undated-source citation disambiguation, appendix reference labels and the CAD bibliography type. The final visual receipt binds the PDF hash.

- Fresh ZIP extraction into an empty folder and a newly installed Python environment: `build.py --figures` passed. All 16 scientific figures regenerated with identical file hashes. Scalar/figure checks and the calm regularity/upper-bound calculation were freshly rerun and matched. All 35 rebuilt pages have identical extracted text and rendered pixels; Poppler text also matches. PDF bytes differ because of native compilation metadata. See `qa/clean_rebuild.json`.

## Not rerun in this formatting task

The 89-test original model/counterfactual suite, continuous-time witness certificates, original source-acquisition/photogrammetry pipelines and optimization search are not reclassified as newly run. Their accepted V3 receipts remain intact. A separately documented command permits users to rerun the exact proof witnesses. No historical clearance, physical calibration, robust feedback, near-optimality or aviation-safety result follows from a new font/layout.

## Reproduction and publication

Clean-folder build evidence is recorded in `qa/clean_rebuild.json`. The source ZIP includes only the selected files listed in `PUBLICATION_INVENTORY.json`; exact archive member bytes are checked. GitHub publication and independently fetched remote artifact hashes are separate final gates, recorded in the project ledger. No website deployment or outreach is authorized by this format request or performed.
