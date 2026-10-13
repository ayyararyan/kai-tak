"""Reconstruct, replay and export the selected wind-conditioned candidate."""
import json,csv,hashlib,sys,tempfile,os,shutil,uuid
from fractions import Fraction as F
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import *
from analytical.verify_full_landing_analysis import analytic


def upper_bound():
    dec=F(15,100)*F(980665,100000)
    bound=(2636-200-2*69-F(69**2)/(2*dec))/3136
    return dict(upper_exact=str(bound),upper_display=float(bound),proof='xTD>=200+500eta, ground speed u>=69; monotone stop xTD+2u+u^2/(2a)<=2636(1-eta); hence3136eta<=2636-200-138-4761/(2a)',scope='fixed decision family terminal relaxation; valid for declared wind; not a global optimum or near-optimality proof')


def validate_certificate(cert,q):
    if not cert.get('certified'):return
    expected=dict(run_id=current_selection()['run_id'],q_real_decimal=[repr(float(x)) for x in q],wind_speed_kt=21,wind_from_true_deg=70,runway_true_deg_exact='799/6',
        checker_source_sha256=hashlib.sha256((OUT/'continuous.py').read_bytes()).hexdigest(),
        calculator_source_sha256=hashlib.sha256((OUT/'calculate.py').read_bytes()).hexdigest(),
        inputs_sha256=hashlib.sha256((OUT/'inputs.json').read_bytes()).hexdigest(),
        reference_point_cloud_sha256=inputs()['reference_cloud_sha256'],
        config_sha256=inputs()['source_sha256']['model/config.json'],trajectory_source_sha256=inputs()['source_sha256']['model/trajectory.py'])
    for key,value in expected.items():
        if cert.get(key)!=value:raise ValueError('stale or substituted certificate: '+key)


def _produce(stage):
    check_sources()
    selected=current_selection();q=np.array(selected['selected']['q']);validate_q(q)
    certpath=OUT/'continuous_check.json'
    cert=json.loads(certpath.read_text()) if certpath.exists() else dict(certified=False,status='missing')
    validate_certificate(cert,q)
    def staged_write(name,data):
        (stage/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    cs=curves(q,P); n=10001;s=np.linspace(0,1,n)
    ds=[phase(c,T,s) for c,T in zip(cs,q[:2])]
    margins,hard,effort=evaluate(q,n)
    pmins={k:float(np.min(v)) for k,v in margins.items()}
    eta=min(pmins.values());primary_eta=min(float(np.min(v)) for v in evaluate(selected['primary']['q'],n)[0].values())
    ev=tr.Evaluator(CFG);ev.reference_tree=EV.reference_tree
    evaluated=ev.evaluate(q,3001)
    replay=tr.replay(evaluated,CFG,reference_tree=EV.reference_tree)
    accepted=selected['selected']['success'] and eta>0 and min(hard)>=0 and all(replay.get(k,False) for k in ['passed','terminal_constraints_passed','path_constraints_passed','stop_constraint_passed'])
    ro=tr.rollout(q,P,501);start_v=ds[0]['vel'][0];gate_v=ds[0]['vel'][-1]
    stats=dict(approach_s=q[0],flare_s=q[1],touchdown_time_s=q[0]+q[1],braking_start_s=q[0]+q[1]+2,
        stop_time_s=float(ro['time_s'][-1]),touchdown_x_m=q[2],touchdown_groundspeed_mps=q[3],touchdown_groundspeed_kt=q[3]/tr.KT,
        touchdown_eas_kt=float(ds[1]['eas'][-1]),touchdown_sink_mps=.7,stop_x_m=ro['stop_x_m'],runway_remaining_m=ro['reserve_remaining_m'],
        margin_beyond_required_150m_m=ro['reserve_remaining_m']-150,ground_travel_m=ro['stop_x_m']-q[2],
        threshold_groundspeed_kt=float(gate_v[0]/tr.KT),entry_horizontal_groundspeed_kt=float(np.linalg.norm(start_v[:2])/tr.KT),
        max_bank_deg=float(max(np.max(abs(d['bank'])) for d in ds)*180/np.pi),max_roll_deg_s=float(max(np.max(abs(d['roll'])) for d in ds)*180/np.pi),
        max_thrust_slew_n_s=float(max(np.max(abs(d['slew'])) for d in ds)),eas_range_kt=[float(min(d['eas'].min() for d in ds)),float(max(d['eas'].max() for d in ds))])
    formula=dict(type='piecewise polynomial time-indexed reference, not feedback control',domain='no extrapolation beyond specified phases',
        position_formula='r(t)=sum(c[k]*s^k), s=(t-t0)/T; derivative k divides by T^k',
        phases=[dict(name=name,t0_s=0 if i==0 else q[0],duration_s=q[i],coefficients_xyz_m=[p.coef.tolist() for p in cs[i]]) for i,name in enumerate(['approach','flare'])],
        ground=dict(delay_s=2,deceleration_mps2=P['brake_deceleration_mps2'],touchdown_x_m=q[2],touchdown_groundspeed_mps=q[3],
        formula='h=t-touchdown_time; for 0<=h<=2: x=xTD+u*h; for 2<=h<=2+u/a: x=xTD+2u+u*(h-2)-a*(h-2)^2/2; thereafter x=xStop, v=0'))
    staged_write('formula.json',formula)
    names=['time_s','phase','x_m','y_m','z_m','vx_mps','vy_mps','vz_mps','eas_kt','bank_deg','roll_deg_s','cl','load_g','thrust_n','thrust_slew_n_s','gamma_air_deg']
    with (stage/'path_controls.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(names)
        for i,(d,T) in enumerate(zip(ds,q[:2])):
            for k in range(0,n,10):
                w.writerow([s[k]*T+(q[0] if i else 0),'approach' if i==0 else 'flare',*d['pos'][k],*d['vel'][k],d['eas'][k],np.rad2deg(d['bank'][k]),np.rad2deg(d['roll'][k]),d['cl'][k],d['load'][k],d['thrust'][k],d['slew'][k],np.rad2deg(d['gamma'][k])])
        for t,x,v in zip(ro['time_s'][1:],ro['x_m'][1:],ro['speed_mps'][1:]):w.writerow([t,'ground',x,0,0,v,0,0]+['']*8)
    coefficient_error=0.;rate_errors=dict(roll_rad_s=0.,slew_n_s=0.,scalar_vector=0.,force_balance_mps2=0.)
    other=tr.curves(q,CFG)
    for i in range(2):
        for j in range(3):
            a,b=cs[i][j].coef,other[i][j].coef;l=max(len(a),len(b));coefficient_error=max(coefficient_error,float(np.max(abs(np.pad(a,(0,l-len(a)))-np.pad(b,(0,l-len(b)))))))
        for ss in np.linspace(.01,.99,31):
            a=analytic(cs[i],q[i],ss,P);vec=phase(cs[i],q[i],np.array([ss]));dt=1e-4
            left=analytic(cs[i],q[i],ss-dt/q[i],P);right=analytic(cs[i],q[i],ss+dt/q[i],P)
            rate_errors['roll_rad_s']=max(rate_errors['roll_rad_s'],abs(a['roll']-(right['bank']-left['bank'])/(2*dt)))
            rate_errors['slew_n_s']=max(rate_errors['slew_n_s'],abs(a['slew']-(right['thrust']-left['thrust'])/(2*dt)))
            for key in ['roll','slew','bank','thrust','eas','gamma']:
                rate_errors['scalar_vector']=max(rate_errors['scalar_vector'],abs(a[key]-vec[key][0]))
            rate_errors['force_balance_mps2']=max(rate_errors['force_balance_mps2'],a['acceleration_residual'])
    bound=upper_bound()
    gap=F(bound['upper_exact'])-F(cert['eta_lower_real_decimal']) if cert.get('certified') else None
    bound['candidate_certified_gap_upper_exact']=str(gap) if gap is not None else None
    bound['candidate_certified_gap_upper_display']=float(gap) if gap is not None else None
    result=dict(run_id=selected['run_id'],utc=datetime.now(timezone.utc).isoformat(),status='conditional_scenario_feasible' if accepted else 'unresolved',metrics=stats,q=q.tolist(),
        exact_rate_dense_grid_per_phase=n,dense_eta=eta,dense_margin_minima=pmins,hard_min_excluding_structural_contact=float(min(hard)),
        primary_dense_eta=primary_eta,secondary_primary_loss=primary_eta-eta,secondary_retention_passed=bool(primary_eta-eta<=1e-4),effort=effort,
        optimizer_runs=selected['runs'],optimization_complete=bool(selected['secondary_complete'] and primary_eta-eta<=1e-4 and accepted),secondary_complete=selected['secondary_complete'],independent_forward_replay=replay,
        verification=dict(coefficient_error=coefficient_error,rate_errors=rate_errors),continuous_check=cert.get('certified',False),global_bound=bound,
        historical_feasibility=None,physical_CI=None,physical_prediction_interval=None,robust_feedback_feasibility=None,
        scope='constructed complete landing in fixed synthetic corridor with uniform 070true/21kt wind; not historical landing, operational procedure, terrain clearance or calibrated uncertainty',
        model_sources_sha256=inputs()['source_sha256'])
    staged_write('result.json',result)
    fig,ax=plt.subplots(2,2,figsize=(12,8));color='#43665a'
    pos=np.concatenate([d['pos'] for d in ds]);tt=np.r_[s*q[0],q[0]+s*q[1]]
    ax[0,0].plot(pos[:,0],pos[:,1],color=color);ax[0,0].plot([0,2786],[0,0],lw=7,color='#888888',alpha=.3)
    ax[0,0].scatter([q[2],ro['stop_x_m']],[0,0],color=['#bc713e',color]);ax[0,0].annotate('Touchdown', (q[2],0),xytext=(350,200),arrowprops=dict(arrowstyle='->'))
    ax[0,0].annotate(f"Stop: {ro['reserve_remaining_m']:.0f} m remain",(ro['stop_x_m'],0),xytext=(1250,500),arrowprops=dict(arrowstyle='->'))
    ax[0,0].set(xlabel='Distance from runway threshold (m)',ylabel='Right of runway (m)',title='Constructed ground track');ax[0,0].axis('equal')
    ax[0,1].plot(tt,pos[:,2],color=color);ax[0,1].axvline(q[0],color='gray',ls=':');ax[0,1].set(xlabel='Seconds from model entry',ylabel='Height above runway (m)',title=f'Threshold {q[0]:.1f}s → touchdown {q[:2].sum():.1f}s')
    for i,d in enumerate(ds):
        ax[1,0].plot(s*q[i]+(q[0] if i else 0),np.linalg.norm(d['vel'][:,:2],axis=1)/tr.KT,color=color)
    ax[1,0].plot(ro['time_s'],ro['speed_mps']/tr.KT,color=color);ax[1,0].axvline(q[:2].sum()+2,color='gray',ls=':')
    ax[1,0].set(xlabel='Seconds from model entry',ylabel='Horizontal ground speed (kt)',title=f'Fixed braking law → stop at {ro["time_s"][-1]:.1f}s')
    ax[1,1].plot(tt,np.rad2deg(np.concatenate([d['bank'] for d in ds])),color=color);ax[1,1].axhline(25,color='gray',ls=':');ax[1,1].axhline(-25,color='gray',ls=':');ax[1,1].set(xlabel='Seconds from model entry',ylabel='Bank angle (degrees)',title='Finite-rate airborne turn')
    for a in ax.flat:a.grid(alpha=.15)
    fig.suptitle('Calculated landing — uniform 070° true / 21 kt wind\nSynthetic entry/corridor; uncalibrated aircraft; no historical terrain-clearance claim',fontsize=12)
    fig.tight_layout();fig.savefig(stage/'landing.png',dpi=170);fig.savefig(stage/'landing.pdf');plt.close(fig)
    print(json.dumps(dict(status=result['status'],metrics=stats,replay_passed=replay['passed'],dense_eta=eta,verification=result['verification']),indent=2))
    return result

BUNDLE_FILES=['formula.json','path_controls.csv','result.json','landing.png','landing.pdf']

def publish_bundle(stage):
    # Stable public file links resolve through one atomic current_bundle pointer.
    # During first migration they continue to resolve to byte-identical old data.
    if any(not (stage/name).is_file() for name in BUNDLE_FILES):raise ValueError('incomplete staged bundle')
    bundles=OUT/'bundles';bundles.mkdir(exist_ok=True)
    pointer=OUT/'current_bundle'
    if not pointer.is_symlink():
        legacy=bundles/('legacy-'+uuid.uuid4().hex);legacy.mkdir()
        for name in BUNDLE_FILES:
            if (OUT/name).is_file():shutil.copy2(OUT/name,legacy/name)
        temporary=OUT/('.pointer-'+uuid.uuid4().hex)
        temporary.symlink_to(legacy.relative_to(OUT),target_is_directory=True)
        os.replace(temporary,pointer)
    for name in BUNDLE_FILES:
        public=OUT/name
        if not public.is_symlink() or os.readlink(public)!='current_bundle/'+name:
            temporary=OUT/('.link-'+uuid.uuid4().hex)
            temporary.symlink_to('current_bundle/'+name)
            os.replace(temporary,public)
    destination=bundles/('delivery-'+uuid.uuid4().hex)
    os.replace(stage,destination)
    temporary=OUT/('.pointer-'+uuid.uuid4().hex)
    temporary.symlink_to(destination.relative_to(OUT),target_is_directory=True)
    os.replace(temporary,pointer)

def produce():
    # No published file is touched until calculations, identity gates and plots pass.
    stage=Path(tempfile.mkdtemp(prefix='.delivery-stage-',dir=OUT))
    try:
        result=_produce(stage)
        if result['run_id']!=current_selection()['run_id']:raise ValueError('search generation changed during delivery')
        publish_bundle(stage)
        return result
    finally:
        if stage.exists():shutil.rmtree(stage)

if __name__=='__main__':produce()
