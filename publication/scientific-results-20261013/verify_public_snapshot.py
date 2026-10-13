"""Verify public bytes against source/public mapping without rewriting scientific seals.

This checks publication provenance, NOT mathematical sufficiency. The original
preservation verifiers require the complete private/source workspace and are kept
unchanged. Missing items must be explicitly classified, never silently passed.
"""
from pathlib import Path
import collections
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ROOT = REPO / 'research/checkers-runway13'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check():
    mapping = json.loads((HERE / 'source_public_mapping.json').read_text())
    by_source = {r['source_path']: r for r in mapping['files']}
    require(len(by_source) == len(mapping['files']), 'duplicate source path')
    for row in mapping['files']:
        path = REPO / row['public_path']
        require(path.is_file() and path.stat().st_size == row['public_bytes']
                and digest(path) == row['public_sha256'], 'public byte mismatch: ' + row['public_path'])
    for row in mapping['exclusions']:
        require(not (ROOT / row['path']).exists(), 'excluded file present: ' + row['path'])
    base = ROOT / 'integrated/assumption_solution'
    sealed_count = 0
    for rel in ['artifact_manifest.json', 'refinement/artifact_manifest.json',
                'refinement/local_certificate/artifact_manifest.json']:
        path = base / rel
        own = by_source[str(path.relative_to(ROOT))]
        require(own['source_sha256'] == own['public_sha256'], 'original seal transformed')
        for name, record in json.loads(path.read_text())['files'].items():
            row = by_source[str((path.parent / name).relative_to(ROOT))]
            require(record['sha256'] == row['source_sha256'] and record['bytes'] == row['source_bytes'],
                    'source binding mismatch: ' + name)
            sealed_count += 1
    preserved = json.loads((base / 'refinement/local_certificate/preserved_snapshot.json').read_text())
    disposition = json.loads((HERE / 'preserved_path_disposition.json').read_text())['paths']
    require(len(disposition) == len(preserved) == 610, 'preservation count mismatch')
    require({r['path'] for r in disposition} == set(preserved), 'preservation membership mismatch')
    for row in disposition:
        original = preserved[row['path']]
        require((row['source_sha256'], row['source_bytes']) == (original['sha256'], original['bytes']),
                'preservation source binding mismatch')
        path = ROOT / row['path']
        if row['status'] == 'not_in_git':
            require(bool(row['reason']) and not path.exists(), 'missing disposition no longer applies')
        else:
            require(path.is_file() and path.stat().st_size == row['public_bytes']
                    and digest(path) == row['public_sha256'], 'preserved public mismatch: ' + row['path'])
            if row['status'] == 'normalized_git':
                source = by_source[row['path']]
                require(bool(source['transformations']) and source['public_sha256'] == row['public_sha256'],
                        'undocumented normalization')
            else:
                require(row['public_sha256'] == row['source_sha256'], 'identical claim mismatch')
    require(sealed_count == 224, 'sealed artifact count mismatch')
    return {'status': 'PASS', 'mapped_public_files': len(mapping['files']),
            'sealed_source_bindings': sealed_count, 'original_sealed_manifests': 3,
            'preservation_dispositions': dict(collections.Counter(r['status'] for r in disposition)),
            'scope': 'public-copy integrity; does not assert private-source reproduction or scientific completeness'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
