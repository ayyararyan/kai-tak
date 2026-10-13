import unittest
from chronology import date_interval,classify,permit_paths,aggregate_statuses,geometry_fields

def e(kind='completion',date='01/01/1980',table=1000,provider='BD'):
    lo,hi,p=date_interval(date,epoch=table==1004)
    return dict(kind=kind,date_min=lo,date_max=hi,source_table=table,provider=provider)

class DateRules(unittest.TestCase):
    def test_day_first(self):self.assertEqual(date_interval('04/11/1993'),('1993-11-04','1993-11-04','day'))
    def test_unpadded_day(self):self.assertEqual(date_interval('28/3/2000')[0],'2000-03-28')
    def test_year_interval(self):self.assertEqual(date_interval('2021'),('2021-01-01','2021-12-31','year'))
    def test_zero_day_not_imputed(self):self.assertEqual(date_interval('00/01/2001'),(None,None,'invalid_zero_day'))
    def test_invalid_leap_day(self):self.assertEqual(date_interval('29/02/1993')[2],'invalid')
    def test_null(self):self.assertEqual(date_interval(None)[2],'missing')
    def test_hong_kong_epoch_timezone(self):self.assertEqual(date_interval(-28886400000,True)[0],'1969-02-01')

class Semantics(unittest.TestCase):
    def test_compact_date_normalized_before_comparison(self):
        r=classify([e(date='05/11/1993')],'19931104')
        self.assertFalse(r['completion_or_permit_by_target'])
    def test_post_demolition_permit_not_clean_absence(self):
        r=classify([e('demolition_completion','01/01/1980'),e('occupation_permit','01/01/1990')],'1993-11-04','Inactive')
        self.assertEqual(r['presence_status'],'conflicting_evidence_presence_unresolved')
        self.assertIn('permit_after_demolition_identity_needs_review',r['conflict_flags'])
    def test_overlap_demolition_permit_not_clean_absence(self):
        r=classify([e('demolition_completion','1980'),e('occupation_permit','01/06/1980')],'1993-11-04','Inactive')
        self.assertEqual(r['presence_status'],'conflicting_evidence_presence_unresolved')
    def test_completion_year_and_day_compatible(self):
        r=classify([e(date='1980'),e(date='01/06/1980')],'1993-11-04')
        self.assertEqual(r['conflict_flags'],'')
    def test_completion_disjoint_year_and_day_conflict(self):
        r=classify([e(date='1980'),e(date='01/06/1981')],'1993-11-04')
        self.assertIn('multiple_completion_dates',r['conflict_flags'])
    def test_op_full_bounds_compatible(self):
        rel=e('occupation_permit','01/06/1980');rel['source_table']=1004
        r=classify([e('occupation_permit','1980'),rel],'1993-11-04')
        self.assertFalse(r['works_op_date_conflict'])
    def test_op_full_bounds_disjoint(self):
        rel=e('occupation_permit','01/06/1981');rel['source_table']=1004
        r=classify([e('occupation_permit','1980'),rel],'1993-11-04')
        self.assertTrue(r['works_op_date_conflict'])
    def test_compatible_interval_not_exact_date_corroboration(self):
        rel=e('occupation_permit','1980');rel['source_table']=1004
        r=classify([e('completion','01/01/1980'),rel],'1993-11-04')
        self.assertFalse(r['completion_matches_relational_permit_by_target'])
        self.assertEqual(r['conflict_flags'],'')
    def test_current_statuses_aggregate_without_last_row_wins(self):
        rows=[dict(building_csuid='a',current_status=s) for s in ['Active','Inactive']]
        for order in [rows,rows[::-1]]:
            r=classify([e('demolition_completion')],'1993-11-04',aggregate_statuses(order)['a'])
            self.assertEqual(r['current_status_evidence'],'Active;Inactive')
            self.assertIn('current_feature_statuses_disagree',r['conflict_flags'])
            self.assertEqual(r['presence_status'],'conflicting_evidence_presence_unresolved')
    def test_later_op_not_absence(self):
        r=classify([e('occupation_permit','01/01/2019')],'1993-11-04');self.assertFalse(r['completion_or_permit_by_target']);self.assertEqual(r['presence_status'],'presence_at_target_unverified')
    def test_completed_not_survival(self):
        r=classify([e()],'1993-11-04');self.assertTrue(r['direct_completion_by_target']);self.assertEqual(r['presence_status'],'presence_at_target_unverified')
    def test_boundary_inclusive(self):self.assertTrue(classify([e(date='04/11/1993')],'1993-11-04')['direct_completion_by_target'])
    def test_partial_year_straddles(self):self.assertIn('straddles',classify([e(date='1993')],'1993-11-04')['status'])
    def test_partial_year_after_end(self):self.assertTrue(classify([e(date='1993')],'1993-12-31')['direct_completion_by_target'])
    def test_duplicate_events_retained(self):
        r=classify([e(),e()],'1993-11-04');self.assertEqual(r['evidence_event_count'],2);self.assertEqual(r['conflict_flags'],'')
    def test_divergent_completion_preserved(self):self.assertIn('multiple_completion_dates',classify([e(),e(date='01/01/2000')],'1993-11-04')['conflict_flags'])
    def test_admin_does_not_certify_completion(self):self.assertFalse(classify([e('administrative_certificate')],'1993-11-04')['completion_or_permit_by_target'])
    def test_null_retained(self):self.assertEqual(classify([e(date=None)],'1993-11-04')['undated_event_count'],1)
    def test_op_source_conflict_retained(self):
        r=classify([e('occupation_permit','01/02/2019'),e('occupation_permit',-28886400000,1004)],'1993-11-04');self.assertTrue(r['has_date_conflict']);self.assertTrue(r['permit_by_target'])
    def test_demolition_absence_only_supported(self):self.assertEqual(classify([e('demolition_completion')],'1993-11-04')['presence_status'],'demolition_document_supported_absence_by_target')
    def test_active_demolition_conflict(self):self.assertEqual(classify([e('demolition_completion')],'1993-11-04','Active')['presence_status'],'conflicting_evidence_presence_unresolved')
    def test_future_demolition_not_target_absence(self):self.assertEqual(classify([e('demolition_completion','01/01/2020')],'1993-11-04')['presence_status'],'presence_at_target_unverified')
    def test_unrecorded_not_absent(self):self.assertEqual(classify([],'1993-11-04')['status'],'no_documentary_chronology_presence_unresolved')
    def test_corroboration_survives_conflicting_works_op(self):
        r=classify([e('completion','01/02/1969'),e('occupation_permit','01/02/2019'),e('occupation_permit',-28886400000,1004)],'1993-11-04')
        self.assertEqual(r['matching_completion_permit_dates'],'1969-02-01')
        self.assertTrue(r['works_op_date_conflict']);self.assertTrue(r['completion_matches_relational_permit_by_target'])
    def test_fresh_raw_source_anomaly_not_parser(self):
        import json,pathlib
        records=json.loads((pathlib.Path(__file__).parent/'documentation/fresh_anomaly_crosscheck.json').read_text())
        sample=[r for r in records if r['building_csuid']=='0621112353T20050430']
        self.assertEqual(len(sample),3)
        works=[r for r in sample if r['raw_record'].get('WorksType')=='OP Date'][0]
        self.assertEqual(works['raw_record']['WorksDate'],'01/02/2019')
        self.assertEqual(date_interval(works['raw_record']['WorksDate'])[0],'2019-02-01')
        permit=[r for r in sample if 'OPDate' in r['raw_record']][0]
        self.assertEqual(date_interval(permit['raw_record']['OPDate'],True)[0],'1969-02-01')

class JoinRules(unittest.TestCase):
    def test_missing_structure_keys_do_not_join(self):
        for missing in [None,'','   ']:
            with self.subTest(missing=missing):
                rel=[dict(OBJECTID=1,BuildingCSUID='a',BuildingStructureID=missing)]
                structures=[dict(OBJECTID=2,BuildingStructureID=missing,OPNo='P')]
                ops=[dict(OBJECTID=3,OPNo='P',OPDate=0)]
                issues=[];self.assertEqual(list(permit_paths(rel,structures,ops,lambda *a:issues.append(a))),[])
                self.assertEqual(len(issues),2)
    def test_missing_permit_keys_do_not_join(self):
        for missing in [None,'','   ']:
            with self.subTest(missing=missing):
                rel=[dict(OBJECTID=1,BuildingCSUID='a',BuildingStructureID=1)]
                structures=[dict(OBJECTID=2,BuildingStructureID=1,OPNo=missing)]
                ops=[dict(OBJECTID=3,OPNo=missing,OPDate=0)]
                issues=[];self.assertEqual(list(permit_paths(rel,structures,ops,lambda *a:issues.append(a))),[])
                self.assertEqual(len(issues),2)
    def test_populated_duplicate_paths_retained(self):
        rel=[dict(OBJECTID=i,BuildingCSUID='a',BuildingStructureID=1) for i in [1,2]]
        structures=[dict(OBJECTID=3,BuildingStructureID=1,OPNo='P')]
        ops=[dict(OBJECTID=4,OPNo='P',OPDate=0)]
        self.assertEqual(len(list(permit_paths(rel,structures,ops,lambda *a:None))),2)

class MissingGeometry(unittest.TestCase):
    def test_null_geometry(self):self.assertEqual(geometry_fields(None),(None,None,None,'missing'))
    def test_empty_geometry(self):self.assertEqual(geometry_fields({'type':'Polygon','coordinates':[]}),(None,None,None,'empty'))
    def test_unreadable_geometry(self):self.assertEqual(geometry_fields({}),(None,None,None,'unreadable'))

class PipelineRegression(unittest.TestCase):
    def test_incomplete_rows_and_status_multiplicity_survive_end_to_end(self):
        import tempfile,pathlib,json,sqlite3,csv,contextlib,io
        from unittest.mock import patch
        import chronology
        with tempfile.TemporaryDirectory() as d:
            base=pathlib.Path(d);root=base/'reconstruction/chronology/structures';geo=base/'geospatial'
            root.mkdir(parents=True);(geo/'raw').mkdir(parents=True);(geo/'derived').mkdir()
            polygon={'type':'Polygon','coordinates':[[[114,22],[114.1,22],[114.1,22.1],[114,22]]]}
            features=[]
            for i,cs,status,geometry in [(1,'A','Active',polygon),(2,'A','Inactive',polygon),(3,'B','Active',None),(4,'C','Active',{'type':'Polygon','coordinates':[]})]:
                props=dict(OBJECTID=i,BuildingCSUID=cs,BuildingNameEN=cs,BuildingNameTC=None,Status=status,BuildingBlockType='Tower',BaseHeight=None,TopHeight=None,DateCreate='20000101',DateStamp='20200101')
                features.append(dict(type='Feature',geometry=geometry,properties=props))
            for f in [geo/'raw/Building_20260921.geojson',geo/'derived/Kowloon_KaiTak_buildings_20260921.geojson']:
                f.write_text(json.dumps(dict(type='FeatureCollection',features=features)))
            payloads={'BuildingWorksHistory':[dict(OBJECTID=1,BuildingCSUID='A',DataProviderID='BD',WorksType='Demolition Completion Date',WorksDate='01/01/1980'),dict(OBJECTID=2,BuildingCSUID='A',DataProviderID='BD',WorksType='OP Date',WorksDate='01/01/1990')],
            'BuildingRelateOPStructure':[dict(OBJECTID=1,BuildingCSUID='B',BuildingStructureID=None),dict(OBJECTID=2,BuildingCSUID='C',BuildingStructureID=1)],
            'OPStructure':[dict(OBJECTID=1,BuildingStructureID=None,OPNo='P'),dict(OBJECTID=2,BuildingStructureID=1,OPNo=None)],
            'OP':[dict(OBJECTID=1,OPNo='P',OPDate=0),dict(OBJECTID=2,OPNo=None,OPDate=0)]}
            for n,rows in payloads.items():(root/(n+'.json')).write_text(json.dumps(rows))
            with patch.object(chronology,'ROOT',root),patch.object(chronology,'GEO',geo),contextlib.redirect_stdout(io.StringIO()):
                chronology.create_database();chronology.query('19931104')
            con=sqlite3.connect(root/'chronology.sqlite')
            self.assertEqual(con.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0],8)
            self.assertEqual(con.execute('SELECT COUNT(*) FROM events WHERE source_table=1004').fetchone()[0],0)
            self.assertEqual(con.execute('SELECT COUNT(*) FROM features WHERE lon IS NULL AND lat IS NULL').fetchone()[0],2)
            self.assertEqual(con.execute('SELECT COUNT(*) FROM features').fetchone()[0],4)
            con.close()
            with (root/'aoi_features_1993-11-04.csv').open() as f:rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),4)
            self.assertEqual(rows[0]['current_status_evidence'],'Active;Inactive')
            self.assertEqual(rows[0]['presence_status'],'conflicting_evidence_presence_unresolved')
            self.assertEqual(rows[2]['geometry_status'],'missing')
            self.assertEqual(rows[3]['geometry_status'],'empty')

if __name__=='__main__':unittest.main()
