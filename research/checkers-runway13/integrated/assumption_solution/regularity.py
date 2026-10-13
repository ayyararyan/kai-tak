from conditional_model import *
from integrated.clearance import polynomial_range
from fractions import Fraction as F
H=Poly([0,0,0,10,-15,6]);A=Poly([0,1,0,-6,8,-3]);B=Poly([0,0,0,-4,7,-3]);b=64*Poly([0,0,0,1,-3,3,-1]);o=b*Poly([-1,2])
bounds={}
for name,p in [('H',H),('A',A),('B',B),('b',b),('o',o)]:
 # Exact rational dyadic cell endpoints via terminating decimal strings.
 bounds[name]=max(max(abs(x) for x in polynomial_range(p.deriv().coef.tolist(),i/128,(i+1)/128)) for i in range(128))
approach=F('124.76')/30*bounds['H']+5*(bounds['A']+bounds['B'])+F(50,30)*(bounds['b']+bounds['o'])
flare=F('15.24')/4*bounds['H']+5*bounds['A']+F('.7')*bounds['B']+F(10,4)*bounds['b']
# Endpoint vertical speeds are <5m/s at146 and21.24m for fixed153EAS,-3.1deg.
result=dict(derivative_abs_upper_exact={k:str(v) for k,v in bounds.items()},endpoint_vertical_abs_upper_assumed_bound=5,approach_vertical_abs_upper_exact=str(approach),flare_vertical_abs_upper_exact=str(flare),approach_display=float(approach),flare_display=float(flare),both_below_135kt=bool(max(approach,flare)<F(135*1852,3600)),scope='all q in frozen12-parameterbox, constant horizontalwinds at selected endpoints; exact rational polynomial shape bounds')
(OUT/'regularity.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
