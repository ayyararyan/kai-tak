#!/usr/bin/env python3
"""Additive exact-road-cell review joins; never historical identity acceptance."""
import sys
sys.dont_write_bytecode=True
import csv,hashlib,json,math
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from shapely.geometry import shape,mapping,Polygon,MultiPolygon
from shapely.strtree import STRtree
from shapely import transform
from pyproj import Transformer

HERE=Path(__file__).resolve().parent;CAND=HERE.parent;ROOT=CAND.parent
sys.path.insert(0,str(CAND))
from extract_candidates import read_map
BLOCKS=ROOT/'aerial_registration/four_road_control_blocks.geojson'
TO_HK=Transformer.from_crs(4326,2326,always_xy=True).transform
TO_LL=Transformer.from_crs(2326,4326,always_xy=True).transform
DATES=['1989-10','1994-07'];EPS=1e-6

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def project(g):return transform(g,TO_HK,interleaved=False)
def ll(g):return transform(g,TO_LL,interleaved=False)
def geo(path,fs):path.write_text(json.dumps({'type':'FeatureCollection','features':fs},separators=(',',':')))
def csvwrite(path,rows,fields=None):
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]) if rows else fields or ['id']);w.writeheader();w.writerows(rows)
def font(size):
    return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',size)
def parts(g):
    if isinstance(g,Polygon):return [g]
    if isinstance(g,MultiPolygon):return list(g.geoms)
    return [p for x in getattr(g,'geoms',[]) for p in parts(x)]

def draw_geometry(draw,g,xy,color,width):
    for p in parts(g):
        draw.line([xy(x,y) for x,y in p.exterior.coords],fill=color,width=width)
        for ring in p.interiors:draw.line([xy(x,y) for x,y in ring.coords],fill=color,width=width)

def overlay(cell_id,cell,records,rasters,cellprops):
    # Same survey-grid extent/scale for both epochs, with legible street context.
    left,bottom,right,top=cell.bounds;pad=12;left-=pad;right+=pad;bottom-=pad;top+=pad
    height=1300;width=math.ceil(height*(right-left)/(top-bottom));header=100;footer=85
    canvas=Image.new('RGB',(2*width+30,header+height+footer),'#f5f2e9');d=ImageDraw.Draw(canvas)
    for j,date in enumerate(DATES):
        gray,tf=rasters[date];inv=~tf
        e=np.linspace(left,right,width,endpoint=False)+(right-left)/(2*width)
        n=np.linspace(top,bottom,height,endpoint=False)-(top-bottom)/(2*height)
        cc=np.floor((e-tf.c)/tf.a).astype(int);rr=np.floor((n-tf.f)/tf.e).astype(int)
        assert cc.min()>=0 and rr.min()>=0 and cc.max()<gray.shape[1] and rr.max()<gray.shape[0]
        crop=Image.fromarray(gray[np.ix_(rr,cc)]).convert('RGB');cd=ImageDraw.Draw(crop)
        xy=lambda x,y:((x-left)/(right-left)*width,(top-y)/(top-bottom)*height)
        draw_geometry(cd,cell,xy,'#366477',5)
        # All intersecting modern templates shown, including low-support ones.
        for rec in records[date]['templates']:
            p=shape(rec['geometry']);p=project(p);props=rec['properties']
            color='#57734b' if props['screen_status']=='strong_content_candidate_unverified' else '#b85e35'
            draw_geometry(cd,p,xy,color,2)
            pt=p.representative_point();x,y=xy(pt.x,pt.y);tag=str(props['cell_local_template_number'])
            bb=cd.textbbox((x,y),tag,font=font(13));cd.rectangle((bb[0]-1,bb[1]-1,bb[2]+1,bb[3]+1),fill='#fffdf3');cd.text((x,y),tag,font=font(13),fill='#242e29')
        x=j*(width+30);canvas.paste(crop,(x,header));d.text((x+8,14),cell_id+'  |  '+date,font=font(20),fill='#28362f')
        d.text((x+8,44),cellprops['west_road']+' to '+cellprops['east_road'],font=font(15),fill='#28362f')
        d.text((x+8,67),f"{len(records[date]['templates'])} current templates; {len(records[date]['regions'])} unclassified map regions",font=font(14),fill='#28362f')
    d.text((10,header+height+10),'Black: historical map | Blue: exact road-control cell',font=font(16),fill='#28362f')
    d.text((10,header+height+34),'Green: strong screen; copper: other screen status. Neither is historical identity acceptance.',font=font(14),fill='#28362f')
    d.text((10,header+height+57),'Numbers join across_dates.csv: same current template, NOT proven historical survival.',font=font(14),fill='#28362f')
    canvas.save(HERE/cell_id/'two_date_overlay.png')

def main():
    blocks=json.loads(BLOCKS.read_text())['features'];assert len(blocks)==4
    parent_manifest_bytes=(CAND/'manifest.json').read_bytes()
    expected={r['file']:r['sha256'] for r in json.loads(parent_manifest_bytes)}
    inputs=[{'file':str(BLOCKS.relative_to(ROOT)),'sha256':sha(BLOCKS),'scope':'exact supplied road-centre cells'}]
    data={};rasters={};checks=[]
    for date in DATES:
        folder=CAND/f'11-NE-11A_{date}';data[date]={}
        for kind,filename in [('templates','ranked_candidates.geojson'),('regions','map_regions.geojson')]:
            path=folder/filename;digest=sha(path);assert digest==expected[str(path.relative_to(CAND))]
            fs=json.loads(path.read_text())['features'];gs=[project(shape(f['geometry'])) for f in fs]
            data[date][kind]=(fs,gs,STRtree(gs));inputs.append({'file':str(path.relative_to(ROOT)),'sha256':digest,'scope':'verified candidate package, unchanged'})
        receipt=next(json.loads(p.read_text()) for p in (ROOT.parent/'chronology/sheets/maps').glob('*.json') if json.loads(p.read_text())['sheet']=='11-NE-11A' and json.loads(p.read_text())['edition_date'][:7]==date)
        gray,tf,source,_=read_map(receipt);rasters[date]=(gray,tf);inputs.append({'file':str(source.relative_to(ROOT.parent.parent)),'sha256':sha(source),'scope':'original map checked against receipt by reader'})
    summaries=[];allcells=[]
    for bf in blocks:
        cid=bf['properties']['block_id'];cell=project(shape(bf['geometry']));out=HERE/cid;out.mkdir(exist_ok=True)
        records={};templates_by_id={};members=[]
        for date in DATES:
            records[date]={}
            for kind in ['templates','regions']:
                fs,gs,tree=data[date][kind];selected=[];touches=0
                for idx in tree.query(cell,predicate='intersects'):
                    g=gs[idx];cut=cell.intersection(g);area=cut.area
                    if area<=EPS:touches+=1;continue
                    source=fs[idx]['properties'];ident=source['candidate_id'] if kind=='templates' else f"11-NE-11A_{date}__region_{source['region_id']}"
                    props={'cell_id':cid,'edition_month':date,'source_object_id':ident,'source_id':'1980_1990:678' if date=='1989-10' else '1980_1990:679','source_sha256':source['source_sha256'],'intersection_area_m2':area,'source_geometry_area_m2':g.area,'source_fraction_inside_cell':area/g.area,'cell_area_fraction':area/cell.area,'assignment_rule':'positive-area intersection in EPSG:2326; numerical area tolerance 1e-6m2','geometry_role':'modern_template_clipped_to_review_cell_NOT_historical_footprint' if kind=='templates' else 'unclassified_map_region_clipped_to_review_cell_NOT_verified_building','historical_identity_verified':False,'historical_presence_on_query_date':None,'historical_roof_elevation_m':None,'contents_verified':False}
                    if kind=='templates':
                        props.update(modern_csuid=source['modern_csuid'],modern_name=source['modern_name'],modern_epoch=source['modern_epoch'],screen_status=source['status'],rank_score=source['rank_score'],best_region_id=source['best_region_id'],best_region_iou=source['best_region_iou'])
                        templates_by_id.setdefault(source['modern_csuid'],{})[date]=props
                    else:props.update(region_id=source['region_id'],classification=source['classification'],touches_source_coverage_boundary=source['touches_clipped_coverage_boundary'],screened_modern_matches_in_whole_sheet=source['screened_modern_matches'])
                    selected.append({'type':'Feature','geometry':mapping(ll(cut)),'properties':props})
                    members.append({'cell_id':cid,'edition_month':date,'kind':kind,'source_object_id':ident,'intersection_area_m2':area,'source_fraction_inside_cell':area/g.area})
                selected.sort(key=lambda f:f['properties']['source_object_id']);records[date][kind]=selected
                checks.append({'check':f'{cid}_{date}_{kind}_all_positive_intersections','pass':len(selected)+touches==len(tree.query(cell,predicate='intersects'))})
        correspondence=[]
        for number,(ident,epochs) in enumerate(sorted(templates_by_id.items()),1):
            row={'cell_id':cid,'cell_local_template_number':number,'modern_csuid':ident,'modern_name':next(iter(epochs.values()))['modern_name'],'modern_epoch':'2026-09-21','join_basis':'same modern CSUID used as image-content template in each source month, NOT historical identity','historical_identity_verified':False,'historical_presence_1989':None,'historical_presence_1994':None,'historical_roof_elevation_m':None}
            for date in DATES:
                p=epochs.get(date)
                for key in ['source_object_id','screen_status','rank_score','best_region_id','best_region_iou','intersection_area_m2','source_fraction_inside_cell']:
                    row[date+'_'+key]=p[key] if p else None
                if p:p['cell_local_template_number']=number
            correspondence.append(row)
        csvwrite(out/'across_dates.csv',correspondence)
        checks.append({'check':cid+'_across_dates_ids_and_nulls','pass':len(correspondence)==len(templates_by_id) and all(r['historical_presence_1989'] is None and r['historical_presence_1994'] is None and not r['historical_identity_verified'] for r in correspondence)})
        # Across-date REGION relation is actual area overlap, independently of modern IDs.
        earlier=records[DATES[0]]['regions'];later=records[DATES[1]]['regions'];laterg=[project(shape(f['geometry'])) for f in later];tree=STRtree(laterg);links=[]
        for a in earlier:
            ga=project(shape(a['geometry']))
            for idx in tree.query(ga,predicate='intersects'):
                gb=laterg[idx];b=later[idx];inter=ga.intersection(gb).area
                if inter<=EPS:continue
                links.append({'cell_id':cid,'earlier_region_id':a['properties']['source_object_id'],'later_region_id':b['properties']['source_object_id'],'intersection_area_m2':inter,'fraction_of_earlier_cell_clipped_region':inter/ga.area,'fraction_of_later_cell_clipped_region':inter/gb.area,'cell_clipped_region_iou':inter/(ga.area+gb.area-inter),'relation':'geometric_overlap_candidate_NOT_temporal_identity','historical_identity_verified':False})
        csvwrite(out/'region_overlap_across_dates.csv',links)
        checks.append({'check':cid+'_across_dates_region_overlap_bounds','pass':all(r['intersection_area_m2']>EPS and 0<r['cell_clipped_region_iou']<=1+1e-8 and 0<r['fraction_of_earlier_cell_clipped_region']<=1+1e-8 and 0<r['fraction_of_later_cell_clipped_region']<=1+1e-8 and not r['historical_identity_verified'] for r in links)})
        for date in DATES:
            for kind in ['templates','regions']:
                fs=records[date][kind];geo(out/f'{date}_{kind}.geojson',fs)
                checks.append({'check':f'{cid}_{date}_{kind}_valid_null_semantics','pass':all(shape(f['geometry']).is_valid and not f['properties']['historical_identity_verified'] and f['properties']['historical_roof_elevation_m'] is None and f['properties']['historical_presence_on_query_date'] is None for f in fs)})
                checks.append({'check':f'{cid}_{date}_{kind}_overlap_bounds','pass':all(0<f['properties']['source_fraction_inside_cell']<=1+1e-8 and 0<f['properties']['cell_area_fraction']<=1+1e-8 and cell.buffer(.002).covers(project(shape(f['geometry']))) for f in fs)})
        csvwrite(out/'memberships.csv',members)
        overlay(cid,cell,records,rasters,bf['properties'])
        with Image.open(out/'two_date_overlay.png') as im:
            im.verify()
        checks.append({'check':cid+'_paired_overlay_decodes','pass':True})
        summary={'cell_id':cid,'road_cell_source_properties':bf['properties'],'cell_area_epsg2326_m2':cell.area,'across_date_current_template_rows':len(correspondence),'across_date_unclassified_region_overlap_rows':len(links),'epochs':{date:{'template_assignments':len(records[date]['templates']),'region_assignments':len(records[date]['regions']),'template_statuses':dict(Counter(f['properties']['screen_status'] for f in records[date]['templates']))} for date in DATES},'full_contents_verified':False,'historical_identity_accepted':0}
        (out/'summary.json').write_text(json.dumps(summary,indent=2));summaries.append(summary)
        allcells.append({'type':'Feature','geometry':bf['geometry'],'properties':{**bf['properties'],'assignment_status':'source-content candidates assigned, not complete inventory','modern_template_across_dates_count':len(correspondence),'region_overlap_across_dates_count':len(links)}})
    geo(HERE/'assigned_road_cells.geojson',allcells)
    checks.append({'check':'parent_manifest_unchanged','pass':(CAND/'manifest.json').read_bytes()==parent_manifest_bytes})
    checks.append({'check':'road_cells_source_unchanged','pass':sha(BLOCKS)==inputs[0]['sha256']})
    for date in DATES:
        for fn in ['ranked_candidates.geojson','map_regions.geojson']:
            p=CAND/f'11-NE-11A_{date}'/fn;checks.append({'check':'input_unchanged_'+str(p.relative_to(CAND)),'pass':sha(p)==expected[str(p.relative_to(CAND))]})
    result={'generated_utc':datetime.now(timezone.utc).isoformat(),'status':'passed' if all(c['pass'] for c in checks) else 'failed','checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks),'cells':summaries,'inputs':inputs,'checks':checks,'full_contents_verified':False,'historical_identity_accepted':0}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2))
    links=''.join(f'<section><h2>{s["cell_id"]}</h2><p>{s["across_date_current_template_rows"]} current-template rows; {s["across_date_unclassified_region_overlap_rows"]} geometric region-overlap pairs. Neither count is accepted historical identities.</p><a href="{s["cell_id"]}/across_dates.csv">Across-date template CSV</a> · <a href="{s["cell_id"]}/region_overlap_across_dates.csv">Map-region overlap CSV</a><p><a href="{s["cell_id"]}/two_date_overlay.png"><img src="{s["cell_id"]}/two_date_overlay.png"></a></p></section>' for s in summaries)
    (HERE/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Four road-cell matching comparisons</title><style>body{margin:32px auto;max-width:1100px;font:16px system-ui;background:#f5f2e9;color:#28362f}img{max-width:100%}section{margin:48px 0}</style><h1>Four road-control cells: 1989 and 1994</h1><p>Exact supplied road-centre cells include parts of streets. Modern template assignments and unclassified map-region overlaps support review, not proven historical identity, survival or height. Click each image for full resolution.</p>'+links)
    manifest=[{'file':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='manifest.json']
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'status':result['status'],'checks_passed':result['checks_passed'],'checks_total':len(checks),'cells':[{k:v for k,v in s.items() if k not in ['road_cell_source_properties','epochs']} for s in summaries]},indent=2))
    assert result['status']=='passed'

if __name__=='__main__':main()
