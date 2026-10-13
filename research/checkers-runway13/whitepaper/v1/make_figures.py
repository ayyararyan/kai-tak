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
FIG = ROOT / 'figures'
QA = ROOT / 'qa'
FIG.mkdir(exist_ok=True)
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
(QA/'figure_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
