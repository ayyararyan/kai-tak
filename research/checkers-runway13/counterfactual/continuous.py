"""Outward-rounded interval feasibility of a fixed REAL-DECIMAL candidate.

mpmath interval arithmetic at 40 decimal digits. Covers closed phase intervals;
does not use a grid as a feasibility certificate. Does not prove optimality.
"""
import sys,json,hashlib,math,time
from decimal import Decimal, InvalidOperation
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mpmath import iv
import numpy as np
from model import trajectory as tr

iv.dps=40
I=lambda x:iv.mpf(str(x))
Z=I(0)
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),Z)
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):return iv.sqrt(sum((x**2 for x in a),Z))
def lo(x):return float(x.a)
def hi(x):return float(x.b)
def positive(x):return bool(x.a>=0)
def safe_atan2(y,x):
    # mpmath 1.3.0 iv.atan2(0,[-a,b]) can return [pi,pi] even when b>0.
    # Never trust its branch-cut enclosure. On x>0 there is no branch cut;
    # elsewhere use the full rigorous range. Candidate acceptance proves x>0.
    if x.a<=0:return iv.mpf([-iv.pi.b,iv.pi.b])
    return iv.atan2(y,x)

def deriv(c,k=1):
    for _ in range(k):c=[(i+1)*c[i+1] for i in range(len(c)-1)]
    return c

def horner(c,x):
    result=Z
    for v in reversed(c):result=result*x+v
    return result

def poly(c,left,right):
    # Centered Taylor polynomial: outward-rounded exact algebra.
    mid=(I(left)+I(right))/2;rad=(I(right)-I(left))/2
    shift=iv.mpf([-rad.b,rad.b]);dc=c[:];coef=[];fact=1
    for k in range(len(c)):
        if k:fact*=k
        coef.append(horner(dc,mid)/fact);dc=deriv(dc)
    return horner(coef,shift)

# Exact declared angle and speed, not rounded component substitution.
W=[-I(21)*I(1852)/3600*iv.cos((I(70)-I(799)/6)*iv.pi/180),
   -I(21)*I(1852)/3600*iv.sin((I(70)-I(799)/6)*iv.pi/180),Z]

def velocity(z,track):
    gam=-I('3.1')*iv.pi/180;chi=I(track)*iv.pi/180
    V=I(153)*I(1852)/3600*iv.exp(I(z)/17000)
    d=[iv.cos(chi),iv.sin(chi)];wd=dot(W[:2],d)
    gs=wd+iv.sqrt((V*iv.cos(gam))**2-dot(W[:2],W[:2])+wd**2)
    return [gs*d[0],gs*d[1],V*iv.sin(gam)]

def coefficients(q):
    v0=velocity(140,-47);vg=velocity('15.24',0)
    bump=[0,0,0,64,-192,192,-64,0];odd=[0,0,0,-64,320,-576,448,-128]
    phases=[]
    for idx,(p0,p1,w0,w1,T) in enumerate([
        ([-2500,1000,140],[0,0,'15.24'],v0,vg,q[0]),
        ([0,0,'15.24'],[q[2],0,0],vg,[q[3],Z,-I('.7')],q[1])]):
        cs=[]
        for j in range(3):
            start=p0[j] if hasattr(p0[j],'a') else I(p0[j]);end=p1[j] if hasattr(p1[j],'a') else I(p1[j])
            c0=start;c1=T*w0[j];A=end-c0-c1;B=T*w1[j]-c1;C=-2*Z
            c=[c0,c1,Z,10*A-4*B+C/2,-15*A+7*B-C,6*A-3*B+C/2,Z,Z]
            even=q[4+2*j] if idx==0 else (q[10] if j==0 else q[11] if j==2 else Z)
            oddamp=q[5+2*j] if idx==0 else Z
            c=[x+even*b+oddamp*o for x,b,o in zip(c,bump,odd)]
            cs.append(c)
        phases.append(cs)
    return phases

def enclose(cs,T,left,right,phase,reference,kinematics=None):
    r,v,a,j=kinematics if kinematics is not None else [[poly(deriv(c,k),left,right)/T**k for c in cs] for k in range(4)]
    va=[x-w for x,w in zip(v,W)]
    V=norm(va);H=norm(va[:2]);et=[x/V for x in va];er=[-va[1]/H,va[0]/H,Z];eu=cross(et,er)
    mass=I('238461.67357166');g=I('9.80665')
    F=[mass*(x+(g if k==2 else Z)) for k,x in enumerate(a)];Fd=[mass*x for x in j]
    lu,lr=dot(F,eu),dot(F,er);L=norm([lu,lr])
    vd=dot(et,a);etd=[(x-y*vd)/V for x,y in zip(a,et)]
    psid=(va[0]*a[1]-va[1]*a[0])/(H*H);erd=[-psid*va[0]/H,-psid*va[1]/H,Z]
    eud=[x+y for x,y in zip(cross(etd,er),cross(et,erd))]
    lud=dot(Fd,eu)+dot(F,eud);lrd=dot(Fd,er)+dot(F,erd)
    roll=(lu*lrd-lr*lud)/(L*L);ld=(lu*lud+lr*lrd)/L
    Q=I('.5')*I('1.225')*iv.exp(-r[2]/8500)*V*V*I('541.2');cl=L/Q
    qd=Q*(-v[2]/8500+2*vd/V);cld=ld/Q-cl*qd/Q
    drag=Q*(I('.08')+I('.045')*cl*cl)
    dd=qd*(I('.08')+I('.045')*cl*cl)+2*Q*I('.045')*cl*cld
    thrust=drag+dot(F,et);slew=dd+dot(Fd,et)+dot(F,etd)
    eas=V*iv.exp(-r[2]/17000)/(I(1852)/3600)
    m={}
    for key,x,l,h in [('eas',eas,I(135),I(175)),('cl',cl,Z,I('2.8')),('load',L/(mass*g),I('.5'),I('1.4')),('thrust',thrust,Z,I(700000))]:
        m[key+'_lower']=(x-l)/(h-l);m[key+'_upper']=(h-x)/(h-l)
    m['bank']=1-abs(safe_atan2(lr,lu))/(I(25)*iv.pi/180)
    m['roll']=1-abs(roll)/(I(5)*iv.pi/180)
    m['slew']=1-abs(slew)/100000
    m['descent']=1+safe_atan2(va[2],H)/(I(6)*iv.pi/180)
    if phase==0:m['approach_sink']=1+v[2]/8
    # One fixed reference point provides an upper bound on nearest distance.
    midpoint=np.array([(lo(x)+hi(x))/2 for x in r]);index=reference.query(midpoint)[1]
    point=reference.data[index]
    # float repr denotes the exact stored point-cloud coordinate, not a new curve.
    point_iv=[iv.mpf(float(x)) for x in point]
    m['corridor']=1-norm([x-y for x,y in zip(r,point_iv)])/400
    # Flare contact is structural. Factor z(s)=(1-s)g(s), with the exact
    # algebraic endpoint equality supplied by Hermite/bump construction.
    if phase==1:
        gcoef=[];cumulative=Z
        for c in cs[2][:-1]:
            cumulative+=c;gcoef.append(cumulative)
        height_factor=poly(gcoef,left,right)
        ground_ok=positive(height_factor)
    else:ground_ok=positive(r[2])
    return m,ground_ok and positive(v[0]) and bool(lu.a>0),{'V':lo(V),'horizontal_speed':lo(H),'lift':lo(L),'lift_up':lo(lu)}

def validate_certificate_arguments(q_strings,eta_string,maxdepth):
    if not isinstance(q_strings,(list,tuple)) or len(q_strings)!=12:raise ValueError('certificate requires exactly 12 decisions')
    def decimal_scalar(x):
        if not isinstance(x,str):raise ValueError('certificate inputs must be real-decimal strings')
        try:d=Decimal(x)
        except InvalidOperation as exc:raise ValueError('malformed real-decimal input') from exc
        if not d.is_finite():raise ValueError('nonfinite certificate input')
        return d
    for x in q_strings:decimal_scalar(x)
    eta=decimal_scalar(eta_string)
    if eta<0 or eta>=1:raise ValueError('eta outside certificate range [0,1)')
    if isinstance(maxdepth,bool) or not isinstance(maxdepth,int) or not 0<=maxdepth<=30:raise ValueError('invalid maxdepth')

def certify(q_strings,eta_string='0.039',maxdepth=22):
    from calculate import check_sources
    check_sources()
    cfg=tr.load_config()
    expected=ROOT/'model/config.json'
    # Bind every physical/domain constant and the exact reference implementation.
    if hashlib.sha256(expected.read_bytes()).hexdigest()!=CONFIG_HASH:raise ValueError('configuration changed')
    if hashlib.sha256((ROOT/'model/trajectory.py').read_bytes()).hexdigest()!=SOURCE_HASH:raise ValueError('reference definition changed')
    validate_certificate_arguments(q_strings,eta_string,maxdepth)
    q=[I(x) for x in q_strings];eta=I(eta_string);cs=coefficients(q);ev=tr.Evaluator(cfg)
    for x,(l,h) in zip(q,tr.BOUNDS):
        if not (x.a>=l and x.b<=h):raise ValueError('candidate outside box')
    stop=q[2]+2*q[3]+q[3]**2/(2*I('1.4709975'))
    terminal={'touchdown_x_lower':(q[2]-200)/500,'touchdown_x_upper':(700-q[2])/500,
        'touchdown_sink_lower':I('.7')/I('1.5'),'touchdown_sink_upper':I('.8')/I('1.5'),
        'touchdown_lateral':I(1),'touchdown_track':I(1),'touchdown_bank':I(1),'stop':(2636-stop)/2636}
    if not all(x.a>=eta.b for x in terminal.values()):
        raise ValueError('terminal margin below requested certificate eta')
    minima={k:lo(x) for k,x in terminal.items()};accepted=[];processed=0
    lower_domain={'V':1e100,'horizontal_speed':1e100,'lift':1e100,'lift_up':1e100}
    start=time.monotonic()
    for phase in range(2):
        stack=[(0.,1.,0)]
        while stack:
            left,right,depth=stack.pop();processed+=1
            try:
                m,hard,dom=enclose(cs[phase],q[phase],left,right,phase,ev.reference_tree)
                ok=hard and all(x.a>=eta.b for x in m.values())
            except (ValueError,ZeroDivisionError):ok=False
            if ok:
                accepted.append([phase,left,right,depth])
                for k,x in m.items():minima[k]=min(minima.get(k,1e100),lo(x))
                for k,x in dom.items():lower_domain[k]=min(lower_domain[k],x)
            elif depth>=maxdepth:
                return dict(certified=False,unresolved=[phase,left,right,depth],processed=processed)
            else:
                mid=(left+right)/2;stack.extend([(mid,right,depth+1),(left,mid,depth+1)])
    return dict(certified=True,eta_lower_real_decimal=eta_string,q_real_decimal=q_strings,
        interval_precision_digits=iv.dps,accepted_intervals=len(accepted),processed=processed,
        maximum_depth=max(x[3] for x in accepted),margin_lower_enclosures_display_only=minima,
        nonsingular_domain_lower_display_only=lower_domain,cover=accepted,
        stop_enclosure_display=[lo(stop),hi(stop)],seconds=time.monotonic()-start,
        config_sha256=CONFIG_HASH,trajectory_source_sha256=SOURCE_HASH,
        reference_point_cloud_sha256=hashlib.sha256(ev.reference_tree.data.tobytes()).hexdigest(),
        reference_point_cloud_shape=list(ev.reference_tree.data.shape),
        domain='declared constant-wind real-decimal polynomial-family model, exact analytic rates; frozen zero-wind reference cloud',
        proof='outward-rounded interval inequalities cover both closed phases; structural endpoint identities; exact ground rule',
        global_optimality=False)

CONFIG_HASH='2165902413c100923ec27e07d7ba9ef1aba62a5e1850cec84e83b8bc2d322693'
SOURCE_HASH='9b557ce07c7e8f177b0b3cfac1765c1c9aec4997e28b52d3185ad533f7cf3f6a'

if __name__=='__main__':
    from calculate import OUT,write,current_selection
    selection=current_selection()
    selected=selection['selected']
    q=[repr(x) for x in selected['q']]
    target=max(0.,selected['sampled_exact_eta']-.002)
    result=certify(q,repr(target))
    result.update(run_id=selection['run_id'],wind_speed_kt=21,wind_from_true_deg=70,runway_true_deg_exact='799/6',historical_clearance=False,physical_prediction_interval=None)
    result['checker_source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['calculator_source_sha256']=hashlib.sha256((OUT/'calculate.py').read_bytes()).hexdigest()
    result['inputs_sha256']=hashlib.sha256((OUT/'inputs.json').read_bytes()).hexdigest()
    write('continuous_check.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='cover'},indent=2))
