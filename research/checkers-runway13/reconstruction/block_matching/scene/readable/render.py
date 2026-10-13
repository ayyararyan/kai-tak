"""Presentation-only scientific figures from unchanged, source-bound scene data."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import Normalize

P = Path(__file__).resolve().parent
ROOT = P.parent.parent
SOURCE = P.parent / 'scene.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
scene_hash = sha(SOURCE)
s = json.loads(SOURCE.read_text())
for row in s['maps']:
    assert sha(ROOT / row['source_path']) == row['sha256']
faces = {f['id']: f for f in s['historical_faces'] if f['source_epoch'] == '1989-10'}
for f in faces.values():
    assert f['height_m'] is None and f['physical_volume'] is None
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13})
BG, INK, BLUE = '#f5f3ed', '#24343d', '#006b95'
landmarks = [('shing_tung', 'Shing Tung House', (200, 620)),
             ('hong_tung', 'Hong Tung House', (485, 620)),
             ('ng_wah', 'Ng Wah College', (650, 570)),
             ('lee_school', 'Lee Kau Yan School', (660, 370)),
             ('regal', 'Regal Airport Hotel', (585, 175)),
             ('city_market', 'Kowloon City Market', (150, 65))]

def base(title, subtitle):
    fig = plt.figure(figsize=(10, 10.5), facecolor=BG)
    ax = fig.add_axes([.06, .19, .88, .64], facecolor='#e0e4e5')
    fig.text(.06, .945, title, fontsize=23, weight='bold', color=INK)
    fig.text(.06, .90, subtitle, fontsize=13, color=INK, linespacing=1.45)
    ax.set(xlim=(-30, 780), ylim=(-10, 640), aspect='equal')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((547,12),127,46,facecolor='white',edgecolor='none',zorder=90))
    fig.text(.92,.845,'↑ N',ha='right',fontsize=15,color=INK)
    ax.plot([560, 660], [25, 25], color=INK, lw=4,zorder=100)
    fig.text(.753,.242,'100 m',ha='center',fontsize=12,color=INK)
    return fig, ax

def locators(ax):
    for i, (key, label, textxy) in enumerate(landmarks, 1):
        f = faces[key]
        q = np.array(f['outer_local'])
        ax.plot(q[:, 0], q[:, 1], color=BLUE, lw=1.4)
        xy = (f['properties']['seed_e'] - 837500, f['properties']['seed_n'] - 821000)
        ax.annotate(label, xy=xy, xytext=textxy, ha='center', va='center',
                    fontsize=11, color=INK, weight='bold', annotation_clip=False, clip_on=False,
                    bbox={'boxstyle':'round,pad=.3', 'fc':'white', 'ec':BLUE, 'lw':.8},
                    arrowprops={'arrowstyle':'-', 'color':BLUE, 'lw':1.2})

fig, ax = base('Start here: the neighbourhood',
               'North-up survey map · October 1989\nBlue outlines and labels locate six inspected mapped forms.')
row = s['maps'][0]
ax.imshow(plt.imread(ROOT / row['source_path']), extent=(0,750,0,600), origin='upper')
locators(ax)
fig.text(.06, .105, 'This is a small Kowloon City / Tung Tau area, not the whole approach.\nThe 1989 map is a locator; it does not establish each building’s state in 1993.',
         fontsize=12, color=INK, linespacing=1.6)
fig.savefig(P/'01-labelled-map.png', dpi=160, facecolor=BG)
plt.close(fig)

m = s['observed_mesh']
v = np.asarray(m['vertices'], dtype=float)
f = np.asarray(m['faces'], dtype=int)[:, :3]
tri = v[f, :3]
keep = ((tri[:,:,0]>=0)&(tri[:,:,0]<=750)&(tri[:,:,1]>=0)&(tri[:,:,1]<=600)).all(axis=1)
tri = tri[keep]
z = tri[:,:,2].mean(axis=1)
norm = Normalize(vmin=-10, vmax=60)
cmap = plt.get_cmap('viridis').copy()
cmap.set_under('#a8c6ed'); cmap.set_over('#fa6b35')

fig, ax = base('What the photos recovered',
               'Same area, same orientation · 2 November 1993\nColour shows relative surface elevation; grey gaps have no mesh coverage.')
collection = PolyCollection(tri[:,:,:2], array=z, cmap=cmap, norm=norm,
                            edgecolors='none', linewidths=0, antialiaseds=False)
ax.add_collection(collection)
locators(ax)
cax = fig.add_axes([.22,.145,.56,.018])
bar = fig.colorbar(collection, cax=cax, orientation='horizontal', extend='both')
bar.set_label('Metres relative to the fitted local reference plane', fontsize=11)
bar.ax.tick_params(labelsize=10)
fig.text(.06,.04,'Blue outlines: 1989 map locators, not recovered roof boundaries.\nConditional calibration; most points lie outside local map controls.\nNot sea-level elevation or building height above ground. No gaps filled.',
         fontsize=11, color=INK, linespacing=1.5)
fig.savefig(P/'02-recovered-surface.png', dpi=160, facecolor=BG)
plt.close(fig)

fig = plt.figure(figsize=(10,9), facecolor=BG)
ax = fig.add_axes([.08,.22,.84,.58], projection='3d', facecolor=BG, computed_zorder=False)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
selected = ((tri[:,:,0]>=0)&(tri[:,:,0]<=110)&(tri[:,:,1]>=90)&(tri[:,:,1]<=275)).all(axis=1)
q = tri[selected]
poly = Poly3DCollection(q, facecolors=cmap(norm(q[:,:,2].mean(axis=1))),
                       edgecolors='none', linewidths=0, antialiased=False)
ax.add_collection3d(poly)
ax.set(xlim=(0,110), ylim=(90,275), zlim=(-10,60))
ax.set_box_aspect((110,185,70)); ax.view_init(elev=35, azim=-55)
ax.set_xlabel('East offset (m)', fontsize=10)
ax.set_ylabel('North offset (m)', fontsize=10)
ax.set_zlabel('Relative elevation (m)', fontsize=10)
ax.tick_params(labelsize=9)
for axis in [ax.xaxis,ax.yaxis,ax.zaxis]: axis.pane.fill=False
roof_points = [p for p in s['stereo']['points'] if 'roof' in p['surface_class']]
for label,p in zip(['A','B'],roof_points):
    ax.scatter([p['x']],[p['y']],[p['z_relative_m']],color='#c83a22',s=65,depthshade=False,zorder=100)
    ax.text(p['x'],p['y'],p['z_relative_m']+5,label,color='#9c2010',fontsize=16,weight='bold',zorder=101)
fig.text(.06,.94,'Close-up: the market area',fontsize=24,color=INK,weight='bold')
fig.text(.06,.88,'Recovered surface patches, not complete buildings\n1993 photo geometry · equal metric scale on all three axes',fontsize=13,color=INK)
fig.text(.06,.14, 'A  Market north roof feature: 10.77 m above the reference plane\nB  South rooftop service structure: 19.20 m above the reference plane',
         fontsize=12,color=INK,linespacing=1.6)
fig.text(.06,.025,'Conditional estimates; both labelled points lie outside the map-control hull.\nNo calibrated height bounds. Colours use the preceding figure’s scale.\nBroken edges and holes are unresolved observations, not real building shapes.',
         fontsize=11,color=INK,linespacing=1.5)
fig.savefig(P/'03-market-closeup.png',dpi=160,facecolor=BG)
plt.close(fig)
assert sha(SOURCE)==scene_hash
receipt={'source_scene_sha256':scene_hash,'source_geometry_modified':False,
         'displayed_core_triangles':len(tri),'closeup_triangles':len(q),
         'core_colour_under_range':int((z < -10).sum()),'core_colour_over_range':int((z > 60).sum()),
         'map_hashes_verified':3,'historical_heights_still_null':True,
         'outputs':{p.name:sha(p) for p in P.glob('*.png')}}
(P/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
