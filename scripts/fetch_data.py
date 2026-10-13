#!/usr/bin/env python3
"""Download, verify and restore the versioned public research data snapshot."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-dir', type=Path, default=ROOT / '.data-downloads')
    parser.add_argument('--verify-only', action='store_true', help='verify archive and member hashes without extracting')
    args = parser.parse_args()
    args.archive_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / 'publication/release_assets.json').read_text())
    snapshot = json.loads((ROOT / 'publication/snapshot_manifest.json').read_text())
    for asset in manifest['assets']:
        archive = args.archive_dir / asset['name']
        if not archive.exists():
            print('Downloading', asset['name'], flush=True)
            temporary = archive.with_suffix(archive.suffix + '.partial')
            with urllib.request.urlopen(asset['url'], timeout=90) as response, temporary.open('wb') as out:
                shutil.copyfileobj(response, out)
            if digest(temporary) != asset['sha256']:
                raise RuntimeError('Download checksum mismatch: ' + asset['name'])
            temporary.replace(archive)
        if archive.stat().st_size != asset['bytes'] or digest(archive) != asset['sha256']:
            raise RuntimeError('Archive integrity mismatch: ' + asset['name'])
        expected = {r['path']: r for r in snapshot['included'] if r['delivery'] == asset['delivery']}
        seen = set()
        with tarfile.open(archive, 'r:gz') as bundle:
            for member in bundle:
                rel = PurePosixPath(member.name)
                if rel.is_absolute() or '..' in rel.parts or not member.isfile() or member.name not in expected or member.name in seen:
                    raise RuntimeError('Unexpected/unsafe archive member: ' + member.name)
                target = ROOT.joinpath(*rel.parts)
                if ROOT not in target.resolve().parents:
                    raise RuntimeError('Path escapes repository: ' + member.name)
                info = expected[member.name]
                if member.size != info['bytes']:
                    raise RuntimeError('Member size mismatch: ' + member.name)
                original = bundle.extractfile(member)
                assert original is not None
                if args.verify_only or target.exists():
                    found = hashlib.file_digest(original, 'sha256').hexdigest()
                    if found != info['sha256']:
                        raise RuntimeError('Member checksum mismatch: ' + member.name)
                    if target.exists() and (target.is_symlink() or digest(target) != found):
                        raise RuntimeError('Refusing to overwrite different local file: ' + member.name)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    temporary = target.with_name(target.name + '.restoring')
                    with temporary.open('wb') as out:
                        shutil.copyfileobj(original, out)
                    if digest(temporary) != info['sha256']:
                        raise RuntimeError('Member checksum mismatch: ' + member.name)
                    temporary.replace(target)
                seen.add(member.name)
        if seen != set(expected):
            raise RuntimeError('Archive member set mismatch: ' + asset['name'])
        print(('Verified' if args.verify_only else 'Restored'), asset['name'], len(seen), 'files', flush=True)

if __name__ == '__main__':
    main()
