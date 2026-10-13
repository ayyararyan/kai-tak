#!/usr/bin/env python3
"""Replay the named NOAA weather tables in isolation using only stdlib and collection 05."""
import argparse,csv,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PREFIX=Path('research/checkers-runway13/evidence');LANE=PREFIX/'cal605_reconstruction/noaa';RAW=PREFIX/'weather_feasibility_2026-10-13/NOAA_450070-99999-1993.gz'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run_step(command, lane):
 try:
  return subprocess.run(command,cwd=lane,text=True,capture_output=True,timeout=90)
 except subprocess.TimeoutExpired as exc:
  detail=exc.stderr or ''
  if isinstance(detail,bytes):detail=detail.decode(errors='replace')
  return subprocess.CompletedProcess(command,124,'',detail+'\nReplay step timed out after 90 seconds')
 except OSError as exc:
  return subprocess.CompletedProcess(command,127,'',str(exc))
def replay(data_root):
 catalogue=json.loads((ROOT/'archive/catalogue/artifacts.json').read_text());am={x['path']:x for x in catalogue['artifacts']};source=data_root/RAW
 if not source.is_file():return {'status':'blocked','reason':'Restore collection 05 first','missing':str(RAW)}
 if sha(source)!=am[str(RAW)]['sha256']:return {'status':'failed','reason':'Source checksum mismatch','source_original_unchanged':False}
 with tempfile.TemporaryDirectory(prefix='kai-tak-replay-') as td:
  base=Path(td);lane=base/LANE;lane.mkdir(parents=True);(base/RAW).parent.mkdir(parents=True);shutil.copyfile(source,base/RAW)
  for n in ['decode_noaa.py','test_decode_noaa.py','isd-format-document.pdf']:
   if not (ROOT/LANE/n).is_file():return {'status':'blocked','reason':'Missing replay dependency','missing':str(LANE/n)}
   shutil.copyfile(ROOT/LANE/n,lane/n)
  producer=run_step([sys.executable,'decode_noaa.py'],lane)
  tests=run_step([sys.executable,'-m','unittest','test_decode_noaa.py','-v'],lane)
  outputs=[]
  for n in ['observations_1993.csv','observations_1993-11-04.csv']:
   p=lane/n;expected=am[str(LANE/n)];h=sha(p) if p.exists() else None
   count=None
   if p.is_file():
    with p.open() as f:count=sum(1 for _ in csv.DictReader(f))
   outputs.append({'path':str(LANE/n),'sha256':h,'expected_sha256':expected['sha256'],'byte_identical':h==expected['sha256'],'rows':count})
  return {'schema_version':'1.0.0','status':'passed' if producer.returncode==tests.returncode==0 and all(x['byte_identical'] for x in outputs) else 'failed','producer_exit':producer.returncode,'producer_stderr':producer.stderr.replace(str(lane),'<isolated-replay>'),'tests_exit':tests.returncode,'tests_output':tests.stderr.replace(str(lane),'<isolated-replay>'),'outputs':outputs,'scope':'Two named NOAA derived tables and decoder tests; not other research lanes or historical aircraft wind-field validation.','source_original_unchanged':sha(source)==am[str(RAW)]['sha256']}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data-root',type=Path,default=ROOT);p.add_argument('--report',type=Path);a=p.parse_args();r=replay(a.data_root)
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2));return 0 if r['status']=='passed' else 2
if __name__=='__main__':raise SystemExit(main())
