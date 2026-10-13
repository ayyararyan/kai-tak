#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,os,sys,time,shutil
A=Path(__file__).resolve().parents[1]
blender=os.environ.get('BLENDER') or shutil.which('blender') or '/Users/maheit/.cache/kaitak-blender/Blender.app/Contents/MacOS/Blender'
jobs=json.loads((A/'metadata/render_jobs.json').read_text())
chosen=set(sys.argv[1:]);unknown=chosen-{j['id'] for j in jobs}
if unknown:raise SystemExit('Unknown render jobs: '+', '.join(sorted(unknown)))
status=[]
for job in jobs:
 if chosen and job['id'] not in chosen:continue
 out=Path(job['output']);record=out.with_suffix('.render.json')
 cmd=[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(A/'scripts/render_scene.py'),'--','--atlas',str(A),'--job',str(A/f'scenes/jobs/{job["id"]}.json')]
 started=time.time()
 with (A/f'qa/render-{job["id"]}.log').open('w') as log:
  rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
 ok=rc==0 and out.exists() and record.exists()
 status.append(dict(id=job['id'],success=ok,returncode=rc,seconds=round(time.time()-started,2)))
 (A/'qa/render_progress.json').write_text(json.dumps(status,indent=2)+'\n')
 print(job['id'],ok,status[-1]['seconds'],flush=True)
 if not ok:sys.exit(1)
