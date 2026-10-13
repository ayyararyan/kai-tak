from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
from pyproj import Transformer
R=Path(__file__).resolve().parents[1];O=R/'integrated/geometry'
rs=json.loads((R/'reconstruction/block_matching/registered/sheet_registration_inventory.json').read_text())['records'];r=next(v for v in rs if v['source_id']=='1980_1990:1011')
# manual centreline picks of visibly mapped outer seawall; displayed at1200px width
p=np.array([[0,575],[180,782],[221,808],[259,824],[302,826],[350,820],[400,794],[447,759],[970,210],[1017,154],[1038,120],[1039,73],[1031,22],[1018,0]],float)/3+[700,300]
source=p*r['width']/1200;a,b,c,d,e,f=r['affine_pixel_edges'];en=np.c_[a*source[:,0]+b*source[:,1]+c,d*source[:,0]+e*source[:,1]+f]
ll=np.array(Transformer.from_crs(2326,4326,always_xy=True).transform(en[:,0],en[:,1])).T
props={'id':'seawall_SE_1993_08','source_id':r['source_id'],'sheet':r['sheet'],'source_archive':r['source_archive'],'source_sha256':r['source_sha256'],'source_tiff':r['tiff_member'],'edition_month':'1993-08','query_date':'1993-11-04','query_date_presence_certified':False,'meaning':'digitized detailed partial outer seawall edge, not complete coastline/landmask or aircraft obstacle solid','category':'deterministically derived from manually interpreted source outer edge','source_pixel_edge_picks':source.tolist(),'pick_tolerance_display_px':3,'pick_tolerance_grid_axis_m':3*r['width']/1200*max(abs(a),abs(e)),'physical_horizontal_error_bound_m':None,'top_height_HKPD_m':None,'physical_height_bound_m':None,'clearance_eligible':False,'crs_source_geometry':'EPSG:2326','EN_m':en.tolist(),'limitations':['Interpolation joins sampled mapped seawallline only','No walltop elevation, sea-surface law or hard spatial bound','Map edition and photo appearance do not certify target-day wall volume']}
fc={'type':'FeatureCollection','features':[{'type':'Feature','properties':props,'geometry':{'type':'LineString','coordinates':ll.tolist()}}]};(O/'historical_seawall.geojson').write_text(json.dumps(fc,indent=2)+'\n')
lightuv=np.array([[676,560],[896,699],[860,737],[822,776]],float)/3+[700,300]
lightpx=lightuv*r['width']/1200
lighten=np.c_[a*lightpx[:,0]+c,e*lightpx[:,1]+f]
lightll=np.array(Transformer.from_crs(2326,4326,always_xy=True).transform(lighten[:,0],lighten[:,1])).T
features=[]
for i in range(4):
 pr=dict(props,id='SE_approach_light_'+str(i),meaning='mapped approach light/strobe symbol, not surveyed extent or top',source_pixel_edge_picks=[lightpx[i].tolist()],EN_m=lighten[i].tolist(),symbol='approachlight and strobelight' if i==0 else 'approachlight',horizontal_extent_m=None)
 features.append({'type':'Feature','properties':pr,'geometry':{'type':'Point','coordinates':lightll[i].tolist()}})
(O/'historical_approach_lights.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n')
im=Image.open(O/'sheet_1011.png').convert('RGB');dr=ImageDraw.Draw(im);scale=im.width/1200;dr.line([tuple(v*scale) for v in p],fill='#b34e25',width=3)
for i,v in enumerate(p*scale):dr.ellipse((v[0]-5,v[1]-5,v[0]+5,v[1]+5),fill='#b34e25');dr.text(tuple(v+[8,0]),str(i),fill='#b34e25')
im.save(O/'seawall_source_picks.png');print('source-bound shoreline vertices',len(p),'digitizing tolerance',props['pick_tolerance_grid_axis_m'],'m peraxis, NOT ground error bound')
