"""Conservative documentary chronology. No historical visual verification or geometry inference."""
from __future__ import annotations
import argparse, calendar, collections, csv, datetime as dt, hashlib, json, pathlib, re, sqlite3
ROOT=pathlib.Path(__file__).resolve().parent
GEO=ROOT.parents[2]/'geospatial'
BASE='https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer'
HK=dt.timezone(dt.timedelta(hours=8))

def date_interval(value, epoch=False):
    if value is None or str(value).strip()=='': return None,None,'missing'
    if epoch:
        try:
            s=dt.datetime.fromtimestamp(float(value)/1000,HK).date().isoformat();return s,s,'day'
        except (ValueError,OverflowError,TypeError): return None,None,'invalid'
    v=str(value).strip()
    if re.fullmatch(r'\d{4}',v):
        try: y=int(v); return dt.date(y,1,1).isoformat(),dt.date(y,12,31).isoformat(),'year'
        except ValueError: return None,None,'invalid'
    m=re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{4})',v)
    if m:
        d,mo,y=map(int,m.groups())
        try:
            # Zero day is not silently repaired. No confirmed publisher partial-date convention.
            if d==0: return None,None,'invalid_zero_day'
            s=dt.date(y,mo,d).isoformat();return s,s,'day'
        except ValueError: return None,None,'invalid'
    return None,None,'unparsed'

def classify(events,target, current_status=None):
    """completed_by is an evidence predicate, never proof of survival/exact geometry at target."""
    valid=[e for e in events if e['date_min'] is not None]
    direct=[e for e in valid if e['kind']=='completion']
    permits=[e for e in valid if e['kind']=='occupation_permit']
    demos=[e for e in valid if e['kind']=='demolition_completion']
    before=lambda e:e['date_max']<=target
    done_direct=[e for e in direct if before(e)]
    done_permits=[e for e in permits if before(e)]
    done_demos=[e for e in demos if before(e)]
    conflicts=[]
    wops={e['date_min'] for e in permits if e['source_table']==1000}
    rops={e['date_min'] for e in permits if e['source_table']==1004}
    if wops and rops and wops != rops: conflicts.append('works_OP_dates_disagree_with_linked_OP_table')
    byprovider=collections.defaultdict(set)
    for e in direct:byprovider[e['provider']].add((e['date_min'],e['date_max']))
    if any(len(s)>1 for s in byprovider.values()): conflicts.append('multiple_completion_dates_same_provider')
    if len({(e['date_min'],e['date_max']) for e in direct})>1: conflicts.append('multiple_completion_dates')
    if current_status=='Active' and demos: conflicts.append('demolition_record_linked_to_active_snapshot')
    if demos and direct and any(c['date_min']>d['date_max'] for c in direct for d in demos):conflicts.append('completion_after_demolition_identity_needs_review')
    # Different issue and completion dates are not inherently contradictory.
    if direct and permits and any(p['date_max']<min(c['date_min'] for c in direct) for p in permits):conflicts.append('permit_predates_all_recorded_completion_dates')
    support=bool(done_direct or done_permits)
    qualifying_relational_permits=[e for e in done_permits if e['source_table']==1004]
    matching_dates=sorted({e['date_min'] for e in done_direct if e['date_min']==e['date_max']} &
                          {e['date_min'] for e in qualifying_relational_permits})
    if done_demos:
        status='demolition_completed_by_target_evidence_conflict' if conflicts else 'demolition_completed_by_target'
    elif done_direct:
        status='documented_completion_by_target'
    elif done_permits:
        status='documented_permit_by_target_linked_scope'
    elif any(e['date_min']<=target<=e['date_max'] for e in direct+permits):
        status='completion_or_permit_date_interval_straddles_target'
    elif direct or permits:
        status='later_completion_or_permit_only_presence_unresolved'
    elif events:
        status='documentary_records_only_presence_unresolved'
    else:
        status='no_documentary_chronology_presence_unresolved'
    if support and not done_demos and conflicts:status+='_with_evidence_conflict'
    if done_demos:
        presence='demolition_document_supported_absence_by_target' if not conflicts else 'conflicting_evidence_presence_unresolved'
    else:presence='presence_at_target_unverified'
    return {'status':status,'completion_or_permit_by_target':int(support),'direct_completion_by_target':int(bool(done_direct)),
            'permit_by_target':int(bool(done_permits)),'demolition_completed_by_target':int(bool(done_demos)),
            'presence_status':presence,'conflict_flags':';'.join(conflicts),'has_date_conflict':int(bool(conflicts)),
            'works_op_date_conflict':int('works_OP_dates_disagree_with_linked_OP_table' in conflicts),
            'completion_matches_relational_permit_by_target':int(bool(matching_dates)),
            'matching_completion_permit_dates':';'.join(matching_dates),
            'qualifying_completion_providers':';'.join(sorted({e['provider'] for e in done_direct})),
            'qualifying_direct_completion_event_ids':';'.join(e.get('event_id','') for e in done_direct),
            'qualifying_relational_permit_event_ids':';'.join(e.get('event_id','') for e in qualifying_relational_permits),
            'earliest_completion_or_permit_bound':min((e['date_max'] for e in direct+permits),default=None),
            'latest_demolition_bound':max((e['date_max'] for e in demos),default=None),
            'evidence_event_count':len(events),'undated_event_count':sum(e['date_min'] is None for e in events)}

def load(name):return json.loads((ROOT/(name+'.json')).read_text())
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(2**20):h.update(b)
    return h.hexdigest()
def create_database():
    import ijson
    from shapely.geometry import shape
    db=ROOT/'chronology.sqlite';tmp=ROOT/'chronology.building.sqlite'
    if tmp.exists(): tmp.unlink()
    con=sqlite3.connect(tmp)
    con.executescript('''
    CREATE TABLE features (objectid INTEGER PRIMARY KEY,building_csuid TEXT,name_en TEXT,name_tc TEXT,current_status TEXT,block_type TEXT,in_aoi INTEGER,lon REAL,lat REAL,base_height REAL,top_height REAL,date_create TEXT,date_stamp TEXT,geometry_valid INTEGER);
    CREATE TABLE objects (building_csuid TEXT PRIMARY KEY,current_feature_count INTEGER,in_aoi INTEGER);
    CREATE TABLE events (event_id TEXT PRIMARY KEY,building_csuid TEXT,kind TEXT,provider TEXT,date_raw TEXT,date_min TEXT,date_max TEXT,date_precision TEXT,source_table INTEGER,source_objectid INTEGER,relation_objectid INTEGER,opstructure_objectid INTEGER,building_structure_id TEXT,op_no TEXT,source_url TEXT,works_type TEXT);
    CREATE TABLE raw_records (table_id INTEGER,objectid INTEGER,payload TEXT,PRIMARY KEY(table_id,objectid));
    CREATE TABLE join_issues (building_csuid TEXT,issue TEXT,detail TEXT);
    ''')
    with (GEO/'derived/Kowloon_KaiTak_buildings_20260921.geojson').open('rb') as f:
        aoi={int(r['properties']['OBJECTID']) for r in ijson.items(f,'features.item')}
    current_counts=collections.Counter();current_aoi=collections.Counter();feat_batch=[]
    with (GEO/'raw/Building_20260921.geojson').open('rb') as f:
        for feat in ijson.items(f,'features.item',use_float=True):
            p=feat['properties'];s=shape(feat['geometry']);point=s.representative_point();cs=p['BuildingCSUID'];inside=int(p['OBJECTID'] in aoi)
            current_counts[cs]+=1;current_aoi[cs]+=inside
            feat_batch.append((p['OBJECTID'],cs,p['BuildingNameEN'],p['BuildingNameTC'],p['Status'],p['BuildingBlockType'],inside,point.x,point.y,p['BaseHeight'],p['TopHeight'],p['DateCreate'],p['DateStamp'],int(s.is_valid)))
            if len(feat_batch)>=5000:con.executemany('INSERT INTO features VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',feat_batch);feat_batch=[]
    con.executemany('INSERT INTO features VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',feat_batch)
    works,rel,structures,ops=[load(n) for n in ['BuildingWorksHistory','BuildingRelateOPStructure','OPStructure','OP']]
    for tid,rows in [(1000,works),(1002,rel),(1003,structures),(1004,ops)]:
        con.executemany('INSERT INTO raw_records VALUES (?,?,?)',((tid,r['OBJECTID'],json.dumps(r,ensure_ascii=False)) for r in rows))
    all_ids=set(current_counts)|{r['BuildingCSUID'] for r in works+rel}
    con.executemany('INSERT INTO objects VALUES (?,?,?)',((cs,current_counts[cs],int(bool(current_aoi[cs])) if current_counts[cs] else None) for cs in sorted(all_ids)))
    ev=[]
    def add(eid,cs,kind,provider,date,table,oid,wt=None,link=None,st=None,op=None):
        lo,hi,prec=date_interval(date,epoch=table==1004)
        ev.append((eid,cs,kind,provider,json.dumps(date),lo,hi,prec,table,oid,link['OBJECTID'] if link else None,st['OBJECTID'] if st else None,str(st['BuildingStructureID']) if st else None,op['OPNo'] if op else None,f'{BASE}/{table}/query?objectIds={oid}&outFields=*&f=pjson',wt))
    for r in works:
        kind={'Completion Date':'completion','OP Date':'occupation_permit','Demolition Completion Date':'demolition_completion'}.get(r['WorksType'],'administrative_certificate')
        add(f'works:{r["OBJECTID"]}',r['BuildingCSUID'],kind,r['DataProviderID'],r['WorksDate'],1000,r['OBJECTID'],wt=r['WorksType'])
    sm=collections.defaultdict(list);om=collections.defaultdict(list);rm=collections.defaultdict(list)
    for r in structures:sm[r['BuildingStructureID']].append(r)
    for r in ops:om[r['OPNo']].append(r)
    def issue(cs,kind,detail):con.execute('INSERT INTO join_issues VALUES (?,?,?)',(cs,kind,json.dumps(detail)))
    for l in rel:
        cs=l['BuildingCSUID'];rm[cs].append(l)
        if not sm[l['BuildingStructureID']]:issue(cs,'missing_opstructure',l)
        for s in sm[l['BuildingStructureID']]:
            if not s['OPNo'] or not om[s['OPNo']]:issue(cs,'missing_or_null_permit_record',s)
            for o in om[s['OPNo']]:
                add(f'op:{l["OBJECTID"]}:{s["OBJECTID"]}:{o["OBJECTID"]}',cs,'occupation_permit','BD',o['OPDate'],1004,o['OBJECTID'],link=l,st=s,op=o)
    for cs,rr in rm.items():
        if len(rr)>1:issue(cs,'multiple_structure_links_retained',{'rows':len(rr),'structure_ids':[r['BuildingStructureID'] for r in rr]})
    for cs,n in current_counts.items():
        if n>1:issue(cs,'multiple_current_features_for_csuid',{'count':n})
    con.executemany('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',ev)
    con.executescript('CREATE INDEX events_cs ON events(building_csuid); CREATE INDEX features_cs ON features(building_csuid); CREATE INDEX issue_cs ON join_issues(building_csuid);')
    con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close();tmp.replace(db)
    inputs={str(p.relative_to(ROOT.parent.parent.parent)):sha(p) for p in [GEO/'raw/Building_20260921.geojson',GEO/'derived/Kowloon_KaiTak_buildings_20260921.geojson']}
    (ROOT/'input_hashes.json').write_text(json.dumps(inputs,indent=2))

def query(target):
    dt.date.fromisoformat(target)
    con=sqlite3.connect(ROOT/'chronology.sqlite');con.row_factory=sqlite3.Row
    events=collections.defaultdict(list)
    for r in con.execute('SELECT * FROM events'):events[r['building_csuid']].append(dict(r))
    statuses={r['building_csuid']:r['current_status'] for r in con.execute('SELECT building_csuid,current_status FROM features')}
    multiplicity={r['building_csuid']:r['n'] for r in con.execute('SELECT building_csuid,COUNT(*) n FROM join_issues GROUP BY building_csuid')}
    results={}
    for o in con.execute('SELECT * FROM objects'):
        cs=o['building_csuid'];r=classify(events[cs],target,statuses.get(cs));r.update({'building_csuid':cs,'target_date':target,'current_feature_count':o['current_feature_count'],'in_aoi':o['in_aoi'],'join_issue_count':multiplicity.get(cs,0),'historical_geometry_status':'unverified','visual_verification_count':0});results[cs]=r
    fields=list(next(iter(results.values())))
    out=ROOT/f'objects_{target}.csv'
    with out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(results.values())
    ff=['objectid','building_csuid','name_en','name_tc','current_status','block_type','in_aoi','lon','lat','base_height','top_height','date_create','date_stamp','geometry_valid']
    extras=[x for x in fields if x not in ff]
    counts=collections.Counter();aoi_counts=collections.Counter();metrics=collections.Counter();aoi_metrics=collections.Counter()
    whole=ROOT/f'current_features_{target}.csv';local=ROOT/f'aoi_features_{target}.csv'
    with whole.open('w',newline='') as f,local.open('w',newline='') as g:
        w=csv.DictWriter(f,fieldnames=ff+extras);v=csv.DictWriter(g,fieldnames=ff+extras);w.writeheader();v.writeheader()
        for feat in con.execute('SELECT * FROM features ORDER BY objectid'):
            r=dict(feat);r.update({k:results[r['building_csuid']][k] for k in extras});w.writerow(r);counts[r['status']]+=1
            if r['in_aoi']:v.writerow(r);aoi_counts[r['status']]+=1
            for key in ['completion_or_permit_by_target','direct_completion_by_target','permit_by_target','demolition_completed_by_target','has_date_conflict']:
                metrics[key]+=r[key]
                if r['in_aoi']:aoi_metrics[key]+=r[key]
            if r['evidence_event_count']:metrics['with_any_event']+=1;aoi_metrics['with_any_event']+=r['in_aoi']
    # Full event provenance exports include every duplicate works row and every permit join path.
    with (ROOT/'events.csv').open('w',newline='') as f:
        cursor=con.execute('SELECT * FROM events ORDER BY event_id');w=csv.writer(f);w.writerow([d[0] for d in cursor.description]);w.writerows(cursor)
    with (ROOT/'join_issues.csv').open('w',newline='') as f:
        cursor=con.execute('SELECT * FROM join_issues ORDER BY building_csuid');w=csv.writer(f);w.writerow([d[0] for d in cursor.description]);w.writerows(cursor)
    examples=[]
    for feat in con.execute("SELECT * FROM features WHERE in_aoi=1 AND name_en IS NOT NULL AND (name_en LIKE '%Mei Tung%' OR name_en LIKE '%Mei Po%' OR name_en LIKE '%Mei Yan%' OR name_en LIKE '%Mei Tak%' OR name_en LIKE '%Regal%' OR name_en LIKE '%Walled%') ORDER BY objectid"):
        cs=feat['building_csuid'];examples.append({'current_feature':dict(feat),'classification':results[cs],'events':events[cs]})
    (ROOT/f'examples_{target}.json').write_text(json.dumps(examples,indent=2,ensure_ascii=False))
    summary={'target_date':target,'query_generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'all_current_features':sum(counts.values()),'aoi_current_features':sum(aoi_counts.values()),'all_objects_including_unlocated_documentary_ids':len(results),'documentary_ids_without_current_geometry':sum(r['current_feature_count']==0 for r in results.values()),'whole_status_counts':dict(counts),'aoi_status_counts':dict(aoi_counts),'whole_feature_metrics':dict(metrics),'aoi_feature_metrics':dict(aoi_metrics),'event_count':sum(map(len,events.values())),'unique_csuid_with_events':len([k for k,v in events.items() if v]),'date_precision_counts':dict(con.execute('SELECT date_precision,COUNT(*) FROM events GROUP BY date_precision').fetchall()),'works_types':dict(con.execute('SELECT works_type,COUNT(*) FROM events WHERE source_table=1000 GROUP BY works_type').fetchall()),'join_issue_counts':dict(con.execute('SELECT issue,COUNT(*) FROM join_issues GROUP BY issue').fetchall()),'visual_verifications':0,'historical_geometry_verifications':0,'exact_target_presence_not_inferred_from_completed_by':True}
    (ROOT/f'summary_{target}.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2));con.close()

def manifest():
    files=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts:
            files.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
    (ROOT/'manifest.json').write_text(json.dumps({'generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'files':files},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--date',default='1993-11-04');p.add_argument('--manifest-only',action='store_true');a=p.parse_args()
    if a.manifest_only:manifest()
    else:
        if a.build:create_database()
        query(a.date);manifest()
