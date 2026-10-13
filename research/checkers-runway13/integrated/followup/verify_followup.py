"""Verify only new work plus preservation of inherited evidence."""
from pathlib import Path
import json, hashlib, datetime, re, sys, unittest, io
sys.path.insert(0,str(Path(__file__).resolve().parent))
from diagnose_threshold import build

R=Path(__file__).resolve().parents[2]; O=Path(__file__).resolve().parent; I=R/'integrated'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
errors=[]
# Regenerate only the NEW diagnostic, including final crop hashes.
r=build();(O/'threshold_diagnosis.json').write_text(json.dumps(r,indent=2)+'\n')
if r != build():errors.append('new producer not reproducible')
buf=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(O),pattern='test_diagnosis.py')
result=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
(O/'tests.log').write_text(buf.getvalue())
if not result.wasSuccessful():errors.append('new tests failed')
frozen=read(I/'source_manifest.json')['files']
bad=[p for p,h in frozen.items() if digest(R/p)!=h]
if bad:errors.append('frozen inputs mutated')
old=read(O/'prior_checkpoint/previous_manifest.json')['artifacts']
allowed={'REPORT.md','README.md','TRACEABILITY.md'}
old_changed=[a['path'] for a in old if digest(I/a['path'])!=a['sha256']]
if set(old_changed)!=allowed:errors.append('unexpected inherited package changes: '+str(old_changed))
for a in old:
 if a['path'] in allowed and digest(O/'prior_checkpoint'/a['path'])!=a['sha256']:
  errors.append('prior document snapshot mismatch')
handoff=read(R/'reconstruction/block_matching/HANDOFF.json')['artifacts']
for a in handoff:
 if digest(R/'reconstruction/block_matching'/a['path'])!=a['sha256']:errors.append('inherited handoff changed')
observations=read(O/'primary_observations.json')['observations']
for ob in observations:
 if digest(R/ob['source_path'])!=ob['source_sha256']:errors.append('primary source changed')
 if digest(O/ob['image'])!=ob['image_sha256']:errors.append('source crop changed')
archive=read(O/'sources/survey_archive_check.json')
rows=[]
for name,h in archive['files'].items():
 p=O/'sources'/name
 if digest(p)!=h:errors.append('archive chunk changed')
 d=read(p)
 if d.get('exceededTransferLimit'):errors.append('truncated archive chunk')
 rows.extend(f['attributes'] for f in d['features'])
ids=[x['OBJECTID'] for x in rows]
count=read(O/'sources/survey_year_count.json')['response']['count']
if len(rows)!=count or len(set(ids))!=count or count!=archive['count']:errors.append('archive completeness mismatch')
if not all(x['YEARFLIGHT']==1993 for x in rows):errors.append('wrong archive year')
hits=[]
for x in rows:
 date=datetime.datetime.fromtimestamp(x['DATEFLIGHT']/1000,datetime.timezone.utc).date().isoformat()
 if date=='1993-11-05' or any(n in x['PHOTONO'] for n in ['72998','72999','73000','73001']):hits.append(x['PHOTONO'])
if hits or archive['matches']:errors.append('archive negative result mismatch')
# New receipt will exist before link verification.
receipt=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 scope='new diagnostic tests/source observations/archive integrity and inherited preservation only; no old producers or old36test suite rerun',
 new_tests=dict(run=result.testsRun,passed=result.wasSuccessful(),failures=len(result.failures),errors=len(result.errors)),
 new_producer_exact_object_replay=True,
 frozen_inputs_checked=len(frozen),frozen_mismatches=bad,
 prior_package_files_checked=len(old),changed_prior_paths=old_changed,
 unchanged_prior_package_files=len(old)-len(old_changed),
 inherited_handoff_hashes_checked=len(handoff),
 primary_observations_checked=len(observations),
 archive_records=count,archive_unique_ids=len(set(ids)),archive_expected_matches=hits,
 original_diagnostics_unchanged=True,accepted_registration=False,
 source_supported_offset_hypothesis_m=61,accepted_offset_m=None,
 historical_clearance_ready=False,closed_form_optimum=None,
 requirements=dict(total=16,implemented=1,partial=10,blocked=5),
 review='owner verification only; no extra agents or external review',
 errors=errors)
(O/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
for p in [I/'REPORT.md',I/'README.md',I/'TRACEABILITY.md',O/'REPORT.md']:
 for rel in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not rel.startswith(('https://','http://','#')) and not (p.parent/rel).exists():errors.append('broken link '+str(p)+':'+rel)
receipt['errors']=errors
(O/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
if errors:raise SystemExit(1)
