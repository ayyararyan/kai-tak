"""Inspect acquired data and derive lossless GIS copies; does not alter landing model."""
from pathlib import Path
import json, hashlib, collections
import ijson
import numpy as np
import rasterio
from rasterio.shutil import copy
from rasterio.windows import from_bounds
from pyproj import Transformer
from shapely.geometry import shape, box

ROOT = Path(__file__).resolve().parent
AOI = (114.10, 22.27, 114.25, 22.40)  # acquisition subset, NOT a flight corridor
result = {"aoi_wgs84": AOI, "interpretation": "Data acquisition only; mixed epochs; no flight feasibility certification"}
srcpath = '/vsizip/' + str(ROOT/'raw/Whole_HK_DTM_5m.zip') + '/Whole_HK_DTM_5m.asc'
dstpath = ROOT/'derived/Hong_Kong_DTM_5m_HK1980.tif'
copy(srcpath, dstpath, driver='GTiff', compress='DEFLATE', predictor=2, tiled=True)
with rasterio.open(dstpath, 'r+') as dst:
    dst.crs = 'EPSG:2326'
    dst.update_tags(vertical_datum='Hong Kong Principal Datum', source='Lands Department, HKSAR Government, DATA.GOV.HK', source_epoch='2014-2015 photography per product documentation', warning='Vegetation and some elevated infrastructure included; nodata is unknown, never zero')
    count = 0; lo = float('inf'); hi = -float('inf')
    for _, window in dst.block_windows(1):
        a = dst.read(1, window=window, masked=True)
        count += a.count()
        if a.count(): lo=min(lo,float(a.min())); hi=max(hi,float(a.max()))
    result['terrain'] = dict(shape=[dst.height,dst.width], bounds=list(dst.bounds), crs=str(dst.crs), nodata=dst.nodata, valid_cells=int(count), total_cells=dst.width*dst.height, min_height_m=lo,max_height_m=hi)
    t=Transformer.from_crs(4326,2326,always_xy=True)
    bounds=t.transform_bounds(*AOI,densify_pts=21)
    w=from_bounds(*bounds,dst.transform).round_offsets().round_lengths()
    a=dst.read(1,window=w)
    profile=dst.profile.copy();profile.update(width=a.shape[1],height=a.shape[0],transform=dst.window_transform(w))
    with rasterio.open(ROOT/'derived/Kowloon_KaiTak_DTM_5m_HK1980.tif','w',**profile) as out:
        out.write(a,1);out.update_tags(**dst.tags(),subset='Approximate projected bounding rectangle enclosing requested WGS84 AOI; no resampling')
    result['terrain']['subset_shape']=list(a.shape)
    # Full-value equality check: conversion must not interpolate or fill nodata.
    equal=True
    with rasterio.open(srcpath) as src:
        for _, window in dst.block_windows(1):
            if not np.array_equal(src.read(1,window=window),dst.read(1,window=window)): equal=False;break
    result['terrain']['all_cells_equal_to_source']=equal
    assert equal
print('Terrain verified',result['terrain'],flush=True)

counts=collections.Counter(); subset=[]; ids=set(); bbox=[180.,90.,-180.,-90.]; roi=box(*AOI)
with (ROOT/'raw/Building_20260921.geojson').open('rb') as stream:
    for f in ijson.items(stream,'features.item',use_float=True):
        counts['features']+=1; prop=f['properties']; oid=prop['OBJECTID']
        if oid in ids: counts['duplicate_objectids']+=1
        ids.add(oid)
        g=shape(f['geometry']); b=g.bounds
        if g.is_empty: counts['empty_geometry']+=1;continue
        if not g.is_valid: counts['invalid_geometry']+=1
        bbox=[min(bbox[0],b[0]),min(bbox[1],b[1]),max(bbox[2],b[2]),max(bbox[3],b[3])]
        for key in ('BaseHeight','TopHeight'):
            if prop.get(key) is None: counts[key+'_missing']+=1
        if prop.get('TopHeight') is not None and prop.get('BaseHeight') is not None and prop['TopHeight']<prop['BaseHeight']: counts['top_below_base']+=1
        if g.intersects(roi):
            subset.append(f)
            for key in ('BaseHeight','TopHeight'):
                if prop.get(key) is None: counts['subset_'+key+'_missing']+=1
out={'type':'FeatureCollection','name':'Kowloon_KaiTak_buildings_20260921','features':subset}
(ROOT/'derived/Kowloon_KaiTak_buildings_20260921.geojson').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
result['buildings']={'counts':dict(counts),'bounds_wgs84':bbox,'subset_features':len(subset),'subset_rule':'Intersects AOI rectangle; entire geometries retained, no clipping or height imputation','height_datum':'HKPD; TopHeight and BaseHeight are elevations, not height above local ground'}
assert counts['duplicate_objectids']==0
assert len(subset)>0
(ROOT/'metadata/validation.json').write_text(json.dumps(result,indent=2))
print('Buildings verified',result['buildings'],flush=True)
