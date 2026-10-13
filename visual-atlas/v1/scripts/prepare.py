#!/usr/bin/env python3
"""Prepare hash-bound atlas inputs; does not change scientific reconstruction."""
from pathlib import Path
import json,hashlib,sys,platform,math
import numpy as np
from PIL import Image
from shapely.geometry import shape,box,mapping
from shapely.ops import transform
from shapely import constrained_delaunay_triangles
from pyproj import Transformer
A=Path(__file__).resolve().parents[1]; ROOT=A.parents[1]; R=ROOT/'research/checkers-runway13'; B=R/'reconstruction/block_matching'; O=np.array([837500.,821000.])
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def display_texture(source,dest):
 im=Image.open(source).convert('RGB');arr=np.array(im).astype(float)
 # Contrast grading of existing raster ink only; no detail generation or upscaling.
 gray=arr.mean(axis=2);ink=np.minimum((255-gray)/255*4,1)
 paper=np.array([242,240,228]);line=np.array([55,75,75]);out=paper[None,None,:]*(1-ink[:,:,None])+line[None,None,:]*ink[:,:,None]
 Image.fromarray(out.astype('uint8')).save(dest)
 return str(dest)
def roofs(features):
 out={}
 for f in features:
  p=shape(f['geometry']); triangles=list(constrained_delaunay_triangles(p).geoms)
  assert abs(sum(t.area for t in triangles)-p.area)<max(1e-6,p.area*1e-9)
  assert all(p.covers(t.representative_point()) for t in triangles)
  out[f['id']]=[[[float(x-O[0]),float(y-O[1])] for x,y in list(t.exterior.coords)[:3]] for t in triangles]
 return out
sources=[B/'scene/scene.json',B/'historical_faces_hk1980.geojson',B/'aerial_registration/observed_surface_mesh.ply',B/'aerial_registration/observed_surface_mesh.glb',B/'aerial_registration/observed_surface_mesh_report.json',B/'aerial_registration/dense_stereo_points.csv',B/'aerial_registration/dense_stereo_report.json',B/'aerial_registration/sparse_stereo_points.csv',B/'aerial_registration/manual_stereo_labels.json',R/'reconstruction/chronology/aerial/date_annotation_audit.json',R/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson',R/'geospatial/derived/Kowloon_KaiTak_DTM_5m_HK1980.tif']
for n in ['runway_map_mosaic.png','map_mosaic_manifest.json','mapped_runway_edges.geojson','historical_seawall.geojson','historical_hill_terrain.geojson']:sources.append(R/'integrated/geometry'/n)
for ep in ['1989-10','1994-07','1997-04']:
 sources += [B/f'registered/11-NE-11A_{ep}_core.png',B/f'registered/11-NE-11A_{ep}_core.json']
for f in ['A36142','A36143']:sources.append(R/f'reconstruction/chronology/aerial/fullframes/{f}.jpg')
s=read(B/'scene/scene.json')
# Producer hash chain: never bypass stale mesh or stale source exports.
for name,h in s['observed_mesh']['report']['input_sha256'].items():
 p=B/'aerial_registration'/name;assert sha(p)==h,name
for section in ['stereo','dense']:
 for ext in ['csv','ply']:
  p=B/'aerial_registration'/f'{"sparse" if section=="stereo" else "dense"}_stereo_points.{ext}';assert sha(p)==s[section][ext+'_sha256'],p
for ext in ['ply','glb']:assert sha(B/'aerial_registration'/('observed_surface_mesh.'+ext))==s['observed_mesh'][ext+'_sha256']
assert all(f['height_m'] is None and f['physical_volume'] is None for f in s['historical_faces'])
write(A/'assets/modern_roofs.json',roofs(s['modern']['features']))
# Broad modern airport rectangle, preserving valid complete polygon geometry; omitted records explicit.
tohk=Transformer.from_crs(4326,2326,always_xy=True).transform
features=[];omitted=[];extent=box(837500,818000,840500,821600)
for f in read(R/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson')['features']:
 p=f['properties']
 if not f.get('geometry'):
  omitted.append({'id':p.get('BuildingCSUID'),'reason':'null geometry'});continue
 g=transform(tohk,shape(f['geometry']))
 if g.geom_type not in ['Polygon','MultiPolygon']:
  omitted.append({'id':p.get('BuildingCSUID'),'reason':'nonpolygon geometry'});continue
 if not g.intersects(extent):continue
 base=p.get('BaseHeight');top=p.get('TopHeight')
 if not g.is_valid or base is None or top is None or not all(isinstance(t,(int,float)) and math.isfinite(t) for t in [base,top]) or top<base:
  omitted.append({'id':p.get('BuildingCSUID'),'reason':'invalid geometry or absent/inconsistent height'});continue
 for i,q in enumerate(g.geoms if g.geom_type=='MultiPolygon' else [g]):
  if q.geom_type!='Polygon':continue
  features.append(dict(id=str(p['BuildingCSUID'])+f':{i}',name=p.get('BuildingNameEN') or 'Unnamed modern component',geometry=mapping(q),rings_local=[[[x-O[0],y-O[1]] for x,y in ring.coords] for ring in [q.exterior,*q.interiors]],base_hkpd_m=base,top_hkpd_m=top,epoch='2026-09-21',vertical_datum='HKPD',height_transfer_to_historical=False))
write(A/'assets/modern_airport_scene.json',{'origin_epsg2326':O.tolist(),'modern':{'vertical_datum':'HKPD','epoch':'2026-09-21','features':features,'omitted':omitted,'source_path':'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson'},'historical_faces':[]})
write(A/'assets/modern_airport_roofs.json',roofs(features))
geo={'origin_epsg2326':O.tolist(),'vertical_datum':'display plane only, not physical terrain','features':[]}
mapdisplay=display_texture(R/'integrated/geometry/runway_map_mosaic.png',A/'assets/map-mosaic-display.png')
for ep in ['1989-10','1994-07','1997-04']:display_texture(B/f'registered/11-NE-11A_{ep}_core.png',A/f'assets/map-{ep}-display.png')
geo['features'].append(dict(name='Historical airport survey map mosaic',type='image_plane',coordinates=[[0,-3000,0],[3000,600,0]],image_path=mapdisplay,evidence_level='A cartographic observations; mixed editions',source='integrated/geometry/map_mosaic_manifest.json',material='map'))
for n in ['mapped_runway_edges','historical_seawall']:
 for f in read(R/f'integrated/geometry/{n}.geojson')['features']:
  p=f['properties'];en=p.get('EN_m');
  if not en:
   g=transform(tohk,shape(f['geometry']));en=list(g.coords)
  geo['features'].append(dict(name=p.get('id',n),type='polyline',coordinates=[[x-O[0],y-O[1],2] for x,y,*_ in en],evidence_level='A source map line; display Z not elevation',source=f'integrated/geometry/{n}.geojson',epoch=p.get('edition_month',p.get('edition_date','see source sheet records')),material='accent' if n=='mapped_runway_edges' else 'water',width=3))
write(A/'assets/geography.json',geo)
hill={'origin_epsg2326':O.tolist(),'vertical_datum':'HKPD for mapped elevations, display plane not terrain','features':[]}
for f in read(R/'integrated/geometry/historical_hill_terrain.geojson')['features']:
 p=f['properties'];g=transform(tohk,shape(f['geometry']));z=p.get('elevation_HKPD_m')
 if z is None:continue
 if g.geom_type=='Point':
  # Cross marks, not invented hill/marker geometry.
  x,y=g.x-O[0],g.y-O[1];coords=[[x-3,y,z],[x+3,y,z],[x,y,z],[x,y-3,z],[x,y+3,z]]
 else:coords=[[x-O[0],y-O[1],z] for x,y in g.coords]
 hill['features'].append(dict(name=p['id'],type='polyline',coordinates=coords,evidence_level='A mapped height observation, not full terrain',source='integrated/geometry/historical_hill_terrain.geojson',epoch=p.get('edition_month','1989-11'),material='accent',width=.8))
write(A/'assets/hill.json',hill)
import rasterio
from rasterio.windows import from_bounds
with rasterio.open(R/'geospatial/derived/Kowloon_KaiTak_DTM_5m_HK1980.tif') as ds:
 win=from_bounds(836850,821700,837550,822350,ds.transform).round_offsets().round_lengths()
 z=ds.read(1,window=win,masked=True);tr=ds.window_transform(win)
 assert not np.ma.getmaskarray(z).any() and np.isfinite(z).all(), 'Missing terrain samples require explicit omission adapter; refusing scene'
 vs=[];fs=[];nr,nc=z.shape
 for row in range(nr):
  for col in range(nc):
   x,y=tr*(col+.5,row+.5);vs.append([x-O[0],y-O[1],float(z[row,col])])
 for row in range(nr-1):
  for col in range(nc-1):
   i=row*nc+col
   for tri in [[i,i+nc,i+1],[i+1,i+nc,i+nc+1]]:
    if all(not np.ma.is_masked(z[k//nc,k%nc]) and np.isfinite(z[k//nc,k%nc]) for k in tri):fs.append(tri)
write(A/'assets/hill_context.json',dict(origin_epsg2326=O.tolist(),vertical_datum='HKPD; modern 2014–2015 terrain only',features=[dict(name='Checkerboard Hill region · 2014–2015 terrain context',type='mesh',vertices=vs,faces=fs,contextual=True,epoch='2014–2015 photography',source='geospatial/derived/Kowloon_KaiTak_DTM_5m_HK1980.tif',evidence_level='B modern contextual DTM, not historical terrain',material='terrain')]))
rows=[dict(path=str(p.relative_to(ROOT)),available=p.exists(),bytes=p.stat().st_size if p.exists() else None,sha256=sha(p) if p.exists() else None) for p in sources]
write(A/'metadata/input_manifest.json',dict(files=rows,original_scene_sha256=sha(B/'scene/scene.json'),source_restore_receipt='metadata/restore_receipt.json; separate recorded acquisition operation, not re-run by prepare.py',unavailable=['complete calibrated 1993 city','complete historical coastline vector','verified historical runway threshold registration','absolute HKPD transform for stereo','historical building heights for mapped faces']))
write(A/'qa/preparation.json',dict(source_hash_chain='passed',modern_core_components=len(s['modern']['features']),modern_wide_components=len(features),modern_wide_omitted=len(omitted),historical_null_heights=len(s['historical_faces']),modern_roof_triangulation_area_and_holes='passed',origin_epsg2326=O.tolist(),blender_axes='X=easting-837500,Y=northing-821000,Z=explicit view datum',glb_mapping_documented='GLB x+837600=E; -GLB z+821200=N; GLB y=relative Z; renderer uses PLY-derived source scene, no GLB reorientation ambiguity',vertical_exaggeration=1))
write(A/'metadata/python_environment.json',dict(python=sys.version,platform=platform.platform(),numpy=np.__version__))
print('Prepared',len(rows),'hash-bound sources;',len(features),'wide modern components;',len(hill['features']),'hill observations')
