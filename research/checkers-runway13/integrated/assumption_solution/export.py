from conditional_model import *
from analysis_tools import replay,terminal_interval_bound,fixed_gate
from analytical.verify_full_landing_analysis import analytic
import csv,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def make_case(p):return Case(p['name'],p['wind_mps'],p['urban'],p['roof_delta'],p['frame_dx'],p['frame_dy'],p['runway_level'],p['buffer'])

def export_one(path):
 result=json.loads(path.read_text());case=make_case(result['condition']);q=result['selected']['q'];cs=case.curves(q)
 certpath=path.parent/'continuous.json';cert=json.loads(certpath.read_text())
 if not cert.get('certified'):raise ValueError('uncertified candidate '+case.name)
 if cert.get('result_sha256')!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('stale certificate '+case.name)
 for name,h in cert['source_sha256'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('stale proof source '+name)
 m,hard,e,ps=case.evaluate(q,10001,True);eta=min(map(np.min,m.values()));hm=min(map(np.min,hard.values()))
 if eta<=0 or hm<-1e-8:raise ValueError('dense verification failed')
 rep=replay(case,q)
 if not rep['passed']:raise ValueError('replay failed')
 primary_eta=min(map(np.min,case.evaluate(result['primary']['q'],10001)[0].values()))
 retention=bool(result['secondary_complete'] and primary_eta-eta<=1e-4)
 tD=q[0]+q[1];stop=q[2]+2*q[3]+q[3]**2/(2*1.4709975);stopT=tD+2+q[3]/1.4709975
 bounds=terminal_interval_bound(case);cl=float(cert['eta_lower_real_decimal']);upper=bounds['family']['upper_display']
 energy=json.loads((path.parent/'energy_bound.json').read_text())
 if energy.get('condition')!=case.parameters():raise ValueError('energy condition mismatch')
 for pn,hh in energy['source_sha256'].items():
  if hashlib.sha256((ROOT/pn).read_bytes()).hexdigest()!=hh:raise ValueError('stale energy bound')
 if energy.get('exclusion',{}).get('excluded'):upper=min(upper,float(energy['exclusion']['eta_upper_real_decimal']))
 gaps=case.geometry({k:np.concatenate([p[k] for p in ps]) for k in ps[0]})
 obstacle_mins={k:float(np.min(v)) for k,v in gaps.items() if k.startswith(('urban','object'))};lim=min(obstacle_mins,key=obstacle_mins.get)
 row=dict(name=case.name,status='continuous_conditional_feasible',numerical_eta=float(eta),certified_eta=cl,global_family_eta_upper=upper,global_full_eta_upper=bounds['full']['upper_display'],family_gap_upper=upper-cl,secondary_local_complete=retention,
 touchdown_s=tD,touchdown_x_m=q[2],touchdown_speed_kt=q[3]/tr.KT,stop_s=stopT,stop_x_m=stop,runway_remaining_m=2786-stop,effort=float(e),limiting_assumed_geometry=lim,minimum_sampled_obstacle_separation_m=obstacle_mins[lim],max_bank_deg=float(max(np.max(abs(p['bank'])) for p in ps)*180/np.pi),historical_certified=False)
 formula=dict(interpretation='Explicit path after numerical parameter selection, NOT a closed-form optimum map',condition=case.parameters(),q=q,construction='DERIVATION section1; exact real-decimal q and wind are authoritative, expanded floats are evaluation conveniences',phases=[dict(name=name,duration_s=q[i],t0_s=0 if i==0 else q[0],cg_coefficients_xyz_m=[p.coef.tolist() for p in cs[i]]) for i,name in enumerate(['approach','flare'])],ground=dict(tD_s=tD,xD_m=q[2],U_mps=q[3],delay_s=2,a_mps2=1.4709975,zCG_m=6,stop_s=stopT,stop_x_m=stop),historical_certified=False)
 (path.parent/'formula.json').write_text(json.dumps(formula,indent=2)+'\n')
 receipt=dict(metrics=row,independent_replay=rep,terminal_global_bounds=bounds,energy_family_bound=energy,primary_dense_eta=float(primary_eta),secondary_loss=float(primary_eta-eta),secondary_local_retention_passed=retention,geometry_minima_sampled_m={k:float(np.min(v))for k,v in hard.items()},operating_minima_sampled={k:float(np.min(v))for k,v in m.items()},result_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),certificate_sha256=hashlib.sha256(certpath.read_bytes()).hexdigest(),hist_certified=False)
 (path.parent/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
 with (path.parent/'path_controls.csv').open('w',newline='') as f:
  wr=csv.writer(f);wr.writerow(['t_s','phase','x_m','y_m','cg_z_m','vx_mps','vy_mps','vz_mps','bank_deg','roll_deg_s','CL','thrust_N','thrust_slew_N_s'])
  for i,(p,T) in enumerate(zip(ps,q[:2])):
   for k in range(0,10001,10):wr.writerow([k/10000*T+(q[0]if i else 0),'approach'if i==0 else'flare',*p['pos'][k],*p['vel'][k],np.rad2deg(p['bank'][k]),np.rad2deg(p['roll'][k]),p['cl'][k],p['thrust'][k],p['slew'][k]])
  for t in np.linspace(0,2+q[3]/1.4709975,401):
   s=max(0,t-2);x=q[2]+q[3]*min(t,2)+q[3]*s-.5*1.4709975*s*s;v=max(0,q[3]-1.4709975*s)
   wr.writerow([tD+t,'ground',x,0,6,v,0,0,0,0,'','',''])
 return row,case,ps

if __name__=='__main__':
 rows=[];data={}
 for path in sorted((OUT/'cases').glob('*/state.json')):
  if (path.parent/'result.json').exists():
   row,c,ps=export_one(path.parent/'result.json');rows.append(row);data[c.name]=(c,ps);print(c.name,row['certified_eta'],row['secondary_local_complete'],flush=True)
  else:
   state=json.loads(path.read_text());case=make_case(state['condition']);gate=fixed_gate(case)
   row=dict(name=case.name,status='conditionally_excluded_by_fixed_gate'if not gate['feasible_under_imposed_gate_constraints'] else'positive_margin_not_found_not_proved_infeasible',fixed_gate=gate,historical_certified=False);rows.append(row)
 (OUT/'conditions.json').write_text(json.dumps(rows,indent=2)+'\n')
 keys=['name','status','numerical_eta','certified_eta','global_family_eta_upper','family_gap_upper','secondary_local_complete','touchdown_x_m','touchdown_speed_kt','stop_x_m','runway_remaining_m','effort']
 with (OUT/'conditions.csv').open('w',newline='')as f:
  wr=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');wr.writeheader();wr.writerows(rows)
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
 fig,axs=plt.subplots(1,3,figsize=(15,4.5));cols={'mean':'#476a70','urban55':'#a26648','calm':'#6d795c'}
 for name,color in cols.items():
  if name not in data:continue
  case,ps=data[name];d={k:np.concatenate([p[k]for p in ps])for k in ps[0]};p=d['pos'];bank=d['bank'];low=p[:,2]-np.maximum(4*np.cos(bank)+32.7*abs(np.sin(bank)),6*np.cos(bank)+6.0579*abs(np.sin(bank)))
  axs[0].plot(p[:,0],p[:,1],color=color,label=name)
  axs[1].plot(p[:,0],low-3,color=color,label=name+' lowest point −3m')
 for ob in SCENE['obstacles']:
  x,y,u,v=ob['bounds_xy'];axs[0].add_patch(Rectangle((x,y),u-x,v-y,fc='#999999',ec='none',alpha=.18))
 axs[0].plot([0,2786],[0,0],color='black',lw=3);axs[0].set(xlim=(-2800,500),ylim=(-950,1200),xlabel='Along runway (m)',ylabel='Right of runway (m)',title='Assumed frame: paths and source footprints');axs[0].legend();axs[0].set_aspect('equal',adjustable='box')
 axs[1].plot([-900,-540],[55,55],color=cols['urban55'],ls=':',label='55m blanket');axs[1].plot([-900,-540],[25,25],color=cols['mean'],ls=':');axs[1].set(xlim=(-900,-400),ylim=(20,90),xlabel='Along runway (m)',ylabel='Supported lower height (m)',title='Tall assumed urban envelope changes the path');axs[1].legend(fontsize=8)
 success=[r for r in rows if 'certified_eta'in r];idx=np.arange(len(success));axs[2].hlines(idx,[r['certified_eta']for r in success],[r['global_family_eta_upper']for r in success],color='#b4b6b2');axs[2].scatter([r['certified_eta']for r in success],idx,c='#476a70',label='Certified candidate');axs[2].scatter([r['global_family_eta_upper']for r in success],idx,marker='|',s=70,c='#a26648',label='Family global upper bound');axs[2].set_yticks(idx,[r['name']for r in success]);axs[2].set(xlabel='Normalized primary margin',title='Optimality gap remains open');axs[2].legend(fontsize=8)
 fig.suptitle('Conditional assumed-airport model • not historical clearance or an optimality certificate',fontsize=12);fig.tight_layout();fig.savefig(OUT/'conditional_landings.png',dpi=160);fig.savefig(OUT/'conditional_landings.pdf');plt.close(fig)
