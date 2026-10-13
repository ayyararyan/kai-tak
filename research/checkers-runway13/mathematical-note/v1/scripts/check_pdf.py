#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,subprocess,shutil
import fitz
P=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--render',action='store_true');a=ap.parse_args()
pdf=fitz.open(P/'certified-local-optimality-v1.pdf')
texts=[];pageinfo=[];fontnames=set();bad=[]
for i,page in enumerate(pdf):
    text=page.get_text();texts.append(text)
    if abs(page.rect.width-182.52/25.4*72)>.03 or abs(page.rect.height-274.92/25.4*72)>.03:bad.append(f'wrong page size {i+1}')
    for f in page.get_fonts(full=True):fontnames.add(f[3].split('+')[-1])
    spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
    overflow=[s['text'] for s in spans if s['bbox'][0]<-1 or s['bbox'][2]>page.rect.width+1 or s['bbox'][1]<-1 or s['bbox'][3]>page.rect.height+1]
    if overflow:bad.append(f'page {i+1} physical overflow {overflow}')
    if len(text.strip())<10:bad.append(f'empty page {i+1}')
    pageinfo.append({'page':i+1,'width_pt':page.rect.width,'height_pt':page.rect.height,'text_chars':len(text),'spans':len(spans),'physical_overflow':overflow})
    if a.render:
        d=P/'qa/pages';d.mkdir(exist_ok=True);page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(d/f'page-{i+1:02}.png')
log=(P/'qa/compile-4.log').read_text()
for pattern in ['undefined references','Citation .* undefined','Reference .* undefined','Missing character:','LaTeX Error:']:
    if re.search(pattern,log,re.I):bad.append('LaTeX '+pattern)
check_fonts={'Times-Roman','Times-Bold','Times-Italic','NewTXMI'}
if not check_fonts<=fontnames:bad.append('missing expected fonts '+str(check_fonts-fontnames))
fonts=shutil.which('pdffonts')
if fonts:
    report=subprocess.check_output([fonts,str(P/'certified-local-optimality-v1.pdf')],text=True);(P/'qa/fonts.txt').write_text(report)
    for line in report.splitlines()[2:]:
        # Poppler's embedded column is three tokens before object id pair, allowing font-type spaces.
        if re.search(r'\sno\s+(?:yes|no)\s+(?:yes|no)\s+\d+\s+\d+\s*$',line):bad.append('unembedded font '+line)
text='\n'.join(texts);(P/'qa/manuscript.txt').write_text(text)
result={'pages':len(pdf),'fonts':sorted(fontnames),'page_info':pageinfo,'failures':bad,'overfull_boxes':re.findall(r'Overfull .*',log),'unresolved_references':False if not any('references' in x for x in bad) else True}
(P/'qa/document_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if bad:raise SystemExit(1)
