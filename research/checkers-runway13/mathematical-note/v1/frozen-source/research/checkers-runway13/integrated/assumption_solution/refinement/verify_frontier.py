from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from certify import *
from analysis_tools import replay
from retention_proof import primary_upper
from decimal import Decimal
HERE=Path(__file__).resolve().parent
for typ,name,val in [('wind','tailwind3',3),('urban','urban58',58)]:
 r=next(r for r in json.loads((HERE/('continuation_'+typ+'.json')).read_text()) if r['condition']['name']==name)
 c=Case(name,urban=val)if typ=='urban'else Case(name,wind=(val*tr.KT,0,0))
 upper,where=primary_upper(c,r['q']);sec=c.solve(np.array(r['q']),1201,True,upper-5e-5,maxiter=700)
 selected=sec if sec['success'] and sec['hard_min']>=-1e-8 and sec['eta']>=upper-1e-4 else r
 eta=str(Decimal(repr(upper))-Decimal('.0001'))
 proof=bind(certify_case(c,selected['q'],eta,maxdepth=22));proof['primary_upper']=where;proof['retention_budget']='0.0001'
 result=dict(condition=c.parameters(),primary=r,secondary=sec,selected=selected,secondary_complete=selected is sec,continuous=proof,replay=replay(c,selected['q']),historical_certified=False,global_optimum=False)
 (HERE/(name+'_verified.json')).write_text(json.dumps(result,indent=2)+'\n');print(name,sec['success'],sec['eta'],proof.get('certified'),proof.get('processed'),result['replay']['passed'],flush=True)
