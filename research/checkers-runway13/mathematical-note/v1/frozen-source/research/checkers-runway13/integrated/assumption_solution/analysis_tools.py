from conditional_model import *
from scipy.integrate import solve_ivp
from fractions import Fraction as F
from mpmath import iv
from counterfactual.continuous import I

def terminal_interval_bound(case):
 wx,wy,_=[I(repr(float(x))) for x in case.p['wind_mps']];k=I(1852)/3600*iv.exp(I(6)/17000);a=I('1.4709975')
 def f(eta,family=False):
  e=I(eta.numerator)/I(eta.denominator);u=wx+iv.sqrt((k*(135+40*e))**2-wy**2-I('.7')**2)
  if family:u=iv.mpf([max(u.a,I(69).a),max(u.b,I(69).b)])
  return 200+500*e+2*u+u**2/(2*a)-2636*(1-e)
 results={}
 for family in [False,True]:
  lo,hi=F(0),F(45,100)
  if f(lo,family).a>0:results['family' if family else 'full']=dict(nonnegative_margin_impossible=True);continue
  if f(hi,family).b<=0:results['family' if family else 'full']=dict(upper_exact=str(hi),reason='entry EAS lower margin');continue
  for _ in range(48):
   mid=(lo+hi)/2;v=f(mid,family)
   if v.b<0:lo=mid
   elif v.a>0:hi=mid
   else:break
  results['family' if family else 'full']=dict(lower_root_exact=str(lo),upper_exact=str(hi),upper_display=float(hi),lower_F_upper_display=float(f(lo,family).b),upper_F_lower_display=float(f(hi,family).a),proof='outward interval residual signs, strict monotonicity and initial EAS cap; lower root is not a feasible-trajectory bound')
 return results

def replay(case,q):
 cs=case.curves(q);p=case.p
 initial=np.r_[[c(0) for c in cs[0]],[c.deriv()(0)/q[0] for c in cs[0]]]
 pe=ve=0.;end=initial
 for polys,T in zip(cs,q[:2]):
  def rhs(t,state):
   u=phase(polys,T,np.array([min(1,max(0,t/T))]),p);v=state[3:]-p['wind_mps'];V=np.linalg.norm(v);et=v/V;H=np.linalg.norm(v[:2]);er=np.array([-v[1]/H,v[0]/H,0]);eu=np.cross(et,er)
   dynamic=.5*p['rho0_kg_m3']*np.exp(-state[2]/8500)*V*V*p['wing_area_m2'];CL=u['cl'][0];L=dynamic*CL;D=dynamic*(.08+.045*CL*CL);bank=u['bank'][0]
   acc=((u['thrust'][0]-D)*et+L*(np.cos(bank)*eu+np.sin(bank)*er))/p['mass_kg']-[0,0,tr.G]
   return np.r_[state[3:],acc]
  t=np.linspace(0,T,301);sol=solve_ivp(rhs,(0,T),end,method='DOP853',t_eval=t,rtol=2e-11,atol=2e-12,max_step=.3)
  if not sol.success:raise RuntimeError(sol.message)
  ref=np.column_stack([c(t/T) for c in polys]);vel=np.column_stack([c.deriv()(t/T)/T for c in polys]);pe=max(pe,float(np.max(np.linalg.norm(sol.y[:3].T-ref,axis=1))));ve=max(ve,float(np.max(np.linalg.norm(sol.y[3:].T-vel,axis=1))));end=sol.y[:,-1]
 return dict(passed=pe<1e-5 and ve<1e-5,max_position_error_m=pe,max_velocity_error_mps=ve,method='independent6-state Newton integration with reference CL,T,bank; lift/drag recomputed from replayed state',terminal_cg_state=end.tolist())

def fixed_gate(case):
 p=case.p;v=tr.endpoint_velocity(153,21.24,0,-3.1,p)
 d={'pos':np.array([[0.,0.,21.24]]),'bank':np.array([0.])}
 geo=case.geometry(d);mins={k:float(v[0]) for k,v in geo.items()};bad={k:v for k,v in mins.items() if v<0}
 return dict(feasible_under_imposed_gate_constraints=not bool(bad),violations_m=bad,proof='Fixed threshold CG(0,0,21.24), zero endpoint acceleration ->bank0 for horizontal wind. These constraints do not depend on path decisions. Negative gap excludes every path in this conservative conditional model, not every physical landing.')
