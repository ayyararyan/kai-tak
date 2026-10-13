"""Public HKMS read-only frame-footprint index acquisition; no imagery licence implied."""
import pathlib,subprocess,re,json,urllib.parse,datetime,time
P=pathlib.Path(__file__).parent
KEY=re.search("API_KEY= '([^']+)'",(P/'constants_appConstant.js').read_text()).group(1)
BASE='https://api.hkmapservice.gov.hk/oss/services/OneStop/FlightPaths/MapServer/2/query'
def get(params):
    p=dict(f='json',key=KEY,**params)
    r=subprocess.run(['curl','-fLsS','--max-time','60',BASE+'?'+urllib.parse.urlencode(p)],capture_output=True,check=True)
    d=json.loads(r.stdout)
    if 'error' in d: raise RuntimeError(d['error'])
    return d
params=dict(where='YEARFLIGHT >= 1985 AND YEARFLIGHT <= 1998',geometry='114.10,22.27,114.25,22.40',geometryType='esriGeometryEnvelope',inSR=4326,spatialRel='esriSpatialRelIntersects')
ids=get(dict(**params,returnIdsOnly='true'));(P/'object_ids_1985_1998.json').write_text(json.dumps(ids))
ids=sorted(ids['objectIds']); features=[]
for i in range(0,len(ids),500):
    p=P/f'index_chunk_{i:05d}.json'
    if p.exists(): d=json.loads(p.read_text())
    else:
        d=get(dict(objectIds=','.join(map(str,ids[i:i+500])),outFields='*',returnGeometry='true',outSR=4326));p.write_text(json.dumps(d))
    assert not d.get('exceededTransferLimit');features.extend(d['features']);print(i,len(features),flush=True)
assert len(features)==len(ids)
fc={'type':'FeatureCollection','features':[]}
for f in features:
 a=f['attributes'];a['capture_date_utc']=datetime.datetime.fromtimestamp(a['DATEFLIGHT']/1000,datetime.timezone.utc).isoformat() if a['DATEFLIGHT'] else None
 a['coverage_interpretation']='HKMS index polygon; not a verified orthorectified image footprint'
 fc['features'].append({'type':'Feature','properties':a,'geometry':{'type':'Polygon','coordinates':f['geometry']['rings']}})
(P/'aerial_footprints_1985_1998.geojson').write_text(json.dumps(fc))
(P/'index_provenance.json').write_text(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public_source':BASE,'parameters':params,'count':len(features),'geometry_crs':'EPSG:4326','source_native_crs':'EPSG:2326','scope':'index polygons intersecting bbox; some centres outside bbox','index_not_imagery':True,'browser_public_application':'https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA'},indent=2))
print('DONE',len(features))
