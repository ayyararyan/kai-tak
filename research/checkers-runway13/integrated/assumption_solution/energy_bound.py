"""Exact-regime scalar relaxation plus interval-certified family exclusions.
Conservative |vz|<=22 and flareCGheight<=34 derived in DERIVATION section8.
"""
from conditional_model import *
from mpmath import iv
from fractions import Fraction as F
import hashlib
from counterfactual.continuous import I

def constants(case,eta):
 wx,wy,_=case.p['wind_mps'];m=case.p['mass_kg'];a=1.4709975;k=tr.KT
 vmin=(135+40*eta)*k;vmax=(175-40*eta)*k
 qs=[.5*1.225*v*v*541.2 for v in [vmin,vmax]];L=m*tr.G*(1.4-.9*eta)
 drag=max(.08*Q+.045*L*L/Q for Q in qs)
 ug=wx+np.sqrt((vmin*np.exp(6/17000))**2-wy*wy-22**2)
 if ug<=0:raise ValueError('energy-bound forward speed domain')
 C=2*max(0,drag-700000*eta)/m*vmax*np.exp(34/17000)/ug
 R=(153*k*np.exp(21.24/17000))**2+2*tr.G*15.24-wy*wy-.7**2
 u0=max(69,wx+np.sqrt((vmin*np.exp(6/17000))**2-wy*wy-.7**2))
 return C,R,u0

def scalar_minimum(case,eta):
 C,R,u0=constants(case,eta);wx=case.p['wind_mps'][0];a=1.4709975
 xl=200+500*eta;xh=700-500*eta;B=2+wx/a
 cand=[('left_endpoint',xl),('right_endpoint',xh)]
 if C>0:
  cross=(R-(u0-wx)**2)/C
  if xl<=cross<=xh:cand.append(('speed_floor_switch',cross))
  den=2-C/a
  if den!=0:
   root=B*C/den
   x=(R-root*root)/C
   if root>0 and xl<=x<=xh and wx+root>=u0:cand.append(('energy_stationary',x))
 def stop(x):
  u=max(u0,wx+np.sqrt(max(0,R-C*x)));return x+2*u+u*u/(2*a)
 values=[dict(regime=kind,x_m=x,stop_m=float(stop(x)))for kind,x in cand]
 best=min(values,key=lambda r:r['stop_m'])
 return dict(best=best,candidates=values,residual=best['stop_m']-2636*(1-eta),C=C,R=R,U0=u0)

def ivmax(x,y):return iv.mpf([max(x.a,y.a),max(x.b,y.b)])
def exclusion(case,eta_string,cells=2048):
 e=I(eta_string);wx,wy,_=[I(repr(float(x)))for x in case.p['wind_mps']];m=I('238461.67357166');a=I('1.4709975');k=I(1852)/3600
 vmin=(135+40*e)*k;vmax=(175-40*e)*k;Qlo=I('.5')*I('1.225')*vmin**2*I('541.2');Qhi=I('.5')*I('1.225')*vmax**2*I('541.2');L=m*I('9.80665')*(I('1.4')-I('.9')*e)
 drag=ivmax(I('.08')*Qlo+I('.045')*L**2/Qlo,I('.08')*Qhi+I('.045')*L**2/Qhi)
 ug=wx+iv.sqrt((vmin*iv.exp(I(6)/17000))**2-wy**2-22**2)
 if ug.a<=0:raise ValueError('interval speed domain')
 C=2*ivmax(I(0),drag-700000*e)/m*vmax*iv.exp(I(34)/17000)/ug
 R=(153*k*iv.exp(I('21.24')/17000))**2+2*I('9.80665')*I('15.24')-wy**2-I('.7')**2
 u0=ivmax(I(69),wx+iv.sqrt((vmin*iv.exp(I(6)/17000))**2-wy**2-I('.7')**2))
 left=200+500*e;right=700-500*e;lowest=math.inf
 for i in range(cells):
  lo=left+(right-left)*I(i)/cells;hi=left+(right-left)*I(i+1)/cells;x=iv.mpf([lo.a,hi.b])
  energy=wx+iv.sqrt(ivmax(I(0),R-C*x));u=ivmax(u0,energy)
  gap=x+2*u+u*u/(2*a)-2636*(1-e)
  lowest=min(lowest,float(gap.a))
  if gap.a<=0:return dict(excluded=False,first_unresolved_cell=i,eta=eta_string,cells=cells)
 return dict(excluded=True,eta_upper_real_decimal=eta_string,cells=cells,residual_lower_display_m=lowest,scope='entire frozen12-dimensionalfamily at eta and above; flareenergy relaxation plus exact interval x cover',historical_certified=False)

def bound(case):
 f=lambda e:scalar_minimum(case,e)['residual']
 if f(0)>0:root=0
 elif f(.45)<=0:return dict(status='no_stronger_upper',estimate=.45)
 else:root=brentq(f,0,.45,xtol=1e-13)
 # Upward rounded comparison value; interval proof, not the rounding, validates it.
 eta=math.ceil((root+.0002)*1e6)/1e6
 proof=exclusion(case,f'{eta:.6f}')
 if not proof['excluded']:
  eta+=.001;proof=exclusion(case,f'{eta:.6f}',4096)
 return dict(estimate=root,scalar_relaxation_at_root=scalar_minimum(case,root),exclusion=proof,exact_optimum=False)

if __name__=='__main__':
 from export import make_case
 for path in sorted((OUT/'cases').glob('*/result.json')):
  r=json.loads(path.read_text());c=make_case(r['condition']);b=bound(c);b['condition']=c.parameters();b['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'energy_bound.py',OUT/'conditional_model.py',OUT/'regularity.py',OUT/'regularity.json',ROOT/'model/config.json']}
  (path.parent/'energy_bound.json').write_text(json.dumps(b,indent=2)+'\n');print(c.name,b['estimate'],b.get('exclusion'),flush=True)
