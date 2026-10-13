from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from certify import *
from analysis_tools import replay
HERE=Path(__file__).resolve().parent

def primary_upper(c,q):
 m,h,e,ps=c.evaluate(q,10001,True)
 # Select a point then enclose that one constraint. It is an upper bound on
 # the all-time minimum, not a lower bound or an optimum estimate.
 key=min(m,key=lambda k:np.min(m[k]));i=int(np.argmin(m[key]));qs=[I(repr(float(x))) for x in q]
 if key=='stop':v=(2636-qs[2]-2*qs[3]-qs[3]**2/(2*I('1.4709975')))/2636;where='terminal'
 elif key in ['touchdown_x_lower','touchdown_x_upper']:
  v=(qs[2]-200)/500 if key.endswith('lower') else (700-qs[2])/500;where='terminal'
 else:
  ph=i//10001 if key!='approach_sink' else 0;j=i%10001;s=j/10000
  cs,W=coeff(qs,c.p['wind_mps']);ic.W=W;mi,ha,dom=ic.enclose(cs[ph],qs[ph],s,s,0,TREE)
  v=mi[key];where=[ph,repr(s)]
 up=float(np.nextafter(float(v.b),np.inf));return up,dict(constraint=key,point=where,upper_real_decimal=repr(up),method='upper interval endpoint at a selected time, rounded toward plus infinity')

if __name__=='__main__':
 for path in sorted((OUT/'cases').glob('*/result.json')):
  old=json.loads(path.read_text());p=old['condition'];c=Case(p['name'],p['wind_mps'],p['urban'],p['roof_delta'],p['frame_dx'],p['frame_dy'],p['runway_level'],p['buffer']);upper,where=primary_upper(c,old['primary']['q'])
  # Round target upward to ensure the certificate implies retention <=1e-4.
  from decimal import Decimal
  eta=str(Decimal(repr(upper))-Decimal('.0001'))
  proof=bind(certify_case(c,old['selected']['q'],eta,maxdepth=22));proof['primary_upper']=where;proof['retention_budget_real_decimal']='0.0001';proof['result_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();proof['proof_source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
  (HERE/('retention_'+c.name+'.json')).write_text(json.dumps(proof,indent=2)+'\n');print(c.name,eta,proof.get('certified'),proof.get('processed'),proof.get('seconds'),proof.get('unresolved'),flush=True)
