"""Rebuild V5 from immutable evidence and editable master sources; never optimize."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
P=Path(__file__).resolve().parent

def run(argv,log=None):
 if log:
  with (P/'qa'/log).open('w') as out:subprocess.run(argv,cwd=P,stdout=out,stderr=subprocess.STDOUT,check=True)
 else:subprocess.run(argv,cwd=P,check=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--figures',action='store_true');ap.add_argument('--proofs',action='store_true');ap.add_argument('--compile-only',action='store_true');a=ap.parse_args()
 if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O.')
 (P/'qa').mkdir(exist_ok=True)
 for r in json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']:
  if hashlib.sha256((P/r['path']).read_bytes()).hexdigest()!=r['sha256']:raise RuntimeError('Changed frozen input: '+r['path'])
 if not a.compile_only:run([sys.executable,'scripts/verify_v5_science.py'],'science_build.log')
 if a.proofs:run([sys.executable,'verify_certificates.py'],'proof_build.log')
 if a.figures:run([sys.executable,'make_figures.py'],'figures_build.log')
 if not a.compile_only:run([sys.executable,'scripts/verify_v5_figures.py'],'figure_semantics_build.log')
 # abstract.md is the editable abstract source; math is written as valid TeX.
 abstract=(P/'abstract.md').read_text().strip()
 (P/'abstract.tex').write_text('\\abstract{'+abstract+'}\n')
 engine=os.environ.get('XELATEX') or shutil.which('xelatex')
 if not engine:raise SystemExit('XeLaTeX required: set XELATEX or add it to PATH.')
 bib=os.environ.get('BIBTEX') or shutil.which('bibtex') or str(Path(engine).parent/'bibtex')
 for n in range(1,5):
  run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','main.tex'],f'compile-{n}.log')
  if n==1:run([bib,'main'],'bibtex.log')
 shutil.copy2(P/'main.pdf',P/'checkers-with-runway-13-white-paper-v5.pdf')
 run([sys.executable,'check_pdf.py'])
 print('V5 manuscript/figure build checked. Visual inspection is a separate required receipt.')
if __name__=='__main__':main()
