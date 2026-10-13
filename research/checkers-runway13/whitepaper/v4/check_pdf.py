from pathlib import Path
import json,hashlib,re,subprocess,sys,unicodedata
import pymupdf as fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;Q=P/'qa';Q.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def normal(s):
 s=re.sub(r'\\(?:clearpage|vfill|par|medskip|smallskip|allowbreak)\b','',s)
 s=re.sub(r'\\Needspace\{\d+\\baselineskip\}','',s)
 s=s.replace('\\citep','\\cite')
 s=re.sub(r'\\section\{Appendix [A-F]\. ',r'\\section{',s)
 # One explicit layout-only wrapper around the summary contents table.
 s=s.replace(r'{\small\begin{tabularx}{\textwidth}{@{}rXr@{}}',r'\begin{tabularx}{\textwidth}{@{}rXr@{}}').replace(r'\end{tabularx}}',r'\end{tabularx}')
 return re.sub(r'\s+','',s)
files=[*sorted((P/'sections').glob('*.tex')),P/'appendices.tex',P/'coefficients.tex']
for f in files:
 a=(P/'baseline'/f.relative_to(P)).read_text();b=f.read_text()
 assert normal(a)==normal(b),'Content changed: '+str(f)
 # Compare paragraph blocks separately; layout-only blocks do not count.
 assert [normal(x) for x in a.split('\n\n') if normal(x)]==[normal(x) for x in b.split('\n\n') if normal(x)],'Paragraph change'
a=(P/'baseline/references.bib').read_text();b=(P/'references.bib').read_text();assert a==b.replace('year={n.d.},','').replace('type={Aircraft accident report},','')
for row in json.loads((P/'FORMAT_BASELINE.json').read_text())['files']:assert sha(P/row['path'])==row['sha256'],row['path']
for row in json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']:assert sha(P/row['path'])==row['sha256'],row['path']
pdf=P/'checkers-with-runway-13-white-paper-v4.pdf';d=fitz.open(pdf);texts=[p.get_text() for p in d];text='\n'.join(texts)
assert d.metadata['title']=='Checkers with Runway 13'
log=(P/'main.log').read_text()
for pat in ['Overfull','Missing character','undefined references','Citation .* undefined','Reference .* undefined','Label\\(s\\) may have changed']:
 assert not re.search(pat,log),'Typesetting defect '+pat
assert '??' not in text and '\ufffd' not in text
assert 'Appendix Appendix' not in text and 'n.d.b,n' not in text
for phrase in ['0.0397','0.1559772','0.1507934696816132','0.216744','313.49','302.11','2,531.32','2,233.23','254.68','552.77','FIRST-PERSON DRAFT']:
 assert phrase in text,phrase
assert all(re.search(r'Figure '+str(i)+r'\n',text) for i in range(1,17))
assert all('Insight '+str(i)+':' in text for i in range(1,8))
assert len(re.findall(r'\\bibitem\[',(P/'main.bbl').read_text()))==14
subprocess.run(['pdftotext','-layout',str(pdf),str(Q/'paper-poppler.txt')],check=True)
pop=(Q/'paper-poppler.txt').read_text();assert '552.77' in pop and 'Checkers with Runway 13' in pop
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True);(Q/'fonts.txt').write_text(fonts)
font_lines=fonts.splitlines()[2:];assert all(re.search(r'\byes\s+(?:yes|no)\s+(?:yes|no)\b',l) for l in font_lines)
assert 'Times-Roman' in fonts and 'Times-Bold' in fonts and 'Times-Italic' in fonts and 'NewTXMI' in fonts
nonunicode=[l.strip() for l in font_lines if re.search(r'\byes\s+(?:yes|no)\s+no\b',l)]
assert all(any(n in l for n in ['txsys','txexs']) for l in nonunicode),'Unexpected Unicode map failure'
pages=Q/'pages';pages.mkdir(exist_ok=True);bad=[];body=[];links=0;unresolved=[]
for i,p in enumerate(d):
 assert abs(p.rect.width-517.38)<.1 and abs(p.rect.height-779.30)<.1
 for b in p.get_text('dict')['blocks']:
  if b['type']!=0:continue
  for ln in b['lines']:
   for s in ln['spans']:
    if not s['text'].strip():continue
    r=fitz.Rect(s['bbox'])
    if r.x0<12 or r.y0<8 or r.x1>p.rect.width-10 or r.y1>p.rect.height-8:bad.append({'page':i+1,'text':s['text'],'rect':list(r)})
    if s['font']=='Times-Roman' and abs(s['size']-11.955)<.05:body.append(s['size'])
 for l in p.get_links():
  links+=1
  if l['kind']==fitz.LINK_GOTO and l.get('page',-1)<0:unresolved.append(l)
 p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(pages/f'{i+1:02}.png')
assert not bad,bad
assert not unresolved,unresolved
assert body,'12 TeX pt Times body not found'
for k in range(0,len(d),2):
 out=Image.new('RGB',(1800,1400),'#dddddd');draw=ImageDraw.Draw(out)
 for j in range(2):
  if k+j>=len(d):continue
  im=Image.open(pages/f'{k+j+1:02}.png');im.thumbnail((885,1350));out.paste(im,(j*900+(900-im.width)//2,30));draw.text((j*900+15,8),f'PDF page {k+j+1}',fill='black')
 out.save(Q/f'page-pair-{k+1:02}.jpg',quality=94)
r={'pages':len(d),'figures':16,'insights':7,'references':14,'body_files_preserved':len(files),'paragraph_boundaries_and_emphasis_preserved':True,'bibliography_change':'n.d. labels for six originally undated records; explicit CAD accident-report type; all source records and citation keys retained','immutable_input_hashes':104,'all_fonts_embedded':True,'body_fonts_have_unicode':True,'legacy_math_fonts_without_explicit_ToUnicode':nonunicode,'geometry_mm':[182.52,274.92],'body_TeX_pt':12,'baseline_TeX_pt':14.4,'all_text_within_page':True,'resolved_links':links,'pdf_sha256':sha(pdf),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in texts],'visual_review':'separate receipt required','scope':'Formatting verification, not new scientific or operational validation'}
(Q/'document_checks.json').write_text(json.dumps(r,indent=2)+'\n');(Q/'paper-text.txt').write_text(text)
print(json.dumps({k:v for k,v in r.items() if k!='page_text_sha256'},indent=2))
