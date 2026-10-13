from pathlib import Path
import sys,json,math
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from energy_bound import *
HERE=Path(__file__).resolve().parent

def data(case,e):
 expected=copy.deepcopy(BASE);expected['wind_mps']=case.p['wind_mps']
 if case.p!=expected:raise ValueError('unsupported force substitution')
 if not np.isfinite(float(e)) or not 0<=float(e)<=.45:raise ValueError('margin domain')
 e=I(str(e));wx,wy,_=[I(repr(float(x))) for x in case.p['wind_mps']];k=I(1852)/3600;m=I('238461.67357166');g=I('9.80665');a=I('1.4709975')
 vm=(135+40*e)*k;vp=(175-40*e)*k;Vmin=vm*iv.exp(I(6)/17000);Vmax=vp*iv.exp(I(34)/17000)
 Qlo=I('.5')*I('1.225')*vm**2*I('541.2');Qhi=I('.5')*I('1.225')*vp**2*I('541.2');L=m*g*(I('1.4')-I('.9')*e)
 D=ivmax(I('.08')*Qlo+I('.045')*L**2/Qlo,I('.08')*Qhi+I('.045')*L**2/Qhi)
 umin=wx+iv.sqrt(Vmin**2-wy**2-22**2)
 if umin.a<=0:raise ValueError('positive speed required')
 # Ratio r(u)^2=1-2wx/u+(wx²+wy²+22²)/u²; no interior maximum on u>=umin.
 ratio=ivmax(I(1),iv.sqrt((umin-wx)**2+wy**2+22**2)/umin)
 C=2*ivmax(I(0),D-700000*e)*ratio/m
 gam=I('3.1')*iv.pi/180;Qg=I('.5')*I('1.225')*(153*k)**2*I('541.2');Lg=m*g*iv.cos(gam)
 Tg=-m*g*iv.sin(gam)+I('.08')*Qg+I('.045')*Lg**2/Qg
 A=ivmax(I(0),Tg-700000*e);K=100000*(1-e)
 R=(153*k*iv.exp(I('21.24')/17000))**2+2*g*I('15.24')-wy**2-I('.7')**2
 u0=ivmax(I(69),wx+iv.sqrt(Vmin**2-wy**2-I('.7')**2))
 return e,wx,m,a,C,R,u0,A,K,Vmin,Vmax

def exclusion(case,eta,cells=2048,ramp=True):
 if not isinstance(cells,int) or isinstance(cells,bool) or cells<1:raise ValueError('cell count')
 e,wx,m,a,C,R,u0,A,K,Vmin,Vmax=data(case,eta);left=200+500*e;right=700-500*e;lowest=math.inf
 for i in range(cells):
  lo=left+(right-left)*I(i)/cells;hi=left+(right-left)*I(i+1)/cells;x=iv.mpf([lo.a,hi.b])
  tmin=ivmax(I(4),x/(wx+Vmax))
  # F(t)= integral_0^t max(A-Ks,0) ds, monotonically nondecreasing.
  z=iv.mpf([min(tmin.a,(A/K).a),min(tmin.b,(A/K).b)])
  bonus=2*Vmin/m*(A*z-K*z*z/2) if ramp else I(0)
  u=ivmax(u0,wx+iv.sqrt(ivmax(I(0),R-C*x+bonus)))
  gap=x+2*u+u*u/(2*a)-2636*(1-e);lowest=min(lowest,float(gap.a))
  if gap.a<=0:return dict(excluded=False,eta=eta,first_unresolved_cell=i,cells=cells)
 return dict(excluded=True,eta_upper_real_decimal=eta,cells=cells,residual_lower_display_m=lowest,C_display=float(C.b),ramp=ramp,scope='frozen polynomial family only')

def bound(c):
 lo=0.;hi=.3
 for _ in range(13):
  mid=(lo+hi)/2;p=exclusion(c,f'{mid:.9f}',256)
  if p['excluded']:hi=mid
  else:lo=mid
 return exclusion(c,f'{hi:.9f}',4096)
if __name__=='__main__':
 results={}
 for c in [Case(),Case('tailwind5',wind=(5*tr.KT,0,0)),Case('calm',wind=(0,0,0))]:
  results[c.name]=bound(c);results[c.name]['eta_zero_exclusion']=exclusion(c,'0',2048);print(c.name,results[c.name],flush=True)
 (HERE/'strong_bound.json').write_text(json.dumps(results,indent=2)+'\n')
