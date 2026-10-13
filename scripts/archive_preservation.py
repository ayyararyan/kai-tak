#!/usr/bin/env python3
"""Verify pre-audit evidence and historical tags without modifying sources."""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--workspace',type=Path,required=True);p.add_argument('--original-checkout',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
 inv=json.loads((ROOT/'archive/audit/initial_inventory.json').read_text())['files'];fail=[];counts={}
 for r in inv:
  loc=r['storage']
  if loc=='remote-checkout':
   if not r['path'].startswith(('research/','publication/','data/')):continue
   path=ROOT/r['path']
  elif loc=='local-checkout':path=a.original_checkout/r['path']
  elif loc in ['research-workspace','data-workspace']:path=a.workspace/r['path']
  else:continue
  if r.get('symlink') or r.get('read_error') or not r.get('sha256'):continue
  counts[loc]=counts.get(loc,0)+1
  if not path.is_file() or path.is_symlink() or sha(path)!=r['sha256']:fail.append({'location':loc,'path':r['path'],'reason':'Missing or checksum changed since initial audit'})
 h=json.loads((ROOT/'archive/audit/git_history.json').read_text());actual=subprocess.check_output(['git','show-ref','--tags'],cwd=ROOT,text=True).splitlines();tags_unchanged=sorted(actual)==sorted(h['tags'])
 dirty=subprocess.check_output(['git','status','--porcelain'],cwd=a.original_checkout,text=True).splitlines();dirty_unchanged=dirty==h['local_dirty']
 report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed' if not fail and tags_unchanged and dirty_unchanged else 'failed','evidence_files_hashed_by_location':counts,'failures':fail,'historical_tags_unchanged':tags_unchanged,'original_checkout_status_unchanged':dirty_unchanged,'source_mutation_performed':False,'scope':'Meaningful public-safe initial inventory; runtime/cache/private entries omitted from this distributable receipt. Original private inventory retained separately.'}
 a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return int(report['status']!='passed')
if __name__=='__main__':raise SystemExit(main())
