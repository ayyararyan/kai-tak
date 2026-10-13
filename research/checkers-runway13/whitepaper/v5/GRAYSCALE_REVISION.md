# V5 grayscale figure refresh — 14 October 2026

Authorized request: make the same V5 figures grayscale, recompile the PDF and update GitHub main. This is a presentation-only revision, not a new paper version.

## What changed

The shared figure palette uses neutral tones. Displayed historical photographs, maps and reconstructed surfaces are converted to grayscale without changing their original input files, crops, coordinates or source meaning. All 15 figures were regenerated as vector PDF/SVG, screen PNG and 600 dpi presentation PNG. Existing direct labels, line styles and markers remain in place.

The paper retains its title, V5 date, 38 pages, text, mathematics, citations, source qualifications, font metrics and layout. The author-review banner is unchanged: the request applies to the figures, not other document elements. Earlier editions and all original evidence remain unchanged.

## Verification

- 60/60 figure exports verified grayscale, including embedded SVG rasters and rendered vector PDFs (`qa/grayscale_exports.json`). The pixel check disables renderer ICC transformations so neutral source paints are tested without profile-conversion tinting.
- 38/38 page texts, text positions and fonts match the original color PDF; independent Poppler text extraction is identical (`qa/grayscale_preservation.json`).
- Only the 15 figure-bearing pages differ visually. The other 23 pages are pixel-identical.
- All 15 figure provenance records preserve their data and semantic fields.
- 287 science checks and 74 independent figure-semantic checks pass. The builder verifies the 104 frozen and 11 supplemental source inputs. No optimization or model changes were made.
- An independent reviewer inspected all 15 changed pages with no must-fix readability or clipping findings (`qa/grayscale_visual_review.json`). This is a rendered-screen check, not a physical print proof.

Run the documented build, then `python scripts/verify_v5_grayscale.py`. The source ZIP is a portable acceptance snapshot; its clean extraction/rebuild verification is recorded in `qa/grayscale_clean_build.json`. PDF compilation timestamps can change binary hashes even when all page text and pixels match.

## Receipt history and publication

The original color artifacts remain in Git history at `bdcbcdb71065797d65c38a37348cb80ea6e1a4d3`. Original local-delivery and publication receipts are retained as historical evidence, including `DELIVERY_MANIFEST.json`, `qa/delivery_acceptance.json`, `qa/clean-location.json`, `qa/visual_acceptance.json` and repository-level `publication/v5_verification.json`. Their original color-artifact hashes are not current grayscale identities.

Current grayscale identities are in `qa/document_checks.json`, `qa/grayscale_exports.json`, the external-to-ZIP `qa/package_manifest.json`, and repository-level `publication/v5_grayscale_verification.json`. The last is updated after Git/HTTP readback; it is deliberately outside the source ZIP to avoid a self-referential archive hash. The repository correction manifest retains the original hashes and pins each exact authorized successor. No historical baseline is rewritten.
