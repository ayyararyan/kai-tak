from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from shapely.geometry import shape
R=Path(__file__).resolve().parent
fs=json.loads((R/'digitization_candidates_hk1980.geojson').read_text())['features']
for sid,epoch in [('1980_1990:678','1989-10'),('1980_1990:679','1994-07'),('1980_1990:680','1997-04')]:
 fig,ax=plt.subplots(figsize=(15,12),dpi=180)
 im=Image.open(R/'registered'/f'11-NE-11A_{epoch}_core.png')
 ax.imshow(im,extent=(837500,838250,821000,821600))
 for f in fs:
  if f['properties']['source_id']!=sid:continue
  p=shape(f['geometry']);x,y=p.exterior.xy;ax.fill(x,y,color='#bc7145',alpha=.28);ax.plot(x,y,color='#8a4221',lw=.5)
  q=p.representative_point();ax.annotate(f['properties']['id'],(q.x,q.y),fontsize=6,color='#b52b16')
 ax.set_title(epoch+' | Closed-region digitization candidates — not yet verified');ax.set_aspect('equal')
 fig.savefig(R/f'digitization_overlay_{epoch}.png',bbox_inches='tight');plt.close(fig)
