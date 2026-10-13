#!/usr/bin/env python3
"""Reproducible image-content screening; never historical identity certification."""
import argparse, calendar, csv, hashlib, json, math, zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np
import rasterio
from affine import Affine
from PIL import Image, ImageDraw
from pyproj import Transformer
from rasterio.enums import Resampling, ColorInterp, MaskFlags
from rasterio.features import rasterize, shapes
from shapely.geometry import shape, mapping, box, Polygon, MultiPolygon
from shapely import make_valid, transform as _transform
from shapely.strtree import STRtree
from shapely.ops import unary_union

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
MAPS=HERE.parents[1]/'chronology/sheets/maps'
MODERN=PROJECT/'geospatial/derived/Kowloon_KaiTak_buildings_20260921.geojson'
TO_HK=Transformer.from_crs(4326,2326,always_xy=True).transform
TO_LL=Transformer.from_crs(2326,4326,always_xy=True).transform
RESOLUTION=.25
INDEX_PATH=MAPS.parent/'aoi_sheet_index.geojson'
_INDEX=None

def source_coverage(meta):
    global _INDEX
    if _INDEX is None:
        _INDEX={f['properties']['source_id']:f for f in json.loads(INDEX_PATH.read_text())['features']}
    return geom_transform(TO_HK,shape(_INDEX[meta['source_id']]['geometry']))

def read_gray(ds,out_shape):
    # Fail closed rather than interpreting arbitrary palette indices as brightness.
    if ds.count!=1 or ds.colorinterp!=(ColorInterp.gray,) or ds.dtypes!=('uint8',):
        raise ValueError('Only single-band uint8 grayscale is supported; palette/RGB require explicit decoding')
    if ds.nodata is not None or any(MaskFlags.all_valid not in f for f in ds.mask_flag_enums):
        raise ValueError('Nodata/masked imagery is unsupported; unknown pixels must not become white regions or ink')
    return ds.read(1,out_shape=out_shape,resampling=Resampling.average)

def coverage_edge_labels(labels,valid):
    edge=valid & (cv2.dilate((~valid).astype('uint8'),np.ones((3,3),dtype='uint8'))>0)
    edge[0,:]|=valid[0,:];edge[-1,:]|=valid[-1,:]
    edge[:,0]|=valid[:,0];edge[:,-1]|=valid[:,-1]
    return set(map(int,np.unique(labels[edge])))

def candidate_status(clipped,support,iou,region_truncated):
    if clipped:return 'edge_clipped_review'
    if region_truncated:return 'ambiguous_region_truncated'
    if support>=.75 and iou>=.50:return 'strong_content_candidate_unverified'
    if support>=.5 or iou>=.25:return 'ambiguous_content_candidate'
    return 'low_support_rejected_by_screen'

def polygonize_cells(mask,tf):
    # Raster cell EDGES, preserving holes and narrow/diagonally linked components.
    polys=[shape(g) for g,value in shapes(mask.astype('uint8'),mask=mask.astype(bool),transform=tf,connectivity=4) if value==1]
    return unary_union(polys)

def geom_transform(fn,g):
    return _transform(g,fn,interleaved=False)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump_geo(path,features):
    path.write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':')))

def boundary_samples(poly,step=.5):
    lines=[p.exterior for p in (poly.geoms if isinstance(poly,MultiPolygon) else [poly]) if isinstance(p,Polygon)]
    return np.array([(q.x,q.y) for line in lines for q in [line.interpolate(d) for d in np.arange(0,line.length,step)]])

def read_map(meta):
    path=MAPS/Path(meta['file']).name
    if sha(path)!=meta['sha256']:
        raise ValueError('Source archive SHA256 differs from acquisition receipt; refusing analysis')
    with zipfile.ZipFile(path) as z:
        tif=next(n for n in z.namelist() if n.lower().endswith('.tif'))
        tfw=next(n for n in z.namelist() if n.lower().endswith('.tfw'))
        a,d,b,e,c,f=map(float,z.read(tfw).decode().split())
    native=Affine(a,b,c-.5*a-.5*b,d,e,f-.5*d-.5*e)
    with rasterio.open('/vsizip/'+str(path)+'/'+tif) as ds:
        h=math.ceil(ds.height*abs(e)/RESOLUTION); w=math.ceil(ds.width*abs(a)/RESOLUTION)
        arr=read_gray(ds,(h,w))
        tf=native*Affine.scale(ds.width/w,ds.height/h)
    return arr,tf,path,tfw

def analyse(meta,features,geoms,tree):
    key=f"{meta['sheet']}_{meta['edition_date'][:7]}"
    out=HERE/key;out.mkdir(exist_ok=True)
    gray,tf,source,tfw=read_map(meta)
    # Actual index polygon clips margins; its geographic envelope is NOT the core.
    coverage=source_coverage(meta)
    valid=rasterize([(coverage,1)],out_shape=gray.shape,transform=tf,dtype='uint8')>0
    ink=(gray<200).astype('uint8')
    dist=cv2.distanceTransform(1-ink,cv2.DIST_L2,cv2.DIST_MASK_PRECISE)*abs(tf.a)
    # No artificial closing: gaps remain gaps and can reject a real structure.
    n,labels,stats,cents=cv2.connectedComponentsWithStats(((1-ink)*valid).astype('uint8'),connectivity=8)
    edge_labels=coverage_edge_labels(labels,valid)
    areas=stats[:,cv2.CC_STAT_AREA]*abs(tf.a*tf.e)
    eligible=(areas>=12)&(areas<=25000);eligible[0]=False
    region_ids=np.flatnonzero(eligible)
    inv=~tf; rows=[];candidate_features=[];used=Counter()
    for idx in tree.query(coverage,predicate='intersects'):
        original=geoms[idx];p=original
        props=features[idx]['properties']
        ident=props['BuildingCSUID']
        repaired=not p.is_valid
        if repaired:p=make_valid(p)
        if not isinstance(p,(Polygon,MultiPolygon)):
            continue
        if not coverage.covers(p):
            clipped=True
        else:clipped=False
        xy=boundary_samples(p)
        if not len(xy):continue
        ij=np.array([inv*(x,y) for x,y in xy]);cols=np.floor(ij[:,0]).astype(int);rr=np.floor(ij[:,1]).astype(int)
        ok=(rr>=0)&(rr<gray.shape[0])&(cols>=0)&(cols<gray.shape[1])
        dv=dist[rr[ok],cols[ok]]
        if not len(dv):continue
        left,bottom,right,top=p.bounds
        c0,r0=inv*(left,top);c1,r1=inv*(right,bottom)
        c0=max(0,int(c0)-1);r0=max(0,int(r0)-1);c1=min(gray.shape[1],math.ceil(c1)+1);r1=min(gray.shape[0],math.ceil(r1)+1)
        mask=rasterize([(p,1)],out_shape=(r1-r0,c1-c0),transform=tf*Affine.translation(c0,r0),dtype='uint8')>0
        labs=labels[r0:r1,c0:c1][mask];ids,count=np.unique(labs,return_counts=True)
        possible=[(int(i),int(k)) for i,k in zip(ids,count) if eligible[i]]
        best_id=None;best_iou=0.;overlap=0
        for i,k in possible:
            iou=k/(mask.sum()+stats[i,cv2.CC_STAT_AREA]-k)
            if iou>best_iou:best_id,best_iou,overlap=i,float(iou),k
        support=float(np.mean(dv<=1.5));score=.65*support+.35*best_iou
        region_truncated=best_id in edge_labels if best_id is not None else False
        status=candidate_status(clipped,support,best_iou,region_truncated)
        if best_id is not None and best_iou>=.25:used[best_id]+=1
        pt=p.representative_point();work=f"{meta['sheet']}_E{int(pt.x//200)*200}_N{int(pt.y//200)*200}"
        y,m=map(int,meta['edition_date'][:7].split('-'))
        row=dict(candidate_id=key+'__'+str(ident),modern_csuid=ident,modern_name=props.get('BuildingNameEN'),modern_epoch='2026-09-21',sheet=meta['sheet'],source_id=meta['source_id'],edition_month=meta['edition_date'][:7],edition_date_min=f'{y}-{m:02}-01',edition_date_max=f'{y}-{m:02}-{calendar.monthrange(y,m)[1]}',source_sha256=meta['sha256'],review_work_unit=work,work_unit_type='200m_grid_review_unit_not_street_block',status=status,rank_score=round(score,6),boundary_within_075m=float(np.mean(dv<=.75)),boundary_within_15m=support,boundary_within_3m=float(np.mean(dv<=3)),boundary_distance_median_m=float(np.median(dv)),boundary_distance_p95_m=float(np.percentile(dv,95)),best_region_id=best_id,best_region_iou=best_iou,modern_area_m2=p.area,region_area_m2=float(areas[best_id]) if best_id is not None else None,interior_ink_fraction=float(ink[r0:r1,c0:c1][mask].mean()),edge_clipped=clipped,derived_geometry_repaired=repaired,historical_geometry_verified=False,historical_identity_verified=False,historical_presence_on_query_date=None,historical_roof_elevation_m=None,geometry_role='modern_outline_matching_template_not_historical_footprint')
        row['best_region_touches_coverage_boundary']=region_truncated
        rows.append(row);candidate_features.append({'type':'Feature','geometry':mapping(geom_transform(TO_LL,p)),'properties':row})
    rows.sort(key=lambda r:r['rank_score'],reverse=True)
    for rank,row in enumerate(rows,1):row['rank_in_sheet']=rank
    with (out/'ranked_candidates.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['candidate_id']);writer.writeheader();writer.writerows(rows)
    dump_geo(out/'ranked_candidates.geojson',candidate_features)
    regions=[]
    for i in region_ids:
        x,y,w,h,px=map(int,stats[i]);mask=(labels[y:y+h,x:x+w]==i).astype('uint8')
        p=polygonize_cells(mask,tf*Affine.translation(x,y))
        if abs(p.area-areas[i])>max(1e-5,areas[i]*1e-8):raise ValueError('Cell polygon area mismatch')
        regions.append({'type':'Feature','geometry':mapping(geom_transform(TO_LL,p)),'properties':dict(region_id=int(i),sheet=meta['sheet'],edition_month=meta['edition_date'][:7],source_sha256=meta['sha256'],classification='unclassified_closed_map_region_not_verified_building',screened_modern_matches=used[int(i)],status='no_modern_correspondence_above_iou_025' if not used[int(i)] else 'modern_correspondence_candidate',pixel_area_m2=float(areas[i]),polygon_grid_area_m2=float(p.area),touches_clipped_coverage_boundary=int(i) in edge_labels,historical_roof_elevation_m=None,geometry_method='white_connected_component_raster_cell_edges_holes_preserved_no_simplification',caveat='May be building, road, garden, text, grid or map omission. Pixel edges and interior ink holes retained. Not a historic building census.' )})
    dump_geo(out/'map_regions.geojson',regions)
    # Audit contact sheet includes strong, middle and low score cases, not only successes.
    sample=rows[:12]+rows[len(rows)//2:len(rows)//2+6]+rows[-6:]
    canvas=Image.new('RGB',(1400,max(1,math.ceil(len(sample)/4))*310),'#efefeb');draw=ImageDraw.Draw(canvas)
    if not sample:draw.text((20,20),'No current building templates overlap this source sheet. Historical map regions remain unresolved.',fill='#222222')
    feature_lookup={f['properties']['candidate_id']:f for f in candidate_features}
    for j,row in enumerate(sample):
        p=geom_transform(TO_HK,shape(feature_lookup[row['candidate_id']]['geometry']));b=p.bounds
        pad=max(8.,(b[2]-b[0]+b[3]-b[1])*.08);x0,y0=inv*(b[0]-pad,b[3]+pad);x1,y1=inv*(b[2]+pad,b[1]-pad)
        x0=max(0,int(x0));y0=max(0,int(y0));x1=min(gray.shape[1],math.ceil(x1));y1=min(gray.shape[0],math.ceil(y1))
        crop=Image.fromarray(gray[y0:y1,x0:x1]).convert('RGB');cd=ImageDraw.Draw(crop)
        for pp in (p.geoms if isinstance(p,MultiPolygon) else [p]):
            coords=[(float((inv*(x,y))[0]-x0),float((inv*(x,y))[1]-y0)) for x,y in pp.exterior.coords]
            cd.line(coords,fill='#d04429',width=3)
        crop.thumbnail((340,250));cx=(j%4)*350;cy=(j//4)*310;canvas.paste(crop,(cx,cy))
        draw.text((cx+3,cy+252),f"rank {row['rank_in_sheet']} {row['modern_csuid']}\nink {row['boundary_within_15m']:.2f}; IoU {row['best_region_iou']:.2f}\n{str(row['modern_name'] or '')[:42]}",fill='#222222')
    canvas.save(out/'audit_contact_sheet.jpg',quality=92)
    summary=dict(schema_version=2,coverage_method='actual_source_index_polygon_projected_not_geographic_bbox',coverage_bounds_epsg2326=list(coverage.bounds),key=key,source=str(source.relative_to(PROJECT)),source_sha256=sha(source),tfw_member=tfw,affine=list(tf)[:6],crs='EPSG:2326 assigned from official survey grid; independent checks in parent registration report',sampling_resolution_m=[abs(tf.a),abs(tf.e)],candidates=len(rows),counts=dict(Counter(r['status'] for r in rows)),map_regions=len(regions),map_regions_without_candidate=sum(not f['properties']['screened_modern_matches'] for f in regions),verified_historical_buildings=0,limitations=['No visual identity acceptance performed by this extractor','Ink includes text, road and grid lines','Candidate rank is heuristic, not calibrated probability','Current feature universe misses vanished structures; closed map regions remain unclassified','No height transfer and no historical volume produced','Date is edition month, not object survey date','No registration adjustment estimated; world file used verbatim'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary),flush=True)
    return summary

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--core-pre1993',action='store_true');args=parser.parse_args()
    allmeta=[json.loads(p.read_text()) for p in MAPS.glob('*.json')]
    selected=[m for m in allmeta if m['sheet']=='11-NE-11A' and m['edition_date'][:7] in ['1989-10','1994-07']]
    if args.core_pre1993:
        latest={}
        for m in allmeta:
            if m.get('in_core') and m['edition_date']<'1993-11-01' and (m['sheet'] not in latest or m['edition_date']>latest[m['sheet']]['edition_date']):latest[m['sheet']]=m
        selected+=list(latest.values())
    selected={m['source_id']:m for m in selected}
    features=json.loads(MODERN.read_text())['features'];geoms=[geom_transform(TO_HK,shape(f['geometry'])) for f in features];tree=STRtree(geoms)
    summaries=[]
    for m in sorted(selected.values(),key=lambda m:(m['sheet'],m['edition_date'])):summaries.append(analyse(m,features,geoms,tree))
    (HERE/'run_summary.json').write_text(json.dumps(dict(schema_version=2,source_index_sha256=sha(INDEX_PATH),generated_utc=datetime.now(timezone.utc).isoformat(),modern_source_sha256=sha(MODERN),script_sha256=sha(Path(__file__)),sheets=summaries,total_candidate_rows=sum(s['candidates'] for s in summaries),verified_historical_buildings=0),indent=2))

if __name__=='__main__':main()
