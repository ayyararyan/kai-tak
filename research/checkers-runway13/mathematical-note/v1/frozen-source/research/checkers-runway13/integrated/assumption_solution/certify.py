"""Conditional all-time verification; interval helpers from preserved checker.
Uses its force law at the actual CG, but new exact coefficients, wind, corridor,
scene/contact predicates and binding receipts. No old certificate is reused.
"""
from conditional_model import *
import hashlib,time
from fractions import Fraction
from counterfactual import continuous as ic
from mpmath import iv
I=ic.I;Z=ic.Z

def coeff(q,wind):
 W=[I(repr(float(x))) for x in wind]
 def velocity(z,track):
  gam=-I('3.1')*iv.pi/180;chi=I(track)*iv.pi/180;V=I(153)*I(1852)/3600*iv.exp(I(z)/17000)
  d=[iv.cos(chi),iv.sin(chi)];wd=ic.dot(W[:2],d)
  gs=wd+iv.sqrt((V*iv.cos(gam))**2-ic.dot(W[:2],W[:2])+wd**2)
  return [gs*d[0],gs*d[1],V*iv.sin(gam)]
 v0=velocity(146,-47);vg=velocity('21.24',0)
 bump=[0,0,0,64,-192,192,-64,0];odd=[0,0,0,-64,320,-576,448,-128];ph=[]
 for idx,(p0,p1,w0,w1,T) in enumerate([([-2500,1000,146],[0,0,'21.24'],v0,vg,q[0]),([0,0,'21.24'],[q[2],0,6],vg,[q[3],Z,-I('.7')],q[1])]):
  cs=[]
  for j in range(3):
   c0=p0[j] if hasattr(p0[j],'a') else I(p0[j]);end=p1[j] if hasattr(p1[j],'a') else I(p1[j]);c1=T*w0[j]
   A=end-c0-c1;B=T*w1[j]-c1
   c=[c0,c1,Z,10*A-4*B,-15*A+7*B,6*A-3*B,Z,Z]
   even=q[4+2*j] if idx==0 else(q[10] if j==0 else q[11] if j==2 else Z);oa=q[5+2*j] if idx==0 else Z
   cs.append([x+even*b+oa*o for x,b,o in zip(c,bump,odd)])
  ph.append(cs)
 return ph,W

def maxiv(a,b):return iv.mpf([max(a.a,b.a),max(a.b,b.b)])
def quotient_one_minus(c):
 # exact endpoint-zero polynomial p(s)=(1-s)g(s), in interval coefficient algebra.
 out=[];v=Z
 for x in c[:-1]:v+=x;out.append(v)
 return out

def geometry_cell(case,cs,T,l,r,phase):
 kin=[[ic.poly(ic.deriv(c,k),l,r)/T**k for c in cs] for k in range(4)]
 pos,v,a,j=kin;W=[I(repr(float(x))) for x in case.p['wind_mps']];va=[x-y for x,y in zip(v,W)];V=ic.norm(va);H=ic.norm(va[:2]);et=[x/V for x in va];er=[-va[1]/H,va[0]/H,Z];eu=ic.cross(et,er)
 F=[I('238461.67357166')*(x+(I('9.80665') if k==2 else Z)) for k,x in enumerate(a)];lu=ic.dot(F,eu);lr=ic.dot(F,er);L=ic.norm([lu,lr]);sinabs=abs(lr/L);cos=lu/L
 low=pos[2]-maxiv(4*cos+I('32.7')*sinabs,6*cos+I('6.0579')*sinabs)
 rad=I(55)+I(case.buffer);vals={}
 x=pos[0];y=pos[1]
 for idx,ob in enumerate(SCENE['obstacles']):
  xmin,ymin,xmax,ymax=[I(v) for v in ob['bounds_xy']];dx=I(case.frame_dx);dy=I(case.frame_dy)
  h=maxiv(maxiv(xmin+dx-x,x-xmax-dx),maxiv(ymin+dy-y,y-ymax-dy))-rad
  vals[f'object_{idx}']=maxiv(h,low-I(ob['top_hkpd_assumed_m'])+I(case.runway_level)-I(case.roof_delta)-3)
 x=x-I(case.frame_dx);y=y-I(case.frame_dy)
 vals['urban_upstream']=maxiv(x-rad+600,low-I(case.urban)-3)
 for sign in [-1,1]:vals[f'urban_side_{sign}']=maxiv(maxiv(maxiv(-600-x,x),100-sign*y)-rad,low-I(case.urban)-3)
 vals['nongear_ground']=pos[2]-4*cos-I('32.7')*sinabs-I('.5')
 # Sufficient factored gear nonpenetration: 6-6cos>=0 for real rotation.
 # For flare, ay=0 and ax(1)=0; sin(phi)/(1-s) = m*wy*(ax/(1-s))/(H*L).
 if phase==1:
  hc=cs[2].copy();hc[0]-=6
  hf=ic.poly(quotient_one_minus(hc),l,r)
  ac=[x/T**2 for x in ic.deriv(cs[0],2)]
  af=ic.poly(quotient_one_minus(ac),l,r)
  vals['gear_factored']=hf-I('6.0579')*I('238461.67357166')*abs(W[1]*af)/(H*L)
 else:vals['gear_ground']=pos[2]-6*cos-I('6.0579')*sinabs
 return vals,kin

def certify_case(case,q,eta,maxdepth=20):
 case.curves(q)
 if any(not lo<=float(v)<=hi for v,(lo,hi) in zip(q,tr.BOUNDS)):raise ValueError('exact decision outside family')
 if not np.isfinite(float(eta)) or not 0<=float(eta)<.5:raise ValueError('certificate margin domain')
 if not isinstance(maxdepth,int) or isinstance(maxdepth,bool) or not 0<=maxdepth<=30:raise ValueError('depth domain')
 expected=copy.deepcopy(BASE);expected['wind_mps']=case.p['wind_mps']
 if case.p!=expected:raise ValueError('unsupported force-parameter substitution')
 if not np.array_equal(np.load(OUT/'reference_cloud.npy'),TREE.data):raise ValueError('reference point cloud changed')
 qstr=[repr(float(v)) for v in q];qs=[I(v) for v in qstr];cs,W=coeff(qs,case.p['wind_mps']);ic.W=W
 stop=qs[2]+2*qs[3]+qs[3]**2/(2*I('1.4709975'))
 terminal={'touchdown_x_lower':(qs[2]-200)/500,'touchdown_x_upper':(700-qs[2])/500,'stop':(2636-stop)/2636,'sink_lower':I('.7')/I('1.5'),'sink_upper':I('.8')/I('1.5')}
 if not all(v.a>=I(eta).b for v in terminal.values()):return dict(certified=False,reason='terminal margin')
 # Entire rollout occupies one straight segment at fixed level pose. Gear contact
 # is structurally exact (zCG=6, roll=pitch=0); do not test cancellation noise.
 ground,unused=geometry_cell(case,[[qs[2],stop-qs[2]],[Z],[I(6)]],I(1),0,1,0)
 ground['gear_ground']=Z
 if not all(v.a>=0 for v in ground.values()):return dict(certified=False,reason='rollout geometry unresolved')
 accepted=[];mins={};geommins={};processed=0;start=time.monotonic()
 for ph in range(2):
  stack=[(0.,1.,0)]
  while stack:
   l,r,dep=stack.pop();processed+=1
   try:
    geo,kin=geometry_cell(case,cs[ph],qs[ph],l,r,ph)
    m,hard,dom=ic.enclose(cs[ph],qs[ph],l,r,0,TREE,kinematics=kin)
    if ph==1:m.pop('approach_sink',None)
    okay=hard and all(v.a>=I(eta).b for v in m.values()) and all(v.a>=0 for v in geo.values())
   except (ValueError,ZeroDivisionError):okay=False
   if okay:
    accepted.append([ph,l,r,dep])
    for key,v in m.items():mins[key]=min(mins.get(key,1e99),float(v.a))
    for key,v in geo.items():geommins[key]=min(geommins.get(key,1e99),float(v.a))
   elif dep>=maxdepth:
    return dict(certified=False,reason='interval_unresolved_not_infeasibility',unresolved=[ph,l,r,dep],processed=processed)
   else:
    mid=(l+r)/2;stack.extend([(mid,r,dep+1),(l,mid,dep+1)])
 return dict(certified=True,eta_lower_real_decimal=eta,q_real_decimal=qstr,condition=case.parameters(),cover=accepted,processed=processed,force_minima_display=mins,geometry_minima_display=geommins,rollout_geometry_minima_display={k:float(v.a) for k,v in ground.items()},stop_display=[float(stop.a),float(stop.b)],seconds=time.monotonic()-start,historical_certified=False,global_optimum=False,domain='assumed scene/pose/force law and exact real-decimal q; continuous flight plus analytic straight rollout')

def bind(result):
 result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'conditional_model.py',OUT/'forces.py',OUT/'certify.py',OUT/'scene.json',OUT/'reference_cloud.npy',ROOT/'counterfactual/continuous.py',ROOT/'model/config.json',ROOT/'model/trajectory.py']}
 return result

if __name__=='__main__':
 for path in sorted((OUT/'cases').glob('*/result.json')):
  result=json.loads(path.read_text());p=result['condition'];c=Case(p['name'],p['wind_mps'],p['urban'],p['roof_delta'],p['frame_dx'],p['frame_dy'],p['runway_level'],p['buffer'])
  q=result['selected']['q'];eta=repr(max(0,result['selected']['eta']-.003))
  receipt=bind(certify_case(c,q,eta));receipt['result_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  (path.parent/'continuous.json').write_text(json.dumps(receipt,indent=2)+'\n');print(c.name,{k:v for k,v in receipt.items() if k in ['certified','reason','processed','seconds','unresolved','eta_lower_real_decimal']},flush=True)
