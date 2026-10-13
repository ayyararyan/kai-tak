from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
for entry in manifest['files']:
    path=root/entry['path']
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual==entry['sha256'], f'Hash mismatch: {path}'
print(f"Verified {len(manifest['files'])} SHA256 file identities.")
