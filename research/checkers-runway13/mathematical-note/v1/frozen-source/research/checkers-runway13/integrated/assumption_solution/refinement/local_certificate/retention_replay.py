from validate import *
from certify import certify_case,bind
from analysis_tools import replay
from decimal import Decimal,localcontext

def run():
 check_preserved();receipt=json.loads((HERE/'certificate.json').read_text());r=receipt['root']
 assert r['certified']and receipt['simplex']['certified']and receipt['path']['certified']
 with localcontext() as ctx:
  ctx.prec=65
  upper=str(Decimal(r['center'][5])+Decimal(r['radius']))
  target=str(Decimal(upper)-Decimal('.0001'))
 c=Case();old=json.loads((HERE.parent.parent/'cases/mean/result.json').read_text())
 proof=bind(certify_case(c,old['selected']['q'],target,maxdepth=24))
 q=BASE['q'].copy()
 for k,i in enumerate([1,2,3,10,11]):q[i]=float(r['center'][k])*SCALE[k]
 result=dict(secondary_retention=proof,retention_budget='.0001',primary_upper_real_decimal=upper,unchanged_secondary_source='integrated/assumption_solution/cases/mean/result.json',root_center_replay=replay(c,q),replay_q=q,replay_is_numerical_center_not_exact_root=True,secondary_global_optimum=False)
 (HERE/'retention_replay.json').write_text(json.dumps(result,indent=2)+'\n');print('retention',proof['certified'],'processed',proof.get('processed'),'replay',result['root_center_replay'],flush=True)
if __name__=='__main__':run()
