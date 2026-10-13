"""Root, simplex, active extrema and full hybrid path certificate producer."""
from interval_root import *
import box_certifier as bc
from mpmath import mp
import time,hashlib

def check_preserved():
 snapshot=json.loads((HERE/'preserved_snapshot.json').read_text())
 for name,v in snapshot.items():
  p=bc.ROOT/name
  if p.stat().st_size!=v['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:raise ValueError('preserved input changed: '+name)
 return len(snapshot)

def simplex(m):
 A=[[m[j].d[k]for j in range(6)]for k in range(5)]+[[I(1)]*6]
 mp.dps=55;Am=mp.matrix([[mp.mpf(decimal_mid(x))for x in row]for row in A]);cm=Am**-1
 C=[[I(mp.nstr(cm[i,j],48))for j in range(6)]for i in range(6)]
 R=minus(eye(6),mm(C,A));rnorm=max(sum((abs(v)for v in row),I(0)).b for row in R)
 if rnorm>=1:return dict(certified=False,reason='simplex contraction failed')
 b=[I(0)]*5+[I(1)];approx=mv(C,b);residual=mv(C,[x-y for x,y in zip(b,mv(A,approx))])
 eps=max(abs(x).b for x in residual)/(1-rnorm)
 weights=[v+iv.mpf([-eps.b,eps.b])for v in approx]
 return dict(certified=bool(rnorm<1 and all(v.a>0 for v in weights)),contraction_display=float(rnorm),multiplier_enclosures=[bounds(v)for v in weights],multiplier_display=[display(v)for v in weights])

def events(X,width):
 z=variables(X);w=I(width);zones=[]
 for index,key in [(6,'slew'),(7,'load_upper'),(8,'thrust_lower')]:
  mid=midpoint(X[index]);a=mid-w;b=mid+w
  # Bounds as real decimal rationals enclosing the selected interval.
  left=float(a.a);right=float(b.b)
  left=np.nextafter(left,-np.inf);right=np.nextafter(right,np.inf)
  th,ld,T=state(z,D(iv.mpf([I(repr(float(left))).a,I(repr(float(right))).b])))
  if key=='slew':
   sv=th.c[1].v/T.v;sgn=1 if sv.a>0 else -1 if sv.b<0 else 0
   curv=-sgn*6*th.c[3].v/T.v/100000
   ok=sgn!=0 and curv.a>0
  elif key=='load_upper':curv=-2*ld.c[2].v/I('.9');ok=curv.a>0
  else:curv=2*th.c[2].v/700000;ok=curv.a>0
  ok=ok and X[index].a>left and X[index].b<right
  zones.append(dict(key=key,left=left,right=right,kind='strict_convex_minimum',curvature_display=display(curv),certified=bool(ok)))
 for left,right,sgn_expected in [(0.,float(width),1),(1-float(width),1.,-1)]:
  th,ld,T=state(z,D(iv.mpf([I(repr(left)).a,I(repr(right)).b])));sv=th.c[1].v/T.v;sgn=1 if sv.a>0 else -1 if sv.b<0 else 0
  slope=-sgn*2*th.c[2].v/T.v/100000
  ok=sgn!=0 and (slope.a>0 if sgn_expected==1 else slope.b<0)
  zones.append(dict(key='slew',left=left,right=right,kind='one_sided_endpoint_minimum',slope_display=display(slope),certified=bool(ok)))
 return zones

def full_path(X,zones,maxdepth=24):
 assert all(v['certified']for v in zones)
 q=[I(str(v)) for v in BASE['q']]
 for k,i in enumerate([1,2,3,10,11]):q[i]=X[k]*SCALE[k]
 for v,(a,b)in zip(q,bc.tr.BOUNDS):assert v.a>=a and v.b<=b
 c=Case();cs,W=bc.coeff(q,c.p['wind_mps']);ic.W=W;bc.parameter_kin=None
 eta=X[5];stop=q[2]+2*q[3]+q[3]**2/(2*I('1.4709975'))
 term={'touchdown_x_lower':(q[2]-200)/500,'touchdown_x_upper':(700-q[2])/500,'sink_lower':I('.7')/I('1.5'),'sink_upper':I('.8')/I('1.5')}
 assert all(v.a>eta.b for v in term.values())
 ground,_=bc.geometry_cell(c,[[q[2],stop-q[2]],[I(0)],[I(6)]],I(1),0,1,0);ground['gear_ground']=I(0)
 assert all(v.a>=0 for v in ground.values())
 cover=[];mins={};geo_min={};processed=0;started=time.monotonic()
 for ph in [0,1]:
  cuts=[0.,1.] if ph==0 else sorted(set([0.,1.]+[v[x]for v in zones for x in ['left','right']]))
  stack=[(a,b,0)for a,b in reversed(list(zip(cuts,cuts[1:])))]
  while stack:
   a,b,d=stack.pop();processed+=1
   try:
    geo,kin=bc.geometry_cell(c,cs[ph],q[ph],a,b,ph)
    marg,hard,dom=ic.enclose(cs[ph],q[ph],a,b,0,bc.TREE,kinematics=kin)
    omitted=[]
    if ph==1:
     marg.pop('approach_sink',None)
     for zone in zones:
      if a>=zone['left'] and b<=zone['right']:
       marg.pop(zone['key'],None);omitted.append(zone['key'])
    ok=hard and all(v.a>eta.b for v in marg.values()) and all(v.a>=0 for v in geo.values())
   except (ValueError,ZeroDivisionError):ok=False
   if ok:
    cover.append([ph,a,b,d,omitted])
    for k,v in marg.items():mins[k]=min(mins.get(k,1e100),float((v-eta).a))
    for k,v in geo.items():geo_min[k]=min(geo_min.get(k,1e100),float(v.a))
   elif d>=maxdepth:
    return dict(certified=False,unresolved=[ph,a,b,d],processed=processed,cover=cover,force_failure={k:display(v-eta)for k,v in marg.items()if v.a<=eta.b},geometry_failure={k:display(v)for k,v in geo.items()if v.a<0},seconds=time.monotonic()-started)
   else:
    mid=(a+b)/2;stack.extend([(mid,b,d+1),(a,mid,d+1)])
 return dict(certified=True,cover=cover,processed=processed,strict_force_slack_display=mins,geometry_minima_display=geo_min,stop_display=display(stop),terminal_slack_display={k:display(v-eta)for k,v in term.items()},seconds=time.monotonic()-started,q_box_display=[display(v)for v in q],note='Stop equality follows from root F0=0; active neighborhoods from strict curvature/one-sided slopes; all other inequalities interval checked.')

if __name__=='__main__':
 check_preserved()
 center=refine([str(v)for v in BASE['z']]);r,X,m=krawczyk(center,'1e-20');print('root',r['certified'],flush=True)
 out={'root':r,'simplex':simplex(m),'event_attempts':[]};print('simplex',out['simplex'],flush=True)
 for width in ['.01','.005','.002','.001']:
  zones=events(X,width);out['event_attempts'].append(dict(width=width,zones=zones));print('events',width,[v['certified']for v in zones],flush=True)
  if all(v['certified']for v in zones):break
 (HERE/'certificate.json').write_text(json.dumps(out,indent=2)+'\n')
 if r['certified']and out['simplex']['certified']and all(v['certified']for v in zones):
  out['path']=full_path(X,zones);print('path',out['path']['certified'],out['path'].get('unresolved'),out['path']['processed'],flush=True)
  (HERE/'certificate.json').write_text(json.dumps(out,indent=2)+'\n')
