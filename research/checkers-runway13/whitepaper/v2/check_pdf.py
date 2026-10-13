from pathlib import Path
import hashlib
import json
import re
import subprocess
import pymupdf as fitz

ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa'
QA.mkdir(exist_ok=True)
pdf=ROOT/'checkers-with-runway-13-white-paper-v2.pdf'
doc=fitz.open(pdf)
texts=[p.get_text() for p in doc]
full='\n'.join(texts)
(QA/'pymupdf_text.txt').write_text(full)
subprocess.run(['pdftotext','-layout',str(pdf),str(QA/'poppler_text.txt')],check=True)
poppler=(QA/'poppler_text.txt').read_text()
assert len(texts)>8 and all(len(t.strip())>40 for t in texts)
for term in ['Executive summary','The research question','Conclusion','References','0.0397','0.1559772','254.68','8,285','552.769','0.1507934696816132','0.2167443782','Wind conversion']:
    assert term in full, f'Missing extracted content: {term}'
    assert term in poppler, f'Missing Poppler content: {term}'
assert '??' not in full
log=(ROOT/'main.log').read_text()
fatal=[line for line in log.splitlines() if re.search(r'Overfull|Missing character|undefined|multiply defined',line,re.I)
       and 'undefined control sequences' not in line.lower()]
assert not fatal, fatal
overflow=[]
for i,p in enumerate(doc):
    for b in p.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            for span in line['spans']:
                if not span['text'].strip(): continue
                x0,y0,x1,y1=span['bbox']
                if x0<10 or y0<10 or x1>p.rect.width-10 or y1>p.rect.height-10:
                    overflow.append({'page':i+1,'text':span['text'],'bbox':span['bbox']})
assert not overflow, overflow
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
(QA/'fonts.txt').write_text(fonts)
for line in fonts.splitlines()[2:]:
    # All fonts must be embedded; pdffonts tail is emb/sub/uni/object/ID.
    assert line.split()[-5]=='yes', line
links=sum(len(p.get_links()) for p in doc)
assert links>=8
for i,p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(.8,.8)).save(QA/f'page-{i+1:02}.png')
result={'pages':len(doc),'characters':len(full),'all_pages_have_text':True,
        'both_extractors_checked':True,'text_within_page_bounds':True,
        'no_unresolved_refs_or_missing_glyphs_or_overfull_boxes':True,
        'all_fonts_embedded':True,'pdf_links':links,
        'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'visual_inspection':'pending human/assistant rendered-page inspection',
        'scientific_scope':'Document/data-derivation checks; no new independent scientific peer review.'}
(QA/'document_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
