"""Regenerate the benchmark, verify numerical identity and run all acceptance tests."""
from pathlib import Path
import subprocess,sys,hashlib,json,re,datetime,csv
from PIL import Image
P=Path(__file__).resolve().parent
PROJECT=P.parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def main():
 numerical=[p for p in P.rglob('*.csv') if 'reviews' not in p.parts]
 numerical += [P/'analysis.json',P/'explicit_rollout.json',P/'flight/flight_summary.json',P/'wind/summary.json']
 before={str(p.relative_to(P)):sha(p) for p in numerical}
 runs=[]
 for rel in ['reconstruct.py','flight/build_flight.py','flight/build_approach.py','noaa/decode_noaa.py','wind/reconstruct_wind.py']:
  r=subprocess.run([sys.executable,'-B',str(P/rel)],text=True,capture_output=True)
  runs.append(dict(script=rel,exit_code=r.returncode))
  (P/'reviews'/('regenerate_'+rel.replace('/','_')+'.log')).write_text(r.stdout+r.stderr)
  if r.returncode:raise RuntimeError('Regeneration failed: '+rel+'\n'+r.stderr)
 after={name:sha(P/name) for name in before}
 changed=[k for k in before if before[k]!=after[k]]
 if changed:raise RuntimeError('Unexpected numerical regeneration changes: '+str(changed))
 suites=[]
 for folder,pattern in [('.', 'test_reconstruction.py'),('flight','test_flight.py'),('noaa','test_decode_noaa.py'),('wind','test_wind.py')]:
  cmd=[sys.executable,'-B','-m','unittest','discover','-s',str(P/folder),'-p',pattern,'-v']
  r=subprocess.run(cmd,text=True,capture_output=True);out=r.stdout+r.stderr
  (P/'reviews'/('tests_'+folder.replace('.','parent')+'.log')).write_text(out)
  m=re.search(r'Ran (\d+) tests?',out)
  suites.append(dict(suite=folder,test_count=int(m.group(1)) if m else None,exit_code=r.returncode,passed=r.returncode==0 and '\nOK' in out))
  if not suites[-1]['passed']:raise RuntimeError('Tests failed: '+folder+'\n'+out)
 checks={}
 counts={'rollout_pixel_anchors':len(rows(P/'rollout_trace.csv')),
         'final_phase_pixel_anchors':len(rows(P/'flight/flight_anchor_readings.csv')),
         'approach_pixel_anchors':len(rows(P/'flight/approach_anchor_readings.csv')),
         'wind_direction_speed_pairs':len(rows(P/'wind/wind_records.csv')),
         'year_weather_records':len(rows(P/'noaa/observations_1993.csv')),
         'event_day_weather_records':len(rows(P/'noaa/observations_1993-11-04.csv')),
         'source_stated_events':len(rows(P/'flight_events.csv')),
         'explicit_rollout_segments':len(json.loads((P/'explicit_rollout.json').read_text())['segments'])}
 checks['counts_match_extraction']=(counts=={'rollout_pixel_anchors':35,'final_phase_pixel_anchors':123,'approach_pixel_anchors':67,'wind_direction_speed_pairs':225,'year_weather_records':8549,'event_day_weather_records':24,'source_stated_events':18,'explicit_rollout_segments':34})
 cfg=json.loads((PROJECT/'approximation/reference_outcomes.json').read_text())['source_sha256']
 checks['frozen_model_unchanged']=all(sha(PROJECT/f)==cfg[f] for f in ['model/config.json','model/trajectory.py'])
 pngs=list(P.rglob('*.png'))
 for p in pngs:
  with Image.open(p) as im:im.verify()
 checks['all_pngs_decode']=True
 a=json.loads((P/'analysis.json').read_text())
 checks['no_physical_ci_or_clock_alignment']=a['uncertainty']['coverage_probability'] is None and a['uncertainty']['clock_offset_to_wind'] is None
 segs=json.loads((P/'explicit_rollout.json').read_text())['segments']
 checks['explicit_segments_continuous']=all(abs(b['x0_m']-a['x1_m'])<1e-9 and abs(b['v0_mps']-a['v1_mps'])<1e-9 and abs(b['start_elapsed_s']-a['start_elapsed_s']-a['duration_s'])<1e-9 for a,b in zip(segs,segs[1:]))
 report=(P/'REPORT.md').read_text()
 links=re.findall(r'\]\(([^)]+)\)',report)
 missing=[q for q in links if not q.startswith(('https:','http:')) and not (P/q.split('#')[0]).exists() and q!='verification.json']
 checks['report_deliverable_links_exist']=not missing
 checks['three_review_reports_present']=all((P/'reviews'/f).exists() for f in ['blind_review.md','edge_review.md','acceptance_review.md'])
 checks['numeric_regeneration_byte_identical']=not changed
 if not all(checks.values()):raise RuntimeError('Failed checks: '+str(checks))
 # Component check artifacts represent earlier runs; their timestamped verification
 # JSON may change on reproduction. Pin current final artifact identities below.
 files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='verification.json' and p.name!='delivery_manifest.json']
 hashes={str(p.relative_to(P)):sha(p) for p in sorted(files)}
 (P/'delivery_manifest.json').write_text(json.dumps({'scope':'current local benchmark artifacts; verification.json files excluded to avoid self-reference and component timestamps','sha256':hashes},indent=2)+'\n')
 verification=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
   status='selected reconstruction benchmark verified; wider historical optimal landing and physical CI remain incomplete',
   suites=suites,tests_run=sum(s['test_count'] for s in suites),tests_passed=sum(s['test_count'] for s in suites if s['passed']),
   regeneration=runs,numerical_files_reproduced=len(numerical),counts=counts,checks=checks,
   artifact_files_hashed=len(hashes),png_files_decoded=len(pngs),
   independent_review='three review lanes completed; defects repaired; acceptance no blocking findings; clock wording corrected',
   source_visual_review='parent Figure5 overlay and Appendix13 table; independent acceptance auditor Figures1/2/4/5 overlays and consequential wind source values',
   limits=['Selected chart readings, not recovered raw DFDR or full three-minute trace','Unknown physical sensor/model errors; digitization sensitivities not physical95%intervals','No precise flight/wind clock join','No terrain clearance or optimum certification','Not operational guidance'])
 (P/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
 print(json.dumps(verification,indent=2))
if __name__=='__main__':main()
