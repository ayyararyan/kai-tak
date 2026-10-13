#!/usr/bin/env python3
"""Independent artifact/semantic acceptance for the screening lane."""
import csv, hashlib, json, math
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from shapely.geometry import shape,box,mapping
from shapely import transform
from pyproj import Transformer
from shapely.strtree import STRtree

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    run=json.loads((HERE/'run_summary.json').read_text());checks=[];counts=Counter();all_rows=[];units={};modern_ids=set();repairs=[]
    to_ll=Transformer.from_crs(2326,4326,always_xy=True).transform
    to_hk=Transformer.from_crs(4326,2326,always_xy=True).transform
    modern=json.loads((PROJECT/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson').read_text())['features']
    modern_geoms=[transform(shape(f['geometry']),to_hk,interleaved=False) for f in modern]
    tree=STRtree(modern_geoms)
    index_path=PROJECT/'reconstruction/chronology/sheets/aoi_sheet_index.geojson'
    index={f['properties']['source_id']:f for f in json.loads(index_path.read_text())['features']}
    for summary in run['sheets']:
        folder=HERE/summary['key'];rows=list(csv.DictReader((folder/'ranked_candidates.csv').open()))
        fc=json.loads((folder/'ranked_candidates.geojson').read_text())['features'];regions=json.loads((folder/'map_regions.geojson').read_text())['features']
        checks.append({'check':summary['key']+'_source_hash','pass':sha(PROJECT/summary['source'])==summary['source_sha256']})
        metadata=json.loads((PROJECT/summary['source']).with_suffix('.json').read_text())
        coverage=transform(shape(index[metadata['source_id']]['geometry']),to_hk,interleaved=False)
        queried_ids={modern[i]['properties']['BuildingCSUID'] for i in tree.query(coverage,predicate='intersects')}
        checks.append({'check':summary['key']+'_all_queried_templates_preserved','pass':queried_ids=={r['modern_csuid'] for r in rows}})
        checks.append({'check':summary['key']+'_counts','pass':len(rows)==len(fc)==summary['candidates'] and len(regions)==summary['map_regions']})
        checks.append({'check':summary['key']+'_ranks','pass':sorted(int(r['rank_in_sheet']) for r in rows)==list(range(1,len(rows)+1))})
        checks.append({'check':summary['key']+'_null_historical_claims','pass':all(f['properties']['historical_roof_elevation_m'] is None and f['properties']['historical_presence_on_query_date'] is None and not f['properties']['historical_geometry_verified'] and not f['properties']['historical_identity_verified'] for f in fc)})
        checks.append({'check':summary['key']+'_valid_geometry','pass':all(shape(f['geometry']).is_valid for f in fc+regions)})
        checks.append({'check':summary['key']+'_finite_metrics','pass':all(all(math.isfinite(float(r[k])) for k in ['rank_score','boundary_distance_median_m','boundary_distance_p95_m','best_region_iou','interior_ink_fraction']) for r in rows)})
        checks.append({'check':summary['key']+'_strong_rule','pass':all(float(r['boundary_within_15m'])>=.75 and float(r['best_region_iou'])>=.5 and r['edge_clipped']=='False' and r['best_region_touches_coverage_boundary']=='False' for r in rows if r['status']=='strong_content_candidate_unverified')})
        checks.append({'check':summary['key']+'_regions_explicit','pass':all(f['properties']['classification']=='unclassified_closed_map_region_not_verified_building' and f['properties']['historical_roof_elevation_m'] is None for f in regions)})
        checks.append({'check':summary['key']+'_cell_area_conserved','pass':all(abs(f['properties']['pixel_area_m2']-f['properties']['polygon_grid_area_m2'])<max(1e-5,f['properties']['pixel_area_m2']*1e-8) and abs(transform(shape(f['geometry']),to_hk,interleaved=False).area-f['properties']['pixel_area_m2'])<max(1e-4,f['properties']['pixel_area_m2']*1e-7) for f in regions)})
        for r in rows:
            counts[r['status']]+=1;modern_ids.add(r['modern_csuid']);all_rows.append(r)
            key=r['review_work_unit'];u=units.setdefault(key,{'review_work_unit':key,'sheet':r['sheet'],'source_candidate_rows':0,'strong_content_candidate_rows':0,'unit_type':'200m_grid_review_work_unit_NOT_traced_street_block','individual_visual_review_complete':False,'historical_height_coverage_complete':False})
            u['source_candidate_rows']+=1;u['strong_content_candidate_rows']+=r['status']=='strong_content_candidate_unverified'
            if r['derived_geometry_repaired']=='True':repairs.append(r['candidate_id'])
    checks.append({'check':'script_hash','pass':sha(HERE/'extract_candidates.py')==run['script_sha256']})
    checks.append({'check':'source_index_hash','pass':sha(index_path)==run['source_index_sha256']})
    regressions=json.loads((HERE/'regression_results.json').read_text())
    checks.append({'check':'regressions_bind_current_extractor','pass':regressions['passed'] and regressions['extractor_sha256']==run['script_sha256'] and regressions['test_script_sha256']==sha(HERE/'test_candidate_repairs.py')})
    checks.append({'check':'aggregate_count','pass':len(all_rows)==run['total_candidate_rows']})
    # Work units containing current templates only; these do not assert complete map coverage.
    unitfeatures=[]
    for k,p in sorted(units.items()):
        east,north=k.rsplit('_E',1)[1].split('_N');e,n=int(east),int(north)
        unitfeatures.append({'type':'Feature','geometry':mapping(transform(box(e,n,e+200,n+200),to_ll,interleaved=False)),'properties':p})
    (HERE/'review_work_units.geojson').write_text(json.dumps({'type':'FeatureCollection','features':unitfeatures}))
    with (HERE/'all_candidates.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(all_rows[0]));w.writeheader();w.writerows(all_rows)
    result={'verified_utc':datetime.now(timezone.utc).isoformat(),'status':'passed' if all(c['pass'] for c in checks) else 'failed','checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks),'sheet_editions':len(run['sheets']),'distinct_sheet_locations':len(set(s['key'].rsplit('_',1)[0] for s in run['sheets'])),'candidate_rows':len(all_rows),'unique_modern_templates':len(modern_ids),'counts':dict(counts),'map_regions':sum(s['map_regions'] for s in run['sheets']),'map_regions_without_candidate':sum(s['map_regions_without_candidate'] for s in run['sheets']),'nonempty_review_work_units':len(units),'repaired_template_rows':repairs,'verified_historical_buildings':0,'checks':checks}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2))
    links='\n'.join(f'<li><a href="{s["key"]}/audit_contact_sheet.jpg">{s["key"]}</a>: {s["candidates"]} templates, {s["counts"].get("strong_content_candidate_unverified",0)} strong candidates; <a href="{s["key"]}/ranked_candidates.csv">CSV</a></li>' for s in run['sheets'])
    (HERE/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Historical-map matching audit</title><style>body{max-width:1000px;margin:3rem auto;font:16px system-ui;background:#f4f1e9;color:#303c38}li{margin:8px}</style><h1>Historical-map matching audit</h1><p>Red: modern template. Black: historical map. Ranking is image-content screening, not historical certification. Low support is not proof of absence. Heights remain unknown. Grid review units are not traced street blocks.</p><ul>'+links+'</ul>')
    manifest=[{'file':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in HERE.rglob('*') if p.is_file() and p.name!='manifest.json' and p.suffix!='.log' and '__pycache__' not in p.parts and 'invalidated' not in p.parts]
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
    if not all(c['pass'] for c in checks):raise SystemExit(1)

if __name__=='__main__':main()
