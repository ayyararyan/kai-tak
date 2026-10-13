#!/usr/bin/env python3
"""Build deterministic, rights-filtered LOCAL candidate bundles; never publish.

Example: python scripts/archive_build.py --source-root /path/to/restored-baseline
         --output-dir /path/outside/repository/bundles
Manifest rows are explicit inclusion decisions, not a directory glob.
"""
import argparse
from contextlib import ExitStack
import gzip
import json
import os
from pathlib import Path
import tarfile
import tempfile
import uuid
from archive_io import (ArchiveError, atomic_json, check_stream, digest, directory,
                        records_by_path, regular_file, relative_parent, safe_path,
                        verify_bundle, read_json, load_policy, validate_collection_policy)

ROOT = Path(__file__).resolve().parents[1]


def commit_generation(replacements):
    """Install a fully staged generation, restoring every prior target on errors.

    Each source is on its destination filesystem. Existing bytes are retained as
    hard-link backups until all bundle and metadata replacements have succeeded.
    This handles catchable failures, not power loss/SIGKILL across filesystems.
    """
    prepared, installed = [], []
    rollback_failed = False
    with ExitStack() as stack:
        try:
            # Capture every previous target before the first replacement.
            for source, target, allow_replace in replacements:
                src_fd = stack.enter_context(directory(source.parent))
                dst_fd = stack.enter_context(directory(target.parent, create=True))
                with regular_file(src_fd, source.name):
                    pass
                backup = None
                identity = None
                try:
                    with regular_file(dst_fd, target.name) as old:
                        if not allow_replace:
                            raise FileExistsError('Candidate target appeared during staging: ' + str(target))
                        info = os.fstat(old.fileno())
                        identity = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
                    backup = '.archive-rollback-' + uuid.uuid4().hex
                    os.link(target.name, backup, src_dir_fd=dst_fd, dst_dir_fd=dst_fd,
                            follow_symlinks=False)
                except FileNotFoundError:
                    pass
                prepared.append((src_fd, source.name, dst_fd, target.name, backup, identity))
            for item in prepared:
                src_fd, src_name, dst_fd, dst_name, backup, identity = item
                if backup:
                    info = os.stat(dst_name, dir_fd=dst_fd, follow_symlinks=False)
                    if (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) != identity:
                        raise ArchiveError('Candidate target changed during commit: ' + dst_name)
                    os.replace(src_name, dst_name, src_dir_fd=src_fd, dst_dir_fd=dst_fd)
                else:
                    os.link(src_name, dst_name, src_dir_fd=src_fd, dst_dir_fd=dst_fd,
                            follow_symlinks=False)
                installed.append(item)
        except BaseException:
            failures = []
            for _, _, dst_fd, dst_name, backup, _ in reversed(installed):
                try:
                    if backup:
                        os.replace(backup, dst_name, src_dir_fd=dst_fd, dst_dir_fd=dst_fd)
                    else:
                        os.unlink(dst_name, dir_fd=dst_fd)
                except OSError as exc:
                    failures.append(str(exc))
            if failures:
                rollback_failed = True
                raise ArchiveError('Candidate rollback failed; retain .archive-rollback-* backups: '
                                   + '; '.join(failures))
            raise
        finally:
            if not rollback_failed:
                for _, _, dst_fd, _, backup, _ in prepared:
                    if backup:
                        try:
                            os.unlink(backup, dir_fd=dst_fd)
                        except FileNotFoundError:
                            pass


def build_bundle(source_root, output_dir, name, records, rebuild=False):
    expected = records_by_path(records)
    if len(safe_path(name)) != 1:
        raise ArchiveError('Bundle name must be a basename')
    for record in records:
        if record.get('publication_decision') not in ('Redistribution permitted', 'redistribution-permitted'):
            raise ArchiveError('Unapproved redistribution: ' + record['path'])
        if not all(record.get(k) for k in ('artifact_id', 'dataset_id', 'rights_id')):
            raise ArchiveError('Missing provenance/rights identity: ' + record['path'])
    with directory(source_root) as source, directory(output_dir, create=True) as output:
        # Check all inputs before creating the candidate.
        for rel, record in expected.items():
            with relative_parent(source, rel) as (parent, leaf), regular_file(parent, leaf) as stream:
                check_stream(stream, record)
        temp = '.archive-build-' + uuid.uuid4().hex
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=output)
        try:
            with os.fdopen(fd, 'wb') as raw:
                with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=9) as gz:
                    with tarfile.open(fileobj=gz, mode='w|', format=tarfile.PAX_FORMAT) as bundle:
                        for rel in sorted(expected):
                            with relative_parent(source, rel) as (parent, leaf), regular_file(parent, leaf) as stream:
                                check_stream(stream, expected[rel])
                                info = tarfile.TarInfo(rel)
                                info.size = expected[rel]['bytes']
                                info.mtime = info.uid = info.gid = 0
                                info.uname = info.gname = ''
                                info.mode = 0o644
                                bundle.addfile(info, stream)
                raw.flush()
                os.fsync(raw.fileno())
            size = os.stat(temp, dir_fd=output, follow_symlinks=False).st_size
            asset = {'name': name, 'bytes': size, 'sha256': digest(Path(output_dir) / temp),
                     'files': len(records), 'unpacked_bytes': sum(r['bytes'] for r in records), 'url': None}
            with regular_file(output, temp) as stream:
                verify_bundle(stream, asset, records)
            try:
                os.link(temp, name, src_dir_fd=output, dst_dir_fd=output, follow_symlinks=False)
            except FileExistsError:
                with regular_file(output, name) as existing:
                    try:
                        check_stream(existing, asset)
                    except ArchiveError:
                        if not rebuild:
                            raise ArchiveError('Refusing differing existing bundle; candidate rebuild must be explicit: ' + name)
                        os.replace(temp, name, src_dir_fd=output, dst_dir_fd=output)
            return asset
        finally:
            try:
                os.unlink(temp, dir_fd=output)
            except FileNotFoundError:
                pass


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', default='v1.0.0')
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--rebuild-candidate', action='store_true', help='replace differing LOCAL candidate bytes; never a published release')
    args = parser.parse_args(argv)
    safe_path(args.release)
    if '/' in args.release:
        parser.error('release must be a single version identifier')
    output = args.output_dir.resolve()
    if output == ROOT.resolve() or ROOT.resolve() in output.parents:
        parser.error('bundles must be outside the Git source tree')
    release_dir = ROOT / 'archive/releases' / args.release
    manifest_path = release_dir / 'manifest.json'
    master = read_json(manifest_path)
    if master.get('status') != 'candidate':
        raise ArchiveError('Only an unpublished candidate can be built or updated')
    if args.release != 'v' + master['archive_version'] or master['schema_version'] != '1.0.0':
        raise ArchiveError('Release identifier/version/schema mismatch')
    original_master = json.loads(json.dumps(master))
    draft_path = ROOT / 'archive/preservation/zenodo-version-draft.json'
    try:
        original_draft = read_json(draft_path)
    except FileNotFoundError:
        original_draft = None
    if original_draft is not None and (original_draft.get('status') != 'DRAFT-NOT-SUBMITTED'
            or original_draft.get('metadata', {}).get('version') != master['archive_version']):
        raise ArchiveError('Preservation draft is not an unpublished draft for this version')
    policy = load_policy(ROOT)
    assets = []
    all_records = []
    collections = []
    for path in sorted((release_dir / 'collections').glob('*.json')):
        collection = read_json(path)
        if collection['archive_version'] != master['archive_version'] or collection['schema_version'] != master['schema_version']:
            raise ArchiveError('Collection/master version mismatch')
        collection_id = collection['collection_id']
        if not isinstance(collection_id, str) or collection_id not in [f'{i:02d}' for i in range(1, 10)] or path.stem != collection_id:
            raise ArchiveError('Invalid collection identifier')
        validate_collection_policy(collection, policy)
        all_records.extend(collection['files'])
        collections.append((path, collection))
    if len(collections) != 9:
        raise ArchiveError('All nine stable collection manifests are required')
    records_by_path(all_records)
    with directory(output, create=True):
        pass
    with tempfile.TemporaryDirectory(prefix='.archive-generation-', dir=output) as stage_name, \
            tempfile.TemporaryDirectory(prefix='.archive-metadata-', dir=release_dir) as metadata_name:
        stage, metadata = Path(stage_name), Path(metadata_name)
        replacements = []
        # A missing source or refused replacement cannot modify the prior generation.
        for path, collection in collections:
            if not collection['files']:
                continue
            collection_id = collection['collection_id']
            name = f'kai-tak-archive-{args.release}-collection-{collection_id}.tar.gz'
            asset = build_bundle(args.source_root, stage, name, collection['files'])
            asset.update(collection_id=collection_id, manifest='collections/' + path.name)
            assets.append(asset)
            try:
                with directory(output) as fd, regular_file(fd, name) as existing:
                    try:
                        check_stream(existing, asset)
                        continue  # Identical existing bytes need no replacement.
                    except ArchiveError:
                        if not args.rebuild_candidate:
                            raise ArchiveError('Refusing differing existing bundle; candidate rebuild must be explicit: ' + name)
            except FileNotFoundError:
                pass
            replacements.append((stage / name, output / name, args.rebuild_candidate))
        master['assets'] = assets
        atomic_json(metadata / 'manifest.json', master)
        atomic_json(metadata / 'checksums.json', {a['name']: a['sha256'] for a in assets})
        with (metadata / 'SHA256SUMS').open('x', encoding='utf-8') as checksums:
            checksums.write(''.join(f"{a['sha256']}  {a['name']}\n" for a in assets))
            checksums.flush()
            os.fsync(checksums.fileno())
        if original_draft is not None:
            draft = json.loads(json.dumps(original_draft))
            draft['proposed_files'] = [dict(name=a['name'], sha256=a['sha256'], bytes=a['bytes'],
                treatment='eligible-source-data; attach full source-specific conditions') for a in assets]
            atomic_json(metadata / 'zenodo-version-draft.json', draft)
            if read_json(draft_path) != original_draft:
                raise ArchiveError('Preservation draft changed while building')
            replacements.append((metadata / 'zenodo-version-draft.json', draft_path, True))
        if (read_json(manifest_path) != original_master
                or any(read_json(path) != cm for path, cm in collections)
                or load_policy(ROOT) != policy):
            raise ArchiveError('Candidate metadata changed while building')
        replacements.extend([(metadata / 'SHA256SUMS', release_dir / 'SHA256SUMS', True),
                             (metadata / 'checksums.json', release_dir / 'checksums.json', True),
                             (metadata / 'manifest.json', manifest_path, True)])
        commit_generation(replacements)
    for asset in assets:
        print('Built', asset['name'], asset['files'], 'files', flush=True)
    print(json.dumps({'status': 'candidate-built', 'assets': len(assets), 'files': len(all_records)}))


if __name__ == '__main__':
    main()
