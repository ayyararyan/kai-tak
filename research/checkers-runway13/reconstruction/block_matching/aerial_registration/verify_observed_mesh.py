from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,struct
import numpy as np
from build_observed_mesh import triangle_metrics
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'observed_surface_mesh_report.json').read_text());checks={}
checks['bound_inputs_unchanged']=all(hashlib.sha256((HERE/k).read_bytes()).hexdigest()==h for k,h in r['input_sha256'].items())
text=(HERE/'observed_surface_mesh.ply').read_text().splitlines();h=text.index('end_header');nv=int(next(x for x in text[:h] if x.startswith('element vertex')).split()[-1]);nf=int(next(x for x in text[:h] if x.startswith('element face')).split()[-1]);verts=np.array([[float(v) for v in line.split()] for line in text[h+1:h+1+nv]]);fac=np.array([[int(v) for v in line.split()] for line in text[h+1+nv:]])
checks['ply_counts_match']=nv==r['counts']['retained_mesh_vertices'] and nf==r['counts']['accepted_faces'] and len(fac)==nf
checks['mesh_positions_finite']=bool(np.isfinite(verts).all());checks['triangle_indices_valid']=bool((fac[:,0]==3).all() and (fac[:,1:4]>=0).all() and (fac[:,1:4]<nv).all())
faces=list(csv.DictReader((HERE/'observed_surface_faces.csv').open()));checks['perface_provenance_count']=len(faces)==nf
ids=verts[:,6].astype(int);fromply=ids[fac[:,1:4]];fromcsv=np.array([[int(f['dense_id0']),int(f['dense_id1']),int(f['dense_id2'])] for f in faces]);checks['all_face_point_ids_match']=np.array_equal(fromply,fromcsv)
qc=np.load(HERE/'dense_pixel_qc.npz');valid=qc['valid_correspondence'];cx=np.array([int(f['rectified42_cell_x']) for f in faces]);cy=np.array([int(f['rectified42_cell_y']) for f in faces]);allvalid=True
for dy in range(4):
 for dx in range(4):allvalid=allvalid and bool(valid[cy+dy,cx+dx].all())
checks['every_face_all16_pixels_supported']=allvalid
p=verts[fac[:,1:4],:3];e=np.stack([p[:,1]-p[:,0],p[:,2]-p[:,1],p[:,0]-p[:,2]],axis=1);checks['every_face_edge_threshold']=bool((np.linalg.norm(e,axis=2).max(1)<=8).all());checks['every_face_depth_jump_threshold']=bool((np.abs(e[:,:,2]).max(1)<=3).all());checks['every_face_disparity_threshold']=all(float(f['disparity_range_rectified_px'])<=1 for f in faces);checks['every_face_quad_planarity_threshold']=all(float(f['quad_planarity_deviation_m'])<=1.5 for f in faces)
ed=np.sort(np.concatenate([fac[:,[1,2]],fac[:,[2,3]],fac[:,[3,1]]]),axis=1);_,cnt=np.unique(ed,axis=0,return_counts=True);checks['boundary_edges_preserved_no_watertight_claim']=int((cnt==1).sum())==r['counts']['boundary_edges'] and not r['watertight'];checks['no_nonmanifold_edges']=not bool((cnt>2).any())
b=(HERE/'observed_surface_mesh.glb').read_bytes();magic,version,length=struct.unpack_from('<4sII',b);jslen,jstype=struct.unpack_from('<I4s',b,12);j=json.loads(b[20:20+jslen]);blen,btype=struct.unpack_from('<I4s',b,20+jslen);body=b[28+jslen:];checks['glb_container_valid']=magic==b'glTF' and version==2 and length==len(b) and jstype==b'JSON' and btype==b'BIN\0' and blen==len(body)
def acc(i,dtype,width):
 a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];return np.frombuffer(body,dtype=dtype,count=a['count']*width,offset=v['byteOffset']).reshape(-1,width)
pos=acc(0,'<f4',3);norm=acc(1,'<f4',3);color=acc(2,'u1',4);index=acc(3,'<u4',1).reshape(-1,3)
expected=np.c_[verts[:,0]-837600,verts[:,2],-(verts[:,1]-821200)];checks['glb_axis_origin_positions_match_ply']=bool(np.max(np.abs(pos-expected))<.0002);checks['glb_colors_match_observed_source']=np.array_equal(color[:,:3],verts[:,3:6].astype('u1'));checks['glb_faces_match_ply']=np.array_equal(index,fac[:,1:4]);checks['glb_normals_finite_unit']=bool(np.isfinite(norm).all() and np.allclose(np.linalg.norm(norm,axis=1),1,atol=1e-4));checks['glb_crs_and_relative_height_explicit']=j['extras']['horizontal_crs']=='EPSG:2326' and 'NOT HKPD' in j['extras']['vertical_reference']
# Synthetic discontinuity cases test different rejection reasons, not just existing data.
base=np.array([[[0.,0,0],[1,0,0],[0,1,0]]]);dis=np.zeros((1,3));checks['fixture_continuous_face_accepted']=bool(triangle_metrics(base,dis)[0][0])
long=base.copy();long[0,1,0]=9;checks['fixture_long_edge_rejected']=not bool(triangle_metrics(long,dis)[0][0])
step=base.copy();step[0,1,2]=3.1;checks['fixture_depth_jump_rejected']=not bool(triangle_metrics(step,dis)[0][0])
checks['fixture_disparity_jump_rejected']=not bool(triangle_metrics(base,np.array([[0,0,1.1]]))[0][0]);zero=np.zeros((1,3,3));checks['fixture_degenerate_face_rejected']=not bool(triangle_metrics(zero,dis)[0][0])
report={'verified_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'all_passed':all(checks.values()),'mesh_watertight':False,'complete_city_mesh':False,'source_reconstruction_accuracy_calibrated':False}
(HERE/'observed_mesh_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
