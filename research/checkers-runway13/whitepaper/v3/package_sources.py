"""Package manuscript inputs, sources, figures and concise receipts, excluding caches/renders."""
from pathlib import Path
import zipfile,hashlib,json
P=Path(__file__).resolve().parent
NAME='checkers-with-runway-13-white-paper-v3-sources.zip'
def source_files():
 for f in sorted(P.rglob('*')):
  if not f.is_file():continue
  r=f.relative_to(P)
  if any(x in {'.venv','__pycache__','.pytest_cache'} for x in r.parts):continue
  if r.parts[0] in {'evidence','inputs','figures','sections'}:yield f;continue
  if r.parts[0]=='qa':
   if len(r.parts)==2 and f.suffix in {'.json','.log','.txt'} and f.name not in {'baseline_hashes.json','paper-text.txt','paper-poppler.txt','clean_environment_install.log','certificate_rerun.log','compile_console.log','build_result.log'}:yield f
   continue
  if len(r.parts)==1 and f.name not in {'main.pdf','main.log','main.aux','main.bbl','main.blg','main.out','DELIVERY_MANIFEST.json'} and f.suffix in {'.tex','.bib','.py','.md','.json','.csv','.txt','.pdf'}:yield f
if __name__=='__main__':
 files=list(source_files())
 with zipfile.ZipFile(P/NAME,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in files:z.write(f,'checkers-with-runway-13-v3/'+str(f.relative_to(P)))
 with zipfile.ZipFile(P/NAME) as z:
  assert z.testzip() is None
  for f in files:assert z.read('checkers-with-runway-13-v3/'+str(f.relative_to(P)))==f.read_bytes()
 r={'archive':NAME,'members':len(files),'bytes':(P/NAME).stat().st_size,'sha256':hashlib.sha256((P/NAME).read_bytes()).hexdigest(),'all_members_match_source':True,'pdf_sha256':hashlib.sha256((P/'checkers-with-runway-13-white-paper-v3.pdf').read_bytes()).hexdigest()}
 (P/'DELIVERY_MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
