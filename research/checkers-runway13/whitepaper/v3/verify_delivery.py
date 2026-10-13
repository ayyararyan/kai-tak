"""Final package acceptance, distinct from scientific proof and visual review."""
from pathlib import Path
import json,csv,re,hashlib,zipfile,datetime
from itertools import zip_longest
P=Path(__file__).resolve().parent
required=['main.tex','appendices.tex','coefficients.tex','references.bib','README.md','SPEC.md','REQUIREMENTS_TRACEABILITY.md','CLAIMS_AND_EVIDENCE.csv','INSIGHTS.md','VERIFICATION.md','RIGHTS_AND_PROVENANCE.md','CITATION_VERIFICATION.md','VERSION_CHANGES.md','abstract.md','executive-summary.md','build.py','make_figures.py','verify_v2_inputs.py','verify_v3_claims.py','verify_certificates.py','check_pdf.py','requirements.txt','SOURCE_MANIFEST.json','evidence_manifest.json','checkers-with-runway-13-white-paper-v3.pdf']
for f in required:
 if not (P/f).is_file() or not(P/f).stat().st_size:raise RuntimeError(f)
rows=list(csv.DictReader((P/'CLAIMS_AND_EVIDENCE.csv').open()));assert len(rows)==51
for r in rows:
 for f in r['supporting_files'].split(';'):assert (P/f).is_file(),(r['claim_id'],f)
tex='\n'.join(f.read_text() for f in [P/'main.tex',P/'appendices.tex',*sorted((P/'sections').glob('*.tex'))])
cited=set()
for x in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cited.update(x.split(','))
keys=set(re.findall(r'@\w+\{([^,]+),',(P/'references.bib').read_text()))
assert cited==keys and len(keys)==14,(cited,keys)
co=(P/'coefficients.tex').read_text();printed=[]
for line in co.splitlines():
 if re.match(r'^\d+ & ',line):printed.append([float(x.strip().rstrip('\\')) for x in line.split('&')[1:]])
expected=[];durations=[]
for source in ['evidence/approximation/reference_formula.json','evidence/counterfactual/formula.json']:
 for phase in json.loads((P/source).read_text())['phases']:
  expected.extend(zip_longest(*phase['coefficients_xyz_m'],fillvalue=0.0));durations.append(phase['duration_s'])
assert len(printed)==len(expected)
for a,b in zip(printed,expected):assert all(abs(x-y)<=5.01e-10 for x,y in zip(a,b)),(a,b)
for d in durations:assert f'{d:.10f}' in co
checks=json.loads((P/'qa/document_checks.json').read_text());visual=json.loads((P/'qa/visual_inspection.json').read_text());clean=json.loads((P/'qa/clean_rebuild.json').read_text())
sha=hashlib.sha256((P/'checkers-with-runway-13-white-paper-v3.pdf').read_bytes()).hexdigest()
assert checks['pdf_sha256']==visual['pdf_sha256']==clean['original_sha256']==sha
assert visual['pages_reviewed']==list(range(1,34))
assert all(r['text_identical'] and r['render_identical'] for r in clean['page_results'])
for scenario in ['calm','wind']:
 for pre in ['fresh','clean']:
  r=json.loads((P/f'qa/{pre}_{scenario}_certificate.json').read_text());assert r['fresh_proof']['certified'] and r['exact_cover_matches_saved']
assert len(list((P/'figures').glob('*.pdf')))==16
receipt={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'required_deliverables_present':len(required),'claim_sources_resolve':51,'bibliography_entries_cited':14,'printed_coefficient_rows_checked':len(printed),'printed_phase_durations_checked':4,'final_document_receipts_bound_to_pdf':True,'clean_rebuild_text_and_pixels_identical':True,'both_scenario_certificates_pass_original_and_clean':True,'pdf_sha256':sha}
(P/'qa/delivery_acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
