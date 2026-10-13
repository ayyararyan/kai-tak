"""Write a SHA256 inventory after rendering, assembly and QA are finished."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

A = Path(__file__).resolve().parents[1]
target = A / 'metadata/artifact_manifest.json'
files = []
for path in sorted(A.rglob('*')):
    rel = path.relative_to(A)
    if not path.is_file() or path == target:
        continue
    if any(p.startswith('.') or p == '__pycache__' for p in rel.parts):
        continue
    if path.suffix == '.blend1' or 'superseded-scenes' in rel.parts:
        continue
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    files.append({'path': str(rel), 'bytes': path.stat().st_size,
                  'sha256': digest.hexdigest(), 'role': rel.parts[0]})
target.write_text(json.dumps({
    'generated_utc': datetime.now(timezone.utc).isoformat(),
    'exclusions': ['this self-referential manifest', 'hidden/runtime cache files',
                   'Blender .blend1 backups and qa/superseded-scenes'],
    'files': files,
    'total_bytes': sum(f['bytes'] for f in files),
}, indent=2) + '\n')
print(f'Inventoried {len(files)} files; {sum(f["bytes"] for f in files):,} bytes')
