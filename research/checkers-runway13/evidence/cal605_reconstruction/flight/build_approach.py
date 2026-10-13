#!/usr/bin/env python3
"""Coarse manual Figure1/2 approach samples, no UTC or A/B alignment."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from build_flight import ROOT,HERE,sha,axis,limits,writecsv

S1=ROOT/'data/kai-tak-2026-10-13/extracts/dfdr_figure1.png'
S2=ROOT/'data/kai-tak-2026-10-13/extracts/dfdr_figure2.png'
# Pixel anchors deliberately coarse. At sharp RA/pitch intersections the declared
# reading sensitivity is larger; original continuous gust peaks are NOT recovered.
X1=[962,1020,1078,1136,1194,1252,1310,1339]
X2=[997,1055,1113,1171,1229,1287,1316,1345,1374]
VARIABLES={
'groundspeed_kt':dict(fig=1,y0=1105,v0=0,y1=591,v1=250,dy=8,unit='kt',points=list(zip(X1,[852,848,837,844,828,791,771,769])),color='#168c94'),
'calibrated_airspeed_kt':dict(fig=1,y0=1105,v0=0,y1=591,v1=250,dy=12,unit='kt',points=list(zip(X1,[777,794,778,789,800,756,762,761])),color='#ba852d'),
'heading_degM':dict(fig=1,y0=1005,v0=0,y1=695,v1=270,dy=6,unit='degree magnetic',points=list(zip(X1,[905,905,905,900,871,857,855,852])),color='#8d5596'),
'barometric_altitude_ft':dict(fig=1,y0=1006,v0=0,y1=78,v1=1800,dy=15,unit='ft; barometric report altitude, not reconciled terrain datum',points=list(zip(X1,[580,612,660,721,827,884,940,955])),color='#ad5442'),
'radio_altitude_ft':dict(fig=1,y0=1005,v0=0,y1=80,v1=1800,dy=15,unit='ft radio height; not AMSL/clearance',points=list(zip(X1,[637,675,723,784,918,931,967,988])),color='#3b5d72'),
'fmc_wind_speed_kt':dict(fig=2,y0=1054,v0=0,y1=845,v1=100,dy=10,unit='kt; FMC-derived wind, not independent sensor',points=list(zip(X2,[956,981,964,953,1000,1024,1007,1005,1010])),color='#ad5442'),
'fmc_wind_direction_degT':dict(fig=2,y0=1004,v0=0,y1=799,v1=200,dy=8,unit='degree true; FMC-derived wind-from direction',points=list(zip(X2,[924,929,930,926,938,957,940,927,912])),color='#3b5d72'),
'drift_deg':dict(fig=2,y0=590,v0=0,y1=487,v1=20,dy=7,unit='degree; published signed drift, positive/negative semantics not inferred',points=list(zip(X2,[570,575,570,560,560,565,522,555,560])),color='#63865d')}
TIME={1:dict(p0=498,v0=0,p1=1541,v1=180),2:dict(p0=533,v0=0,p1=1577,v1=180)}

def main():
 rows=[]
 for name,c in VARIABLES.items():
  tx=TIME[c['fig']]
  for i,(x,y) in enumerate(c['points']):
   t=axis(x,tx['p0'],0,tx['p1'],180);tlo,thi=limits(x,4,tx['p0'],0,tx['p1'],180,4)
   v=axis(y,c['y0'],c['v0'],c['y1'],c['v1']);vlo,vhi=limits(y,c['dy'],c['y0'],c['v0'],c['y1'],c['v1'],4)
   rows.append(dict(variable=name,anchor_id=f'fig{c["fig"]}-{name}-{i:02d}',x_px=x,y_px=y,time_datum_A_s=round(t,3),time_lo_s=round(tlo,3),time_hi_s=round(thi,3),value=round(v,3),reading_lo=round(vlo,3),reading_hi=round(vhi,3),unit=c['unit'],construction='coarse manual pixel anchor; raster sensitivity only',source=f'CAD1/95 Appendix11 Figure{c["fig"]} PDFpage{150+c["fig"]}'))
 writecsv(HERE/'approach_anchor_readings.csv',rows)
 metadata={'sources':[dict(path=str(p.relative_to(ROOT)),sha256=sha(p),pixel_dimensions=list(Image.open(p).size)) for p in (S1,S2)],'time_calibration':TIME,'variables':VARIABLES,'anchor_halfwidth_x_px':4,'time_axis_calibration_halfwidth_px':4,'vertical_calibration_halfwidth_px':4,'uncertainty':'Declared pixel reading sensitivity, no statistical confidence; between-anchor excursions unresolved; source trace amplitudes may exceed sampled range. Figure1 and2 share printed arbitrary datumA. No exact A/B or UTC alignment asserted. Wind values are derived by FMC, not independent ground sensors.','anchors':rows}
 (HERE/'approach_anchors.json').write_text(json.dumps(metadata,indent=2)+'\n')
 for fi,p in [(1,S1),(2,S2)]:
  im=Image.open(p).convert('RGB');d=ImageDraw.Draw(im)
  for name,c in VARIABLES.items():
   if c['fig']!=fi:continue
   for x,y in c['points']:d.ellipse((x-5,y-5,x+5,y+5),outline=c['color'],width=2)
  im.save(HERE/f'figure{fi}_anchor_overlay.png')
 fig,axs=plt.subplots(4,1,figsize=(11,11),sharex=True,constrained_layout=True)
 for name,ai in [('groundspeed_kt',0),('calibrated_airspeed_kt',0),('barometric_altitude_ft',1),('radio_altitude_ft',1),('fmc_wind_speed_kt',2),('drift_deg',3)]:
  r=[a for a in rows if a['variable']==name];t=np.array([a['time_datum_A_s'] for a in r]);v=np.array([a['value'] for a in r]);lo=np.array([a['reading_lo'] for a in r]);hi=np.array([a['reading_hi'] for a in r])
  axs[ai].errorbar(t,v,xerr=[t-np.array([a['time_lo_s'] for a in r]),np.array([a['time_hi_s'] for a in r])-t],yerr=[v-lo,hi-v],fmt='o',markersize=4,capsize=2,color=VARIABLES[name]['color'],label=name.replace('_',' '))
 for a in axs:a.grid(alpha=.2);a.legend(fontsize=8)
 for a,label in zip(axs,['Speed (kt)','Published altitude (ft)','FMC wind speed (kt)','Published drift (°)']):a.set_ylabel(label)
 axs[-1].set_xlabel('Seconds from report arbitrary datum A, not UTC')
 fig.suptitle('CAL605 final-turn approach: coarse published-chart samples\nBars: declared raster-reading sensitivity only; unsampled gust excursions are not bounded',fontsize=12)
 fig.savefig(HERE/'approach_wind_samples.png',dpi=170)
 print(f'{len(rows)} approach/FMC anchors generated')
if __name__=='__main__':main()
