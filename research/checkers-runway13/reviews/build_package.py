"""Package reproducible local model, excluding environments and third-party papers."""
from pathlib import Path
import hashlib
import json
import zipfile
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'checkers-runway13-model-v1.zip'
paths=list(ROOT.glob('*.md'))+[ROOT/'requirements.lock',ROOT/'.gitignore']
paths+=list((ROOT/'model').glob('*.py'))+[ROOT/'model/config.json']
paths+=list((ROOT/'reviews').glob('*.md'))+list((ROOT/'reviews').glob('*.py'))
paths+=list((ROOT/'foundations').glob('*'))
paths+=list((ROOT/'evidence').glob('*.csv'))+[ROOT/'evidence/EVIDENCE_REPORT.md']
paths+=list((ROOT/'outputs/scenario').glob('*'))+list((ROOT/'outputs/historical').glob('*'))
paths+=[ROOT/'outputs/artifact_acceptance.json']
paths=sorted(set(p for p in paths if p.is_file()))
manifest={str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths}
with zipfile.ZipFile(DEST,'w',zipfile.ZIP_DEFLATED) as z:
    for p in paths:z.write(p,arcname='checkers-runway13/'+str(p.relative_to(ROOT)))
    z.writestr('checkers-runway13/PACKAGE_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(DEST) as z:
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read('checkers-runway13/'+p)).hexdigest()==meta['sha256'] for p,meta in manifest.items())
print(json.dumps({'path':str(DEST),'files':len(paths)+1,'bytes':DEST.stat().st_size,'sha256':hashlib.sha256(DEST.read_bytes()).hexdigest()},indent=2))
