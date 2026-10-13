"""Fresh cross-checks and deliverable for the certified fixed candidate."""
import json,hashlib
from pathlib import Path
import numpy as np
import certify_candidate as cert
import solve_coupled as coupled
from model import trajectory as tr
from model.solve import save_csv,plot
from analytical.verify_full_landing_analysis import analytic,curves
from global_exclusion_attempt import excludes,endpoint_kinematics

HERE=Path(__file__).parent

def run():
    saved=json.loads((HERE/'continuous_certificate_refined.json').read_text())
    assert saved['certified'];q=np.array([float(x) for x in saved['q_real_decimal']])
    # The certificate's partition must cover both complete closed phases.
    for phase in [0,1]:
        cover=sorted((a,b) for p,a,b,_ in saved['cover'] if p==phase)
        assert cover[0][0]==0 and cover[-1][1]==1
        assert all(a[1]==b[0] for a,b in zip(cover,cover[1:]))
    cfg=tr.load_config();p=tr.values(cfg);ev=tr.Evaluator(cfg)
    ip=cert.coefficients([cert.I(x) for x in saved['q_real_decimal']]);fp=curves(q,p)
    rng=np.random.default_rng(9113);checks=0
    for phase in range(2):
        for s in rng.uniform(.01,.99,30):
            width=1e-5
            intervals,_,_=cert.enclose(ip[phase],cert.I(saved['q_real_decimal'][phase]),float(s-width),float(s+width),phase,ev.reference_tree)
            for point in [s-width/2,s,s+width/2]:
                a=analytic(fp[phase],q[phase],point,p)
                b=coupled.phase(fp[phase],q[phase],np.array([point]))
                for key,other,tol in [('roll','roll',1e-10),('slew','slew',1e-5),('bank','bank',1e-10),('thrust','thrust',1e-5)]:
                    assert abs(a[key]-b[other][0])<tol
                exact={'roll':1-abs(a['roll'])/np.deg2rad(5),'slew':1-abs(a['slew'])/100000,
                       'descent':1+a['gamma']/np.deg2rad(6),'eas_lower':(a['eas']-135)/40}
                for key,value in exact.items():assert cert.lo(intervals[key])<=value<=cert.hi(intervals[key])
                checks+=1
    # Reject an overstated objective before certifying flight. Stop alone fails.
    assert not excludes({'corridor':cert.I(-100)},cert.I('.1'))
    assert excludes({'thrust_lower':cert.I(-1),'corridor':cert.I(100)},cert.I('.1'))
    branch=cert.safe_atan2(cert.I(0),cert.iv.mpf([-1,1]))
    assert branch.a<=0 and branch.b>=cert.iv.pi.a
    # A certified feasible witness must survive EVERY enclosing search box.
    point=[float(saved['q_real_decimal'][i]) for i in [1,2,3,10,11]]
    box=[(4.,12.),(200.,700.),(69.,88.),(-50.,50.),(-10.,10.)]
    scales=[8,500,19,100,20]
    for depth in range(130):
        T,x,u,fx,fz=[cert.iv.mpf([a,b]) for a,b in box]
        pq=[cert.I(36),T,x,u]+[cert.Z]*6+[fx,fz];pc=cert.coefficients(pq)[1]
        for s in [0.,1.,.5,.25,.75]:
            kin=endpoint_kinematics(T,x,u,fx,fz,s) if s in (0.,1.) else None
            try:mb,_,_=cert.enclose(pc,T,s,s,1,ev.reference_tree,kinematics=kin)
            except (ValueError,ZeroDivisionError):continue
            assert not excludes(mb,cert.I(saved['eta_lower_real_decimal'])),(depth,s)
        axis=max(range(5),key=lambda k:(box[k][1]-box[k][0])/scales[k])
        a,b=box[axis];mid=(a+b)/2;box[axis]=(a,mid) if point[axis]<=mid else (mid,b)
    endpoint_checks=0
    for _ in range(12):
        z=q.copy()
        z[1]=rng.uniform(4,12);z[2]=rng.uniform(200,700);z[3]=rng.uniform(69,88)
        z[10]=rng.uniform(-50,50);z[11]=rng.uniform(-10,10)
        polys=curves(z,p)[1]
        T,x,u,fx,fz=[cert.I(repr(float(z[k]))) for k in [1,2,3,10,11]]
        for s in [0,1]:
            kin=endpoint_kinematics(T,x,u,fx,fz,s)
            for order in range(4):
                target=np.array([c.deriv(order)(s)/z[1]**order for c in polys])
                actual=np.array([(cert.lo(v)+cert.hi(v))/2 for v in kin[order]])
                assert np.max(abs(target-actual))<1e-8
            endpoint_checks+=1
    try:cert.certify(saved['q_real_decimal'],'0.04')
    except AssertionError:pass
    else:raise AssertionError('invalid claimed margin accepted')
    source_hash=cert.SOURCE_HASH
    try:
        cert.SOURCE_HASH='changed'
        try:cert.certify(saved['q_real_decimal'])
        except ValueError:pass
        else:raise AssertionError('changed source accepted')
    finally:cert.SOURCE_HASH=source_hash
    # Recompute the entire proof from its saved vector, independently of search.
    fresh=cert.certify(saved['q_real_decimal'],saved['eta_lower_real_decimal'])
    assert fresh['certified'] and fresh['accepted_intervals']==saved['accepted_intervals']
    sampled=ev.evaluate(q,2401);replay=tr.replay(sampled,cfg,reference_tree=ev.reference_tree)
    assert all(replay[k] for k in ['passed','path_constraints_passed','terminal_constraints_passed','stop_constraint_passed'])
    save_csv(HERE/'candidate.csv',sampled)
    plot(HERE/'candidate.png',ev.evaluate(tr.BASE_Q,2401),sampled,cfg)
    report=dict(status='passed',identity_interval_comparisons=checks,coverage_phases=2,
        rejection_cases=5,feasible_witness_ancestor_boxes=130,global_endpoint_identity_cases=endpoint_checks,fresh_certificate=True,certificate_intervals=fresh['accepted_intervals'],
        replay=replay,candidate=tr.summary(sampled),
        csv_rates='v1 phasewise spline estimates; proof uses exact analytic derivatives separately',
        claim='verified candidate and feasibility certificate, not global optimum')
    (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in HERE.iterdir() if f.is_file() and f.name!='manifest.json'}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return {k:v for k,v in report.items() if k not in ['replay','candidate']}

if __name__=='__main__':print(json.dumps(run(),indent=2))
