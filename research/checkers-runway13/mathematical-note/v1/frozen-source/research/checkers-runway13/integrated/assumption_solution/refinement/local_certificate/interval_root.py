"""Outward interval dual numbers nested in normalized-time Taylor jets.
All real constants enter as decimal strings; no finite differences in proof.
Jets store f^(k)/k!, order 3 suffices for the slew-stationarity Jacobian
and the curvature sign of the active slew margin.
"""
from pathlib import Path
import sys,json,math
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent));sys.path.insert(1,str(HERE.parent.parent))
from box_certifier import I,iv,coeff,Case,ic
import numpy as np
iv.dps=50
N=9; ORDER=3

def interval(x):return x if hasattr(x,'a') else I(x)
def bounds(x):return [str(x.a),str(x.b)]
def display(x):return [float(x.a),float(x.b)]
def mag(x):return max(abs(float(x.a)),abs(float(x.b)))
def midpoint(x):return (x.a+x.b)/2
class D:
 def __init__(self,v,d=None):self.v=interval(v);self.d=[I(0)]*N if d is None else d
 def __add__(self,b):
  b=dual(b);return D(self.v+b.v,[x+y for x,y in zip(self.d,b.d)])
 __radd__=__add__
 def __neg__(self):return D(-self.v,[-x for x in self.d])
 def __sub__(self,b):return self+-dual(b)
 def __rsub__(self,b):return dual(b)+-self
 def __mul__(self,b):
  b=dual(b);return D(self.v*b.v,[x*b.v+self.v*y for x,y in zip(self.d,b.d)])
 __rmul__=__mul__
 def __truediv__(self,b):
  b=dual(b);return D(self.v/b.v,[(x*b.v-self.v*y)/b.v**2 for x,y in zip(self.d,b.d)])
 def __rtruediv__(self,b):return dual(b)/self
 def __pow__(self,n):
  if n==0:return D(1)
  if n<0:return D(1)/(self**(-n))
  return D(self.v**n,[n*self.v**(n-1)*x for x in self.d])
 def sqrt(self):
  v=iv.sqrt(self.v);return D(v,[x/(2*v) for x in self.d])
 def exp(self):
  v=iv.exp(self.v);return D(v,[v*x for x in self.d])
def dual(x):return x if isinstance(x,D) else D(x)
class J:
 def __init__(self,c):self.c=[dual(x) for x in c]+[D(0)]*(ORDER+1-len(c))
 def __add__(self,b):
  b=jet(b);return J([x+y for x,y in zip(self.c,b.c)])
 __radd__=__add__
 def __neg__(self):return J([-x for x in self.c])
 def __sub__(self,b):return self+-jet(b)
 def __rsub__(self,b):return jet(b)+-self
 def __mul__(self,b):
  b=jet(b);return J([sum((self.c[k]*b.c[n-k] for k in range(n+1)),D(0)) for n in range(ORDER+1)])
 __rmul__=__mul__
 def reciprocal(self):
  out=[1/self.c[0]]
  for n in range(1,ORDER+1):out.append(-sum((self.c[k]*out[n-k] for k in range(1,n+1)),D(0))/self.c[0])
  return J(out)
 def __truediv__(self,b):return self*jet(b).reciprocal()
 def __rtruediv__(self,b):return jet(b)*self.reciprocal()
 def __pow__(self,n):
  if n<0:return (self**(-n)).reciprocal()
  out=J([1])
  for _ in range(n):out=out*self
  return out
 def sqrt(self):
  out=[self.c[0].sqrt()]
  for n in range(1,ORDER+1):out.append((self.c[n]-sum((out[k]*out[n-k] for k in range(1,n)),D(0)))/(2*out[0]))
  return J(out)
 def exp(self):
  out=[self.c[0].exp()]
  for n in range(1,ORDER+1):out.append(sum((k*self.c[k]*out[n-k] for k in range(1,n+1)),D(0))/n)
  return J(out)
def jet(x):return x if isinstance(x,J) else J([x])
def dot(a,b):return sum((x*y for x,y in zip(a,b)),J([0]))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):return dot(a,a).sqrt()
BASE=json.loads((HERE.parent/'active_branch.json').read_text())['baseline']
SCALE=[5,300,75,1,1]
W=[I('-4.876589552990943'),I('9.64006667211232'),I(0)]
def variables(xs):return [D(x,[I(int(i==j)) for j in range(N)]) for i,x in enumerate(xs)]
def coefficients(z):
 T,x,U,fx,fz=[z[k]*SCALE[k] for k in range(5)]
 gam=-I('3.1')*iv.pi/180;V=I(153)*I(1852)/3600*iv.exp(I('21.24')/17000)
 vg=[W[0]+iv.sqrt((V*iv.cos(gam))**2-W[1]**2),I(0),V*iv.sin(gam)]
 cs=[]
 for p0,p1,v0,v1,b in zip([0,0,'21.24'],[x,D(0),D(6)],vg,[U,D(0),D('-.7')],[fx,D(0),fz]):
  c0=D(p0);c1=T*v0;A=p1-c0-c1;B=T*v1-c1
  c=[c0,c1,D(0),10*A-4*B,-15*A+7*B,6*A-3*B,D(0)]
  cs.append([v+b*k for v,k in zip(c,[0,0,0,64,-192,192,-64])])
 return cs,T

def state(z,s):
 cs,T=coefficients(z);s=J([s,1]);kin=[]
 for k in range(3):
  row=[]
  for c in cs:
   dc=c[:]
   for _ in range(k):dc=[(i+1)*dc[i+1] for i in range(len(dc)-1)]
   # Centered polynomial Taylor algebra limits interval dependency in time.
   mid=D(midpoint(s.c[0].v)); shifted=[]; dd=dc[:]
   for j in range(len(dc)):
    value=D(0)
    for c in reversed(dd):value=value*mid+c
    shifted.append(value/math.factorial(j));dd=[(i+1)*dd[i+1] for i in range(len(dd)-1)]
   val=J([0])
   for v in reversed(shifted):val=val*(s-J([mid]))+J([v])
   row.append(val/J([T**k]))
  kin.append(row)
 r,v,a=kin;va=[x-w for x,w in zip(v,W)];V=norm(va);H=norm(va[:2]);et=[x/V for x in va];er=[-va[1]/H,va[0]/H,J([0])];eu=cross(et,er)
 F=[(x+(I('9.80665') if k==2 else 0))*I('238461.67357166') for k,x in enumerate(a)]
 L=norm([dot(F,eu),dot(F,er)]);Q=(-r[2]/8500).exp()*V**2*I('.5')*I('1.225')*I('541.2')
 thrust=Q*I('.08')+L**2*I('.045')/Q+dot(F,et)
 return thrust,L/(I('238461.67357166')*I('9.80665')),T

# Signed branches are checked explicitly at every certificate evaluation.
def active(z):
 T,x,U,fx,fz=[z[k]*SCALE[k] for k in range(5)]
 m=[(2636-x-2*U-U**2/(2*I('1.4709975')))/2636];station=[];curvature=[];signs=[]
 for s in [D(0),D(1),z[6]]:
  th,ld,T=state(z,s);v=th.c[1]/T
  sign=1 if v.v.a>0 else -1 if v.v.b<0 else 0
  if not sign:raise ValueError('slew sign not separated')
  signs.append(sign);m.append(1-sign*v/100000)
  if s is z[6]:station.append(-sign*2*th.c[2]/T/100000);curvature.append(-sign*6*th.c[3]/T/100000)
 th,ld,T=state(z,z[7]);m.append((D('1.4')-ld.c[0])/I('.9'));station.append(-ld.c[1]/I('.9'));curvature.append(-2*ld.c[2]/I('.9'))
 th,ld,T=state(z,z[8]);m.append(th.c[0]/700000);station.append(th.c[1]/700000);curvature.append(2*th.c[2]/700000)
 return m,station,curvature,signs

def system(xs):
 z=variables(xs);m,st,cu,signs=active(z);F=[x-z[5] for x in m]+st
 return [x.v for x in F],[[v for v in x.d] for x in F],m,cu,signs

def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),I(0)) for col in zip(*B)] for row in A]
def mv(A,b):return [sum((x*y for x,y in zip(row,b)),I(0)) for row in A]
def eye(n):return [[I(int(i==j)) for j in range(n)] for i in range(n)]
def minus(A,B):return [[x-y for x,y in zip(a,b)]for a,b in zip(A,B)]
def decimal_mid(x):
 from mpmath import mp
 mp.dps=55
 # conversion through exact mpf endpoint, not float
 return mp.nstr((mp.mpf(x._mpi_[0])+mp.mpf(x._mpi_[1]))/2,48)
def refine(xs,steps=3):
 for _ in range(steps):
  f,j,*_=system(xs)
  from mpmath import mp
  mp.dps=55
  jm=mp.matrix([[mp.mpf(decimal_mid(x)) for x in row] for row in j]);fm=mp.matrix([mp.mpf(decimal_mid(x)) for x in f])
  step=mp.lu_solve(jm,fm)
  xs=[mp.nstr(mp.mpf(str(x))-v,48) for x,v in zip(xs,step)]
 return xs

def krawczyk(center,radius):
 from decimal import Decimal
 if len(center)!=9 or any(not Decimal(str(c)).is_finite() for c in center):raise ValueError('nine finite coordinates required')
 if not Decimal(str(radius)).is_finite() or Decimal(str(radius))<=0:raise ValueError('positive finite radius required')
 n=len(center);rad=I(radius);X=[I(c)+iv.mpf([-rad.b,rad.b]) for c in center]
 f,j0,*_=system(center);_,jx,m,cu,signs=system(X)
 from mpmath import mp
 mp.dps=55
 inv=mp.inverse(mp.matrix([[mp.mpf(decimal_mid(x))for x in row]for row in j0]))
 C=[[I(mp.nstr(inv[i,j],48)) for j in range(n)]for i in range(n)]
 R=minus(eye(n),mm(C,jx));offset=[-v for v in mv(C,f)];dev=mv(R,[iv.mpf([-rad.b,rad.b])]*n);K=[a+b for a,b in zip(offset,dev)]
 inside=all(v.a>-rad.a and v.b<rad.a for v in K)
 contraction=max(sum((abs(v) for v in row),I(0)).b for row in R)<1
 return dict(certified=bool(inside and contraction),center=center,radius=radius,krawczyk_offset=[bounds(v)for v in K],offset_display=[display(v) for v in K],jacobian_contraction_bound_display=max(float(sum((abs(v)for v in row),I(0)).b)for row in R),strict_inclusion=bool(inside),all_jacobians_nonsingular=bool(contraction),curvature_display=[display(v.v)for v in cu],slew_signs=signs),X,m

if __name__=='__main__':
 center=refine([str(x)for x in BASE['z']]);print('refined center',center,flush=True)
 out=[]
 for rad in ['1e-9','1e-10','1e-11']:
  r,X,m=krawczyk(center,rad);out.append(r);print(rad,r['certified'],r['jacobian_contraction_bound_display'],flush=True)
 (HERE/'root_attempts.json').write_text(json.dumps(out,indent=2)+'\n')
