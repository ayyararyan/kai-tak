"""Encode explicitly inspected map observations; no automatic image recognition."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parent
# These named forms were visually read on the three full-sheet previews, not inferred from modern dates.
COMMON=[('Shing Tung House','shing_tung_house'),('Mau Tung House','mau_tung_house'),('On Tung House','on_tung_house'),('Hong Tung House','hong_tung_house'),('Ng Wah College','ng_wah_college'),('Lee Kau Yan Memorial School','lee_kau_yan_memorial_school'),('Regal Airport Hotel','regal_airport_hotel'),('Po Sing Court','po_sing_court'),('Tung Fung House','tung_fung_house'),('Tak Fung House','tak_fung_house'),('Lam Kee Memorial Dispensary','lam_kee_memorial_dispensary'),('Kowloon City Market','kowloon_city_market'),('Airport Terminal Building','kai_tak_terminal'),('Multi-storey Car Park','kai_tak_multistorey_carpark')]
SOURCES=[('1980_1990:678','1989-10','1980_1990_678_11-NE-11A_1989-10-01.png'),('1980_1990:679','1994-07','1980_1990_679_11-NE-11A_1994-07-01.png'),('1980_1990:680','1997-04','1980_1990_680_11-NE-11A_1997-04-01.png')]
rows=[]
for sid,month,img in SOURCES:
 for name,key in COMMON:
  rows.append(dict(historical_object_id='hist:'+key,name_on_source=name,source_id=sid,source_epoch=month,date_precision='edition_month',evidence_type='visually_inspected_official_survey_sheet',classification='named_structure_depicted',observation='Label and building outline visible on sheet; not a day-specific occupancy or survey assertion.',source_asset='sheets/previews/'+img,geometry_status='not_digitized',height_status='not_measured',modern_identity_join='not_certified',target_1993_status='requires_temporal_corroboration'))
# Same-site change evidence; footprints and within-interval dates not identified.
for sid,month,img,state,note in [
 ('1980_1990:678','1989-10',SOURCES[0][2],'construction_in_progress_depicted','Plot subsequently labelled Chung Tung House is marked C I P Oct 1989; no completed named block depicted there.'),
 ('1980_1990:679','1994-07',SOURCES[1][2],'named_structure_depicted','Chung Tung House name and footprint visible in the corresponding plot.'),
 ('1980_1990:680','1997-04',SOURCES[2][2],'named_structure_depicted','Chung Tung House name and footprint remain depicted.'),
]:
 rows.append(dict(historical_object_id='hist:chung_tung_house_site',name_on_source='Chung Tung House site',source_id=sid,source_epoch=month,date_precision='edition_month',evidence_type='visually_inspected_official_survey_sheet',classification=state,observation=note,source_asset='sheets/previews/'+img,geometry_status='not_digitized',height_status='not_measured',modern_identity_join='not_certified',target_1993_status='construction_completion_transition_unresolved'))
for sid,month,img,state,note in [
 ('1980_1990:678','1989-10',SOURCES[0][2],'map_interior_omission','Kowloon Walled City labelled but interior building outlines omitted; this is not empty-ground evidence.'),
 ('1980_1990:679','1994-07',SOURCES[1][2],'map_interior_omission','Former site interior largely blank on partial-revision sheet; image alone does not date demolition or prove all structures absent.'),
 ('1980_1990:680','1997-04',SOURCES[2][2],'park_layout_depicted','Kowloon Walled City Park labelled, with paths, ponds and structures mapped.'),
 ('HKMS:A36143','1993-11-02','', 'demolition_stage_site_observed','Parent inspected full 3000px frame: site mostly exposed/cleared ground with isolated residual structures; intact dense compound not present. Does not establish per-building clearance. Handwritten capture date independently read as 2.11.93.'),
]:
 rows.append(dict(historical_object_id='hist:kowloon_walled_city_site',name_on_source='Kowloon Walled City site',source_id=sid,source_epoch=month,date_precision='day' if sid.startswith('HKMS') else 'edition_month',evidence_type='visually_inspected_aerial_photo' if sid.startswith('HKMS') else 'visually_inspected_official_survey_sheet',classification=state,observation=note,source_asset='aerial/fullframes/A36143.jpg' if sid.startswith('HKMS') else 'sheets/previews/'+img,geometry_status='site_only_not_individual_buildings',height_status='not_measured',modern_identity_join='historical_site_not_current_building_id',target_1993_status='demolition_stage_near_reference_date'))
for object_id,name,frame,day,state,note in [
 ('kowloon_walled_city_site','Kowloon Walled City site','A23632','1990-11-13','dense_compound_observed','Dense, contiguous roof mass visible at Walled City site. Individual building identities and heights not resolved.'),
 ('kowloon_walled_city_site','Kowloon Walled City site','CN4581','1993-10-08','demolition_stage_site_observed','Site largely cleared with residual structures; not a certification that every structure was demolished.'),
 ('checkerboard_hill_landmark','Checkerboard Hill painted landmark','CN4581','1993-10-08','painted_landmark_observed','Painted checkerboard visible on hillside; slope and landmark elevations not measured from this image.'),
]:
 rows.append(dict(historical_object_id='hist:'+object_id,name_on_source=name,source_id='HKMS:'+frame,source_epoch=day,date_precision='day',evidence_type='visually_inspected_aerial_photo',classification=state,observation=note,source_asset='aerial/fullframes/'+frame+'.jpg',geometry_status='site_only_not_individual_buildings',height_status='not_measured',modern_identity_join='historical_site_not_current_building_id',target_1993_status='requires_temporal_corroboration'))
with (ROOT/'historical_visual_observations.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'visual_observation_summary.json').write_text(json.dumps({'observations':len(rows),'distinct_named_objects_or_sites':len(set(r['historical_object_id'] for r in rows)),'map_sheets_visually_inspected':3,'full_aerial_frames_parent_inspected':3,'not_a_building_census':True,'manual_source_interpretation_not_automatic_detection':True},indent=2))
print(len(rows),'observations',len(set(r['historical_object_id'] for r in rows)),'objects/sites')
