"""Fail-closed archive I/O; no third-party dependencies (Python 3.11+).

POSIX directory descriptors prevent symlink-ancestor races. Restore is staged and
no-clobber: an interruption can leave verified files, never unverified targets.
A receipt is emitted only after all selected bundles have succeeded.
"""
from contextlib import contextmanager
from pathlib import Path
import gzip
import hashlib
import json
import os
import re
import shutil
import stat
import tarfile
import unicodedata
import urllib.parse
import urllib.request
import uuid


class ArchiveError(ValueError):
    pass


def read_json(path):
    """Read trusted metadata without following a substituted link or special file."""
    path = Path(path)
    with directory(path.parent) as parent, regular_file(parent, path.name) as stream:
        return json.load(stream)


def load_policy(root):
    archive = Path(root) / 'archive'
    catalogue = read_json(archive / 'catalogue/artifacts.json')
    indexes = []
    for rows in (catalogue['artifacts'],
                 read_json(archive / 'licensing/rights_registry.json')['records'],
                 read_json(archive / 'catalogue/datasets.json')['datasets']):
        index = {r['id']: r for r in rows}
        if len(index) != len(rows):
            raise ArchiveError('Duplicate policy identity')
        indexes.append(index)
    return catalogue['archive_version'], *indexes


def validate_collection_policy(collection, policy):
    """Bind every selected byte to the authoritative catalogue and rights registry."""
    version, artifacts, rights, datasets = policy
    cid = collection['collection_id']
    if collection['archive_version'] != version:
        raise ArchiveError('Collection/catalogue version mismatch')
    rows = collection['files']
    records_by_path(rows)
    seen = set()
    for row in rows:
        identifier = row.get('artifact_id')
        item = artifacts.get(identifier)
        if identifier in seen or not item:
            raise ArchiveError('Duplicate or unknown manifest artifact: ' + str(identifier))
        seen.add(identifier)
        if (not item.get('included_in_v1') or item.get('symlink')
                or item.get('collection_id') != cid
                or item.get('provenance_status') not in ('source-and-checksum-bound',
                    'pinned-source-and-output-hashes', 'producer-reassembly-byte-identical')
                or any(row.get(k) != item.get(k) for k in
                       ('path', 'bytes', 'sha256', 'rights_id', 'publication_decision'))):
            raise ArchiveError('Manifest/catalogue policy mismatch: ' + row['path'])
        dataset = row.get('dataset_id')
        if dataset not in datasets or not item.get('dataset_ids') or dataset != item['dataset_ids'][0]:
            raise ArchiveError('Manifest dataset identity mismatch: ' + row['path'])
        right = rights.get(row.get('rights_id'))
        if (row.get('publication_decision') != 'Redistribution permitted' or not right
                or right.get('publication_decision') != 'Redistribution permitted'):
            raise ArchiveError('Registry does not permit redistribution: ' + row['path'])
    expected = {x['id'] for x in artifacts.values()
                if x.get('included_in_v1') and x.get('collection_id') == cid}
    if seen != expected:
        raise ArchiveError('Collection/catalogue permitted member set mismatch: ' + cid)


def safe_path(name):
    if not isinstance(name, str) or not name or name.startswith('/') or '\\' in name:
        raise ArchiveError('Unsafe path: ' + repr(name))
    parts = name.split('/')
    reserved = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', re.I)
    if any(p in ('', '.', '..') or p.casefold() in ('.git', '.hg', '.svn', '.archive-receipts') or p.endswith((' ', '.')) or ':' in p or reserved.match(p)
           or any(unicodedata.category(c).startswith('C') for c in p) for p in parts):
        raise ArchiveError('Unsafe path: ' + repr(name))
    return parts


def collision_key(name):
    return unicodedata.normalize('NFC', name).casefold()


def records_by_path(records):
    result, folded = {}, set()
    for r in records:
        safe_path(r['path'])
        key = collision_key(r['path'])
        if key in folded:
            raise ArchiveError('Duplicate/colliding path: ' + r['path'])
        if type(r.get('bytes')) is not int or r['bytes'] < 0 or not re.fullmatch('[0-9a-f]{64}', r.get('sha256', '')):
            raise ArchiveError('Invalid file integrity metadata: ' + r['path'])
        folded.add(key)
        result[r['path']] = r
    for key in folded:
        bits = key.split('/')
        if any('/'.join(bits[:i]) in folded for i in range(1, len(bits))):
            raise ArchiveError('File/directory path collision: ' + key)
    return result


@contextmanager
def directory(path, create=False):
    """Open every ancestor without following symlinks, including an absolute root."""
    absolute = Path(os.path.abspath(path))
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in absolute.parts[1:]:
            if create:
                try:
                    os.mkdir(part, 0o755, dir_fd=fd)
                except FileExistsError:
                    pass
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        yield fd
    finally:
        os.close(fd)


@contextmanager
def relative_parent(root_fd, rel, create=False):
    parts = safe_path(rel)
    fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            if create:
                try:
                    os.mkdir(part, 0o755, dir_fd=fd)
                except FileExistsError:
                    pass
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        yield fd, parts[-1]
    finally:
        os.close(fd)


@contextmanager
def regular_file(parent_fd, name):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ArchiveError('Not a regular file: ' + name)
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            yield stream
    finally:
        os.close(fd)


def stream_hash(stream):
    return hashlib.file_digest(stream, 'sha256').hexdigest()


def digest(path):
    with directory(Path(path).parent) as parent:
        with regular_file(parent, Path(path).name) as stream:
            return stream_hash(stream)


def check_stream(stream, record):
    stream.seek(0)
    if os.fstat(stream.fileno()).st_size != record['bytes'] or stream_hash(stream) != record['sha256']:
        raise ArchiveError('File hash/size mismatch: ' + record.get('path', record.get('name', '?')))
    stream.seek(0)


def atomic_json(path, obj, replace=False):
    path = Path(path)
    with directory(path.parent, create=True) as fd:
        name = '.archive-json-' + uuid.uuid4().hex
        raw = (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode()
        handle = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
        try:
            with os.fdopen(handle, 'wb') as out:
                out.write(raw)
                out.flush()
                os.fsync(out.fileno())
            if replace:
                try:
                    mode = os.stat(path.name, dir_fd=fd, follow_symlinks=False).st_mode
                    if not stat.S_ISREG(mode):
                        raise ArchiveError('Refusing nonregular report/manifest target')
                except FileNotFoundError:
                    pass
                os.replace(name, path.name, src_dir_fd=fd, dst_dir_fd=fd)
            else:
                os.link(name, path.name, src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
        finally:
            try:
                os.unlink(name, dir_fd=fd)
            except FileNotFoundError:
                pass


def validate_asset(asset, records):
    expected = records_by_path(records)
    if len(safe_path(asset['name'])) != 1:
        raise ArchiveError('Asset name must be a basename')
    if type(asset.get('bytes')) is not int or asset['bytes'] < 0 or not re.fullmatch('[0-9a-f]{64}', asset.get('sha256', '')):
        raise ArchiveError('Invalid archive integrity metadata')
    if asset.get('files') != len(expected) or asset.get('unpacked_bytes') != sum(r['bytes'] for r in records):
        raise ArchiveError('Inconsistent archive counts/totals')
    return expected


class BoundedReader:
    """Bound decompressed tar bytes, including headers and padding."""
    def __init__(self, stream, limit):
        self.stream, self.remaining = stream, limit
    def read(self, size=-1):
        size = min(size if size >= 0 else self.remaining + 1, self.remaining + 1)
        value = self.stream.read(size)
        self.remaining -= len(value)
        if self.remaining < 0:
            raise ArchiveError('Archive exceeds decompressed size bound')
        return value


@contextmanager
def tar_stream(stream, expected):
    stream.seek(0)
    # Allow bounded PAX headers/long filenames but not unbounded expansion.
    limit = sum(r['bytes'] for r in expected.values()) + len(expected) * 65536 + 1048576
    with gzip.GzipFile(fileobj=stream, mode='rb') as gz:
        bounded = BoundedReader(gz, limit)
        with tarfile.open(fileobj=bounded, mode='r|') as bundle:
            yield bundle
        # Read trailer/remaining gzip members too; compressed bombs after tar EOF fail.
        while bounded.read(1024 * 1024):
            pass


def verify_bundle(stream, asset, records):
    expected = validate_asset(asset, records)
    check_stream(stream, asset)
    seen = set()
    with tar_stream(stream, expected) as bundle:
        for member in bundle:
            safe_path(member.name)
            if member.name in seen or member.name not in expected or not member.isfile() or member.sparse is not None:
                raise ArchiveError('Unexpected/unsafe archive member: ' + member.name)
            info = expected[member.name]
            if member.size != info['bytes']:
                raise ArchiveError('Member size mismatch: ' + member.name)
            source = bundle.extractfile(member)
            if source is None or stream_hash(source) != info['sha256']:
                raise ArchiveError('Member checksum mismatch: ' + member.name)
            seen.add(member.name)
    if seen != set(expected):
        raise ArchiveError('Archive member set mismatch')
    stream.seek(0)
    return expected


def obtain_bundle(cache, asset, records, offline=False):
    validate_asset(asset, records)
    with directory(cache, create=True) as fd:
        try:
            with regular_file(fd, asset['name']) as stream:
                verify_bundle(stream, asset, records)
            return Path(cache) / asset['name']
        except FileNotFoundError:
            pass
        if offline or not asset.get('url'):
            raise ArchiveError('Bundle unavailable locally; no authorized published URL: ' + asset['name'])
        parsed = urllib.parse.urlparse(asset['url'])
        if parsed.scheme not in ('https', 'http') or parsed.username or parsed.password:
            raise ArchiveError('Only credential-free HTTP(S) download URLs are allowed')
        temp = '.archive-download-' + uuid.uuid4().hex
        out_fd = os.open(temp, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
        try:
            with os.fdopen(out_fd, 'w+b') as out:
                with urllib.request.urlopen(asset['url'], timeout=90) as response:
                    if urllib.parse.urlparse(response.geturl()).scheme not in ('http', 'https'):
                        raise ArchiveError('Unsafe download redirect')
                    total = 0
                    while True:
                        chunk = response.read(min(1024 * 1024, asset['bytes'] - total + 1))
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > asset['bytes']:
                            raise ArchiveError('Download exceeds declared size')
                        out.write(chunk)
                out.flush()
                os.fsync(out.fileno())
                verify_bundle(out, asset, records)
            os.link(temp, asset['name'], src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
        finally:
            os.unlink(temp, dir_fd=fd)
    return Path(cache) / asset['name']


def preflight_destination(destination, records):
    expected = records_by_path(records)
    with directory(destination, create=True) as fd:
        for rel, record in expected.items():
            try:
                with relative_parent(fd, rel) as (parent, name):
                    with regular_file(parent, name) as stream:
                        check_stream(stream, record)
            except FileNotFoundError:
                pass


def restore_bundle(path, asset, records, destination):
    with directory(Path(path).parent) as cache_fd:
        with regular_file(cache_fd, Path(path).name) as stream:
            expected = verify_bundle(stream, asset, records)
            preflight_destination(destination, records)
            with directory(destination, create=True) as root_fd:
                stage_name = '.archive-stage-' + uuid.uuid4().hex
                os.mkdir(stage_name, 0o700, dir_fd=root_fd)
                stage_fd = os.open(stage_name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root_fd)
                staged = []
                try:
                    seen = set()
                    with tar_stream(stream, expected) as bundle:
                        for member in bundle:
                            safe_path(member.name)
                            if (member.name in seen or member.name not in expected
                                    or not member.isfile() or member.sparse is not None):
                                raise ArchiveError('Changed/unsafe archive member: ' + member.name)
                            if member.size != expected[member.name]['bytes']:
                                raise ArchiveError('Changed member size: ' + member.name)
                            seen.add(member.name)
                            key = str(len(staged))
                            fd = os.open(key, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=stage_fd)
                            staged.append((key, member.name))
                            with os.fdopen(fd, 'wb') as out:
                                shutil.copyfileobj(bundle.extractfile(member), out)
                                out.flush()
                                os.fsync(out.fileno())
                            with regular_file(stage_fd, key) as check:
                                check_stream(check, expected[member.name])
                    if seen != set(expected):
                        raise ArchiveError('Changed archive member set')
                    check_stream(stream, asset)
                    # No target is changed until every staged byte is verified.
                    preflight_destination(destination, records)
                    for key, rel in staged:
                        with relative_parent(root_fd, rel, create=True) as (parent, name):
                            try:
                                os.link(key, name, src_dir_fd=stage_fd, dst_dir_fd=parent, follow_symlinks=False)
                            except FileExistsError:
                                with regular_file(parent, name) as existing:
                                    check_stream(existing, expected[rel])
                finally:
                    for key, _ in staged:
                        os.unlink(key, dir_fd=stage_fd)
                    os.close(stage_fd)
                    os.rmdir(stage_name, dir_fd=root_fd)
    return len(records)
