#!/usr/bin/env python3
"""Reproduce coarse manual readings of CAD1/95 Appendix11 Figure4.
No inferred raw recorder samples, probabilistic CIs, or UTC registration.
"""
from pathlib import Path
import csv, json, hashlib, itertools
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE=ROOT/'research/checkers-runway13/evidence/cal605_reconstruction/source_pages/view_dfdr-154.png'
PDF=ROOT/'data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def limits(p,dp,p0,v0,p1,v1,dc):
 vals=[v0+(q-a)*(v1-v0)/(b-a) for q,a,b in itertools.product((p-dp,p+dp),(p0-dc,p0+dc),(p1-dc,p1+dc))]
 return min(vals),max(vals)
def axis(p,p0,v0,p1,v1):return v0+(p-p0)*(v1-v0)/(p1-p0)
def writecsv(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Every pair is manually read from the 1800x1228 source raster, not calculated
# from narrative values. Coarse spacing intentionally cannot capture all extrema.
DATA={
'groundspeed_kt':{'unit':'kt','y0':1156,'v0':0,'y1':647,'v1':250,'dy':8,'color':'#168c94','points':[
[568,891],[603,883],[638,875],[674,863],[712,850],[748,839],[784,834],[820,830],[856,826],[892,825],[928,823],[964,827],[1000,837],[1012,841],[1036,850],[1072,858],[1108,865],[1144,873],[1180,882],[1216,889],[1252,897],[1288,910],[1324,933],[1360,962],[1396,990],[1432,1018],[1468,1044],[1504,1066],[1540,1084],[1572,1099]]},
'calibrated_airspeed_kt':{'unit':'kt','y0':1156,'v0':0,'y1':647,'v1':250,'dy':8,'color':'#ba852d','points':[
[568,855],[603,858],[638,863],[674,852],[712,838],[748,811],[784,825],[820,814],[856,814],[892,811],[928,814],[964,820],[1000,811],[1012,827],[1036,814],[1072,842],[1108,852],[1144,857],[1180,871],[1216,843],[1252,874],[1288,886],[1324,889],[1360,941],[1396,972],[1432,1010],[1468,1036],[1504,1041],[1540,1060],[1572,1053]]},
'heading_degM':{'unit':'degree magnetic','y0':1105,'v0':50,'y1':902,'v1':150,'dy':4,'color':'#8d5596','points':[
[568,995],[603,979],[638,968],[674,963],[712,967],[748,951],[784,940],[820,953],[856,945],[892,950],[928,946],[964,940],[1000,940],[1012,942],[1036,946],[1072,940],[1108,939],[1144,932],[1180,933],[1216,935],[1252,942],[1288,948],[1324,947],[1360,936],[1396,942],[1432,934],[1468,930],[1504,955],[1540,985],[1572,1009]]},
'radio_altitude_ft':{'unit':'ft radio height; not AMSL or geometric clearance','y0':1055,'v0':0,'y1':136,'v1':180,'dy':5,'color':'#3b5d72','points':[
[584,185],[600,245],[612,287],[625,166],[638,136],[655,390],[669,382],[683,421],[697,431],[714,573],[727,362],[741,452],[754,412],[770,448],[788,483],[806,522],[825,578],[843,647],[862,710],[881,778],[900,869],[920,932],[941,974],[961,1008],[982,1057],[1002,1074],[1017,1083],[1031,1084],[1047,1094],[1119,1094],[1250,1094],[1450,1094],[1548,1093]]}}
TIME={'pixel0':566,'value0':0,'pixel1':1573,'value1':70,'calibration_halfwidth_px':3,'anchor_halfwidth_px':3,'unit':'seconds from arbitrary datum B'}
CAL_Y=3

def main():
 anchors=[]
 for name,c in DATA.items():
  for i,(x,y) in enumerate(c['points']):
   t=axis(x,566,0,1573,70);lo,hi=limits(x,3,566,0,1573,70,3)
   v=axis(y,c['y0'],c['v0'],c['y1'],c['v1']);vlo,vhi=limits(y,c['dy'],c['y0'],c['v0'],c['y1'],c['v1'],CAL_Y)
   anchors.append({'variable':name,'anchor_id':f'{name}-{i:02d}','x_px':x,'y_px':y,'time_datum_B_s':round(t,3),'time_lo_s':round(lo,3),'time_hi_s':round(hi,3),'value':round(v,3),'reading_lo':round(vlo,3),'reading_hi':round(vhi,3),'unit':c['unit'],'construction':'manual pixel anchor; bounded raster reading sensitivity only','source':'CAD Report1/95 PDF page154 Appendix11 Fig4'})
 meta={'source_pdf':str(PDF.relative_to(ROOT)),'source_pdf_sha256':sha(PDF),'source_raster':str(SOURCE.relative_to(ROOT)),'source_raster_sha256':sha(SOURCE),'raster_dimensions':[1800,1228],'source_figure':'Appendix11 Figure4 printed A11-5 PDFpage154','time_axis':TIME,'variables':DATA,'vertical_calibration_halfwidth_px':CAL_Y,'uncertainty':'Declared pixel sensitivity; no coverage probability, raw DFDR accuracy, source-chart distortion guarantee, or clock synchronization. Linear interpolation is a representation of these coarse anchors, not recovered recorder samples.','anchors':anchors}
 (HERE/'trace_anchors.json').write_text(json.dumps(meta,indent=2)+'\n')
 writecsv(HERE/'flight_anchor_readings.csv',anchors)
 # Piecewise interpolation envelope: candidate segments and interval times/values.
 # q=(t-t0)/(t1-t0), monotone decreasing in both endpoints within a segment;
 # endpoint extremes enclose all independent point-time shifts. Shared calibration
 # correlation is deliberately relaxed (conservative within declared anchor boxes).
 rows=[]
 for name in DATA:
  aa=[a for a in anchors if a['variable']==name]
  for t in range(int(np.ceil(aa[0]['time_hi_s'])),int(np.floor(aa[-1]['time_lo_s']))+1):
   candidates=[]
   for a,b in zip(aa[:-1],aa[1:]):
    if a['time_lo_s']<=t<=b['time_hi_s']:
     qmin=max(0.,min(1.,(t-a['time_hi_s'])/(b['time_hi_s']-a['time_hi_s'])))
     qmax=max(0.,min(1.,(t-a['time_lo_s'])/(b['time_lo_s']-a['time_lo_s'])))
     for q in (qmin,qmax):
      candidates.extend([(1-q)*a['reading_lo']+q*b['reading_lo'],(1-q)*a['reading_hi']+q*b['reading_hi']])
   value=np.interp(t,[a['time_datum_B_s'] for a in aa],[a['value'] for a in aa])
   rows.append({'variable':name,'time_datum_B_s':t,'value':round(float(value),3),'reading_lo':round(min(candidates),3),'reading_hi':round(max(candidates),3),'unit':DATA[name]['unit'],'construction':'piecewise-linear interpolation of coarse manual anchors, not independent observation','uncertainty':'pixel sensitivity only; not CI/PI'})
 writecsv(HERE/'flight_traces.csv',rows)
 # Plot digitization overlay; sampled anchors only, to expose omissions and mistakes.
 im=Image.open(SOURCE).convert('RGB');d=ImageDraw.Draw(im)
 for name,c in DATA.items():
  for x,y in c['points']:d.ellipse((x-4,y-4,x+4,y+4),outline=c['color'],width=2)
 d.line((1012,1107,1012,1148),fill='#d44444',width=3)
 for j,(name,c) in enumerate(DATA.items()):d.text((590,30+15*j),name,fill=c['color'])
 im.save(HERE/'source_anchor_overlay.png')
 fig,axs=plt.subplots(3,1,figsize=(11,10),sharex=True,constrained_layout=True)
 for name,axi in [('groundspeed_kt',0),('calibrated_airspeed_kt',0),('heading_degM',1),('radio_altitude_ft',2)]:
  rr=[r for r in rows if r['variable']==name];aa=[a for a in anchors if a['variable']==name];ax=axs[axi];c=DATA[name]['color']
  ax.plot([r['time_datum_B_s'] for r in rr],[r['value'] for r in rr],color=c,label=name.replace('_',' '))
  ax.fill_between([r['time_datum_B_s'] for r in rr],[r['reading_lo'] for r in rr],[r['reading_hi'] for r in rr],color=c,alpha=.16)
  ax.scatter([a['time_datum_B_s'] for a in aa],[a['value'] for a in aa],s=10,color=c)
 for ax in axs:
  ax.axvspan(*limits(1012,3,566,0,1573,70,3),color='#b64c43',alpha=.2,label='air/ground flag transition')
  ax.legend(loc='best',fontsize=8);ax.grid(alpha=.2)
 axs[0].set_ylabel('Speed (kt)');axs[1].set_ylabel('Heading (° magnetic)');axs[2].set_ylabel('Radio height (ft)');axs[2].set_xlabel('Seconds from report arbitrary datum B; not UTC')
 fig.suptitle('CAL605: coarse digitization of published final72-second plot\nShading is declared pixel-reading sensitivity, NOT a confidence/prediction interval',fontsize=12)
 fig.savefig(HERE/'final_approach_rollout.png',dpi=180);plt.close(fig)
 events=[
 {'event':'touchdown_air_ground_transition','time_datum_B_s':round(axis(1012,566,0,1573,70),3),'time_lo_s':round(limits(1012,3,566,0,1573,70,3)[0],3),'time_hi_s':round(limits(1012,3,566,0,1573,70,3)[1],3),'relative_touchdown_s':'','source':'Appendix11 Fig4 air/ground flag','category':'manual pixel reading','details':'First air-to-ground transition x=1012px; NOT radio-altitude zero crossing.'},
 {'event':'touchdown_narrative','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':0,'source':'Report section1.11.4 printed32','category':'report-stated','details':'About480m beyond threshold markers; GS160kt; CAS172 to161kt; heading131degM. No supplied statistical bounds.'},
 {'event':'sir_reverse_call','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':17,'source':'Report section1.11.4 printed33','category':'report-stated','details':'GS130kt; alternate section2.2.6 chronology says selection18s, GS129kt and880m remaining; not interchangeable events.'},
 {'event':'audible_reverse_selection_click','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':17.5,'source':'Report section1.11.4 printed33','category':'report-stated','details':'Half a second after call; speedbrake lever began rearward motion.'},
 {'event':'aggressive_deceleration','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':20,'source':'Report section1.11.4 printed33','category':'report-stated','details':'All reversers deployed; retardation generally exceeded0.3g.'},
 {'event':'left_turn_near_runway_end','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':'','source':'Report section1.11.4 printed33','category':'report-stated','details':'GS54kt; do not equate to later narrative tiller action at60kt.'},
 {'event':'reverse_speedbrake_cancel','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':'','source':'Report section1.11.4 printed33','category':'report-stated','details':'GS48kt, about6s before water impact.'},
 {'event':'water_impact','time_datum_B_s':'','time_lo_s':'','time_hi_s':'','relative_touchdown_s':'','source':'Report section1.11.4 printed33','category':'report-stated','details':'GS about30kt. A precise graph-to-water or graph-to-runway-end event alignment is not observed in Fig4.'}]
 writecsv(HERE/'flight_events.csv',events)
 # Conditional integral: measured time series is a distance diagnostic, not map truth.
 gs=[a for a in anchors if a['variable']=='groundspeed_kt'];t0=axis(1012,566,0,1573,70);t1=axis(1572,566,0,1573,70)
 ts=np.array([a['time_datum_B_s'] for a in gs]);vs=np.array([a['value'] for a in gs]);lo=np.array([a['reading_lo'] for a in gs]);hi=np.array([a['reading_hi'] for a in gs]);sel=ts>=t0-0.001
 distance=np.trapezoid(vs[sel],ts[sel])*1852/3600
 # Simplified pointwise hull adds horizontal sensitivity via global max slope;
 # end interval uncertainty adds maxGS times combined endpoint halfwidth.
 dt=max(max(abs(a['time_datum_B_s']-a['time_lo_s']),abs(a['time_hi_s']-a['time_datum_B_s'])) for a in gs)
 max_slope=max(abs(np.diff(vs)/np.diff(ts)));shift=dt*max_slope
 dlo=np.trapezoid(lo[sel]-shift,ts[sel])*1852/3600-max(vs)*2*dt*1852/3600
 dhi=np.trapezoid(hi[sel]+shift,ts[sel])*1852/3600+max(vs)*2*dt*1852/3600
 summary={'touchdown_flag_datum_B_s':t0,'touchdown_flag_reading_range_s':limits(1012,3,566,0,1573,70,3),'last_pre_terminal_speed_anchor_datum_B_s':t1,'last_pre_terminal_speed_anchor_kt':vs[-1],'flag_to_last_speed_anchor_s':t1-t0,'last_anchor_is_runway_end':False,'distance_integral_flag_to_last_anchor_m':float(distance),'distance_sensitivity_range_m':[float(dlo),float(dhi)],'distance_bound_scope':'Conservative independent anchor-box + max-slope horizontal shifts and endpoint buffer for piecewise-linear digitization ONLY; no chart transcription bias, raw DFDR physical error, or unknown curvature between anchors covered. NOT historical physical worst-case bounds.','anchor_count':len(anchors),'interpolated_row_count':len(rows),'omissions':['No precise UTC sync','No raw DFDR calibration errors','No continuous-time curve accuracy guarantee between coarse anchors','No AMSL from radio height','Whole-approach extraction limited to Figure1/2 A80–145sec in separate approach artifacts; not full three-minute coverage']}
 (HERE/'flight_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
