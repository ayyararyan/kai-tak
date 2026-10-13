# Independent implementation review and repairs

Three isolated native review lanes inspected the implementation: blind adversarial review, edge-case review, and acceptance audit. Their findings are criticism, not certification. Parent verified each adopted repair.

| Finding | Decision and repair | Evidence |
|---|---|---|
| Wide mosaic wrongly labelled 1989–1993 | Accepted. Actual oldest sheet July 1986; updated captions/jobs/metadata to 1986–1993. | Manifest min/max and acceptance check |
| Evidence mode downloaded contextual masters | Accepted. Separate evidence PNG masters, previews, captions, limits, types and epochs for 04/06/12. | PNG metadata/path checks |
| Assembly accepted changed sources/renders | Accepted. Verify all declared original inputs, prepared assets, render SHA256 and current job hashes before composition. | Positive checks; renderer negative checksum test |
| Unconditional restoration/GLB verification prose | Accepted. Separate actual restoration receipt; preparation labels GLB mapping as documented. Independent acceptance decoder now compares all GLB positions and indices. | restore_receipt.json; acceptance.json |
| DTM missing cells could become geometry | Accepted. Masked read and fail-closed missing/nonfinite rejection; triangle-validity check. No missing samples in current crop. | Preparation succeeds on current declared data |
| Invalid modern geometry could crash silently | Accepted. Explicit null/nonpolygon/nonnumeric-height omissions or rejection; no imputation. | 3546 components /167 omissions current data |
| Print/web derivative metadata missing | Accepted. Print PNG text metadata; per-web-image sidecars including variants. | Acceptance checks and final inventory |
| Triptych markers too small | Accepted. Draw surface/map marks after fitting, consistent visible marker size. | Final pixel inspection |
| Crops retained inset claims after removing inset | Accepted. Crop12 uses original surface panorama, no map inset, with single-source1993 metadata. | Pixel inspection and metadata checks |
| Daylight alternative undiscoverable | Accepted. Linked matched architectural/daylight output in gallery and README. | Link check |
| Locator had unequal east/north pixel scales | Accepted. Single 880/3700 pixels per metre in both directions. | Code and diagram inspection |
| Generated jobs machine-local | Qualified. Jobs intentionally record absolute georeferenced input/output locations; reproduction regenerates them in the new checkout. Portable fonts/PATH overrides added. | README, make_jobs.py, render_all.py |
| Photo inclusion lacked explicit rights gate | Accepted. Route-specific affirmative rights register checked before assembly; source audit verifies DAP-L0 terms. No publication performed. | rights.json and SOURCE_AUDIT.md |
| Invisible uncertainty in detached plates | Accepted. Limits now printed on every annotated plate and print export, alongside epoch. | Final visual inspection |
| Unknown job IDs succeeded silently | Accepted. Reject unknown requested render IDs before processing. | CLI negative-input check |

No frozen historical geometry, missing heights, temporal meaning, trajectory objective or source calibration was changed to satisfy review. Gallery interaction remains unverified due the actual browser policy blocker, not reviewer omission.
