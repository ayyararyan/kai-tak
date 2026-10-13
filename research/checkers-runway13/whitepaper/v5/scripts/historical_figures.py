"""V5 evidence-led historical illustrations. Source bytes stay unmodified.

The aircraft-model trajectory is never placed onto a photograph or historical map.
PLY faces are the accepted open surface: no remeshing, hole filling or extrusion.
"""
import argparse, csv, json, math
from pathlib import Path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Arc, Circle
from matplotlib.collections import PolyCollection
from figure_style import P, INK, SLATE, COPPER, SAGE, PALE, LIGHT, BLUE, bare, label, arrow, save, read, rows
H='inputs/historical/'

def photo(fig, rect, name, crop):
    ax=fig.add_axes(rect)
    # Convert only the displayed copy; the hash-bound archival input is intact.
    a=np.asarray(Image.open(P/name).convert('L'))
    x0,y0,x1,y1=crop
    ax.imshow(a[y0:y1,x0:x1],cmap='gray',extent=(x0,x1,y1,y0),interpolation='lanczos')
    ax.set_xlim(x0,x1);ax.set_ylim(y1,y0);bare(ax)
    return ax

def leader(ax,text,xy,at,ha='left',color=INK,size=12.5):
    # Small borderless white backing protects labels over real image texture.
    a=ax.annotate(text,xy=xy,xytext=at,ha=ha,va='center',fontsize=size,color=color,
      arrowprops={'arrowstyle':'-','color':color,'lw':.7,'shrinkB':2,'shrinkA':4},bbox={'fc':'white','ec':'none','pad':1.5,'alpha':.87},clip_on=False)
    return a

def place():
    fig=plt.figure(figsize=(7.1,5.4))
    # The airport dominates. The two independent October frames provide the
    # hillside reference and water-bound runway end missing from that scan.
    ax=photo(fig,[.035,.165,.57,.75],'inputs/A36143.jpg',(120,100,2890,2780))
    leader(ax,'Kowloon City',(1210,610),(650,290),ha='center')
    leader(ax,'Runway 13\nthreshold',(820,1745),(280,1410))
    leader(ax,'Kai Tak Airport',(1760,2070),(1950,2540),ha='center')
    fig.text(.036,.955,'THE CITY AT THE THRESHOLD',fontsize=12.5,weight='bold',color=INK)
    fig.text(.036,.115,'A36143  ·  November 1993*',fontsize=11.5,color=SLATE)
    ah=photo(fig,[.64,.56,.325,.345],H+'CN4581.jpg',(300,1070,1750,2200))
    leader(ah,'Checkerboard\nHill',(1075,1310),(1180,1120),ha='center',size=12)
    fig.text(.64,.525,'CN4581  ·  8 October 1993',fontsize=11.1,color=SLATE)
    ab=photo(fig,[.64,.165,.325,.345],H+'CN4589.jpg',(300,450,2100,2140))
    leader(ab,'Kowloon Bay',(1010,1610),(1490,1970),ha='center',size=12)
    leader(ab,'Runway end',(695,1200),(1470,570),ha='center',size=12)
    fig.text(.64,.115,'CN4589  ·  8 October 1993',fontsize=11.1,color=SLATE)
    fig.text(.036,.050,'Separate source views; original scan perspectives.',fontsize=11.5,color=SLATE)
    fig.text(.036,.016,'*Catalogue: 2 November. Handwritten frame label: apparently 3 November.',fontsize=10.4,color=SLATE)
    save(fig,'01_place',['inputs/A36143.jpg','inputs/A36143_product.json',H+'CN4581.jpg',H+'CN4589.jpg',H+'SOURCE_MANIFEST.json'],
      'The real airport, Checkerboard Hill and Kowloon Bay in separate historical source photographs',
      image_operations='Source crops only; no stitching, geometric registration, synthetic scenery or flight overlay.',
      crop_pixels={'A36143':[120,100,2890,2780],'CN4581':[300,1070,1750,2200],'CN4589':[300,450,2100,2140]},
      source_date_discrepancy='A36143 catalogue 1993-11-02; handwritten border appears 3.11.93; unresolved',
      annotation_basis='Visually inspected physical features, not measured geographic coordinates')

def bearings():
    fig=plt.figure(figsize=(7.1,5.0))
    ax=fig.add_axes([.025,.12,.95,.85]);bare(ax)
    ax.set(xlim=(0,11),ylim=(0,7.5),aspect='equal')
    ax.text(.15,7.23,'TWO DIRECTIONS IN ONE LANDSCAPE',fontsize=12.5,weight='bold')
    ax.text(.15,6.76,'Geographic relations schematic · not a navigational chart',fontsize=11,color=SLATE)
    # The map remains a bounded source fragment. Positions outside its border
    # encode approximate relative place only; there is no aerial registration.
    im=np.asarray(Image.open(P/'inputs/11-NE-11A_1989-10_core.png').convert('L'))
    ax.imshow(im,cmap='gray',extent=(2.8,7.5,1.65,5.41),alpha=.57,zorder=0)
    ax.add_patch(Rectangle((2.8,1.65),4.7,3.76,fill=False,ec=LIGHT,lw=.65))
    ax.text(5.15,1.35,'Kowloon City',fontsize=12,ha='center')
    ax.text(5.15,1.00,'1989 survey-map fragment',fontsize=10.5,ha='center',color=SLATE)
    ax.scatter([2.35],[5.85],s=32,color=COPPER,zorder=3)
    ax.text(2.25,6.2,'Checkerboard Hill',ha='center',fontsize=12)
    # All orientation guides are constructed rays. Their intersection is not
    # an inferred historical turning location or a route on the map.
    o=np.array([5.35,5.7]);uig=np.array([np.sin(np.deg2rad(88)),np.cos(np.deg2rad(88))]);ur=np.array([np.sin(np.deg2rad(135)),np.cos(np.deg2rad(135))])
    arrow(ax,o-4.85*uig,o-.12*uig,lw=1.6,color=INK,head=11)
    ax.plot([o[0],o[0]+2.75*uig[0]],[o[1],o[1]+2.75*uig[1]],color=SLATE,lw=.8,dashes=(4,3))
    ax.text(.15,4.60,'IGS direction\n088° magnetic',fontsize=12.2,color=INK)
    # Runway strip lies southeast, consistent with the source-place relation.
    start=o+ur*2.1; end=o+ur*5.45;normal=np.array([-ur[1],ur[0]])
    corners=np.array([start+normal*.17,end+normal*.17,end-normal*.17,start-normal*.17])
    ax.add_patch(Polygon(corners,fc=INK,ec='white',lw=.8,zorder=4))
    ax.plot([start[0],end[0]],[start[1],end[1]],color='white',lw=.7,dashes=(4,3),zorder=5)
    ax.plot([o[0],start[0]],[o[1],start[1]],color=COPPER,lw=1.2,dashes=(4,3),zorder=5)
    ax.add_patch(Arc(o,2.5,2.5,theta1=-45,theta2=2,ec=COPPER,lw=1.2,zorder=6))
    ax.text(o[0]+1.35,o[1]-.45,'47°',fontsize=24,color=COPPER,zorder=6)
    ax.text(9.7,3.2,'Runway 13\n135° magnetic',fontsize=12.2,ha='center')
    ax.text(9.1,.83,'Kowloon Bay',fontsize=12,color=BLUE,ha='center')
    arrow(ax,(10.05,5.5),(10.05,6.3),color=SLATE,lw=.8,head=8)
    ax.text(10.05,6.5,'Magnetic N',fontsize=10.7,ha='center')
    ax.text(.10,2.80,'The turn belongs to\nthe visual segment.',fontsize=12,color=INK)
    ax.text(.10,1.65,'Dashed rays compare\ndirections only.',fontsize=11.1,color=SLATE)
    fig.text(.04,.045,'47° is a change of direction, not a wing-bank angle.',fontsize=12,color=INK)
    save(fig,'02_bearings',['inputs/11-NE-11A_1989-10_core.png','inputs/11-NE-11A_1989-10_core.json',H+'landmark_frame_matches.csv','evidence/evidence/cal605_reconstruction/analysis.json'],
      'The 47-degree difference drawn as direction guides in a geographic-relations schematic',
      geometry_status='Diagrammatic geographic relations, not to scale. Map fragment, landmark, construction origin and runway symbol are not registered. Rays compare magnetic bearings; no historical route, beam position or turning point inferred.',
      bearing_sources='CAD Report 1/95 sections 1.8.1, 1.10 and Appendix 1; unchanged V4 factual bearing transcription',
      bearing_values={'IGS_degM':88,'runway_degM':135,'difference_deg':47},
      source_note='Genuine 1989 source-map fragment; approximate source acquisition anchors support northwest/southeast relation only.')

def load_mesh():
    fn=P/(H+'observed_surface_mesh.ply')
    with fn.open() as f:
      nv=nf=0
      while True:
        line=f.readline()
        if line.startswith('element vertex'):nv=int(line.split()[-1])
        if line.startswith('element face'):nf=int(line.split()[-1])
        if line.strip()=='end_header':break
      v=np.loadtxt([next(f) for _ in range(nv)])
      ff=np.loadtxt(f,dtype=np.int64)
    assert (nv,nf)==(155891,225371)
    assert ff.shape==(nf,5) and np.all(ff[:,0]==3)
    return v,ff[:,1:4]

def project(v,az=-33,elev=32):
    # Orthonormal camera basis: equal metric scale in every direction.
    a=np.deg2rad(az);e=np.deg2rad(elev)
    right=np.array([np.cos(a),np.sin(a),0.])
    depth=np.array([np.sin(a)*np.cos(e),-np.cos(a)*np.cos(e),np.sin(e)])
    up=np.cross(depth,right)
    basis=np.stack([right,up,depth])
    assert np.allclose(basis@basis.T,np.eye(3),atol=1e-12) and up[2]>0 and depth[2]>0
    return np.column_stack([v@right,v@up]),v@depth

def stereo():
    fig=plt.figure(figsize=(7.1,7.0))
    fig.text(.035,.969,'TWO PHOTOGRAPHS ACQUIRE DEPTH',fontsize=12.5,weight='bold')
    labels=read(H+'manual_stereo_labels.json')['labels']
    matches=[next(x for x in labels if x['fundamental_inlier_row']==n) for n in [26,1135,788]]
    crops={'A36142':(2010,1300,2530,1850),'A36143':(2010,560,2530,1110)}
    for frame,rect in [('A36142',[.04,.680,.425,.255]),('A36143',[.535,.680,.425,.255])]:
      ax=photo(fig,rect,H+frame+'.jpg' if frame=='A36142' else 'inputs/A36143.jpg',crops[frame])
      for r,s in zip(matches,['R','S','G']):
        x,y=r['frame'+frame[-2:]+'_xy'];ax.scatter([x],[y],s=55,fc='white',ec=COPPER,lw=1,zorder=3)
        ax.text(x+15,y-16,s,color=COPPER,fontsize=11.5,weight='bold',zorder=4)
      ax.text(.02,1.03,frame,transform=ax.transAxes,fontsize=12,color=SLATE)
    fig.text(.50,.650,'R  market roof       S  rooftop structure       G  paved-path junction',ha='center',fontsize=11.3)
    v,faces=load_mesh();xyz=v[:,:3]-np.array([837500.,821000.,0.]);uv,depth=project(xyz)
    order=np.argsort(depth[faces].mean(axis=1))
    # Original image radiometry modulated mildly by surface-normal lighting.
    tri=xyz[faces];n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);ln=np.linalg.norm(n,axis=1);n/=np.maximum(ln[:,None],1e-12)
    n*=np.where(n[:,2:3]<0,-1,1)
    light=np.array([-.30,-.40,.866]);illum=.70+.30*np.clip(n@light,0,1)
    gray=v[:,3:6].mean(axis=1)[faces].mean(axis=1)/255
    # Original gray imagery, lifted for print; no geometric smoothing.
    val=np.clip(.07+.60*gray,0,1)*illum
    rgba=np.column_stack([val,val,val,np.ones(len(val))])
    ax=fig.add_axes([.03,.227,.70,.388]);bare(ax)
    ax.add_collection(PolyCollection(uv[faces][order],facecolors=rgba[order],edgecolors='none',rasterized=True))
    rrs=rows(H+'sparse_stereo_points.csv'); market=next(r for r in rrs if r['track_id']=='26'); mxyz=np.array([[float(market['easting_hk1980_m'])-837500,float(market['northing_hk1980_m'])-821000,float(market['z_above_fitted_local_park_road_plane_m'])]]); muv,_=project(mxyz); ax.scatter(muv[:,0],muv[:,1],s=25,fc='white',ec=COPPER,lw=1,zorder=5); label(ax,'Market roof',muv[0],(muv[0,0]+200,muv[0,1]+100),color=COPPER,size=11)
    ax.set_xlim(uv[:,0].min()-25,uv[:,0].max()+25);ax.set_ylim(uv[:,1].min()-25,uv[:,1].max()+25);ax.set_aspect('equal')
    ax.text(.00,1.0,'ROOFS AND ROADS, WITH GAPS',transform=ax.transAxes,fontsize=11.5,weight='bold')
    ax.text(.00,-.045,'True metre scale in all directions; gaps left open.',transform=ax.transAxes,fontsize=11.1,color=SLATE)
    # True control polygon in a distinct plan, never a filled accuracy region.
    bx=fig.add_axes([.75,.248,.215,.34]);bare(bx)
    rr=rows('evidence/stereo_plot_data.csv');en=np.array([[float(r['easting_hk1980_m']),float(r['northing_hk1980_m'])] for r in rr])-np.array([837500,821000])
    bx.scatter(en[:,0],en[:,1],s=.16,c=LIGHT,rasterized=True)
    hull=np.array(read(H+'registration.json')['support_polygon_hk1980']['coordinates'][0])-np.array([837500,821000])
    bx.add_patch(Polygon(hull,fc=COPPER,alpha=.65,ec=COPPER,lw=1))
    bx.set_aspect('equal');bx.text(.5,1.06,'CONTROL SUPPORT',transform=bx.transAxes,ha='center',fontsize=10.5,weight='bold')
    bx.text(.5,-.07,'3,780 / 171,307\npoints within hull',transform=bx.transAxes,ha='center',fontsize=11.1,color=COPPER)
    # Third stage: a real dated map fragment and accepted conditional heights.
    mx=photo(fig,[.04,.035,.255,.162],'inputs/11-NE-11A_1989-10_core.png',(0,1360,660,1970))
    fig.text(.335,.162,'A mapped identity: Kowloon City Market',fontsize=11.8,weight='bold')
    fig.text(.335,.132,'R  roof feature: 10.77 m above fitted plane',fontsize=11.3)
    fig.text(.335,.091,'S  rooftop structure: 19.20 m above fitted plane',fontsize=11.3)
    fig.text(.335,.046,'Conditional stereo heights; no absolute roof datum.',fontsize=10.7,color=SLATE)
    fig.text(.335,.016,'Both labelled roof features lie outside the control hull.',fontsize=10.4,color=COPPER)
    for track in ['26','1135']:
      assert next(r for r in rrs if r['track_id']==track)['within_map_control_hull']=='False'
    save(fig,'07_stereo',['inputs/A36143.jpg',H+'A36142.jpg',H+'observed_surface_mesh.ply',H+'manual_stereo_labels.json',H+'sparse_stereo_report.json',H+'sparse_stereo_points.csv',H+'registration.json','inputs/11-NE-11A_1989-10_core.png','inputs/historical_faces.geojson','evidence/stereo_plot_data.csv'],
      'Matched source photographs, an actual open stereo surface and a dated map-form identity',
      mesh_vertices=len(v),mesh_faces=len(faces),surface_operations='Orthonormal true-scale projection; original triangle topology and pixel luminance; normal-based mild lighting only; no remeshing, gap filling, capping, extrusion or vertical exaggeration.',
      projection={'azimuth_deg':-33,'elevation_deg':32,'equal_metric_scale_xyz':True,'camera_up_z':float(np.cos(np.deg2rad(32))),'camera_above_scene':True},
      crop_pixels=crops,vertical_reference='Fitted local park/road plane, not HKPD and not height above local building ground',
      named_heights={'26':10.769431630259533,'1135':19.195490912459263},
      dense_counts={'retained':171307,'inside_control_hull':3780},
      map_fragment='October 1989 survey sheet 11-NE-11A; geographic identity lead, not proved unchanged 1993 building')

def maps():
    fig=plt.figure(figsize=(7.1,6.15))
    fig.text(.035,.962,'OCTOBER 1989',fontsize=12.5,weight='bold')
    fig.text(.72,.962,'Sheet 11-NE-11A',fontsize=11,color=SLATE,ha='right')
    ax=photo(fig,[.035,.397,.675,.53],'inputs/11-NE-11A_1989-10_core.png',(0,0,3000,2400))
    faces=read('inputs/historical_faces.geojson')['features']
    sites=[('shing_tung','Shing Tung\nHouse',(820,0,1420,600)),('regal','Regal Airport\nHotel',(1500,1300,2100,1900)),('city_market','Kowloon City\nMarket',(0,1430,600,2030))]
    for i,(key,name,crop) in enumerate(sites):
      r=next(f for f in faces if f['properties']['id']==key and f['properties']['source_epoch']=='1989-10')['properties']
      xy=((r['seed_e']-837500)/.25,(821600-r['seed_n'])/.25)
      x0,y0,x1,y1=crop
      ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,ec=COPPER,lw=.8))
      ax.scatter([xy[0]],[xy[1]],s=17,color=COPPER,zorder=4)
      # Named outside locators avoid hiding the map's own printed labels.
      ay=[250,1240,2220][i]
      label(ax,name,xy,(3270,ay),color=INK,size=11.7)
    ax.plot([2050,2450],[2240,2240],color=INK,lw=1.7)
    ax.text(2250,2180,'100 m',ha='center',fontsize=10.8,color=INK)
    arrow(ax,(2780,510),(2780,180),color=INK,lw=.8,head=8)
    ax.text(2780,100,'Grid N',ha='center',fontsize=10.8)
    fig.text(.035,.347,'JULY 1994 · the same three map windows',fontsize=12.0,weight='bold')
    # Identical source-pixel crop widths and identical physical axes: all three
    # detail windows have the same 150m ground-width scale.
    for i,(key,name,crop) in enumerate(sites):
      xx=.035+i*.323
      axd=photo(fig,[xx,.050,.286,.264],'inputs/11-NE-11A_1994-07_core.png',crop)
      axd.text(.5,-.085,name.replace('\n',' '),ha='center',va='top',transform=axd.transAxes,fontsize=10.9)
      for sp in axd.spines.values():sp.set_visible(True);sp.set_color(LIGHT);sp.set_linewidth(.65)
    save(fig,'06_maps',['inputs/11-NE-11A_1989-10_core.png','inputs/11-NE-11A_1989-10_core.json','inputs/11-NE-11A_1994-07_core.png','inputs/11-NE-11A_1994-07_core.json','inputs/historical_faces.geojson'],
      'A 1989 survey field locates three named forms; matched 150-metre windows show their 1994 map depiction',
      main_extent_EPSG2326=[837500,821000,838250,821600],registered_pixel_spacing_m=.25,
      positional_accuracy='Unspecified; raster spacing is not an accuracy bound',
      detail_crop_pixels={key:crop for key,name,crop in sites},detail_width_m=150,
      historical_status='Mapped forms at separate edition epochs; unchanged presence, identity and height in1993 are not inferred',
      image_operations='Source raster crops only; no erased or invented linework. Main-map rectangles identify exact later-edition crop extents.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--prototypes',action='store_true');p.add_argument('--only',choices=['place','bearings','stereo','maps']);args=p.parse_args()
    calls={'place':place,'bearings':bearings,'stereo':stereo,'maps':maps}
    for key,fn in calls.items():
      if args.prototypes and key=='maps':continue
      if args.only is None or args.only==key:fn();print('Rendered',key,flush=True)
if __name__=='__main__':main()
