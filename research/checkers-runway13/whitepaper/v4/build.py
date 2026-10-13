"""Build the V4 RFS author-format manuscript. No model changes or optimization."""
from pathlib import Path
import sys,subprocess,os,json,hashlib,shutil
P=Path(__file__).resolve().parent;os.chdir(P);(P/'qa').mkdir(exist_ok=True)
if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O.')
for row in json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']:
 if hashlib.sha256((P/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise RuntimeError('Changed source: '+row['path'])
if '--figures' in sys.argv:
 for script in ['verify_v2_inputs.py','make_figures.py','verify_v3_claims.py']:
  with (P/'qa'/(script.replace('.py','')+'.log')).open('w') as out:subprocess.run([sys.executable,script],stdout=out,stderr=subprocess.STDOUT,check=True)
engine=os.environ.get('XELATEX') or shutil.which('xelatex')
if not engine:raise SystemExit('Install XeLaTeX and put it on PATH, or set XELATEX to its executable.')
engine=str(Path(engine).resolve());bib=os.environ.get('BIBTEX') or str(Path(engine).parent/'bibtex')
# symlink resolution can erase the xelatex invocation name; use the given executable.
engine=os.environ.get('XELATEX') or shutil.which('xelatex')
for iteration in range(1,5):
 with (P/'qa'/f'compile-{iteration}.log').open('w') as out:subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','main.tex'],stdout=out,stderr=subprocess.STDOUT,check=True)
 if iteration==1:
  with (P/'qa/bibtex.log').open('w') as out:subprocess.run([bib,'main'],stdout=out,stderr=subprocess.STDOUT,check=True)
shutil.copy2(P/'main.pdf',P/'checkers-with-runway-13-white-paper-v4.pdf')
if (P/'check_pdf.py').exists():subprocess.run([sys.executable,'check_pdf.py'],check=True)
print('V4 manuscript compiled; 104 immutable input hashes checked.')
