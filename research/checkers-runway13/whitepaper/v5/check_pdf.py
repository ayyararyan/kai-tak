"""Automated document checks and all-page renders; does not assert visual approval."""
import sys
if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O.')
from pathlib import Path
import hashlib,json,re,subprocess
import pymupdf as fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;Q=P/'qa';Q.mkdir(exist_ok=True)
pdf=P/'checkers-with-runway-13-white-paper-v5.pdf';doc=fitz.open(pdf)
texts=[p.get_text() for p in doc];text='\n'.join(texts);log=(P/'main.log').read_text()
issues=[]
for pat in ['Overfull','Missing character','undefined references','Citation .* undefined','Reference .* undefined','Label\\(s\\) may have changed']:
 if re.search(pat,log):issues.append('Typesetting: '+pat)
assert '??' not in text and '\ufffd' not in text
assert doc.metadata['title']=='Checkers with Runway 13'
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True);(Q/'fonts.txt').write_text(fonts)
for l in fonts.splitlines()[2:]:
 assert re.search(r'\byes\s+(?:yes|no)\s+(?:yes|no)\b',l),'Font not embedded: '+l
assert all(f in fonts for f in ['Times-Roman','Times-Bold','Times-Italic','NewTXMI'])
assert len(re.findall(r'\\bibitem\[',(P/'main.bbl').read_text()))==14
assert 'FIRST-PERSON DRAFT' in text or 'FOR AUTHOR APPROVAL' in text or "FOR ARYAN AYYAR'S REVIEW" in text
for phrase in ['0.0397','0.1559772','0.1507934696816132','171,307','3,780','2,786','313.49','302.11','2,531.32','2,233.23','254.68','552.77']:
 assert phrase in text,'Missing core result '+phrase
subprocess.run(['pdftotext','-layout',str(pdf),str(Q/'paper-poppler.txt')],check=True)
assert 'Checkers with Runway 13' in (Q/'paper-poppler.txt').read_text()
(Q/'paper-text.txt').write_text(text)
pgdir=Q/'pages';pgdir.mkdir(exist_ok=True)
bad=[];links=0;body=[];pageinfo=[]
for i,p in enumerate(doc):
 assert abs(p.rect.width-517.38)<.1 and abs(p.rect.height-779.30)<.1
 for b in p.get_text('dict')['blocks']:
  if b['type']!=0:continue
  for line in b['lines']:
   for s in line['spans']:
    if not s['text'].strip():continue
    r=fitz.Rect(s['bbox'])
    if r.x0<10 or r.y0<8 or r.x1>p.rect.width-9 or r.y1>p.rect.height-8:bad.append({'page':i+1,'text':s['text'],'box':list(r)})
    if s['font']=='Times-Roman' and abs(s['size']-11.955)<.05:body.append(s['size'])
 for l in p.get_links():
  links+=1
  assert not(l['kind']==fitz.LINK_GOTO and l.get('page',-1)<0),'Unresolved link'
 pix=p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False);pix.save(pgdir/f'{i+1:02}.png')
 pageinfo.append({'page':i+1,'text_sha256':hashlib.sha256(texts[i].encode()).hexdigest(),'pixel_sha256':hashlib.sha256(pix.samples).hexdigest(),'words':len(texts[i].split())})
assert body,'Expected 12pt Times body missing'
assert not bad,bad
for start in range(0,len(doc),4):
 sheet=Image.new('RGB',(1500,2260),'#dddddd');draw=ImageDraw.Draw(sheet)
 for j,i in enumerate(range(start,min(start+4,len(doc)))):
  im=Image.open(pgdir/f'{i+1:02}.png');im.thumbnail((725,1100));x=(j%2)*750;y=(j//2)*1130;sheet.paste(im,(x+(750-im.width)//2,y+25));draw.text((x+12,y+5),f'V5 PDF page {i+1}',fill='black')
 sheet.save(Q/f'contact-{start+1:02}.jpg',quality=94)
report={'pages':len(doc),'title':doc.metadata['title'],'geometry_pdf_pt':[517.38,779.30],'body_TeX_pt':12,'baseline_TeX_pt':14.4,'references':14,'all_fonts_embedded':True,'links':links,'layout_issues':issues,'page_records':pageinfo,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'visual_review':'Requires separate actual-page inspection, not inferred from these checks.'}
(Q/'document_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='page_records'},indent=2))
if issues:raise SystemExit('Repair typesetting issues before acceptance.')
