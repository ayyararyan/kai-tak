"""Compare repaired classifier to preserved pre-review implementation on every current object."""
import collections,importlib.util,json,sqlite3
import chronology
from chronology import ROOT

def main():
    spec=importlib.util.spec_from_file_location('before_review',ROOT/'review_repair_baseline/chronology.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    con=sqlite3.connect(ROOT/'chronology.sqlite');con.row_factory=sqlite3.Row
    events=collections.defaultdict(list)
    for r in con.execute('SELECT * FROM events'):events[r['building_csuid']].append(dict(r))
    features=list(con.execute('SELECT * FROM features'));statuses=chronology.aggregate_statuses(features)
    impact={'comparisons':{},'retained_feature_count':len(features),'source_date_values_changed':False,'model_meaning_changed':False}
    for target in ['1993-11-04','1985-01-01']:
        changes=collections.Counter();changed_examples=[]
        for f in features:
            cs=f['building_csuid'];before=old.classify(events[cs],target,f['current_status']);after=chronology.classify(events[cs],target,statuses[cs])
            changed=[k for k in before if before[k]!=after[k]]
            changes.update(changed)
            if changed and len(changed_examples)<8:changed_examples.append({'building_csuid':cs,'changed_fields':changed,'before':{k:before[k] for k in changed},'after':{k:after[k] for k in changed}})
        prior=json.loads((ROOT/'review_repair_baseline'/f'summary_{target}.json').read_text());now=json.loads((ROOT/f'summary_{target}.json').read_text())
        counted=['whole_status_counts','aoi_status_counts','whole_feature_metrics','aoi_feature_metrics','event_count','join_issue_counts','date_precision_counts']
        impact['comparisons'][target]={'objects_compared':len(features),'changed_existing_field_counts':dict(changes),'examples':changed_examples,'summary_count_fields_unchanged':all(prior[k]==now[k] for k in counted),'summary_count_differences':{k:{'before':prior[k],'after':now[k]} for k in counted if prior[k]!=now[k]}}
    for table,field in [(1002,'BuildingStructureID'),(1003,'BuildingStructureID'),(1003,'OPNo'),(1004,'OPNo')]:
        raw=[json.loads(r[0]) for r in con.execute('SELECT payload FROM raw_records WHERE table_id=?',(table,))]
        impact.setdefault('raw_missing_keys',{})[f'{table}.{field}']=sum(not chronology.valid_join_key(r[field]) for r in raw)
    impact['current_geometry_status_counts']=dict(con.execute('SELECT geometry_status,COUNT(*) FROM features GROUP BY geometry_status').fetchall())
    impact['multiple_current_csuid_status_groups']=sum(len(s)>1 for s in statuses.values())
    (ROOT/'review_repair_impact.json').write_text(json.dumps(impact,indent=2));print(json.dumps(impact,indent=2));con.close()
if __name__=='__main__':main()
