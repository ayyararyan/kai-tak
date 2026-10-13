"""Create a compact manuscript source ZIP; no environments or raw third-party scans."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent
DEST=ROOT.parent/'checkers-with-runway-13-white-paper-v2-source.zip'
allowed_root={'.tex','.py','.md','.txt','.json'}
files=[]
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT)
    if rel.parts[0]=='evidence': files.append(p)
    elif len(rel.parts)==1 and (p.suffix in allowed_root or p.name=='checkers-with-runway-13-white-paper-v2.pdf'): files.append(p)
    elif rel.parts[0]=='figures' and p.suffix=='.pdf': files.append(p)
    elif rel.parts[0]=='qa' and p.suffix=='.json': files.append(p)
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):z.write(p,Path('checkers-with-runway-13-white-paper-v2-source')/p.relative_to(ROOT))
print(f'{DEST.name}: {len(files)} files, {DEST.stat().st_size} bytes')
