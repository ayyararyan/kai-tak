"""Local lexicographic search; run with python -m model.solve from project root."""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys
from datetime import datetime, timezone
import numpy as np
import scipy
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .trajectory import (BASE_Q, BOUNDS, Evaluator, HistoricalUnavailable, load_config,
                         replay, summary, validate_config)

SCALE=np.array([40,7,500,77,100,100,100,100,20,20,20,5],float)


def margins(e,eta):
    _,m,h,_,_=e
    return np.concatenate([*(v-eta for v in m.values()),*h.values()])


def optimize(cfg,n=121,maxiter=600):
    if not isinstance(n, int) or n < 5 or not isinstance(maxiter, int) or maxiter < 1:
        raise ValueError('samples must be an integer >=5 and maxiter an integer >=1')
    ev=Evaluator(cfg)
    cache={}
    def get(x):
        key=np.asarray(x[:-1]).tobytes()
        if key not in cache:
            cache.clear()
            cache[key]=ev.evaluate(x[:-1]*SCALE,n)
        return cache[key]
    bounds=[(a/s,b/s) for (a,b),s in zip(BOUNDS,SCALE)]+[(-10,.49)]
    x0=np.r_[BASE_Q/SCALE,min(summary(ev.evaluate(BASE_Q,n))['eta']-.01,0)]
    primary=minimize(lambda x:-x[-1],x0,method='SLSQP',bounds=bounds,
        constraints=[{'type':'ineq','fun':lambda x:margins(get(x),x[-1])}],
        options={'maxiter':maxiter,'ftol':1e-9})
    eta=float(primary.x[-1])
    secondary=minimize(lambda x:get(x)[-1]/50,primary.x,method='SLSQP',bounds=bounds,
        constraints=[{'type':'ineq','fun':lambda x:margins(get(x),x[-1])},
                     {'type':'ineq','fun':lambda x:x[-1]-(eta-5e-5)}],
        options={'maxiter':maxiter,'ftol':1e-9})
    selected=secondary if primary.success and secondary.success and secondary.x[-1] >= eta-1e-4-1e-9 and np.min(margins(get(secondary.x),secondary.x[-1]))>=-1e-6 else primary
    def record(r):
        return dict(success=bool(r.success),status=int(r.status),message=str(r.message),
                    iterations=int(r.nit),eta_variable=float(r.x[-1]),decisions=(r.x[:-1]*SCALE).tolist(),
                    min_solver_constraint=float(np.min(margins(get(r.x),r.x[-1]))))
    return selected.x[:-1]*SCALE,dict(primary=record(primary),secondary=record(secondary),
        selected='secondary' if selected is secondary else 'primary',collocation_per_phase=n,
        interpretation='local optimization within declared polynomial family; no global optimum or infeasibility proof',
        eta_retention_tolerance=1e-4,solver_retention_budget=5e-5)


def save_csv(path,e):
    d,_,_,ro,_=e
    names=['time_s','phase','x_m','y_m','z_m','vx_mps','vy_mps','vz_mps','tas_mps','eas_kt','air_heading_rad','track_rad','gamma_rad','bank_rad','roll_rad_s','cl','load_g','thrust_n','thrust_slew_n_s']
    with path.open('w',newline='') as f:
        wr=csv.writer(f);wr.writerow(names)
        for i,t in enumerate(d['time_s']):
            wr.writerow([t,'approach' if d['phase'][i]==0 else 'flare',*d['pos'][i],*d['vel'][i],
                *(d[k][i] for k in names[8:])])
        # Ground state does not have an aerodynamic flight control interpretation.
        for i,t in enumerate(ro['time_s'][1:],1):
            wr.writerow([t,'rollout',ro['x_m'][i],0,0,ro['speed_mps'][i],0,0]+['']*(len(names)-8))


def plot(path,base,cand,cfg):
    fig,axs=plt.subplots(2,2,figsize=(12,8))
    for e,label,col in ((base,'Unoptimized synthetic reference','#8a7660'),(cand,'Local candidate','#48665b')):
        d=e[0]; ro=e[3]
        axs[0,0].plot(d['pos'][:,0],d['pos'][:,1],color=col,label=label)
        axs[0,1].plot(d['pos'][:,0],d['pos'][:,2],color=col)
        axs[1,0].plot(d['time_s'],np.rad2deg(d['bank_rad']),color=col)
        axs[1,1].plot(d['time_s'],d['eas_kt'],color=col)
        axs[0,0].plot(ro['x_m'],np.zeros_like(ro['x_m']),color=col,alpha=.4)
        axs[0,0].scatter(ro['stop_x_m'],0,color=col,marker='x')
    p=validate_config(cfg)
    axs[0,0].plot([0,p['lda_m']],[0,0],color='black',lw=5,alpha=.2)
    axs[0,0].axvline(p['lda_m']-p['reserve_m'],color='gray',ls=':')
    axs[0,0].set(xlabel='x from displaced threshold (m)',ylabel='y right of runway (m)',title='Ground track and stop (×)')
    axs[0,0].axis('equal');axs[0,0].legend(fontsize=8)
    axs[0,1].set(xlabel='x from threshold (m)',ylabel='Height above runway (m)',title='Continuous approach and flare')
    axs[1,0].axhline(p['bank_limit_deg'],ls=':',color='gray');axs[1,0].axhline(-p['bank_limit_deg'],ls=':',color='gray')
    axs[1,0].set(xlabel='Flight time (s)',ylabel='Bank, positive right (deg)')
    axs[1,1].axhline(p['eas_min_kt'],ls=':',color='gray');axs[1,1].axhline(p['eas_max_kt'],ls=':',color='gray')
    axs[1,1].set(xlabel='Flight time (s)',ylabel='Equivalent airspeed (kt)')
    fig.suptitle('Runway 13 — uncalibrated scenario, not historical paths or flight guidance')
    for ax in axs.flat:ax.grid(alpha=.15)
    fig.tight_layout();fig.savefig(path,dpi=180);plt.close(fig)


def validation_samples(n):
    if not isinstance(n, int) or n < 5:
        raise ValueError('samples must be an integer >=5')
    return max(1201, 10*(n-1)+1)


def sensitivity_cases(p):
    wind=np.asarray(p['wind_mps'], dtype=float)
    return [('steady_crosswind_plus5','wind_mps',(wind+[0,5,0]).tolist()),
            ('steady_crosswind_minus5','wind_mps',(wind-[0,5,0]).tolist()),
            ('mass_plus5percent','mass_kg',p['mass_kg']*1.05),
            ('braking_minus10percent','brake_deceleration_mps2',p['brake_deceleration_mps2']*.9)]


def run(cfg,out,n=121,maxiter=600):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    q,opt=optimize(cfg,n,maxiter)
    ev=Evaluator(cfg)
    dense_n=validation_samples(n)
    base=ev.evaluate(BASE_Q,dense_n);cand=ev.evaluate(q,dense_n)
    bs,cs=summary(base),summary(cand)
    br,cr=replay(base,cfg,reference_tree=ev.reference_tree),replay(cand,cfg,reference_tree=ev.reference_tree)
    selected_success=opt[opt['selected']]['success']
    primary_dense=summary(ev.evaluate(np.asarray(opt['primary']['decisions']),dense_n))
    dense_retained=cs['eta'] >= primary_dense['eta']-1e-4-1e-8
    optimization_complete=bool(opt['primary']['success'] and opt['secondary']['success'] and opt['selected']=='secondary' and dense_retained)
    status='sampled_scenario_feasible' if selected_success and cs['sampled_feasible'] and cr['passed'] and cr['terminal_constraints_passed'] and cr['stop_constraint_passed'] and cr['path_constraints_passed'] else 'unresolved'
    sensitivity=[]
    for label,field,val in sensitivity_cases(ev.p):
        modified=copy.deepcopy(cfg);modified['parameters'][field].update(value=val,category='scenario-based',source=f'Sensitivity {label}: perturbation of executed nominal {field}; not an observed or unit-converted historical value')
        se=Evaluator(modified)
        # Freeze the same nominal spatial corridor even when wind changes endpoint air/ground mapping.
        se.reference_tree=ev.reference_tree
        fixed=tuple(cand[0][k] for k in ('time_s','pos','vel','acc','phase'))
        result=se.evaluate(q,dense_n,kinematics_override=fixed)
        sensitivity.append(dict(case=label,parameter=field,value=val,summary=summary(result),replay=replay(result,modified,reference_tree=ev.reference_tree),provenance=modified['parameters'][field],
            interpretation='exact nominal ground path and timing, inverse controls conditioned on wind; airspeed/air-gamma endpoint equalities may change; not common-policy robustness' if field=='wind_mps' else 'fixed trajectory decisions; conditional inverse-force diagnostic'))
    source_root=Path(__file__).parent
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source_root.glob('*.py'))}
    report=dict(source_sha256=source_hashes,schema_version=1,utc=datetime.now(timezone.utc).isoformat(),status=status,
        category='scenario-based',aircraft_calibration='unavailable',historical_comparison='not performed',
        optimization=opt,optimization_complete=optimization_complete,baseline=bs,candidate=cs,baseline_replay=br,candidate_replay=cr,
        dense_grid_per_phase=dense_n,mesh_check={'optimization_grid_eta':summary(ev.evaluate(q,n))['eta'],
            'primary_dense_eta':primary_dense['eta'],'secondary_retains_primary_dense_eta':dense_retained,
            'dense_grid_eta':cs['eta'],'difference':cs['eta']-summary(ev.evaluate(q,n))['eta']},
        sensitivity=sensitivity,nominal_objective_delta=cs['eta']-bs['eta'],
        improvement_interpretation='Difference from an infeasible unoptimized synthetic seed, not an admissible historical comparator; no historical or globally optimal claim' if not bs['sampled_feasible'] else 'Difference from unoptimized synthetic reference only; no historical or globally optimal claim',
        constraints='Sampled and replay-checked; finite grids are not continuous-time proof',
        runtime={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()})
    (out/'optimization_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'parameter_provenance.json').write_text(json.dumps(cfg,indent=2)+'\n')
    save_csv(out/'baseline.csv',base);save_csv(out/'candidate.csv',cand)
    plot(out/'trajectory.png',base,cand,cfg)
    manifest={f.name:{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}
              for f in sorted(out.iterdir()) if f.is_file() and f.name!='manifest.json'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config',type=Path,default=Path(__file__).with_name('config.json'))
    ap.add_argument('--out',type=Path,default=Path('outputs/scenario'))
    ap.add_argument('--mode',choices=['scenario','historical'],default='scenario')
    ap.add_argument('--samples',type=int,default=121)
    ap.add_argument('--maxiter',type=int,default=600)
    args=ap.parse_args()
    cfg=load_config(args.config)
    try:validate_config(cfg,args.mode)
    except HistoricalUnavailable as exc:
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/'historical_blocked.json').write_text(json.dumps({'status':'blocked','reason':str(exc)},indent=2)+'\n')
        print(str(exc));return 2
    report=run(cfg,args.out,args.samples,args.maxiter)
    print(json.dumps({k:report[k] for k in ('status','candidate','candidate_replay','mesh_check')},indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
