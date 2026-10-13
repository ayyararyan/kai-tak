from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from conditional_model import *
r=json.loads((OUT/'cases/mean/result.json').read_text());q=r['primary']['q']; c=Case();m,h,e,ps=c.evaluate(q,20001,True)
for key in ['slew','load_upper','thrust_lower']:
 for ph,d in enumerate(ps):
  vals={'slew':1-abs(d['slew'])/1e5,'load_upper':(1.4-d['load'])/.9,'thrust_lower':d['thrust']/7e5}[key]
  from scipy.signal import find_peaks
  inds=list(find_peaks(-vals)[0])+[0,len(vals)-1]
  print(key,ph,[(i/20000,float(vals[i])) for i in inds])
print('bounds',q)
