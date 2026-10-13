from pathlib import Path
import json
A=Path(__file__).resolve().parents[1];(A/'scenes/jobs').mkdir(exist_ok=True)
def cam(loc,target,scale=None,lens=48):
 return dict(location=loc,target=target,projection='ORTHO' if scale else 'PERSP',ortho_scale=scale or 1500,lens=lens)
core=cam([1100,-1050,1100],[375,300,20],1300)
wide=cam([5200,-5500,5700],[1500,-1200,0],6900)
mosaic=json.loads((A.parents[1]/'research/checkers-runway13/integrated/geometry/map_mosaic_manifest.json').read_text());dates=sorted(s['edition_date'] for s in mosaic['sources']);assert dates[0][:4]=='1986' and dates[-1][:4]=='1993'
J=[]
def job(id,kind,epoch,camera,**kw):
 d=dict(id=id,kind=kind,epoch=epoch,style='architectural',lighting='daylight',mode='evidence',camera=camera,width=3840,height=2160,samples=48,output=str(A/f'renders/master/{id}.png'),save_blend=str(A/f'scenes/{id}.blend'));d.update(kw);J.append(d)
# Required priority: direct photo surface first, then current comparison, maps, broad geography.
job('08-november-surface','stereo','1993-11-02',cam([1500,-2100,1800],[280,-240,15],3000),style='cinematic',lighting='warm')
job('03-city-beneath','stereo','1993-11-02',core,stereo_bounds=[0,0,750,600],board_bounds=[0,0,750,600])
job('08-surface-daylight','stereo','1993-11-02',cam([1500,-2100,1800],[280,-240,15],3000))
job('10-modern-core','modern','2026-09-21',core)
job('10-modern-airport','modern','2026-09-21',wide,scene_path=str(A/'assets/modern_airport_scene.json'),modern_roofs_path=str(A/'assets/modern_airport_roofs.json'),board_bounds=[0,-3000,3000,600])
for ep in ['1989-10','1994-07','1997-04']:job('map-'+ep,'map',ep,core)
job('01-grand-overview','geography','mixed map editions 1986–1993',wide,geography_path=str(A/'assets/geography.json'),board_bounds=[0,-3000,3000,600])
job('02-runway-water','geography','mixed map editions 1986–1993',cam([4300,-4600,3300],[1800,-1600,0],4000),geography_path=str(A/'assets/geography.json'),board_bounds=[0,-3000,3000,600],style='cinematic',lighting='warm')
job('05-virtual-perspective','stereo','1993-11-02',cam([-500,550,240],[380,-550,25],None,35),style='cinematic',lighting='warm',mode='interpretive')
job('06-final-alignment','geography','mixed map editions 1986–1993',cam([1500,-1200,6000],[1500,-1200,0],6400),geography_path=str(A/'assets/geography.json'),board_bounds=[0,-3000,3000,600],mode='interpretive')
job('04-hill-observations','geography','1989-11',cam([10,620,370],[-315,1000,50],480),geography_path=str(A/'assets/hill.json'),board_bounds=[-480,830,-150,1160])
job('12-panorama','stereo','1993-11-02',cam([400,-2600,1400],[260,-220,15],2600),style='cinematic',lighting='warm',mode='interpretive')
job('11-surface-top','stereo','1993-11-02',cam([100,210,1600],[100,210,0],500))
job('11-map-top','map','1989-10',cam([100,210,1600],[100,210,0],500))
job('04-hill-context','geography','2014–2015 photography-derived terrain',cam([100,420,650],[-300,1020,50],1100),geography_path=str(A/'assets/hill_context.json'),mode='interpretive',style='cinematic',lighting='warm')
import csv,hashlib
R=A.parents[1]/'research/checkers-runway13'
marks=[]
for r in csv.DictReader((R/'reconstruction/block_matching/aerial_registration/sparse_stereo_points.csv').open()):
 if int(r['track_id']) in [26,708,1135]:marks.append({'label':{'26':'1','708':'2','1135':'3'}[r['track_id']],'point':[float(r['easting_hk1980_m'])-837500,float(r['northing_hk1980_m'])-821000,float(r['z_above_fitted_local_park_road_plane_m'])]})
for j in J:
 if j['id'] in ['01-grand-overview','02-runway-water','06-final-alignment']:
  j['marks']=[{'label':'KOWLOON','point':[280,160,2]},{'label':'RUNWAY 13 / 31','point':[2100,-2050,2]},{'label':'KOWLOON BAY','point':[850,-1400,2]},{'label':'SOURCE TILE GAP','point':[900,-2400,2]}]
 j['asset_hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (A/'assets').iterdir() if p.is_file()}
 if j['id']=='12-panorama':j['camera']['shift_x']=.16
 if j['id']=='03-city-beneath':j['marks']=[{'label':'scale0','point':[60,20,0]},{'label':'scale1','point':[160,20,0]}]
 if j['kind']=='map':j['map_image_path']=str(A/f'assets/map-{j["epoch"]}-display.png')
 if j['id'] in ['11-surface-top','11-map-top']:
  j['marks']=[dict(m,point=[*m['point'][:2],0] if j['kind']=='map' else m['point']) for m in marks]
 if j['kind'] in ['stereo','modern','map']:
  p=Path(j.get('scene_path',R/'reconstruction/block_matching/scene/scene.json'))
  j['scene_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
for j in J:(A/f'scenes/jobs/{j["id"]}.json').write_text(json.dumps(j,indent=2)+'\n')
(A/'metadata/render_jobs.json').write_text(json.dumps(J,indent=2)+'\n')
print(len(J),'jobs')
