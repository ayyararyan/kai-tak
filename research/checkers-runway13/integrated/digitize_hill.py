"""Additional observed hill geometry, no interpolation or targetday certification."""
from pathlib import Path
import json,hashlib,numpy as np,zipfile,io
from PIL import Image,ImageDraw
from pyproj import Transformer
R=Path(__file__).resolve().parents[1];G=R/'integrated/geometry';S=R/'integrated/sources'
r=next(x for x in json.loads((R/'reconstruction/block_matching/registered/sheet_registration_inventory.json').read_text())['records'] if x['source_id']=='1980_1990:1292')
core=R/'reconstruction/obstacles/review/11-NW-10D_1989-11_core.png';meta=R/'reconstruction/obstacles/review/11-NW-10D_1989-11_core.json';T=Transformer.from_crs(2326,4326,always_xy=True)
a,b,c,d,e,f=r['affine_pixel_edges'];features=[]
def common(id,meaning):
 return {'id':id,'source_id':r['source_id'],'sheet':r['sheet'],'source_archive':r['source_archive'],'source_sha256':r['source_sha256'],'source_tiff_sha256':r['tiff_sha256'],'edition_month':'1989-11','query_date':'1993-11-04','query_date_presence_certified':False,'vertical_datum':'HKPD','grid_crs':'EPSG:2326','display_geometry_crs':'EPSG:4326','meaning':meaning,'category':'manually interpreted mapped surface observation','physical_horizontal_error_bound_m':None,'physical_height_error_bound_m':None,'physical_upper_bound_m':None,'is_full_structure_top':False,'clearance_eligible':False,'limitations':['Mapedition is not individualsurvey or targetdaypresence date.','Mapped contours/spots do not bound equipment, roofs or intervening unknown terrain.','Digitizingtolerance is not a physical error bound.']}
# Exact source-image lineage of the two inspected labelled contour segments.
p60=np.array([[380,698],[372,650],[380,620],[373,600],[374,560],[375,492],[390,432],[399,383],[420,365],[439,322],[458,307],[489,303],[534,310],[571,312],[604,301],[621,303],[649,325],[678,330],[711,319],[739,294],[778,247],[803,233],[834,234]],float)/4+[1475,670]
p80=np.array([[120,98],[149,142],[191,180],[244,200],[319,216],[388,241],[438,274],[470,307],[486,339],[482,364],[456,399],[425,431],[394,459],[361,482],[321,507],[286,531],[254,556],[219,587],[185,624],[163,650],[146,675]],float)/4+[1385,500]
for height,p in [(60,p60),(80,p80)]:
 en=p*[.25,-.25]+[836750,822200];ll=np.array(T.transform(en[:,0],en[:,1])).T;pr=common(f'hill_contour_{height}_1989','partial mapped terrainisoline, not a closed terrain surface');pr.update(elevation_HKPD_m=height,core_pixel_edge_picks=p.tolist(),EN_m=en.tolist(),source_core=str(core.relative_to(R)),source_core_sha256=hashlib.sha256(core.read_bytes()).hexdigest(),digitizing_pick_tolerance_core_px=1.,digitizing_axis_tolerance_m=.25,interpolation_error_bound_m=None,length_m=float(np.linalg.norm(np.diff(en,axis=0),axis=1).sum()))
 features.append({'type':'Feature','properties':pr,'geometry':{'type':'LineString','coordinates':ll.tolist()}})
# Numerals and actual cross-symbol centres read from ORIGINAL TIFF contact sheet.
centres=json.loads((G/'hill_spot_crop_centres.json').read_text());values={0:58.2,1:59.4,3:73.5,4:None,5:35.7,6:31.4,7:38.4,8:31.4,10:31.7};stars={0:[216,133],1:[416,133],3:[128,333],4:[411,392],5:[732,384],6:[116,640],7:[407,596],8:[733,634],10:[438,824]}
with zipfile.ZipFile(R/r['source_archive']) as z:original=Image.open(io.BytesIO(z.read(r['tiff_member']))).convert('L')
for i,value in values.items():
 centre_core=np.array(centres[i])+[1300,400];cen=centre_core*[.25,-.25]+[836750,822200];src=np.array([(cen[0]-c)/a,(cen[1]-f)/e]);crop_lo=(src+[-105,-82]).astype(int);local=np.array(stars[i])-[300*(i%3),250*(i//3)];px=crop_lo+local/1.4;en=np.array([a*px[0]+c,e*px[1]+f]);ll=T.transform(*en);core_px=(en-[836750,822200])/[.25,-.25]
 cp=S/f'hill_spot_{i}_original.png';original.crop(tuple(crop_lo)+tuple((src+[105,82]).astype(int))).save(cp)
 pr=common(f'hill_surface_spot_{i}_1989','mapped ground/path/playground surface spot; notroof/equipmenttop');pr.update(elevation_HKPD_m=value,source_pixel_edge_pick=px.tolist(),core_pixel_edge_pick=core_px.tolist(),EN_m=en.tolist(),source_symbol='spotheightcross',reading_status='unresolved_digit' if value is None else 'accepted_source_reading',source_crop=str(cp.relative_to(R)),source_crop_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),digitizing_pick_tolerance_source_px=4,digitizing_axis_tolerance_m=4*max(abs(a),abs(e)))
 features.append({'type':'Feature','properties':pr,'geometry':{'type':'Point','coordinates':list(ll)}})
(G/'historical_hill_terrain.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n')
im=Image.open(core).convert('RGB');dr=ImageDraw.Draw(im)
for ftr in features:
 p=ftr['properties']
 if ftr['geometry']['type']=='LineString':
  points=p['core_pixel_edge_picks'];dr.line([tuple(x) for x in points],fill='#b94e26',width=5);dr.text(tuple(np.array(points[len(points)//2])+[8,8]),str(p['elevation_HKPD_m'])+'m contour',fill='#b94e26')
 else:
  x,y=p['core_pixel_edge_pick'];dr.ellipse((x-9,y-9,x+9,y+9),outline='#255f88',width=3);dr.text((x+10,y+4),str(p['elevation_HKPD_m']) if p['elevation_HKPD_m'] is not None else 'unreadable',fill='#255f88')
im.crop((1300,400,2100,1200)).save(G/'hill_terrain_picks.png')
receipt={'source_sha256':r['source_sha256'],'inspected_original_contact':'integrated/sources/hill_additional_spots_original.png','accepted_spot_readings':{k:v for k,v in values.items() if v is not None},'excluded_unresolved_readings':{'2':'lastdigitambiguous; no numeric value exported','4':'final digit intersects contour; top remains null','9':'middle digit ambiguous; no numeric value exported'},'contour_labels_read':[60,80],'contour_geometry_scope':'two partial traces; no contourclosure or terraininterpolation','new_complete_historical_volumes':0,'new_hard_upper_height_bounds':0}
(G/'hill_terrain_inspection.json').write_text(json.dumps(receipt,indent=2)+'\n');print('8numericgroundspots,1unresolvedreading,2partialcontours; nohardbounds');print('Contourlengths',[f['properties'].get('length_m') for f in features[:2]])
