#!/usr/bin/env python3
"""Check paper-specific numerical direction, labels and source bindings."""
from pathlib import Path
import hashlib,json,re
from decimal import Decimal,localcontext,ROUND_FLOOR
P=Path(__file__).resolve().parents[1]
checks=[]
def check(name,value):
    if not value:raise AssertionError(name)
    checks.append(name)
c=json.loads((P/'inputs/local_certificate.json').read_text());r=c['root'];s=c['simplex'];path=c['path']
check('root accepted',r['certified'] and r['strict_inclusion'] and r['all_jacobians_nonsingular'])
check('source slew signs, correcting sealed prose',r['slew_signs']==[-1,1,1])
check('root radius',r['radius']=='1e-20')
with localcontext() as ctx:
    ctx.prec=90
    eta=Decimal(r['center'][5]);rad=Decimal(r['radius'])
    check('family lower endpoint is rounded down',Decimal('0.15236076430186170190')<eta-rad)
    retention=eta+rad-Decimal('.0001')
    check('secondary threshold matches exact upper comparison',str(retention) in (P/'sections/conditional.tex').read_text())
    for bounds in s['multiplier_enclosures']:
        lower=Decimal(bounds[0].split(',')[0].lstrip('['))
        check('positive multiplier '+str(len(checks)),lower>0)
cover=path['cover'];check('398 accepted cells',len(cover)==398);check('786 processed cells',path['processed']==786)
for ph,n in [(0,32),(1,366)]:
    cells=[x for x in cover if x[0]==ph];check(f'phase {ph} count',len(cells)==n)
    check(f'phase {ph} gap-free cover',cells[0][1]==0 and cells[-1][2]==1 and all(a[2]==b[1] for a,b in zip(cells,cells[1:])))
texfiles=[P/'main.tex',P/'abstract.tex',P/'appendices.tex',*sorted((P/'sections').glob('*.tex')),P/'root_table.tex',P/'condition_table.tex',P/'wind_table.tex',P/'approach_table.tex']
text='\n'.join(f.read_text() for f in texfiles)
labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
check('unique labels',len(labels)==len(set(labels)));check('every source reference has a label',not(set(refs)-set(labels)))
check('four named central theorems',text.count('\\begin{theorem}')==4)
check('each formal result has a proof',sum(text.count('\\begin{'+n+'}') for n in ['theorem','lemma','proposition','corollary'])==text.count('\\begin{proof}'))
for val in r['center']:check('exact root centre '+str(len(checks)),val in (P/'root_table.tex').read_text())
bib=(P/'references.bib').read_text();keys=set(re.findall(r'@\w+\{([^,]+),',bib));cites=set(k.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}',text) for k in group.split(','))
check('all citations have bibliography entries',cites<=keys)
vs=P/'frozen-source/research/checkers-runway13/whitepaper/v5'
# V5 format source hashes are recorded separately; no hidden fallback font/template.
if (P/'FORMAT_SOURCE_MANIFEST.json').exists():
    for record in json.loads((P/'FORMAT_SOURCE_MANIFEST.json').read_text())['files']:
        check('byte-identical V5 '+record['path'],hashlib.sha256((P/record['path']).read_bytes()).hexdigest()==record['sha256'])
rows=json.loads((P/'verification/condition-values.json').read_text());check('ten accepted conditions',len(rows)==10 and len({r['name'] for r in rows})==10)
for row in rows:
    down=Decimal(row['eta_certified']).quantize(Decimal('.000001'),rounding=ROUND_FLOOR)
    check('downward condition value '+row['name'],str(down) in (P/'condition_table.tex').read_text())
result={'passed':len(checks),'checks':checks,'note':'Consistency checks, not substitutes for the independently reviewed theorem proofs.'}
(P/'qa').mkdir(exist_ok=True);(P/'qa/content-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
