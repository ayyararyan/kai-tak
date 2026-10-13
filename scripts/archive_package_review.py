#!/usr/bin/env python3
"""Create a LOCAL review/preservation package from a clean committed branch.

The Git bundle contains mixed-rights history: private preservation, NOT a public
upload. The support tar requires author approval. This command never publishes.
"""
import argparse,gzip,hashlib,json,os,subprocess,tarfile,tempfile,datetime
from pathlib import Path
from archive_io import digest,verify_bundle
ROOT=Path(__file__).resolve().parents[1]
def git(*args,**kwargs):return subprocess.check_output(['git',*args],cwd=ROOT,**kwargs)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bundles',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();out=a.output_dir.resolve()
 if out.exists() or out==ROOT or ROOT in out.parents:raise SystemExit('Use a new directory outside the source tree')
 if git('status','--porcelain').strip():raise SystemExit('Commit reviewed source first; dirty checkout refused')
 master=json.loads((ROOT/'archive/releases/v1.0.0/manifest.json').read_text())
 if master['status']!='candidate':raise SystemExit('This command is only for an unpublished local review candidate')
 revision=git('rev-parse','HEAD',text=True).strip();branch=git('symbolic-ref','--short','HEAD',text=True).strip();out.mkdir(parents=True);files=[]
 for asset in master['assets']:
  source=a.bundles/asset['name'];cm=json.loads((ROOT/'archive/releases/v1.0.0'/asset['manifest']).read_text())
  with source.open('rb') as f:verify_bundle(f,asset,cm['files'])
  os.link(source,out/asset['name']);files.append(dict(name=asset['name'],bytes=asset['bytes'],sha256=asset['sha256'],treatment='source-specific redistribution conditions; publication authorization still absent'))
 name='kai-tak-archive-v1.0.0-private-source-history.bundle';git('bundle','create',str(out/name),branch)
 verify=subprocess.run(['git','bundle','verify',str(out/name)],cwd=ROOT,capture_output=True,text=True,check=True)
 files.append(dict(name=name,bytes=(out/name).stat().st_size,sha256=digest(out/name),treatment='PRIVATE preservation only; includes mixed-rights inherited Git history, not proposed for public deposit'))
 names=[x for x in git('ls-tree','-r','--name-only',revision,text=True).splitlines() if x.startswith(('archive/','scripts/','tests/')) or x in ['README.md','CITATION.cff','.gitignore']]
 name='kai-tak-archive-v1.0.0-review-support.tar.gz'
 with tempfile.TemporaryDirectory(prefix='kai-tak-support-') as td:
  raw=Path(td)/'source.tar'
  with raw.open('wb') as f:subprocess.run(['git','archive',revision,'--',*names],cwd=ROOT,stdout=f,check=True)
  with tarfile.open(raw) as source,(out/name).open('wb') as f,gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w|') as target:
   for info in sorted(source.getmembers(),key=lambda x:x.name):
    if info.isdir():continue
    if not info.isfile():raise SystemExit('Unexpected non-regular support member')
    info.mtime=info.uid=info.gid=0;info.uname=info.gname='';info.mode=0o644;info.pax_headers={};target.addfile(info,source.extractfile(info))
 files.append(dict(name=name,bytes=(out/name).stat().st_size,sha256=digest(out/name),files=len(names),treatment='Review-only metadata/tooling; original-work license grants and publication approval pending; excludes inherited research bytes'))
 receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'LOCAL-REVIEW-ONLY','archive_version':'1.0.0','source_commit':revision,'baseline_commit':master['source_commit'],'branch':branch,'public_release_created':False,'doi_assigned':False,'license_granted':False,'files':files,'source_bundle_verified':verify.returncode==0}
 (out/'REVIEW_PACKAGE_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
 (out/'SHA256SUMS').write_text(''.join(f"{x['sha256']}  {x['name']}\n" for x in files))
 (out/'README.md').write_text(f'''# Local archival review package — NOT a public release\n\nExact archive branch commit: `{revision}`.\nBaseline: `{master['source_commit']}`.\n\nFive data bundles have source-specific redistribution conditions. The review-support tar contains metadata/tooling awaiting original-work license approval. The Git bundle contains mixed-rights inherited history and is PRIVATE preservation only, not a proposed Zenodo upload. No DOI/license grant/publication is implied.\n\nVerify: `shasum -a 256 -c SHA256SUMS`.\n\nTo restore the exact private review environment locally:\n\n```sh\ngit clone kai-tak-archive-v1.0.0-private-source-history.bundle restored\ncd restored\ngit checkout {branch}\npython3 scripts/fetch_data.py --release v1.0.0 --offline --archive-dir .. --report /new/path/restore.json\n```\n\nThe catalogue states remaining missing/restricted sources. See `archive/PUBLICATION_READINESS.md`. The support tar alone does not include inherited research dependencies. Do not upload this directory wholesale.\n''')
 print(json.dumps({'status':receipt['status'],'source_commit':revision,'files':len(files),'output_dir':str(out)}))
if __name__=='__main__':main()
