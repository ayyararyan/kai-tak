from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'integrated';G=O/'geometry'
j=json.loads((G/'runway_crosscheck.json').read_text());c=json.loads((O/'conditions.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(11,4.8),gridspec_kw={'width_ratios':[1,1.1]});fig.patch.set_facecolor('#fbfaf6')
p=np.array(j['north_pick']['derived_EN_m']);q=np.array(j['back_projection']['threshold_EN_m']);origin=(p+q)/2
ax[0].plot([p[0]-origin[0],q[0]-origin[0]],[p[1]-origin[1],q[1]-origin[1]],'--',color='#af6b47')
for a,label,color,off in [(p,'North image: threshold bar','#425b69',(8,2)),(q,'South image + LDA back-projection','#916440',(8,-5))]:
 z=a-origin;ax[0].scatter(*z,s=60,color=color);ax[0].annotate(label,z,xytext=off,textcoords='offset points',fontsize=8)
ax[0].set(xlabel='East relative to comparison midpoint (m)',ylabel='North relative to comparison midpoint (m)',title=f'Threshold cross-check: {j["threshold_disagreement_m"]:.1f} m disagreement')
ax[0].set_aspect('equal');ax[0].set_xlim(-65,125);ax[0].set_ylim(-70,70);ax[0].grid(alpha=.16)
names=['Dry','Wet, no standing water','Standing water / slush'];limits=[25,22,10];value=c['cal605_mean_scenario_checks']['dry']['rightward_crosswind_kt']
ax[1].barh(names,limits,color=['#8d9f8f','#8d9f8f','#b9b5a7']);ax[1].axvline(abs(value),color='#a35237',lw=2,label=f'070° / 21 kt scenario: {abs(value):.2f} kt')
ax[1].invert_yaxis();ax[1].set(xlabel='Steady crosswind component (kt)',title='Published operator condition only');ax[1].legend(fontsize=8,loc='lower right');ax[1].grid(axis='x',alpha=.15)
fig.suptitle('Historical geometry is not yet a certified landing model',fontsize=14,x=.03,ha='left')
fig.text(.03,.02,'Left: unaccepted image fits; disagreement is not a hard error bound.  Right: chart-bearing scenario; passing does not establish landing feasibility.',fontsize=8)
fig.tight_layout(rect=(0,.08,1,.93));fig.savefig(O/'evidence_gates.png',dpi=160);fig.savefig(O/'evidence_gates.pdf');print('exported evidence_gates.png/pdf')
