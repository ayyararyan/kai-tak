"""Smooth trajectories, inverse forces, constraints and independent Newton replay.
SI internally; x forward from threshold, y right, z above runway. This is not
flight guidance, a calibrated 747 simulator or a continuous-time certificate.
"""
from pathlib import Path
import copy
import json
import numpy as np
from numpy.polynomial import Polynomial as P
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.spatial import cKDTree

G = 9.80665
KT = 1852 / 3600
LB = 0.45359237


class HistoricalUnavailable(ValueError):
    pass


def load_config(path=None):
    path = Path(path or Path(__file__).with_name('config.json'))
    cfg = json.loads(path.read_text())
    validate_config(cfg)
    return cfg


def values(cfg):
    return {key: entry['value'] for key, entry in cfg['parameters'].items()}


def validate_config(cfg, mode='scenario'):
    if mode == 'historical':
        raise HistoricalUnavailable('BLOCKED: calibrated aircraft envelope, historical terrain/obstacles and navigation corridor input adapter unavailable; flags cannot waive these requirements.')
    if mode != 'scenario':
        raise ValueError('mode must be scenario or historical')
    if not isinstance(cfg, dict) or not isinstance(cfg.get('parameters'), dict):
        raise ValueError('configuration requires a parameters mapping')
    required = set("mass_lb vref_kt case_target_kt mass_kg initial_eas_kt start_xyz_m initial_track_deg threshold_height_m threshold_gamma_deg touchdown_sink_mps touchdown_x_min_m touchdown_x_max_m touchdown_y_tol_m touchdown_track_tol_deg touchdown_bank_tol_deg touchdown_sink_max_mps reserve_m bank_limit_deg roll_limit_deg_s cl_min cl_max load_min_g load_max_g eas_min_kt eas_max_kt descent_limit_deg approach_sink_max_mps thrust_max_n thrust_slew_n_s rho0_kg_m3 density_scale_m wing_area_m2 cd0 induced_factor brake_delay_s brake_deceleration_mps2 corridor_halfwidth_m wind_mps lda_m".split())
    missing = required - cfg['parameters'].keys()
    if missing:
        raise ValueError(f'missing parameters: {sorted(missing)}')
    for key, entry in cfg['parameters'].items():
        if not isinstance(entry, dict) or not all(k in entry for k in ('value', 'unit', 'category', 'source')):
            raise ValueError(f'provenance missing: {key}')
        if any(not isinstance(entry[k], str) or not entry[k].strip() for k in ('unit', 'category', 'source')):
            raise ValueError(f'invalid provenance: {key}')
        try:
            numeric = np.asarray(entry['value'], dtype=float)
            expected = (3,) if key in ('wind_mps', 'start_xyz_m') else ()
            if numeric.shape != expected or not np.all(np.isfinite(numeric)):
                raise ValueError(f'invalid shape or nonfinite parameter: {key}')
            if np.asarray(entry['value']).dtype.kind not in 'iuf':
                raise ValueError(f'parameter must be numeric: {key}')
        except (TypeError, ValueError) as exc:
            raise ValueError(f'invalid parameter {key}') from exc
    p = values(cfg)
    if cfg.get('wind_type') != 'constant' or np.shape(p['wind_mps']) != (3,):
        raise ValueError('only constant 3-vector wind supported; wind acceleration is not implemented')
    for key in ('touchdown_y_tol_m','touchdown_track_tol_deg','touchdown_bank_tol_deg','approach_sink_max_mps','threshold_height_m','mass_kg','wing_area_m2','rho0_kg_m3','density_scale_m','bank_limit_deg','roll_limit_deg_s','cl_max','thrust_max_n','thrust_slew_n_s','brake_deceleration_mps2','corridor_halfwidth_m','lda_m','eas_min_kt','eas_max_kt','touchdown_sink_max_mps'):
        if p[key] <= 0:
            raise ValueError(f'{key} must be positive')
    if not 0 < p['eas_min_kt'] < p['initial_eas_kt'] < p['eas_max_kt']:
        raise ValueError('initial speed must be within positive EAS envelope')
    if not 0 <= p['cl_min'] < p['cl_max'] or not 0 < p['load_min_g'] < p['load_max_g']:
        raise ValueError('invalid lift/load envelope')
    if p['brake_delay_s'] < 0 or not 0 <= p['reserve_m'] < p['lda_m']:
        raise ValueError('invalid stopping geometry')
    if p['touchdown_x_max_m'] <= p['touchdown_x_min_m'] or p['touchdown_x_min_m'] <= 0:
        raise ValueError('invalid touchdown interval')
    if p['cd0'] < 0 or p['induced_factor'] < 0 or not 0 < p['descent_limit_deg'] < 90:
        raise ValueError('invalid drag/descent envelope')
    if np.shape(p['start_xyz_m']) != (3,) or p['start_xyz_m'][2] <= 0:
        raise ValueError('invalid start position')
    if not 0 < p['bank_limit_deg'] < 90 or not -90 < p['threshold_gamma_deg'] < 0 or not -p['descent_limit_deg'] <= p['threshold_gamma_deg']:
        raise ValueError('invalid angular envelope')
    if not 0 <= p['touchdown_sink_mps'] <= p['touchdown_sink_max_mps']:
        raise ValueError('invalid touchdown sink')
    if not isinstance(cfg.get('obstacles', []), list):
        raise ValueError('obstacles must be a list')
    for ob in cfg.get('obstacles', []):
        if not isinstance(ob, dict):
            raise ValueError('invalid cylindrical obstacle')
        required = ('x_m','y_m','radius_m','height_m','clearance_m')
        if any(k not in ob or not isinstance(ob[k], (int, float)) or not np.isfinite(ob[k]) for k in required):
            raise ValueError('invalid cylindrical obstacle')
        if any(ob[k] < 0 for k in ('radius_m','height_m','clearance_m')):
            raise ValueError('negative obstacle dimension')
    return p


def density(z, p):
    return p['rho0_kg_m3'] * np.exp(-np.asarray(z) / p['density_scale_m'])


def endpoint_velocity(eas_kt, z, track_deg, gamma_deg, p):
    """Fix EAS and air gamma plus ground track under declared steady wind."""
    w = np.array(p['wind_mps'], dtype=float)
    tas = eas_kt * KT * np.sqrt(p['rho0_kg_m3'] / density(z, p))
    gam, tr = np.deg2rad([gamma_deg, track_deg])
    d = np.array([np.cos(tr), np.sin(tr)])
    wd = np.dot(w[:2], d)
    disc = (tas * np.cos(gam))**2 - np.dot(w[:2], w[:2]) + wd**2
    if disc <= 0:
        raise ValueError('wind prevents prescribed ground-track endpoint')
    groundspeed = wd + np.sqrt(disc)
    if groundspeed <= 0:
        raise ValueError('nonpositive endpoint groundspeed')
    return np.r_[groundspeed*d, tas*np.sin(gam)+w[2]]


def quintic(p0, p1, v0, v1, a0, a1, duration):
    if not np.isfinite(duration) or duration <= 0:
        raise ValueError('flight duration must be positive finite')
    c = np.zeros((6, 3))
    c[0], c[1], c[2] = p0, np.asarray(v0)*duration, np.asarray(a0)*duration**2/2
    c[3:] = np.linalg.solve(np.array([[1,1,1],[3,4,5],[6,12,20]],float),
        np.array([np.asarray(p1)-c[:3].sum(axis=0), np.asarray(v1)*duration-c[1]-2*c[2], np.asarray(a1)*duration**2-2*c[2]]))
    return [P(c[:,j]) for j in range(3)]


# q=[approach seconds, flare seconds, touchdown x, touchdown vx,
#    approach x/y/z even and odd endpoint-null bump amplitudes, flare x/z bumps].
BASE_Q = np.array([36., 6.5, 500., 77., 0.,0.,0.,0.,0.,0.,0.,0.])
BOUNDS = [(30,55),(4,12),(200,700),(69,88)] + [(-400,400),(-400,400),(-400,400),(-400,400),(-50,50),(-50,50),(-50,50),(-10,10)]
BUMP = P([0,0,0,1,-3,3,-1])*64  # peak 1, first two derivatives vanish at endpoints
ODD = BUMP * P([-1,2])


def curves(q, cfg):
    p = validate_config(cfg)
    q = np.asarray(q, dtype=float)
    if q.shape != (12,) or not np.all(np.isfinite(q)) or q[0] <= 0 or q[1] <= 0 or q[3] <= 0:
        raise ValueError('invalid trajectory decision vector')
    start = np.array(p['start_xyz_m'])
    gate = np.array([0.,0.,p['threshold_height_m']])
    v0 = endpoint_velocity(p['initial_eas_kt'],start[2],p['initial_track_deg'],p['threshold_gamma_deg'],p)
    vg = endpoint_velocity(p['initial_eas_kt'],gate[2],0,p['threshold_gamma_deg'],p)
    vend = np.array([q[3],0.,-p['touchdown_sink_mps']])
    a = quintic(start,gate,v0,vg,np.zeros(3),np.zeros(3),q[0])
    f = quintic(gate,np.array([q[2],0.,0.]),vg,vend,np.zeros(3),np.zeros(3),q[1])
    for j in range(3):
        a[j] += q[4+2*j]*BUMP + q[5+2*j]*ODD
    f[0] += q[10]*BUMP
    f[2] += q[11]*BUMP
    return a,f


def kinematics(q,cfg,n=121):
    if n < 5:
        raise ValueError('at least five samples per segment required')
    a,f = curves(q,cfg)
    arrays = []
    for i,(polys,T) in enumerate(zip((a,f),q[:2])):
        s = np.linspace(0,1,n)
        # keep threshold only once, preserving C2 connection
        if i:
            s = s[1:]
        pos = np.column_stack([v(s) for v in polys])
        vel = np.column_stack([v.deriv()(s)/T for v in polys])
        acc = np.column_stack([v.deriv(2)(s)/T**2 for v in polys])
        arrays.append((s*T+(q[0] if i else 0),pos,vel,acc,np.full(len(s),i)))
    return tuple(np.concatenate([x[j] for x in arrays]) for j in range(5))


def flight_basis(velocity_air):
    V = np.linalg.norm(velocity_air,axis=-1)
    if np.any(V <= 1e-8) or not np.all(np.isfinite(V)):
        raise ValueError('airspeed must be positive finite')
    tangent = velocity_air/V[...,None]
    psi = np.arctan2(velocity_air[...,1],velocity_air[...,0])
    gamma = np.arctan2(velocity_air[...,2],np.linalg.norm(velocity_air[...,:2],axis=-1))
    right = np.stack([-np.sin(psi),np.cos(psi),np.zeros_like(psi)],axis=-1)
    up = np.stack([-np.sin(gamma)*np.cos(psi),-np.sin(gamma)*np.sin(psi),np.cos(gamma)],axis=-1)
    return V,psi,gamma,tangent,right,up


def inverse(pos,vel,acc,p):
    V,psi,gamma,et,er,eu = flight_basis(vel-np.array(p['wind_mps']))
    force = p['mass_kg']*(acc+np.array([0.,0.,G]))
    Lu = np.sum(force*eu,axis=-1)
    Lr = np.sum(force*er,axis=-1)
    lift = np.hypot(Lu,Lr)
    bank = np.arctan2(Lr,Lu)
    dyn = .5*density(pos[:,2],p)*V**2*p['wing_area_m2']
    cl = lift/dyn
    drag = dyn*(p['cd0']+p['induced_factor']*cl**2)
    thrust = drag + np.sum(force*et,axis=-1)
    return dict(tas_mps=V,eas_kt=V*np.sqrt(density(pos[:,2],p)/p['rho0_kg_m3'])/KT,
        air_heading_rad=psi,gamma_rad=gamma,bank_rad=bank,cl=cl,thrust_n=thrust,
        drag_n=drag,load_g=lift/(p['mass_kg']*G),lift_n=lift)


def rollout(q,p,n=101):
    if q[3] <= 0 or p['brake_deceleration_mps2'] <= 0 or p['brake_delay_s'] < 0:
        raise ValueError('invalid rollout inputs')
    delay,dec,v = p['brake_delay_s'],p['brake_deceleration_mps2'],q[3]
    time = np.unique(np.r_[np.linspace(0,delay+v/dec,n),delay])
    braking = np.maximum(time-delay,0)
    velocity = np.maximum(v-dec*braking,0)
    x = q[2]+v*np.minimum(time,delay)+v*braking-.5*dec*braking**2
    return dict(time_s=time+q[0]+q[1],x_m=x,speed_mps=velocity,
                stop_x_m=float(x[-1]),reserve_remaining_m=float(p['lda_m']-x[-1]))


def phase_splines(t, values, phase):
    """Separate interpolants: the C2 spatial join need not have C1 controls."""
    join = np.flatnonzero(np.diff(phase) != 0)
    if len(join) != 1 or phase[0] != 0 or phase[-1] != 1:
        raise ValueError('expected approach then flare with one shared join')
    j = int(join[0])
    return j, (CubicSpline(t[:j+1], values[:j+1]), CubicSpline(t[j:], values[j:]))


def phase_derivative(t, values, phase):
    # Finite-grid approximation, not a continuous-time derivative certificate.
    j, splines = phase_splines(t, values, phase)
    left, right = splines[0].derivative()(t[:j+1]), splines[1].derivative()(t[j:])
    result = np.concatenate([left, right[1:]])
    result[j] = np.where(np.abs(left[-1]) >= np.abs(right[0]), left[-1], right[0])
    return result


def obstacle_margins(pos, touchdown_x, stop_x, obstacles, width):
    """Airborne sampled margins plus exact clearance of straight runway rollout."""
    result = {}
    lo, hi = sorted((touchdown_x, stop_x))
    for i, ob in enumerate(obstacles):
        radial = np.linalg.norm(pos[:,:2]-[ob['x_m'],ob['y_m']], axis=1)-ob['radius_m']-ob['clearance_m']
        above = pos[:,2]-ob['height_m']-ob['clearance_m']
        nearest_x = np.clip(ob['x_m'], lo, hi)
        ground_radial = np.hypot(nearest_x-ob['x_m'], ob['y_m'])-ob['radius_m']-ob['clearance_m']
        ground_above = -ob['height_m']-ob['clearance_m']
        result[f'obstacle_{i}'] = np.r_[np.maximum(radial, above), max(ground_radial, ground_above)]/width
    return result


class Evaluator:
    def __init__(self,cfg):
        self.cfg=copy.deepcopy(cfg)
        self.p=validate_config(cfg)
        _,xyz,*_ = kinematics(BASE_Q,cfg,1001)
        self.reference_tree=cKDTree(xyz)

    def evaluate(self,q,n=121,kinematics_override=None):
        p=self.p
        t,pos,vel,acc,phase=kinematics(q,self.cfg,n) if kinematics_override is None else kinematics_override
        d=inverse(pos,vel,acc,p)
        d.update(time_s=t,pos=pos,vel=vel,acc=acc,phase=phase)
        d['roll_rad_s']=phase_derivative(t,np.unwrap(d['bank_rad']),phase)
        d['thrust_slew_n_s']=phase_derivative(t,d['thrust_n'],phase)
        d['track_rad']=np.arctan2(vel[:,1],vel[:,0])
        d['corridor_distance_m']=self.reference_tree.query(pos)[0]
        ro=rollout(q,p)
        m={}
        def band(name,x,lo,hi):
            m[name+'_lower']=(np.asarray(x)-lo)/(hi-lo)
            m[name+'_upper']=(hi-np.asarray(x))/(hi-lo)
        band('eas',d['eas_kt'],p['eas_min_kt'],p['eas_max_kt'])
        band('cl',d['cl'],p['cl_min'],p['cl_max'])
        band('load',d['load_g'],p['load_min_g'],p['load_max_g'])
        band('thrust',d['thrust_n'],0,p['thrust_max_n'])
        m['bank']=1-np.abs(d['bank_rad'])/np.deg2rad(p['bank_limit_deg'])
        m['roll_rate']=1-np.abs(d['roll_rad_s'])/np.deg2rad(p['roll_limit_deg_s'])
        m['thrust_slew']=1-np.abs(d['thrust_slew_n_s'])/p['thrust_slew_n_s']
        m['descent']=1+d['gamma_rad']/np.deg2rad(p['descent_limit_deg'])
        m['approach_sink']=1+vel[phase==0,2]/p['approach_sink_max_mps']
        m['corridor']=1-d['corridor_distance_m']/p['corridor_halfwidth_m']
        band('touchdown_x',q[2],p['touchdown_x_min_m'],p['touchdown_x_max_m'])
        band('touchdown_sink',-vel[-1,2],0,p['touchdown_sink_max_mps'])
        m['touchdown_lateral']=np.array([1-abs(pos[-1,1])/p['touchdown_y_tol_m']])
        m['touchdown_track']=np.array([1-abs(d['track_rad'][-1])/np.deg2rad(p['touchdown_track_tol_deg'])])
        m['touchdown_bank']=np.array([1-abs(d['bank_rad'][-1])/np.deg2rad(p['touchdown_bank_tol_deg'])])
        m['stop_reserve']=np.array([(p['lda_m']-p['reserve_m']-ro['stop_x_m'])/(p['lda_m']-p['reserve_m'])])
        m.update(obstacle_margins(pos, q[2], ro['stop_x_m'], self.cfg.get('obstacles', []), p['corridor_halfwidth_m']))
        m={k:np.atleast_1d(v) for k,v in m.items()}
        # Hard-only constraints: structural contact has exactly zero clearance.
        hard={'ground_height':pos[:,2]/100, 'positive_forward_groundspeed':vel[:,0]/100,
              'positive_lift_up':np.cos(d['bank_rad'])}
        effort=float(np.trapezoid((d['bank_rad']/np.deg2rad(p['bank_limit_deg']))**2+
            (d['roll_rad_s']/np.deg2rad(p['roll_limit_deg_s']))**2+
            (d['thrust_slew_n_s']/p['thrust_slew_n_s'])**2,t))
        return d,m,hard,ro,effort


def summary(evaluated):
    d,m,h,ro,eff=evaluated
    for group in (d,m,h,ro,{'effort':eff}):
        for key,value in group.items():
            a=np.asarray(value)
            if not a.size or not np.all(np.isfinite(a)):
                raise ValueError(f'nonfinite or empty diagnostic: {key}')
    mins={k:float(np.min(v)) for k,v in m.items()}
    hard={k:float(np.min(v)) for k,v in h.items()}
    return dict(category='scenario-based',evidence='sampled nominal diagnostics, not continuous certificate',
        eta=min(mins.values()),margin_minima=mins,hard_minima=hard,
        violations={k:v for k,v in (mins|hard).items() if v < -1e-6},
        sampled_feasible=min([*mins.values(),*hard.values()])>=-1e-6,
        effort=eff,stop_x_m=ro['stop_x_m'],reserve_remaining_m=ro['reserve_remaining_m'],
        max_bank_deg=float(np.rad2deg(np.abs(d['bank_rad']).max())),
        max_roll_deg_s=float(np.rad2deg(np.abs(d['roll_rad_s']).max())),
        eas_range_kt=[float(d['eas_kt'].min()),float(d['eas_kt'].max())],
        thrust_range_n=[float(d['thrust_n'].min()),float(d['thrust_n'].max())],
        touchdown_x_m=float(d['pos'][-1,0]),flight_duration_s=float(d['time_s'][-1]))


def replay(evaluated,cfg,reference_tree=None):
    """Integrate forces independently of the reference polynomial acceleration.
    Controls are time-indexed bank, CL and thrust, held to their interpolated
    values. Orientation and drag are recomputed from the integrated air velocity.
    Ground impact impulse removes residual vertical velocity at touchdown.
    """
    d,_,_,ro,_=evaluated
    p=validate_config(cfg)
    t=d['time_s']
    summary(evaluated)  # Reject nonfinite state/controls before integrating.
    join, controls=phase_splines(t,np.column_stack([d['bank_rad'],d['cl'],d['thrust_n']]),d['phase'])
    def control(time):
        return controls[0 if time <= t[join] else 1](time)
    def rhs(time,state):
        pos,vel=state[:3],state[3:]
        V,_,_,et,er,eu=flight_basis(vel-np.array(p['wind_mps']))
        phi,cl,T=control(time)
        dyn=.5*density(pos[2],p)*V**2*p['wing_area_m2']
        L=dyn*cl
        D=dyn*(p['cd0']+p['induced_factor']*cl**2)
        acc=((T-D)*et+L*(np.cos(phi)*eu+np.sin(phi)*er))/p['mass_kg']-[0,0,G]
        return np.r_[vel,acc]
    sol=solve_ivp(rhs,(t[0],t[-1]),np.r_[d['pos'][0],d['vel'][0]],t_eval=t,
                  rtol=2e-10,atol=1e-10,max_step=.1)
    if not sol.success or sol.y.shape[1] != len(t):
        return dict(passed=False,integration_success=False,message=sol.message)
    pos,vel=sol.y[:3].T,sol.y[3:].T
    errp=float(np.linalg.norm(pos-d['pos'],axis=1).max())
    errv=float(np.linalg.norm(vel-d['vel'],axis=1).max())
    # Independently integrate the fixed ground rule after the touchdown impulse.
    delay=p['brake_delay_s']; dec=p['brake_deceleration_mps2']; vx=vel[-1,0]
    coast_end=pos[-1,0]+vx*delay
    ground=solve_ivp(lambda t,s:[s[1],-dec],(0,max(vx,0)/dec),[coast_end,vx],rtol=1e-11,atol=1e-11)
    if not ground.success or not np.all(np.isfinite(ground.y)):
        return dict(passed=False,integration_success=False,message='ground integration failed')
    stop_x = float(ground.y[0,-1])
    stop_error=float(abs(stop_x-ro['stop_x_m']))
    # Check integrated states and replayed forces, never polynomial acceleration.
    acceleration=np.array([rhs(time,state)[3:] for time,state in zip(t,sol.y.T)])
    q_replay=np.array([t[join]-t[0],t[-1]-t[join],pos[-1,0],vx]+[0.]*8)
    checker=Evaluator(cfg)
    if reference_tree is not None:
        checker.reference_tree=reference_tree
    checked=checker.evaluate(q_replay,kinematics_override=(t,pos,vel,acceleration,d['phase']))
    checked[3]['stop_x_m']=stop_x
    checked[3]['reserve_remaining_m']=p['lda_m']-stop_x
    checked[1]['stop_reserve']=np.array([(p['lda_m']-p['reserve_m']-stop_x)/(p['lda_m']-p['reserve_m'])])
    checked[1].update(obstacle_margins(pos,pos[-1,0],stop_x,cfg.get('obstacles',[]),p['corridor_halfwidth_m']))
    # z=0 at the last point is a prescribed contact equality. Report its residual
    # separately; every non-contact airborne altitude remains a hard inequality.
    checked[2]['ground_height']=checked[2]['ground_height'][:-1]
    replay_summary=summary(checked)
    all_minima=replay_summary['margin_minima'] | replay_summary['hard_minima']
    negative={k:v for k,v in all_minima.items() if v < 0}
    # Conservative numerical classification only, not a widened envelope or a
    # proved integration-error bound. Both signs near zero remain unresolved.
    boundary={k:v for k,v in all_minima.items() if abs(v) <= 1e-6}
    constraint_status='violated' if any(v < -1e-6 for v in negative.values()) else ('boundary_unresolved' if boundary else 'passed')
    path_ok=constraint_status == 'passed'
    terminal_keys=[k for k in all_minima if k.startswith('touchdown_')]
    terminal_boundary={k:all_minima[k] for k in terminal_keys if abs(all_minima[k]) <= 1e-6}
    terminal_status='violated' if any(all_minima[k] < -1e-6 for k in terminal_keys) or abs(pos[-1,2]) >= .05 else ('boundary_unresolved' if terminal_boundary else 'passed')
    touchdown_ok=terminal_status == 'passed'
    stop_ok=bool(all_minima['stop_reserve'] > 1e-6)
    return dict(passed=bool(errp<.05 and errv<.005 and stop_error<.1),
        terminal_constraints_passed=touchdown_ok,stop_constraint_passed=stop_ok,
        path_constraints_passed=path_ok,constraint_status=constraint_status,
        numerical_boundary_band_normalized=1e-6,
        replay_constraint_summary=replay_summary,boundary_unresolved=boundary,
        terminal_boundary_unresolved=terminal_boundary,terminal_constraint_status=terminal_status,contact_height_residual_m=float(pos[-1,2]),
        constraint_evidence='integrated-state airborne samples; phasewise one-sided rates; exact straight rollout obstacle clearance; no continuous-flight certificate',
        integration_success=True,max_position_error_m=errp,max_velocity_error_mps=errv,
        touchdown_xyz_m=pos[-1].tolist(),touchdown_velocity_mps=vel[-1].tolist(),
        stop_x_m=float(ground.y[0,-1]),stop_error_m=stop_error,
        tolerances={'position_m':.05,'velocity_mps':.005,'stop_m':.1},
        control_semantics='nominal time-indexed CL, bank and thrust; not feedback',
        ground_contact='inelastic removal of vertical velocity; deceleration begins after fixed delay')
