"""Apply evidenced lineage corrections to a freshly generated unpublished catalogue."""
import collections,csv,json,re
from pathlib import Path
from archive_catalogue import ROOT,A,P,TITLES,read,write,digest,require_candidate,scientific_status_from_evidence,geospatial_dates

def unique_records(values):
 result=[]
 for value in values:
  if value not in result:result.append(value)
 return result

def refine(source_root):
 master=require_candidate(A)
 artifacts=read(A/'catalogue/artifacts.json');datasets=read(A/'catalogue/datasets.json');pv=read(A/'catalogue/provenance.json');corr=read(A/'catalogue/catalogue_corrections.json');lineage=read(A/'catalogue/lineage_edges.json')
 am={x['id']:x for x in artifacts['artifacts']};dm={x['id']:x for x in datasets['datasets']}
 for x in am.values():
  if 'source_attribution' not in x:
   x['source_attribution']=list(x['creator'])
   if x['processing_level']!='downloaded':x['creator']=['Aryan Ayyar (authorship proposed)'] if 'src-aryan-research' in x['source_ids'] else []
  if 'kt-survey-rasters' in x['dataset_ids'] and x['publication_date']:
   x.setdefault('source_publication_date_raw',x['publication_date']);x['publication_date']=x['publication_date'][:7];x['publication_date_precision']='month'
 for c in corr['dataset_and_global_corrections']:
  if 'dataset_id' in c:
   d=dm[c['dataset_id']];d['derived_from']=[v for v in d['derived_from'] if v not in c['remove_derived_from']]
   if c['add_relation'] not in d.setdefault('related_datasets',[]):d['related_datasets'].append(c['add_relation'])
 for u in corr['artifact_updates']:
  if u['artifact_id'] not in am:raise ValueError('Missing correction artifact')
  x=am[u['artifact_id']]
  if x['path']!=u['path']:raise ValueError('Correction path mismatch')
  x.update(u['fields'])
  if x['publication_decision']=='Redistribution permitted' and x['provenance_status'] in ('pinned-source-and-output-hashes','producer-reassembly-byte-identical'):
   p=source_root/x['path']
   if not p.is_file() or p.is_symlink() or digest(p)!=x['sha256']:raise ValueError('Corrected item bytes mismatch: '+x['path'])
   x['included_in_v1']=True
 for d in dm.values():
  if 'related_datasets' in d:d['related_datasets']=unique_records(d['related_datasets'])
  d['limitations']=unique_records(d['limitations'])
  if 'frozen-evidence' in d['id']:
   d.setdefault('consumer_scripts',list(d['producer_scripts']));d['producer_scripts']=[]
   limitation='build.py validates/consumes frozen evidence; it is not asserted to have created the snapshots.'
   if limitation not in d['limitations']:d['limitations'].append(limitation)
  members=[am[i] for i in d['artifact_ids']];d['permitted_bundle_files']=sum(x['included_in_v1'] for x in members)
 # Include the audited distinct virtual ZIP members/version nodes, not fictitious filesystem paths.
 pv['nodes']=lineage['additional_nodes'];nodeids={x['id'] for x in pv['nodes']}
 # Rebuild attribution from corrected source IDs, not just remove obsolete edges.
 merged={}
 for e in pv['edges']+lineage['edges']:
  if e['relation']=='attributed-to-source' and e['subject'] in am:continue
  if e['id'] in merged and merged[e['id']]!=e:raise ValueError('Conflicting lineage edge: '+e['id'])
  merged[e['id']]=e
 for x in am.values():
  for sid in x['source_ids']:
   identifier=f'edge-{x["id"]}-{sid}'
   merged[identifier]=dict(id=identifier,relation='attributed-to-source',subject=x['id'],object=sid,evidence_level=x['provenance_status'])
 pv['edges']=[merged[k] for k in sorted(merged)]
 # Correct scientific meaning after all legacy field overrides, without changing evidence.
 geo_path=ROOT/(P+'geospatial/manifest.json')
 geo=read(geo_path) if geo_path.is_file() else {}
 geo_members={P+'geospatial/'+f['path']:f for f in geo.get('files',[]) if f['path'].startswith(('raw/','derived/'))}
 for x in am.values():
  scientific_status_from_evidence(x,[ROOT,source_root])
  if x['path'] in geo_members and x['sha256']==geo_members[x['path']]['sha256']:
   x.update(geospatial_dates(geo.get('verified_at_utc'),'/raw/' in x['path']))
 for activity in pv['activities']:
  activity['input_datasets']=dm[activity['output_dataset']]['derived_from']
  if 'frozen-evidence' in activity['output_dataset']:activity['status']='Consumes/validates frozen snapshots; creation process not established'
 for x in am.values():
  if any(p not in am and p not in nodeids for p in x['derived_from']):raise ValueError('Unbound corrected parent')
 write(A/'catalogue/artifacts.json',artifacts);write(A/'catalogue/datasets.json',datasets);write(A/'catalogue/provenance.json',pv)
 approved=[x for x in am.values() if x['included_in_v1']];exceptions=[]
 for x in am.values():
  if x['included_in_v1']:continue
  reason='Authored grant/publication scope requires approval' if x['publication_decision']=='Original authored material' else 'Exact source/channel rights or item-level lineage not established; metadata only in new candidate.'
  exceptions.append(dict(artifact_id=x['id'],path=x['path'],collection_id=x['collection_id'],decision=x['publication_decision'],reason=reason,reproducibility_required=x['required_for_reproducibility']))
 old_assets={x['collection_id']:x for x in master['assets']}
 master['exceptions']=exceptions;master['assets']=[]
 for i,title in enumerate(TITLES,1):
  cid=f'{i:02}';members=[x for x in approved if x['collection_id']==cid];cm=dict(schema_version='1.0.0',archive_version='1.0.0',collection_id=cid,files=[dict(path=x['path'],bytes=x['bytes'],sha256=x['sha256'],artifact_id=x['id'],dataset_id=x['dataset_ids'][0],rights_id=x['rights_id'],publication_decision=x['publication_decision']) for x in members])
  cm_path=A/f'releases/v1.0.0/collections/{cid}.json';unchanged=cm_path.is_file() and read(cm_path)==cm
  write(cm_path,cm)
  if members and unchanged and cid in old_assets:master['assets'].append(old_assets[cid])
  elif members:master['assets'].append(dict(name=f'kai-tak-archive-v1.0.0-collection-{cid}.tar.gz',collection_id=cid,bytes=0,sha256='0'*64,files=len(members),unpacked_bytes=sum(x['bytes'] for x in members),url=None,manifest=f'collections/{cid}.json'))
  meta=read(A/f'collections/{cid}/collection.json');meta['permitted_bundle_files']=len(members);write(A/f'collections/{cid}/collection.json',meta)
  p=A/f'collections/{cid}/README.md';t=p.read_text();t=re.sub(r'\d+ verified-permitted files',f'{len(members)} verified-permitted files',t)
  for d in dm.values():
   # Keep each displayed dataset count synchronized without rewriting scientific prose.
   if d['collection_id']==cid:
    pat=r'(\*\*ID:\*\* `'+re.escape(d['id'])+r'`[\s\S]*?New candidate includes )\d+( matched permitted files\.)';t=re.sub(pat,lambda m:m[1]+str(d['permitted_bundle_files'])+m[2],t)
  p.write_text(t)
  p=A/'CATALOGUE.md';t=p.read_text();t=re.sub(r'(\| \['+cid+r'[^\n]+?\| \d+ \| )\d+( \|)',lambda m:m[1]+str(len(members))+m[2],t);p.write_text(t)
 write(A/'releases/v1.0.0/manifest.json',master)
 for filename,rows,fields in [('artifacts.csv',list(am.values()),['id','path','bytes','sha256','collection_id','processing_level','publication_decision','rights_id','provenance_status','included_in_v1']),('datasets.csv',list(dm.values()),['id','collection_id','title','file_count','total_bytes','permitted_bundle_files','represented_epoch','scientific_verification_status','provenance_completeness'])]:
  with (A/'catalogue'/filename).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
 write(A/'reports/catalogue_generation.json',dict(artifacts=len(am),datasets=len(dm),sources=len(read(A/'catalogue/sources.json')['sources']),permitted_files=len(approved),permitted_bytes=sum(x['bytes'] for x in approved),exceptions=len(exceptions),provenance_status_counts=dict(collections.Counter(x['provenance_status'] for x in am.values())),rights_counts=dict(collections.Counter(x['publication_decision'] for x in am.values())),supplemental_lineage_edges=len(lineage['edges']),virtual_member_and_version_nodes=len(nodeids)))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);refine(p.parse_args().source_root)
