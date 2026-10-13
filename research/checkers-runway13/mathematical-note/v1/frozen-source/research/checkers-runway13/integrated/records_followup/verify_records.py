"""Verify additive record research; never certify historical geometry."""
from pathlib import Path
from fractions import Fraction as F
import json, hashlib, re, datetime
P=Path(__file__).resolve().parent; I=P.parent; R=I.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,msg):
 if not x:raise RuntimeError(msg)
old=json.loads((I/'artifact_manifest.json').read_text())
bad=[a['path'] for a in old['artifacts'] if sha(I/a['path'])!=a['sha256'] or (I/a['path']).stat().st_size!=a['bytes']]
require(not bad,'prior package changed: '+str(bad))
frozen=json.loads((I/'source_manifest.json').read_text())['files']
require(all(sha(R/p)==h for p,h in frozen.items()),'frozen mismatch')
source_rows=[]
for f in ['retrieval.json','disclosure_retrieval.json','catalogue_search.json','targeted_search.json','targeted_expanded.json','catalogue_details.json','structure_details.json','survey_plan_details.json']:
 rows=json.loads((P/'sources'/f).read_text())
 for a in rows:
  name=a.get('file') or (a.get('id','')+'.html')
  require('error' not in a, 'retrieval failure: '+str(a))
  require(sha(P/'sources'/name)==a['sha256'],'source mismatch '+name)
  source_rows.append({'file':'sources/'+name,'url':a.get('final_url',a['url']),'sha256':a['sha256'],'category':'official administrative/catalogue metadata, not accepted historical geometry','redistribution':'not established; local research copy'})
records=[]
for f in ['catalogue_details.json','structure_details.json','survey_plan_details.json']:
 for a in json.loads((P/'sources'/f).read_text()):
  require(a['id'] in a['text'],'wrong record identity')
  records.append({'record_id':a['id'],'url':a['final_url'],'source_file':'sources/'+a['id']+'.html','sha256':a['sha256'],'record_contents_obtained':False,'numerical_geometry_accepted':False})
require(len(records)==14,'unexpected record count')
for filename,recipient in [('LANDS_ENQUIRY_DRAFT.md','landsd@landsd.gov.hk'),('CAD_ENQUIRY_DRAFT.md','enquiry@cad.gov.hk')]:
 s=(P/filename).read_text(); require('NOT SENT' in s and recipient in s and '115-93 A' in s and '404 Part II' in s and 'charge' in s,'draft incomplete')
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if not link.startswith('http'):require((P/link).is_file(),'missing draft source '+link)
require('mailto:landsd@landsd.gov.hk' in (P/'sources/lands_access.html').read_text(),'Lands recipient not source verified')
require('mailto:enquiry@cad.gov.hk' in (P/'sources/cad_contacts.html').read_text(),'CAD recipient not source verified')
# Exact arithmetic checks of stated prerequisite identities, not uncertainty calibration.
checks=0
for hi,hr,c in [(F(100),F(4),F(3,2)),(F(-2),F(7),F(-100)),(F(1,3),F(2,7),F(1000))]:
 require((hi+c)-(hr+c)==hi-hr,'translation invariance');checks+=1
# Independent source bounds subtract; all four interval corners enclosed.
l,u,lr,ur=F(20),F(21),F(3),F(5)
for a in [l,u]:
 for b in [lr,ur]:require(l-ur<=a-b<=u-lr,'relative interval corner');checks+=1
# Removing vertical zero does not remove tilt or scale.
z1,z0,e1,e0=F(2),F(1),F(100),F(0)
require(F(2)*(z1-z0)+F(1,100)*(e1-e0)!=z1-z0,'scale/tilt noncancellation');checks+=1
logs={'integration_tests.log':20,'frame_gate_tests.log':10,'source_geometry_tests.log':6,'diagnostic_tests.log':7}
for name,n in logs.items():
 s=(P/name).read_text(); require(f'Ran {n} tests' in s and s.rstrip().endswith('OK'),'tests failed '+name)
require(len(re.findall(r'^\| (?:INT|GEO|AIR|OPT|UNC|VAL|OUT)-\d\d \|', (I/'TRACEABILITY.md').read_text(),re.M))==16,'audit missing row')
status=json.loads((I/'integration_status.json').read_text());require(status['historical_integration_acceptance'] is False and status['historical_optimum'] is None,'historical gate changed')
inv={'retrievals':source_rows,'catalogue_records':records,'physical_historical_geometry_added':0,'private_exclusions':['LANDS_ENQUIRY_DRAFT.md','CAD_ENQUIRY_DRAFT.md'],'third_party_sources':'local only pending independent redistribution-rights check'}
(P/'source_inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
receipt={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_package_checked':len(old['artifacts']),'prior_package_mismatches':bad,'frozen_inputs_checked':len(frozen),'source_retrieval_hashes_checked':len(source_rows),'catalogue_detail_records_checked':len(records),'existing_tests_passed':sum(logs.values()),'exact_rational_prerequisite_checks':checks,'historical_geometry_added':0,'historical_clearance_ready':False,'closed_form_optimum':None,'requirements':{'total':16,'implemented':1,'partial':10,'blocked':5},'outreach_sent':False,'publication_performed':False,'review':'owner verification, no independent reviewer','errors':[]}
(P/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
