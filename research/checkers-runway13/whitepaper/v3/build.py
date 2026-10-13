"""Reproduce Version 3 figures/manuscript from immutable supplied inputs."""
from pathlib import Path
import sys,subprocess,os,json,hashlib,shutil
P=Path(__file__).resolve().parent;os.chdir(P);(P/'qa').mkdir(exist_ok=True)
if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O: inherited evidence checks contain assertions.')
manifest=P/'SOURCE_MANIFEST.json'
if not manifest.exists():raise SystemExit('SOURCE_MANIFEST.json missing; do not invent replacement evidence.')
m=json.loads(manifest.read_text())
for row in m['files']:
 f=P/row['path']
 if hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:raise RuntimeError('Changed source: '+row['path'])
for script in ['verify_v2_inputs.py','make_figures.py','verify_v3_claims.py']:
 with (P/'qa'/(script.replace('.py','')+'.log')).open('w') as out:subprocess.run([sys.executable,script],stdout=out,stderr=subprocess.STDOUT,check=True)
with (P/'qa/compile_console.log').open('w') as out:subprocess.run(['tectonic','--keep-logs','--keep-intermediates','main.tex'],stdout=out,stderr=subprocess.STDOUT,check=True)
shutil.copy2(P/'main.pdf',P/'checkers-with-runway-13-white-paper-v3.pdf')
subprocess.run([sys.executable,'check_pdf.py'],check=True)
print('Immutable input hashes checked:',len(m['files']))
