"""Certified vertical-speed regularity and stronger family-wide upper bound."""
import json
from pathlib import Path
from mpmath import iv
from certify_candidate import I,Z,deriv,poly,velocity,lo,hi

def vertical_bound():
    # Exact Hermite basis, with interval parameter ranges covering the full box.
    P1=deriv([I(x) for x in [0,0,0,10,-15,6]])
    V0=deriv([I(x) for x in [0,1,0,-6,8,-3]])
    V1=deriv([I(x) for x in [0,0,0,-4,7,-3]])
    B=deriv([I(x) for x in [0,0,0,64,-192,192,-64]])
    O=deriv([I(x) for x in [0,0,0,-64,320,-576,448,-128]])
    cases=[(0,iv.mpf([30,55]),I('-124.76'),iv.mpf([-50,50]),iv.mpf([-50,50]),velocity(140,-47)[2],velocity('15.24',0)[2]),
           (1,iv.mpf([4,12]),I('-15.24'),iv.mpf([-10,10]),Z,velocity('15.24',0)[2],-I('.7'))]
    records=[]
    for phase,T,delta,a,b,v0,v1 in cases:
        maximum=0
        for k in range(128):
            l=k/128;r=(k+1)/128
            v=delta/T*poly(P1,l,r)+v0*poly(V0,l,r)+v1*poly(V1,l,r)+a/T*poly(B,l,r)+b/T*poly(O,l,r)
            assert v.a > -14 and v.b < 14
            maximum=max(maximum,abs(lo(v)),abs(hi(v)))
        records.append(dict(phase=phase,cover_intervals=128,max_abs_display=maximum))
    # V>=135 knots because h>=0. Global nonsingularity bound independent of q.
    horizontal_sq=(I(135)*I(1852)/3600)**2-I(14)**2
    assert horizontal_sq.a>I(68)**2
    return dict(certified_abs_vertical_speed_lt_mps=14,records=records,
                certified_horizontal_speed_gt_mps=68,domain='entire parameter box, nominal zero wind, airborne h>=0 and EAS>=135')

def stronger_bound():
    # In flare y=0; at eta>=0, descent >= -(1-eta)6 degrees.
    # If v_z<=0 then v_x >= V*cos((1-eta)6deg).
    # If v_z>0, use polynomial-family |v_z|<14 (not a flight-envelope assumption).
    # Both branches admit v_x>=sqrt([k(135+40eta)]^2-14^2).
    # Tf>=4 therefore xTD>=4*sqrt(...); this improves xTD>=200+500eta.
    k=I(1852)/3600;dec=I('1.4709975')
    def F(e):
        E=k*(135+40*e);u=iv.sqrt(E**2-I('.7')**2)
        horizontal=iv.sqrt(E**2-I(14)**2)
        return 4*horizontal+2*u+u**2/(2*dec)-2636*(1-e)
    # Simple rational-decimal bracket, proved by interval signs.
    left=0;right=1600000;den=10000000
    assert F(I(left)/den).b<0 and F(I(right)/den).a>0
    while right-left>1:
        mid=(left+right)//2;x=F(I(mid)/den)
        if x.b<0:left=mid
        elif x.a>0:right=mid
        else:raise ArithmeticError('unresolved interval sign')
    return dict(lower_numerator=left,upper_numerator=right,denominator=den,
                upper_display=right/den,lower_F_upper_display=hi(F(I(left)/den)),
                upper_F_lower_display=lo(F(I(right)/den)),
                domain='continuous polynomial family only; Tf>=4 and proved |vz|<14; unchanged nominal ground rule',
                attained=False)

if __name__=='__main__':
    result=dict(vertical_speed=vertical_bound(),family_upper_bound=stronger_bound())
    Path(__file__).with_name('existence_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
