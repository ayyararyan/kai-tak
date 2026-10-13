"""Portable deterministic V5 source/figure package with explicit exclusions."""
import sys
if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O.')
from pathlib import Path
import hashlib,json,zipfile
P=Path(__file__).resolve().parent
OUT=P/'checkers-with-runway-13-white-paper-v5-sources.zip'
DIRS=['sections','scripts','figures','presentation','inputs','evidence','editorial']
EXT={'.py','.md','.csv','.json','.tex','.bib','.cls','.bst','.sty','.cfg','.png','.jpg','.pdf','.svg','.geojson','.ply','.txt','.npy','.npz'}
files=[]
for f in P.iterdir():
 if f.is_file() and f.suffix in EXT and f.name not in {'main.pdf','abstract.tex','DELIVERY_MANIFEST.json'}:files.append(f)
for d in DIRS:
 for f in (P/d).rglob('*'):
  if f.is_file() and f.suffix in EXT and '__pycache__' not in f.parts:files.append(f)
# Compact acceptance evidence, not bulky rendered page images/compiler logs.
for f in (P/'qa').glob('*.json'):
 if f.name not in {'package_manifest.json','clean-location.json','delivery_acceptance.json'}:files.append(f)
for f in (P/'qa/figure-records').glob('*.json'):files.append(f)
if (P/'qa/fonts.txt').is_file():files.append(P/'qa/fonts.txt')
files=sorted(set(files));records=[]
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in files:
  rel=f.relative_to(P).as_posix();data=f.read_bytes()
  if f.is_symlink():raise ValueError('No symlink sources '+rel)
  zi=zipfile.ZipInfo('checkers-with-runway-13-v5/'+rel,(2026,10,13,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16
  z.writestr(zi,data);records.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
with zipfile.ZipFile(OUT) as z:
 assert len(z.namelist())==len(records)
 for r in records:assert hashlib.sha256(z.read('checkers-with-runway-13-v5/'+r['path'])).hexdigest()==r['sha256']
r={'members':len(records),'archive_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'files':records,'scope':'Source/figure package. No installable proprietary fonts or restricted CAD scans.'}
(P/'qa/package_manifest.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'members':len(records),'bytes':OUT.stat().st_size,'sha256':r['archive_sha256']},indent=2))
