"""Regression checks for source timing, missing evidence and cache integrity."""
import csv,datetime,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import match_sources as match
from sheets import acquire_sheets as sheets
class SourceMatching(unittest.TestCase):
 def test_month_does_not_imply_pre_target(self):
  lo,hi=sheets.month_bounds('1993-11-01')
  self.assertLess(lo,match.TARGET);self.assertGreater(hi,match.TARGET)
  self.assertEqual(hi,datetime.date(1993,11,30))
 def test_leap_month(self):
  self.assertEqual(match.month_bounds('1992-02-01')[1],datetime.date(1992,2,29))
 def test_real_selection_retains_preceding_same_month(self):
  picked=sheets.select();fs=json.loads((sheets.ROOT/'aoi_sheet_index.geojson').read_text())['features']
  selected={p['source_id'] for p in picked}
  affected=0
  for sheet in {p['sheet'] for p in picked}:
   rows=[f['properties'] for f in fs if f['properties']['sheet']==sheet and f['properties']['family']=='1980_1990']
   if any(p['edition_date'][:7]=='1993-11' for p in rows):
    prior=[p for p in rows if sheets.month_bounds(p['edition_date'])[1]<=match.TARGET]
    if prior:
     latest=max(p['edition_date'] for p in prior)
     self.assertTrue(any(p['source_id'] in selected for p in prior if p['edition_date']==latest));affected+=1
  self.assertGreaterEqual(affected,5)
 def test_cache_checks_bytes_and_existence(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'a.zip';r={'status':'validated_zip','sha256':hashlib.sha256(b'good').hexdigest()}
   self.assertFalse(sheets.cached_valid(r,p));p.write_bytes(b'good');self.assertTrue(sheets.cached_valid(r,p));p.write_bytes(b'bad');self.assertFalse(sheets.cached_valid(r,p))
 def test_missing_geometry_date_and_invalid_geometry(self):
  good={'type':'Feature','properties':{'source_id':'x','edition_date':'1993-01-01'},'geometry':{'type':'Polygon','coordinates':[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}}
  import copy
  missing=copy.deepcopy(good);missing['geometry']=None
  no_date=copy.deepcopy(good);no_date['properties']['edition_date']=''
  invalid=copy.deepcopy(good);invalid['geometry']['coordinates']=[[[0,0],[1,1],[1,0],[0,1],[0,0]]]
  accepted,issues=match.valid_sources([good,missing,no_date,invalid],'sheet')
  self.assertEqual(len(accepted),1);self.assertEqual(len(issues),3)
 def test_missing_frame_date_not_epoch(self):
  f={'properties':{'PHOTONO':'x'},'geometry':{'type':'Point','coordinates':[0,0]}}
  good,issues=match.valid_sources([f],'frame');self.assertEqual(good,[]);self.assertEqual(len(issues),1)
 def test_empty_csv_has_stable_header(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'empty.csv';match.write_csv(p,[],match.PAIR_FIELDS)
   with p.open() as f:r=csv.DictReader(f);self.assertEqual(r.fieldnames,match.PAIR_FIELDS);self.assertEqual(list(r),[])
if __name__=='__main__':unittest.main()
