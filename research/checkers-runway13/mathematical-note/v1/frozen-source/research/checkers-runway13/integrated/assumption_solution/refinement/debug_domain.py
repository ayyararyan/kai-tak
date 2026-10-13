from pathlib import Path
import json
from box_certifier import *
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'active_branch.json').read_text())['baseline'];q=r['q'];dq=[0.]*12
for i,v in zip([1,2,3,10,11],r['dq_dwx']):dq[i]=v
from parameter_taylor import *
import box_certifier as bc
for radius in ['0','.00001','.01']:
 bc.parameter_kin=prepare(q,dq,Case(),radius)
 c=Case();ds=iv.mpf([-I(radius).b,I(radius).b]);c.p['wind_mps']=[I(repr(c.p['wind_mps'][0]))+ds,I(repr(c.p['wind_mps'][1])),I(0)];qs=[I(repr(v))+I(repr(d))*ds for v,d in zip(q,dq)];cs,W=coeff(qs,c.p['wind_mps']);ic.W=W
 geo,kin=bc.geometry_cell(c,cs[1],qs[1],0,1/262144,1);m,h,dom=ic.enclose(cs[1],qs[1],0,1/262144,0,TREE,kinematics=kin);m.pop('approach_sink')
 print(radius,'m',[(k,float(v.a),float(v.b))for k,v in m.items()if v.a<.149], 'geo',[(k,float(v.a))for k,v in geo.items()if v.a<0], 'hard',h)
