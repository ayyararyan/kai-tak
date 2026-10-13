"""Shared V5 art direction: source-preserving, vector-first scientific illustration."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
P=Path(__file__).resolve().parents[1]
# Neutral print palette. Keep the established semantic roles, layout and data;
# distinct tones supplement the existing direct labels, dashes and markers.
INK='#141414'; SLATE='#666666'; COPPER='#3C3C3C'; SAGE='#737373'
PALE='#F1F1F1'; LIGHT='#DEDEDE'; GRID='#D8D8D8'; BLUE='#5A5A5A'
plt.rcParams.update({'font.family':'Arial','font.size':12.5,'axes.labelsize':12,
 'xtick.labelsize':11,'ytick.labelsize':11,'text.color':INK,'axes.labelcolor':INK,
 'axes.edgecolor':SLATE,'axes.spines.top':False,'axes.spines.right':False,
 'axes.linewidth':.6,'xtick.major.width':.6,'ytick.major.width':.6,
 'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','svg.hashsalt':'kaitak-v5',
 'savefig.facecolor':'white','figure.facecolor':'white','mathtext.fontset':'stix'})

def read(path):return json.loads((P/path).read_text())
def rows(path):
 with (P/path).open() as f:return list(csv.DictReader(f))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def bare(ax):
 ax.set_axis_off()
 return ax

def arrow(ax,start,end,color=INK,lw=1.4,head=10,**kw):
 a=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=head,lw=lw,color=color,**kw)
 ax.add_patch(a);return a

def label(ax,text,xy,at,color=INK,size=12,align='left'):
 ax.annotate(text,xy=xy,xytext=at,ha=align,va='center',fontsize=size,color=color,
  arrowprops={'arrowstyle':'-','lw':.6,'color':color,'shrinkA':4,'shrinkB':2})

def save(fig,name,inputs,meaning,**extra):
 """One master; vector PDF/SVG, screen PNG, 600dpi presentation PNG."""
 (P/'figures').mkdir(exist_ok=True);(P/'presentation').mkdir(exist_ok=True);(P/'qa/figure-records').mkdir(parents=True,exist_ok=True)
 # Keep fixed master canvas proportions; no mutable tight-bbox camera crop.
 meta={'CreationDate':None,'ModDate':None,'Title':meaning,'Author':'Aryan Ayyar'}
 fig.savefig(P/'figures'/f'{name}.pdf',metadata=meta)
 fig.savefig(P/'figures'/f'{name}.svg',metadata={'Date':None,'Title':meaning,'Creator':'V5 reproducible scientific illustration'})
 fig.savefig(P/'figures'/f'{name}.png',dpi=190)
 fig.savefig(P/'presentation'/f'{name}.png',dpi=600)
 paths=[]
 for s in inputs:
  f=P/s
  if not f.is_file():raise FileNotFoundError('Missing declared figure input: '+s)
  paths.append({'path':s,'sha256':sha(f)})
 out={'figure':name,'inputs':paths,'meaning':meaning,'master_inches':list(fig.get_size_inches()),
  'color_mode':'grayscale',
  'screen_dpi':190,'presentation_dpi':600,'pdf_sha256':sha(P/'figures'/f'{name}.pdf'),**extra}
 (P/'qa/figure-records'/f'{name}.json').write_text(json.dumps(out,indent=2)+'\n')
 plt.close(fig)

def curve(form,n=1001):
 out=[]
 for ph in form['phases']:
  s=np.linspace(0,1,n);T=ph['duration_s'];t0=ph.get('start_s',ph.get('t0_s',0));c=ph['coefficients_xyz_m']
  q=np.column_stack([np.polynomial.polynomial.polyval(s,r) for r in c])
  v=np.column_stack([np.polynomial.polynomial.polyval(s,np.polynomial.polynomial.polyder(r))/T for r in c])
  out.append((t0+s*T,q,v))
 return out
