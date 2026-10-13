# Reproducibility

## Metadata-only checks

```sh
python3 -m venv .venv-archive
.venv-archive/bin/python -m pip install -r archive/requirements-archive.txt
.venv-archive/bin/python scripts/archive_validate.py --report /new/path/metadata-report.json
python3 -m unittest discover -s tests -v
```

JSON Schemas validate required metadata, not the truth of unknown historical facts. The validator separately reports unresolved lineage; a structurally valid record with explicit nulls is not complete provenance.

## Verified public-data example: NOAA weather tables

Restore collection 05 using the [download guide](DOWNLOAD.md), then:

```sh
python3 scripts/archive_reproduce.py --report /new/path/weather-reproduction.json
```

The replay copies the pinned NOAA source, decoder, decoder tests and retained format document from the source checkout into a temporary isolated tree. It does not overwrite evidence. It checks station/year identity, runs 12 decoder tests and compares the two regenerated CSVs to catalogue hashes: 8,549 annual records and 24 records on 4 November 1993. The format PDF is an existing Git dependency; it is not newly relicensed by this archive. Missing observations/quality flags remain explicit; results are not an aircraft-local gust history.

## Installed geospatial checks

```sh
.venv-archive/bin/python scripts/archive_validate.py --data-root /path/to/restored --report /new/path/data-report.json
# Use the separate, recorded geospatial environment:
python3 scripts/archive_geospatial.py --data-root /path/to/restored --report /new/path/geo-report.json
```

The optional geospatial command needs `ijson`, `numpy`, `rasterio` and `shapely`; see the existing [geospatial dependency lock](../research/checkers-runway13/geospatial/requirements.lock). It counts all modern features, missing heights, invalid geometries, bounds, raster dimensions, CRS and valid cells. Known invalid source polygons remain unmodified. HKPD elevations and 2014–2015/2026 vintages do not certify 1993 obstacle clearance.

## Other research lanes

[Model reproduction](../research/checkers-runway13/README.md), [white-paper v2 build](../research/checkers-runway13/whitepaper/v2/README.md) and [historical integration checks](../publication/INTEGRATION_UPDATE.md) retain their original commands and environments. Their dependency locks differ. LaTeX, GDAL/PROJ, rasterio, OpenCV, trimesh, mpmath and source-bound scans are not interchangeable prerequisites. Some historical mpmath declarations differ; use the specific lane's documented version and verify it before replay.

Full source-dependent integration/photogrammetry is **not reproducible from this new permitted-data set alone**. Exact excluded CAD report/crops, Boeing drawings, datum realization, calibrated aircraft data and other dependencies remain missing or restricted. Saved old verification reports are historical receipts, not fresh execution. The archive does not waive those checks or silently substitute modern geometry.

## Local release preparation

```sh
python3 scripts/archive_catalogue.py --source-root /read-only/original/workspace
python3 scripts/archive_build.py --source-root /read-only/original/workspace --output-dir /outside/git/bundles
python3 scripts/archive_prepare_metadata.py
python3 scripts/archive_acceptance.py --bundles /outside/git/bundles \
  --work /new/outside/git/acceptance --report /new/path/acceptance.json
```

After a build, `archive_prepare_metadata.py` refreshes citation/rights proposal exports without granting a license.

Catalogue regeneration resets the unpublished candidate manifest to awaiting-build and must be followed by a build. Do not run it on a published release. It uses frozen audit/definition inputs and exact acquisition checks, not directory-wide rights inference. The builder refuses non-candidate manifests and different existing bundle bytes unless explicit candidate rebuild is requested. Determinism is verified by comparing independent builds; gzip versions across systems may differ, so published hashes remain authoritative.
