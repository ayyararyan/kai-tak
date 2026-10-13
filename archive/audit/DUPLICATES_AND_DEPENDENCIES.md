# Duplicates and dependencies

The initial audit is nonmutating. [Duplicate hash groups](duplicates.json) report identical research bytes at multiple paths; no file was removed or consolidated. Frozen paper evidence and invalidated experiments often intentionally duplicate data. Location copies and same-path differing versions are represented in [artifacts](../catalogue/artifacts.json), not conflated.

[Dependency scan](dependencies.json) records 1,158 Python import occurrences, one machine-path reference and 193 unresolved Markdown targets in the baseline source checkout. This static scan is not a declaration that 193 sources are unavailable: some targets are directories, release-only bytes, restricted evidence, generated outputs or historical relative paths. Import presence does not prove a compatible environment.

The weather decoder replay requires the exact NOAA gzip, retained decoder/tests, expected CSV hashes and an existing format PDF. The new collection 05 supplies the gzip; the baseline source commit supplies its code/reference dependencies. Building and raster quality checks require the lane-specific geospatial environment. Scientific lanes use differing locks (including mpmath versions); do not merge them into an invented universal environment. The full photogrammetry/integration pipeline additionally depends on restricted CAD/Boeing inputs and unvalidated calibration/geometry.

[Source route availability](../reports/source_link_availability.json) is a fresh bounded GET probe, not a permission or whole-file check: 13 of 24 routes answered successfully; 11 failed or remained unverified, including CSDI API HTTP 403 responses. Previously acquired, checksum-pinned source bytes remain available locally. An unavailable service today does not invalidate a previously verified acquisition, but it blocks a claim that all sources can be refetched today.

Large downloaded historical release assets and runtime environments remain outside this branch. New public data bundles contain only exact allowlisted files. [Release exceptions](../releases/v1.0.0/manifest.json) record all catalogue items not bundled; no unapproved fallback download bypasses these exclusions.
