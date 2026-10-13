# Download and verify

Python 3.12+ on POSIX is supported by the archive tools. Downloads, building and NOAA replay use the standard library. Descriptor-relative no-follow filesystem operations protect restoration; native Windows is not supported. Use a real directory path, not a symlink (on macOS use `/private/tmp`, not `/tmp`).

## Discovery and selection

```sh
git clone https://github.com/ayyararyan/kai-tak.git
cd kai-tak
python3 scripts/fetch_data.py --list
```

**[Data Release v1.0.0](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0)** supplies the verified permitted-data bundles. New open licenses are not implied; consult source-specific rights.

```sh
# One collection; no other data required for the weather replay
python3 scripts/fetch_data.py --release v1.0.0 --collection 05 \
  --report /new/path/weather-integrity.json

# All permitted-data collections, preserving the original research paths
python3 scripts/fetch_data.py --release v1.0.0 \
  --report /new/path/integrity.json

# Check archive/member hashes without extracting or creating the destination
python3 scripts/fetch_data.py --release v1.0.0 --collection 01 --verify-only \
  --archive-dir /absolute/path/to/cache

# Restore into a separate empty directory
python3 scripts/fetch_data.py --release v1.0.0 --collection 03 \
  --destination /new/path/restored
```

Repeat `--collection` for several IDs. IDs with no permitted byte bundle return `catalogue-only` and a reason. All five bundles are independent **complete snapshots of their selected member sets**, not incremental patches. They do not contain every item described by their collection catalogue. The master manifest enumerates exceptions per artifact. A successful restore means the selected bytes are correct, not that missing historical research inputs have been acquired.

## Existing public research snapshots

```sh
python3 scripts/fetch_data.py
python3 scripts/fetch_data.py --verify-only
```

Legacy defaults select five data groups across three existing releases: initial chronology/geospatial, updated reconstruction/supporting, and integration. The integration archive alone is not complete. Legacy data remain under their original rights; their earlier publication does not establish permission for a new license. Original publication manifests and old release contents are untouched.

## Integrity and failure behavior

Downloads are hashed before cache promotion. Every member is checked for expected path, type, size and hash before restore. Absolute/traversal/Windows-reserved/control-character paths, duplicate and case/Unicode-colliding paths, links, device files and unexpected members are refused. Destination/cache symlink ancestors and conflicting files are refused. Verified staging and no-clobber promotion prevent unverified target files. An interrupted restore can leave already verified files; rerun safely. A successful receipt appears only after all selected bundles finish.

A report destination must be new; reports are not silently overwritten. File-set integrity is distinct from historical accuracy, scientific verification and rights status. URL availability is verified separately from byte integrity. The frozen manifest records public release URLs; `--offline --archive-dir /path/to/verified/cache` restores without network access.
