"""Read-only package checks; --seal explicitly writes only this additive package."""
from pathlib import Path
import sys,json,hashlib,re,platform
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_records(base,records):
 for name,v in records.items():
  p=base/name
  assert p.is_file() and p.stat().st_size==v['bytes'] and sha(p)==v['sha256'],str(p)
 return len(records)
def verify(seal=False):
 snapshot=json.loads((HERE/'preserved_snapshot.json').read_text());n=check_records(ROOT,snapshot)
 counts={}
 for label,base in [('refinement',HERE.parent),('parent',HERE.parent.parent)]:
  m=json.loads((base/'artifact_manifest.json').read_text());counts[label]=check_records(base,m['files'])
  assert sha(base/'artifact_manifest.json')==snapshot[str((base/'artifact_manifest.json').relative_to(ROOT))]['sha256']
 counts['prior']=check_records(ROOT,json.loads((ROOT/'integrated/aircraft_followup/prior_integrity.json').read_text()))
 frozen=json.loads((ROOT/'integrated/source_manifest.json').read_text())['files']
 for name,value in frozen.items():assert sha(ROOT/name)==value
 counts['frozen']=len(frozen)
 c=json.loads((HERE/'certificate.json').read_text());r=c['root'];p=c['path']
 assert r['certified']and r['strict_inclusion']and r['all_jacobians_nonsingular']and c['simplex']['certified']and p['certified']
 zones=c['event_attempts'][-1]['zones'];assert len(zones)==5 and all(z['certified']for z in zones)
 for ph in [0,1]:
  cells=sorted((a,b)for phase,a,b,*_ in p['cover']if phase==ph)
  assert cells[0][0]==0 and cells[-1][1]==1 and all(a[1]==b[0]for a,b in zip(cells,cells[1:]))
 for ph,a,b,d,omitted in p['cover']:
  for key in omitted:assert ph==1 and any(z['key']==key and a>=z['left']and b<=z['right']for z in zones)
 rr=json.loads((HERE/'retention_replay.json').read_text());assert rr['secondary_retention']['certified']and rr['root_center_replay']['passed']
 from decimal import Decimal,localcontext
 with localcontext()as ctx:
  ctx.prec=80
  assert Decimal(rr['secondary_retention']['eta_lower_real_decimal'])+Decimal('.0001')>=Decimal(r['center'][5])+Decimal(r['radius'])
  assert Decimal('0.15236076430186170190')<Decimal(r['center'][5])-Decimal(r['radius'])
 for name,value in rr['secondary_retention']['source_sha256'].items():assert sha(ROOT/name)==value
 logs=(HERE/'tests.log').read_text();assert '108 passed' in logs and 'FAILED' not in logs
 geo=(HERE/'geospatial_tests.log').read_text();assert 'Ran 16 tests' in geo and 'OK' in geo
 for name in ['REPORT.md','DERIVATION.md','TRACEABILITY.md','README.md']:
  text=(HERE/name).read_text()
  for target in re.findall(r'\]\(([^)]+)\)',text):
   if not target.startswith(('http:','https:','#')):assert (HERE/target).exists(),target
 if seal:
  import mpmath,numpy,scipy
  result=dict(verified_utc=datetime.now(timezone.utc).isoformat(),preserved_unique_paths=n,preserved_counts=counts,preserved_manifests=2,tests=dict(core_and_certificate=108,new_within_core=11,geospatial=16),root_existence_uniqueness=True,jacobian_nonsingularity=True,positive_active_simplex=True,active_time_extrema=True,all_time_approach_flare_stop=True,accepted_time_cells=len(p['cover']),processed_time_cells=p['processed'],strict_local_flare_primary=True,nonstrict_local_family_primary=True,unique_full_path=False,global_optimum=False,global_secondary=False,historical_certified=False,baseline_family_lower='0.15236076430186170190',inherited_family_upper='0.181970215',secondary_retention_budget='.0001',secondary_processed_cells=rr['secondary_retention']['processed'],root_center_replay=rr['root_center_replay'],unresolved_conditions=['tailwind5','urban60','urban65'],requirements={'implemented':5,'partial':2,'overall':'INCOMPLETE'},environment=dict(python=platform.python_version(),mpmath=mpmath.__version__,numpy=numpy.__version__,scipy=scipy.__version__,interval_decimal_digits=50),errors=[])
  (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
  records={}
  for path in sorted(HERE.rglob('*')):
   if path.is_file()and path.name!='artifact_manifest.json'and not any(x in path.parts for x in ['__pycache__','.pytest_cache']):records[str(path.relative_to(HERE))]={'bytes':path.stat().st_size,'sha256':sha(path)}
  m=dict(created_utc=datetime.now(timezone.utc).isoformat(),scope='local_certificate additive only; excludes itself and runtime caches',refinement_manifest_sha256=sha(HERE.parent/'artifact_manifest.json'),parent_manifest_sha256=sha(HERE.parent.parent/'artifact_manifest.json'),files=records)
  (HERE/'artifact_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 manifest=json.loads((HERE/'artifact_manifest.json').read_text());new=check_records(HERE,manifest['files'])
 print(json.dumps(dict(status='PASS',preserved_unique_paths=n,preserved_counts=counts,new_artifacts=new,manifest_sha256=sha(HERE/'artifact_manifest.json'))))
if __name__=='__main__':verify('--seal'in sys.argv)
