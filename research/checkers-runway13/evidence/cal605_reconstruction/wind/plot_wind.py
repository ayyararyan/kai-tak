from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def plot(root=ROOT):
    root=Path(root)
    with (root/'wind_records.csv').open() as f:
        rows=list(csv.DictReader(f))
    fig,axes=plt.subplots(5,1,figsize=(10,10),sharex=True,sharey=True)
    colors={'A':'#b56b47','B':'#647e69','C':'#536779'}
    labels={'A':'A: 5-sec max 1-sec','B':'B: 2-min mean','C':'C: 10-min mean'}
    for sensor,ax in zip(['SE','NW','MID','LYM','YYC'],axes):
        for field in ['A','B','C']:
            data=[r for r in rows if r['sensor']==sensor and r['field']==field and r['speed_kt_printed'] not in ('', None)]
            ax.scatter([int(r['seconds_since_wind_clock_033000'])/60 for r in data],
              [int(r['speed_kt_printed']) for r in data],label=labels[field],s=22,
              color=colors[field],marker={'A':'o','B':'s','C':'x'}[field])
        ax.set_ylabel(sensor+'\nknots');ax.grid(alpha=.18);ax.set_ylim(0,45)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,ncol=3,loc='upper center',bbox_to_anchor=(.5,.954),fontsize=9)
    axes[-1].set_xticks(list(range(11)),[f'03:{30+i:02}:00' for i in range(11)],rotation=35,ha='right')
    axes[-1].set_xlabel('Printed wind-system clock (UTC label; alignment to flight clock unresolved)')
    fig.suptitle('CAL605: surface wind depends on location and averaging window',fontsize=14)
    missing_speed=sum(r['speed_kt_printed'] in ('',None) for r in rows)
    fig.text(.1,.018,f'Actual printed records only; no temporal interpolation. Rolling means overlap. Missing speeds omitted: {missing_speed}.\nSource: CAD Report 1/95, Appendix 7, PDF pages 138–139. Display precision is not instrument uncertainty.',fontsize=9)
    fig.tight_layout(rect=(0,.055,1,.915))
    fig.savefig(root/'wind_windows.png',dpi=180)
    fig.savefig(root/'wind_windows.pdf')
    plt.close(fig)

if __name__=='__main__':
    plot()
