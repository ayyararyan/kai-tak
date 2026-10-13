"""Analytic-rate force evaluator adapted from frozen counterfactual/calculate.py; parameterized explicitly."""
import numpy as np
from model import trajectory as tr
def phase(polys,T,s,p):
    r,v,a,j=[np.column_stack([z.deriv(k)(s)/T**k for z in polys]) for k in range(4)]
    va=v-np.array(p['wind_mps']); V=np.linalg.norm(va,axis=1); et=va/V[:,None]
    h=np.linalg.norm(va[:,:2],axis=1)
    er=np.column_stack([-va[:,1]/h,va[:,0]/h,np.zeros(len(s))]); eu=np.cross(et,er)
    F=p['mass_kg']*(a+[0,0,tr.G]); Fd=p['mass_kg']*j
    dot=lambda x,y:np.sum(x*y,axis=1)
    lu,lr=dot(F,eu),dot(F,er); L=np.hypot(lu,lr)
    vd=dot(et,a); etd=(a-et*vd[:,None])/V[:,None]
    psid=(va[:,0]*a[:,1]-va[:,1]*a[:,0])/h**2
    erd=-psid[:,None]*np.column_stack([va[:,0]/h,va[:,1]/h,np.zeros(len(s))])
    eud=np.cross(etd,er)+np.cross(et,erd)
    lud,lrd=dot(Fd,eu)+dot(F,eud),dot(Fd,er)+dot(F,erd)
    roll=(lu*lrd-lr*lud)/L**2
    ld=(lu*lud+lr*lrd)/L
    Q=.5*p['rho0_kg_m3']*np.exp(-r[:,2]/p['density_scale_m'])*V**2*p['wing_area_m2']
    cl=L/Q; qd=Q*(-v[:,2]/p['density_scale_m']+2*vd/V); cld=ld/Q-cl*qd/Q
    drag=Q*(p['cd0']+p['induced_factor']*cl**2)
    dd=qd*(p['cd0']+p['induced_factor']*cl**2)+2*Q*p['induced_factor']*cl*cld
    thrust=drag+dot(F,et); slew=dd+dot(Fd,et)+dot(F,etd)
    return dict(pos=r,vel=v,acc=a,bank=np.arctan2(lr,lu),roll=roll,cl=cl,load=L/(p['mass_kg']*tr.G),
                thrust=thrust,slew=slew,eas=V*np.exp(-r[:,2]/(2*p['density_scale_m']))/tr.KT,
                gamma=np.arctan2(va[:,2],h),lu=lu)
