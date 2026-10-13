"""Run all original V5 visual masters from documented source inputs."""
import sys
if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O.')
from pathlib import Path
import json,hashlib,subprocess,sys
P=Path(__file__).resolve().parent
for r in json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']:
 assert hashlib.sha256((P/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
for r in json.loads((P/'inputs/historical/SOURCE_MANIFEST.json').read_text())['records']:
 assert hashlib.sha256((P/r['snapshot']).read_bytes()).hexdigest()==r['sha256'],r['snapshot']
for script in ['historical_figures.py','mechanics_figures.py','evidence_figures.py']:
 subprocess.run([sys.executable,str(P/'scripts'/script)],cwd=P,check=True)
records=[r for f in sorted((P/'qa/figure-records').glob('*.json')) if 'figure' in (r:=json.loads(f.read_text()))]
assert len(records)==15 and len({r['figure'] for r in records})==15
(P/'qa/figure_provenance.json').write_text(json.dumps(records,indent=2)+'\n')
print('Generated',len(records),'V5 figures; all original evidence hashes preserved.')
