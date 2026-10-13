"""Budgeted interval exclusion over the entire flare parameter box.

An unexcluded box is UNKNOWN, not feasible. Completes a global upper certificate
only if every box is excluded. Time/budget exhaustion explicitly means failure.
"""
import json,time,heapq
from pathlib import Path
from mpmath import iv
from certify_candidate import I,Z,coefficients,enclose,tr,lo,velocity

def excludes(m,eta):
    # Feasibility lower bounds cannot be used as exclusion upper bounds.
    return any(v.b<eta.a for key,v in m.items() if key!='corridor')

def endpoint_kinematics(T,x,u,fx,fz,s):
    vg=velocity('15.24',0);vend=[u,Z,-I('.7')]
    delta=[x,Z,-I('15.24')];bump=[fx,Z,fz]
    if s==0:
        j=[(60*d-36*T*v-24*T*w+384*b)/T**3 for d,v,w,b in zip(delta,vg,vend,bump)]
        return [Z,Z,I('15.24')],vg,[Z,Z,Z],j
    j=[(60*d-24*T*v-36*T*w-384*b)/T**3 for d,v,w,b in zip(delta,vg,vend,bump)]
    return [x,Z,Z],vend,[Z,Z,Z],j

def run(eta='.10',budget=1500,initial_frontier=None):
    eta=I(eta);cfg=tr.load_config();ref=tr.Evaluator(cfg).reference_tree
    # Full v1 flare box, without restricting to a neighborhood of the candidate.
    root=[(4.,12.),(200.,700.),(69.,88.),(-50.,50.),(-10.,10.)]
    scales=[8,500,19,100,20]
    queue=[(-max((d-c)/scale for (c,d),scale in zip(box,scales)),i,box)
           for i,box in enumerate(initial_frontier if initial_frontier is not None else [root])]
    heapq.heapify(queue);counter=len(queue);processed=0;pruned=0;start=time.monotonic()
    while queue and processed<budget:
        _,_,box=heapq.heappop(queue);processed+=1
        if processed%5000==0:print(json.dumps({'processed':processed,'frontier':len(queue),'excluded':pruned}),flush=True)
        T,x,u,fx,fz=[iv.mpf([a,b]) for a,b in box]
        terminal=[(x-200)/500,(700-x)/500,(2636-x-2*u-u**2/(2*I('1.4709975')))/2636,
                  (iv.sqrt(u**2+I('.7')**2)/(I(1852)/3600)-135)/40]
        excluded=any(m.b<eta.a for m in terminal)
        if not excluded:
            q=[I(36),T,x,u]+[Z]*6+[fx,fz];cs=coefficients(q)[1]
            for s in [0.,1.,.5,.25,.75]:
                try:
                    kin=endpoint_kinematics(T,x,u,fx,fz,s) if s in (0.,1.) else None
                    m,_,_=enclose(cs,T,s,s,1,ref,kinematics=kin)
                    # Corridor entry encloses distance to ONE reference point:
                    # valid as a feasibility LOWER bound, not an exclusion upper
                    # bound for nearest-point margin. Never use it for pruning.
                    if excludes(m,eta):excluded=True;break
                except (ValueError,ZeroDivisionError):pass
        if excluded:pruned+=1;continue
        axis=max(range(5),key=lambda k:(box[k][1]-box[k][0])/scales[k]);a,b=box[axis];mid=(a+b)/2
        for bounds in [(a,mid),(mid,b)]:
            child=box.copy();child[axis]=bounds
            priority=-max((d-c)/scale for (c,d),scale in zip(child,scales))
            heapq.heappush(queue,(priority,counter,child));counter+=1
    return dict(trial_eta=str(eta),processed_boxes=processed,excluded_boxes=pruned,
        unexcluded_frontier_boxes=len(queue),complete_exclusion=not queue,
        result='certified_upper' if not queue else 'unresolved_budget_exhausted',
        scope='necessary flare constraints over full parameter box; no assumption of a local optimum',
        seconds=time.monotonic()-start,frontier=[item[2] for item in queue])

if __name__=='__main__':
    result=run();Path(__file__).with_name('global_exclusion_attempt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='frontier'},indent=2))
