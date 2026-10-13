"""First-order interval automatic differentiation in one condition parameter.
Mean-value form preserves cross-coefficient cancellation before multiplying delta.
All operations enclose exact real arithmetic; no finite-difference proof step.
"""
from box_certifier import *
class Dual:
 def __init__(self,v,d=0):self.v=v if hasattr(v,'a') else I(v);self.d=d if hasattr(d,'a') else I(d)
 def __add__(self,b):
  b=dual(b);return Dual(self.v+b.v,self.d+b.d)
 __radd__=__add__
 def __neg__(self):return Dual(-self.v,-self.d)
 def __sub__(self,b):return self+-dual(b)
 def __rsub__(self,b):return dual(b)+-self
 def __mul__(self,b):
  b=dual(b);return Dual(self.v*b.v,self.d*b.v+self.v*b.d)
 __rmul__=__mul__
 def __truediv__(self,b):
  b=dual(b);return Dual(self.v/b.v,(self.d*b.v-self.v*b.d)/(b.v*b.v))
 def __rtruediv__(self,b):return dual(b)/self
 def __pow__(self,n):return Dual(self.v**n,n*self.v**(n-1)*self.d)
 def sqrt(self):
  v=iv.sqrt(self.v);return Dual(v,self.d/(2*v))
def dual(x):return x if isinstance(x,Dual)else Dual(x)

def dual_coeff(q,w):
 def vel(z,track):
  gam=-I('3.1')*iv.pi/180;chi=I(track)*iv.pi/180;V=I(153)*I(1852)/3600*iv.exp(I(z)/17000);d=[iv.cos(chi),iv.sin(chi)]
  wd=w[0]*d[0]+w[1]*d[1];gs=wd+(dual((V*iv.cos(gam))**2)-w[0]**2-w[1]**2+wd**2).sqrt()
  return [gs*d[0],gs*d[1],dual(V*iv.sin(gam))]
 v0=vel(146,-47);vg=vel('21.24',0);bump=[0,0,0,64,-192,192,-64,0];odd=[0,0,0,-64,320,-576,448,-128];ph=[]
 for idx,(p0,p1,a,b,T)in enumerate([([-2500,1000,146],[0,0,'21.24'],v0,vg,q[0]),([0,0,'21.24'],[q[2],0,6],vg,[q[3],dual(0),dual('-.7')],q[1])]):
  cs=[]
  for j in range(3):
   c0=dual(p0[j]);c1=T*a[j];A=dual(p1[j])-c0-c1;B=T*b[j]-c1
   c=[c0,c1,dual(0),A*10-B*4,A*(-15)+B*7,A*6-B*3,dual(0),dual(0)]
   even=q[4+2*j]if idx==0 else q[10]if j==0 else q[11]if j==2 else dual(0);oa=q[5+2*j]if idx==0 else dual(0)
   cs.append([x+even*y+oa*z for x,y,z in zip(c,bump,odd)])
  ph.append(cs)
 return ph

def prepare(qcenter,qderiv,case,delta):
 rad=I(delta);ds=iv.mpf([-rad.b,rad.b]);q=[Dual(I(repr(float(v)))+I(repr(float(d)))*ds,I(repr(float(d)))) for v,d in zip(qcenter,qderiv)]
 wind=[Dual(I(repr(float(case.p['wind_mps'][0])))+ds,1),Dual(repr(float(case.p['wind_mps'][1]))),Dual(0)]
 dc=dual_coeff(q,wind);base,W=coeff([I(repr(float(v)))for v in qcenter],case.p['wind_mps'])
 def kin(cs,T,l,r,phase):
  if len(cs[0])<=2:return [[ic.poly(ic.deriv(c,k),l,r)/T**k for c in cs] for k in range(4)]
  result=[]
  for k in range(4):
   row=[]
   for j in range(3):
    val=ic.poly(ic.deriv(base[phase][j],k),l,r)/I(repr(float(qcenter[phase])))**k
    dcval=ic.poly(ic.deriv([c.d for c in dc[phase][j]],k),l,r)/q[phase].v**k
    if k:dcval-=k*ic.poly(ic.deriv([c.v for c in dc[phase][j]],k),l,r)*q[phase].d/q[phase].v**(k+1)
    row.append(val+ds*dcval)
   result.append(row)
  return result
 return kin
