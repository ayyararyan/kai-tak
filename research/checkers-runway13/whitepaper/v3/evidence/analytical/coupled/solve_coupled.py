"""Coupled continuous-model candidate search. Finite search is NOT a proof.

Preserves v1 parameter family and all margins; uses analytic rates, both joins.
Does not modify or supersede the sampled v1 executable.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import json
import numpy as np
from scipy.optimize import minimize
from model import trajectory as tr
from model.solve import SCALE
from analytical.verify_full_landing_analysis import curves

CFG=tr.load_config()
P=tr.values(CFG)
EV=tr.Evaluator(CFG)

def phase(polys,T,s):
    r,v,a,j=[np.column_stack([z.deriv(k)(s)/T**k for z in polys]) for k in range(4)]
    va=v-np.array(P['wind_mps']); V=np.linalg.norm(va,axis=1); et=va/V[:,None]
    h=np.linalg.norm(va[:,:2],axis=1)
    er=np.column_stack([-va[:,1]/h,va[:,0]/h,np.zeros(len(s))]); eu=np.cross(et,er)
    F=P['mass_kg']*(a+[0,0,tr.G]); Fd=P['mass_kg']*j
    dot=lambda x,y:np.sum(x*y,axis=1)
    lu,lr=dot(F,eu),dot(F,er); L=np.hypot(lu,lr)
    vd=dot(et,a); etd=(a-et*vd[:,None])/V[:,None]
    psid=(va[:,0]*a[:,1]-va[:,1]*a[:,0])/h**2
    erd=-psid[:,None]*np.column_stack([va[:,0]/h,va[:,1]/h,np.zeros(len(s))])
    eud=np.cross(etd,er)+np.cross(et,erd)
    lud,lrd=dot(Fd,eu)+dot(F,eud),dot(Fd,er)+dot(F,erd)
    roll=(lu*lrd-lr*lud)/L**2
    ld=(lu*lud+lr*lrd)/L
    Q=.5*P['rho0_kg_m3']*np.exp(-r[:,2]/P['density_scale_m'])*V**2*P['wing_area_m2']
    cl=L/Q; qd=Q*(-v[:,2]/P['density_scale_m']+2*vd/V); cld=ld/Q-cl*qd/Q
    drag=Q*(P['cd0']+P['induced_factor']*cl**2)
    dd=qd*(P['cd0']+P['induced_factor']*cl**2)+2*Q*P['induced_factor']*cl*cld
    thrust=drag+dot(F,et); slew=dd+dot(Fd,et)+dot(F,etd)
    return dict(pos=r,vel=v,acc=a,bank=np.arctan2(lr,lu),roll=roll,cl=cl,load=L/(P['mass_kg']*tr.G),
                thrust=thrust,slew=slew,eas=V*np.exp(-r[:,2]/(2*P['density_scale_m']))/tr.KT,
                gamma=np.arctan2(va[:,2],h),lu=lu)

def evaluate(q,n=161):
    s=np.linspace(0,1,n); cs=curves(q,P)
    phases=[phase(c,T,s) for c,T in zip(cs,q[:2])]
    d={k:np.concatenate([p[k] for p in phases]) for k in phases[0]}
    m={}
    for key,lo,hi in [('eas',135,175),('cl',0,2.8),('load',.5,1.4),('thrust',0,700000)]:
        m[key+'_lower']=(d[key]-lo)/(hi-lo);m[key+'_upper']=(hi-d[key])/(hi-lo)
    for key,cap in [('bank',np.deg2rad(25)),('roll',np.deg2rad(5)),('slew',100000)]:
        m[key]=1-abs(d[key])/cap
    m['descent']=1+d['gamma']/np.deg2rad(6)
    m['approach_sink']=1+phases[0]['vel'][:,2]/8
    m['corridor']=1-EV.reference_tree.query(d['pos'])[0]/400
    stop=q[2]+2*q[3]+q[3]**2/(2*P['brake_deceleration_mps2'])
    m['touchdown_x_lower']=np.array([(q[2]-200)/500])
    m['touchdown_x_upper']=np.array([(700-q[2])/500])
    m['touchdown_sink_lower']=np.array([.7/1.5])
    m['touchdown_sink_upper']=np.array([.8/1.5])
    for key in ['touchdown_lateral','touchdown_track','touchdown_bank']:m[key]=np.array([1.])
    m['stop']=np.array([(2636-stop)/2636])
    m.update(tr.obstacle_margins(d['pos'],q[2],stop,CFG.get('obstacles',[]),400))
    # Touchdown height is identically zero by construction, not a numerical
    # inequality to differentiate through cancellation residuals.
    h=np.r_[d['pos'][:-1,2]/100,d['vel'][:,0]/100,d['lu']/(P['mass_kg']*tr.G)]
    effort=sum(np.trapezoid((p['bank']/np.deg2rad(25))**2+(p['roll']/np.deg2rad(5))**2+(p['slew']/100000)**2,s*T) for p,T in zip(phases,q[:2]))
    return m,h,effort

def solve(q,n=161,secondary=False,eta_floor=0,maxiter=600):
    cache={}
    def get(x):
        key=x[:-1].tobytes()
        if key not in cache:
            cache.clear();cache[key]=evaluate(x[:-1]*SCALE,n)
        return cache[key]
    def con(x):
        m,h,_=get(x)
        return np.r_[np.concatenate(list(m.values()))-x[-1],h]
    m,_,_=evaluate(q,n)
    x0=np.r_[q/SCALE,min(map(np.min,m.values()))-1e-6]
    b=[(a/s,b/s) for (a,b),s in zip(tr.BOUNDS,SCALE)]+[(eta_floor if secondary else -2,.49)]
    result=minimize((lambda x:get(x)[2]/50) if secondary else (lambda x:-x[-1]),x0,
        method='SLSQP',bounds=b,constraints=[{'type':'ineq','fun':con}],
        options={'maxiter':maxiter,'ftol':1e-10,'eps':1e-6})
    q=result.x[:-1]*SCALE
    m,h,eff=evaluate(q,2001)
    return dict(success=bool(result.success),message=str(result.message),iterations=int(result.nit),q=q.tolist(),
        eta_variable=float(result.x[-1]),sampled_exact_eta=float(min(map(np.min,m.values()))),
        minima={k:float(np.min(v)) for k,v in m.items()},hard_min=float(min(h)),effort=float(eff),n=n,
        interpretation='local search and sampled exact derivatives, not continuous or global proof')

def main():
    saved=json.loads((ROOT/'outputs/scenario/optimization_replay.json').read_text())
    q=np.array(saved['optimization']['secondary']['decisions'])
    out=Path(__file__).with_name('candidate_search.json')
    results=[]
    for n in [121,301]:
        r=solve(q,n);results.append(r);q=np.array(r['q'])
        out.write_text(json.dumps({'runs':results},indent=2)+'\n')
        print(json.dumps(r),flush=True)
    r=solve(q,301,True,results[-1]['sampled_exact_eta']-5e-5);results.append(r)
    out.write_text(json.dumps({'runs':results},indent=2)+'\n');print(json.dumps(r),flush=True)

if __name__=='__main__':main()
