"""Independent checks on source completeness, joins and dated inventory outputs."""
import collections,csv,hashlib,json,pathlib,sqlite3
from chronology import ROOT

def main():
    con=sqlite3.connect(ROOT/'chronology.sqlite');con.row_factory=sqlite3.Row
    manifest=json.loads((ROOT/'acquisition_manifest.json').read_text()); checks=[]
    for t in manifest['tables']:
        rows=json.loads((ROOT/(t['name']+'.json')).read_text()); n=t['retrieved_count'];assert len(rows)==n==t['count_before']==t['count_after']
        assert len({r['OBJECTID'] for r in rows})==n
        assert con.execute('SELECT COUNT(*) FROM raw_records WHERE table_id=?',(t['table_id'],)).fetchone()[0]==n
        for f in t['files']:assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
        checks.append(t['name']+': source counts, IDs, DB rows, original response hashes match')
    assert con.execute('SELECT COUNT(*) FROM events WHERE source_table=1000').fetchone()[0]==168042
    assert con.execute('SELECT COUNT(*) FROM events WHERE source_table=1004').fetchone()[0]==53341
    assert con.execute('SELECT COUNT(*) FROM features').fetchone()[0]==342195
    assert con.execute('SELECT COUNT(DISTINCT building_csuid) FROM features').fetchone()[0]==342195
    assert con.execute('SELECT SUM(in_aoi) FROM features').fetchone()[0]==69915
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    checks.append('Every works row and every resolvable permit relationship preserved; all current polygons unique by CSUID')
    summary=json.loads((ROOT/'summary_1993-11-04.json').read_text())
    for prefix,total,expected in [('current',342195,summary['whole_status_counts']),('aoi',69915,summary['aoi_status_counts'])]:
        rows=list(csv.DictReader((ROOT/f'{prefix}_features_1993-11-04.csv').open()));assert len(rows)==total
        assert dict(collections.Counter(r['status'] for r in rows))==expected
        assert all(r['historical_geometry_status']=='unverified' and r['visual_verification_count']=='0' for r in rows)
        assert all(r['presence_status']=='presence_at_target_unverified' for r in rows)
    checks.append('Both dated feature exports reconcile exactly; zero fabricated image checks or exact-target presence labels')
    duplicate_groups=con.execute('SELECT COUNT(*) FROM (SELECT COUNT(*) n FROM events WHERE source_table=1000 GROUP BY building_csuid,provider,works_type,date_raw HAVING n>1)').fetchone()[0]
    duplicate_extra=con.execute('SELECT SUM(n-1) FROM (SELECT COUNT(*) n FROM events WHERE source_table=1000 GROUP BY building_csuid,provider,works_type,date_raw HAVING n>1)').fetchone()[0]
    works_ops=collections.defaultdict(set);rel_ops=collections.defaultdict(set);comps=collections.defaultdict(set)
    for r in con.execute("SELECT * FROM events WHERE kind IN ('occupation_permit','completion')"):
        if r['date_min'] is None:continue
        if r['kind']=='completion':comps[r['building_csuid']].add(r['date_min'])
        elif r['source_table']==1000:works_ops[r['building_csuid']].add(r['date_min'])
        else:rel_ops[r['building_csuid']].add(r['date_min'])
    shared=set(works_ops)&set(rel_ops);disagree={cs for cs in shared if works_ops[cs]!=rel_ops[cs]}
    corroborated={cs for cs in comps.keys() & rel_ops.keys() if comps[cs] & rel_ops[cs]}
    # Date value conflict is different from independently corroborated completion evidence.
    demo_rows=[dict(r) for r in con.execute("SELECT * FROM events WHERE kind='demolition_completion'")]
    (ROOT/'demolition_events.json').write_text(json.dumps(demo_rows,indent=2))
    anomaly_examples=[]
    for cs in sorted(disagree)[:12]:anomaly_examples.append({'building_csuid':cs,'works_OP_dates':sorted(works_ops[cs]),'linked_OP_dates':sorted(rel_ops[cs]),'completion_dates':sorted(comps[cs])})
    issues=[dict(r) for r in con.execute("SELECT * FROM events WHERE date_precision!='day'")]
    report={'checks_passed':checks,'source_files_hashed':sum(len(t['files']) for t in manifest['tables']),
            'works_duplicate_natural_key_groups_preserved':duplicate_groups,'works_duplicate_extra_rows_preserved':duplicate_extra,
            'csuid_with_both_works_and_relational_OP_dates':len(shared),'csuid_with_disagreeing_OP_source_dates':len(disagree),
            'csuid_with_completion_date_corroborated_by_relational_OP_date':len(corroborated),
            'works_OP_year_counts':dict(collections.Counter(d[:4] for v in works_ops.values() for d in v)),
            'op_date_timezone_from_source':'China Standard Time (UTC+08:00); epoch timestamp normalized to Hong Kong calendar date',
            'non_day_events':issues,'anomaly_examples':anomaly_examples,'database_integrity':'ok'}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['non_day_events','anomaly_examples']},indent=2))
if __name__=='__main__':main()
