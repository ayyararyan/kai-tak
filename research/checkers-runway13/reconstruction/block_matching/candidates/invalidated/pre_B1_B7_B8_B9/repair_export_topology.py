#!/usr/bin/env python3
"""Repair only invalid derived region exports, preserving original geometry evidence."""
import json,hashlib
from pathlib import Path
from shapely.geometry import shape,mapping
from shapely import make_valid,transform
from shapely.validation import explain_validity
from pyproj import Transformer
HERE=Path(__file__).resolve().parent
to_hk=Transformer.from_crs(4326,2326,always_xy=True).transform
repairs=[]
for path in sorted(HERE.glob('*/map_regions.geojson')):
    obj=json.loads(path.read_text());originals=[]
    for f in obj['features']:
        g=shape(f['geometry'])
        if g.is_valid:continue
        originals.append(json.loads(json.dumps(f)))
        before=transform(g,to_hk,interleaved=False).area
        corrected=make_valid(g)
        assert corrected.is_valid
        after=transform(corrected,to_hk,interleaved=False).area
        record={'sheet_epoch':path.parent.name,'region_id':f['properties']['region_id'],'reason':explain_validity(g),'method':'GEOS make_valid on derived EPSG:4326 contour; original preserved','area_before_hk_grid_m2':before,'area_after_hk_grid_m2':after,'area_change_m2':after-before,'output_geometry_type':corrected.geom_type}
        f['geometry']=mapping(corrected);f['properties']['derived_export_topology_repair']=record
        repairs.append(record)
    if originals:
        backup=path.parent/'invalid_export_regions_preserved.geojson'
        preserved={'type':'FeatureCollection','features':originals}
        if backup.exists() and json.loads(backup.read_text())!=preserved:raise RuntimeError(f'Refusing to overwrite different preserved evidence: {backup}')
        if not backup.exists():backup.write_text(json.dumps(preserved))
        path.write_text(json.dumps(obj,separators=(',',':')))
result={'repaired_regions':len(repairs),'max_absolute_area_change_m2':max([abs(r['area_change_m2']) for r in repairs] or [0]),'repairs':repairs,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
# Idempotent invocation retains prior repair evidence when there is nothing left to fix.
if repairs or not (HERE/'topology_repairs.json').exists():(HERE/'topology_repairs.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='repairs'}))
