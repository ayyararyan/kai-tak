"""Reproduce draft figures from frozen evidence; never run or modify the landing solver."""
from pathlib import Path
import csv
import hashlib
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'qa' / 'v2_reference_figures'
QA = ROOT / 'qa'
FIG.mkdir(exist_ok=True, parents=True)
QA.mkdir(exist_ok=True)
SLATE, SAGE, COPPER = '#354B55', '#687767', '#A46542'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelcolor': SLATE, 'text.color': SLATE,
                     'axes.edgecolor': '#87918F', 'pdf.fonttype': 42,
                     'savefig.facecolor': 'white'})
checks = {}
manifest = json.loads((ROOT / 'evidence_manifest.json').read_text())
for item in manifest['files']:
    if 'snapshot' in item:
        p = ROOT / item['snapshot']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256'], p
checks['snapshot_hashes'] = True

def save(fig, name):
    fig.savefig(FIG / f'{name}.pdf', bbox_inches='tight', metadata={'CreationDate': None})
    fig.savefig(FIG / f'{name}.png', bbox_inches='tight', dpi=160)
    plt.close(fig)

formula = json.loads((ROOT/'evidence/approximation/reference_formula.json').read_text())
out = json.loads((ROOT/'evidence/approximation/reference_outcomes.json').read_text())
assert out['scene_id'] == 'synthetic-v1-empty-obstacles-fixed-certified-witness'
assert out['uncertainty']['prediction_intervals'] is None
assert out['optimality']['globally_near_optimal'] is False
p = formula['scalar_inputs']
xD, u, delay, decel, length = (p[k] for k in ['touchdown_x_m', 'touchdown_speed_mps',
                            'brake_delay_s', 'brake_deceleration_mps2', 'runway_length_m'])
stop = xD + u*delay + u*u/(2*decel)
assert math.isclose(stop, out['nominal']['total_runway_consumed_m'], abs_tol=1e-9)
assert math.isclose(length-stop, out['nominal']['runway_remaining_m'], abs_tol=1e-9)
assert math.isclose(p['approach_s']+p['flare_s']+delay+u/decel,
                    out['nominal']['entry_to_stop_s'], abs_tol=1e-10)
checks['scalar_outcomes_recomputed'] = True
curves=[]
for phase in formula['phases']:
    s=np.linspace(0, 1, 801)
    c=np.array(phase['coefficients_xyz_m'])
    xyz=np.array([np.polynomial.polynomial.polyval(s, row) for row in c]).T
    time=phase['start_s']+phase['duration_s']*s
    curves.append((time,xyz))
assert np.max(abs(curves[0][1][-1]-curves[1][1][0])) < 1e-8
assert np.max(abs(curves[0][1][0]-[-2500,1000,140])) < 1e-9
assert np.max(abs(curves[1][1][-1]-[xD,0,0])) < 1e-8
checks['polynomial_endpoints'] = True
fig,axs=plt.subplots(2,1,figsize=(6.9,5.2),layout='constrained',gridspec_kw={'height_ratios':[1,1]})
for (_,xyz),col,name in zip(curves,[SLATE,COPPER],['Approach','Flare']):
    axs[0].plot(xyz[:,0],xyz[:,1],color=col,label=name,lw=2)
axs[0].plot([xD,stop],[0,0],color=SAGE,lw=2,label='Ground travel')
axs[0].plot([0,length],[0,0],color='#CBD0CC',lw=7,zorder=0)
axs[0].scatter([0,xD,stop],[0,0,0],s=18,color=[SLATE,COPPER,SAGE],zorder=5)
axs[0].set(xlabel='Runway-relative x (m)',ylabel='Lateral position y (m)',title='Synthetic geometry; no historical obstacles')
axs[0].legend(frameon=False,ncol=3,loc='upper right',fontsize=8)
for (time,xyz),col in zip(curves,[SLATE,COPPER]):
    axs[1].plot(time,xyz[:,2],color=col,lw=2)
axs[1].axvline(p['approach_s'],color='#87918F',ls=':',lw=1)
axs[1].set(xlabel='Time from synthetic entry (s)',ylabel='Height above runway (m)',title='Airborne height, including the permitted brief climb')
save(fig,'synthetic_trajectory')

speeds=np.linspace(69,88,350)
boundary=length-150-speeds*delay-speeds**2/(2*decel)
fig,ax=plt.subplots(figsize=(6.5,3.5),layout='constrained')
ax.fill_between(speeds,200,np.maximum(200,np.minimum(700,boundary)),where=boundary>=200,color=SAGE,alpha=.18)
ax.plot(speeds,boundary,color=SLATE,lw=2,label='Fixed-law reserve boundary')
ax.scatter([u],[xD],marker='*',s=120,color=COPPER,label='Synthetic candidate',zorder=4)
ax.axhline(200,color='#87918F',ls=':',lw=1)
ax.set(xlabel='Forward touchdown speed (m/s)',ylabel='Touchdown station xD (m)',ylim=(0,850),xlim=(69,88),title='Stopping inequality only; not flight feasibility')
ax.legend(frameon=False,fontsize=8,loc='upper right')
save(fig,'stopping_boundary')
checks['local_sensitivities']={'dR_du_m_per_mps':-delay-u/decel,'dR_dd_m_per_s':-u}

rows=list(csv.DictReader((ROOT/'evidence/weather_plot_data.csv').open()))
subset=[r for r in rows if r['report_type']=='FM-15' and r['source_flag']=='4'
        and r['datetime_utc'][14:19]=='00:00' and r['wind_type']=='N'
        and r['wind_speed_mps'] and r['wind_speed_mps_strict_qc_accepted']=='True'
        and r['partial_weather_row']=='False']
v=np.array([float(r['wind_speed_mps']) for r in subset])
assert len(rows)==8549 and len(v)==8360
assert ((v<10.8).sum(),(v==10.8).sum(),(v>10.8).sum())==(8285,17,58)
for hour,gust in [('03',17.5),('04',20.6)]:
    r=next(r for r in rows if r['datetime_utc']==f'1993-11-04T{hour}:00:00Z')
    assert float(r['wind_speed_mps'])==10.8 and float(r['gust_mps'])==gust
checks['weather_counts_and_event_values'] = True
fig,ax=plt.subplots(figsize=(6.5,3.3),layout='constrained')
sv=np.sort(v)
ax.step(sv,100*np.arange(1,len(v)+1)/len(v),where='post',color=SLATE,lw=1.8)
ax.axvline(10.8,color=COPPER,lw=1.5,ls='--')
ax.annotate('4 November, 03:00 and 04:00 UTC\n10.8 m/s mean wind',xy=(10.8,99.1),xytext=(6,49),
            arrowprops={'arrowstyle':'-','color':COPPER},fontsize=9,color=COPPER)
ax.set(xlabel='Reported station mean wind speed (m/s)',ylabel='Cumulative share of selected records (%)',ylim=(0,103),xlim=(0,max(v)+.3))
save(fig,'weather_context')

historical=json.loads((ROOT/'evidence/evidence/cal605_reconstruction/analysis.json').read_text())
for row in historical['fixed_formula']:
    speed=row['touchdown_speed_kt']*1852/3600
    calc=length-row['touchdown_x_m']-speed*row['delay_s']-speed**2/(2*row['deceleration_g']*9.80665)
    assert math.isclose(calc,row['remaining_m'],abs_tol=1e-8)
landmarks=historical['report_landmark_stopping_frontier']
for row in landmarks:
    speed=row['speed_kt']*1852/3600
    for lag,key in [(0,'required_decel_no_delay_g'),(2,'required_decel_with_2s_delay_g')]:
        calc=speed**2/(2*(row['remaining_m']-speed*lag))/9.80665
        assert math.isclose(calc,row[key],abs_tol=1e-12)
checks['historical_conditional_stopping_recomputed']=True
fig,axs=plt.subplots(1,2,figsize=(7,3.4),layout='constrained')
names=['Touchdown','Roll restored','Autobrake call','Reverse selected']
idx=np.arange(4)
axs[0].plot(idx,[r['speed_kt'] for r in landmarks],'-o',color=SLATE,lw=1.5,markersize=4)
axs[0].set(ylabel='Reported groundspeed (kt)',title='Speed decreases')
axs[1].plot(idx,[r['required_decel_no_delay_g'] for r in landmarks],'-o',color=COPPER,lw=1.5,markersize=4,label='No additional delay')
axs[1].plot(idx,[r['required_decel_with_2s_delay_g'] for r in landmarks],'--o',color=SAGE,lw=1.5,markersize=4,label='2 s additional delay')
axs[1].set(ylabel='Required constant deceleration (g)',title='Stopping requirement increases')
axs[1].legend(frameon=False,fontsize=7,loc='upper left')
for ax in axs:
    ax.set_xticks(idx,names,rotation=25,ha='right',fontsize=7)
save(fig,'historical_stopping')

st=list(csv.DictReader((ROOT/'evidence/stereo_plot_data.csv').open()))
e=np.array([float(r['easting_hk1980_m']) for r in st])-837500
n=np.array([float(r['northing_hk1980_m']) for r in st])-821000
z=np.array([float(r['z_above_fitted_local_park_road_plane_m']) for r in st])
inside=np.array([r['within_map_control_hull']=='True' for r in st])
assert len(st)==34262 and np.isfinite(np.column_stack([e,n,z])).all()
handoff=json.loads((ROOT/'evidence/reconstruction/block_matching/HANDOFF.json').read_text())
assert handoff['dense_points']==171307 and handoff['dense_points_inside_control_hull']==3780
assert handoff['surface_triangles']==225371 and handoff['clearance_certified'] is False
fig,axs=plt.subplots(1,2,figsize=(7,3.5),layout='constrained')
axs[0].scatter(e[~inside],n[~inside],s=.5,color='#B7BFBA',rasterized=True,label='Outside control hull')
axs[0].scatter(e[inside],n[inside],s=1.2,color=COPPER,rasterized=True,label='Inside control hull')
axs[0].set(xlabel='Easting − 837,500 (m)',ylabel='Northing − 821,000 (m)',title='1993 measured surface points')
axs[0].set_aspect('equal',adjustable='datalim')
axs[0].legend(frameon=False,markerscale=4,fontsize=7,loc='best')
sc=axs[1].scatter(e[inside],n[inside],c=z[inside],s=4,cmap='cividis',rasterized=True)
axs[1].set(xlabel='Easting − 837,500 (m)',ylabel='Northing − 821,000 (m)',title='Locally supported display sample')
axs[1].set_aspect('equal',adjustable='datalim')
cb=fig.colorbar(sc,ax=axs[1],shrink=.8)
cb.set_label('Height above fitted plane (m)',fontsize=8)
save(fig,'historical_support')
checks['stereo_display_sample']={'points':len(st),'inside_hull_points':int(inside.sum()),'subsampling':'every fifth source row'}
# Version 2: independently evaluate the new explicit wind case and exact bound.
from fractions import Fraction
cf=ROOT/'evidence/counterfactual'
wform=json.loads((cf/'formula.json').read_text())
wres=json.loads((cf/'result.json').read_text())
cert=json.loads((cf/'continuous_check.json').read_text())
wm=wres['metrics']
assert wres['status']=='conditional_scenario_feasible' and cert['certified']
assert wres['physical_prediction_interval'] is None and cert['historical_clearance'] is False
for key,name in [('checker_source_sha256','continuous.py'),('calculator_source_sha256','calculate.py'),('inputs_sha256','inputs.json')]:
    assert hashlib.sha256((cf/name).read_bytes()).hexdigest()==cert[key]
assert cert['q_real_decimal']==[str(x) for x in wres['q']]
assert cert['run_id']==wres['run_id']
for ph in [0,1]:
    boxes=sorted([x for x in cert['cover'] if x[0]==ph],key=lambda x:x[1])
    assert boxes[0][1]==0 and boxes[-1][2]==1
    assert all(a[2]==b[1] for a,b in zip(boxes,boxes[1:]))
assert len(cert['cover'])==376
upper=(Fraction(2636-200-138)-Fraction(69**2)/(2*Fraction('1.4709975')))/3136
lower=Fraction(cert['eta_lower_real_decimal'])
assert upper==Fraction(wres['global_bound']['upper_exact'])
assert upper-lower==Fraction(wres['global_bound']['candidate_certified_gap_upper_exact'])
wind=-21*1852/3600*np.array([np.cos(np.deg2rad(70-799/6)),np.sin(np.deg2rad(70-799/6)),0.])
assert np.allclose(wind,[-4.876589552990943,9.64006667211232,0],rtol=0,atol=1e-13)
assert math.isclose(wm['stop_x_m'],wm['touchdown_x_m']+2*wm['touchdown_groundspeed_mps']+wm['touchdown_groundspeed_mps']**2/(2*decel),abs_tol=1e-9)
assert math.isclose(wm['stop_time_s'],wm['touchdown_time_s']+2+wm['touchdown_groundspeed_mps']/decel,abs_tol=1e-10)
wrows=list(csv.DictReader((cf/'path_controls.csv').open()))
wcurves=[]
for phase in wform['phases']:
    data=[r for r in wrows if r['phase']==phase['name']]
    t=np.array([float(r['time_s']) for r in data]);s=(t-phase['t0_s'])/phase['duration_s']
    c=phase['coefficients_xyz_m']
    xyz=np.column_stack([np.polynomial.polynomial.polyval(s,row) for row in c])
    vel=np.column_stack([np.polynomial.polynomial.polyval(s,np.polynomial.polynomial.polyder(row))/phase['duration_s'] for row in c])
    assert np.max(np.abs(xyz-np.array([[float(r[k]) for k in ['x_m','y_m','z_m']] for r in data])))<1e-8
    assert np.max(np.abs(vel-np.array([[float(r[k]) for k in ['vx_mps','vy_mps','vz_mps']] for r in data])))<1e-9
    eas=np.linalg.norm(vel-wind,axis=1)*np.exp(-xyz[:,2]/17000)/(1852/3600)
    assert np.max(abs(eas-np.array([float(r['eas_kt']) for r in data])))<1e-8
    wcurves.append((t,xyz,vel,eas))
fig,axs=plt.subplots(3,1,figsize=(7,7.2),layout='constrained')
for (t,xyz,vel,eas),color,name in zip(wcurves,[SLATE,COPPER],['Approach','Flare']):
    axs[0].plot(xyz[:,0],xyz[:,1],color=color,lw=2,label=name)
    axs[1].plot(t,xyz[:,2],color=color,lw=2)
    axs[2].plot(t,np.linalg.norm(vel[:,:2],axis=1)/(1852/3600),color=SLATE,lw=2,label='Horizontal ground speed' if name=='Approach' else None)
    axs[2].plot(t,eas,color=COPPER,ls='--',lw=1.5,label='Equivalent airspeed' if name=='Approach' else None)
axs[0].plot([0,length],[0,0],lw=7,color='#D8DEDA',zorder=0)
axs[0].plot([wm['touchdown_x_m'],wm['stop_x_m']],[0,0],color=SAGE,lw=2,label='Ground travel')
axs[0].scatter([wm['stop_x_m']],[0],color=SAGE,s=25)
axs[0].set(xlabel='Runway-relative x (m)',ylabel='Lateral y (m)',title='Fixed mean wind; synthetic corridor; no historical clearance')
axs[0].legend(frameon=False,ncol=3,fontsize=8)
axs[1].axvline(wm['approach_s'],ls=':',color='#87918F')
axs[1].set(xlabel='Time from synthetic entry (s)',ylabel='Height (m)',title='Airborne reference, including the permitted shallow rise')
start=wm['touchdown_time_s'];end=wm['stop_time_s'];tt=np.linspace(start,end,600)
ug=np.maximum(0,wm['touchdown_groundspeed_mps']-decel*np.maximum(tt-start-2,0))
axs[2].plot(tt,ug/(1852/3600),color=SLATE,lw=2)
axs[2].axvline(start,color='#87918F',ls=':',lw=1)
axs[2].set(xlabel='Time from synthetic entry (s)',ylabel='Speed (kt)',title='Airspeed governs flight forces; ground speed governs stopping')
axs[2].legend(frameon=False,fontsize=8)
save(fig,'wind_landing')
fig,axs=plt.subplots(1,2,figsize=(7,3.7),layout='constrained',gridspec_kw={'width_ratios':[1.25,1]})
labels=['Calm witness','Mean-wind case']
for i,(xd,st) in enumerate([(xD,stop),(wm['touchdown_x_m'],wm['stop_x_m'])]):
    for left,width,color,label in [(0,xd,COPPER,'Before touchdown'),(xd,st-xd,SLATE,'Ground travel'),(st,length-st,SAGE,'Remaining')]:
        axs[0].barh(i,width,left=left,color=color,height=.38,label=label if i==0 else None)
    axs[0].text(length+35,i,f'{length-st:.0f} m',va='center',fontsize=8)
axs[0].set_yticks([0,1],labels,fontsize=8)
axs[0].set(xlim=(0,3400),xlabel='Threshold-relative distance (m)',title='Fixed 2 s delay / 0.15g braking')
axs[0].legend(frameon=False,fontsize=7,loc='upper left',bbox_to_anchor=(0,-.22))
for i,(lo,hi) in enumerate([(.0397,.1559772),(float(lower),float(upper))]):
    axs[1].plot([lo,hi],[i,i],color=SLATE,lw=3)
    axs[1].scatter([lo],[i],color=SAGE,s=35,zorder=3)
    axs[1].scatter([hi],[i],facecolors='white',edgecolors=COPPER,s=35,zorder=3)
    axs[1].text(lo,i-.17,f'{lo:.4f}',fontsize=8,ha='center')
    axs[1].text(hi,i+.16,f'{hi:.4f}',fontsize=8,ha='center')
axs[1].set(yticks=[0,1],yticklabels=[],ylim=(-.55,1.55),xlim=(0,.24),xlabel='Normalized margin',title='Feasible certificate → upper bound')
save(fig,'scenario_comparison')
checks['wind_case']={'formula_csv_states_and_velocities_match':True,'eas_recomputed_from_wind':True,'certificate_source_bindings':True,'closed_interval_cover':376,'exact_upper':str(upper),'exact_gap':str(upper-lower),'stopping_and_time_recomputed':True,'runway_remaining_m':wm['runway_remaining_m'],'remainder_difference_m':wm['runway_remaining_m']-(length-stop),'touchdown_component_m':xD-wm['touchdown_x_m'],'ground_travel_component_m':(stop-xD)-wm['ground_travel_m']}

(QA/'figure_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
