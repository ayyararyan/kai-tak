"""Conservative image-grid surface patches, no filling, solids, or hidden geometry."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,struct,sys
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'python_deps'))
import cv2
MAX_EDGE_M=8.;MAX_DZ_M=3.;MAX_DISPARITY_STEP=1.;MAX_QUAD_PLANE_DEVIATION_M=1.5

def triangle_metrics(p,d):
 edges=np.stack([p[:,1]-p[:,0],p[:,2]-p[:,1],p[:,0]-p[:,2]],axis=1)
 edge=np.linalg.norm(edges,axis=2).max(1);dz=np.abs(edges[:,:,2]).max(1);dd=np.max(d,axis=1)-np.min(d,axis=1);area=np.linalg.norm(np.cross(edges[:,0],-edges[:,2]),axis=1)/2
 valid=np.isfinite(p).all((1,2))&np.isfinite(d).all(1)&(edge<=MAX_EDGE_M)&(dz<=MAX_DZ_M)&(dd<=MAX_DISPARITY_STEP)&(area>1e-8)
 return valid,edge,dz,dd,area

def run():
 rows=list(csv.DictReader((HERE/'dense_stereo_points.csv').open()));n=len(rows);world=np.array([[float(r['easting_hk1980_m']),float(r['northing_hk1980_m']),float(r['z_above_fitted_local_park_road_plane_m'])] for r in rows]);rgb=np.array([[int(r['r']),int(r['g']),int(r['b'])] for r in rows],np.uint8);xy=np.array([[int(r['rectified42_x']),int(r['rectified42_y'])] for r in rows]);qc=np.load(HERE/'dense_pixel_qc.npz');valid=qc['valid_correspondence'];disp=qc['disparity'];N=valid.shape[0]
 # Refuse changed point/calibration inputs if a previous completed verification no longer agrees.
 sr=json.loads((HERE/'sparse_stereo_report.json').read_text());dr=json.loads((HERE/'dense_stereo_report.json').read_text())
 if hashlib.sha256((HERE/'sparse_stereo_transform.npz').read_bytes()).hexdigest()!=dr['accepted_sparse_transform_sha256']:raise ValueError('Dense calibration binding changed')
 ids=np.full(valid.shape,-1,np.int32);ids[xy[:,1],xy[:,0]]=np.arange(n);top=ids[:-3,:-3];right=ids[:-3,3:];bottomright=ids[3:,3:];bottom=ids[3:,:-3]
 complete=(top>=0)&(right>=0)&(bottomright>=0)&(bottom>=0)
 all_pixels=cv2.erode(valid.astype(np.uint8),np.ones((4,4),np.uint8),anchor=(0,0),borderType=cv2.BORDER_CONSTANT,borderValue=0)[:-3,:-3]>0
 cy,cx=np.where(complete&all_pixels);qidx=np.c_[top[cy,cx],right[cy,cx],bottomright[cy,cx],bottom[cy,cx]];qp=world[qidx];norm=np.cross(qp[:,1]-qp[:,0],qp[:,2]-qp[:,0]);normlength=np.linalg.norm(norm,axis=1);deviation=np.divide(np.abs(np.sum((qp[:,3]-qp[:,0])*norm,axis=1)),normlength,out=np.full(len(norm),np.inf),where=normlength>1e-8)
 # Whole 4x4 observed pixel cell must have accepted data: this never bridges rejected/unknown interior holes.
 triangle_indices=np.concatenate([qidx[:,[0,1,2]],qidx[:,[0,2,3]]]);cell_x=np.tile(cx,2);cell_y=np.tile(cy,2);diagpart=np.r_[np.zeros(len(cx),int),np.ones(len(cx),int)];quaddev=np.tile(deviation,2)
 dp=disp[xy[:,1],xy[:,0]];passed,edge,dz,dd,area=triangle_metrics(world[triangle_indices],dp[triangle_indices]);passed&=quaddev<=MAX_QUAD_PLANE_DEVIATION_M
 faces=triangle_indices[passed];face_xyz=world[faces];signed=np.cross(face_xyz[:,1]-face_xyz[:,0],face_xyz[:,2]-face_xyz[:,0])[:,2];reverse=signed<0;faces[reverse]=faces[reverse][:,[0,2,1]]
 source_ids=np.array([int(r['dense_id']) for r in rows]);used=np.unique(faces);remap=np.full(n,-1,int);remap[used]=np.arange(len(used));fcompact=remap[faces];v=world[used];col=rgb[used]
 with (HERE/'observed_surface_mesh.ply').open('w') as f:
  f.write('ply\nformat ascii 1.0\ncomment partial observed-image-grid surfaces; NOT watertight or building solids\ncomment x y EPSG2326 metres; z relative fitted local park-road plane NOT HKPD\n'+f'element vertex {len(v)}\nproperty double x\nproperty double y\nproperty double z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nproperty int dense_point_id\nelement face {len(faces)}\nproperty list uchar int vertex_indices\nproperty int face_id\nend_header\n')
  for j,k in enumerate(used):f.write(' '.join(map(str,[*v[j],*col[j],source_ids[k]]))+'\n')
  for i,face in enumerate(fcompact):f.write('3 '+' '.join(map(str,face))+f' {i}\n')
 with (HERE/'observed_surface_faces.csv').open('w') as f:
  wr=csv.writer(f);wr.writerow(['face_id','dense_id0','dense_id1','dense_id2','rectified42_cell_x','rectified42_cell_y','diagonal_part','max_edge_m','max_relative_z_difference_m','disparity_range_rectified_px','quad_planarity_deviation_m','surface_area_m2','all_16_intervening_pixels_accepted','surface_identity_verified'])
  for j,k in enumerate(np.flatnonzero(passed)):wr.writerow([j,*source_ids[faces[j]],cell_x[k],cell_y[k],diagpart[k],edge[k],dz[k],dd[k],quaddev[k],area[k],True,False])
 # glTF uses right-handed Y-up. Local x=east, y=relative height, z=-north; metric origin is explicitly retained.
 origin=np.array([837600.,821200.,0.]);gltfpos=np.c_[v[:,0]-origin[0],v[:,2],-(v[:,1]-origin[1])].astype('<f4');index=fcompact.astype('<u4').ravel();rgba=np.c_[col,np.full(len(col),255,np.uint8)].astype(np.uint8)
 normals=np.zeros_like(gltfpos);normal=np.cross(gltfpos[fcompact[:,1]]-gltfpos[fcompact[:,0]],gltfpos[fcompact[:,2]]-gltfpos[fcompact[:,0]])
 for k in range(3):np.add.at(normals,fcompact[:,k],normal)
 leng=np.linalg.norm(normals,axis=1);normals/=np.where(leng>0,leng,1)[:,None]
 blobs=[gltfpos.tobytes(),normals.astype('<f4').tobytes(),rgba.tobytes(),index.tobytes()];binary=b'';views=[]
 for i,blob in enumerate(blobs):
  binary+=b'\0'*((-len(binary))%4);views.append({'buffer':0,'byteOffset':len(binary),'byteLength':len(blob),'target':34963 if i==3 else 34962});binary+=blob
 access=[{'bufferView':0,'componentType':5126,'count':len(v),'type':'VEC3','min':gltfpos.min(0).tolist(),'max':gltfpos.max(0).tolist()},{'bufferView':1,'componentType':5126,'count':len(v),'type':'VEC3'},{'bufferView':2,'componentType':5121,'normalized':True,'count':len(v),'type':'VEC4'},{'bufferView':3,'componentType':5125,'count':len(index),'type':'SCALAR'}]
 gltf={'asset':{'version':'2.0','generator':'historical observed stereo grid mesh'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'Observed historical surface patches'}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'COLOR_0':2},'indices':3,'material':0,'mode':4}]}],'materials':[{'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'metallicFactor':0,'roughnessFactor':1}}],'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':access,'extras':{'horizontal_crs':'EPSG:2326','origin_easting_m':origin[0],'origin_northing_m':origin[1],'axis_mapping':'glTF(x,y,z)=(easting-origin_easting,relative_height,-(northing-origin_northing))','vertical_reference':'fitted local park-road plane; NOT HKPD','source_epoch':'1993-11-02','surface_status':'partial observed correspondence patches; no unseen faces/closed solids','face_provenance':'observed_surface_faces.csv','face_order_matches_csv':True}}
 js=json.dumps(gltf,separators=(',',':')).encode();js+=b' '*((-len(js))%4);binary+=b'\0'*((-len(binary))%4);glb=struct.pack('<4sII',b'glTF',2,12+8+len(js)+8+len(binary))+struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(binary),b'BIN\0')+binary;(HERE/'observed_surface_mesh.glb').write_bytes(glb)
 # Topological openness: boundary edges remain deliberately unfilled.
 ed=np.sort(np.concatenate([fcompact[:,[0,1]],fcompact[:,[1,2]],fcompact[:,[2,0]]]),axis=1);_,counts=np.unique(ed,axis=0,return_counts=True)
 report={'generated_utc':datetime.now(timezone.utc).isoformat(),'status':'partial_observed_surface_mesh','method':'two fixed triangles per complete accepted rectified-grid 3px cell; no unconstrained Delaunay, extrusion, hole filling or unseen faces','surface_identity_note':'continuity-filtered image observations, not semantic proof of one named object per face','thresholds_engineering_choices_not_error_bounds':{'max_3d_edge_m':MAX_EDGE_M,'max_relative_z_difference_m':MAX_DZ_M,'max_disparity_range_rectified_px':MAX_DISPARITY_STEP,'max_quad_planarity_deviation_m':MAX_QUAD_PLANE_DEVIATION_M,'required_valid_intervening_pixels_per_cell':16,'source_grid_step_pixels':3},'counts':{'dense_input_points':n,'four_corner_cells':int(complete.sum()),'cells_all16_pixels_valid':len(qidx),'candidate_triangles':len(triangle_indices),'accepted_faces':len(faces),'retained_mesh_vertices':len(v),'boundary_edges':int((counts==1).sum()),'nonmanifold_edges':int((counts>2).sum())},'watertight':bool((counts==2).all()),'source_colors':'original A36143 greyscale pixel RGB; no generated textures','horizontal_crs':'EPSG:2326 diagnostic','vertical_reference':'same relative park-road plane as dense cloud, NOT HKPD','gltf_axis_origin':gltf['extras'],'face_metrics':{'max_3d_edge_m':float(edge[passed].max()),'max_relative_z_difference_m':float(dz[passed].max()),'max_disparity_range_rectified_px':float(dd[passed].max()),'max_quad_planarity_deviation_m':float(quaddev[passed].max()),'sum_observed_triangle_area_m2':float(area[passed].sum())},'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'dense_stereo_points.csv',HERE/'dense_pixel_qc.npz',HERE/'dense_stereo_report.json']},'limitations':['nominal-calibration and local-control limitations inherited from sparse/dense reports','occluded/textureless/rejected regions deliberately unmeshed','continuity thresholds do not prove all matches are correct','surfaces are not watertight buildings or complete ground/obstacle geometry']}
 (HERE/'observed_surface_mesh_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
