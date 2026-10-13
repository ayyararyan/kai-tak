from pathlib import Path
import sys,json,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'integrated/python_deps'))
import ezdxf
from ezdxf.path import make_path
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=ROOT/'integrated/sources/747-400.dxf';d=ezdxf.readfile(p);curves=[]
for e in d.modelspace():
 if e.dxftype() not in ['LINE','POLYLINE','ARC','CIRCLE']:continue
 try:
  pts=np.array([tuple(v)[:2] for v in make_path(e).flattening(.05)])
  if len(pts)>1:curves.append(pts)
 except Exception as ex:raise RuntimeError(e.dxftype()) from ex
fig,ax=plt.subplots(figsize=(14,9))
for pts in curves:ax.plot(pts[:,0],pts[:,1],color='black',lw=.35)
ax.set_aspect('equal');ax.grid(alpha=.3);fig.savefig(ROOT/'integrated/geometry/aircraft_dxf_axes.png',dpi=150);plt.close(fig)
np.savez_compressed(ROOT/'integrated/geometry/aircraft_dxf_curves.npz',**{f'c{i}':v for i,v in enumerate(curves)})
print('curves',len(curves))
for e in d.modelspace().query('TEXT'):print(e.dxf.text,e.dxf.insert)
