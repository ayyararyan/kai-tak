"""Restore published Blender scenes/assets, checking archive and every member."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import tempfile
import urllib.request
import zipfile

A = Path(__file__).resolve().parents[1]
ROOT = A.parents[1]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def restore(archive, destination):
    manifest = json.loads((A / 'metadata/scene_bundle.json').read_text())
    if sha(archive.read_bytes()) != manifest['sha256']:
        raise ValueError('Archive checksum mismatch')
    with zipfile.ZipFile(archive) as bundle:
        expected = {r['path']: r for r in manifest['members']}
        if len(bundle.namelist()) != len(expected) or set(bundle.namelist()) != set(expected):
            raise ValueError('Archive member set mismatch')
        # Validate the entire archive and all destinations before writing anything.
        for name, record in expected.items():
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name:
                raise ValueError('Unsafe archive path')
            data = bundle.read(name)
            if len(data) != record['bytes'] or sha(data) != record['sha256']:
                raise ValueError('Member checksum mismatch: ' + name)
            target = destination / name
            if not target.resolve().is_relative_to(destination.resolve()):
                raise ValueError('Destination escapes through a symlink')
            if target.exists() and (not target.is_file() or sha(target.read_bytes()) != record['sha256']):
                raise ValueError('Conflicting local file: ' + name)
        for name in expected:
            target = destination / name
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(bundle.read(name))
    print(f'Verified/restored {len(expected)} scene and asset files')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--destination', type=Path, default=ROOT)
    args = parser.parse_args()
    if args.archive:
        restore(args.archive, args.destination)
    else:
        manifest = json.loads((A / 'metadata/scene_bundle.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / 'scenes.zip'
            urllib.request.urlretrieve(manifest['url'], archive)
            restore(archive, args.destination)
