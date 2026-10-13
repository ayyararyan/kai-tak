from pathlib import Path
import sys,copy,json,math
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import numpy as np
from numpy.polynomial import Polynomial as Poly
from scipy.optimize import minimize,brentq
from scipy.spatial import cKDTree
from model import trajectory as tr
from model.solve import SCALE
from analytical.verify_full_landing_analysis import explicit
from forces import phase
OUT=Path(__file__).resolve().parent
SCENE=json.loads((OUT/'scene.json').read_text())
BASE=tr.values(tr.load_config());EV=tr.Evaluator(tr.load_config());TREE=cKDTree(EV.reference_tree.data+[0,0,6])
BOUNDS=np.array(tr.BOUNDS)

class Case:
 def __init__(self,name='mean',wind=(-4.876589552990943,9.64006667211232,0),urban=25,roof_delta=0,frame_dx=0,frame_dy=0,runway_level=6,buffer=5):
  self.name=name;self.p=copy.deepcopy(BASE);self.p['wind_mps']=list(wind)
  self.urban=urban;self.roof_delta=roof_delta;self.frame_dx=frame_dx;self.frame_dy=frame_dy;self.runway_level=runway_level;self.buffer=buffer
  vals=[*wind,urban,roof_delta,frame_dx,frame_dy,runway_level,buffer]
  if not np.isfinite(vals).all() or len(wind)!=3 or wind[2]!=0 or buffer<0:raise ValueError('invalid condition')
 def parameters(self):return {k:v for k,v in vars(self).items() if k!='p'}|{'wind_mps':self.p['wind_mps']}
 def curves(self,q):
  q=np.asarray(q,float)
  if q.shape!=(12,) or not np.isfinite(q).all() or np.any(q<BOUNDS[:,0]-1e-10) or np.any(q>BOUNDS[:,1]+1e-10):raise ValueError('decision domain')
  p=self.p;start=np.array([-2500,1000,146]);gate=np.array([0,0,21.24]);zero=np.zeros(3)
  v0=tr.endpoint_velocity(153,146,-47,-3.1,p);vg=tr.endpoint_velocity(153,21.24,0,-3.1,p)
  a=explicit(start,gate,v0,vg,zero,zero,q[0]);f=explicit(gate,[q[2],0,6],vg,[q[3],0,-.7],zero,zero,q[1])
  bump=64*Poly([0,0,0,1,-3,3,-1]);odd=bump*Poly([-1,2])
  for k in range(3):a[k]+=q[4+2*k]*bump+q[5+2*k]*odd
  f[0]+=q[10]*bump;f[2]+=q[11]*bump
  return a,f
 def geometry(self,d):
  r=d['pos'];co=np.cos(d['bank']);si=np.abs(np.sin(d['bank']))
  low=r[:,2]-np.maximum(4*co+32.7*si,6*co+6.0579*si)
  # Whole-body horizontal radius55 covers body box and all gear at any roll/yaw.
  rad=55+self.buffer
  out={}
  for i,ob in enumerate(SCENE['obstacles']):
   xmin,ymin,xmax,ymax=ob['bounds_xy'];xmin+=self.frame_dx;xmax+=self.frame_dx;ymin+=self.frame_dy;ymax+=self.frame_dy
   # Disk/rectangle separating exterior gap; negative inside inflated rectangle.
   dx=np.maximum(xmin-r[:,0],r[:,0]-xmax);dy=np.maximum(ymin-r[:,1],r[:,1]-ymax)
   horizontal=np.maximum(dx,dy)-rad
   top=ob['top_hkpd_assumed_m']-self.runway_level+self.roof_delta
   out[f'object_{i}']=np.maximum(horizontal,low-top-3)
  # Infinite urban halfplane; frame shift applies to the assumed background too.
  x=r[:,0]-self.frame_dx;y=r[:,1]-self.frame_dy
  out['urban_upstream']=np.maximum(x-rad+600,low-self.urban-3)
  # Remaining strip excludes either side: rectangle(-600,0) × (100,+infinity), etc.
  for sign in [-1,1]:
   side=sign*y
   hgap=np.maximum.reduce([-600-x,x,100-side])-rad
   out[f'urban_side_{sign}']=np.maximum(hgap,low-self.urban-3)
  out['nongear_ground']=r[:,2]-4*co-32.7*si-.5
  out['gear_ground']=r[:,2]-6*co-6.0579*si
  return out
 def evaluate(self,q,n=161,details=False,geometry=True):
  s=np.linspace(0,1,n);cs=self.curves(q);ps=[phase(c,T,s,self.p) for c,T in zip(cs,q[:2])]
  d={k:np.concatenate([p[k] for p in ps]) for k in ps[0]};m={}
  for key,lo,hi in [('eas',135,175),('cl',0,2.8),('load',.5,1.4),('thrust',0,700000)]:m[key+'_lower']=(d[key]-lo)/(hi-lo);m[key+'_upper']=(hi-d[key])/(hi-lo)
  for key,cap in [('bank',np.deg2rad(25)),('roll',np.deg2rad(5)),('slew',100000)]:m[key]=1-abs(d[key])/cap
  m['descent']=1+d['gamma']/np.deg2rad(6);m['approach_sink']=1+ps[0]['vel'][:,2]/8
  m['corridor']=1-TREE.query(d['pos'])[0]/400
  stop=q[2]+2*q[3]+q[3]**2/(2*1.4709975)
  m.update(touchdown_x_lower=np.array([(q[2]-200)/500]),touchdown_x_upper=np.array([(700-q[2])/500]),touchdown_sink_lower=np.array([.7/1.5]),touchdown_sink_upper=np.array([.8/1.5]),touchdown_lateral=np.array([1.]),touchdown_track=np.array([1.]),touchdown_bank=np.array([1.]),stop=np.array([(2636-stop)/2636]))
  hard={'forward_speed':d['vel'][:,0],'lift_up':d['lu']/self.p['mass_kg']}
  if geometry:
   hard.update(self.geometry(d))
   # With forward x, the urban halfplane exit is a unique scalar root.
   # Its one-sided limit must retain vertical clearance; imposing that limit
   # prevents coarse-mesh horizontal/vertical disjunction aliasing.
   exit_x=-600+55+self.buffer+self.frame_dx
   if -2500<exit_x<0:
    sr=brentq(lambda ss:cs[0][0](ss)-exit_x,0,1,xtol=1e-13)
    dd=phase(cs[0],q[0],np.array([sr]),self.p)
    co=np.cos(dd['bank']);si=np.abs(np.sin(dd['bank']))
    lower=dd['pos'][:,2]-np.maximum(4*co+32.7*si,6*co+6.0579*si)
    hard['urban_exit_limit']=lower-self.urban-3
  # Structural endpoint contact equality: remove its cancellation residual only.
  if geometry:hard['gear_ground']=hard['gear_ground'][:-1]
  hardvec=np.concatenate([(v-(.2 if k.startswith(('object_','urban_')) else 0))/100 for k,v in hard.items()])
  effort=sum(np.trapezoid((p['bank']/np.deg2rad(25))**2+(p['roll']/np.deg2rad(5))**2+(p['slew']/100000)**2,s*T) for p,T in zip(ps,q[:2]))
  if details:return m,hard,effort,ps
  return m,hardvec,effort
 def solve(self,q,n=161,secondary=False,eta_floor=0,maxiter=350,geometry=True):
  cache={}
  def get(x):
   key=x[:-1].tobytes()
   if key not in cache:cache.clear();cache[key]=self.evaluate(x[:-1]*SCALE,n,geometry=geometry)
   return cache[key]
  def con(x):
   m,h,_=get(x);return np.r_[np.concatenate(list(m.values()))-x[-1],h]
  q=np.clip(q,BOUNDS[:,0],BOUNDS[:,1]);m,_,_=self.evaluate(q,n,geometry=geometry)
  x0=np.r_[q/SCALE,min(map(np.min,m.values()))-1e-6]
  result=minimize((lambda x:get(x)[2]/50) if secondary else(lambda x:-x[-1]),x0,method='SLSQP',bounds=[(a/s,b/s) for (a,b),s in zip(BOUNDS,SCALE)]+[(eta_floor if secondary else -2,.49)],constraints=[dict(type='ineq',fun=con)],options=dict(maxiter=maxiter,ftol=1e-10,eps=1e-6))
  q=result.x[:-1]*SCALE;m,h,e,ps=self.evaluate(q,3001,details=True,geometry=geometry)
  return dict(success=bool(result.success),message=str(result.message),iterations=int(result.nit),q=q.tolist(),eta=float(min(map(np.min,m.values()))),effort=float(e),minima={k:float(np.min(v)) for k,v in m.items()},hard_minima={k:float(np.min(v)) for k,v in h.items()},hard_min=float(min(map(np.min,h.values()))),mesh=n,secondary=secondary,geometry=geometry)

def terminal_bound(case):
 # CG height6 means EAS->TAS at touchdown uses exp(6/17000).
 wx,wy,_=case.p['wind_mps'];k=tr.KT*np.exp(6/17000);sig=.7;a=1.4709975
 def speed(eta):
  rad=(k*(135+40*eta))**2-wy*wy-sig*sig
  if rad<=0:raise ValueError('terminal radical outside selected domain')
  return wx+np.sqrt(rad)
 def fun(eta):
  u=speed(eta);return 200+500*eta+2*u+u*u/(2*a)-2636*(1-eta)
 if speed(0)<=0:raise ValueError('positive air-forward/ground-speed branch required')
 if fun(0)>0:return dict(status='terminal_relaxation_infeasible',eta_upper=0.,root=None)
 if fun(.45)<=0:root=None;upper=.45
 else:root=brentq(fun,0,.45,xtol=1e-14);upper=root
 # Quartic polynomial: Q^2-B^2D; root selection must preserve unsquared sign.
 D=Poly([k*135,k*40])**2-(wy*wy+sig*sig)
 Q=Poly([200-2636+2*wx+wx*wx/(2*a),3136])+D/(2*a);B=2+wx/a
 return dict(status='global_terminal_relaxation_upper_not_full_optimum',eta_upper=float(upper),root=root,quartic_coefficients=(Q*Q-B*B*D).coef.tolist(),radical_multiplier=B,root_sign_rule='Q+B*sqrt(D)=0; reject roots failing original equation',terminal_speed_at_bound=float(speed(upper)),residual=float(fun(upper)))
