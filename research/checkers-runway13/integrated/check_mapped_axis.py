from pathlib import Path
import cv2,numpy as np,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];G=R/'integrated/geometry';p=G/'south_runway_map.png';im=np.array(Image.open(p).convert('L'));edges=cv2.Canny(im,70,150);lines=cv2.HoughLinesP(edges,1,np.pi/3600,threshold=100,minLineLength=250,maxLineGap=20);out=[]
for row in np.asarray(lines).reshape(-1,4):
 x1,y1,x2,y2=map(int,row)
 if x2<x1:x1,y1,x2,y2=x2,y2,x1,y1
 dx=x2-x1;dy=y2-y1;ang=np.degrees(np.arctan2(dx,-dy))%360;l=np.hypot(dx,dy)
 if 125<ang<145:out.append({'pixels':[x1,y1,x2,y2],'length_px':float(l),'grid_bearing_deg':float(ang)})
out=sorted(out,key=lambda x:-x['length_px'])[:20];pic=Image.open(p).convert('RGB');dr=ImageDraw.Draw(pic)
for i,v in enumerate(out):
 a=v['pixels'];dr.line(a,fill='red' if i<10 else 'blue',width=2);dr.text(((a[0]+a[2])/2,(a[1]+a[3])/2),str(i),fill='red')
pic.save(G/'mapped_axis_candidates.png');(G/'mapped_axis_candidates.json').write_text(json.dumps({'method':'Houghline candidates only; sourceidentity requiresvisualinspection','pixel_scale_m':1,'lines':out},indent=2)+'\n');print(json.dumps(out,indent=2))
# Second candidate pass joins longer source fragments; it deliberately does NOT
# certify line identity. The selected edges live in an explicit reviewed record.
lines=cv2.HoughLinesP(edges,1,np.pi/3600,threshold=60,minLineLength=200,maxLineGap=80);candidates=[]
for row in np.asarray(lines).reshape(-1,4):
 x,y,X,Y=map(int,row)
 if X<x:x,y,X,Y=X,Y,x,y
 if X==x:continue
 m=(Y-y)/(X-x);theta=np.degrees(np.arctan2(X-x,y-Y))%360;intercept=y-m*x
 if 133.6<theta<134.4 and 60<intercept<270:candidates.append({'px':[x,y,X,Y],'length':float(np.hypot(X-x,Y-y)),'bearing':float(theta),'intercept':float(intercept)})
candidates=sorted(candidates,key=lambda x:-x['length'])[:12];(G/'mapped_runway_edge_candidates.json').write_text(json.dumps(candidates,indent=2)+'\n')
pic=Image.open(p).convert('RGB');dr=ImageDraw.Draw(pic)
for i,v in enumerate(candidates):
 a=v['px'];dr.line(a,fill='red',width=2);dr.text(((a[0]+a[2])/2,(a[1]+a[3])/2-15),str(i),fill='red')
pic.save(G/'mapped_runway_edge_candidates.png')
