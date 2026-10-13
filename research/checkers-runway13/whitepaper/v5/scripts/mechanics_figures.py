"""Original V5 mechanics illustrations; source coefficients and scalars are immutable."""
from figure_style import *
from matplotlib.patches import Rectangle,Arc,Polygon,Circle
import argparse,math
C=read('evidence/approximation/reference_formula.json')
W=read('evidence/counterfactual/formula.json')
WR=read('evidence/counterfactual/result.json')['metrics']
c=C['scalar_inputs'];g=9.80665;L=2786.;a=c['brake_deceleration_mps2']
u=c['touchdown_speed_mps'];xd=c['touchdown_x_m'];stop=xd+2*u+u*u/(2*a)
calm=curve(C);wind=curve(W)

def project(q):
 # Orthonormal camera rows: one metric scale for all three coordinates.
 az=np.deg2rad(-14);el=np.deg2rad(53)
 cam=np.array([[np.cos(az),-np.sin(az),0],[np.sin(az)*np.sin(el),np.cos(az)*np.sin(el),np.cos(el)]])
 return np.asarray(q)@cam.T

def path(ax,q,**kw):
 r=project(q);return ax.plot(r[:,0],r[:,1],**kw)

def landing():
 fig=plt.figure(figsize=(7.1,4.7));ax=fig.add_axes([.025,.25,.95,.70]);bare(ax)
 # A usable landing strip, 61 m wide. This is a local model plane, not a terrain model.
 verts=np.array([[0,-30.5,0],[L,-30.5,0],[L,30.5,0],[0,30.5,0]])
 ax.add_patch(Polygon(project(verts),facecolor=LIGHT,edgecolor=SLATE,lw=.65))
 verts[:,0]=np.array([stop,L,L,stop]);ax.add_patch(Polygon(project(verts),fc=SAGE,ec='none',alpha=.35))
 path(ax,[[0,0,0],[L,0,0]],color='white',lw=1,ls=(0,(6,5)))
 for y in np.linspace(-25,20,6):
  ax.add_patch(Polygon(project([[12,y,0],[48,y,0],[48,y+4,0],[12,y+4,0]]),fc='white',ec='none'))
 q=np.vstack([x[1] for x in calm]);ground=q.copy();ground[:,2]=0
 path(ax,ground,color=SLATE,lw=.8,ls=(0,(2,3)),alpha=.75)
 for (_t,p,_v),col in zip(calm,[INK,COPPER]):path(ax,p,color=col,lw=2.4)
 path(ax,[[xd,0,0],[xd+2*u,0,0]],color=BLUE,lw=3)
 path(ax,[[xd+2*u,0,0],[stop,0,0]],color=SAGE,lw=2.8)
 for xyz in [q[0],[0,0,15.24]]:
  path(ax,[xyz,[xyz[0],xyz[1],0]],color=SLATE,lw=.75)
 for xyz,col in [(q[0],INK),([0,0,15.24],COPPER),([xd,0,0],BLUE),([stop,0,0],SAGE)]:
  t=project(xyz);ax.scatter(*t,s=16,color=col,zorder=8)
 label(ax,'Entry\n140 m above runway',project(q[0]),(-2700,1550),size=12)
 label(ax,'Threshold\n15.24 m',project([0,0,15.24]),(-250,620),size=12,align='center')
 label(ax,'Touchdown\n313.49 m',project([xd,0,0]),(750,430),size=12,align='center')
 label(ax,'Stop\n2,531.32 m',project([stop,0,0]),(2650,-30),size=12,align='center',color=SAGE)
 path(ax,[[0,-190,0],[L,-190,0]],color=SLATE,lw=.7)
 for x in [0,L]:path(ax,[[x,-160,0],[x,-220,0]],color=SLATE,lw=.7)
 mid=project([L/2,-290,0]);ax.text(*mid,'2,786 m landing distance available',rotation=-11.2,ha='center',va='center',fontsize=11.5,color=SLATE)
 fig.text(.055,.97,'LOCAL MODEL · ORTHOGRAPHIC VIEW',fontsize=10.5,color=SLATE,va='top')
 fig.text(.97,.97,'Equal physical scale in x, y and height',fontsize=10.5,color=SLATE,ha='right',va='top')
 ax.set(xlim=(-2900,3100),ylim=(-970,1800),aspect='equal')
 # A local detail enlarges all coordinates together, exposing the runway plane.
 ai=fig.add_axes([.63,.73,.34,.17]);bare(ai)
 ai.add_patch(Polygon(project([[0,-30.5,0],[500,-30.5,0],[500,30.5,0],[0,30.5,0]]),fc=LIGHT,ec=SLATE,lw=.6))
 path(ai,[[0,0,0],[500,0,0]],color='white',lw=1,ls=(0,(5,4)))
 for y in np.linspace(-25,20,6):
  ai.add_patch(Polygon(project([[12,y,0],[48,y,0],[48,y+4,0],[12,y+4,0]]),fc='white',ec='none'))
 path(ai,calm[1][1],color=COPPER,lw=2)
 path(ai,[[0,0,0],[0,0,15.24]],color=INK,lw=.7)
 path(ai,[[xd,0,0],[xd+2*u,0,0]],color=BLUE,lw=2)
 ai.text(10,62,'Flare detail',fontsize=11.5,weight='bold')
 path(ai,[[270,-90,0],[370,-90,0]],color=SLATE,lw=1)
 pp=project([320,-120,0]);ai.text(*pp,'100 m',ha='center',va='top',fontsize=10,color=SLATE)
 ai.set(xlim=(-20,530),ylim=(-190,88),aspect='equal')
 ap=fig.add_axes([.12,.095,.80,.15])
 for (t,q,v),col in zip(calm,[INK,COPPER]):ap.plot(t,q[:,2],color=col,lw=1.6)
 ap.set(xlim=(0,42),ylim=(0,165),xticks=[0,10,20,30,40],yticks=[0,140]);ap.set_xlabel('Time from model entry (s)',labelpad=3,fontsize=11)
 ap.text(0,1.12,'Height above runway (m)',transform=ap.transAxes,fontsize=10.5,color=SLATE)
 ap.axvline(c['approach_s'],color=SLATE,ls=':',lw=.7)
 tt,qq,vv=calm[0];mask=(tt>3)&(tt<25);j=np.flatnonzero(mask)[np.argmax(qq[mask,2])]
 ap.annotate('brief rise retained',xy=(tt[j],qq[j,2]),xytext=(24,145),fontsize=10.5,ha='left',arrowprops={'arrowstyle':'-','color':SLATE,'lw':.6})
 save(fig,'04_landing',['evidence/approximation/reference_formula.json'],
  'Calm complete landing in an accurately scaled orthographic local model scene',
  coordinate_frame='runway forward/right/up; metres; not geographically registered',vertical_exaggeration=1,
  camera={'azimuth_deg':-14,'elevation_deg':53,'projection':'orthographic, orthonormal rows'},
  runway_display={'length_m':L,'width_m':61,'meaning':'reported width and LDA used to draw local strip, not historical registration'},
  plotted_stop_m=stop)

def runway():
 fig,ax=plt.subplots(figsize=(7.1,4.0));fig.subplots_adjust(left=.07,right=.98,top=.98,bottom=.06);bare(ax)
 ax.set(xlim=(-100,2920),ylim=(-.48,2.65))
 vals=[('Calm air',xd,u,stop,1.9),('Steady wind',WR['touchdown_x_m'],WR['touchdown_groundspeed_mps'],WR['stop_x_m'],.32)]
 for title,x,v,s,y in vals:
  bounds=[0,x,x+2*v,s,L];col=[COPPER,BLUE,INK,SAGE]
  ax.text(0,y+.36,title,fontsize=13,weight='bold')
  ax.text(L,y+.36,f'{L-s:,.2f} m left',ha='right',color=SAGE,fontsize=13,weight='bold')
  for i in range(4):ax.add_patch(Rectangle((bounds[i],y-.10),bounds[i+1]-bounds[i],.20,fc=col[i],ec='white',lw=.6,alpha=.9 if i<3 else .7))
  ax.plot([0,L],[y,y],color='white',lw=.55,ls=(0,(5,5)))
  for b in [0,x,x+2*v,s,L]:ax.plot([b,b],[y-.13,y+.13],color='white',lw=.7)
  # small segments labelled by leaders, not text squeezed into the runway.
  for value,txt,at in [(x,f'Touchdown\n{x:.2f} m',(x-95,y+.05)),(x+2*v,f'Braking begins\n{x+2*v:.2f} m',(x+360,y+.05))]:
   # label rail below each runway; leader angles distinguish close stations.
   label(ax,txt,(value,y-.12),(at[0],y-.36),size=10.7,align='center')
  label(ax,f'Stop {s:,.2f} m',(s,y-.10),(s-100,y-.36),size=11,align='center',color=INK)
  ax.text((x+2*v+s)/2,y+.08,f'{v*v/(2*a):,.2f} m braking',ha='center',va='bottom',fontsize=11.2,color=INK)
  ax.text(70,y+.09,f'{x:.2f} m',ha='left',va='bottom',fontsize=9.5,color=COPPER)
  # True reserve boundary common to both; not a prediction band.
  ax.plot([L-150,L-150],[y-.13,y+.19],color=INK,lw=.8,ls=':')
 ax.text(0,2.48,'THRESHOLD',fontsize=10.5,color=SLATE)
 ax.text(L,2.48,'END OF LDA',ha='right',fontsize=10.5,color=SLATE)
 # The delay lengths are exact, listed once as part of the common grammar.
 for x,col,txt in [(0,COPPER,'Before touchdown'),(830,BLUE,'2 s delay'),(1500,INK,'Braking'),(2150,SAGE,'Remaining')]:
  ax.plot([x,x+70],[1.12,1.12],color=col,lw=4);ax.text(x+95,1.12,txt,va='center',fontsize=10.5)
 ax.text(0,.94,f'Delay travel: {2*u:.2f} m calm; {2*WR["touchdown_groundspeed_mps"]:.2f} m wind',fontsize=10.5,color=SLATE)
 ax.text(2910,-.39,'Dotted mark: 150 m reserve',ha='right',fontsize=10.2,color=SLATE)
 save(fig,'05_runway',['evidence/approximation/reference_formula.json','evidence/counterfactual/result.json'],
  'Shared-scale runway allocation for two separately optimized cases, not a causal wind effect',
  scale={'same_horizontal_metres_for_both':True,'LDA_m':L,'braking_deceleration_mps2':a,'delay_s':2},
  outcomes=[{'name':v[0],'touchdown_m':v[1],'delay_m':2*v[2],'braking_m':v[2]**2/(2*a),'stop_m':v[3],'remaining_m':L-v[3]} for v in vals])

def turning():
 fig=plt.figure(figsize=(7.1,5.7));ax=fig.add_axes([.02,.38,.47,.56]);bare(ax);ax.set(xlim=(-1.45,1.5),ylim=(-1.55,1.85),aspect='equal')
 ph=np.deg2rad(15);rot=np.array([[np.cos(ph),-np.sin(ph)],[np.sin(ph),np.cos(ph)]])
 # Front-view generic wing and fuselage, with bank perpendicular to lift.
 wing=np.array([[-1.12,0],[-.16,.045],[0,.10],[.16,.045],[1.12,0],[.16,-.045],[0,-.10],[-.16,-.045]])@rot.T
 ax.add_patch(Polygon(wing,fc=INK,ec='none'));ax.add_patch(Circle((0,0),.105,fc=INK,ec='white',lw=.5))
 lift=np.array([-np.sin(ph),np.cos(ph)])*1.35
 arrow(ax,(0,0),lift,COPPER,lw=2,head=13);arrow(ax,(0,0),(0,-float(lift[1])),INK,lw=1.5)
 arrow(ax,(0,0),(0,lift[1]),SAGE,lw=1.2);arrow(ax,(0,lift[1]),lift,BLUE,lw=1.2)
 ax.plot([-1.17,1.17],[0,0],ls=':',lw=.7,color=SLATE,zorder=0)
 ax.add_patch(Arc((0,0),1.35,1.35,theta1=0,theta2=15,ec=COPPER,lw=1))
 ax.text(.77,.13,'15° bank',fontsize=12,color=COPPER)
 ax.text(.12,1.00,'Vertical lift\nbalances weight',fontsize=11.4,color=SAGE)
 ax.text(-1.34,1.51,'Inward lift\nbends the motion',fontsize=11.4,color=BLUE)
 ax.text(-.53,.69,'Lift',rotation=15,color=COPPER,fontsize=12)
 ax.text(.12,-1.26,'Weight',fontsize=11.4)
 fig.text(.055,.95,'FRONT VIEW',fontsize=11.2,color=SLATE)
 # Circular-arc geometry: exact 47 degree central angle, metric radius.
 ap=fig.add_axes([.52,.40,.46,.52]);bare(ap);ap.set(xlim=(-.1,1.27),ylim=(-.17,1.23),aspect='equal')
 th=np.deg2rad(np.linspace(0,47,150));x=np.sin(th);y=np.cos(th)
 ap.plot(x,y,color=INK,lw=2.3)
 center=np.array([0,0]);ap.plot([0,0],[0,1],color=SLATE,lw=.7);ap.plot([center[0],x[-1]],[center[1],y[-1]],color=SLATE,lw=.7)
 ap.add_patch(Arc(center,.50,.50,theta1=43,theta2=90,ec=COPPER,lw=1.2));ap.text(.14,.27,'47°',color=COPPER,fontsize=17)
 arrow(ap,(-.02,1),(.24,1),BLUE,lw=1.1);arrow(ap,(x[-1]-.04*np.cos(th[-1]),y[-1]+.04*np.sin(th[-1])),(x[-1]+.18*np.cos(th[-1]),y[-1]-.18*np.sin(th[-1])),BLUE,lw=1.1)
 ap.text(.00,1.15,'PLAN VIEW',fontsize=11.2,color=SLATE)
 ap.text(-.015,.35,'R = 2.315 km',fontsize=11.2,rotation=90,ha='right')
 ap.text(.70,.08,'1.899 km of arc\n24.35 seconds',fontsize=12,ha='center')
 ap.text(.02,-.16,'78 m/s throughout',fontsize=11.3,color=SLATE)
 aq=fig.add_axes([.12,.105,.78,.22]);vv=np.linspace(55,95,200);rr=vv**2/(g*np.tan(ph))/1000
 aq.plot(vv,rr,color=INK,lw=1.8);r=78**2/(g*np.tan(ph))/1000;aq.scatter([78],[r],color=COPPER,s=24,zorder=4)
 aq.plot([78,78],[0,r],color=COPPER,lw=.7,ls=':');aq.text(79.5,r-.25,'78 m/s → 2.32 km',fontsize=11,color=COPPER)
 aq.set(xlim=(55,95),ylim=(1,3.6),yticks=[1,2,3],xticks=[55,65,78,95],xlabel='Airspeed (m/s)');aq.text(0,1.08,'Radius (km), at 15° bank',transform=aq.transAxes,fontsize=11.2,color=SLATE)
 save(fig,'03_turn',['evidence/approximation/reference_formula.json'],'Force balance, exact circular arc and quadratic radius dependence',g_mps2=g,speed_mps=78,bank_deg=15,radius_m=r*1000,arc_m=r*1000*np.deg2rad(47),turn_time_s=r*1000*np.deg2rad(47)/78,scope='Ideal coordinated level still-air turn; no roll transitions')

def wind_diagram():
 fig=plt.figure(figsize=(7.1,4.0));w=np.array(read('evidence/counterfactual/inputs.json')['wind_runway_mps'][:2])
 # Fixed screen mapping: runway x up, runway y right, identical arrows in both views.
 screen=lambda q:np.array([q[1],q[0]])
 for i,(name,theta) in enumerate([('ENTRY TRACK',-47),('RUNWAY ALIGNMENT',0)]):
  ax=fig.add_axes([.03+i*.50,.17,.45,.65]);bare(ax);ax.set(xlim=(-6,13),ylim=(-13,11),aspect='equal')
  r=np.deg2rad(theta);f=np.array([np.cos(r),np.sin(r)]);right=np.array([-np.sin(r),np.cos(r)]);fw=float(w@f);cw=float(w@right);p=fw*f;side=cw*right
  ax.plot(*np.array([screen(-12*f),screen(10*f)]).T,color=LIGHT,lw=5,zorder=0)
  arrow(ax,screen([0,0]),screen(9*f),INK,lw=1.4,head=11)
  arrow(ax,screen([0,0]),screen(w),COPPER,lw=2,head=14)
  arrow(ax,screen([0,0]),screen(p),BLUE,lw=1.3)
  arrow(ax,screen(p),screen(w),SAGE,lw=1.3)
  ax.scatter([0],[0],s=16,color=INK)
  ax.text(-5,10.3,name,fontsize=12,weight='bold')
  if i==0:
   ax.text(-5,-10.4,'Track −47° to runway',fontsize=12)
   label(ax,'Same wind',screen(w)*.6,(7,1.0),color=COPPER,size=11.3,align='center')
  else:
   ax.text(-5,-10.4,'Track 0° to runway',fontsize=12)
   label(ax,'Same wind',screen(w)*.6,(7,3.3),color=COPPER,size=11.3,align='center')
  fig.text(.04+i*.50,.10,f'Headwind {abs(fw):.3f} m/s',fontsize=12,color=BLUE)
  fig.text(.04+i*.50,.035,f'Rightward wind {cw:.3f} m/s',fontsize=12,color=SAGE)
 fig.text(.04,.94,'ONE WIND · TWO MOVING FRAMES',fontsize=13,weight='bold')
 fig.text(.04,.85,'From 070° true at 21 kt; arrows use a common velocity scale.',fontsize=11,color=SLATE)
 save(fig,'08_wind',['evidence/counterfactual/inputs.json'],'Identical wind decomposed along and right of two ground-track axes',runway_true_deg=133+10/60,wind_mps=w.tolist(),screen_mapping='runway-forward up, runway-right right; generic track arrows, not aircraft heading')

def verification():
 fig,ax=plt.subplots(figsize=(7.1,3.7));fig.subplots_adjust(left=.13,right=.96,top=.79,bottom=.20)
 x=np.linspace(0,1,1001);f=lambda t:(t-.5)**2-.04
 edges=np.linspace(0,1,9);bounds=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  low=0 if lo<=.5<=hi else min((lo-.5)**2,(hi-.5)**2);low-=.04;high=max(f(lo),f(hi));bounds.append([lo,hi,low,high]);col=COPPER if low<0 else BLUE
  ax.add_patch(Rectangle((lo,low),hi-lo,high-low,fc=col,ec=col,alpha=.13,lw=.8))
 ax.axhline(0,color=INK,lw=.9);ax.plot(x,f(x),color=INK,lw=1.7)
 samples=np.array([0,.2,.8,1]);ax.scatter(samples,f(samples),s=35,fc='white',ec=SAGE,lw=1.5,zorder=5)
 ax.text(.02,.025,'Required margin ≥ 0',fontsize=11.3,color=SLATE)
 label(ax,'Accepted samples',(.2,f(.2)),(.30,.185),size=11.5,color=SAGE)
 label(ax,'Violation between samples',(.5,-.04),(.56,-.10),size=11.5,color=COPPER,align='center')
 ax.set(xlim=(-.015,1.015),ylim=(-.12,.24),xticks=[0,.25,.5,.75,1],yticks=[0,.1,.2],xlabel='Normalized time',ylabel='Illustrative margin')
 fig.text(.065,.94,'THE SPACE BETWEEN THE SAMPLES',fontsize=13,weight='bold')
 fig.text(.065,.855,'Each shaded rectangle encloses every curve value in its interval.',fontsize=11.2,color=SLATE)
 save(fig,'09_certificate',[],'Pedagogical exact quadratic demonstrates missed between-sample violation',pedagogical_function='f(t)=(t-0.5)^2-0.04, t in [0,1]',not_landing_data=True,exact_enclosures=bounds,sample_times=samples.tolist())

def supplemental():
 fig=plt.figure(figsize=(7.1,6.4));ap=fig.add_axes([.04,.57,.92,.35]);bare(ap)
 ap.add_patch(Polygon(project([[0,-30.5,0],[L,-30.5,0],[L,30.5,0],[0,30.5,0]]),fc=LIGHT,ec=SLATE,lw=.6))
 for paths,col,sty in [(calm,INK,'-'),(wind,COPPER,'--')]:
  for t,q,v in paths:path(ap,q,color=col,lw=1.7,ls=sty)
 ap.set(xlim=(-2700,2850),ylim=(-650,1650),aspect='equal')
 fig.text(.07,.96,'TWO CONSTRUCTED LANDINGS',fontsize=13,weight='bold')
 fig.text(.07,.90,'Calm air —',color=INK,fontsize=12);fig.text(.37,.90,'Steady wind – –',color=COPPER,fontsize=12)
 fig.text(.07,.56,'Equal-scale local view; no geographic registration.',fontsize=11,color=SLATE)
 keys=[('Height (m)',lambda q,v:q[:,2]),('Vertical speed (m/s)',lambda q,v:v[:,2]),('Horizontal ground speed (kt)',lambda q,v:np.linalg.norm(v[:,:2],axis=1)/(1852/3600))]
 for j,(name,fun) in enumerate(keys):
  ax=fig.add_axes([.15,.39-j*.14,.77,.085])
  for paths,col,sty in [(calm,INK,'-'),(wind,COPPER,'--')]:
   for t,q,v in paths:ax.plot(t,fun(q,v),color=col,lw=1.2,ls=sty)
  ax.set(xlim=(0,46));ax.tick_params(labelsize=12);ax.text(.01,1.09,name,transform=ax.transAxes,va='bottom',fontsize=12,color=SLATE)
  if j==1:ax.axhline(0,color=SLATE,lw=.5,ls=':')
  if j<2:ax.tick_params(labelbottom=False)
  else:ax.set_xlabel('Time from each model entry (s)',fontsize=12)
 save(fig,'A1_paths',['evidence/approximation/reference_formula.json','evidence/counterfactual/formula.json'],'Both exact polynomial candidates and derived kinematic profiles; distinct scenario times',vertical_exaggeration=1,paths_evaluated=2)
 # Technical control curves deserve their own aligned strip chart, not six small boxes.
 d=[r for r in rows('evidence/counterfactual/path_controls.csv') if r['phase'] in ['approach','flare']];t=np.array([float(r['time_s']) for r in d])
 fig=plt.figure(figsize=(7.1,7.7));fig.text(.08,.965,'WIND-CONDITIONED CONTROL HISTORY',fontsize=13,weight='bold')
 fig.text(.08,.925,'Dashed rules: model limits. Vertical rule: approach–flare join.',fontsize=11,color=SLATE)
 items=[('eas_kt','Equivalent airspeed (kt)',(135,175),1),('bank_deg','Bank angle (°)',(-25,25),1),('roll_deg_s','Bank-angle rate (°/s)',(-5,5),1),('thrust_n','Thrust (kN)',(0,700),1000),('thrust_slew_n_s','Thrust slew (kN/s)',(-100,100),1000)]
 for j,(key,lab,limits,div) in enumerate(items):
  ax=fig.add_axes([.14,.75-j*.145,.78,.098]);v=np.array([float(r[key])/div for r in d]);ax.plot(t,v,color=COPPER,lw=1.4)
  for y in limits:ax.axhline(y,color=SLATE,lw=.6,ls=(0,(4,4)))
  ax.axvline(W['phases'][0]['duration_s'],color=SLATE,lw=.6,ls=':');ax.tick_params(labelsize=12);ax.set(xlim=(0,46),yticks=limits);span=limits[1]-limits[0];ax.set_ylim(limits[0]-.12*span,limits[1]+.12*span)
  ax.text(0,1.12,lab,transform=ax.transAxes,fontsize=12)
  if j<4:ax.tick_params(labelbottom=False)
  else:ax.set_xlabel('Time from model entry (s)',fontsize=12)
 save(fig,'A2_controls',['evidence/counterfactual/path_controls.csv','evidence/model/config.json'],'Aligned sampled control display for separately certified fixed wind candidate',bank_rate_frame='moving flight-path bank-angle rate, not generally body-axis roll rate')


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prototypes',action='store_true');args=ap.parse_args()
 landing();runway()
 if not args.prototypes:turning();wind_diagram();verification();supplemental()
if __name__=='__main__':main()
