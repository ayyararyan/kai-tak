"""Reproduce CAL605 Figure 5 digitization and conditional stopping diagnostics.

Only digitization-coordinate uncertainty is enclosed; no physical or population CI.
Primary source CAD Report 1/95. No frozen model/configuration changes.
"""
from pathlib import Path
import csv, hashlib, itertools, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
WORKSPACE = PROJECT.parents[1]
KNOT = 1852 / 3600
G = 9.80665

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(path, rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def axis_value(p, p0, p1, v0, v1):
    if p0 == p1: raise ValueError('Degenerate pixel axis')
    return v0+(p-p0)*(v1-v0)/(p1-p0)
def axis_range(p, p0, p1, v0, v1, pe, ae):
    """Exact corner enclosure of affine axis map with uncertain pixel anchors.
    Denominator never changes sign; derivative w.r.t each coordinate has constant
    sign when other coordinates are held fixed, so extrema occur at box corners.
    """
    if abs(p1-p0)<=2*ae: raise ValueError('Overlapping calibration anchors')
    vals=[axis_value(a,b,c,v0,v1) for a,b,c in itertools.product(
        (p-pe,p+pe),(p0-ae,p0+ae),(p1-ae,p1+ae))]
    return min(vals),max(vals)
def stop_remaining(L, x, v, delay, a):
    if not all(math.isfinite(q) for q in [L,x,v,delay,a]) or v<0 or delay<0 or a<=0:
        raise ValueError('Invalid stopping inputs')
    return L-x-v*delay-v*v/(2*a)
def required_deceleration(v, remaining, delay=0):
    if not all(math.isfinite(q) for q in (v,remaining,delay)) or v<0 or remaining<=0 or delay<0:raise ValueError('Invalid state')
    usable=remaining-v*delay
    return math.inf if usable<=0 else v*v/(2*usable)

def segment_time(distance, v0, v1):
    """Exact integral dx/v for positive linearly interpolated speed in position."""
    if not all(math.isfinite(q) for q in (distance,v0,v1)) or distance<0 or min(v0,v1)<=0:
        raise ValueError('Invalid reconstruction segment')
    z=(v1-v0)/v0
    return distance/v0 if z==0 else distance/v0*math.log1p(z)/z

def segment_position(t, x0, x1, v0, v1):
    if not all(math.isfinite(q) for q in (x0,x1)) or x1<=x0: raise ValueError('Invalid segment coordinates')
    duration=segment_time(x1-x0,v0,v1)
    if not math.isfinite(t) or t<0 or t>duration+1e-10: raise ValueError('Outside segment')
    m=(v1-v0)/(x1-x0)
    return x0+v0*t if m==0 else x0+v0*math.expm1(m*t)/m

def build_explicit_rollout(rows):
    segments=[];elapsed=0.;lo=0.;hi=0.
    for i,(left,right) in enumerate(zip(rows,rows[1:])):
        x0=left['distance_from_end_m'];x1=right['distance_from_end_m']
        v0=left['groundspeed_kt']*KNOT;v1=right['groundspeed_kt']*KNOT
        dt=segment_time(x1-x0,v0,v1)
        dlow=max(0,left['remaining_reading_low_m']-right['remaining_reading_high_m'])
        dhigh=left['remaining_reading_high_m']-right['remaining_reading_low_m']
        dtlo=segment_time(dlow,left['speed_reading_high_kt']*KNOT,right['speed_reading_high_kt']*KNOT)
        dthi=segment_time(dhigh,left['speed_reading_low_kt']*KNOT,right['speed_reading_low_kt']*KNOT)
        segments.append(dict(segment=i+1,start_elapsed_s=elapsed,duration_s=dt,x0_m=x0,x1_m=x1,
            v0_mps=v0,v1_mps=v1,speed_position_slope_per_s=(v1-v0)/(x1-x0),
            duration_reading_low_s=dtlo,duration_reading_high_s=dthi))
        elapsed+=dt;lo+=dtlo;hi+=dthi
    out=dict(method='piecewise linear speed in runway coordinate, inverted analytically',
       formula='x(t)=x0+v0*expm1(m*(t-t0))/m; v(t)=v0*exp(m*(t-t0)); constant-speed branch when m=0',
       time_origin='first digitized Figure5 anchor, BEFORE touchdown; not datum A/B/UTC',
       duration_s=elapsed,duration_reading_box_low_s=lo,duration_reading_box_high_s=hi,
       uncertainty='conservative coordinate-and-speed-box enclosure CONDITIONAL on piecewise-linear interpolation and runway-parallel motion; not physical error/CI',
       domain='only retained graph span; no extrapolation to stopping or outside source; late turn not represented',segments=segments)
    (ROOT/'explicit_rollout.json').write_text(json.dumps(out,indent=2)+'\n')
    samples=[]
    for seg in segments:
        for tau in np.linspace(0,seg['duration_s'],5):
            samples.append(dict(time_since_first_anchor_s=seg['start_elapsed_s']+tau,
                distance_from_runway_end_m=segment_position(tau,seg['x0_m'],seg['x1_m'],seg['v0_mps'],seg['v1_mps']),
                ground_speed_mps=seg['v0_mps']*math.exp(seg['speed_position_slope_per_s']*tau),
                segment=seg['segment'],category='analytical interpolation, not new observation'))
    write_csv(ROOT/'explicit_rollout_samples.csv',samples)
    return out

def main():
    anchors=json.loads((ROOT/'trace_anchors.json').read_text())
    imfile=ROOT/anchors['image']
    primary=WORKSPACE/'data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf'
    if sha(imfile)!=anchors['image_sha256'] or sha(primary)!=anchors['primary_pdf_sha256']:
        raise ValueError('Source identity changed; recalibration required')
    comparator=json.loads((PROJECT/'approximation/reference_outcomes.json').read_text())
    for name in ('model/config.json','model/trajectory.py'):
        if sha(PROJECT/name)!=comparator['source_sha256'][name]:
            raise ValueError('Frozen model changed; comparison must be revalidated')
    rows=[]
    xa=anchors['x_axis']; ya=anchors['y_axis']; errs=anchors['reading_sensitivity_pixels']
    for i,(x,y) in enumerate(anchors['groundspeed_xy']):
        d=axis_value(x,xa['pixel_0'],xa['pixel_1'],xa['value_0'],xa['value_1'])
        dlow,dhigh=axis_range(x,xa['pixel_0'],xa['pixel_1'],xa['value_0'],xa['value_1'],errs['x'],errs['calibration'])
        v=axis_value(y,ya['pixel_0'],ya['pixel_1'],ya['value_0'],ya['value_1'])
        vl,vh=axis_range(y,ya['pixel_0'],ya['pixel_1'],ya['value_0'],ya['value_1'],errs['y'],errs['calibration'])
        rem=-d;rl=-dhigh;rh=-dlow
        row=dict(anchor_id=i+1,pixel_x=x,pixel_y=y,distance_from_end_m=d,
                 remaining_m=rem,remaining_reading_low_m=rl,remaining_reading_high_m=rh,
                 groundspeed_kt=v,speed_reading_low_kt=vl,speed_reading_high_kt=vh,
                 source_pdf_page=anchors['source_pdf_page'],source_figure=anchors['source_figure'],source_method='manual_pixel_anchor',
                 required_constant_decel_g=(v*KNOT)**2/(2*rem*G) if rem>0 else None,
                 required_decel_reading_low_g=(vl*KNOT)**2/(2*rh*G) if rh>0 else None,
                 required_decel_reading_high_g=(vh*KNOT)**2/(2*rl*G) if rl>0 else None,
                 required_decel_reading_high_status='finite' if rl>0 else 'unbounded_as_remaining_approaches_zero',
                 required_decel_domain='remaining>0; coordinate reading interval may include runway end')
        rows.append(row)
    write_csv(ROOT/'rollout_trace.csv',rows)
    explicit_rollout=build_explicit_rollout(rows)
    # Source overlay remains visibly a reading of the published graph.
    im=Image.open(imfile).convert('RGB'); draw=ImageDraw.Draw(im)
    for i,(x,y) in enumerate(anchors['groundspeed_xy']):
        draw.ellipse((x-4,y-4,x+4,y+4),outline='#0057b7',width=2)
        if i%3==0: draw.text((x-8,y-20),str(i+1),fill='#0057b7')
    im.save(ROOT/'source_pages/rollout_overlay.png')
    rem=np.array([r['remaining_m'] for r in rows]);speed=np.array([r['groundspeed_kt'] for r in rows])
    # Chronology obtained from speed-distance graph, not joined to unknown wind UTC.
    # Straight-line interpolation of speed in runway coordinate; final turning path
    # makes ds/v a lower estimate of elapsed time, not an exact inertial replay.
    distance=-rem
    chronology=[]
    for R in [2300,1365,1080,880,800,750,350,120,70,15]:
        v=float(np.interp(-R,distance,speed))
        xx=np.linspace(-2300,-R,max(2,int(2300-R)+1))
        vv=np.interp(xx,distance,speed)*KNOT
        elapsed=float(np.trapezoid(1/vv,xx))
        chronology.append(dict(remaining_m=R,interpolated_speed_kt=v,
            elapsed_from_R2300_straight_track_s=elapsed,
            required_no_delay_decel_g=required_deceleration(v*KNOT,R)/G,
            note='linear interpolation of digitized graph; R2300 origin is narrative approximate; not synchronized DFDR time'))
    write_csv(ROOT/'rollout_diagnostics.csv',chronology)
    ref=json.loads((PROJECT/'approximation/reference_outcomes.json').read_text())['nominal']
    a=0.15*G; L=2786; hist_x=480; hist_v=160*KNOT
    scenarios=[]
    for name,x,v in [('synthetic_reference',ref['touchdown_x_m'],ref['touchdown_speed_mps']),
                     ('later_touchdown_only',hist_x,ref['touchdown_speed_mps']),
                     ('higher_speed_only',ref['touchdown_x_m'],hist_v),
                     ('historical_touchdown_inputs',hist_x,hist_v)]:
        scenarios.append(dict(case=name,touchdown_x_m=x,touchdown_speed_kt=v/KNOT,
            delay_s=2,deceleration_g=.15,remaining_m=stop_remaining(L,x,v,2,a),
            category='conditional fixed-braking formula; not a historical simulation'))
    delayed=[dict(delay_s=d,remaining_m=stop_remaining(L,hist_x,hist_v,d,a)) for d in [0,1,2,5,10,20]]
    # Report-stated landmarks, not graph-derived assumptions.
    landmarks=[('touchdown',2300,160),('roll_restored',1365,139),
               ('autobrake_call',1080,133),('reverse_selected',880,129)]
    frontier=[]
    for name,R,vkt in landmarks:
        v=vkt*KNOT
        frontier.append(dict(event=name,remaining_m=R,speed_kt=vkt,
            required_decel_no_delay_g=required_deceleration(v,R)/G,
            required_decel_with_2s_delay_g=required_deceleration(v,R,2)/G,
            max_delay_at_0p3g_s=R/v-v/(2*.3*G),source='CAD narrative §§2.2.5–2.2.7'))
    autobrake=[dict(setting=k,reported_rollout_m=d,remaining_using_2300m_m=2300-d)
               for k,d in [(2,2350),(3,2100),(4,1720)]]
    analysis=dict(status='exploratory historical benchmark; no operational certificate',
       explicit_reconstruction=dict(segments=len(explicit_rollout['segments']),formula_file='explicit_rollout.json',
          scope='analytic reconstruction of digitized speed-distance graph under stated interpolation; not an optimal landing formula'),
       fixed_formula=scenarios, historical_input_delay_sensitivity=delayed,
       decomposition_m=dict(later_touchdown=480-ref['touchdown_x_m'],
           higher_speed_at_fixed_delay=2*(hist_v-ref['touchdown_speed_mps'])+(hist_v**2-ref['touchdown_speed_mps']**2)/(2*a)),
       report_landmark_stopping_frontier=frontier,report_autobrake_distances=autobrake,
       late_phase=dict(appendix13_20s_checkpoint=dict(runway_remaining_m=800,speed_kt=127,runway_consumed_fraction_relative_narrative2300=(2300-800)/2300,kinetic_energy_fraction_constant_mass=(127/160)**2,source_pdf_page=159,scope='source-stated rounded checkpoint; constant-mass energy ratio, not full mechanics'), remaining_2300_to_750_fraction_consumed=(2300-750)/2300,
         speed_at_750_kt=float(np.interp(-750,distance,speed)),
         apparent_no_delay_required_g=required_deceleration(float(np.interp(-750,distance,speed))*KNOT,750)/G),
       uncertainty=dict(type='pixel-reading sensitivity bounds only',coverage_probability=None,
          calibration_pixel_error=errs['calibration'],manual_x_pixel_error=errs['x'],manual_y_pixel_error=errs['y'],figure_band='vertical speed sensitivity only; horizontal bounds are in rollout_trace.csv',
          physical_sensor_error=None,plot_position_integration_error=None,clock_offset_to_wind=None,
          explanation='Axis/raster intervals are not calibrated physical error bars or CIs. Derived stop counterfactuals use rounded source point values without invented physical ranges.'),
       comparison_limits=['Historical and synthetic entry/controls/environment differ; no like-for-like path superiority claim.',
         'Ground distance in Figure5 is derived, not independent raw GPS; reference point/datum uncertainty unquantified.',
         'Final yaw means runway-coordinate distance differs from along-path distance; no late-turn exact dynamics inference.',
         'Source narrative touchdown ~2300m remaining differs from plotted air/ground transition ~2210m; preserve both, do not force-align.',
         'Report Appendix13 rounds some events (e.g. reverse at900m) differently from narrative (880m).',
         'Constant braking formula is diagnostic; actual autobrake/spoiler/reverse/braking state changes are not represented.'])
    (ROOT/'analysis.json').write_text(json.dumps(analysis,indent=2,allow_nan=False)+'\n')
    write_csv(ROOT/'conditional_stopping_cases.csv',scenarios)
    # Compact scientific diagnostic figure.
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf7','axes.facecolor':'#fbfaf7'})
    fig,ax=plt.subplots(1,2,figsize=(12,4.6))
    aa=ax[0]; aa.plot(rem,speed,color='#3e555c',lw=2,label='Published speed–distance trace')
    aa.fill_between(rem,[r['speed_reading_low_kt'] for r in rows],[r['speed_reading_high_kt'] for r in rows],color='#3e555c',alpha=.15,label='Vertical reading sensitivity only')
    R=np.linspace(1,2300,300)
    for ag,c in [(.15,'#a66e45'),(.3,'#6d7c58')]:aa.plot(R,np.sqrt(2*ag*G*R)/KNOT,'--',color=c,label=f'No-delay stop boundary: {ag:g}g')
    aa.axvline(750,color='#80534a',ls=':',lw=1);aa.text(770,190,'Strong braking\n~750 m remaining',ha='right',va='top',fontsize=9)
    aa.set(xlim=(2350,0),ylim=(0,210),xlabel='Runway remaining (m; derived report coordinate)',ylabel='Ground speed (kt)',title='Speed fell, but stopping room fell faster')
    aa.legend(loc='lower left',fontsize=8,frameon=False)
    bb=ax[1];labels=['Reference','Later touchdown','Higher speed','Both historical\ntouchdown inputs']
    vals=[r['remaining_m'] for r in scenarios]; bb.bar(range(4),vals,color=['#6d7c58','#8c9880','#a66e45','#80534a'],width=.65)
    bb.axhline(0,color='#333333',lw=.8);bb.axhline(150,color='#8b8b8b',ls=':',label='Model reserve:150 m')
    for i,v in enumerate(vals):bb.text(i,v+(9 if v>=0 else -10),f'{v:.0f} m',ha='center',va='bottom' if v>=0 else 'top')
    bb.set_xticks(range(4),labels,fontsize=8);bb.set(ylabel='Runway remaining at calculated stop (m)',title='Same 2 s delay and 0.15g braking formula',ylim=(-210,310));bb.legend(fontsize=8,frameon=False)
    fig.suptitle('CAL605 reconstruction benchmark • conditional calculations, not a landing recommendation',fontsize=12)
    fig.tight_layout();fig.savefig(ROOT/'findings.png',dpi=180);fig.savefig(ROOT/'findings.pdf');plt.close(fig)
    # Don't overwrite the shared project ledger from this script.
    manifest={str(p.relative_to(WORKSPACE)):sha(p) for p in [
        WORKSPACE/'data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf',
        WORKSPACE/'data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605.txt',
        PROJECT/'model/config.json',PROJECT/'model/trajectory.py',
        PROJECT/'approximation/reference_outcomes.json',imfile,ROOT/'trace_anchors.json']}
    (ROOT/'manifest.json').write_text(json.dumps(dict(source_sha256=manifest,scope='sources and read-only frozen comparator; hashes not physical validation'),indent=2)+'\n')
    print(json.dumps({'anchors':len(rows),'scenarios':scenarios,'frontier':frontier},indent=2))
if __name__=='__main__':main()
