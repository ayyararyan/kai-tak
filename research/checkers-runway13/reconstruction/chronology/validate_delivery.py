"""Final content, provenance, timing and count checks for the local handoff."""
from pathlib import Path
import csv,datetime,hashlib,json,subprocess,sys,zipfile
from PIL import Image
R=Path(__file__).resolve().parent
checks=[]
def check(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readcsv(p):
 with p.open() as f:return list(csv.DictReader(f))
archives=json.loads((R/'sheets/map_downloads.json').read_text())
check(len(archives)==227,'227 selected map editions')
for a in archives:
 p=R/'sheets'/a['file'];check(a['status']=='validated_zip' and sha(p)==a['sha256'],'map hash '+a['source_id'])
 with zipfile.ZipFile(p) as z:check(z.testzip() is None,'map CRC '+a['source_id'])
index=readcsv(R/'sheets/all_hk_sheet_index.csv');check(len(index)==72691 and len({x['source_id'] for x in index})==72691,'complete unique sheet index')
source_receipts=list((R/'sheets/raw').glob('*.source.json'))
for p in source_receipts:
 meta=json.loads(p.read_text());source=p.with_name(p.name.removesuffix('.source.json'));check(sha(source)==meta['sha256'],'sheet index response hash '+source.name)
for name,expected in [('fullframe_manifest.json',48),('preview_manifest.json',47)]:
 images=json.loads((R/'aerial'/name).read_text());check(len(images)==expected,name+' count')
 for a in images:
  p=R/'aerial'/a['path'];check(sha(p)==a['sha256'],'aerial hash '+a['path'])
  with Image.open(p) as im:im.load();check(im.size==(a['width'],a['height']),'aerial decode '+a['path'])
sm=json.loads((R/'structures/manifest.json').read_text())
for a in sm['files']:check(sha(R/'structures'/a['path'])==a['sha256'],'structure hash '+a['path'])
obs=readcsv(R/'historical_visual_observations.csv');check(len(obs)==52 and len({x['historical_object_id'] for x in obs})==17,'52 visual observations for 17 objects/sites')
for o in obs:check((R/o['source_asset']).is_file(),'observation asset '+o['source_id'])
check({'HKMS:A23632','HKMS:CN4581','HKMS:A36143'} <= {o['source_id'] for o in obs},'all inspected aerial transitions integrated')
rows=readcsv(R/'structure_source_matches_1993-11-04.csv');check(len(rows)==69915 and len({x['building_csuid'] for x in rows})==69915,'unique complete local matches')
check(all(x['content_match_status']=='not_visually_verified' for x in rows),'coverage not content match')
check(all(not x['sheet_before_edition_month'] or x['sheet_before_edition_month']<'1993-11' for x in rows),'November month not counted before November 4')
pairs=readcsv(R/'sheet_photo_pairs_1993.csv');check(len(pairs)==16968,'16968 coverage pairs')
check(all(float(x['overlap_m2'])>0 and 0<float(x['fraction_sheet_covered'])<=1.000001 and 0<float(x['fraction_frame_covered'])<=1.000001 for x in pairs),'strictly positive overlap fractions retained')
check(all(x['match_kind']=='index_polygon_overlap_only' for x in pairs),'pair semantics preserved')
check(len({x['sheet_id'] for x in pairs})==227,'all selected maps paired')
handoff=json.loads((R/'HANDOFF.json').read_text())
for k,a in handoff['artifacts'].items():check(sha(R/a['path_relative_to_handoff'])==a['sha256'],'handoff hash '+k)
check(handoff['clearance_certified'] is False and handoff['uncertainty']['historical_obstacle_height_intervals'] is None,'no fabricated historical clearance')
test_results=[]
for sub,pattern,expected in [('structures','test_*.py',39),('','test_matching.py',7)]:
 p=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(R/sub),'-p',pattern],capture_output=True,text=True)
 check(p.returncode==0 and f'Ran {expected} tests' in p.stderr,'test suite '+str(expected));test_results.append({'directory':sub or '.','tests':expected,'passed':p.returncode==0,'output':p.stderr})
result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks_passed':len(checks),'checks':checks,'tests':test_results,'map_archives':227,'full_aerial_frames':48,'aerial_previews':47,'structure_manifest_files_checked':len(sm['files']),'sheet_index_response_hashes_checked':len(source_receipts),'current_features_classified':342195,'local_features_classified':69915,'visual_observations':52,'visual_objects_or_sites':17,'historical_reconstruction_complete':False,'historical_geometries_verified':0,'clearance_certified':False}
(R/'validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','tests']},indent=2))
