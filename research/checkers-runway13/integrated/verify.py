"""Reproducible correctness/blocked-path receipt; never full scientific acceptance."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess,unittest,io,platform,importlib.metadata,re
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];O=R/'integrated';sys.path.insert(0,str(O))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
errors=[];log=[]
frozen=read(O/'source_manifest.json')['files'];frozen_bad=[p for p,h in frozen.items() if digest(R/p)!=h]
if frozen_bad:errors.append('frozen input changed')
handoff=read(R/'reconstruction/block_matching/HANDOFF.json')['artifacts'];bad=[]
for a in handoff:
 p=R/'reconstruction/block_matching'/a['path']
 if p.stat().st_size!=a['bytes'] or digest(p)!=a['sha256']:bad.append(a['path'])
if bad:errors.append('inherited artifact changed')
files=['geometry/historical_seawall.geojson','geometry/historical_approach_lights.geojson','geometry/historical_hill_terrain.geojson','geometry/mapped_runway_edges.geojson','geometry/integrated_evidence.geojson','geometry/runway_registration_diagnostic.json','geometry/south_registration_diagnostic.json','geometry/runway_crosscheck.json','geometry/printed_grid_check.json','geometry/mapped_runway_axis_check.json','geometry/airframe_envelope.json','registration.json','conditions.json','source_observations.json']
before={p:digest(O/p) for p in files}
for name in ['register_runway.py','register_south.py','check_runway_registration.py','check_printed_grid.py','check_mapped_axis.py','derive_mapped_runway.py','digitize_coast.py','digitize_hill.py','build_airframe.py','build_source_ledger.py','build_scene.py']:
 r=subprocess.run([sys.executable,str(O/name)],cwd=R,capture_output=True,text=True,timeout=120);log.append(name+'\n'+r.stdout+r.stderr)
 if r.returncode:errors.append('rebuild failed: '+name)
(O/'build_replay.log').write_text('\n'.join(log))
changed=[p for p,h in before.items() if digest(O/p)!=h]
if changed:errors.append('deterministic outputs changed: '+str(changed))
buf=io.StringIO();suite=unittest.defaultTestLoader.discover(str(O),pattern='test_*.py');result=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite);(O/'tests.log').write_text(buf.getvalue())
if not result.wasSuccessful():errors.append('tests failed')
r=subprocess.run([sys.executable,str(O/'evaluate.py'),'--output',str(O/'evaluation.json')],cwd=R,capture_output=True,text=True,timeout=30)
try:gate=json.loads(r.stdout)
except Exception:gate={};errors.append('evaluator invalidJSON')
blocked_ok=(r.returncode==2 and gate.get('overall')=='INCOMPLETE' and gate.get('closed_form_optimum') is None and gate.get('historical_condition_cells_certified')==0)
if not blocked_ok:errors.append('historical gate refusal failed')
scene=read(O/'geometry/integrated_evidence.geojson')['features'];primary=read(O/'primary_source_manifest.json')['sources']
inspection=read(O/'inspection_receipt.json')['items'];inspection_bad=[a['path'] for a in inspection if digest(O/a['path'])!=a['sha256']]
if inspection_bad:errors.append('inspected image changed: '+str(inspection_bad))
for a in primary:
 if digest(R/a['path'])!=a['sha256']:errors.append('primarysource changed: '+a['id'])
links=[]
# Source-backed overview must not contain an allblack rendering in the known tile.
image=Image.open(O/'geometry/runway_map_mosaic.png').convert('L');tile=np.asarray(image)[10:280,385:735];tile_check={'mean':float(tile.mean()),'std':float(tile.std()),'all_black':bool(np.all(tile==0))}
if tile_check['all_black'] or tile_check['std']<.1:errors.append('overview rendering regression')
# Frozen inputs checked again after every producer/replay.
if any(digest(R/p)!=h for p,h in frozen.items()):errors.append('baseline mutated during replay')
ver={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verification_scope':'implemented correctness,sourceintegrity,rebuild and expectedblockedgate; NOT scientificcompletion','correctness':{'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful()},'rebuild':{'producers_run':11,'deterministic_outputs_compared':len(files),'unexpected_output_changes':changed},'integrity':{'frozen_inputs_checked':len(frozen),'frozen_mismatches':frozen_bad,'inherited_handoff_artifacts_checked':len(handoff),'inherited_mismatches':bad,'primary_documents_checked':len(primary),'inspected_images_checked':len(inspection),'inspected_image_mismatches':inspection_bad},'scene_features':len(scene),'source_observations':len(read(O/'source_observations.json')['observations']),'new_accepted_complete_historical_obstacle_volumes':0,'new_hard_height_bounds':0,'overview_halftone_tile_check':tile_check,'local_broken_links':links,'end_to_end':{'blocked_path_verified':blocked_ok,'historical_clearance_accepted':False,'condition_to_closed_form_optimum_implemented':False,'global_optimality_proof':False},'specification':{'required':16,'Implemented':1,'Partially implemented':10,'Blocked':5,'unapproved_scope_reductions':0,'unapproved_proxy_substitutions':0,'overall':'INCOMPLETE'},'errors':errors,'review':'ownerverificationonly; no independent external reviewer','runtime':{'python':sys.version,'platform':platform.platform(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','scipy','matplotlib','rasterio','pyproj','shapely','pillow']},'isolated_packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions(path=[str(O/'python_deps')])}}}
(O/'verification.json').write_text(json.dumps(ver,indent=2)+'\n')
# Check local links after creating the receipt, including links to this receipt.
for p in O.glob('*.md'):
 for rel in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not rel.startswith(('https://','http://','#')) and not (p.parent/rel).exists():links.append(str(p.relative_to(O))+':'+rel)
if links:errors.append('broken local links: '+str(links))
ver['local_broken_links']=links;ver['errors']=errors
(O/'verification.json').write_text(json.dumps(ver,indent=2)+'\n')
# Manifest includes receipt and scripts; excludes itself, dependencies and ephemeralbytecode.
artifacts=[]
for p in sorted(O.rglob('*')):
 if not p.is_file() or any(x in p.parts for x in ['python_deps','__pycache__']) or p.name=='artifact_manifest.json':continue
 artifacts.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':digest(p)})
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':'integrated/','scope':'localresearchpackage; thirdpartysourcesnotapprovedforpublication','artifacts':artifacts,'excludes':['python_deps (versions inverification.json)','__pycache__','artifact_manifest.json itself']};(O/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if any(digest(O/a['path'])!=a['sha256'] for a in artifacts):raise RuntimeError('manifest immediateverificationfailed')
print(json.dumps({'tests':result.testsRun,'tests_passed':result.wasSuccessful(),'rebuild_outputs':len(files),'manifest_files':len(artifacts),'baseline_files':len(frozen),'inherited_hashes':len(handoff),'errors':errors,'full_goal':'INCOMPLETE','blocked_path_verified':blocked_ok},indent=2));raise SystemExit(1 if errors else 0)
