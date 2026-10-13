"""Whole-body continuous enclosure primitives; no implicit historical certification.

World/reference components: forward,right,up in a declared frame. Positive yaw
turns right, positive pitch raises nose, positive bank lowers right wing.
The reference can be CG/gear only if body_reference is supplied explicitly.
"""
from pathlib import Path
import sys,math
from fractions import Fraction as F
from math import comb
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent/'python_deps'))
from mpmath import iv
iv.dps=40


def finite(x,name='value'):
    a=np.asarray(x,dtype=float)
    if not np.all(np.isfinite(a)):raise ValueError(name+' must be finite')
    return a


def interval(x):
    if len(x)!=2:raise ValueError('interval needs two endpoints')
    a=finite(x)
    if a[0]>a[1]:raise ValueError('reversed interval')
    return iv.mpf([str(x[0]),str(x[1])])


def polynomial_range(coefficients,a=0,b=1):
    """Exact rational Bernstein hull on a supplied normalized phase subinterval."""
    finite(coefficients);finite([a,b])
    a,b=F(str(a)),F(str(b))
    if not 0<=a<=b<=1:raise ValueError('phase extrapolation is not permitted')
    c=[F(str(x)) for x in coefficients]
    if not c:raise ValueError('empty polynomial')
    n=len(c)-1
    power=[sum(c[k]*comb(k,j)*a**(k-j)*(b-a)**j for k in range(j,n+1)) for j in range(n+1)]
    bern=[sum(power[j]*F(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]
    return min(bern),max(bern)


def outward_float(x,up=False):
    return float(np.nextafter(float(x),math.inf if up else -math.inf))


def polynomial_position_box(coefficients_xyz,a=0,b=1):
    if len(coefficients_xyz)!=3:raise ValueError('three position polynomials required')
    return [[outward_float(lo),outward_float(hi,True)] for lo,hi in (polynomial_range(c,a,b) for c in coefficients_xyz)]


def rotation(yaw,pitch,bank):
    """Numeric pose helper, radians; independent tests check explicit rotation signs."""
    finite([yaw,pitch,bank]);cy,sy=math.cos(yaw),math.sin(yaw);cp,sp=math.cos(pitch),math.sin(pitch);cb,sb=math.cos(bank),math.sin(bank)
    return np.array([[cy,-sy,0],[sy,cy,0],[0,0,1.]])@np.array([[cp,0,-sp],[0,1,0],[sp,0,cp]])@np.array([[1,0,0],[0,cb,sb],[0,-sb,cb]])


def enclose_body(vertices,body_reference,position_ranges,angle_ranges,tracking_xyz=(0,0,0)):
    """Interval enclosure for ALL times covered by caller's position/angle boxes.

    No sampling-based angle range is promoted to an all-time bound. Each supplied
    vertex and reference offset is interpreted as its exact real-decimal string.
    Bounds apply to convex hull of vertices and independent tracking box.
    """
    vertices=finite(vertices,'vertices');ref=finite(body_reference,'body_reference');track=finite(tracking_xyz,'tracking')
    if vertices.ndim!=2 or vertices.shape[1]!=3 or len(vertices)<1:raise ValueError('vertices must be Nx3')
    if ref.shape!=(3,) or track.shape!=(3,) or np.any(track<0):raise ValueError('invalid reference or tracking box')
    if len(position_ranges)!=3 or len(angle_ranges)!=3:raise ValueError('three ranges required')
    pos=[interval(x) for x in position_ranges];yaw,pitch,bank=[interval(x) for x in angle_ranges]
    cy,sy=iv.cos(yaw),iv.sin(yaw);cp,sp=iv.cos(pitch),iv.sin(pitch);cb,sb=iv.cos(bank),iv.sin(bank)
    R=iv.matrix([[cy,-sy,0],[sy,cy,0],[0,0,1]])*iv.matrix([[cp,0,-sp],[0,1,0],[sp,0,cp]])*iv.matrix([[1,0,0],[0,cb,sb],[0,-sb,cb]])
    lows=[];highs=[]
    for v in vertices:
        vv=iv.matrix([iv.mpf(str(v[i]))-iv.mpf(str(ref[i])) for i in range(3)]);w=R*vv
        q=[pos[i]+w[i]+iv.mpf([str(-track[i]),str(track[i])]) for i in range(3)]
        lows.append([outward_float(x.a) for x in q]);highs.append([outward_float(x.b,True) for x in q])
    return np.array([np.min(lows,axis=0),np.max(highs,axis=0)])


def box_clearance(body_bounds,obstacle_bounds):
    """Axis separation lower bound; positive => disjoint supplied outer boxes.
    Nonpositive => possible intersection ONLY. This is not physical collision proof.
    """
    b=finite(body_bounds);o=finite(obstacle_bounds)
    if b.shape!=(2,3) or o.shape!=(2,3) or np.any(b[0]>b[1]) or np.any(o[0]>o[1]):raise ValueError('invalid bounds')
    # nextafter protects the single floating subtraction used in each separation.
    gaps=np.maximum(np.nextafter(o[0]-b[1],-np.inf),np.nextafter(b[0]-o[1],-np.inf))
    axis=int(np.argmax(gaps));return {'separated':bool(gaps[axis]>0),'separating_axis':axis,'gap_lower_m':float(gaps[axis]),'overlap_means':'possible intersection, not collision'}


def screen_scene(body_bounds,features,coverage_complete=False):
    """Conservative broad-phase screen of same-frame supplied feature bounds.
    Unknown top at a horizontally intersecting footprint cannot pass as zero.
    No global completeness from counts of known features.
    """
    b=finite(body_bounds)
    if b.shape!=(2,3) or np.any(b[0]>b[1]):raise ValueError('invalid body box')
    unknown=[];possible=[];clear=[]
    for f in features:
        xy=finite(f['xy_bounds'])
        if xy.shape!=(2,2) or np.any(xy[0]>xy[1]):raise ValueError('invalid footprint bbox')
        if np.any(b[1,:2]<xy[0]) or np.any(b[0,:2]>xy[1]):continue
        if f.get('top_upper_m') is None or not f.get('same_frame_and_epoch_verified',False):unknown.append(f['id']);continue
        top=float(finite(f['top_upper_m']))
        gap=float(np.nextafter(b[0,2]-top,-np.inf))
        if gap>0:clear.append({'id':f['id'],'vertical_gap_lower_m':gap})
        else:possible.append(f['id'])
    if not coverage_complete:unknown.append('unresolved_relevant_scene_coverage')
    return {'status':'unknown' if unknown else ('possible_intersection' if possible else 'clear_for_supplied_enclosures'), 'unknown':unknown,'possible_intersections':possible,'cleared_features':clear,'historical_certified':False,'scope':'continuous geometric enclosure conditional on supplied bounds; no empirical validity inferred'}


def reference_kinematics(r_ref,v_ref,a_ref,R,omega,alpha,b_cg,b_ref):
    """Transfer a genuine rigid-body reference to CG using WORLD angular vectors.
    Uses right-handed component algebra for cross products: callers must convert
    physical angular vectors consistently if using forward/right/up coordinates.
    Prefer use in ENU; not a replacement of frozen point-mass dynamics.
    """
    r,v,a=map(finite,(r_ref,v_ref,a_ref));RR=finite(R);w,al,bc,br=map(finite,(omega,alpha,b_cg,b_ref))
    if any(x.shape!=(3,) for x in (r,v,a,w,al,bc,br)) or RR.shape!=(3,3):raise ValueError('dimensions')
    if not np.allclose(RR.T@RR,np.eye(3),atol=1e-12,rtol=0) or not np.isclose(np.linalg.det(RR),1,atol=1e-12):raise ValueError('rotation')
    d=RR@(bc-br)
    return r+d,v+np.cross(w,d),a+np.cross(al,d)+np.cross(w,np.cross(w,d))
