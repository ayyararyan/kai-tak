"""Source-conditional gear plan, kinematics and partial systems logic.
Not a calibrated aircraft model, sensor model, or historical clearance evaluator.
Angular cross products require a declared RIGHT-HANDED body/world basis.
"""
import itertools
import math
import numpy as np

INCH = .0254

def finite_vector(x, name):
    a = np.asarray(x, dtype=float)
    if a.shape != (3,) or not np.isfinite(a).all():
        raise ValueError(name + ' must be a finite 3-vector')
    return a

def wheel_plan():
    """18 nominal wheel centre xy values, aft/right, nose-axle origin.
    Derived from Boeing RevF p7-5 imperial dimensions; z is unknown.
    Drawing says NOT TO SCALE. Never digitize pixel distances as dimensions.
    """
    out = []
    for side in [-1, 1]:
        out.append(dict(id=f'nose_{side}',gear='nose',aft_m=0.,right_m=side*18*INCH,z_m=None))
        for gear, station, track in [('wing',947.5,433),('body',1068.5,151)]:
            for axle in [-1,1]:
                for tyre in [-1,1]:
                    out.append(dict(id=f'{gear}_{side}_{axle}_{tyre}',gear=gear,
                        aft_m=(station+axle*29)*INCH,
                        right_m=(side*track/2+tyre*22)*INCH,z_m=None))
    return out

def landing_cg_percent_mac(fuel_centroid_percent_mac, *, landing_lb=525718, zero_fuel_lb=476116, zero_fuel_cg=27.1):
    """Conditional mass-moment identity, not a measured landing CG or CG bound."""
    vals=[fuel_centroid_percent_mac,landing_lb,zero_fuel_lb,zero_fuel_cg]
    if not all(math.isfinite(float(x)) for x in vals) or not 0 < zero_fuel_lb <= landing_lb:
        raise ValueError('invalid loading inputs')
    return (zero_fuel_lb*zero_fuel_cg+(landing_lb-zero_fuel_lb)*fuel_centroid_percent_mac)/landing_lb

def partial_boolean(formula, *values):
    """Complete unknown Boolean inputs both ways; only return a common result."""
    if any(v is not None and type(v) is not bool for v in values):
        raise ValueError('logic inputs must be bool or None')
    outcomes={formula(*row) for row in itertools.product(*[([False,True] if v is None else [v]) for v in values])}
    return outcomes.pop() if len(outcomes)==1 else None

def spoiler_command(position, ground, idle1, idle3, reverse2_idle_detent, reverse4_idle_detent):
    """Only the three automatic transitions explicitly described in Appendix3.
    'none' means no transition from THESE predicates, not no other system effect.
    Actuator travel times, sensor rules/failures and manual commands are absent.
    """
    if position not in ('DN','ARM','UP'):
        raise ValueError('only DN/ARM/UP automatic transitions are represented')
    values=(ground,idle1,idle3,reverse2_idle_detent,reverse4_idle_detent)
    if position=='DN': pred=lambda g,i,j,r,s:g and i and j and (r or s)
    elif position=='ARM': pred=lambda g,i,j,r,s:g and i and j
    else: pred=lambda g,i,j,r,s:g and (not i or not j)
    result=partial_boolean(pred,*values)
    return 'unknown' if result is None else ('raise' if position!='UP' else 'lower') if result else 'none'

def reverse_selection_permitted(ground, idle):
    """Report p15 necessary interlock condition; not deployment or force prediction."""
    return partial_boolean(lambda g,i:g and i,ground,idle)

def autobrake_activation_prerequisites(armed, main_spinup, main_on_ground, idle1,idle2,idle3,idle4):
    """Necessary source predicates, NOT a complete autobrake controller.
    The source's 3-second idle/disarm timer must be modeled separately with history.
    """
    return partial_boolean(lambda *v:all(v),armed,main_spinup,main_on_ground,idle1,idle2,idle3,idle4)

def deforming_point_kinematics(cg,velocity,acceleration,R,omega,alpha,b,bdot,bddot):
    """World contact material point including supplied suspension/deformation.
    R maps a right-handed body basis to a right-handed world basis. No pose or
    suspension state is inferred from the static plan or point-mass inverse forces.
    """
    cg,velocity,acceleration,omega,alpha,b,bdot,bddot=[finite_vector(v,n) for v,n in zip(
        [cg,velocity,acceleration,omega,alpha,b,bdot,bddot],
        ['cg','velocity','acceleration','omega','alpha','b','bdot','bddot'])]
    R=np.asarray(R,dtype=float)
    if R.shape!=(3,3) or not np.isfinite(R).all() or not np.allclose(R.T@R,np.eye(3),atol=1e-10,rtol=0) or not math.isclose(np.linalg.det(R),1,abs_tol=1e-10):
        raise ValueError('R must be a proper orthogonal matrix')
    d=R@b;u=R@bdot
    return (cg+d,velocity+np.cross(omega,d)+u,
        acceleration+np.cross(alpha,d)+np.cross(omega,np.cross(omega,d))+2*np.cross(omega,u)+R@bddot)

def plane_observation(position,velocity,normal,offset):
    """Signed gap and gap speed to a stationary plane; no collision certificate.
    Plane n.p=offset; normalization returns metres and metres/second.
    """
    p=finite_vector(position,'position');v=finite_vector(velocity,'velocity');n=finite_vector(normal,'normal')
    norm=np.linalg.norm(n)
    if not math.isfinite(float(offset)) or norm==0:raise ValueError('invalid plane')
    return dict(gap_m=float((n@p-offset)/norm),normal_speed_mps=float(n@v/norm))
