# Independent review and repair disposition

Three independent review passes covered adversarial code, edge cases and all 15 request sections. Findings below were accepted unless qualified. No scientific model meaning or source bytes changed; no additional approval was needed for implementation repairs.

| Finding | Disposition | Evidence |
|---|---|---|
| Catalogue/refine could mutate published release | Fixed: guard before first write | Catalogue regression tests |
| Build trusted publication string without registry binding | Fixed: exact artifact/dataset/source-right decision binding in build and new fetch | Policy tampering tests |
| Later build failure could replace earlier candidate files | Fixed: stage full generation; rollback catchable commit failures | Multi-collection late-failure and metadata rollback tests |
| `..` output containment bypass | Fixed: resolve containment before creating output | Builder boundary test |
| Re-read archive could change after initial verification | Fixed: staging pass validates member type/duplicates/full set and compressed hash | Mutation-during-restore tests |
| Wrong collection/dataset/master manifest pointers passed validator | Fixed: identity/path/count/member binding checks | Negative metadata fixtures |
| Conflicting checksum/deposition records passed | Fixed: checksums.json, SHA256SUMS, master and draft file-set binding; transactional build updates | Metadata and builder regression tests |
| Duplicate virtual IDs and full-graph cycles passed | Fixed: global identity and graph checks | Negative graph fixtures |
| Corrected source-attribution edges missing | Fixed: regenerate edges from corrected source IDs | Bidirectional attribution validation |
| Refinement duplicated relationships/changed already-correct dates | Fixed: idempotent corrections and asset preservation | Repeat-refinement regression |
| Geospatial zero-missing count could skip expected check | Fixed: iterate required counters, not observed keys | Zero-count regression |
| Missing replay output crashed instead of reporting failure | Fixed: report missing output before opening | Missing-output regression |
| Seven invalidated JSON outputs had regular verification label | Fixed from checksum-matched content; frozen copies inspected | Scientific-status regression |
| Branch-safe unresolved attempt conflated with invalidation | Fixed: explicit unresolved-budget status | Scientific-status regression |
| Geospatial verification timestamp mislabelled acquisition | Fixed: unknown acquisition/generation remain null; verified/upper-bound fields separate | Date regression |
| Four-bundle/400-file reports described superseded candidate | Final five-bundle/418-file checks rerun; initial reports retained | clean_restore.json, installed_validation.json, deterministic_rebuild.json |
| schema.org attributed all source data to researcher | Fixed: source creator distinct from archive curator | schemaorg-datasets.jsonld |
| Global completeness overclaim risk | Accepted: full request remains partial/blocked as documented | TRACEABILITY.md and PUBLICATION_READINESS.md |

Transaction caveat: catchable-error rollback does not promise an indivisible transaction across filesystems under power loss/SIGKILL. Per-file hash verification prevents partial bytes being accepted; verify and rebuild the unpublished candidate after an interrupted generation. Published releases are never rebuild targets.
