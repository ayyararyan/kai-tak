"""Version 3 original scientific figures. Inputs are frozen, never generated history."""
from pathlib import Path
import csv,json,math,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc,Rectangle,FancyArrowPatch
from matplotlib.collections import LineCollection
P=Path(__file__).resolve().parent;F=P/'figures';F.mkdir(exist_ok=True)
INK='#304750';SAGE='#687C69';COPPER='#AF6843';BLUE='#367C91';LIGHT='#DDE3DF';GREY='#929B99'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'axes.titleweight':'bold','axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'text.color':INK,'axes.labelcolor':INK,'axes.edgecolor':GREY,'pdf.fonttype':42,'savefig.facecolor':'white'})
records=[]
def read(s):return json.loads((P/s).read_text())
def csvread(s):return list(csv.DictReader((P/s).open()))
def save(fig,name,inputs,meaning):
 fig.savefig(F/(name+'.pdf'),bbox_inches='tight',metadata={'CreationDate':None,'Title':meaning})
 fig.savefig(F/(name+'.png'),bbox_inches='tight',dpi=190)
 records.append({'figure':name,'inputs':inputs,'meaning':meaning,'pdf_sha256':hashlib.sha256((F/(name+'.pdf')).read_bytes()).hexdigest()});plt.close(fig)
def grid(ax):ax.grid(alpha=.16);ax.set_axisbelow(True)
def note(ax,s):ax.text(.02,.96,s,transform=ax.transAxes,va='top',fontsize=9,bbox=dict(fc='white',ec='none',alpha=.9))
cf=read('evidence/approximation/reference_formula.json');wf=read('evidence/counterfactual/formula.json');wr=read('evidence/counterfactual/result.json')['metrics'];p=cf['scalar_inputs'];a=p['brake_deceleration_mps2'];u=p['touchdown_speed_mps'];xd=p['touchdown_x_m'];L=2786;stop=xd+2*u+u*u/(2*a)
def curve(form,wind=False):
 out=[]
 for ph in form['phases']:
  s=np.linspace(0,1,801);T=ph['duration_s'];t0=ph.get('start_s',ph.get('t0_s'));c=ph['coefficients_xyz_m'];q=np.column_stack([np.polynomial.polynomial.polyval(s,r) for r in c]);v=np.column_stack([np.polynomial.polynomial.polyval(s,np.polynomial.polynomial.polyder(r))/T for r in c]);out.append((t0+s*T,q,v))
 return out
calm=curve(cf);wind=curve(wf)
# 1: original photograph, with source-bound visual locators, no invented track overlay.
im=plt.imread(P/'inputs/A36143.jpg');h,w=im.shape[:2]
fig,ax=plt.subplots(figsize=(7.1,6.3));ax.imshow(im,cmap='gray',vmin=0,vmax=255);ax.axis('off')
for text,xy,tx in [('Runway 13 pavement',(.29,.63),(.17,.21)),('Apron and aircraft',(.63,.69),(.78,.87)),('Dense Kowloon blocks',(.65,.22),(.70,.09))]:
 ax.annotate(text,xy=(xy[0]*w,xy[1]*h),xytext=(tx[0]*w,tx[1]*h),ha='center',fontsize=10,color=INK,bbox=dict(fc='white',ec=INK,pad=4,alpha=.94),arrowprops=dict(arrowstyle='-',color='white',lw=1.7))
save(fig,'01_historical_airport',['inputs/A36143.jpg','inputs/A36143_product.json'],'Historical photograph; scanned orientation, not a route reconstruction')
# 2: exact bearings in common magnetic frame; schematic not a flight path.
fig,axs=plt.subplots(1,2,figsize=(7.1,3.65),layout='constrained',gridspec_kw={'width_ratios':[1.15,1]})
ax=axs[0]
for b,col,lab in [(88,BLUE,'IGS localiser: 088° M'),(135,COPPER,'Runway direction: 135° M')]:
 end=np.array([np.sin(np.deg2rad(b)),np.cos(np.deg2rad(b))]);ax.annotate('',xy=end,xytext=(0,0),arrowprops=dict(arrowstyle='-|>',lw=2,color=col));ax.text(end[0]*1.04,end[1]*1.1,lab,fontsize=9,ha='right' if b==135 else 'center',va='top' if b==135 else 'bottom',color=col)
ax.annotate('',xy=(0,1),xytext=(0,0),arrowprops=dict(arrowstyle='->',color=GREY));ax.text(0,1.08,'Magnetic north',ha='center',fontsize=9)
ax.add_patch(Arc((0,0),1,1,theta1=-45,theta2=2,color=INK,lw=1.5));ax.text(.58,-.16,'47°',fontsize=18)
ax.set(xlim=(-.25,1.5),ylim=(-1,1.3),aspect='equal');ax.axis('off');ax.set_title('Direction change ≠ bank angle')
ax=axs[1];ax.axis('off')
for y,title,desc in [(.83,'INSTRUMENT SEGMENT','Lateral IGS beam + 3.1° glidepath'),(.49,'VISUAL TRANSITION','Acquire visual references by middle marker'),(.15,'RUNWAY ALIGNMENT','Right turn, then flare, touchdown and stop')]:
 ax.text(0,y,title,color=COPPER,weight='bold',fontsize=10);ax.text(0,y-.10,desc,fontsize=8.5,wrap=True)
 if y>.2:ax.annotate('',xy=(.06,y-.26),xytext=(.06,y-.14),arrowprops=dict(arrowstyle='->',color=GREY))
save(fig,'02_approach_geometry',['CAD Report 1/95 §1.8.1, §1.10, Appendix 1'],'Magnetic bearing difference and procedure sequence; schematic, not to scale')
# 3: dated survey maps on identical coordinate extents.
fig,axs=plt.subplots(1,2,figsize=(7.1,3.8),layout='constrained')
faces=read('inputs/historical_faces.geojson')['features']
for ax,epoch in zip(axs,['1989-10','1994-07']):
 ax.imshow(plt.imread(P/f'inputs/11-NE-11A_{epoch}_core.png'),extent=(0,750,0,600));ax.set_title(epoch+' · sheet 11-NE-11A');ax.set(xlabel='East − 837,500 m',ylabel='North − 821,000 m',xlim=(0,750),ylim=(0,600));ax.set_aspect('equal')
 for key,num in [('shing_tung','1'),('regal','2'),('city_market','3')]:
  f=next(f for f in faces if f['properties']['id']==key and f['properties']['source_epoch']=='1989-10');q=f['properties'];ax.text(q['seed_e']-837500,q['seed_n']-821000,num,ha='center',va='center',fontsize=9,weight='bold',bbox=dict(boxstyle='circle',fc='white',ec=COPPER))
 ax.plot([550,650],[30,30],color=INK,lw=3);ax.text(600,48,'100 m',ha='center',fontsize=8)
fig.supxlabel('Locators: 1 Shing Tung House     2 Regal Airport Hotel     3 Kowloon City Market',fontsize=9)
save(fig,'03_dated_maps',['inputs/11-NE-11A_1989-10_core.png','inputs/11-NE-11A_1994-07_core.png','inputs/historical_faces.geojson'],'Same local grid, different map editions; locator labels do not prove 1993 presence')
# 4: reconstruction and spatial support.
r=csvread('evidence/stereo_plot_data.csv');e=np.array([float(x['easting_hk1980_m']) for x in r])-837500;n=np.array([float(x['northing_hk1980_m']) for x in r])-821000;z=np.array([float(x['z_above_fitted_local_park_road_plane_m']) for x in r]);inside=np.array([x['within_map_control_hull']=='True' for x in r])
fig,axs=plt.subplots(1,2,figsize=(7.1,3.7),layout='constrained')
axs[0].scatter(e[~inside],n[~inside],s=.55,c=LIGHT,rasterized=True);axs[0].scatter(e[inside],n[inside],s=1,c=COPPER,rasterized=True);axs[0].set_title('Local control support');note(axs[0],'171,307 retained points\n3,780 inside control hull')
sc=axs[1].scatter(e,n,c=z,s=.7,cmap='cividis',vmin=-10,vmax=60,rasterized=True);axs[1].set_title('Relative surface elevation');cb=fig.colorbar(sc,ax=axs[1],shrink=.8,extend='both');cb.set_label('Height above fitted plane (m)',fontsize=8)
for ax in axs:ax.set(xlabel='East − 837,500 m',ylabel='North − 821,000 m');ax.set_aspect('equal',adjustable='datalim')
save(fig,'04_reconstruction',['evidence/stereo_plot_data.csv','evidence/reconstruction/block_matching/HANDOFF.json'],'Every-fifth-point display; conditional local plane, not HKPD or complete roofs')
# 5: turn physics at stipulated illustrative speeds.
fig,axs=plt.subplots(1,2,figsize=(7.1,3.7),layout='constrained');phi=np.linspace(5,30,250);g=9.80665;ang=np.deg2rad(47);insights={}
for speed,col in [(70,SAGE),(78,INK),(85,COPPER)]:
 R=speed**2/(g*np.tan(np.deg2rad(phi)));axs[0].plot(phi,R/1000,color=col,label=f'{speed} m/s');axs[1].plot(phi,ang*R/speed,color=col)
for ax in axs:ax.axvline(15,color=GREY,ls=':',lw=1);ax.set_xlabel('Bank angle (degrees)');grid(ax)
axs[0].set(ylabel='Air-relative turn radius (km)',title='Radius grows with speed²');axs[0].legend(frameon=False,fontsize=8);axs[1].set(ylabel='Time for 47° change (s)',title='Time needed for a 47° turn');R=78**2/(g*np.tan(np.deg2rad(15)));insights['turn_78mps_15deg']={'radius_m':R,'time_47deg_s':ang*R/78,'arc_m':ang*R,'load_factor':1/np.cos(np.deg2rad(15))};note(axs[1],f'78 m/s, 15° bank:\n{R/1000:.2f} km radius; {ang*R/78:.1f} s')
save(fig,'05_turn_physics',['Equations R=V²/(g tan phi), t=delta R/V; illustrative level coordinated turn'],'Constant-speed, still-air level-turn benchmark, not a reconstructed flight')
# 6: vector triangle and components varying along direction.
W=21*1852/3600;alpha=799/6;wx=-W*np.cos(np.deg2rad(70-alpha));wy=-W*np.sin(np.deg2rad(70-alpha));uw=wr['touchdown_groundspeed_mps']
fig,axs=plt.subplots(1,2,figsize=(7.1,3.8),layout='constrained');ax=axs[0]
# display forward horizontally, right down for physical top-view orientation
points=[((0,0),(uw-wx,-wy),INK,'Air velocity'),((uw-wx,-wy),(uw,0),COPPER,'Wind'),((0,0),(uw,0),SAGE,'Ground velocity')]
for start,end,col,label in points:ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='-|>',lw=2,color=col),label=label)
ax.text(30,-11,'Air velocity',color=INK);ax.text(79,-7,'Wind',color=COPPER);ax.text(20,2,'Ground velocity',color=SAGE);ax.set(xlim=(-3,100),ylim=(-18,10),xlabel='Forward component (m/s)',ylabel='Right component (m/s)',title='At model touchdown');ax.invert_yaxis();grid(ax)
chi=np.linspace(-47,0,150);c=np.deg2rad(chi);along=wx*np.cos(c)+wy*np.sin(c);cross=-wx*np.sin(c)+wy*np.cos(c);axs[1].plot(chi,along,color=INK,label='Along track');axs[1].plot(chi,cross,color=COPPER,label='Right across track');axs[1].axhline(0,color=GREY,lw=.7);axs[1].set(xlabel='Ground track relative to runway (degrees)',ylabel='Wind component (m/s)',title='The same wind changes its role');axs[1].legend(frameon=False,fontsize=8);grid(axs[1]);insights['wind']={'forward_mps':wx,'right_mps':wy,'entry_along_mps':along[0],'entry_cross_mps':cross[0]}
save(fig,'06_wind_vectors',['evidence/counterfactual/inputs.json','evidence/counterfactual/result.json'],'070° true / 21 kt constant wind; runway true-bearing convention 133°10′')
# 7: calm altitude and derived kinematics (no controls silently interpolated).
fig,axs=plt.subplots(3,1,figsize=(7.1,5.1),layout='constrained',sharex=True)
for t,q,v in calm:
 axs[0].plot(t,q[:,2],color=INK);axs[1].plot(t,v[:,2],color=COPPER);axs[2].plot(t,np.linalg.norm(v[:,:2],axis=1)*3600/1852,color=SAGE)
for ax in axs:ax.axvline(p['approach_s'],color=GREY,ls=':');grid(ax)
axs[0].set(ylabel='Height (m)',title='The retained calm-air candidate has a brief rise');axs[1].set(ylabel='Vertical speed (m/s)');axs[1].axhline(0,color=GREY,lw=.7);axs[2].set(ylabel='Ground speed (kt)',xlabel='Time from synthetic entry (s)');save(fig,'07_calm_profiles',['evidence/approximation/reference_formula.json'],'Exact polynomial evaluation; height above runway, positive vertical speed is climb')
# 8: stopping decomposition + nonlinear boundary.
fig,axs=plt.subplots(1,2,figsize=(7.1,3.65),layout='constrained',gridspec_kw={'width_ratios':[.8,1.2]})
for i,(name,val,col) in enumerate([('Before touchdown',xd,COPPER),('Delay travel',2*u,BLUE),('Braking travel',u*u/(2*a),INK),('Remaining',L-stop,SAGE)]):
 axs[0].barh(3-i,val,color=col,height=.6);axs[0].text(val+40,3-i,f'{val:,.0f} m',va='center',fontsize=8)
axs[0].set_yticks(range(4),['Remaining','Braking travel','Delay travel','Before touchdown'],fontsize=8);axs[0].set(xlim=(0,2600),xlabel='Distance (m)',title='Where the runway goes')
speed=np.linspace(69,88,250);bound=L-150-2*speed-speed**2/(2*a);axs[1].fill_between(speed,200,bound,where=bound>=200,color=SAGE,alpha=.18);axs[1].plot(speed,bound,color=INK,lw=2);axs[1].scatter(u,xd,marker='*',s=110,color=COPPER,zorder=5);axs[1].set(xlabel='Touchdown ground speed (m/s)',ylabel='Latest touchdown station (m)',ylim=(0,900),title='Leave the stipulated 150 m reserve');grid(axs[1]);insights['stop']={'delay_m':2*u,'braking_m':u*u/(2*a),'dR_du':-2-u/a,'dR_dd':-u,'speed_10pct_braking_ratio':1.1**2}
save(fig,'08_stopping',['evidence/approximation/reference_formula.json'],'Fixed 2 s delay, 0.15g braking and 2,786 m LDA; scalar condition only')
# 9: complete calm trajectory, 3D plus undistorted plan.
fig=plt.figure(figsize=(7.1,4.8),layout='constrained');gs=fig.add_gridspec(2,1,height_ratios=[3,1]);ax=fig.add_subplot(gs[0],projection='3d');ap=fig.add_subplot(gs[1])
for (t,q,v),col in zip(calm,[INK,COPPER]):ax.plot(q[:,0],q[:,1],q[:,2],color=col,lw=2);ap.plot(q[:,0],q[:,1],color=col,lw=2)
ax.plot([xd,stop],[0,0],[0,0],color=SAGE,lw=2);ax.set(xlabel='x (m)',ylabel='y (m)',zlabel='Height (m)',title='Approach → flare → full stop');ax.view_init(24,-110);ax.set_proj_type('ortho');ax.set_box_aspect((4,1.3,.8),zoom=1.5);ax.set_xticks([-2500,0,2500]);ax.set_yticks([0,1000]);ax.set_zticks([0,70,140]);ax.tick_params(labelsize=8);ax.xaxis.pane.fill=False;ax.yaxis.pane.fill=False;ax.zaxis.pane.fill=False
ap.plot([0,L],[0,0],color=LIGHT,lw=8,zorder=0);ap.plot([xd,stop],[0,0],color=SAGE,lw=2);ap.scatter([0,xd,stop],[0,0,0],color=[INK,COPPER,SAGE],s=20);ap.set(xlabel='Runway-forward x (m)',ylabel='Right-of-runway y (m)',aspect='equal');note(ap,'Plan view: equal horizontal scale\n3D view above: height exaggerated')
save(fig,'09_complete_calm',['evidence/approximation/reference_formula.json'],'Synthetic runway-relative geometry without historical terrain')
# 10: certificate coverage actual accepted dyadic intervals.
cert0=read('evidence/analytical/coupled/continuous_certificate_refined.json');cert1=read('evidence/counterfactual/continuous_check.json')
# Inspect cover schema defensively, use wind verified structure for an actual interval chart.
fig,axs=plt.subplots(2,1,figsize=(7.1,3.6),layout='constrained',sharex=True)
for ph,ax in enumerate(axs):
 boxes=np.array([r for r in cert1['cover'] if r[0]==ph]);mid=(boxes[:,1]+boxes[:,2])/2;width=boxes[:,2]-boxes[:,1];ax.step(mid,width,where='mid',color=INK);ax.set_yscale('log',base=2);ax.set(ylabel='Interval width Δs',title=['Approach: adaptive closed-interval cover','Flare: separately checked through touchdown'][ph]);grid(ax)
axs[1].set_xlabel('Normalized phase time s (dimensionless)');save(fig,'10_certificate',['evidence/counterfactual/continuous_check.json'],'Actual accepted wind-certificate subdivisions, not sampled aircraft tracking error')
# 11: wind candidate controls with envelope.
rows=csvread('evidence/counterfactual/path_controls.csv');flight=[r for r in rows if r['phase'] in ['approach','flare']];t=np.array([float(r['time_s']) for r in flight])
fig,axs=plt.subplots(3,2,figsize=(7.1,5.7),layout='constrained',sharex=True)
items=[('z_m','Height (m)',None),('eas_kt','Equivalent airspeed (kt)',(135,175)),('bank_deg','Bank angle (degrees)',(-25,25)),('roll_deg_s','Bank-angle rate (deg/s)',(-5,5)),('thrust_n','Thrust (kN)',(0,700)),('thrust_slew_n_s','Thrust slew (kN/s)',(-100,100))]
for ax,(key,lab,limits) in zip(axs.flat,items):
 vals=np.array([float(r[key]) for r in flight])/(1000 if key in ['thrust_n','thrust_slew_n_s'] else 1);ax.plot(t,vals,color=INK,lw=1.4);ax.axvline(wr['threshold_time_s'] if 'threshold_time_s' in wr else wf['phases'][0]['duration_s'],color=COPPER,ls=':',lw=1);ax.set_ylabel(lab);grid(ax)
 if limits:
  for y in limits:ax.axhline(y,color=GREY,ls='--',lw=.8)
for ax in axs[-1]:ax.set_xlabel('Time from synthetic entry (s)')
save(fig,'11_wind_profiles',['evidence/counterfactual/path_controls.csv','evidence/model/config.json'],'Wind-conditioned candidate: sampled display; continuous validity comes from separate certificate')
# 12: separately optimized scenarios and separate optimum brackets.
fig,allaxs=plt.subplots(3,1,figsize=(7.1,5.6),layout='constrained',gridspec_kw={'height_ratios':[.7,1,1]})
pa=allaxs[0];axs=allaxs[1:]
for group,col,label in [(calm,INK,'Calm'),(wind,COPPER,'Steady wind')]:
 for j,(tt,qq,vv) in enumerate(group):pa.plot(qq[:,0],qq[:,1],color=col,lw=1.6,label=label if j==0 else None)
pa.set(xlabel='Runway-forward x (m)',ylabel='Lateral y (m)',aspect='equal');pa.legend(frameon=False,ncol=2,fontsize=8,loc='upper right');grid(pa)
for i,(x,s) in enumerate([(xd,stop),(wr['touchdown_x_m'],wr['stop_x_m'])]):
 for left,width,col,label in [(0,x,COPPER,'To touchdown'),(x,s-x,INK,'Ground travel'),(s,L-s,SAGE,'Remaining')]:axs[0].barh(i,width,left=left,height=.4,color=col,label=label if i==0 else None)
 axs[0].text(L+30,i,f'{L-s:.2f} m left',fontsize=9,va='center')
axs[0].set(yticks=[0,1],yticklabels=['Calm witness','Steady-wind witness'],xlim=(0,3400),xlabel='Threshold-relative station (m)');axs[0].legend(frameon=False,ncol=3,fontsize=8,loc='lower center',bbox_to_anchor=(.55,1.01))
for i,(lo,hi) in enumerate([(.0397,.1559772),(.1507934696816132,66656817/307536544)]):
 axs[1].plot([lo,hi],[i,i],color=INK,lw=3);axs[1].scatter(lo,i,c=SAGE,s=45,zorder=5);axs[1].scatter(hi,i,facecolor='white',edgecolor=COPPER,s=45,zorder=5);axs[1].text(lo,i-.24,f'{lo:.5f}',ha='center',fontsize=8);axs[1].text(hi,i+.19,f'{hi:.5f}',ha='center',fontsize=8)
axs[1].set(yticks=[0,1],yticklabels=['Calm problem','Wind problem'],ylim=(-.5,1.5),xlim=(0,.24),xlabel='Normalized margin η (dimensionless)');grid(axs[1]);save(fig,'12_scenario_comparison',['evidence/approximation/reference_outcomes.json','evidence/counterfactual/result.json'],'Two problems, not a causal treatment/control comparison; bounds are not confidence intervals')
# 13: manual recorder anchors, no interpolated samples posing as observations.
r=csvread('evidence/evidence/cal605_reconstruction/flight/flight_anchor_readings.csv');fig,axs=plt.subplots(3,1,figsize=(7.1,5),layout='constrained',sharex=True)
for ax,vars,lab in [(axs[0],['calibrated_airspeed_kt','groundspeed_kt'],'Speed (kt)'),(axs[1],['radio_altitude_ft'],'Radio altitude (ft)'),(axs[2],['heading_degM'],'Heading (° magnetic)')]:
 for key,col in zip(vars,[INK,COPPER]):
  rr=sorted([x for x in r if x['variable']==key],key=lambda x:float(x['time_datum_B_s']));tt=np.array([float(x['time_datum_B_s']) for x in rr]);vv=np.array([float(x['value']) for x in rr]);lo=np.array([float(x['reading_lo']) for x in rr]);hi=np.array([float(x['reading_hi']) for x in rr]);ax.errorbar(tt,vv,yerr=[vv-lo,hi-vv],fmt='o-',ms=2.5,lw=.8,elinewidth=.5,alpha=.85,color=col,label=key.replace('_',' '))
 ax.set_ylabel(lab);grid(ax)
axs[0].legend(frameon=False,ncol=2,fontsize=8);axs[-1].set_xlabel('Flight-recorder plot time, datum B (s; not the wind-system clock)');save(fig,'13_recorder',['evidence/evidence/cal605_reconstruction/flight/flight_anchor_readings.csv'],'Manual readings of CAD Appendix 11 Fig. 4; bars are raster-reading sensitivity, not physical confidence intervals')
# 14: sensor readings and annual context.
r=csvread('evidence/evidence/cal605_reconstruction/wind/wind_records.csv');fig,axs=plt.subplots(1,2,figsize=(7.1,3.9),layout='constrained')
for sensor,col in [('NW',INK),('LYM',COPPER)]:
 rr=[x for x in r if x['sensor']==sensor and x['field']=='A'];
 if not rr:print('Available sensors',sorted(set(x['sensor'] for x in r)));continue
 axs[0].plot([float(x['seconds_since_wind_clock_033000'])/60 for x in rr],[float(x['speed_kt_printed']) for x in rr],'o-',ms=3,lw=1,color=col,label=sensor)
axs[0].set(xlabel='Minutes after wind-clock 03:30',ylabel='A-field speed (kt)',title='Different places, same printout');axs[0].legend(frameon=False,fontsize=8);grid(axs[0])
r=csvread('evidence/weather_plot_data.csv');rr=[x for x in r if x['report_type']=='FM-15' and x['source_flag']=='4' and x['datetime_utc'][14:19]=='00:00' and x['wind_type']=='N' and x['wind_speed_mps'] and x['wind_speed_mps_strict_qc_accepted']=='True' and x['partial_weather_row']=='False'];v=np.sort([float(x['wind_speed_mps']) for x in rr]);axs[1].step(v,np.arange(1,len(v)+1)/len(v)*100,color=INK);axs[1].axvline(10.8,color=COPPER,ls='--');axs[1].set(xlabel='Station mean wind (m/s)',ylabel='Cumulative share (%)',title='1993 selected archive: 8,360 rows');note(axs[1],'10.8 m/s:\n8,285 lower · 17 tied · 58 higher');grid(axs[1]);save(fig,'14_weather',['evidence/evidence/cal605_reconstruction/wind/wind_records.csv','evidence/weather_plot_data.csv'],'Event-triggered ground sensors and routine annual station subset; clocks not synchronized')
# 15: observed landmark stopping challenge.
hist=read('evidence/evidence/cal605_reconstruction/analysis.json');r=hist['report_landmark_stopping_frontier'];fig,axs=plt.subplots(1,2,figsize=(7.1,3.7),layout='constrained');idx=np.arange(4);names=['Touchdown','Roll restored','Autobrake call','Reverse selected']
axs[0].plot(idx,[x['speed_kt'] for x in r],'-o',color=INK);axs[0].set(ylabel='Report-stated ground speed (kt)',title='Speed falls')
for key,col,label in [('required_decel_no_delay_g',COPPER,'No additional delay'),('required_decel_with_2s_delay_g',SAGE,'Two more seconds')]:axs[1].plot(idx,[x[key] for x in r],'-o',color=col,label=label)
axs[1].set(ylabel='Required constant deceleration (g)',title='But the stopping requirement rises');axs[1].legend(frameon=False,fontsize=8)
for ax in axs:ax.set_xticks(idx,names,rotation=25,ha='right',fontsize=8);grid(ax)
save(fig,'15_rollout',['evidence/evidence/cal605_reconstruction/analysis.json'],'Derived necessary deceleration from four narrative landmarks; not actual measured braking')
# 16: explicit evidence chain, all categories visible.
fig,ax=plt.subplots(figsize=(7.1,4.2));ax.axis('off');ax.set(xlim=(0,10),ylim=(0,6))
labels=[('OBSERVED / SOURCE-REPORTED','Charts, photographs, recorder plots, weather',.3,4.7,BLUE),('RECONSTRUCTED','Dated map faces, approximate trace anchors',.3,3.15,BLUE),('ASSUMED + CONSTRUCTED','Aircraft envelope, synthetic entry; two paths',5.25,4.7,COPPER),('COMPUTER-ASSISTED CERTIFICATE','All-time feasibility in the stated model',5.25,3.15,SAGE),('STILL UNIDENTIFIED','Complete historical obstacles • calibrated tracking and braking\nCausal gust policy • useful global gap • fair historical improvement',.3,.75,GREY)]
for title,desc,x,y,col in labels:
 width=9.4 if y<1 else 4.45;ax.add_patch(Rectangle((x,y),width,1.05,fc=col,alpha=.10,ec=col,lw=1));ax.text(x+.16,y+.70,title,fontsize=8.5,weight='bold',color=col);ax.text(x+.16,y+.30,desc,fontsize=8,va='center')
for x in [2.5,7.5]:ax.annotate('',xy=(x,4.23),xytext=(x,4.68),arrowprops=dict(arrowstyle='->',color=GREY))
ax.text(5,2.45,'The missing connection is empirical calibration and common geometry.',ha='center',fontsize=10,color=INK)
save(fig,'16_evidence_synthesis',['SPEC.md','evidence/reconstruction/obstacles/readiness.json','evidence/counterfactual/result.json'],'Evidence categories; arrows denote dependencies, not proof of the historical landing')
(P/'qa/figure_provenance.json').write_text(json.dumps(records,indent=2)+'\n');(P/'qa/insight_calculations.json').write_text(json.dumps(insights,indent=2)+'\n');print('Generated',len(records),'original figure composites')
