"""Document acceptance and render output; human/model visual review remains a separate step."""
from pathlib import Path
import json,re,hashlib,subprocess,sys
import pymupdf as fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;Q=P/'qa';pdf=P/'checkers-with-runway-13-white-paper-v3.pdf';d=fitz.open(pdf)
if not 25<=len(d)<=35:raise RuntimeError(f'Unexpected length {len(d)}')
if d.metadata['title']!='Checkers with Runway 13':raise RuntimeError('Title changed')
log=(P/'main.log').read_text()
for pat in ['Overfull','Missing character','undefined references','Citation .* undefined','Reference .* undefined']:
 if re.search(pat,log):raise RuntimeError('Typesetting defect: '+pat)
texts=[p.get_text() for p in d];text='\n'.join(texts)
if '??' in text or '\ufffd' in text:raise RuntimeError('Broken text or cross-reference')
for phrase in ['0.0397','0.1559772','0.1507934696816132','0.216744','313.49','302.11','2,531.32','2,233.23','254.68','552.77','FIRST-PERSON DRAFT']:
 if phrase not in text:raise RuntimeError('Missing required claim '+phrase)
if not all(f'Figure {i}:' in text for i in range(1,17)):raise RuntimeError('Missing numbered figure')
if not all(f'Insight {i}:' in text for i in range(1,8)):raise RuntimeError('Missing insight')
subprocess.run(['pdftotext','-layout',str(pdf),str(Q/'paper-poppler.txt')],check=True)
pop=(Q/'paper-poppler.txt').read_text()
if 'Checkers with' not in pop or '552.77' not in pop:raise RuntimeError('Second text extractor failed')
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True);(Q/'fonts.txt').write_text(fonts)
if any(not re.search(r'\byes\s+yes\s+yes\b',line) for line in fonts.splitlines()[2:]):
 # Embedding and Unicode matter; subset can be no for a fully embedded font.
 for line in fonts.splitlines()[2:]:
  if not re.search(r'\byes\s+(?:yes|no)\s+yes\b',line):raise RuntimeError('Font embedding/Unicode issue '+line)
bad=[];pages=Q/'pages';pages.mkdir(exist_ok=True);links=0
for i,p in enumerate(d):
 for b in p.get_text('dict')['blocks']:
  if b['type']!=0:continue
  for line in b['lines']:
   for s in line['spans']:
    r=fitz.Rect(s['bbox'])
    if r.x0<12 or r.y0<8 or r.x1>p.rect.width-10 or r.y1>p.rect.height-8:bad.append({'page':i+1,'text':s['text'],'rect':list(r)})
 links+=len(p.get_links());p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(pages/f'{i+1:02d}.png')
if bad:raise RuntimeError('Page overflow '+repr(bad))
for k in range(0,len(d),2):
 out=Image.new('RGB',(1800,1320),'#dddddd');draw=ImageDraw.Draw(out)
 for j in range(2):
  if k+j>=len(d):continue
  im=Image.open(pages/f'{k+j+1:02d}.png');im.thumbnail((885,1280));out.paste(im,(j*900+(900-im.width)//2,30));draw.text((j*900+15,8),f'PDF page {k+j+1}',fill='black')
 out.save(Q/f'page-pair-{k+1:02d}.jpg',quality=92)
fore=(P/'sections/foreword.tex').read_text();body=fore.split('Long before',1)[1].split('\\vfill',1)[0];wc=len(re.findall(r"\b[\w]+(?:['’][\w]+)?\b",'Long before'+body))
if not 400<=wc<=600:raise RuntimeError('Foreword length '+str(wc))
r={'pages':len(d),'foreword_words_approx':wc,'figures':16,'insights':7,'links':links,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'text_extractors':['PyMuPDF','Poppler'],'embedded_unicode_fonts':True,'no_overfull_missing_glyph_or_unresolved_reference':True,'page_text_bounds_passed':True,'visual_inspection':'separate explicit receipt required','page_text_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in texts]}
(Q/'document_checks.json').write_text(json.dumps(r,indent=2)+'\n');(Q/'paper-text.txt').write_text(text);print(json.dumps({k:v for k,v in r.items() if k!='page_text_sha256'},indent=2))
