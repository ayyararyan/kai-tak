#!/usr/bin/env python3
"""Test actual candidate bytes through local HTTP into a clean source checkout.

Creates a new, explicit outside-repository test directory. Never publishes.
"""
import argparse,hashlib,http.server,json,shutil,subprocess,sys,tarfile,threading,functools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(cmd,cwd):
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=900)
 return {'command':[str(c).replace(str(cwd),'<clean-checkout>') for c in cmd],'returncode':p.returncode,'stdout':p.stdout[-5000:],'stderr':p.stderr[-3000:]}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bundles',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
 if a.work.exists():raise SystemExit('Acceptance work directory must be new')
 if a.work.resolve()==ROOT or ROOT in a.work.resolve().parents:raise SystemExit('Acceptance work must be outside source tree')
 a.work.mkdir(parents=True);clean=a.work/'clean';clean.mkdir();base=a.work/'baseline.tar';manifest=json.loads((ROOT/'archive/releases/v1.0.0/manifest.json').read_text())
 with base.open('wb') as f:subprocess.run(['git','archive',manifest['source_commit']],cwd=ROOT,stdout=f,check=True)
 with tarfile.open(base) as tf:tf.extractall(clean,filter='data')
 for directory in ['archive','scripts','tests']:
  shutil.copytree(ROOT/directory,clean/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
 for name in ['README.md','CITATION.cff']:
  if (ROOT/name).exists():shutil.copyfile(ROOT/name,clean/name)
 handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(a.bundles.resolve()));server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 for asset in manifest['assets']:asset['url']=f'http://127.0.0.1:{server.server_port}/'+asset['name']
 (clean/'archive/releases/v1.0.0/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');cache=a.work/'cache';report=a.work/'restore.json';runs=[]
 try:
  runs.append(run([sys.executable,'scripts/fetch_data.py','--release','v1.0.0','--archive-dir',str(cache),'--report',str(report)],clean))
  runs.append(run([sys.executable,'scripts/archive_reproduce.py','--report',str(a.work/'reproduction.json')],clean))
  # A checksum-only run must not create destination directories.
  empty=a.work/'must-not-exist';runs.append(run([sys.executable,'scripts/fetch_data.py','--release','v1.0.0','--collection','05','--archive-dir',str(cache),'--offline','--verify-only','--destination',str(empty)],clean));verify_no_mutation=not empty.exists()
  # Idempotent full restore exercises identical already-existing files.
  runs.append(run([sys.executable,'scripts/fetch_data.py','--release','v1.0.0','--offline','--archive-dir',str(cache)],clean))
 finally:server.shutdown();server.server_close();thread.join()
 result={'schema_version':'1.0.0','status':'passed' if all(r['returncode']==0 for r in runs) and verify_no_mutation else 'failed','scope':f"Actual {len(manifest['assets'])} candidate bundles via loopback HTTP into baseline checkout with proposed archive tooling; public URLs remain absent.",'source_commit':manifest['source_commit'],'runs':runs,'verify_only_no_destination_mutation':verify_no_mutation,'public_download_verified':False,'local_download_restore_verified':all(r['returncode']==0 for r in runs),'complete_historical_reproducibility':False}
 if report.exists():
  receipt=json.loads(report.read_text());result['restored_assets']=receipt['assets'];result['reported_exception_count']=len(receipt['exceptions'])
 if (a.work/'reproduction.json').exists():result['reproduction']=json.loads((a.work/'reproduction.json').read_text())
 # Hide machine-specific test paths in the distributable report.
 text=json.dumps(result,indent=2).replace(str(a.work),'<acceptance-work>');a.report.write_text(text+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['runs','restored_assets','reproduction']},indent=2));return 0 if result['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
