"""Source-derived convex projection envelope; NOT a calibrated in-flight shape."""
from pathlib import Path
import json,hashlib,numpy as np
from scipy.spatial import ConvexHull,HalfspaceIntersection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'integrated/geometry'
curves=np.load(OUT/'aircraft_dxf_curves.npz')
regions={'plan':(4100,450,6920,3100),'side':(4100,3500,6920,4300),'front':(550,2150,3200,2980)}
raw={}
for k,(x0,y0,x1,y1) in regions.items():
 p=np.vstack([p for p in curves.values() if np.all((p[:,0]>=x0)&(p[:,0]<=x1)&(p[:,1]>=y0)&(p[:,1]<=y1))]);raw[k]=p
s=.0254;nose=raw['side'][:,0].min();plan_mid=(raw['plan'][:,1].max()+raw['plan'][:,1].min())/2;front_mid=(raw['front'][:,0].max()+raw['front'][:,0].min())/2;ground_side=raw['side'][:,1].min();ground_front=raw['front'][:,1].min()
projections={'plan':np.c_[(nose-raw['plan'][:,0])*s,(raw['plan'][:,1]-plan_mid)*s], 'side':np.c_[(nose-raw['side'][:,0])*s,(raw['side'][:,1]-ground_side)*s], 'front':np.c_[(raw['front'][:,0]-front_mid)*s,(raw['front'][:,1]-ground_front)*s]}
planes=[];hulls={}
# drawing website says +/-6in SHOULD be accurate for gate planning, NOT hard flight error bound
padding=.1524 + .05*s
for name,p in projections.items():
 if name in ['plan','front']:
  mirrored=p.copy();mirrored[:,1 if name=='plan' else 0]*=-1;p=np.vstack([p,mirrored])
 h=ConvexHull(p);hulls[name]=p[h.vertices].tolist()
 for a,b,c in h.equations:
  n={'plan':[a,b,0],'side':[a,0,b],'front':[0,a,b]}[name]
  planes.append(n+[float(c-padding)])
planes=np.array(planes);interior=np.array([-35.,0.,6.]);hs=HalfspaceIntersection(planes,interior);verts=hs.intersections;h=ConvexHull(verts)
r={'schema_version':1,'status':'source_derived_static_planning_envelope_conditional_only','calibrated_inflight_envelope':False,'query_airframe':'747-409B baseline; source drawing generic747-400, exact historical fit unverified','source_dxf':'integrated/sources/747-400.dxf','source_dxf_sha256':hashlib.sha256((ROOT/'integrated/sources/747-400.dxf').read_bytes()).hexdigest(),'source_archive_date':'1998-03-19 archive-member timestamp, not verified engineering revision','units_inference':'drawing coordinates inches, checked against213ft front span and225ft2in side fuselage dimension; no $INSUNITS header','scale_m_per_drawing_unit':s,'body_axes':'x forward (nose station0, aftnegative), y right (symmetrized), z up; left-handed engineering coordinates','origin':'nose longitudinal station, symmetryplane, static drawn wheel-ground plane; NOT CG','source_region_bounds_drawing_units':regions,'projection_normalization':{'nose_draw_x':float(nose),'plan_center_y':float(plan_mid),'front_center_x':float(front_mid),'side_ground_y':float(ground_side),'front_ground_y':float(ground_front)},'drawing_projection_hulls_body_m':hulls,'halfspaces_n_dot_b_plus_c_le_zero':planes.tolist(),'vertices_body_m':verts.tolist(),'triangles':h.simplices.tolist(),'bounds_m':[verts.min(axis=0).tolist(),verts.max(axis=0).tolist()],'projection_padding_m':padding,'padding_semantics':'conditional engineering inflation using website SHOULD +/-6in plus chord approximation .05in; NOT statisticalCI or certified deformation bound','clearance_eligible_historical':False,'missing':['inflightwingflex/flaps30shape','aircraft-specific configuration confirmation','CG and actual gear-contact reference','pitch/angle-of-attack relation and sideslip','tracking and attitude uncertainty','validated swept-envelope hard error bounds'],'limitations':['Convex hull fills unoccupied space; overlap is not physical collision proof.','Projectionintersection is only an outer shape if all normalized true projections lie inside supplied hulls.','Static front/side ground planes and pitch are aligned by assumption; not independently calibrated.','Drawing cropping removes annotation entities, hulls and dimensions require inspection.']}
r['status']='diagnostic_projection_intersection_not_accepted_airframe_bound'
r['limitations'].append('Projectionintersection reaches19.14m, below manual maximum19.51m: static views not sufficiently registered to use this tighter shape as a conservative aircraft bound.')
(OUT/'airframe_projection_intersection.json').write_text(json.dumps(r,indent=2)+'\n')
from itertools import product
lo=np.array([-max(np.ptp(raw['side'][:,0])*s,70.67),-np.ptp(raw['plan'][:,1])*s/2,0.])-padding
hi=np.array([0.,np.ptp(raw['plan'][:,1])*s/2,19.51])+padding
verts=np.array(list(product(*zip(lo,hi))));h=ConvexHull(verts)
r=dict(r,status='static_planning_dimension_outer_box_conditional_only',vertices_body_m=verts.tolist(),triangles=h.simplices.tolist(),bounds_m=[lo.tolist(),hi.tolist()],halfspaces_n_dot_b_plus_c_le_zero=h.equations.tolist())
r['limitations'].append('Primary box uses union of drawing dimensional extents and manual maximumstaticheight, not rejected tighter projectionintersection. No precise collision follows from boxoverlap.')
(OUT/'airframe_envelope.json').write_text(json.dumps(r,indent=2)+'\n')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig=plt.figure(figsize=(11,7));ax=fig.add_subplot(projection='3d');ax.plot_trisurf(verts[:,0],verts[:,1],verts[:,2],triangles=h.simplices,color='#85998b',alpha=.65,linewidth=.15,edgecolor='#425348');ax.set(xlabel='Forward from nose station (m)',ylabel='Right (m)',zlabel='Above drawn ground plane (m)',title='747-400 source-derived outer envelope\nStatic planning geometry; not calibrated flight clearance');ax.set_box_aspect((71,65,20));fig.tight_layout();fig.savefig(OUT/'airframe_envelope.png',dpi=150);fig.savefig(OUT/'airframe_envelope.pdf');plt.close(fig)
print('planes',len(planes),'vertices',len(verts),'bounds',r['bounds_m']);print('un-padded frontspan',(raw['front'][:,0].max()-raw['front'][:,0].min())*s,'plan span',np.ptp(raw['plan'][:,1])*s,'side total',np.ptp(raw['side'][:,0])*s,'side height',np.ptp(raw['side'][:,1])*s)
