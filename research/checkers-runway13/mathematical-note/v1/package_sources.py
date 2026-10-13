#!/usr/bin/env python3
"""Create a deterministic portable source package; does not publish."""
from pathlib import Path
import argparse, hashlib, json, zipfile
P=Path(__file__).resolve().parent
NAME='certified-local-optimality-v1-sources.zip'
SKIP_DIRS={'.venv','__pycache__','.pytest_cache','.git','pages'}
SKIP_SUFFIX={'.aux','.log','.out','.bbl','.blg','.toc','.synctex.gz','.pyc','.zip'}
# Selected evidence logs are kept, including all documented failures and proof logs.
def selected(f):
    rel=f.relative_to(P)
    if any(x in SKIP_DIRS for x in rel.parts):return False
    if f.name in {'main.pdf','DELIVERY_MANIFEST.json','PACKAGE_MANIFEST.json'}:return False
    if f.suffix=='.log':return rel.parts[0]=='verification' or (rel.parts[0]=='frozen-source')
    if f.suffix in SKIP_SUFFIX:return False
    if rel.parts[:2]==('qa','contact-sheets'):return False
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);a=ap.parse_args()
    output=a.output or P/NAME
    files=sorted([f for f in P.rglob('*') if f.is_file() and selected(f)],key=lambda f:f.relative_to(P).as_posix())
    # All included frozen entries must equal the immutable snapshot manifest.
    manifest=json.loads((P/'frozen-source/PUBLIC_SOURCE_MANIFEST.json').read_text())
    assert len(manifest['files']) == manifest['file_count']
    total = 0
    for relative, expected in manifest['files'].items():
        data = (P/'frozen-source'/relative).read_bytes()
        if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
            raise RuntimeError('Frozen source differs: '+relative)
        total += len(data)
    assert total == manifest['total_bytes']
    records=[]
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in files:
            rel=f.relative_to(P).as_posix();data=f.read_bytes()
            info=zipfile.ZipInfo(rel,(2026,10,14,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,data);records.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    with zipfile.ZipFile(output) as z:
        assert len(z.namelist())==len(records) and len(set(z.namelist()))==len(records)
        for r in records:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
    receipt={'archive':output.name,'members':len(records),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'files':records}
    (P/'PACKAGE_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='files'},indent=2))
if __name__=='__main__':main()
