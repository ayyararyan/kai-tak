"""Coupled continuous-model candidate search. Finite search is NOT a proof.

Preserves v1 parameter family and all margins; uses analytic rates, both joins.
Does not modify or supersede the sampled v1 executable.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import json
import numpy as np
from scipy.optimize import minimize
from model import trajectory as tr
from model.solve import SCALE
from analytical.verify_full_landing_analysis import curves

import copy, hashlib, csv, argparse, uuid, shutil, os
OUT=Path(__file__).resolve().parent

def wind_vector(speed_kt, from_true_deg, runway_true_deg):
    vals=np.array([speed_kt,from_true_deg,runway_true_deg],float)
    if not np.all(np.isfinite(vals)) or speed_kt<0: raise ValueError('invalid wind')
    delta=np.deg2rad(from_true_deg-runway_true_deg)
    return np.array([-speed_kt*tr.KT*np.cos(delta),-speed_kt*tr.KT*np.sin(delta),0.])

BASE_CFG=tr.load_config()
EV=tr.Evaluator(BASE_CFG)  # frozen original zero-wind corridor
CFG=copy.deepcopy(BASE_CFG)
CFG['parameters']['wind_mps'].update(value=wind_vector(21,70,133+1/6).tolist(),category='scenario-based',source='CAD report surface mean 070 true / 21 kt held spatially and temporally constant; runway true =135 magnetic -1deg50min west (1990 chart)')
P=tr.values(CFG)

def validate_q(q):
    q=np.asarray(q,float)
    if q.shape!=(12,) or not np.all(np.isfinite(q)): raise ValueError('invalid decisions')
    if any(not lo<=x<=hi for x,(lo,hi) in zip(q,tr.BOUNDS)): raise ValueError('decisions outside frozen box')
    return q


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
    q=validate_q(q)
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

def solve(q,n=161,secondary=False,eta_floor=0,maxiter=500):
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
    return dict(success=bool(result.success),message=str(result.message),iterations=int(result.nit),status=int(result.status),q=q.tolist(),
        eta_variable=float(result.x[-1]),sampled_exact_eta=float(min(map(np.min,m.values()))),
        minima={k:float(np.min(v)) for k,v in m.items()},hard_min=float(min(h)),effort=float(eff),n=n,
        interpretation='local search and sampled exact derivatives, not continuous or global proof')


def write(name,data):
    temporary=OUT/(name+'.tmp-'+uuid.uuid4().hex)
    temporary.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    os.replace(temporary,OUT/name)

def inputs():
    paths=['model/config.json','model/trajectory.py','model/solve.py','analytical/verify_full_landing_analysis.py','analytical/coupled/solve_coupled.py','analytical/coupled/certify_candidate.py','evidence/EVIDENCE_REPORT.md','outputs/scenario/optimization_replay.json']
    paths += ['evidence/cal605_reconstruction/noaa/README.md']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    return dict(source_sha256=hashes,scenario_configuration=CFG,wind_from_true_deg=70,wind_speed_kt=21,
        runway_magnetic_deg=135,variation_east_positive_deg=-(1+50/60),runway_true_deg=133+1/6,
        wind_runway_mps=P['wind_mps'],reference_cloud_sha256=hashlib.sha256(EV.reference_tree.data.tobytes()).hexdigest(),
        observed_mean='Report rounded 21 kt; NOAA 10.8 m/s is about 20.994 kt, corroborating but not numerically substituted.',
        assumptions=['uniform steady surface mean used throughout airborne path','chart 1990 variation used as scenario bearing, not surveyed 1993 true axis','synthetic entry/corridor and uncalibrated point-mass envelope retained','ground brake law unchanged'],
        historical_feasibility=None,physical_prediction_intervals=None,global_optimality_gap=None)

def check_sources():
    record=json.loads((OUT/'inputs.json').read_text())
    for path,want in record['source_sha256'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=want: raise ValueError('source changed: '+path)
    if inputs()!=record: raise ValueError('input scenario changed')

def current_selection():
    state=json.loads((OUT/'search_state.json').read_text())
    if state.get('status')!='completed':raise ValueError('search not completed: '+state.get('status','missing'))
    selected=json.loads((OUT/'selected.json').read_text())
    if selected.get('run_id')!=state.get('run_id') or hashlib.sha256((OUT/'selected.json').read_bytes()).hexdigest()!=state.get('selected_sha256'):
        raise ValueError('stale selection from another search')
    return selected

def eligible_record(r):
    return bool(r['success'] and np.isfinite(r['sampled_exact_eta']) and r['sampled_exact_eta']>0 and np.isfinite(r['hard_min']) and r['hard_min']>=0)

def search():
    run_id=uuid.uuid4().hex
    archive=OUT/'archive'/run_id
    archive.mkdir(parents=True)
    for name in ['search_state.json','selected.json','search_checkpoint.json','continuous_check.json','result.json','formula.json','path_controls.csv','landing.png','landing.pdf','verification.json','delivery_manifest.json']:
        if (OUT/name).is_file():shutil.copy2(OUT/name,archive/name)
    write('search_state.json',dict(run_id=run_id,status='running',prior_artifacts_archive=str(archive.relative_to(OUT))))
    try:
        return _search(run_id)
    except BaseException as exc:
        write('search_state.json',dict(run_id=run_id,status='failed_or_interrupted',reason=type(exc).__name__+': '+str(exc)))
        raise

def _search(run_id):
    if (OUT/'inputs.json').exists(): check_sources()
    else: write('inputs.json',inputs())
    prior=json.loads((ROOT/'outputs/scenario/optimization_replay.json').read_text())
    seed=np.array(prior['optimization']['secondary']['decisions'])
    starts=[seed, tr.BASE_Q.copy(),seed+np.array([3,1,20,-3,10,-10,15,-15,2,-2,0,0]),seed+np.array([-2,2,40,-2,-15,15,-10,10,-1,1,0,0])]
    runs=[]
    for i,q in enumerate(starts):
        q=np.clip(q,np.array(tr.BOUNDS)[:,0],np.array(tr.BOUNDS)[:,1])
        r=solve(q,161);r.update(stage='primary_multistart',start=i);runs.append(r)
        write('search_checkpoint.json',dict(runs=runs));print(json.dumps(r),flush=True)
    eligible=[r for r in runs if eligible_record(r)]
    if not eligible:
        write('search_state.json',dict(run_id=run_id,status='unresolved',reason='No numerically successful feasible start'));return
    best=max(eligible,key=lambda r:r['sampled_exact_eta'])
    r=solve(np.array(best['q']),601);r.update(stage='primary_refinement');runs.append(r)
    write('search_checkpoint.json',dict(runs=runs));print(json.dumps(r),flush=True)
    if eligible_record(r) and r['sampled_exact_eta']>=best['sampled_exact_eta']:best=r
    secondary=solve(np.array(best['q']),601,True,best['sampled_exact_eta']-5e-5)
    secondary.update(stage='secondary');runs.append(secondary)
    write('search_checkpoint.json',dict(runs=runs));print(json.dumps(secondary),flush=True)
    selected=secondary if eligible_record(secondary) and secondary['sampled_exact_eta']>=best['sampled_exact_eta']-1e-4 else best
    write('selected.json',dict(run_id=run_id,primary=best,secondary=secondary,selected=selected,secondary_complete=selected is secondary,runs=len(runs)))
    write('search_state.json',dict(run_id=run_id,status='completed',selected_sha256=hashlib.sha256((OUT/'selected.json').read_bytes()).hexdigest()))

if __name__=='__main__':
    search()
