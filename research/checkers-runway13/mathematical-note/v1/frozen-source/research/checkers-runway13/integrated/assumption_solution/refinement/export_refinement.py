from pathlib import Path
import sys,json,csv
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from conditional_model import *
HERE=Path(__file__).resolve().parent

def evaluate(name,t,side='right'):
 r=json.loads((HERE/(name+'_verified.json')).read_text());p=r['condition'];c=Case(p['name'],p['wind_mps'],p['urban'],p['roof_delta'],p['frame_dx'],p['frame_dy'],p['runway_level'],p['buffer']);q=r['selected']['q'];td=q[0]+q[1];end=td+2+q[3]/1.4709975
 if not np.isfinite(t) or not 0<=t<=end or side not in ['left','right']:raise ValueError('time/side domain')
 if t<td or (t==td and side=='left'):
  ph=0 if t<q[0] else 1;s=(t-(q[0]if ph else 0))/q[ph];d=phase(c.curves(q)[ph],q[ph],np.array([s]),c.p)
  return dict(time_s=t,phase='approach'if ph==0 else'flare',position_cg_m=d['pos'][0].tolist(),velocity_mps=d['vel'][0].tolist(),bank_deg=float(np.rad2deg(d['bank'][0])),roll_deg_s=float(np.rad2deg(d['roll'][0])),CL=float(d['cl'][0]),thrust_N=float(d['thrust'][0]),thrust_slew_N_s=float(d['slew'][0]))
 u=t-td;b=max(0,u-2);x=q[2]+q[3]*min(u,2)+q[3]*b-.5*1.4709975*b*b
 return dict(time_s=t,phase='ground',position_cg_m=[x,0,6],velocity_mps=[max(0,q[3]-1.4709975*b),0,0],bank_deg=0,roll_deg_s=0,CL=None,thrust_N=None,thrust_slew_N_s=None)

def export():
 rows=[]
 for name in ['tailwind3','urban58']:
  r=json.loads((HERE/(name+'_verified.json')).read_text());p=r['condition'];c=Case(p['name'],p['wind_mps'],p['urban'],p['roof_delta'],p['frame_dx'],p['frame_dy'],p['runway_level'],p['buffer']);q=r['selected']['q'];td=q[0]+q[1];end=td+2+q[3]/1.4709975;stop=q[2]+2*q[3]+q[3]**2/(2*1.4709975)
  row=dict(name=name,certified_eta=r['continuous']['eta_lower_real_decimal'],touchdown_x_m=q[2],stop_x_m=stop,runway_remaining_m=2786-stop,effort=r['selected']['effort'],secondary_local_complete=r['secondary_complete']);rows.append(row)
  formula=dict(condition=p,q_real_decimal=[repr(float(v))for v in q],expanded_cg_polynomial_coefficients=[[a.coef.tolist()for a in pp]for pp in c.curves(q)],ground=dict(touchdown_s=td,delay_s=2,deceleration_mps2=1.4709975,stop_s=end),interpretation='conditional numerical path, not a global optimum; real-decimal Hermite construction is authoritative')
  (HERE/(name+'_formula.json')).write_text(json.dumps(formula,indent=2)+'\n')
  times=np.unique(np.r_[np.linspace(0,q[0],301),np.linspace(q[0],td,301),np.linspace(td,end,201)])
  with (HERE/(name+'_path_controls.csv')).open('w',newline='')as f:
   w=csv.writer(f);w.writerow(['t_s','phase','cg_x_m','cg_y_m','cg_z_m','vx_mps','vy_mps','vz_mps','bank_deg','roll_deg_s','CL','thrust_N','thrust_slew_N_s'])
   for t in times:
    d=evaluate(name,float(t));w.writerow([t,d['phase'],*d['position_cg_m'],*d['velocity_mps'],*[d[k]for k in ['bank_deg','roll_deg_s','CL','thrust_N','thrust_slew_N_s']]])
 (HERE/'new_conditions.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--case',choices=['tailwind3','urban58']);p.add_argument('--time',type=float);p.add_argument('--side',default='right',choices=['left','right']);a=p.parse_args()
 if a.case:print(json.dumps(evaluate(a.case,a.time,a.side),indent=2))
 else:export()
