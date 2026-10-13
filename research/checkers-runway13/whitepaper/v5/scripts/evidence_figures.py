"""V5 historical-evidence graphics: original source readings, no new reconstruction.

All marks are read directly from the retained evidence. Short connecting lines
are eye guides, never newly inferred observations. Export metadata records the
source categories, plotted anchors, and assumptions behind derived quantities.
"""
from figure_style import *
from matplotlib.patches import Rectangle
import argparse

BASE = 'evidence/evidence/cal605_reconstruction/'
ANCHORS = BASE + 'flight/flight_anchor_readings.csv'
FLIGHT_SUMMARY = BASE + 'flight/flight_summary.json'
WIND = BASE + 'wind/wind_records.csv'
ANALYSIS = BASE + 'analysis.json'
WEATHER = 'evidence/weather_plot_data.csv'


def restrained_axes(ax, time_ticks=None):
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(axis='y', length=0, pad=5, labelsize=12)
    ax.tick_params(axis='x', length=3, color=SLATE, labelsize=12)
    if time_ticks is not None:
        for t in time_ticks:
            ax.axvline(t, color=GRID, lw=.55, zorder=0)
    ax.set_axisbelow(True)


def recorder():
    records = rows(ANCHORS)
    summary = read(FLIGHT_SUMMARY)
    lo, hi = summary['touchdown_flag_reading_range_s']
    tflag = summary['touchdown_flag_datum_B_s']
    fig = plt.figure(figsize=(7.1, 6.25))
    # Plot area leaves a dedicated label rail; all three strips share a time scale.
    specs = [(.67, .20, ['calibrated_airspeed_kt', 'groundspeed_kt'],
              'Speed (kt)', (0, 180), [0, 80, 160]),
             (.405, .185, ['radio_altitude_ft'],
              'Radio altitude (ft)', (-25, 205), [0, 100, 200]),
             (.145, .18, ['heading_degM'],
              'Heading (° magnetic)', (90, 146), [100, 120, 140])]
    colors = {'calibrated_airspeed_kt': INK, 'groundspeed_kt': COPPER,
              'radio_altitude_ft': INK, 'heading_degM': INK}
    series = {}
    axes = []
    for bottom, height, keys, heading, ylim, yticks in specs:
        ax = fig.add_axes([.105, bottom, .715, height])
        axes.append(ax)
        restrained_axes(ax, [0, 10, 20, 30, 40, 50, 60, 70])
        ax.axvspan(lo, hi, facecolor=SAGE, alpha=.19, zorder=.5)
        ax.axvline(tflag, color=SAGE, lw=.6, alpha=.7, zorder=.7)
        for key in keys:
            source = sorted((x for x in records if x['variable'] == key),
                            key=lambda x: float(x['time_datum_B_s']))
            t = np.array([float(x['time_datum_B_s']) for x in source])
            v = np.array([float(x['value']) for x in source])
            low = np.array([float(x['reading_lo']) for x in source])
            high = np.array([float(x['reading_hi']) for x in source])
            tlo = np.array([float(x['time_lo_s']) for x in source])
            thi = np.array([float(x['time_hi_s']) for x in source])
            if not (np.all(low <= v) and np.all(v <= high)
                    and np.all(tlo <= t) and np.all(t <= thi)):
                raise ValueError('A recorder anchor lies outside its reading range')
            ax.plot(t, v, lw=.65, color=colors[key], alpha=.65, zorder=2)
            ax.errorbar(t, v, xerr=[t-tlo, thi-t], yerr=[v-low, high-v],
                        fmt='o', markersize=2.9, markeredgewidth=.45,
                        markeredgecolor='white', color=colors[key],
                        elinewidth=.65, capsize=0, zorder=3)
            series[key] = {'count': len(source),
                           'anchor_ids': [x['anchor_id'] for x in source],
                           'time_datum_B_s': t.tolist(), 'value': v.tolist(),
                           'reading_lo': low.tolist(), 'reading_hi': high.tolist(),
                           'time_lo_s': tlo.tolist(), 'time_hi_s': thi.tolist()}
        ax.set(xlim=(-1, 71), ylim=ylim, yticks=yticks,
               xticks=[0, 10, 20, 30, 40, 50, 60, 70])
        ax.text(0, 1.12, heading, transform=ax.transAxes, fontsize=12.5,
                va='bottom', weight='bold')
        if keys[0] == 'calibrated_airspeed_kt':
            ax.annotate('Calibrated\nairspeed', (t[-1], series[keys[0]]['value'][-1]),
                        xytext=(73, 83), fontsize=12, color=INK,
                        va='center', annotation_clip=False,
                        arrowprops={'arrowstyle':'-', 'lw':.55, 'color':INK})
            ax.annotate('Ground\nspeed', (t[-1], series[keys[1]]['value'][-1]),
                        xytext=(73, 15), fontsize=12, color=COPPER,
                        va='center', annotation_clip=False,
                        arrowprops={'arrowstyle':'-', 'lw':.55, 'color':COPPER})
        if bottom > .2:
            ax.tick_params(axis='x', labelbottom=False)
        else:
            ax.set_xlabel('Time on the published flight plot, Datum B (s)',
                          labelpad=9, fontsize=12)
    # Place the indicator's description in unused upper air, with an exact-band leader.
    axes[0].annotate('First ground indication\n(reading range)',
                     xy=(tflag, 178), xytext=(43, 204),
                     fontsize=12, color=SAGE, ha='left', va='bottom',
                     annotation_clip=False,
                     arrowprops={'arrowstyle':'-', 'lw':.7, 'color':SAGE})
    fig.text(.105, .018, 'Markers: manual anchors    Bars: raster-reading sensitivity',
             fontsize=12, color=SLATE)
    if sum(s['count'] for s in series.values()) != 123:
        raise ValueError('Unexpected final-phase source anchor count')
    save(fig, '10_recorder', [ANCHORS, FLIGHT_SUMMARY],
         'Selected published CAL605 plot readings, with source reading sensitivity',
         evidence_category='manual digitization, not raw recorder data',
         plotted_series=series,
         first_ground_indication={'datum_B_s': tflag, 'reading_range_s':[lo, hi],
          'interpretation':'Declared raster-reading sensitivity, not exact physical touchdown time or sensor uncertainty'},
         connector_meaning='straight eye guides only; no resampling, smoothing, or new anchors',
         clocks='Datum B; offset to the ground-wind clock unidentified',
         radio_altitude_negative_values='retained; no clamping or geometric runway-height reinterpretation')


def weather():
    records = rows(WIND)
    fig = plt.figure(figsize=(7.1, 4.35))
    ax = fig.add_axes([.105, .24, .72, .61])
    restrained_axes(ax)
    for val in [10, 20, 30, 40]:
        ax.axhline(val, color=GRID, lw=.55, zorder=0)
    ax.axvline(8, color=SLATE, lw=.7, ls=(0,(2,3)), zorder=0)
    series = {}
    for sensor, title, color, marker in [('NW','Northwest',INK,'o'),
                                       ('LYM','Lei Yue Mun',COPPER,'D')]:
        source = sorted((r for r in records if r['sensor']==sensor and r['field']=='A'),
                        key=lambda r: float(r['seconds_since_wind_clock_033000']))
        t = np.array([float(r['seconds_since_wind_clock_033000'])/60 for r in source])
        v = np.array([float(r['speed_kt_printed']) for r in source])
        if len(source) != 15:
            raise ValueError('Expected all 15 irregular A-field readings for each sensor')
        ax.plot(t, v, color=color, lw=.8, alpha=.8, zorder=2)
        ax.scatter(t, v, s=22, color=color, marker=marker,
                   edgecolor='white', linewidth=.5, zorder=3)
        ax.annotate(title, (t[-1],v[-1]), xytext=(10.23,v[-1]),
                    fontsize=12.3, color=color, va='center', annotation_clip=False)
        j = int(np.flatnonzero(t==8)[0])
        ax.scatter(t[j], v[j], s=69, facecolor='white', edgecolor=color,
                   lw=1.15, marker=marker, zorder=4)
        ax.scatter(t[j], v[j], s=18, color=color, marker=marker, zorder=5)
        ax.annotate(f'{v[j]:.0f} kt', (t[j],v[j]),
                    xytext=(7.8, 43 if sensor=='LYM' else 5.9),
                    ha='right', fontsize=13, color=color,
                    arrowprops={'arrowstyle':'-', 'color':color, 'lw':.65})
        series[sensor] = {'clock_times':[r['wind_clock_time'] for r in source],
                          'minutes_after_033000':t.tolist(), 'speed_kt':v.tolist()}
    ax.set(xlim=(-.12, 10.15), ylim=(4, 45), yticks=[10,20,30,40],
           xticks=[0,2,4,6,8,10],
           xticklabels=['03:30','03:32','03:34','03:36','03:38','03:40'])
    ax.tick_params(axis='x', pad=7)
    ax.set_xlabel('Wind-system clock', fontsize=12, labelpad=10)
    fig.text(.105, .94, 'A-field wind speed (kt)', fontsize=12.5, weight='bold')
    fig.text(.105, .88, 'Maximum one-second speed in each five-second window',
             fontsize=12, color=SLATE)
    fig.text(.105, .045, 'Irregular printed observations; lines guide the eye.',
             fontsize=12, color=SLATE)
    save(fig, '11_weather', [WIND],
         'Two ground sensors on one irregularly sampled wind-system clock',
         evidence_category='source-transcribed ground-sensor printout',
         plotted_series=series,
         highlighted_clock_time='03:38:00', highlighted_speeds_kt={'NW':12,'LYM':37},
         field='A: maximum one-second speed within a five-second window',
         connector_meaning='eye guides, not recovered peaks between printouts',
         clocks='Wind-system clock only; no flight-event synchronization',
         aircraft_local_wind=False)


def rollout():
    source = read(ANALYSIS)['report_landmark_stopping_frontier']
    expected = [('touchdown',2300,160),('roll_restored',1365,139),
                ('autobrake_call',1080,133),('reverse_selected',880,129)]
    for r, (event, distance, speed) in zip(source, expected):
        if (r['event'],r['remaining_m'],r['speed_kt']) != (event,distance,speed):
            raise ValueError('Unexpected historical landmark order or value')
        v = r['speed_kt']*1852/3600
        for delay, key in [(0,'required_decel_no_delay_g'),(2,'required_decel_with_2s_delay_g')]:
            independent = v*v/(2*(r['remaining_m']-v*delay))/9.80665
            if abs(independent-r[key]) > 1e-13:
                raise ValueError('Historical landmark deceleration failed recomputation')
    fig = plt.figure(figsize=(7.1, 4.45))
    labels = fig.add_axes([.025,.20,.275,.61]);bare(labels)
    runway = fig.add_axes([.345,.20,.275,.61]);bare(runway)
    decel = fig.add_axes([.715,.20,.25,.61]);bare(decel)
    for ax in [labels,runway,decel]:ax.set_ylim(-.52,3.65)
    labels.set_xlim(0,1);runway.set_xlim(0,2450);decel.set_xlim(.135,.322)
    names = ['Touchdown','Roll\nrestored','Autobrake\ncall','Reverse\nselected']
    for i,(r,name) in enumerate(zip(source,names)):
        y=3-i
        labels.text(0,y,name,va='center',fontsize=12.2)
        labels.text(1,y,f'{r["speed_kt"]}',ha='right',va='center',fontsize=13,weight='bold')
        runway.add_patch(Rectangle((0,y-.10),r['remaining_m'],.20,
                                  fc=INK,ec='none',alpha=.88))
        runway.text(r['remaining_m'],y+.17,f'{r["remaining_m"]:,}',ha='right',
                    fontsize=12.2,va='bottom')
        runway.plot([0,2300],[y-.10,y-.10],color=GRID,lw=.6,zorder=0)
        x0=r['required_decel_no_delay_g'];x2=r['required_decel_with_2s_delay_g']
        decel.plot([x0,x2],[y,y],color=SLATE,lw=.8,zorder=1)
        decel.scatter([x0],[y],s=38,color=INK,zorder=3)
        decel.scatter([x2],[y],s=38,marker='D',color=COPPER,zorder=3)
        decel.text(x0,y-.28,f'{x0:.3f}',ha='right',va='top',fontsize=12,color=INK)
        decel.text(x2,y+.20,f'{x2:.3f}',ha='center',va='bottom',fontsize=12,color=COPPER)
    fig.text(.025,.905,'Report landmark',fontsize=12,weight='bold')
    fig.text(.30,.905,'Speed\n(kt)',ha='right',fontsize=12,weight='bold')
    fig.text(.345,.905,'Runway left\n(m)',fontsize=12,weight='bold')
    fig.text(.715,.905,'Required\ndeceleration (g)',fontsize=12,weight='bold')
    # A small direct key explains the two conditions without repeating each row.
    key=fig.add_axes([.025,.066,.94,.065]);bare(key);key.set(xlim=(0,1),ylim=(0,1))
    key.scatter([.025],[.5],s=38,color=INK)
    key.text(.06,.5,'No further delay',va='center',fontsize=12)
    key.scatter([.49],[.5],s=38,marker='D',color=COPPER)
    key.text(.525,.5,'Two more seconds',va='center',fontsize=12,color=COPPER)
    fig.text(.025,.015,'Constant deceleration needed to stop; not measured brake force.',
             fontsize=11.5,color=SLATE)
    save(fig,'12_rollout',[ANALYSIS],
         'Runway-distance and speed landmarks with conditional stopping requirements',
         evidence_category='report-stated rounded landmarks and conditional derived quantities',
         plotted_landmarks=source, speed_conversion_mps_per_kt=1852/3600,
         gravity_mps2=9.80665, additional_delay_cases_s=[0,2],
         formula='a_req/g = v^2 / [2(R-v*tau)g], R > v*tau',
         distance_scale='common linear metre scale for all four rows',
         event_axis='categorical rows in source narrative order; no time-spacing inference',
         connectors='within-row comparison of assumed delays only; no between-event trace')


def annual():
    records = rows(WEATHER)
    retained = [r for r in records if r['report_type']=='FM-15'
                and r['source_flag']=='4' and r['datetime_utc'][14:19]=='00:00'
                and r['wind_type']=='N' and r['wind_speed_mps']
                and r['wind_speed_mps_strict_qc_accepted']=='True'
                and r['partial_weather_row']=='False']
    v = np.sort([float(r['wind_speed_mps']) for r in retained])
    threshold=10.8
    counts={'lower':int((v<threshold).sum()),'tied':int((v==threshold).sum()),
            'higher':int((v>threshold).sum())}
    if len(v)!=8360 or counts!={'lower':8285,'tied':17,'higher':58}:
        raise ValueError('Annual subset selection or rank changed')
    # Unique values preserve exactly the empirical CDF while avoiding overplotted ties.
    unique, frequency=np.unique(v,return_counts=True)
    cumulative=np.cumsum(frequency)/len(v)*100
    fig=plt.figure(figsize=(7.1,4.65));ax=fig.add_axes([.115,.32,.79,.52])
    restrained_axes(ax)
    for y in [0,25,50,75,100]:ax.axhline(y,color=GRID,lw=.55,zorder=0)
    ax.step(np.r_[0,unique],np.r_[0,cumulative],where='post',color=INK,lw=1.5)
    ax.axvline(threshold,color=COPPER,lw=1,ls=(0,(3,3)))
    ax.scatter([threshold],[(counts['lower']+counts['tied'])/len(v)*100],
               color=COPPER,s=30,zorder=3)
    ax.annotate('10.8 m/s',xy=(threshold,99.3),xytext=(12.0,80),
                fontsize=12.5,color=COPPER,
                arrowprops={'arrowstyle':'-','lw':.65,'color':COPPER})
    ax.set(xlim=(0,21),ylim=(-2,104),xticks=[0,5,10,15,20],yticks=[0,25,50,75,100])
    ax.set_xlabel('Station wind speed (m/s)',fontsize=12,labelpad=8)
    ax.text(0,1.11,'Cumulative share of selected observations (%)',
            transform=ax.transAxes,fontsize=12.5,va='bottom')
    for x,big,small,col in [(.12,'8,285','below 10.8 m/s',INK),
                          (.44,'17','equal',SLATE),(.68,'58','above',COPPER)]:
        fig.text(x,.09,big,fontsize=17,color=col,weight='bold')
        fig.text(x,.035,small,fontsize=12,color=col)
    save(fig,'A3_weather_context',[WEATHER],
         '1993 station-wind empirical distribution in the declared routine subset',
         evidence_category='selected observed archive distribution, not return period or landing risk',
         source_records=len(records),selected_records=len(v),threshold_mps=threshold,
         threshold_counts=counts,empirical_cdf='right-continuous, no density smoothing',
         plotted_unique_values=unique.tolist(),plotted_frequencies=frequency.tolist(),
         selection={'report_type':'FM-15','source_flag':'4','minute_second':'00:00',
                    'wind_type':'N','strict_qc_accepted':True,'partial_weather_row':False})


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--only',choices=['recorder','weather','rollout','annual'])
    args=parser.parse_args()
    jobs={'recorder':recorder,'weather':weather,'rollout':rollout,'annual':annual}
    for key,job in jobs.items():
        if args.only is None or args.only==key:job()


if __name__=='__main__':main()
