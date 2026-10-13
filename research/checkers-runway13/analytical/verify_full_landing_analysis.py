#!/usr/bin/env python3
"""Analytic identities and exact rational bound. Never calls an optimizer."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from numpy.polynomial import Polynomial as P

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model import trajectory as impl


def explicit(p0,p1,v0,v1,a0,a1,T):
    c0=np.asarray(p0); c1=T*np.asarray(v0); c2=T*T*np.asarray(a0)/2
    A=np.asarray(p1)-c0-c1-c2
    B=T*np.asarray(v1)-c1-2*c2
    C=T*T*np.asarray(a1)-2*c2
    c=np.array([c0,c1,c2,10*A-4*B+C/2,-15*A+7*B-C,6*A-3*B+C/2])
    return [P(c[:,i]) for i in range(3)]


def curves(q,p):
    start=np.array(p['start_xyz_m']); gate=np.array([0,0,p['threshold_height_m']])
    v0=impl.endpoint_velocity(p['initial_eas_kt'],start[2],p['initial_track_deg'],p['threshold_gamma_deg'],p)
    vg=impl.endpoint_velocity(p['initial_eas_kt'],gate[2],0,p['threshold_gamma_deg'],p)
    z=np.zeros(3)
    a=explicit(start,gate,v0,vg,z,z,q[0])
    f=explicit(gate,[q[2],0,0],vg,[q[3],0,-p['touchdown_sink_mps']],z,z,q[1])
    bump=64*P([0,0,0,1,-3,3,-1]); odd=bump*P([-1,2])
    for j in range(3):
        a[j]+=q[4+2*j]*bump+q[5+2*j]*odd
    f[0]+=q[10]*bump; f[2]+=q[11]*bump
    return a,f


def analytic(polys,T,s,p):
    r=np.array([v(s) for v in polys]); v=np.array([v.deriv()(s)/T for v in polys])
    acc=np.array([v.deriv(2)(s)/T**2 for v in polys])
    jerk=np.array([v.deriv(3)(s)/T**3 for v in polys])
    va=v-np.asarray(p['wind_mps']); V=np.linalg.norm(va); et=va/V
    psi=np.arctan2(va[1],va[0]); er=np.array([-np.sin(psi),np.cos(psi),0.])
    eu=np.cross(et,er); force=p['mass_kg']*(acc+[0,0,impl.G])
    lu,lr=force@eu,force@er; L=np.hypot(lu,lr)
    Q=.5*p['rho0_kg_m3']*np.exp(-r[2]/p['density_scale_m'])*V**2*p['wing_area_m2']
    cl=L/Q; drag=Q*(p['cd0']+p['induced_factor']*cl*cl)
    phi=np.arctan2(lr,lu); thrust=drag+force@et
    Vdot=et@acc; etd=(acc-et*Vdot)/V
    psid=(va[0]*acc[1]-va[1]*acc[0])/(va[0]**2+va[1]**2)
    erd=-psid*np.array([np.cos(psi),np.sin(psi),0.])
    eud=np.cross(etd,er)+np.cross(et,erd); fd=p['mass_kg']*jerk
    lud,lrd=fd@eu+force@eud,fd@er+force@erd
    phid=(lu*lrd-lr*lud)/L**2; ld=(lu*lud+lr*lrd)/L
    qd=Q*(-v[2]/p['density_scale_m']+2*Vdot/V)
    cld=ld/Q-cl*qd/Q
    dd=qd*(p['cd0']+p['induced_factor']*cl*cl)+2*Q*p['induced_factor']*cl*cld
    td=dd+fd@et+force@etd
    replay=((thrust-drag)*et+L*(np.cos(phi)*eu+np.sin(phi)*er))/p['mass_kg']-[0,0,impl.G]
    return dict(pos=r,vel=v,acc=acc,bank=phi,thrust=thrust,roll=phid,slew=td,
                acceleration_residual=float(np.linalg.norm(replay-acc)),
                eas=V*np.exp(-r[2]/(2*p['density_scale_m']))/impl.KT,
                gamma=np.arctan2(va[2],np.linalg.norm(va[:2])))


def sqrt_enclosure(x,digits=40):
    scale=10**digits
    n=math.isqrt((x.numerator*scale*scale)//x.denominator)
    lo,hi=F(n,scale),F(n+1,scale)
    assert lo*lo<=x<=hi*hi
    return lo,hi


def bound_certificate():
    # Rational values are exact nominal printed constants, not binary floats.
    k=F(1852,3600); sig=F(7,10); dec=F(15,100)*F(980665,100000)
    def interval(eta):
        v2=(k*(135+40*eta))**2-sig**2
        vl,vh=sqrt_enclosure(v2)
        other=200+500*eta+v2/(2*dec)-2636*(1-eta)
        return other+2*vl,other+2*vh
    lo,hi=F(0),F(45,100)
    assert interval(lo)[1]<0 and interval(hi)[0]>0
    for _ in range(60):
        mid=(lo+hi)/2; fl,fh=interval(mid)
        if fh<0:lo=mid
        elif fl>0:hi=mid
        else:break
    assert interval(lo)[1]<0 and interval(hi)[0]>0
    # Conservative quadratic from v>=k(135+40eta)-sigma.
    aa=40*k; bb=135*k-sig
    qa=aa*aa/(2*dec)
    qb=500+2*aa+aa*bb/dec+2636
    qc=200+2*bb+bb*bb/(2*dec)-2636
    conservative=(-float(qb)+math.sqrt(float(qb*qb-4*qa*qc)))/(2*float(qa))
    return {'lower_rational':str(lo),'upper_rational':str(hi),
            'lower_decimal_approx':float(lo),'upper_decimal_approx':float(hi),
            'width_rational':str(hi-lo),'lower_F_upper_enclosure':str(interval(lo)[1]),
            'upper_F_lower_enclosure':str(interval(hi)[0]),
            'method':'exact Fraction arithmetic; isqrt rational sqrt enclosures',
            'conservative_explicit_quadratic_upper_approx':conservative}


def check_bound_domain(p):
    expected = {'touchdown_sink_mps': .7, 'touchdown_x_min_m': 200,
                'touchdown_x_max_m': 700, 'eas_min_kt': 135, 'eas_max_kt': 175,
                'brake_delay_s': 2, 'brake_deceleration_mps2': .15*9.80665,
                'lda_m': 2786, 'reserve_m': 150}
    for key, value in expected.items():
        if p[key] != value:
            raise ValueError(f'Nominal bound does not apply: {key}')
    if list(p['wind_mps']) != [0, 0, 0] or impl.G != 9.80665 or impl.KT != 1852/3600:
        raise ValueError('Nominal bound requires zero wind and unchanged unit constants')


def run():
    source=ROOT/'model/trajectory.py'; initial_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    cfg=impl.load_config(); p=impl.values(cfg)
    check_bound_domain(p)
    # Changed assumptions must not inherit the nominal certificate.
    for key, value in [('wind_mps', [1,0,0]), ('brake_delay_s', 3),
                       ('touchdown_sink_mps', .8), ('eas_min_kt', 134)]:
        try:
            check_bound_domain({**p, key: value})
        except ValueError:
            pass
        else:
            raise AssertionError('Changed bound assumptions accepted')
    saved=json.loads((ROOT/'outputs/scenario/optimization_replay.json').read_text())
    assert initial_hash==saved['source_sha256']['trajectory.py']
    q=np.array(saved['optimization'][saved['optimization']['selected']]['decisions'])
    # Exact proof of coefficient map: endpoint residual matrix times formula inverse.
    mat=[[F(1),F(1),F(1)],[F(3),F(4),F(5)],[F(6),F(12),F(20)]]
    inv=[[F(10),F(-4),F(1,2)],[F(-15),F(7),F(-1)],[F(6),F(-3),F(1,2)]]
    for i in range(3):
        for j in range(3):
            assert sum(mat[i][k]*inv[k][j] for k in range(3))==int(i==j)
    rng=np.random.default_rng(20261013)
    worst_coeff=0.
    for case in range(41):
        z=q if case==0 else np.array([rng.uniform(lo,hi) for lo,hi in impl.BOUNDS])
        ac=curves(z,p); bc=impl.curves(z,cfg)
        for ap,bp in zip(ac,bc):
            for av,bv in zip(ap,bp):
                n=max(len(av.coef),len(bv.coef))
                err=np.max(np.abs(np.pad(av.coef,(0,n-len(av.coef)))-np.pad(bv.coef,(0,n-len(bv.coef)))))
                worst_coeff=max(worst_coeff,float(err)); assert err<1e-8
    cs=curves(q,p)
    worst={'roll_fd_rad_s':0.,'slew_fd_n_s':0.,'newton_m_s2':0.}
    exact_rate_min={'roll_rate':1.,'thrust_slew':1.}
    for polys,T in zip(cs,q[:2]):
        for s in np.linspace(.03,.97,25):
            a=analytic(polys,T,s,p); dt=1e-4
            l=analytic(polys,T,s-dt/T,p); r=analytic(polys,T,s+dt/T,p)
            pe=abs(a['roll']-(r['bank']-l['bank'])/(2*dt))
            te=abs(a['slew']-(r['thrust']-l['thrust'])/(2*dt))
            worst['roll_fd_rad_s']=max(worst['roll_fd_rad_s'],pe)
            worst['slew_fd_n_s']=max(worst['slew_fd_n_s'],te)
            worst['newton_m_s2']=max(worst['newton_m_s2'],a['acceleration_residual'])
            assert pe<1e-6 and te<.2 and a['acceleration_residual']<1e-10
        for s in np.linspace(0,1,1201):
            a=analytic(polys,T,s,p)
            exact_rate_min['roll_rate']=min(exact_rate_min['roll_rate'],1-abs(a['roll'])/math.radians(p['roll_limit_deg_s']))
            exact_rate_min['thrust_slew']=min(exact_rate_min['thrust_slew'],1-abs(a['slew'])/p['thrust_slew_n_s'])
    endpoints=[]
    for name,polys,T,s in [('start',cs[0],q[0],0),('gate_left',cs[0],q[0],1),('gate_right',cs[1],q[1],0)]:
        a=analytic(polys,T,s,p)
        assert abs(a['eas']-153)<1e-8
        assert abs(math.degrees(a['gamma'])+3.1)<1e-8
        assert abs(a['bank'])<1e-9
        d=impl.inverse(a['pos'][None,:],a['vel'][None,:],a['acc'][None,:],p)
        endpoint_limits={'eas':.45,'descent':1-3.1/6,
                         'load_lower':float((d['load_g'][0]-.5)/.9),
                         'load_upper':float((1.4-d['load_g'][0])/.9),
                         'cl_lower':float(d['cl'][0]/2.8),'cl_upper':float(1-d['cl'][0]/2.8),
                         'thrust_lower':float(d['thrust_n'][0]/700000),
                         'thrust_upper':float(1-d['thrust_n'][0]/700000)}
        endpoints.append({'name':name,'eas_kt':a['eas'],'gamma_deg':math.degrees(a['gamma']),
                          'fixed_margin_upper_bounds':endpoint_limits})
    stop=q[2]+q[3]*p['brake_delay_s']+q[3]**2/(2*p['brake_deceleration_mps2'])
    assert abs(stop-saved['candidate']['stop_x_m'])<1e-9
    ev=impl.Evaluator(cfg).evaluate(q,1201); sm=impl.summary(ev)
    assert abs(sm['eta']-saved['candidate']['eta'])<1e-9
    # This minimum still samples all remaining quantities; NOT all-time feasibility.
    mins=dict(sm['margin_minima']); mins.update(exact_rate_min)
    bound=bound_certificate()
    assert bound['upper_decimal_approx']<.158
    assert initial_hash==hashlib.sha256(source.read_bytes()).hexdigest()
    return {'utc':datetime.now(timezone.utc).isoformat(),'status':'passed',
            'source_sha256':initial_hash,'authoritative_artifact_utc':saved['utc'],
            'exact_rational_hermite_identity':True,'curve_comparison_cases':41,
            'nominal_bound_domain_checked':True,'changed_bound_domains_rejected':4,
            'max_coefficient_error':worst_coeff,'derivative_check_points':50,
            'derivative_residuals':worst,'fixed_endpoints':endpoints,
            'upper_bound_certificate':bound,'candidate_stop_m':float(stop),
            'candidate_saved_sampled_eta':saved['candidate']['eta'],
            'candidate_sampled_exact_rate_minima':exact_rate_min,
            'candidate_sampled_exact_rate_eta':min(mins.values()),
            'upper_to_saved_sampled_difference':bound['upper_decimal_approx']-saved['candidate']['eta'],
            'certified_continuous_optimality_gap':None,'new_optimizer_run':False,
            'full_landing_global_optimum_found':False,
            'interpretation':'global necessary upper bound plus identity checks; no continuous candidate lower certificate'}


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('full_landing_analysis_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
