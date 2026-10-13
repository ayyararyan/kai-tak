"""Select the settled V4 publication files; exclude all build/private scratch."""
from pathlib import Path
import zipfile,hashlib,json
P=Path(__file__).resolve().parent
NAME='checkers-with-runway-13-white-paper-v4-sources.zip'
def source_files():
 for f in sorted(P.rglob('*')):
  if not f.is_file():continue
  r=f.relative_to(P)
  if any(x in {'.venv','__pycache__','.pytest_cache'} for x in r.parts):continue
  if r.parts[0] in {'evidence','inputs','figures','sections','baseline'}:yield f;continue
  if r.parts[0]=='qa':
   if len(r.parts)==3 and r.parts[1]=='v3-baseline':yield f
   elif len(r.parts)==2 and f.suffix=='.json':yield f
   elif len(r.parts)==2 and f.name=='fonts.txt':yield f
   continue
  if r==Path('.gitignore'):yield f;continue
  if len(r.parts)==1 and f.name not in {'main.pdf','main.log','main.aux','main.bbl','main.blg','main.out','DELIVERY_MANIFEST.json','PUBLICATION_INVENTORY.json','check_pdf_v3_reference.py'} and f.suffix in {'.tex','.bib','.py','.md','.json','.csv','.txt','.pdf','.sty','.cls','.cfg','.bst'}:yield f
if __name__=='__main__':
 files=list(source_files());rows=[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]
 with zipfile.ZipFile(P/NAME,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in files:z.write(f,'checkers-with-runway-13-v4/'+str(f.relative_to(P)))
 with zipfile.ZipFile(P/NAME) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(files)
  for f in files:assert z.read('checkers-with-runway-13-v4/'+str(f.relative_to(P)))==f.read_bytes()
 r={'archive':NAME,'members':len(files),'bytes':(P/NAME).stat().st_size,'sha256':hashlib.sha256((P/NAME).read_bytes()).hexdigest(),'all_members_match_source':True,'pdf_sha256':hashlib.sha256((P/'checkers-with-runway-13-white-paper-v4.pdf').read_bytes()).hexdigest()}
 (P/'DELIVERY_MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n');(P/'PUBLICATION_INVENTORY.json').write_text(json.dumps({'files':rows,'selection':'Exact source ZIP members; archive and these two manifests additionally published'},indent=2)+'\n');print(json.dumps(r,indent=2))
