"""Build offline evidence workbench without inventing missing historic volumes."""
from pathlib import Path
import json,hashlib,base64,math,shutil
import numpy as np
from PIL import Image
from pyproj import Transformer
from shapely.geometry import shape,mapping,box,Polygon
from shapely.ops import transform,triangulate
from plotly.offline import get_plotlyjs

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
PROJ=ROOT.parent.parent
ORIGIN=[837500,821000]
EPOCHS=['1989-10','1994-07','1997-04']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dataurl(p):return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
def local_ring(ring):return [[round(x-ORIGIN[0],4),round(y-ORIGIN[1],4)] for x,y,*_ in ring]

def modern_layer():
 p=PROJ/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson'
 fcs=read(p)['features'];tohk=Transformer.from_crs(4326,2326,always_xy=True).transform
 out=[];omitted=[];bounds=box(837500,821000,838250,821600)
 for f in fcs:
  geom=transform(tohk,shape(f['geometry']));pr=f['properties']
  if not geom.intersects(bounds):continue
  b=pr.get('BaseHeight');t=pr.get('TopHeight')
  if not geom.is_valid or b is None or t is None or not all(math.isfinite(v) for v in (b,t)) or t<b:
   omitted.append(dict(id=pr.get('BuildingCSUID'),reason='invalid_geometry_or_missing_inconsistent_heights'));continue
  g=geom.intersection(bounds)
  parts=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
  for j,q in enumerate(parts):
   if q.geom_type!='Polygon':continue
   out.append(dict(id=pr['BuildingCSUID']+f':{j}',name=pr.get('BuildingNameEN') or 'Unnamed current component',category='modern_2026_comparison_only',epoch='2026-09-21',crs='EPSG:2326',vertical_datum='HKPD',top_hkpd_m=t,base_hkpd_m=b,geometry=mapping(q),outer_local=local_ring(q.exterior.coords),rings_local=[local_ring(r.coords) for r in [q.exterior,*q.interiors]],height_transfer_to_historical=False))
 return dict(source_path=str(p.relative_to(PROJ)),source_sha256=sha(p),epoch='2026-09-21',vertical_datum='HKPD',category='modern_2026_comparison_only',features=out,omitted=omitted,not_historical_geometry=True)

def stereo_adapter():
 import csv
 report=ROOT/'aerial_registration/sparse_stereo_report.json'
 source=ROOT/'aerial_registration/sparse_stereo_points.csv'
 if not report.exists() or not source.exists():return dict(available=False,status='Stereo producer has not yet supplied verified point inputs.',points=[],vertical_datum=None)
 d=read(report)
 if 'NOT HKPD' not in d['vertical_reference']:raise ValueError('Stereo adapter requires explicit relative vertical reference')
 points=[];omitted=[]
 with source.open() as stream:rows=list(csv.DictReader(stream))
 for r in rows:
  if r.get('passes_diagnostic_5px_filter')!='True' or r.get('positive_depth_both_views')!='True':
   omitted.append(dict(track_id=r.get('track_id'),reason='diagnostic_filter_or_positive_depth_not_explicitly_true'));continue
  e=float(r['easting_hk1980_m']);n=float(r['northing_hk1980_m']);z=float(r['z_above_fitted_local_park_road_plane_m'])
  if not all(math.isfinite(v) for v in (e,n,z)):raise ValueError('Nonfinite stereo point')
  points.append(dict(id=int(r['track_id']),e=e,n=n,z_relative_m=z,x=e-ORIGIN[0],y=n-ORIGIN[1],color=[int(r[k]) for k in ('r','g','b')],reprojection_rms_px=float(r['reprojection_rms_px']),within_control_hull=r['within_map_control_hull']=='True',surface_class=r['surface_class'],note=r['manual_surface_note'],in_core=837500<=e<=838250 and 821000<=n<=821600,category='measured_stereo_point_conditional_nominal_calibration',epoch=d['source_date'],hkpd_elevation_m=None))
 return dict(available=True,vertical_datum='relative_ground_plane',source_epoch=d['source_date'],source_frames=d['source_frames'],points=points,source_row_count=len(rows),accepted_row_count=len(points),omitted_row_count=len(omitted),omitted=omitted,report=d,report_sha256=sha(report),csv_sha256=sha(source),ply_sha256=sha(source.with_suffix('.ply')),downloads={'csv':'../aerial_registration/sparse_stereo_points.csv','ply':'../aerial_registration/sparse_stereo_points.ply','report':'../aerial_registration/sparse_stereo_report.json'},physical_surface_mesh=False,calibrated_error_bounds=None)

def dense_adapter():
 import csv
 report=ROOT/'aerial_registration/dense_stereo_report.json';source=ROOT/'aerial_registration/dense_stereo_points.csv'
 if not report.exists() or not source.exists():return dict(available=False,points=[])
 d=read(report)
 with source.open() as stream:rows=list(csv.DictReader(stream))
 preview=[]
 # Display-only thinning to bound browser load; complete, original-coordinate
 # CSV and PLY remain the exported reconstruction and are linked explicitly.
 stride=max(1,math.ceil(len(rows)/60000))
 for k,r in enumerate(rows):
  if k%stride:continue
  e=float(r['easting_hk1980_m']);n=float(r['northing_hk1980_m']);z=float(r['z_above_fitted_local_park_road_plane_m'])
  preview.append([int(r['dense_id']),e-ORIGIN[0],n-ORIGIN[1],z,int(r['r']),r['within_map_control_hull']=='True',float(r['reprojection_rms_px'])])
 return dict(available=True,category='conditional_dense_image_triangulation_unclassified',source_epoch=d['source_epoch'],vertical_datum='relative_ground_plane',total_source_points=len(rows),display_stride=stride,display_count=len(preview),columns=['dense_id','local_e_m','local_n_m','z_relative_m','gray','inside_control_hull','reprojection_rms_px'],points=preview,report=d,csv_sha256=sha(source),ply_sha256=sha(source.with_suffix('.ply')),report_sha256=sha(report),downloads={'csv':'../aerial_registration/dense_stereo_points.csv','ply':'../aerial_registration/dense_stereo_points.ply','report':'../aerial_registration/dense_stereo_report.json'},absolute_vertical_datum=None,physical_mesh=False)

def mesh_adapter():
 report=ROOT/'aerial_registration/observed_surface_mesh_report.json';source=ROOT/'aerial_registration/observed_surface_mesh.ply'
 if not source.exists() or not report.exists():return dict(available=False,vertices=[],faces=[])
 d=read(report)
 if d.get('watertight') is not False or 'NOT HKPD' not in d.get('vertical_reference',''):raise ValueError('Unsupported mesh semantics')
 for name,h in d['input_sha256'].items():
  if sha(report.parent/name)!=h:raise ValueError('Mesh input changed since production: '+name)
 vertices=[];faces=[]
 with source.open() as f:
  header=[]
  for line in f:
   header.append(line.strip())
   if line.strip()=='end_header':break
  nv=int(next(x for x in header if x.startswith('element vertex ')).split()[-1]);nf=int(next(x for x in header if x.startswith('element face ')).split()[-1])
  if header[1]!='format ascii 1.0':raise ValueError('Unsupported PLY encoding')
  for _ in range(nv):
   q=next(f).split();vertices.append([float(q[0])-ORIGIN[0],float(q[1])-ORIGIN[1],float(q[2]),int(q[3]),int(q[4]),int(q[5]),int(q[6])])
  for _ in range(nf):
   q=list(map(int,next(f).split()))
   if q[0]!=3 or any(v<0 or v>=nv for v in q[1:4]):raise ValueError('Invalid mesh triangle')
   faces.append(q[1:])
 if nv!=d['counts']['retained_mesh_vertices'] or nf!=d['counts']['accepted_faces']:raise ValueError('Mesh report count mismatch')
 return dict(available=True,category='partial_observed_image_surfaces_not_building_solids',source_epoch='1993-11-02',vertical_datum='relative_ground_plane',watertight=False,complete_buildings=False,vertices=vertices,vertex_columns=['local_e_m','local_n_m','z_relative_m','r','g','b','dense_point_id'],faces=faces,face_columns=['vertex_i','vertex_j','vertex_k','source_face_id'],report=d,ply_sha256=sha(source),glb_sha256=sha(source.with_suffix('.glb')),report_sha256=sha(report),downloads={'ply':'../aerial_registration/observed_surface_mesh.ply','glb':'../aerial_registration/observed_surface_mesh.glb','report':'../aerial_registration/observed_surface_mesh_report.json'})

def main():
 fs=read(ROOT/'historical_faces_hk1980.geojson')['features'];historical=[]
 for f in fs:
  p=f['properties']
  if p['review_status']!='visually_checked_map_face':raise ValueError('Unreviewed historic geometry')
  if p['historical_top_hkpd_m'] is not None or p['historical_base_hkpd_m'] is not None:raise ValueError('Historical non-null height needs a new explicit height source adapter')
  historical.append(dict(id=p['id'],name=p['name'],source_epoch=p['source_epoch'],category='historical_depicted_map_face',geometry=f['geometry'],outer_local=local_ring(f['geometry']['coordinates'][0]),height_m=None,base_hkpd_m=None,top_hkpd_m=None,physical_volume=None,display_reference_plane_z=0,display_plane_is_physical_surface=False,properties=p))
 tf=Transformer.from_crs(4326,2326,always_xy=True).transform;blocks=[]
 for f in read(ROOT/'aerial_registration/four_road_control_blocks.geojson')['features']:
  g=transform(tf,shape(f['geometry']));blocks.append(dict(**f['properties'],outer_local=local_ring(g.exterior.coords),geometry=mapping(g),crs='EPSG:2326',physical_volume=None))
 maps=[];render_maps=[]
 for ep in EPOCHS:
  p=ROOT/f'registered/11-NE-11A_{ep}_core.png';meta=read(p.with_suffix('.json'))
  maps.append(dict(epoch=ep,source_path=str(p.relative_to(ROOT)),sha256=sha(p),crs='EPSG:2326',bounds=meta['bounds'],role='historical_map_reference_plane_not_terrain'))
  im=Image.open(p).convert('L');small=np.array(im.resize((250,200),Image.Resampling.LANCZOS))
  render_maps.append(dict(epoch=ep,image=dataurl(p),gray=small.tolist()))
 stereo=stereo_adapter();modern=modern_layer();dense=dense_adapter();mesh=mesh_adapter()
 scene=dict(schema_version='1.0',title='Kai Tak · a city reconstructed from evidence',status='historical_reconstruction_incomplete',origin_epsg2326=ORIGIN,horizontal_crs='EPSG:2326',historical_faces=historical,road_block_cells=blocks,maps=maps,modern=modern,stereo=stereo,dense=dense,observed_mesh=mesh,source_files={n:sha(ROOT/n) for n in ['historical_faces_hk1980.geojson','structure_matches.json','modern_correspondences.json','aerial_registration/four_road_control_blocks.geojson']},historical_height_unknown=True,clearance_certified=False,vertical_separation='Historical map faces have no physical height. Relative stereo and absolute modern HKPD elevations are separate views, never combined.',scope='45 source faces / 15 named mapped forms; not a complete historical building census',downloads={'historical':'../historical_faces.geojson','projected':'../historical_faces_hk1980.geojson','matches':'../structure_matches.json','report':'../REPORT.md','registration':'../registration_report.md'})
 (OUT/'scene.json').write_text(json.dumps(scene,indent=2)+'\n')
 (OUT/'modern_comparison_hk1980.geojson').write_text(json.dumps({'type':'FeatureCollection','crs':{'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::2326'}},'features':[{'type':'Feature','geometry':f['geometry'],'properties':{k:v for k,v in f.items() if k not in ('geometry','outer_local')}} for f in modern['features']]},indent=2)+'\n')
 html=(OUT/'template.html').read_text().replace('/*PLOTLY_BUNDLE*/',get_plotlyjs()).replace('/*SCENE_DATA*/',json.dumps({**scene,'render_maps':render_maps}).replace('</','<\\/'))
 (OUT/'index.html').write_text(html)
 validation=dict(historical_faces=len(historical),named_forms=len({f['id'] for f in historical}),source_epochs=EPOCHS,historic_physical_volumes=sum(f['physical_volume'] is not None for f in historical),historic_nonnull_heights=sum(f['height_m'] is not None for f in historical),road_cells=len(blocks),modern_components=len(modern['features']),modern_omitted_components=len(modern['omitted']),stereo_available=stereo['available'],dense_available=dense['available'],dense_source_points=dense.get('total_source_points',0),dense_preview_points=dense.get('display_count',0),observed_mesh_faces=len(mesh.get('faces',[])),observed_mesh_vertices=len(mesh.get('vertices',[])),sparse_omitted_rows=stereo.get('omitted_row_count',0),modern_courtyard_components=sum(len(f['rings_local'])>1 for f in modern['features']),offline_plotly_bundled=True,browser_interaction_verified=False,browser_verification_blocker='Parent attempted file and localhost navigation via OpenClaw; navigation policy blocked both. No bypass attempted.',scene_sha256=sha(OUT/'scene.json'))
 (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation))
if __name__=='__main__':main()
