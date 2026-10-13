#!/usr/bin/env python3
"""Compose public captions/comparisons, retaining separate epochs and source frames."""
from pathlib import Path
import json,math,csv,hashlib,textwrap,html,os
from PIL import Image,ImageDraw,ImageFont,PngImagePlugin,ImageOps
A=Path(__file__).resolve().parents[1];R=A.parents[1]/'research/checkers-runway13';W,H=3840,2160
IVORY='#f3f0e8';INK='#263c41';MUTED='#586e70';ACCENT='#a8653e';SLATE='#24383e'
fontroot=Path('/System/Library/Fonts/Supplemental')
def font(n=36,serif=False):
 candidates=[os.environ.get('ATLAS_SERIF_FONT' if serif else 'ATLAS_SANS_FONT',''),str(fontroot/('Baskerville.ttc' if serif else 'Arial.ttf')),'/usr/share/fonts/truetype/dejavu/'+('DejaVuSerif.ttf' if serif else 'DejaVuSans.ttf')]
 for p in candidates:
  if p and Path(p).exists():return ImageFont.truetype(p,n)
 raise RuntimeError('Set ATLAS_SERIF_FONT and ATLAS_SANS_FONT to installed fonts')
def wrapped(draw,text,xy,width,size=37,color=INK,leading=1.3):
 f=font(size);words=text.split();lines=[];cur=''
 for w in words:
  q=(cur+' '+w).strip()
  if draw.textlength(q,font=f)>width and cur:lines.append(cur);cur=w
  else:cur=q
 if cur:lines.append(cur)
 for i,l in enumerate(lines):draw.text((xy[0],xy[1]+i*size*leading),l,font=f,fill=color)
 return xy[1]+len(lines)*size*leading

def digest(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest=json.loads((A/'metadata/input_manifest.json').read_text())
for rec in manifest['files']:
 if rec['available']:assert digest(A.parents[1]/rec['path'])==rec['sha256'], 'Changed source: '+rec['path']
for asset,h in json.loads((A/'metadata/render_jobs.json').read_text())[0]['asset_hashes'].items():assert digest(asset)==h, 'Changed derived asset: '+asset
assert json.loads((A/'metadata/rights.json').read_text())['A36143']['distribution']=='permitted_with_attribution', 'Photo rights not approved in register'
def read(name):
 p=A/f'renders/master/{name}.png';rec=json.loads(p.with_suffix('.render.json').read_text())
 assert digest(p)==rec['output_sha256'], 'Changed render: '+name
 job=A/f'scenes/jobs/{name}.json';assert rec['source_sha256'][str(job)]==digest(job), 'Stale job: '+name
 return Image.open(p).convert('RGB')
def fit(canvas,im,rect):
 x,y,w,h=rect;small=ImageOps.contain(im,(int(w),int(h)),Image.Resampling.LANCZOS);px=int(x+(w-small.width)/2);py=int(y+(h-small.height)/2);canvas.paste(small,(px,py));return px,py,small.width/im.width

def mark(draw,x,y,label,r=26):
 draw.ellipse((x-r,y-r,x+r,y+r),fill=ACCENT,outline=IVORY,width=4);draw.text((x,y),str(label),font=font(30),fill='white',anchor='mm')
def projected_panel(canvas,name,rect):
 im=read(name);d=ImageDraw.Draw(im);rec=json.loads((A/f'renders/master/{name}.render.json').read_text())
 px,py,scale=fit(canvas,im,rect)
 for p in rec['projected_marks']:mark(ImageDraw.Draw(canvas),px+p['x']*scale,py+p['y']*scale,p['label'],34)
 return px,py,scale
def metadata(item):
 m=PngImagePlugin.PngInfo()
 for k in ['title','epoch','mode','type','caption','limit']:m.add_text(k,item[k])
 m.add_text('Attribution','Lands Department and Buildings Department, HKSAR Government; CSDI; DATA.GOV.HK. Research and visualization: Aryan Ayyar.')
 return m

def comparison(items,labels):
 c=Image.new('RGB',(W,H),IVORY);d=ImageDraw.Draw(c)
 if len(items)==4:
  for n,(name,label) in enumerate(zip(items,labels)):
   x=50+(n%2)*1900;y=25+(n//2)*1070;fit(c,read(name),(x,y+80,1840,960));d.text((x+25,y+15),label,font=font(48,True),fill=INK)
 else:
  for n,(name,label) in enumerate(zip(items,labels)):
   x=60+n*1900;fit(c,read(name),(x,260,1820,1580));d.text((x+15,160),label,font=font(59,True),fill=INK)
 return c

def photograph_panel(with_marks=True):
 original=Image.open(R/'reconstruction/chronology/aerial/fullframes/A36143.jpg').convert('RGB');w,h=original.size
 im=original.transpose(Image.Transpose.ROTATE_90);box=(600,480,1200,1050);im=im.crop(box);d=ImageDraw.Draw(im)
 for row in csv.DictReader((R/'reconstruction/block_matching/aerial_registration/sparse_stereo_points.csv').open()):
  labels={'26':'1','708':'2','1135':'3'}
  if with_marks and row['track_id'] in labels:
   x=float(row['frame43_y'])-box[0];y=w-1-float(row['frame43_x'])-box[1];mark(d,x,y,labels[row['track_id']],17)
 return im

def locator(labels=True):
 c=Image.new('RGB',(1100,1450),IVORY);d=ImageDraw.Draw(c)
 def xy(e,n):return (100+(e+600)*(880/3700),130+(1400-n)*(880/3700))
 # Exact source-local coordinate positions; simple cartographic relationship only.
 g=json.loads((A/'assets/hill.json').read_text());pts=[p for f in g['features'] for p in f['coordinates']];e=sum(p[0] for p in pts)/len(pts);n=sum(p[1] for p in pts)/len(pts);x,y=xy(e,n)
 d.ellipse((x-14,y-14,x+14,y+14),fill=ACCENT)
 for f in json.loads((A/'assets/geography.json').read_text())['features']:
  if f['type']=='polyline':d.line([xy(p[0],p[1]) for p in f['coordinates']],fill=ACCENT if f['material']=='accent' else MUTED,width=6)
 if labels:
  d.text((x+30,y-20),'HILL REGION',font=font(32),fill=INK);d.text((530,820),'1993 RUNWAY EDGES',font=font(30),fill=INK)
  d.line((910,290,910,150),fill=INK,width=4);d.polygon([(910,135),(900,160),(920,160)],fill=INK);d.text((855,85),'GRID N',font=font(28),fill=INK)
  x0,y0=xy(-300,-2600);x1,y1=xy(200,-2600);d.line((x0,y0,x1,y1),fill=INK,width=5);d.text((x0,y0+22),'500 m',font=font(28),fill=INK)
  wrapped(d,'No inferred track. Land surface and painted checkerboard position unresolved.',(85,1300),930,27)
 return c

def raw_composite(it):
 n=it['id']
 if n=='09':return comparison(['map-1989-10','03-city-beneath','map-1994-07','map-1997-04'],['OCTOBER 1989 · MAP','NOVEMBER 1993 · PARTIAL SURFACE','JULY 1994 · MAP','APRIL 1997 · MAP'])
 if n=='10':return comparison(['01-grand-overview','10-modern-airport'],['1986–1993 · DOCUMENTED AIRPORT','SEPTEMBER 2026 · CURRENT BUILDINGS'])
 if n=='04':
  c=Image.new('RGB',(W,H),IVORY);d=ImageDraw.Draw(c)
  fit(c,read('04-hill-observations'),(20,500,1150,1000));fit(c,read('04-hill-context'),(1220,500,1150,1000));fit(c,locator(True),(2490,330,1250,1550))
  for x,t in [(80,'1989 · MAPPED HEIGHTS'),(1260,'2014–2015 · TERRAIN'),(2540,'GEOGRAPHIC RELATIONSHIP')]:d.text((x,210),t,font=font(40),fill=INK)
  wrapped(d,'Historical observations and later terrain are separate panels. The location diagram identifies the hill region, not a surveyed position of the painted board.',(140,1910),3500,42)
  return c
 if n=='11':
  c=Image.new('RGB',(W,H),IVORY);d=ImageDraw.Draw(c)
  fit(c,photograph_panel(),(65,350,1190,1300));projected_panel(c,'11-surface-top',(1325,350,1190,1300));projected_panel(c,'11-map-top',(2585,350,1190,1300))
  for x,t in [(75,'01  THE PHOTOGRAPH'),(1335,'02  THE OBSERVED SURFACE'),(2595,'03  THE MAP CONTEXT')]:d.text((x,190),t,font=font(45),fill=INK)
  for x,t in [(75,'A36143 · rotated toward north, not an orthophoto'),(1335,'Same source tracks · 1993 relative-height mesh'),(2595,'October 1989 map · geographic positions')]:wrapped(d,t,(x,1740),1130,35)
  wrapped(d,'1  North market roof     2  Carpenter Road ground track     3  South market roof',(160,1950),3500,43)
  return c
 if n=='06':
  c=Image.new('RGB',(W,H),IVORY);fit(c,read('06-final-alignment'),(0,0,2300,2160));d=ImageDraw.Draw(c);cx,cy=2700,1050;rad=620
  d.text((2310,340),'A change of direction',font=font(72,True),fill=INK)
  for deg,label,col in [(88,'088° magnetic',MUTED),(135,'135° magnetic',ACCENT)]:
   ang=math.radians(deg);ex=cx+rad*math.sin(ang);ey=cy-rad*math.cos(ang);d.line((cx,cy,ex,ey),fill=col,width=13)
   ux,uy=math.sin(ang),-math.cos(ang);d.polygon([(ex,ey),(ex-55*ux+25*uy,ey-55*uy-25*ux),(ex-55*ux-25*uy,ey-55*uy+25*ux)],fill=col);d.text((ex-220,ey+65),label,font=font(46),fill=col)
  d.arc((cx-330,cy-330,cx+330,cy+330),-2,45,fill=ACCENT,width=9);d.text((cx+390,cy+85),'47°',font=font(100,True),fill=ACCENT)
  wrapped(d,'Schematic only. These arrows use magnetic north; the adjacent map uses grid north. No geographical flight path is drawn.',(2320,1640),1300,43)
  return c
 if n=='12':
  c=read('12-panorama');inset=read('01-grand-overview');fit(c,inset,(2680,1320,1090,680));d=ImageDraw.Draw(c);d.rectangle((2670,1290,3780,2020),outline='#d9d7ca',width=3);d.text((2720,1320),'AIRPORT MAP · SEPARATE VIEW',font=font(30),fill=IVORY);return c
 im=read(it['source_render'])
 if n=='03':
  d=ImageDraw.Draw(im);m=json.loads((A/'renders/master/03-city-beneath.render.json').read_text())['projected_marks'];p,q=m;d.line((p['x'],p['y'],q['x'],q['y']),fill=IVORY,width=8);d.text((p['x'],p['y']+30),'100 m horizontal',font=font(38),fill=IVORY)
 if n in ['01','02']:
  d=ImageDraw.Draw(im);rec=json.loads((A/f'renders/master/{it['source_render']}.render.json').read_text())
  for p in rec['projected_marks']:
   x,y=p['x'],p['y'];text=p['label'];f=font(44);tw=d.textlength(text,font=f)
   x=max(50,min(x-tw/2,W-tw-65));y=max(70,min(y,H-100))
   d.rounded_rectangle((x-16,y-12,x+tw+16,y+62),radius=8,fill=IVORY);d.text((x,y),text,font=f,fill=INK)
 return im

def clean_composite(it):
 n=it['id'];c=Image.new('RGB',(W,H),IVORY)
 if n=='04':
  fit(c,read('04-hill-observations'),(20,500,1150,1000));fit(c,read('04-hill-context'),(1220,500,1150,1000));fit(c,locator(False),(2490,330,1250,1550))
 elif n=='10':
  names=['01-grand-overview','10-modern-airport']
  for k,name in enumerate(names):fit(c,read(name),(60+k*1900,260,1820,1580))
 elif n=='09':
  for k,name in enumerate(['map-1989-10','03-city-beneath','map-1994-07','map-1997-04']):fit(c,read(name),(50+k%2*1900,105+k//2*1070,1840,960))
 elif n=='11':
  fit(c,photograph_panel(False),(65,350,1190,1300));fit(c,read('11-surface-top'),(1325,350,1190,1300));fit(c,read('11-map-top'),(2585,350,1190,1300))
 elif n=='12':
  c=read('12-panorama');fit(c,read('01-grand-overview'),(2680,1320,1090,680))
 elif n=='06':c=read('06-final-alignment')
 else:c=read(it['source_render'])
 return c

def annotate(raw,it):
 c=Image.new('RGB',(W,H),IVORY);d=ImageDraw.Draw(c)
 d.text((115,66),'KAI TAK  /  A VISUAL ATLAS',font=font(28),fill=MUTED)
 d.text((W-115,66),it['id']+'  /  12',font=font(30),fill=MUTED,anchor='ra')
 size=86
 while d.textlength(it['title'],font=font(size,True))>W-230:size-=2
 d.text((110,110),it['title'],font=font(size,True),fill=INK)
 d.text((115,219),it['subtitle'],font=font(36),fill=MUTED)
 fit(c,raw,(70,292,W-140,1530))
 d.line((115,1850,W-115,1850),fill='#bac2ba',width=2)
 d.text((115,1873),it['epoch'],font=font(35),fill=ACCENT)
 d.text((W-115,1873),('EVIDENCE-LED' if it['mode']=='evidence' else 'INTERPRETIVE / DISCLOSED CONTEXT'),font=font(29),fill=INK,anchor='ra')
 wrapped(d,it['caption'],(115,1930),W-230,32)
 wrapped(d,it['limit'],(115,2023),W-230,27,color=MUTED)
 d.text((115,2100),'Lands Department / Buildings Department, HKSAR Government · CSDI · DATA.GOV.HK  |  Aryan Ayyar',font=font(22),fill=MUTED)
 return c

S=json.loads((A/'storyboard/storyboard.json').read_text());out=[]
# Image04's deliverable separates historical evidence and explicitly later terrain context.
S[3]['subtitle']='Actual historical height observations and a separately dated modern terrain view';S[3]['mode']='interpretive';S[3]['type']='Separated historical observations and modern terrain context';S[3]['epoch']='Hill observations: November 1989 / terrain context: 2014–2015'
(A/'storyboard/storyboard.json').write_text(json.dumps(S,indent=2,ensure_ascii=False)+'\n')
for it in S:
 raw=raw_composite(it);base=it['id']+'-'+it['slug'];master=A/f'renders/master/atlas-{base}.png';annotated=A/f'renders/annotated/{base}.png';web=A/f'renders/web/{base}.webp'
 clean_composite(it).save(master,pnginfo=metadata(it));img=annotate(raw,it);img.save(annotated,pnginfo=metadata(it));small=ImageOps.contain(img,(1920,1080));small.save(web,quality=90)
 if it['id'] in ['09','10','11']:img.save(A/f'comparisons/{base}.png',pnginfo=metadata(it))
 web.with_suffix('.json').write_text(json.dumps(it,indent=2,ensure_ascii=False)+'\n')
 it.update(master=str(master.relative_to(A)),annotated=str(annotated.relative_to(A)),web=str(web.relative_to(A)),size=[W,H]);out.append(it)
(A/'metadata/gallery.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Print layouts: 300dpi A4 landscape. Content is downsampled, never upsampled.
(A/'renders/print').mkdir(exist_ok=True);(A/'renders/crops').mkdir(exist_ok=True);pages=[]
for it in out:
 p=Image.new('RGB',(3508,2480),IVORY);fit(p,Image.open(A/it['annotated']),(0,0,3508,2480));p.save(A/f'renders/print/{it["id"]}-A4.png',dpi=(300,300),pnginfo=metadata(it));pages.append(p)
pages[0].save(A/'renders/print/Kai-Tak-Visual-Atlas-A4.pdf',save_all=True,append_images=pages[1:],resolution=300)
for id in ['03','08','12']:
 it=dict(next(t for t in out if t['id']==id));im=read('12-panorama') if id=='12' else Image.open(A/it['master'])
 if id=='12':it['limit']='Nominally calibrated partial surface, with relative heights rather than HKPD. No map context is included.';it.update(epoch='Photographs: 2 November 1993',type='Selected crop of partial observed surface',caption='Selected portion of the observed surface only. No airport map inset is included.',mode='evidence')
 it['limit']='Cropped view, not full reconstruction extent. '+it['limit']
 square=im.crop((840,0,3000,2160));square.save(A/f'renders/crops/{id}-square.png',pnginfo=metadata(it))
 vertical=im.crop((1312,0,2527,2160)).resize((1080,1920),Image.Resampling.LANCZOS);vertical.save(A/f'renders/crops/{id}-vertical.png',pnginfo=metadata(it))
# Reusable transparent, non-geographic legend overlay.
over=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(over)
for x,col,t in [(110,INK,'A  SOURCE OBSERVATIONS'),(1270,'#77909a','B  PARTIAL / APPROXIMATE'),(2530,'#9aa5a0','C  MISSING EVIDENCE')]:
 d.rectangle((x,2020,x+28,2048),fill=col);d.text((x+45,2014),t,font=font(31),fill=col)
over.save(A/'renders/annotated/evidence-legend-overlay.png')
# Readable overview contact sheet.
c=Image.new('RGB',(1800,1200),IVORY);d=ImageDraw.Draw(c)
for i,it in enumerate(out):
 im=Image.open(A/it['annotated']);fit(c,im,((i%3)*600,(i//3)*300,600,300))
c.save(A/'qa/contact-sheet.jpg',quality=95)
print('Assembled',len(out),'annotated/master/web, print PDF, comparisons and crops')
# Selectable evidence/context views share source geometry and camera; added material is disclosed.
for id,render in [('04','04-hill-observations'),('06','06-final-alignment'),('12','12-panorama')]:
 item=next(t for t in out if t['id']==id);ev=dict(item);ev['mode']='evidence'
 if id=='04':
  ev.update(epoch='Survey edition: November 1989',subtitle='Partial source-backed contours and spot elevations only',type='Historical terrain observations, no interpolated surface',caption='Two partial contours and eight spot elevations survive in the audited source. The missing hill surface is not filled. The painted checkerboard itself has not been placed as a surveyed 3D object.')
 if id=='06':ev['limit']='Map reference plane only. Exact threshold registration remains unresolved. No course diagram or inferred flight track is included.';ev.update(subtitle='Historical map context and the partial digitized runway edges',type='Historical cartographic reference',caption='The accepted map lines are highlighted; complete runway registration is still unresolved. This evidence-only view adds no schematic course arrows or inferred flight track.')
 if id=='12':ev['limit']='Only the partial nominally calibrated 1993 surface is shown. Elevations remain relative to a fitted park/road plane, not HKPD; no geographic inset is included.';ev.update(epoch='Photographs: 2 November 1993',subtitle='Panoramic source surface, without the separate geographic inset',type='Partial observed-surface panorama',caption='This is only the supported photo-derived patch. Missing faces remain absent; the neutral support is not reconstructed terrain. Relative elevations are not HKPD.')
 path=A/f'renders/annotated/{id}-evidence.png';evim=annotate(read(render),ev);evim.save(path,pnginfo=metadata(ev));wp=A/f'renders/web/{id}-evidence.webp';ImageOps.contain(evim,(1920,1080)).save(wp,quality=90);wp.with_suffix('.json').write_text(json.dumps(ev,indent=2,ensure_ascii=False)+'\n')
 mp=A/f'renders/master/atlas-{id}-evidence.png';read(render).save(mp,pnginfo=metadata(ev))
 item['evidence_variant']=dict(web=str(wp.relative_to(A)),annotated=str(path.relative_to(A)),master=str(mp.relative_to(A)),epoch=ev['epoch'],caption=ev['caption'],type=ev['type'],subtitle=ev['subtitle'],limit=ev['limit'],mode='evidence')
(A/'metadata/gallery.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')

# Discoverable matched daylight alternative, with unchanged camera and scientific geometry.
it=dict(next(t for t in out if t['id']=='08'));it['subtitle']='Architectural daylight treatment · same source and camera';it['caption']='The same original mesh in neutral daylight. The artistic treatment changes; the source coordinates, holes and camera do not.'
day=annotate(read('08-surface-daylight'),it);day.save(A/'renders/annotated/08-daylight.png',pnginfo=metadata(it));ImageOps.contain(day,(1920,1080)).save(A/'renders/web/08-daylight.webp',quality=90)
(A/'renders/web/08-daylight.json').write_text(json.dumps(it,indent=2,ensure_ascii=False)+'\n')
