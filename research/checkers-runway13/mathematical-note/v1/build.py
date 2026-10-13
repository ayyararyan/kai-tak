#!/usr/bin/env python3
"""Build the mathematical note from local, manifest-bound inputs; never optimize."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys
P=Path(__file__).resolve().parent

def run(cmd,log):
    with (P/'qa'/log).open('w') as out:
        subprocess.run(cmd,cwd=P,stdout=out,stderr=subprocess.STDOUT,check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--figures',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args()
    (P/'qa').mkdir(exist_ok=True)
    if (P/'INPUT_MANIFEST.json').exists():
        for r in json.loads((P/'INPUT_MANIFEST.json').read_text())['files']:
            if hashlib.sha256((P/r['path']).read_bytes()).hexdigest()!=r['sha256']:
                raise RuntimeError('Frozen build input differs: '+r['path'])
    run([sys.executable,'scripts/verify_content.py'],'content-checks.log')
    if a.figures:run([sys.executable,'make_figures.py'],'figures.log')
    engine=os.environ.get('XELATEX') or shutil.which('xelatex')
    if not engine:raise SystemExit('XeLaTeX required: add its bin directory to PATH or set XELATEX.')
    bib=os.environ.get('BIBTEX') or shutil.which('bibtex') or str(Path(engine).parent/'bibtex')
    for n in range(1,5):
        run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','main.tex'],f'compile-{n}.log')
        if n==1:run([bib,'main'],'bibtex.log')
    shutil.copy2(P/'main.pdf',P/'certified-local-optimality-v1.pdf')
    run([sys.executable,'scripts/check_pdf.py']+(['--render'] if a.render else []),'pdf-checks.log')
    print('Build and automated document checks passed. Mathematical and visual review have separate receipts.')
if __name__=='__main__':main()
