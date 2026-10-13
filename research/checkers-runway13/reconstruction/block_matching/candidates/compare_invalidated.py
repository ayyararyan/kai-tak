#!/usr/bin/env python3
import csv,json,hashlib
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent
old={r['candidate_id']:r for r in csv.DictReader((P/'invalidated/pre_B1_B7_B8_B9/all_candidates.csv').open())}
run=json.loads((P/'run_summary.json').read_text())
new={r['candidate_id']:r for sheet in run['sheets'] for r in csv.DictReader((P/sheet['key']/'ranked_candidates.csv').open())}
changes=[];transitions=Counter();by_sheet=Counter()
for k in sorted(old.keys()|new.keys()):
    a,b=old.get(k),new.get(k);sa=a['status'] if a else 'not_in_old_query';sb=b['status'] if b else 'outside_actual_index_polygon'
    if sa!=sb:
        transitions[(sa,sb)]+=1;by_sheet[k.split('__')[0]]+=1
        changes.append({'candidate_id':k,'old_status':sa,'new_status':sb,'old_iou':a['best_region_iou'] if a else None,'new_iou':b['best_region_iou'] if b else None})
with (P/'changed_classifications.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=['candidate_id','old_status','new_status','old_iou','new_iou']);w.writeheader();w.writerows(changes)
out={'old_run':'invalidated/pre_B1_B7_B8_B9','old_candidate_rows':len(old),'new_candidate_rows':len(new),'shared_rows':len(old.keys()&new.keys()),'removed_outside_actual_index_polygon':len(old.keys()-new.keys()),'added_rows':len(new.keys()-old.keys()),'changed_status_shared_rows':sum(c['candidate_id'] in old and c['candidate_id'] in new for c in changes),'unchanged_status_shared_rows':sum(old[k]['status']==new[k]['status'] for k in old.keys()&new.keys()),'shared_rows_with_iou_change':sum(old[k]['best_region_iou']!=new[k]['best_region_iou'] for k in old.keys()&new.keys()),'transitions':[{'old':a,'new':b,'count':n} for (a,b),n in sorted(transitions.items())],'changed_by_sheet':dict(sorted(by_sheet.items()))}
(P/'review_repair_comparison.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='changed_by_sheet'},indent=2))
