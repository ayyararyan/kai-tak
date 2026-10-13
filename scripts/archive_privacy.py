#!/usr/bin/env python3
"""Bounded pattern and inclusion scan; emits counts/paths, never matched values."""
import argparse,collections,datetime,json,re,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'machine-path':re.compile(rb'/' + rb'Users/[^\s\"\'<>]+'),
 'secret-shaped':re.compile(rb'gh[pousr]_[A-Za-z0-9]{25,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----'),
 'private-session-query':re.compile(rb'[?&](?:token|access_token|signature|sessionid|auth)=[^&\s\"<>]+',re.I)}
TEXT={'.json','.geojson','.csv','.md','.txt','.py','.cff','.tfw','.wld','.xml','.html','.tex','.yaml','.yml','.jsonld'}
def scan(stream,label,findings):
 tail=b'';counts=collections.Counter()
 while b:=stream.read(1024*1024):
  block=tail+b
  for kind,rx in PATTERNS.items():
   counts[kind]+=sum(m.end()>len(tail) for m in rx.finditer(block))
  tail=block[-256:]
 findings.extend({'path':label,'kind':k,'count':v} for k,v in counts.items() if v)
def main():
 p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();findings=[];scanned=0;nested=0
 files=list((ROOT/'archive').rglob('*'))+list((ROOT/'scripts').glob('archive_*.py'))+list((ROOT/'tests').glob('*.py'))+[ROOT/'README.md',ROOT/'CITATION.cff',ROOT/'scripts/fetch_data.py']
 for f in files:
  if f.is_file() and f.suffix in TEXT and f!=a.report.resolve():
   with f.open('rb') as s:scan(s,str(f.relative_to(ROOT)),findings)
   scanned+=1
 arts=json.loads((ROOT/'archive/catalogue/artifacts.json').read_text())['artifacts'];included=[x for x in arts if x['included_in_v1']]
 for x in included:
  f=a.data_root/x['path']
  if not f.is_file() or f.is_symlink():findings.append({'path':x['path'],'kind':'missing-or-symlink'});continue
  if f.suffix in TEXT:
   with f.open('rb') as s:scan(s,x['path'],findings)
   scanned+=1
  if f.suffix=='.zip':
   with zipfile.ZipFile(f) as z:
    for info in z.infolist():
     nested+=1;name=info.filename;parts=Path(name).parts
     if name.startswith('/') or '..' in parts or '\\' in name or any(q.startswith('.') for q in parts) or (info.external_attr>>16)&0o170000==0o120000:findings.append({'path':x['path'],'member':name,'kind':'unexpected-nested-member'})
     if Path(name).suffix in TEXT:
      with z.open(info) as s:scan(s,x['path']+'!'+name,findings)
 report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed-pattern-scan' if not findings else 'review-required','text_files_scanned':scanned,'permitted_files_reviewed':len(included),'nested_zip_members_inspected':nested,'findings':findings,'scope':'New metadata/code and exact permitted source members; nested ZIP names/text inspected. Private/runtime files excluded from public inventory and bundle allowlist. Binary image semantics and arbitrary encoded secrets are not proven absent by a pattern scan.','matched_values_emitted':False}
 a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='scope'}));return bool(findings)
if __name__=='__main__':raise SystemExit(main())
