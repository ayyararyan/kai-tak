# V5 production state

Baseline 2b65c24, branch editorial/v5; separate worktree <V5_WORKTREE>. Authorized scope SPEC.md and editorial/AUTHORIZED_REQUEST.md. Parent owns state/integration; editorial_diagnosis owns editorial notes; visual_diagnosis owns visual notes; scientific_audit owns science revalidation. No V4/model/source edits allowed.

## Current
Stage1 full source read completed by parent; all35 pages rendered and inspected as page contact sheets. Separate audits in progress. Typography verified as Times-Roman/Italic/Bold with NewTX math; page 517.38×779.30pt. RFS style/class copied unchanged apart from eventual V5 metadata. Baseline all238 tracked V4 files hashed in editorial/V4_BASELINE.json.

## Binding narrative
Seven acts: place/puzzle → turning physics → complete landing/stopping → historical reconstruction → wind/continuous verification → CAL605 → synthesis/open questions. No preliminary executive-summary table that reveals the complete calculation before the puzzle. Source limitations consolidated at meaningful first uses and appendices.

## Environment
Python: <WORKSPACE>/scratch/kaitak-v3-clean-env/bin/python. XeLaTeX/BibTeX: <WORKSPACE>/research/jamshidian-website-2026-09-09/toolchain/TinyTeX/bin/universal-darwin/. Portable commands will use PATH or explicit XELATEX/BIBTEX environment overrides, not these absolute local paths.

## Next
Finish stage1/2 audits, substantive prose, then inspect four major figure prototypes before full suite. Final source packaging and clean rebuild after independent editorial review. No current blocker; author foreword review is deliverable status, not a prerequisite to production.

## Stage 1–3 update
Full editorial audit now persisted:228 entries classified120 A/36 B/14 C/58 D. All51 claims mapped into the seven acts/technical appendices. Four opening alternatives compared; A selected with course-versus-heading precision correction. Full main-text rewrite in progress. Technical appendices A–F preserved, G source conventions and H comprehensive scope/rights added; independent science review corrected a moving-frame bank-rate explanation. Fresh256 numerical/integrity checks and89 original regression tests pass, both exact interval covers reproduced. Supplemental historical inputs:10 hash-verified files, no regenerated reconstruction.


## Stage 3–4 update
Full seven-act prose,202-word abstract and review-marked foreword complete. Four prototype families inspected by parent:01geography,02bearings,04completepath/05runway,07stereo. Fixed stereo camera orientation, roof examples outside-control-hull qualification, diagram overlaps; accepted gate then released remaining suite. Current independent science288checks/89originaltests;53claim rows (51baseline+2newly displayed source facts). Eleven supplemental input hashes bound. Remaining: full suite integration, complete PDF inspection, independent final reader review, portable clean rebuild and reports.

## Final local delivery — 13 October 2026

All six authorized production stages complete. Final PDF:38 pages,15 redesigned figures,14 references,202-word abstract,review-marked foreword. Seven-act prose substantially rewritten; all19 requirements implemented. Independent final read accepted after five targeted repairs. Every page visually inspected; last layout-only fixes preserve reviewed prose/math. Final PDF SHA256328f848d805df1e5bac5fd6aff6f28363112bea3acd9a5fcb71c33ec16842939.

Verification:287standard/288fresh-bound science checks;74 independentfigure checks;89 regressiontests; bothoriginalfixed-witnesscertificates freshly reproduced.104frozen+11supplementalinputs preserved; all238V4files unchanged;26mathblocks andexactcoefficients retained. FreshPythonenvironment/sourceextraction rebuild reproduces38/38page texts/pixels and60/60figureexports. Finalpackage/manifest verification recorded in qa/delivery_acceptance.json and DELIVERY_MANIFEST.json.

Currentcanonicalhandoff:VERIFICATION.md,REPRODUCIBILITY.md,EDITORIAL_ASSESSMENT.md,REQUIREMENTS_TRACEABILITY.md. No substantive production blocker; foreword approval and human specialist review remain explicitly outstanding boundaries, not hidden completed steps. No commit,push,publication,outreach orpeer-sync performed. V5 edition completion doesnot close the separate integrated historical-flight solution's gaps.

## 14 October 2026 — authorized grayscale refresh

Aryan requested only that V5's same figures be made grayscale, the PDF recompiled,
and GitHub main updated. This supersedes the older local-only publication boundary
for this specific refresh. Baseline public main is
`bdcbcdb71065797d65c38a37348cb80ea6e1a4d3`; the original color PDF and source package
remain retrievable at that commit. Scope: neutral figure palette and displayed
raster copies, unchanged 15 figure designs/data/coordinates/crops, rebuilt 60
exports and 38-page PDF, matching portable source package and dated verification.
Preserve manuscript wording, all mathematics/calculations, source originals,
previous editions, original publication receipts, author-maintained root README,
archive/atlas and all unrelated work. No optimizer run or model change.

Current artifact state: all 15 figures / 60 exports regenerated in grayscale;
38-page PDF compiled with unchanged text, font positions and mathematics. Only the
15 figure pages changed; the other 23 pages are pixel-identical. All 287 science
and 74 figure-semantic checks pass; independent visual review has no must-fix
findings. Clean source-package verification is recorded in
`qa/grayscale_clean_build.json`; current PDF/export/package identities are in the
QA manifests listed in `GRAYSCALE_REVISION.md`.

Publication is authorized for `ayyararyan/kai-tak` main. Its live outcome is recorded
in repository-level `publication/v5_grayscale_verification.json`, updated after
remote Git and anonymous HTTP readback. That receipt is intentionally outside the
portable source ZIP; this ledger is the frozen artifact-acceptance snapshot, not a
claim that a future push has already succeeded. Historical color receipts remain
unchanged. Parent owns integration and publication; independent review covered
rendered pages and the narrowly scoped preservation-correction support.
