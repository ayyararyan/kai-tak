"""Independent audit of actual V5 plotted coordinates; masters constructed in memory.

Only qa/science_figure_semantics.json is written. No optimization or publication
figure generation occurs; every figure save function is replaced by capture.
"""
from pathlib import Path
import sys,json,hashlib,datetime,csv
import numpy as np
P=Path(__file__).resolve().parents[1]
if sys.flags.optimize:raise SystemExit('Use ordinary Python, not -O.')
sys.path.insert(0,str(P/'scripts'))
import mechanics_figures as m, historical_figures as h, evidence_figures as e
checks=[]
def check(name,val):
 if not val:raise AssertionError(name)
 checks.append(name)
figures={}
def capture(fig,name,inputs,meaning,**meta):figures[name]=(fig,meta)
for mod in [m,h,e]:mod.save=capture
# All plots are constructed in memory; no published figure/evidence files are written.
for fn in [m.landing,m.runway,m.turning,m.wind_diagram,m.verification,m.supplemental,h.place,h.bearings,h.stereo,h.maps,e.recorder,e.weather,e.rollout,e.annual]:fn()
check('fifteen_figure_masters',len(figures)==15)
# Front-view bank and plan-view signed curvature agree for a right turn.
f=figures['03_turn'][0];a=f.axes[0];arr=[p for p in a.patches if hasattr(p,'_posA_posB')]
lift=np.array(arr[0]._posA_posB[1]);weight=np.array(arr[1]._posA_posB[1]);vertical=np.array(arr[2]._posA_posB[1])
check('vertical_lift_balances_weight',np.allclose(vertical,-weight))
check('lift_tilt_is_fifteen_degrees',abs(np.rad2deg(np.arctan2(-lift[0],lift[1]))-15)<1e-12)
x,y=f.axes[1].lines[0].get_data();dt=np.diff(np.c_[x,y],axis=0)
check('plan_turn_is_clockwise',np.all(dt[:-1,0]*dt[1:,1]-dt[:-1,1]*dt[1:,0]<0))
check('plan_arc_angle_47',abs(np.rad2deg(np.arctan2(x[-1],y[-1]))-47)<1e-12)
check('plan_arc_unit_radius',np.allclose(x*x+y*y,1))
for ax in figures['08_wind'][0].axes:
 arrows=[p for p in ax.patches if hasattr(p,'_posA_posB')]
 actual=np.array(arrows[1]._posA_posB[1]);p=np.array(arrows[2]._posA_posB[1]);start,end=map(np.array,arrows[3]._posA_posB)
 check('wind_common_screen_vector',np.allclose(actual,[9.64006667211232,-4.876589552990943]))
 check('wind_projection_tip_to_tail',np.allclose(start,p) and np.allclose(end,actual) and abs(np.dot(p,actual-p))<1e-10)
 check('rightward_wind_not_from_right',any('Rightward wind' in t.get_text() for t in figures['08_wind'][0].texts))
# Every illustrated quadratic enclosure contains both endpoint extrema and interior minimum.
f=figures['09_certificate'][0];ax=f.axes[0]
for rect in ax.patches:
 lo=rect.get_x();hi=lo+rect.get_width();cand=np.array([lo,hi]+([.5] if lo<=.5<=hi else []));v=(cand-.5)**2-.04
 check('pedagogical_interval_full_extrema',abs(rect.get_y()-v.min())<1e-14 and abs(rect.get_y()+rect.get_height()-v.max())<1e-14)
check('pedagogical_samples_positive',np.all(ax.collections[0].get_offsets()[:,1]>0))
check('pedagogical_interior_negative',figures['09_certificate'][1]['not_landing_data'] is True and -.04<0)
f=figures['A1_paths'][0]
for line,(_,q,v) in zip(f.axes[3].lines,[*m.calm,*m.wind]):
 check('A1_horizontal_groundspeed',np.allclose(line.get_ydata(),np.hypot(v[:,0],v[:,1])/(1852/3600)))
check('A1_two_scenario_height_profiles',len(f.axes[1].lines)==4)
expected=[(135,175),(-25,25),(-5,5),(0,700),(-100,100)]
for ax,limits in zip(figures['A2_controls'][0].axes,expected):
 check('A2_frozen_limit_rules',all(np.all(np.array(line.get_ydata())==lim) for line,lim in zip(ax.lines[1:3],limits)))
# Camera keeps positive vertical up and has no vertical exaggeration.
u,d=h.project(np.eye(3));basis=np.vstack([u.T,d]);check('stereo_camera_orthonormal',np.allclose(basis@basis.T,np.eye(3)))
check('stereo_camera_up_positive',u[2,1]>0 and d[2]>0)
check('stereo_roofs_outside_hull_label',any('outside the control hull' in t.get_text() for t in figures['07_stereo'][0].texts))
meta=figures['10_recorder'][1];check('recorder_all_123_original_anchors',sum(x['count'] for x in meta['plotted_series'].values())==123)
check('recorder_negative_radio_height_retained',min(meta['plotted_series']['radio_altitude_ft']['value'])<0)
check('ground_indication_reading_not_exact_touchdown','not exact physical touchdown' in meta['first_ground_indication']['interpretation'])
meta=figures['11_weather'][1];check('weather_full_two_A_field_series',all(len(s['speed_kt'])==15 for s in meta['plotted_series'].values()))
check('weather_unaligned_clock','no flight-event synchronization' in meta['clocks'])
meta=figures['12_rollout'][1];check('four_categorical_rollout_landmarks',len(meta['plotted_landmarks'])==4 and 'categorical' in meta['event_axis'])
meta=figures['A3_weather_context'][1];check('annual_counts',meta['threshold_counts']==dict(lower=8285,tied=17,higher=58))
check('annual_no_tail_clipped',max(meta['plotted_unique_values'])<=figures['A3_weather_context'][0].axes[0].get_xlim()[1])
check('annual_ecdf_total',sum(meta['plotted_frequencies'])==8360)
# PDF master records bind each source and generated PDF, not only filenames.
for name in figures:
 r=json.loads((P/'qa/figure-records'/f'{name}.json').read_text())
 check(name+'_generated_pdf_hash',hashlib.sha256((P/'figures'/f'{name}.pdf').read_bytes()).hexdigest()==r['pdf_sha256'])
 check(name+'_all_declared_input_hashes',all(hashlib.sha256((P/i['path']).read_bytes()).hexdigest()==i['sha256'] for i in r['inputs']))
receipt=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_passed=len(checks),checks=checks,figures=list(figures),method='Read source; instantiate all masters in memory with output capture; inspect actual plotted coordinates/metadata against independent geometry and frozen inputs',mutated_evidence_or_figure_outputs=False,source_sha256={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'scripts/mechanics_figures.py',P/'scripts/historical_figures.py',P/'scripts/evidence_figures.py']})
(P/'qa/science_figure_semantics.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(len(checks),'figure semantic checks passed for',len(figures),'masters')
