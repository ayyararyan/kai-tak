from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).resolve().parent
s=json.loads((P/'scene.json').read_text());a=np.array(s['dense']['points'],dtype=float)
a=a[(a[:,1]>=0)&(a[:,1]<=750)&(a[:,2]>=0)&(a[:,2]<=600)]
fig=plt.figure(figsize=(14,10),facecolor='#f5f4ef');ax=fig.add_subplot(111,projection='3d',facecolor='#f5f4ef')
cmap=LinearSegmentedColormap.from_list('sage',['#20382f','#82967e','#e6e6d3'])
if s.get('observed_mesh',{}).get('available'):
 m=s['observed_mesh'];v=np.array(m['vertices']);f=np.array(m['faces'],dtype=int)[:,:3];q=v[f,:3]
 keep=((q[:,:,0]>=0)&(q[:,:,0]<=750)&(q[:,:,1]>=0)&(q[:,:,1]<=600)).all(axis=1)
 q=q[keep];rgb=v[f[keep],3:6].mean(axis=1)/255
 collection=Poly3DCollection(q,facecolors=rgb,edgecolors='none',linewidths=0,antialiased=False)
 ax.add_collection3d(collection)
else:
 ax.scatter(a[:,1],a[:,2],a[:,3],c=a[:,4],cmap=cmap,vmin=0,vmax=255,s=2,linewidths=0,depthshade=False)
for f in s['historical_faces']:
 if f['source_epoch']!='1989-10':continue
 q=np.array(f['outer_local']);ax.plot(q[:,0],q[:,1],np.zeros(len(q)),color='#a7704c',linewidth=.7,alpha=.55)
for p in s['stereo']['points']:
 if 'roof' in p['surface_class']:
  ax.scatter([p['x']],[p['y']],[p['z_relative_m']],c='#b25531',s=24,depthshade=False)
ax.set(xlim=(0,750),ylim=(0,600),zlim=(-15,100),xlabel='East offset from 837500 m',ylabel='North offset from 821000 m',zlabel='Relative Z (m; not HKPD)')
ax.set_box_aspect((750,600,115));ax.view_init(elev=33,azim=-120)
for a in [ax.xaxis,ax.yaxis,ax.zaxis]:a.pane.fill=False;a._axinfo['grid']['color']='#d7dcd3'
ax.tick_params(labelsize=8,colors='#687566')
fig.suptitle('Kai Tak · 2 November 1993',x=.1,y=.94,ha='left',fontfamily='serif',fontsize=26,color='#283732')
fig.text(.1,.895,'Recovered image surfaces from stereo photographs A36142 + A36143',fontsize=12,color='#61725e')
fig.text(.1,.065,'Observed surface patches relative to a fitted local plane. 1989 outlines shown only as locators.\nConditional camera calibration; horizontal extrapolation outside controls; non-watertight surfaces, not complete buildings or calibrated height bounds.',fontsize=10,color='#6c7868')
fig.savefig(P/'overview.png',dpi=150,bbox_inches='tight',facecolor=fig.get_facecolor())
print('Wrote',P/'overview.png')
