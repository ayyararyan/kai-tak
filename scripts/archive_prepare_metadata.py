#!/usr/bin/env python3
"""Refresh derived local review metadata. Does not grant licenses or publish."""
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'archive'
def read(p): return json.loads(p.read_text())
def write(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def main():
 m=read(A/'releases/v1.0.0/manifest.json')
 if m['status']!='candidate': raise SystemExit('Refusing to change published release metadata')
 assets=m['assets']
 if any(x['bytes']<=0 or x['sha256']=='0'*64 for x in assets):raise SystemExit('Build candidate before preparing metadata')
 (A/'releases/v1.0.0/SHA256SUMS').write_text(''.join(f"{x['sha256']}  {x['name']}\n" for x in assets))
 z=read(A/'preservation/zenodo-version-draft.json');z['proposed_files']=[dict(name=x['name'],sha256=x['sha256'],bytes=x['bytes'],treatment='eligible-source-data; attach full source-specific conditions') for x in assets];z['additional_files_requiring_review']=['kai-tak-archive-v1.0.0-review-support.tar.gz (original-work grants and attribution pending)', 'Exact source commit: local Git bundle is private preservation only; mixed-rights source history is not a proposed Zenodo upload'];write(A/'preservation/zenodo-version-draft.json',z)
 graph=[]
 for d in read(A/'catalogue/datasets.json')['datasets']:
  graph.append({'@type':'Dataset','@id':'urn:kai-tak:dataset:'+d['id'],'name':d['title'],'description':d['description'],'identifier':d['id'],'version':'1.0.0-candidate','creator':[{'@type':'Person' if 'Aryan' in c else 'Organization','name':c} for c in d.get('creator',[]) if c and 'unresolved' not in c.lower()], 'contributor':{'@type':'Person','name':'Aryan Ayyar','description':'Archive researcher and curator; not necessarily original source creator'},'isBasedOn':d.get('source_links',[]),'citation':d['citation'],'conditionsOfAccess':'Unpublished candidate; per-artifact/source rights apply. No blanket license.'})
 write(A/'preservation/schemaorg-datasets.jsonld',{'@context':'https://schema.org','@graph':graph})
 rights=read(A/'licensing/rights_registry.json')['records']
 fields=['id','title','publication_decision','scope','required_attribution','verification_date','official_terms_urls']
 with (A/'licensing/rights_matrix.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows([{k:json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rights])
 # New archive files and frozen original-work candidates remain proposals, not grants.
 proposed={}
 for x in read(A/'catalogue/artifacts.json')['artifacts']:
  if x['publication_decision']=='Original authored material':proposed[x['path']]={'path':x['path'],'sha256':x['sha256'],'candidate_license':'MIT' if x['path'].endswith('.py') else 'CC-BY-4.0','approved':False,'authorship':'Proposed; copied portions, upstream restrictions and contributors require confirmation.'}
 for p in sorted([ROOT/'README.md',ROOT/'CITATION.cff',*ROOT.glob('scripts/archive_*.py'),ROOT/'scripts/fetch_data.py',*ROOT.glob('tests/*.py'),*A.glob('*.md'),*A.glob('collections/*/README.md')]):
  rel=p.relative_to(ROOT).as_posix();proposed[rel]={'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'candidate_license':'MIT' if p.suffix=='.py' else 'CC-BY-4.0','approved':False,'authorship':'Archive curation prepared for Aryan Ayyar; human approval required. No upstream work relicensed.'}
 write(A/'licensing/proposed_scope.json',{'status':'DRAFT-NOT-A-GRANT','files':list(proposed.values()),'excluded':'All third-party expression, supplied photograph, mixed-rights figures and unknown authorship remain outside a new grant. Exact final source commit is also required before approval.'})
 print(json.dumps({'status':'prepared-no-grant','assets':len(assets),'datasets':len(graph),'proposed_original_files':len(proposed)}))
if __name__=='__main__': main()
