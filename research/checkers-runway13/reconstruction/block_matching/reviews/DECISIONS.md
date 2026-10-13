# Review decisions

All findings are evaluated against source evidence; reviewer assertions alone are not treated as proof. Original source downloads and the numerical landing model are unchanged.

## Blind review

| Finding | Decision and verification |
|---|---|
| B1 palette indices vs brightness | Accepted robustness issue. Fresh audit of all 227 actual TIFFs: every input is one-band grayscale with no palette, so no current output was affected by this issue. Both extractors now reject unsupported palette/RGB/nodata inputs rather than silently thresholding indices. |
| B2 visual review not bound to outputs | Fixed. Explicit reviewed_geometry_manifest.json binds 45 inspected features to full raw candidate, geometry, source archive and overlay hashes. Modified geometry, dates, labels or heights cannot inherit approval. |
| B3 render despite failed registration | Fixed by owner. Entire input audit precedes rendering; hash/transform/core failures reject the run. Real tampered-ZIP regression preserves failed audit and renders nothing. |
| B4 mutable stereo indices | Fixed by owner. Ground/roof observations pinned to input-track and source-frame hashes plus exact paired pixels; reassigned points refused. |
| B5 rejected stereo controls/roofs | Fixed by owner. Finite values, cheirality, reprojection, plane/fit rank and ray intersection gates precede use. Per-variant roof results nullable on failed checks. Sparse and dense outputs unchanged by these guard repairs. |
| B6 wrong CRS property in WGS84 output | Fixed. Output properties say EPSG:4326; EPSG:2326 is retained separately as source-grid provenance. |
| B7 artificial clipping closure | Accepted. Candidate owner removes edge-truncated regions from strong closed-outline evidence; full rerun and comparison required. |
| B8 geographic bbox instead of source core | Accepted. Candidate owner uses the actual index polygon; full rerun records changed coverage. |
| B9 centre-based contour erosion | Accepted. Candidate owner polygonizes raster-cell edges and records geometry changes; old derived outputs retained under invalidated/. |
| B10 seed rounding | Fixed using containing-cell floor. All final extracted source geometries unchanged; narrow one-pixel fixture covers the failed boundary. |

## Edge review

| Finding | Decision |
|---|---|
| Bilinear right-disparity interpolation includes invalid sentinels | Accepted actual defect. Reviewer reproduced 69 accepted pixel matches / six sampled exports involving invalid interpolation support. Photo owner is invalidating affected exports and regenerating dense points/surface with all nonzero-weight contributors required valid. Final counts and hashes must come from repaired artifacts. |
| Sparse viewer ignores acceptance flags | Accepted regeneration defect; present 1,318 sparse rows all pass. Viewer owner now filters explicit diagnostic and cheirality flags, preserving omitted counts. |
| Modern courtyard rings omitted | Accepted. Viewer owner must render inner as well as outer boundaries; this affects the separate 2026 comparison, not historical geometry. |

## Delivery verification boundary

The OpenClaw browser returned 'unsupported protocol file:' for a local file and 'browser navigation blocked by policy' for a localhost preview. No alternate access path was used to bypass those controls. HTML/data tests, JavaScript syntax and separately generated static images can be verified; actual browser interaction remains unverified. This is a delivery-verification limitation, not a claim the standalone viewer fails in a user's normal browser.
