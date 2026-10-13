#!/usr/bin/env python3
"""Acceptance checks on real source coordinates, rendered outputs and gallery references."""
from pathlib import Path
import json,hashlib,struct,re,datetime
import numpy as np
from PIL import Image
from shapely.geometry import shape,Polygon
A=Path(__file__).resolve().parents[1];ROOT=A.parents[1];R=ROOT/'research/checkers-runway13';checks=[]
def load(p):return json.loads(p.read_text())
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def check(name,condition,detail=None):
 checks.append(dict(name=name,passed=bool(condition),detail=detail));assert condition,name
s=load(R/'reconstruction/block_matching/scene/scene.json');manifest=load(A/'metadata/input_manifest.json')
check('All declared input hashes current',all(sha(ROOT/f['path'])==f['sha256'] for f in manifest['files'] if f['available']),len(manifest['files']))
receipt=load(A/'metadata/restore_receipt.json');check('Archive restore actual receipt',receipt['archive_count']==5 and receipt['member_count']==1254 and receipt['output'].count('Restored')==5)
v=np.array(s['observed_mesh']['vertices']);f=np.array(s['observed_mesh']['faces'])[:,:3]
check('Authoritative mesh counts',v.shape[0]==155891 and f.shape[0]==225371)
check('No historical invented heights',all(g['height_m'] is None and g['physical_volume'] is None for g in s['historical_faces']))
check('Stereo relative vertical datum',s['observed_mesh']['vertical_datum']=='relative_ground_plane' and not s['observed_mesh']['watertight'])
# Independently decode GLB positions and indices; verify existing Y-up mapping numerically.
with (R/'reconstruction/block_matching/aerial_registration/observed_surface_mesh.glb').open('rb') as stream:
 magic,version,total=struct.unpack('<III',stream.read(12));n,t=struct.unpack('<II',stream.read(8));glb=json.loads(stream.read(n));n,t=struct.unpack('<II',stream.read(8));data=stream.read(n)
acc=glb['accessors'][0];bv=glb['bufferViews'][acc['bufferView']];pos=np.frombuffer(data,dtype='<f4',count=acc['count']*3,offset=bv.get('byteOffset',0)).reshape(-1,3)
restored=np.c_[pos[:,0]+100,-pos[:,2]+200,pos[:,1]]
err=float(np.max(np.abs(restored-v[:,:3])));check('GLB Y-up mapping independently compared to all original vertices',err<.0002,{'maximum_difference_m':err,'vertices':len(v)})
acc=glb['accessors'][3];bv=glb['bufferViews'][acc['bufferView']];idx=np.frombuffer(data,dtype='<u4',count=acc['count'],offset=bv['byteOffset']).reshape(-1,3);check('GLB original triangle order preserved',np.array_equal(idx,f))
roof=load(A/'assets/modern_roofs.json');area_error=0;holes=0
for g in s['modern']['features']:
 p=shape(g['geometry']);tri=roof[g['id']];area=sum(Polygon(t).area for t in tri);area_error=max(area_error,abs(area-p.area));holes+=len(p.interiors)
check('Modern courtyard-safe roof area conservation',area_error<1e-5,{'max_area_error_m2':area_error,'interior_rings':holes})
wide=load(A/'assets/modern_airport_scene.json')['modern'];check('Wide modern component/omission accounting',len(wide['features'])==3546 and len(wide['omitted'])==167)
check('Modern elevations valid and never transferred',all(g['top_hkpd_m']>=g['base_hkpd_m'] and not g['height_transfer_to_historical'] for g in wide['features']))
J=load(A/'metadata/render_jobs.json');records={}
for j in J:
 p=Path(j['output']);r=load(p.with_suffix('.render.json'));records[j['id']]=r
 check('4K render and output hash: '+j['id'],Image.open(p).size==(3840,2160) and sha(p)==r['output_sha256'])
 check('Current pinned renderer inputs: '+j['id'],all(sha(Path(p))==h for p,h in r['source_sha256'].items()))
 check('Saved editable Blender scene: '+j['id'],Path(j['save_blend']).exists() and Path(j['save_blend']).stat().st_size>1000)
 check('Nonphysical support and no exaggeration: '+j['id'],not r['display_board']['is_terrain'] and r['vertical_exaggeration']==1)
for a,b in [('03-city-beneath','map-1989-10'),('map-1989-10','map-1994-07'),('map-1989-10','map-1997-04'),('01-grand-overview','10-modern-airport'),('08-november-surface','08-surface-daylight'),('11-surface-top','11-map-top')]:
 check('Matched actual camera: '+a+' / '+b,records[a]['camera']==records[b]['camera'])
check('Full source preserved in hero',records['08-november-surface']['source_counts']['triangles']==225371)
inside=(v[:,0]>=0)&(v[:,0]<=750)&(v[:,1]>=0)&(v[:,1]<=600);nf=int(np.all(inside[f],axis=1).sum())
check('Core subset keeps only original supported triangles',records['03-city-beneath']['source_counts']['triangles']==nf,{'retained_triangles':nf})
check('Distinct vertical datums',records['03-city-beneath']['vertical_datum']=='relative_ground_plane' and records['10-modern-core']['vertical_datum']=='HKPD')
mi=load(R/'integrated/geometry/map_mosaic_manifest.json');years=sorted(t['edition_date'][:4] for t in mi['sources'])
check('All mosaic source epochs included',years[0]=='1986' and years[-1]=='1993' and all('1986' in records[n]['epoch'] for n in ['01-grand-overview','02-runway-water','06-final-alignment']))
# Runway grid bearing from actual documented vector, not magnetic heading.
edges=load(R/'integrated/geometry/mapped_runway_edges.geojson')['features'];en=np.array(edges[0]['properties']['EN_m']);delta=en[-1]-en[0];bearing=float(np.degrees(np.arctan2(delta[0],delta[1]))%180)
check('Runway line grid bearing',abs(bearing-134.02)<.1,{'grid_bearing_deg':bearing,'not_magnetic':True})
G=load(A/'metadata/gallery.json');check('Twelve subjects accounted',len(G)==12 and [g['id'] for g in G]==[f'{n:02}' for n in range(1,13)])
for g in G:
 for field in ['annotated','master']:
  im=Image.open(A/g[field]);check('Finished PNG semantics '+g['id']+' '+field,im.size==(3840,2160) and im.info.get('epoch')==g['epoch'] and im.info.get('type')==g['type'])
 check('Web preview/caption record '+g['id'],(A/g['web']).exists() and (A/g['web']).with_suffix('.json').exists())
 check('Print metadata '+g['id'],Image.open(A/f'renders/print/{g["id"]}-A4.png').info.get('epoch')==g['epoch'])
 check('Local source links '+g['id'],all((R/p).exists() for p in g['sources']))
 if 'evidence_variant' in g:
  ev=g['evidence_variant'];im=Image.open(A/ev['master']);check('Evidence-mode master consistency '+g['id'],ev['master']!=g['master'] and im.info['mode']=='evidence' and im.info['epoch']==ev['epoch'])
for name in ['12-square.png','12-vertical.png']:
 im=Image.open(A/'renders/crops'/name);check('Crop semantics '+name,im.info['mode']=='evidence' and im.info['epoch']=='Photographs: 2 November 1993' and 'No airport map inset' in im.info['caption'])
page=(A/'gallery/index.html').read_text();static=[h for h in re.findall(r'href="([^"]+)"',page) if '$' not in h and not h.startswith(('http','#'))]
check('Static gallery links resolve',all((A/'gallery'/h).exists() for h in static),static)
check('Gallery no external runtime dependencies','<script src=' not in page and '@import' not in page)
report={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':len(checks),'failed':0,'checks':checks,'browser_interaction':'unverified: OpenClaw file protocol unsupported and localhost navigation explicitly blocked by policy; no bypass attempted'}
(A/'qa/acceptance.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks),'acceptance checks')
