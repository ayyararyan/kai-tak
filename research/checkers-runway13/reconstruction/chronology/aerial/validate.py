import json,pathlib,hashlib,collections,datetime,csv
from PIL import Image
P=pathlib.Path(__file__).parent; checks=[]
for mf in ['preview_manifest.json','fullframe_manifest.json']:
 m=json.loads((P/mf).read_text())
 for row in m:
  assert row['status']!='failed';path=P/row['path'];b=path.read_bytes();assert hashlib.sha256(b).hexdigest()==row['sha256'];im=Image.open(path);im.verify()
  with Image.open(path) as im:row['width'],row['height']=im.size;row['image_mode']=im.mode;row['dpi']=[float(x) for x in im.info.get('dpi',[])]
  if 'stable_preview_url' in row:row['stable_preview_url']='https://www.hkmapservice.gov.hk/OneStopSystem/map-search/productPreview?itemId=DAP&sheetNo='+row['product_id']
  checks.append({'file':row['path'],'sha256_ok':True,'jpeg_decode_ok':True,'width':row['width'],'height':row['height']})
 (P/mf).write_text(json.dumps(m,indent=2));print(mf,len(m),collections.Counter((x['width'],x['height']) for x in m))
fs=json.loads((P/'aerial_footprints_1985_1998.geojson').read_text())['features'];csvrows=list(csv.DictReader((P/'frame_catalogue.csv').open()));assert len(fs)==14927==len(csvrows);assert len(set(x['properties']['PHOTONO'] for x in fs))==14927
v={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'index_features':len(fs),'csv_rows':len(csvrows),'unique_frame_ids':14927,'index_service_count':json.loads((P/'count_1985_1998.json').read_text())['count'],'image_checks':checks,'all_images_hash_and_decode_passed':True,'georeferenced_photos':0,'per_building_classification_complete':False}
assert v['index_service_count']==14927
(P/'validation.json').write_text(json.dumps(v,indent=2));print('PASS',len(checks),'image checks; 14927 index count/unique/CSV checks')
