#!/usr/bin/env python3
"""Six source-grounded vector figures; default build uses portable exported data.

python make_figures.py                 # no repository imports or optimization
python make_figures.py --refresh-data  # read bundled frozen proof/evaluator sources

Grayscale V5 palette; Arial/STIX labels, open axes and vector-first export retained.
No installable font is copied or bundled. Numerical curves are illustrations,
not certificates. All proof values and accepted cells are exported unchanged.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_FLOOR
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyArrowPatch, PathPatch
from matplotlib.path import Path as MPath

P = Path(__file__).resolve().parent
FIG = P / "figures"
DATA = P / "inputs/figure_data.json"
WIDTH = 373.2 / 72.27  # exact manuscript text measure, expressed in inches
# Author-requested grayscale: round(0.2126 R + 0.7152 G + 0.0722 B)
# for each original V5 RGB colour. Geometry, labels, data and alpha are unchanged.
INK = "#393939"
SLATE = "#737373"
COPPER = "#6C6C6C"
SAGE = "#7C7C7C"
PALE = "#F1F1F1"
LIGHT = "#E0E0E0"
GRID = "#DADADA"
BLUE = "#737373"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def configure():
    # V5 uses Arial. A free fallback keeps source packages buildable on Linux.
    # Font availability and the selected name are written into the figure manifest.
    try:
        font_manager.findfont("Arial", fallback_to_default=False)
        chosen = "Arial"
    except ValueError:
        try:
            font_manager.findfont("Liberation Sans", fallback_to_default=False)
            chosen = "Liberation Sans"
        except ValueError:
            chosen = "DejaVu Sans"
    plt.rcParams.update({
        "font.family": chosen, "font.size": 8.8,
        "axes.labelsize": 8.8, "xtick.labelsize": 8, "ytick.labelsize": 8,
        "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": SLATE,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": .55, "xtick.major.width": .55, "ytick.major.width": .55,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "svg.hashsalt": "kaitak-mathematical-note-v1",
        "savefig.facecolor": "white", "figure.facecolor": "white",
        "mathtext.fontset": "stix", "axes.unicode_minus": True,
    })
    return chosen


def refresh_data():
    frozen = P / "frozen-source/research/checkers-runway13"
    source = frozen / "integrated/assumption_solution"
    sys.path.insert(0, str(source))
    from conditional_model import Case
    from forces import phase

    cert_file = P / "inputs/local_certificate.json"
    branch_file = P / "inputs/active_branch.json"
    conditions_file = P / "verification/condition-values.json"
    cert = json.loads(cert_file.read_text())
    branch = json.loads(branch_file.read_text())["baseline"]
    conditions = json.loads(conditions_file.read_text())
    assert len(conditions) == 10 and len({r["name"] for r in conditions}) == 10
    assert cert["root"]["certified"] and cert["path"]["certified"]
    q = list(branch["q"])
    root = cert["root"]["center"]
    for i, k, scale in [(1, 0, 5), (2, 1, 300), (3, 2, 75),
                         (10, 3, 1), (11, 4, 1)]:
        q[i] = float(Decimal(root[k]) * scale)
    case = Case()
    approach, flare = case.curves(q)
    events = {"slew": float(root[6]), "load_upper": float(root[7]),
              "thrust_lower": float(root[8])}
    s = np.unique(np.r_[np.linspace(0, 1, 2001), list(events.values())])
    f = phase(flare, q[1], s, case.p)
    margins = {"slew": 1 - np.abs(f["slew"]) / 100000,
               "load_upper": (1.4 - f["load"]) / .9,
               "thrust_lower": f["thrust"] / 700000}
    input_paths = [cert_file, branch_file, conditions_file,
                   source / "conditional_model.py", source / "forces.py",
                   frozen / "model/trajectory.py", frozen / "model/config.json"]
    out = {
        "schema": "kai-tak-note-figures-v1",
        "source_commit": "78a9ce1c627f917c94306af5529d5e9ebeb743e8",
        "input_sha256": {str(v.relative_to(P)): sha(v) for v in input_paths},
        "quantity_status": {
            "curves": "binary64 evaluations at numerical root-box centre; not proof samples",
            "events": "rounded plotting values of root-box centre coordinates",
            "cover": "unaltered accepted cells from sealed whole-path certificate",
            "condition_margins": "individual continuous feasibility lower bounds for secondary paths",
            "landing_and_certificate": "explicitly conceptual diagrams, not geometric projections",
        },
        "root_center_scaled_decimal": root,
        "root_scaled_radius_decimal": cert["root"]["radius"],
        "q_plot": q,
        "wind_mps": case.p["wind_mps"],
        "eta_local_center_decimal": root[5],
        "family_lower_decimal": "0.15236076430186170190",
        "family_upper_decimal": "0.181970215",
        "retention_tolerance_decimal": "0.0001",
        "events_s": events,
        "events_elapsed_seconds": {k: v * q[1] for k, v in events.items()},
        "events_x_m": {k: float(flare[0](v)) for k, v in events.items()},
        "flare": {"s": s.tolist(), "elapsed_s": (s * q[1]).tolist(),
                  "margins": {k: v.tolist() for k, v in margins.items()}},
        "zones": cert["event_attempts"][0]["zones"],
        "cover": cert["path"]["cover"],
        "accepted_cells_by_phase": [sum(r[0] == ph for r in cert["path"]["cover"])
                                     for ph in [0, 1]],
        "processed_cells": cert["path"]["processed"],
        "conditions": conditions,
        "unresolved_conditions": ["Tailwind 5 kt", "Urban 60 m", "Urban 65 m"],
    }
    assert out["accepted_cells_by_phase"] == [32, 366]
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")


def arrow(ax, start, end, color=INK, lw=.8, head=7, style="-|>"):
    patch = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=head,
                            linewidth=lw, color=color, shrinkA=1.5, shrinkB=1.5)
    ax.add_patch(patch)
    return patch


def save(fig, name, meaning):
    FIG.mkdir(parents=True, exist_ok=True)
    # Fixed canvas: not bbox_inches=tight, which silently changes figure size.
    fig.savefig(FIG / f"{name}.pdf", metadata={"CreationDate": None, "ModDate": None,
                "Title": meaning, "Author": "Aryan Ayyar"})
    fig.savefig(FIG / f"{name}.svg", metadata={"Date": None, "Title": meaning,
                "Creator": "Kai Tak mathematical note: reproducible scientific figures"})
    fig.savefig(FIG / f"{name}.png", dpi=240)
    size = list(fig.get_size_inches())
    plt.close(fig)
    return {"figure": name, "meaning": meaning, "master_inches": size,
            "input": "inputs/figure_data.json", "input_sha256": sha(DATA),
            "outputs": {ext: sha(FIG / f"{name}.{ext}") for ext in ["pdf", "svg", "png"]}}


def landing(d):
    fig, ax = plt.subplots(figsize=(WIDTH, 3.03))
    fig.subplots_adjust(left=.06, right=.98, bottom=.04, top=.97)
    ax.set(xlim=(0, 10), ylim=(0, 5)); ax.axis("off")
    ax.text(.0, 4.84, "One path, two flight phases, one ideal reset", fontsize=10.5,
            fontweight="bold", va="top")
    # Conceptual side elevation. The drawing explicitly does not use metric scale.
    x0, gate, touch, coast, stop = .55, 4.35, 6.2, 7.3, 9.4
    floor, offset = 1.57, .27
    vertices = [(x0, 4.1), (1.6, 3.6), (3.1, 2.9), (gate, 2.50),
                (5.0, 2.24), (5.3, floor+offset), (touch, floor+offset)]
    codes = [MPath.MOVETO] + [MPath.CURVE4] * 6
    ax.add_patch(PathPatch(MPath(vertices, codes), fill=False, edgecolor=BLUE, lw=1.65))
    ax.add_patch(PathPatch(MPath([(x,y-offset) for x,y in vertices], codes),
                          fill=False, edgecolor=SLATE, lw=.9, linestyle=(0,(3,2))))
    ax.plot([touch, stop], [floor+offset]*2, color=BLUE, lw=1.4)
    ax.plot([gate-.45, 9.75], [floor]*2, color=INK, lw=1)
    ax.plot([touch,stop],[floor]*2,color=SLATE,lw=.8,ls=(0,(3,2)))
    for x,y in [(x0,4.1),(gate,2.5),(touch,floor+offset),(stop,floor+offset)]:
        ax.plot(x,y,"o",ms=3.6,color=BLUE)
    ax.plot(touch,floor,"o",ms=3,color=INK)
    ax.plot([touch,touch],[floor,floor+offset],color=INK,lw=.8)
    ax.plot([touch-.1,touch+.1],[floor,floor],color=INK,lw=1.4)
    for x in [gate,touch,coast,stop]:
        ax.plot([x,x],[.63,1.39],color=GRID,lw=.7)
    ax.annotate("CG path  $R$",xy=(2.1,3.4),xytext=(1.7,4.26),fontsize=9,
                arrowprops=dict(arrowstyle="-",color=BLUE,lw=.7),color=BLUE)
    ax.annotate("Virtual reference  $r$",xy=(3.25,2.65),xytext=(1.15,2.40),fontsize=9,
                arrowprops=dict(arrowstyle="-",color=SLATE,lw=.7),color=SLATE)
    ax.text(7.24,3.38,"Contact",ha="center",fontweight="bold",fontsize=9)
    ax.text(7.24,2.99,r"$\dot z:\;-0.7\;\longmapsto\;0$",ha="center",fontsize=10)
    ax.text(7.24,2.63,"CG stays 6 m above runway",ha="center",fontsize=8.5)
    arrow(ax,(6.76,2.39),(touch+.04,floor+.11),SLATE,lw=.7)
    ax.text(gate,2.87,"Gate",ha="center",fontsize=8.4)
    ax.text(stop,2.04,"Stop",ha="center",fontsize=8.4)
    for l,r,name,detail,color in [(.55,gate,"Approach","turn and descent",BLUE),
                                 (gate,touch,"Flare","straight track",COPPER),
                                 (touch,coast,"Delay","2 s",SAGE),
                                 (coast,stop,"Braking",r"$a_b=0.15g$",SLATE)]:
        ax.plot([l+.06,r-.06],[1.12,1.12],lw=2.6,color=color)
        ax.text((l+r)/2,.88,name,ha="center",fontsize=9,fontweight="bold",color=color)
        ax.text((l+r)/2,.54,detail,ha="center",fontsize=8.1,color=SLATE)
    arrow(ax,(.54,1.7),(.54,2.16),INK)
    arrow(ax,(.54,1.7),(1.15,1.7),INK)
    ax.text(.36,2.19,"h",fontsize=8.5);ax.text(1.19,1.66,"x",fontsize=8.5)
    ax.text(.0,.1,"Schematic, not to scale.  y is runway-right, out of this side view.",
            fontsize=8,color=SLATE)
    return save(fig,"landing","Conceptual hybrid landing and inertial CG/reference distinction")


def active(d):
    fig,ax=plt.subplots(figsize=(WIDTH,3.03))
    fig.subplots_adjust(left=.33,right=.96,bottom=.19,top=.80)
    eta=float(d["eta_local_center_decimal"])
    s=d["events_s"]
    rows=[("Stopping (hybrid)",1.,INK,"D"),("Gate slew",0.,BLUE,"o"),
          ("Touchdown slew",1.,BLUE,"o"),("Interior slew",s["slew"],BLUE,"o"),
          ("Upper load",s["load_upper"],COPPER,"o"),
          ("Lower thrust",s["thrust_lower"],SAGE,"o")]
    for i,(label,x,color,marker) in enumerate(rows):
        y=5-i
        ax.hlines(y,0,1,color=GRID,lw=.8)
        ax.plot(x,y,marker,color=color,ms=5.2,clip_on=False)
        text="terminal equation" if i==0 else f"s = {x:.4f}"
        if x>.8: tx,ha=x-.04,"right"
        else: tx,ha=x+.045,"left"
        ax.text(tx,y+.16,text,color=color,fontsize=7.8,ha=ha,va="bottom")
    ax.set_yticks(range(6),[r[0] for r in rows[::-1]])
    ax.tick_params(axis="y",length=0,pad=9)
    ax.spines[["left","right","top"]].set_visible(False)
    ax.set(xlim=(0,1),ylim=(-.43,5.52),xlabel="Normalized flare time  s")
    ax.set_xticks([0,.25,.5,.75,1])
    fig.text(.025,.975,"Five flare variables · six equal active margins",fontsize=10.4,
             fontweight="bold",va="top")
    fig.text(.025,.917,r"$\eta_{\rm loc}\simeq$ "+f"{eta:.10f}"+
             f"   ·   Flare duration {d['q_plot'][1]:.4f} s",fontsize=8.7,color=SLATE,va="top")
    return save(fig,"active","Six active constraints and separate normalized-time event locations")


def certificate(d):
    fig,ax=plt.subplots(figsize=(WIDTH,3.66))
    fig.subplots_adjust(left=.035,right=.985,bottom=.03,top=.99)
    ax.set(xlim=(0,10),ylim=(0,7));ax.axis("off")
    def box(x,y,w,h,title,lines,color):
        ax.add_patch(Rectangle((x,y),w,h,facecolor="white",edgecolor=color,lw=.9))
        ax.plot([x,x+w],[y+h,y+h],color=color,lw=2)
        ax.text(x+w/2,y+h-.34,title,ha="center",va="center",fontsize=9.5,
                fontweight="bold",color=color)
        ax.text(x+w/2,y+h-.76,lines,ha="center",va="top",fontsize=8.5,
                linespacing=1.35,color=INK)
    box(2.1,5.23,5.8,1.54,r"Unique root $F(\zeta^*)=0$",
        "Krawczyk inclusion · nine equations\n"+r"Scaled root box, radius $10^{-20}$",BLUE)
    box(.13,2.8,4.6,1.7,"Active-gradient sufficiency",
        r"Six gradients in $\mathbb{R}^5$ · $\lambda_i>0$"+"\nNonsingular augmented matrix",COPPER)
    box(5.24,2.8,4.6,1.7,"Whole-time feasibility",
        "398 accepted cells · event bounds\nGeometry and exact ground law",SAGE)
    arrow(ax,(3.65,5.23),(2.45,4.49),BLUE)
    arrow(ax,(6.35,5.23),(7.55,4.49),BLUE)
    box(1.1,.92,7.8,1.3,"Strict local primary optimum",
        "Five flare variables; the connected path attains its value",INK)
    arrow(ax,(2.45,2.8),(3.6,2.23),COPPER)
    arrow(ax,(7.55,2.8),(6.4,2.23),SAGE)
    ax.text(5,.52,"Necessary flare constraints transfer the bound to 12 parameters",
            ha="center",fontsize=8.4)
    ax.text(5,.15,"Full-family conclusion: non-strict local optimality, not uniqueness",
            ha="center",fontsize=8.4,color=SLATE)
    return save(fig,"certificate","Logical implications in the certificate; no high-dimensional geometric projection")


def continuous(d):
    fig=plt.figure(figsize=(WIDTH,4.45))
    gs=fig.add_gridspec(5,1,height_ratios=[1,1,1,.22,.22],
                        left=.14,right=.965,bottom=.12,top=.92,hspace=.38)
    s=np.asarray(d["flare"]["s"]);eta=float(d["eta_local_center_decimal"])
    keys=[("slew","Thrust-slew margin",BLUE),
          ("load_upper","Upper-load margin",COPPER),
          ("thrust_lower","Lower-thrust margin",SAGE)]
    for i,(key,label,col) in enumerate(keys):
        ax=fig.add_subplot(gs[i])
        vals=np.asarray(d["flare"]["margins"][key])
        for zone in d["zones"]:
            if zone["key"]==key:ax.axvspan(zone["left"],zone["right"],color=col,alpha=.14,lw=0)
        ax.plot(s,vals,color=col,lw=1.15)
        ax.axhline(eta,color=INK,lw=.7,ls=(0,(3,2)))
        ev=[d["events_s"][key]]+([0,1] if key=="slew" else [])
        ax.plot(ev,[eta]*len(ev),"o",ms=3.3,color=col,clip_on=False)
        ax.text(.015,.87,label,transform=ax.transAxes,va="top",fontsize=8.5,color=col,
                bbox=dict(facecolor="white",alpha=.9,edgecolor="none",pad=1.5))
        if i==0:
            ax.text(.985,eta+.035,r"$\eta_{\rm loc}$",ha="right",fontsize=8.7,color=INK)
        ax.set_xlim(0,1);ax.set_ylim(eta-.06,max(vals)*1.065)
        ax.tick_params(axis="x",labelbottom=False,length=2)
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(3))
        ax.grid(axis="y",color=GRID,lw=.35,alpha=.65)
    for i,ph in enumerate([0,1]):
        ax=fig.add_subplot(gs[3+i]); rows=[r for r in d["cover"]if r[0]==ph]
        for j,(_,a,b,depth,omitted) in enumerate(rows):
            ax.add_patch(Rectangle((a,0),b-a,1,facecolor=LIGHT if j%2==0 else PALE,
                                   edgecolor=SLATE,linewidth=.13))
        ax.set(xlim=(0,1),ylim=(0,1));ax.set_yticks([])
        ax.spines[["left","top","right"]].set_visible(False)
        ax.text(-.018,.5,("Approach\n32 cells" if ph==0 else "Flare\n366 cells"),
                transform=ax.transAxes,ha="right",va="center",fontsize=7.2,color=SLATE)
        if ph==0:ax.tick_params(axis="x",bottom=False,labelbottom=False)
        else:
            ax.set_xticks([0,.25,.5,.75,1])
            ax.set_xlabel("Normalized phase time  s",fontsize=8.5)
    fig.text(.026,.988,"Critical margins and complete time coverage",fontsize=10.4,
             fontweight="bold",va="top")
    fig.text(.026,.948,"Curves: numerical centre. Shading: certified event-proof neighborhoods.",
             fontsize=8,color=SLATE,va="top")
    return save(fig,"continuous","Numerical critical margins plus all 398 accepted time cells and event zones")


def bracket(d):
    lower=float(d["family_lower_decimal"]);upper=float(d["family_upper_decimal"])
    fig=plt.figure(figsize=(WIDTH,2.75))
    ax=fig.add_axes([.12,.55,.81,.19])
    ax.axvspan(lower,upper,color=PALE,zorder=0)
    ax.plot([lower,upper],[0,0],color=SLATE,lw=2)
    ax.plot(lower,0,"o",color=SAGE,ms=6)
    ax.plot(upper,0,"|",color=COPPER,ms=16,mew=1.5)
    ax.set(xlim=(.145,.19),ylim=(-.75,.75));ax.set_yticks([])
    ax.spines[["left","right","top"]].set_visible(False)
    ax.set_xticks([.15,.16,.17,.18,.19]);ax.tick_params(labelsize=8)
    ax.text(lower,.87,"Certified feasible\n0.1523607643",ha="left",fontsize=8.4,
            color=SAGE,clip_on=False,linespacing=1.3)
    ax.text(upper,.87,"Family exclusion\n0.181970215",ha="right",fontsize=8.4,
            color=COPPER,clip_on=False,linespacing=1.3)
    ax.text((lower+upper)/2,-.40,r"$\eta^*_{\mathcal{P}}$ remains unidentified",ha="center",
            fontsize=8.6,color=INK)
    fig.text(.025,.975,"The global-family gap is still open",fontsize=10.4,
             fontweight="bold",va="top")
    gap=Decimal(d["family_upper_decimal"])-Decimal(d["family_lower_decimal"])
    fig.text(.12,.41,"Bracket width  "+f"{float(gap):.8f}",fontsize=8.6,color=SLATE)
    inset=fig.add_axes([.25,.16,.54,.115])
    inset.annotate("",xy=(3e-5,0),xytext=(-1e-4,0),
                   arrowprops=dict(arrowstyle="-|>",lw=1.8,color=BLUE,
                                   shrinkA=0,shrinkB=0,mutation_scale=9))
    inset.plot(-1e-4,0,"|",ms=10,color=BLUE)
    inset.set(xlim=(-1.15e-4,3.5e-5),ylim=(-.5,.5));inset.set_yticks([])
    inset.set_xticks([-1e-4,0],[r"$-10^{-4}$","0"])
    inset.spines[["top","right","left","bottom"]].set_visible(False)
    inset.tick_params(axis="x",length=0,pad=3)
    inset.set_title(r"Retention guarantee: $\eta_S-\eta_{\rm loc}\geq-10^{-4}$",fontsize=8.6,
                    color=BLUE,pad=4)
    fig.text(.52,.028,"Separate scale; no upper endpoint is asserted.",ha="center",fontsize=8,
             color=SLATE)
    return save(fig,"bracket","Global family bracket, with one-sided retention lower bound on a separate scale")


def conditions(d):
    order=["mean","headwind10","calm","tailwind2","tailwind3",
           "urban45","urban50","urban55","urban58","buffer15"]
    lookup={r["name"]:r for r in d["conditions"]}
    labels=["Baseline wind","Headwind 10 kt","Calm","Tailwind 2 kt","Tailwind 3 kt",
            "Urban 45 m","Urban 50 m","Urban 55 m","Urban 58 m","Buffer 15 m"]
    positions=[11,10,9,8,7,5,4,3,2,1]
    fig,ax=plt.subplots(figsize=(WIDTH,4.2))
    fig.subplots_adjust(left=.285,right=.89,bottom=.23,top=.88)
    for i,(name,y) in enumerate(zip(order,positions)):
        val=lookup[name]["eta_certified"];x=float(val)
        color=INK if name=="mean" else BLUE if i<5 else SAGE
        ax.barh(y,x,height=.5,color=color,alpha=.86)
        display=Decimal(val).quantize(Decimal(".000001"),rounding=ROUND_FLOOR)
        ax.text(x+.004,y,str(display),ha="left",va="center",fontsize=7.8,color=color)
    ax.set_yticks(positions,labels);ax.tick_params(axis="y",length=0,pad=6)
    ax.set(xlim=(0,.183),ylim=(.2,11.8))
    ax.set_xticks([0,.05,.10,.15]);ax.set_xticklabels(["0","0.05","0.10","0.15"])
    ax.spines[["left","right","top"]].set_visible(False)
    ax.set_axisbelow(True);ax.grid(axis="x",color=GRID,lw=.4)
    ax.text(0,6.05,"Geometry changes at baseline wind",fontsize=8,color=SLATE)
    ax.set_xlabel("Certified primary lower bound",fontsize=8.6,labelpad=5)
    fig.text(.025,.975,"Ten individually certified secondary paths",fontsize=10.4,
             fontweight="bold",va="top")
    fig.text(.025,.929,"Separate constructions; bars do not define a feasibility frontier.",
             fontsize=8.1,color=SLATE,va="top")
    fig.text(.025,.107,"UNRESOLVED",fontsize=7.5,fontweight="bold",color=COPPER)
    fig.text(.025,.057,"Tailwind 5 kt  ·  Urban 60 m  ·  Urban 65 m",fontsize=8.8,color=INK)
    return save(fig,"conditions","Ten individually certified secondary-path margins; unresolved cases have no invented bars")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-data",action="store_true")
    args=parser.parse_args()
    if args.refresh_data:refresh_data()
    if not DATA.is_file():raise SystemExit("Missing inputs/figure_data.json; use --refresh-data with bundled proof sources.")
    d=json.loads(DATA.read_text())
    assert d["schema"]=="kai-tak-note-figures-v1"
    selected_font=configure()
    records=[f(d)for f in [landing,active,certificate,continuous,bracket,conditions]]
    manifest={"figure_count":6,"formats":["pdf","svg","png"],
              "font_family":selected_font,"v5_palette_preserved":False,
              "grayscale":True,
              "palette_conversion":"round(0.2126 R + 0.7152 G + 0.0722 B), equal RGB channels",
              "fixed_text_width_tex_pt":373.2,"records":records}
    (FIG/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Generated six figures in PDF, SVG and PNG from portable inputs/figure_data.json.")


if __name__=="__main__":
    main()
