from pathlib import Path
import csv,json,datetime,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Patch
from matplotlib.collections import PatchCollection
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent

def render():
 rows=list(csv.DictReader((ROOT/'structures/aoi_features_1993-11-04.csv').open()))
 downloads=json.loads((ROOT/'sheets/map_downloads.json').read_text());good={r['source_id'] for r in downloads if r['status']=='validated_zip'}
 sheets=json.loads((ROOT/'sheets/aoi_sheet_index.geojson').read_text())['features']
 selected=[f for f in sheets if f['properties']['source_id'] in good]
 xy=np.array([[float(r['lon']),float(r['lat'])] for r in rows]);agreement=np.array([r.get('completion_matches_relational_permit_by_target')=='1' for r in rows])
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'figure.facecolor':'#f7f5ee','axes.facecolor':'#f7f5ee','axes.edgecolor':'#8b918d','text.color':'#273d43','axes.labelcolor':'#273d43','xtick.color':'#526369','ytick.color':'#526369'})
 fig,axs=plt.subplots(1,2,figsize=(15,8),layout='constrained')
 for ax,bounds,title in zip(axs,[(114.10,114.25,22.27,22.40),(114.16,114.22,22.30,22.35)],['Wider acquisition area','Approach / airport source coverage']):
  ax.scatter(xy[~agreement,0],xy[~agreement,1],s=.55,color='#aaa9a0',rasterized=True,alpha=.65)
  ax.scatter(xy[agreement,0],xy[agreement,1],s=.65,color='#587b63',rasterized=True,alpha=.85)
  seen=set()
  for f in selected:
   p=f['properties']
   if p['sheet'] in seen:continue
   seen.add(p['sheet'])
   coords=np.array(f['geometry']['coordinates'][0]);ax.plot(coords[:,0],coords[:,1],lw=.55,color='#b47645',alpha=.65)
  for label,x,y in [('Checkerboard Hill',114.1832,22.335),('Walled City site',114.1903,22.3323),('Runway 13 threshold',114.1967,22.3217)]:
   ax.plot(x,y,'o',ms=4,color='#713c33');ax.annotate(label,(x,y),xytext=(5,7),textcoords='offset points',fontsize=8,bbox={'facecolor':'#f7f5ee','alpha':.88,'edgecolor':'none','pad':1})
  ax.set(xlim=bounds[:2],ylim=bounds[2:],xlabel='Longitude (WGS84)',ylabel='Latitude (WGS84)',title=title);ax.set_aspect(1/np.cos(np.deg2rad(22.33)));ax.grid(alpha=.15)
 fig.suptitle('Kai Tak historical reconstruction — source coverage, not a reconstructed city',fontsize=16,fontweight='bold')
 fig.legend(handles=[Patch(color='#587b63',label='Current feature: completion and linked permit agree before 4 Nov 1993'),Patch(color='#aaa9a0',label='Other current features: earlier presence unresolved by that test'),Patch(facecolor='none',edgecolor='#b47645',label='Downloaded historical survey-sheet locations')],loc='outside lower center',ncol=1,frameon=False,fontsize=9)
 fig.savefig(ROOT/'coverage.png',dpi=180);plt.close(fig)
 # Actual source pages, deliberately not registered or morphed into false pixel correspondence.
 paths=[('1989-10 survey sheet','sheets/previews/1980_1990_678_11-NE-11A_1989-10-01.png'),('1993-11-02 aerial photograph A36143','aerial/fullframes/A36143.jpg'),('1994-07 survey sheet','sheets/previews/1980_1990_679_11-NE-11A_1994-07-01.png'),('1997-04 survey sheet','sheets/previews/1980_1990_680_11-NE-11A_1997-04-01.png')]
 fig,axs=plt.subplots(2,2,figsize=(14,14),layout='constrained')
 for ax,(title,path) in zip(axs.flat,paths):
  im=Image.open(ROOT/path).convert('RGB');ax.imshow(im);ax.axis('off');ax.set_title(title,fontsize=12)
 fig.suptitle('The same neighbourhood through dated sources',fontsize=17,fontweight='bold')
 fig.text(.5,.002,'Lands Department / Hong Kong Government. Photograph is not orthorectified; panels are not pixel-aligned. Sheet dates are edition months.',ha='center',fontsize=9)
 fig.savefig(ROOT/'source_comparison.png',dpi=180);plt.close(fig)
 print('Rendered coverage.png and source_comparison.png')
if __name__=='__main__':render()
