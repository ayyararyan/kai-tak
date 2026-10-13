# Independent architecture review and dispositions

Three separate no-context reviews examined acceptance coverage, edge cases and
blind implementation defects. The initial reviews found concrete implementation
problems; none justified altering scientific meaning or frozen artifacts.
All recommendations below were accepted as engineering repairs within the existing
authorized scope. No model change or additional approval was needed.

| Finding | Repair and acceptance evidence |
|---|---|
| Per-file role map conflated generated evidence, publication boundaries and invalidated work | All 2,969 rows reclassified across independent role/disposition/preservation fields; exact producers distinguished from documentary pointers. Acceptance reviewer independently verified complete coverage and semantic examples. |
| Paper could be relabelled as a future version without new artifacts | Versioned PDF/guide/package identities and document QA must agree; full-row relabel regression rejects. |
| Paper page count lacked evidence | Require version-specific protected QA page count and PDF digest; false count rejects. |
| Whole historical-document waiver could exempt a new page | Both individual and whole-document exceptions require immutable baseline and actual live source identity. |
| Existing ignored files could make public links pass locally | Targets must belong to the public Git/addition inventory or its directories; local-only fixture rejects. |
| Editable baseline could conceal a retargeted historical tag | Five original tag targets independently pinned in code; altered-baseline regression rejects. |
| Browser receipt could be reused for a different atlas | Receipt binds edition, gallery path and exact SHA256; three mismatch regressions reject. |
| Empty or malformed atlas manifests could pass zero checks | Validate 25/27 coverage, unique safe paths, digest/size/member fields; malformed/truncated cases reject. |
| Future atlas navigation left the gallery route stale | Current gallery route and local serving instruction generated from status metadata. |
| HTML line-reference shortcut accepted nonexistent anchors | HTML requires actual anchors; source line-number links remain bounded. |
| New paper was automatically called a formatting edition | Generated navigation uses neutral edition terminology. |
| Two generated blocks in one file could overwrite one another | Render cumulatively by path, write once; simultaneous-staleness regression plus independent real-atlas reproducer pass. |
| Concurrent scientific publication's strict ledger hash no longer matched appended main ledger | Preserve original verifier; compare 234 current mapped scientific files and ledger prefix, then run its recorded artifact snapshot. Mutation tests cover scientific bytes, mapping and ledger changes. |

The acceptance reviewer returned a scoped pass for the revised inventory and v5 /
conditional-local-optimality navigation. The edge reviewer independently reran the
repair regressions, found the multi-block bug, then verified its repair with three
targeted tests and the original reproducer. No demonstrated review finding remains
unresolved. This is code/architecture review, not human aerospace peer review or a
claim that hosted CI ran.

See [validation](VALIDATION.md) for actual scientific, restoration, build and browser
checks, and [handoff](HANDOFF.md) for the separate publication decision.
