# V4 requirements traceability

| Requirement | Implementation | Evidence |
|---|---|---|
| V4-01 Website RFS author format | Implemented | `FORMAT_PROVENANCE.md`, `qa/format_authority.json`, `rfs-workingpaper.sty` |
| V4-02 Full V3 content and title preserved | Implemented | `baseline/`, `check_pdf.py`, `qa/document_checks.json` |
| V4-03 Scientific inputs/figures unchanged | Implemented | `SOURCE_MANIFEST.json`, `FORMAT_BASELINE.json`; exact hash checks |
| V4-04 Compile, inspect every page | Implemented | 35 pages; `qa/document_checks.json`, `qa/visual_inspection.json` |
| V4-05 Portable editable package | Implemented | `README.md`, `package_sources.py`, `DELIVERY_MANIFEST.json`; `qa/clean_rebuild.json`: 35 identical text/pixel pages |
| V4-06 Authorized GitHub update | Implemented; push verified separately | Exact selected inventory; project ledger and publication record distinguish local package from verified remote result |

V3 scientific requirement/evidence records are retained in `V3_REQUIREMENTS_TRACEABILITY.md` and `V3_VERIFICATION.md`; this table does not supersede their scientific scope.
