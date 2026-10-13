"""Assemble hash-bound partial reconstruction handoff; never imply scientific completion."""
from pathlib import Path
import json, hashlib, csv
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def read(n): return json.loads((ROOT/n).read_text())
def write(n,d): (ROOT/n).write_text(json.dumps(d,indent=2)+'\n')

def main():
    receipt=read('parent_test_receipt.json')
    assert receipt['all_passed']
    for row in receipt['bound_source_files']:
        assert sha(ROOT/row['path'])==row['sha256'], 'Test receipt stale: '+row['path']
    c=read('candidates/validation.json'); s=read('scene/validation.json')
    st=read('aerial_registration/stereo_verification.json')
    m=read('aerial_registration/observed_mesh_verification.json')
    assert c['checks_passed']==c['checks_total'] and st['all_passed'] and m['all_passed']
    assert s['dense_source_points']==171307 and s['observed_mesh_faces']==225371
    assert s['historical_faces']==45 and s['historic_nonnull_heights']==0
    manifest=read('candidates/manifest.json')
    for row in manifest:
        p=ROOT/'candidates'/row['file']
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],p
    road=read('candidates/road_cells/validation.json')
    assert road['checks_passed']==road['checks_total']
    road_manifest=read('candidates/road_cells/manifest.json')
    for row in road_manifest:
        p=ROOT/'candidates/road_cells'/row['file']
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],p
    for obs in read('road_cell_visual_observations.json')['observations']:
        assert sha(ROOT/obs['overlay_path'])==obs['overlay_sha256']
        assert sha(ROOT/'candidates/road_cells'/obs['cell_id']/'across_dates.csv')==obs['row_table_sha256']
    now=datetime.now(timezone.utc).isoformat()
    columns=['easting_hk1980_m','northing_hk1980_m','z_above_fitted_local_park_road_plane_m']
    lo=[float('inf')]*3; hi=[-float('inf')]*3
    with (ROOT/'aerial_registration/dense_stereo_points.csv').open() as stream:
        for row in csv.DictReader(stream):
            for i,key in enumerate(columns):
                v=float(row[key]);lo[i]=min(lo[i],v);hi[i]=max(hi[i],v)
    validation={
        'verified_utc':now,'overall_status':'incomplete',
        'correctness':'tested and actual output invariants verified',
        'completeness':'3 implemented / 4 partially implemented of 7 requirements',
        'end_to_end':'partial source-to-surface artifacts verified; browser interaction unverified; full historical scene incomplete',
        'parent_test_reruns':{'suites':receipt['python_suites'],'all_passed':receipt['all_passed'],'total_python_tests':receipt['total_python_tests'],'recorded_utc':receipt['recorded_utc'],'source_hash_receipt':'parent_test_receipt.json'},
        'parent_node_ui_logic_test':'passed; stubbed trace construction, not browser/WebGL',
        'candidate_artifact_checks':{'passed':c['checks_passed'],'total':c['checks_total']},
        'candidate_manifest_hashes':{'passed':len(manifest),'total':len(manifest)},
        'road_cell_artifact_checks':{'passed':road['checks_passed'],'total':road['checks_total']},
        'road_cell_manifest_hashes':{'passed':len(road_manifest),'total':len(road_manifest)},
        'road_cell_parent_replay':read('road_cell_parent_verification.json'),
        'stereo_artifact_checks':len(st['checks']), 'mesh_artifact_checks':len(m['checks']),
        'static_surface_preview':'parent visually inspected scene/overview.png; not browser screenshot',
        'browser_interaction_verified':False,'browser_blocker':'OpenClaw navigation blocked file and localhost URLs; no bypass attempted',
        'full_historical_reconstruction_complete':False,'clearance_certified':False,
        'unapproved_scope_reductions':0,'unapproved_proxy_substitutions':0,
        'scene_counts':s,
    }
    write('validation.json',validation)
    paths=['REPORT.md','MODEL_REQUIREMENTS_TRACEABILITY.md','SPEC.md','validation.json','parent_test_receipt.json',
        'historical_faces.geojson','historical_faces_hk1980.geojson','structure_matches.json',
        'historical_3d_unknown_mask.geojson','reviewed_geometry_manifest.json','manual_review_decisions.json',
        'modern_correspondences.json','scene/index.html','scene/scene.json','scene/overview.png',
        'aerial_registration/four_road_control_blocks.geojson','aerial_registration/sparse_stereo_report.json',
        'aerial_registration/dense_stereo_report.json','aerial_registration/dense_stereo_points.csv',
        'aerial_registration/dense_stereo_points.ply','aerial_registration/observed_surface_mesh.glb',
        'aerial_registration/observed_surface_mesh.ply','aerial_registration/observed_surface_mesh_report.json',
        'aerial_registration/observed_surface_faces.csv','aerial_registration/dense_pixel_qc.npz',
        'aerial_registration/stereo_verification.json','aerial_registration/observed_mesh_verification.json',
        'candidates/all_candidates.csv','candidates/review_work_units.geojson','candidates/validation.json','candidates/manifest.json',
        'candidates/road_cells/index.html','candidates/road_cells/validation.json','candidates/road_cells/manifest.json',
        'candidates/road_cells/assigned_road_cells.geojson','road_cell_visual_observations.json','road_cell_parent_verification.json']
    artifacts=[{'path':n,'bytes':(ROOT/n).stat().st_size,'sha256':sha(ROOT/n)} for n in paths]
    handoff={
        'schema_version':1,'generated_utc':now,'status':'partial_historical_reconstruction_incomplete',
        'photo_date':'1993-11-02','historical_query_date':'1993-11-04','query_date_presence_certified':False,
        'map_edition_months':['1989-10','1994-07','1997-04'],
        'horizontal_crs':'EPSG:2326 diagnostic map-controlled stereo alignment; EPSG:4326 face delivery also available',
        'vertical_datum':'local fitted park/road plane; NOT HKPD',
        'absolute_vertical_datum_reconciled':False,'historical_hard_height_intervals':None,
        'horizontal_holdout_rmse_m':5.7542656,'horizontal_holdout_count':4,
        'height_error_confidence_intervals':None,'camera_calibration':'nominal film-label/scan assumptions',
        'named_map_forms':15,'reviewed_source_faces':45,'screening_pairs':c['candidate_rows'],
        'screening_pairs_identity_verified':False,'road_control_cells':4,'road_cells_contents_verified':False,
        'road_cell_template_joins':202,'road_cell_dated_template_assignments':404,'road_cell_qualitative_map_observations':8,
        'dense_points':s['dense_source_points'],'dense_points_inside_control_hull':3780,
        'surface_triangles':s['observed_mesh_faces'],'surface_vertices':s['observed_mesh_vertices'],
        'surface_is_watertight':False,'surface_is_building_classified':False,
        'sample_coordinate_bounds_ENZrelative':{'min':lo,'max':hi,'meaning':'sample envelope, not filled coverage or validated accuracy region'},
        'map_core_epsg2326':[837500,821000,838250,821600],
        'coverage':'local paired-image surfaces and three core map editions; not whole-approach completed geometry',
        'unknown_mask':'historical_3d_unknown_mask.geojson; epistemic unknown, NOT physical occupancy or free space',
        'pixel_correspondence_mask':'aerial_registration/dense_pixel_qc.npz; invalid pixels are unknown',
        'presence_uncertainty':'map depiction at edition epoch; no certified interpolation to query date',
        'modern_comparison':'2026 buildings, separate HKPD layer; no historical height transfer',
        'clearance_certified':False,'landing_model_modified':False,
        'full_scope_remaining':['comprehensive block/structure/vanished-object identity resolution','broader frame and control coverage','validated camera/scan calibration','independent horizontal and vertical checks','historical absolute datum/terrain/runway reconciliation','supported occlusion and roof interpretation'],
        'browser_interaction_verified':False,'artifacts':artifacts,
    }
    write('HANDOFF.json',handoff)
    for row in artifacts: assert sha(ROOT/row['path'])==row['sha256']
    print(json.dumps({'artifacts_bound_and_reverified':len(artifacts),'candidate_manifest_hashes_verified':len(manifest),'status':handoff['status']}))

if __name__=='__main__':main()
