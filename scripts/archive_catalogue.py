#!/usr/bin/env python3
"""Generate the additive archive catalogue from frozen audit inputs; never alter evidence."""
import argparse,csv,fnmatch,hashlib,json,collections,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'archive'; P='research/checkers-runway13/'
TITLES=['Historical Maps and Aerial Photography','Historical Buildings and Urban Geography','Terrain and Geospatial Data','Aviation and Flight Evidence','Weather and Meteorological Records','Three-Dimensional Reconstruction','Mathematical Models and Results','Research Figures and Visualizations','Documentation and Research Publications']
RIGHTS={'src-hk-historical-survey':'rights.hk.old-survey-sheets','src-hk-aerial-index':'rights.hk.hkms-index-preview','src-hk-dap-l0':'rights.hk.dap-l0','src-hk-building-20260921':'rights.hk.csdi-building','src-hk-building-works':'rights.hk.csdi-building','src-hk-dtm5':'rights.hk.dtm5m','src-cad-1-95':'rights.cad.report-1-95','src-noaa-isd450070-1993':'rights.noaa.isd','src-noaa-isd-format':'rights.unresolved','src-hk-geodetic-transform':'rights.hk.geodetic-docs','src-boeing-747400':'rights.boeing.manual-drawing','src-hk-aip20261001':'rights.cad.ais','src-grs-catalogue':'rights.grs.records','src-aryan-research':'rights.original','src-scholarly-literature':'rights.unresolved','src-unresolved':'rights.unresolved'}
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def aid(p):return 'artifact-'+hashlib.sha256(p.encode()).hexdigest()[:20]
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def require_candidate(archive_root):
 """Refuse any generation/refinement before writes to a non-candidate release."""
 manifest=read(archive_root/'releases/v1.0.0/manifest.json')
 if manifest.get('status')!='candidate':
  raise ValueError('Only an unpublished candidate may be regenerated or refined')
 return manifest

def geospatial_dates(verified_at,raw):
 """A verification receipt establishes an upper bound, never an exact acquisition."""
 return dict(acquisition_date=None,generation_date=None,verification_date=verified_at,
             acquisition_no_later_than=verified_at if raw else None,
             generation_no_later_than=None if raw else verified_at,
             date_qualification='Exact acquisition/generation time unknown; source manifest verification establishes only the stated upper bound.')

def scientific_status_from_evidence(item,roots):
 """Read only checksum-matched canonical JSON, including frozen evidence copies."""
 if Path(item['path']).suffix=='.json' and item.get('sha256'):
  for root in roots:
   p=root/item['path']
   if not p.is_file() or p.is_symlink() or p.stat().st_size>10_000_000:continue
   if digest(p)!=item['sha256']:continue
   try:value=read(p)
   except (ValueError,UnicodeError):continue
   if not isinstance(value,dict):continue
   if value.get('invalidated') is True or value.get('result')=='invalidated_do_not_use':
    item['scientific_verification_status']='invalidated; retained for provenance; do not use as an accepted result'
    item['scientific_status_evidence']=dict(path=item['path'],sha256=item['sha256'],invalidated=value.get('invalidated'),result=value.get('result'),reason=value.get('invalidation_reason'))
   elif value.get('result')=='unresolved_budget_exhausted':
    item['scientific_verification_status']='unresolved; search budget exhausted; no complete exclusion established'
    item['scientific_status_evidence']=dict(path=item['path'],sha256=item['sha256'],result=value['result'],complete_exclusion=value.get('complete_exclusion'))
   return

def category(p):
 if '/whitepaper/' in p:return '09'
 if '/noaa/' in p or '/weather_' in p or '/wind/' in p:return '05'
 if '/structures/' in p or '/obstacles/' in p:return '02'
 if '/geospatial/' in p:return '03'
 if '/chronology/' in p or '/downloads/' in p:return '01'
 if '/reconstruction/' in p:return '06'
 if '/evidence/' in p or p.startswith('data/'):return '04'
 if '/figures/' in p or p.startswith('assets/'):return '08'
 if p.endswith(('.md','.tex','.bib')) or p.startswith('publication/'):return '09'
 return '07'
def isprivate(p):return any(x in p.lower() for x in ['queue_state_private','enquiry_draft','request_drafts','handoff_task','/whitepaper/v3/','change_snapshot.txt'])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source-root',type=Path,required=True,help='Read-only original evidence root');args=ap.parse_args()
 require_candidate(A)
 rights=read(A/'licensing/rights_registry.json');rm={r['id']:r for r in rights['records']}
 if 'rights.unresolved' not in rm:
  r=dict(id='rights.unresolved',title='Unresolved or mixed item-specific rights',publication_decision='Rights unresolved',scope='No new byte redistribution until exact provenance and rights are resolved.',verification_date='2026-10-13',evidence_ids=[],official_terms_urls=[],required_attribution='Identify original creator and all upstream sources before reuse.',rights_basis='Insufficient item-specific evidence; public visibility is not permission.',derivative_conditions='Review upstream expression and contributions.',representative_paths=[],outstanding_questions=['Resolve item-specific provenance and authorship.'],selection_rule='Never auto-include.')
  rights['records'].append(r);rm[r['id']]=r
 write(A/'licensing/rights_registry.json',rights)
 ds=read(A/'catalogue/dataset_definitions.json')['datasets'];sources=read(A/'catalogue/source_definitions.json')['sources']
 sources.append(dict(id='src-unresolved',title='Unresolved item-specific source',creator=None,urls=[],local_evidence=[],date_semantics='Unknown; no source identity inferred.'))
 sm={s['id']:s for s in sources}
 for s in sources:
  s['rights_id']=RIGHTS[s['id']];s['rights_status']=rm[s['rights_id']]['publication_decision'];s['landing_page_url']=s['urls'][0] if s['urls'] else None
  s['publication_date']=s.get('publication_date');s['observation_date']=s.get('observation_date',s.get('capture_date'));s['revision_date']=s.get('revision_date');s['acquisition_date']=s.get('acquired_date');s['source_version']=s.get('revision_date');s['required_attribution']=rm[s['rights_id']]['required_attribution']
 # Distinguish previews from the permitted full-frame product, even if visual subjects coincide.
 for d in ds:
  if d['id']=='kt-aerial-previews':d['source_ids']=['src-hk-aerial-index']
  d['artifact_ids']=[];d['related_publications']=['Checkers with Runway 13, v2 (frozen manuscript; no archive version equivalence)'];d['citation']=f"Ayyar, Aryan (2026). {d['title']}. The Kai Tak Historical Research Archive, candidate v1.0.0, dataset {d['id']}. No DOI assigned."
  d['rights_ids']=sorted({RIGHTS[s] for s in d['source_ids']});d['rights_decision']='Mixed/source-specific; see artifact decisions';d['publication_date']=None;d['observation_date']=d.get('represented_epoch');d['acquisition_date']=d.get('acquired_or_generated_date');d['generated_date']=None;d['source_revision_date']=None
  d['scientific_purpose']=d['description'];d['creator']=[sm[s]['creator'] for s in d['source_ids'] if sm[s].get('creator')];d['download']='Candidate collection manifest; publication URL not assigned';d['formats']=[]
 # Supporting files stay discoverable but unknown lineage is never upgraded by a path heuristic.
 for c,title in enumerate(TITLES,1):
  ds.append(dict(id=f'kt-support-{c:02}',collection_id=f'{c:02}',title=title+' — supporting and unclassified artifacts',description='Ancillary reports, scripts and outputs; consult file-level provenance gaps.',scientific_purpose='Retain evidence and identify incomplete metadata.',path_patterns=[],source_ids=['src-unresolved'],processing_level='mixed/unclassified',represented_epoch=None,observation_date=None,acquisition_date=None,publication_date=None,generated_date=None,source_revision_date=None,quantity={},producer_scripts=[],verification_evidence=[],scientific_verification_status='Not independently verified',limitations=['Directory classification is navigational, not a verified source or transformation chain.'],derived_from=[],horizontal_crs=None,vertical_datum=None,geographic_coverage=None,rights_ids=['rights.unresolved'],rights_decision='Mixed/source-specific; see artifact decisions',reproducibility_required=None,artifact_ids=[],creator=[],related_publications=['Checkers with Runway 13'],citation=f'Ayyar, Aryan (2026). Collection {c:02}, candidate v1.0.0.',download='Metadata only unless artifact explicitly included.',formats=[]))
 dm={d['id']:d for d in ds}
 inventory=read(A/'audit/initial_inventory.json')['files'];locs=collections.defaultdict(list)
 for r in inventory:locs[r['path']].append(r)
 snap=read(ROOT/'publication/snapshot_manifest.json');records={x['path']:dict(x) for x in snap['included']}
 for x in snap['excluded']:
  if not isprivate(x['path']):records.setdefault(x['path'],dict(x,delivery='not-published'))
 for r in inventory:
  if r['storage']=='remote-checkout':records.setdefault(r['path'],dict(path=r['path'],bytes=r['size'],sha256=r['sha256'],delivery='git'))
  elif r['storage'] in ('research-workspace','data-workspace') and not isprivate(r['path']):records.setdefault(r['path'],dict(path=r['path'],bytes=r['size'],sha256=r['sha256'],delivery='local-only',symlink=r['symlink']))
 accessions=read(A/'catalogue/accessions.json')['accessions']; struct=read(A/'catalogue/structure_acquisitions.json')['acquisitions'];exact={}
 for ac in accessions:
  rid=RIGHTS[ac['source_id']];exact[ac['artifact_path']]={'rights_id':rid,'source_ids':[ac['source_id']],'dataset_id':ac['dataset_id'],'sha256':ac['original_sha256'],'bytes':ac['original_size'],'acquisition_id':ac['id'],'acquired_at':ac['acquired_utc'],'observation_date':ac.get('observation_or_capture_date',ac.get('capture_date',ac.get('observation_or_survey_date'))),'publication_date':ac.get('publication_or_edition_date'),'source_url':ac.get('direct_download_url',ac.get('source_interface')),'processing_level':'downloaded','parents':[]}
 for ac in struct:
  exact[ac['artifact_path']]={'rights_id':'rights.hk.csdi-building','source_ids':[ac['source_id']],'dataset_id':ac['dataset_id'],'sha256':ac['expected_sha256'],'bytes':ac['expected_bytes'],'acquisition_id':ac['id'],'acquired_at':ac['acquired_utc'],'observation_date':None,'publication_date':None,'source_url':ac['source_url'],'processing_level':'downloaded','parents':[]}
 g=P+'geospatial/';geo=read(ROOT/(g+'manifest.json'))
 for f in geo['files']:
  if f['path'].startswith('raw/') or f['path'].startswith('derived/'):
   dtm='DTM' in f['path'];rid='rights.hk.dtm5m' if dtm else 'rights.hk.csdi-building';sid='src-hk-dtm5' if dtm else 'src-hk-building-20260921';raw=g+('raw/Whole_HK_DTM_5m.zip' if dtm else 'raw/Building_20260921.geojson')
   exact[g+f['path']]={'rights_id':rid,'source_ids':[sid],'dataset_id':'kt-dtm5-original' if dtm else 'kt-modern-buildings','sha256':f['sha256'],'bytes':f['bytes'],'acquisition_id':'geo-'+aid(f['path']),'acquired_at':None,'verified_at':geo.get('verified_at_utc'),'observation_date':'2014–2015' if dtm else None,'publication_date':'2017' if dtm else None,'source_url':f.get('source_url'),'processing_level':'downloaded' if f['path'].startswith('raw/') else 'transformed','parents':[] if f['path'].startswith('raw/') else [aid(raw)]}
 noaa=P+'evidence/weather_feasibility_2026-10-13/NOAA_450070-99999-1993.gz'; nr=records[noaa]
 exact[noaa]={'rights_id':'rights.noaa.isd','source_ids':['src-noaa-isd450070-1993'],'dataset_id':'kt-noaa-raw','sha256':'617c7db4f19c3aaacef91ae8a688c0aab196cdfc7ddfba72857c8e70056d66e0','bytes':nr['bytes'],'acquisition_id':'noaa-450070-99999-1993','acquired_at':'2026-10-13','observation_date':'1993','publication_date':None,'source_url':'https://www.ncei.noaa.gov/pub/data/noaa/1993/450070-99999-1993.gz','processing_level':'downloaded','parents':[]}
 artifacts=[]; approved=[];proposed=[];edges=[];exceptions=[]
 for path,r in sorted(records.items()):
  if isprivate(path):continue
  matches=[d for d in ds if any(fnmatch.fnmatchcase(path,p) for p in d.get('path_patterns',[]))]
  matches.sort(key=lambda d:max([len(p.split('*')[0]) for p in d.get('path_patterns',[]) if fnmatch.fnmatchcase(path,p)]+[0]),reverse=True)
  d=matches[0] if matches else dm['kt-support-'+category(path)]
  ids=[x['id'] for x in matches] or [d['id']];e=exact.get(path);h=r.get('sha256');bytes_=r['bytes']
  if not h:
   candidate=next((x for x in locs[path] if x['storage'] in ('research-workspace','data-workspace')),None)
   if candidate:h=candidate['sha256'];bytes_=candidate['size']
  rid='rights.unresolved';source_ids=d['source_ids'];processing=d['processing_level'];parents=[];prov='dataset-level-only';acquired=None;obs=None;pub=None;source_url=None;acq=None
  if e:
   if h!=e['sha256'] or bytes_!=e['bytes']:raise ValueError('Acquisition does not match canonical artifact: '+path)
   rid=e['rights_id'];source_ids=e['source_ids'];d=dm[e['dataset_id']];ids=list(dict.fromkeys([d['id']]+ids));processing=e['processing_level'];parents=e['parents'];prov='source-and-checksum-bound';acquired=e['acquired_at'];obs=e['observation_date'];pub=e['publication_date'];source_url=e['source_url'];acq=e['acquisition_id']
  elif path.endswith(('.py','.md','.tex','.bib')) and not any(s in path for s in ['/sources/','/downloads/','/raw/','/source_pages/']):
   rid='rights.original';source_ids=list(dict.fromkeys(['src-aryan-research']+([s for s in source_ids if s!='src-unresolved'])));prov='authorship-proposed-exact-upstream-review-pending';processing='original authored material'
  elif 'src-cad-1-95' in source_ids and (path.startswith('data/') or '/source_pages/' in path):rid='rights.cad.report-1-95'
  elif d['id'] in ('kt-aerial-index','kt-aerial-index-all-hk-1993','kt-aerial-previews'):rid='rights.hk.hkms-index-preview'
  decision=rm[rid]['publication_decision'];collection=d['collection_id'];identifier=aid(path)
  loc=[{'location':x['storage'],'sha256':x['sha256'],'bytes':x['size'],'matches_canonical':x['sha256']==h} for x in locs[path]]
  scientific='superseded-or-invalidated; retained for provenance' if any(z in path.lower() for z in ['/invalidated/','/invalidated_dense_lr_blend/']) else d['scientific_verification_status']
  item=dict(id=identifier,path=path,file_name=Path(path).name,extension=Path(path).suffix,bytes=bytes_,sha256=h,collection_id=collection,dataset_ids=ids,source_ids=source_ids,creator=[sm[s]['creator'] for s in source_ids if sm[s].get('creator')],acquisition_date=acquired,generation_date=None,observation_date=obs,publication_date=pub,source_revision_date=sm[source_ids[0]].get('revision_date') if source_ids else None,locations=loc,existing_delivery=r.get('delivery'),existing_version='integration-2026-10-13' if r.get('delivery') not in ('local-only','not-published') else None,processing_level=processing,rights_id=rid,publication_decision=decision,scientific_verification_status=scientific,provenance_status=prov,derived_from=parents,source_url=source_url,acquisition_id=acq,required_for_reproducibility=d.get('reproducibility_required'),producer_scripts=d.get('producer_scripts',[]),horizontal_crs=d.get('horizontal_crs'),vertical_datum=d.get('vertical_datum'),geographic_coverage=d.get('geographic_coverage'),limitations=d['limitations'],included_in_v1=bool(e),source_sha256=r.get('source_sha256'),symlink=bool(r.get('symlink')))
  if e and 'verified_at' in e:item.update(geospatial_dates(e['verified_at'],e['processing_level']=='downloaded'))
  if item['symlink']:item['included_in_v1']=False;item['publication_decision']='Excluded';item['rights_id']='rights.private'
  if e and item['included_in_v1']:
   q=args.source_root/path
   if not q.is_file() or q.is_symlink() or digest(q)!=h:raise ValueError('Missing/conflicting source bytes: '+path)
   approved.append(item)
  else:exceptions.append(dict(artifact_id=identifier,path=path,collection_id=collection,decision=item['publication_decision'],reason='Authored grant/publication scope requires approval' if rid=='rights.original' else 'Exact source/channel rights or item-level lineage not established; metadata only in new candidate.',reproducibility_required=item['required_for_reproducibility']))
  if rid=='rights.original':proposed.append(dict(path=path,sha256=h,candidate_license='MIT' if path.endswith('.py') else 'CC-BY-4.0',approved=False,authorship='Proposed based on research context; copied portions, contributions and upstream expression require confirmation.'))
  for did in ids:dm[did]['artifact_ids'].append(identifier)
  for sid in source_ids:edges.append(dict(id=f'edge-{identifier}-{sid}',relation='attributed-to-source',subject=identifier,object=sid,evidence_level=prov))
  for parent in parents:edges.append(dict(id=f'edge-{identifier}-{parent}',relation='derived-from',subject=identifier,object=parent,evidence_level='recorded-processing-and-hash-manifest'))
  artifacts.append(item)
 am={x['id']:x for x in artifacts}
 for d in ds:
  members=[am[i] for i in d['artifact_ids']];d['formats']=sorted({x['extension'] or 'no-extension' for x in members});d['file_count']=len(members);d['total_bytes']=sum(x['bytes'] for x in members);d['permitted_bundle_files']=sum(x['included_in_v1'] for x in members);d['source_links']=[u for sid in d['source_ids'] for u in sm[sid]['urls']];d['required_attribution']=[rm[x]['required_attribution'] for x in d['rights_ids']]
  d['provenance_completeness']='file-level-bound' if members and all(x['provenance_status']=='source-and-checksum-bound' for x in members) else 'partial; inspect artifact-level status'
 write(A/'catalogue/datasets.json',dict(schema_version='1.0.0',archive_version='1.0.0',status='candidate',datasets=ds));write(A/'catalogue/sources.json',dict(schema_version='1.0.0',sources=sources));write(A/'catalogue/artifacts.json',dict(schema_version='1.0.0',archive_version='1.0.0',artifacts=artifacts))
 activities=[]
 for d in ds:
  if d['producer_scripts']:
   activities.append(dict(id='activity-'+d['id'],output_dataset=d['id'],input_datasets=d['derived_from'],source_ids=d['source_ids'],scripts=d['producer_scripts'],evidence=d.get('chain_record_paths',d['verification_evidence']),status='recorded process; not all producer runs replayed',limitation='Dataset-level chain, not asserted all-to-all file dependence.'))
 # Explicit NOAA source-to-derived chain.
 for suffix in ['observations_1993.csv','observations_1993-11-04.csv']:
  target=aid(P+'evidence/cal605_reconstruction/noaa/'+suffix)
  if target in am:
   am[target]['derived_from']=[aid(noaa)];am[target]['provenance_status']='producer-replay-byte-identical';edges.append(dict(id='edge-noaa-'+suffix,relation='derived-from',subject=target,object=aid(noaa),evidence_level='fresh-byte-identical-producer-replay'))
 write(A/'catalogue/artifacts.json',dict(schema_version='1.0.0',archive_version='1.0.0',artifacts=artifacts));write(A/'catalogue/provenance.json',dict(schema_version='1.0.0',edges=edges,activities=activities))
 write(A/'licensing/proposed_scope.json',dict(status='DRAFT-NOT-A-GRANT',files=proposed,excluded=['Third-party content','Mixed/source-derived expression','Contributed homepage photograph','Any unconfirmed authorship']))
 byhash=collections.defaultdict(list)
 for x in artifacts:
  if x['sha256']:byhash[x['sha256']].append(x['path'])
 write(A/'audit/duplicates.json',dict(policy='Report only; no deletion or consolidation.',groups=[dict(sha256=h,paths=p) for h,p in sorted(byhash.items()) if len(p)>1]))
 with (A/'catalogue/artifacts.csv').open('w',newline='') as f:
  cols=['id','path','bytes','sha256','collection_id','processing_level','publication_decision','rights_id','provenance_status','included_in_v1'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(artifacts)
 with (A/'audit/old_to_catalogue.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['original_path','artifact_id','dataset_ids','collection_id','new_path']);w.writerows((x['path'],x['id'],';'.join(x['dataset_ids']),x['collection_id'],x['path']) for x in artifacts)
 with (A/'catalogue/datasets.csv').open('w',newline='') as f:
  cols=['id','collection_id','title','file_count','total_bytes','permitted_bundle_files','represented_epoch','scientific_verification_status','provenance_completeness'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(ds)
 assets=[]
 for i,title in enumerate(TITLES,1):
  c=f'{i:02}';members=[x for x in approved if x['collection_id']==c];cds=[d for d in ds if d['collection_id']==c];directory=A/'collections'/c;directory.mkdir(exist_ok=True)
  meta=dict(schema_version='1.0.0',id=c,title=title,dataset_ids=[d['id'] for d in cds],citation=f'Ayyar, Aryan (2026). {title}. The Kai Tak Historical Research Archive, candidate v1.0.0, collection {c}.',file_count=sum(x['collection_id']==c for x in artifacts),permitted_bundle_files=len(members),release_manifest=f'../../releases/v1.0.0/collections/{c}.json')
  write(directory/'collection.json',meta)
  page=f'# {c} — {title}\n\n'+meta['citation']+' **Unpublished candidate; no DOI assigned.**\n\n'
  page+=f'{meta["file_count"]} catalogued artifacts; {len(members)} verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.\n\n'
  page+='[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/'+c+'.json)\n\n'
  for d in cds:
   if not d['file_count']:continue
   page+=f'## {d["title"]}\n\n**ID:** `{d["id"]}`. {d["description"]}\n\n- Quantity: {json.dumps(d["quantity"],ensure_ascii=False)}; {d["file_count"]} catalogued files.\n- Epoch: {d["represented_epoch"] or "not established"}.\n- Processing: {d["processing_level"]}.\n- Verification: {d["scientific_verification_status"]}.\n- CRS / vertical datum: {d["horizontal_crs"] or "not applicable or unresolved"} / {d["vertical_datum"] or "not applicable or unresolved"}.\n- Limitations: '+ '; '.join(d['limitations'])+'\n- Source links: '+', '.join(f'[source {j+1}]({u})' for j,u in enumerate(d['source_links']))+'\n- Reuse: source-specific; consult artifact decisions. New candidate includes '+str(d['permitted_bundle_files'])+' matched permitted files.\n\n'
  (directory/'README.md').write_text(page)
  m=dict(schema_version='1.0.0',archive_version='1.0.0',collection_id=c,files=[dict(path=x['path'],bytes=x['bytes'],sha256=x['sha256'],artifact_id=x['id'],dataset_id=x['dataset_ids'][0],rights_id=x['rights_id'],publication_decision=x['publication_decision']) for x in members]);write(A/f'releases/v1.0.0/collections/{c}.json',m)
  if members:assets.append(dict(name=f'kai-tak-archive-v1.0.0-collection-{c}.tar.gz',collection_id=c,bytes=0,sha256='0'*64,files=len(members),unpacked_bytes=sum(x['bytes'] for x in members),url=None,manifest=f'collections/{c}.json',status='awaiting-local-build'))
 master=dict(schema_version='1.0.0',archive_version='1.0.0',status='candidate',title='Kai Tak Historical Research Archive — Data Release v1.0.0',source_commit='128f7006e8c929a878bd80bdf84521a97c45ee30',release_date=None,doi=None,concept_doi=None,complete_historical_archive=False,assets=assets,exceptions=exceptions,dependencies=['Source checkout at source_commit plus archive branch reviewed commit; see source_checkout.json','Restricted sources listed in catalogue; not bundled','No original-work license grants activated'],rights_notice='Source-specific terms remain; no institutional endorsement; see archive/licensing/ATTRIBUTION.md')
 write(A/'releases/v1.0.0/manifest.json',master)
 title='# The Kai Tak Historical Research Archive\n\n## Collection catalogue\n\n**Candidate v1.0.0, unpublished.** Counts distinguish artifacts from observations. Catalogue completeness and scientific completeness are separate.\n\n| Collection | Catalogued artifacts | Permitted bundle files |\n|---|---:|---:|\n'
 for i,t in enumerate(TITLES,1):
  c=f'{i:02}';title+=f'| [{c} — {t}](collections/{c}/README.md) | {sum(x["collection_id"]==c for x in artifacts)} | {sum(x["collection_id"]==c for x in approved)} |\n'
 title+='\n[Dataset JSON](catalogue/datasets.json) · [Dataset CSV](catalogue/datasets.csv) · [Artifact inventory](catalogue/artifacts.json) · [Source register](catalogue/sources.json) · [Provenance graph](catalogue/provenance.json) · [Download instructions](DOWNLOAD.md)\n\nEvery original path is retained. The [old-path mapping](audit/old_to_catalogue.csv) is a catalogue mapping, not a relocation. Metadata-only entries do not promise downloadable source bytes. Source-checksum binding is currently strongest for permitted raw data; other lineage gaps remain explicit.\n'
 (A/'CATALOGUE.md').write_text(title)
 attr='# Attribution and retained conditions\n\nNo source institution endorses the archive. Scientific usefulness and permission are independent. Full linked terms apply, including their disclaimers and conditions.\n\n'
 for r in rights['records']:attr+=f'## {r["title"]}\n\n{r["required_attribution"]}\n\nDecision: **{r["publication_decision"]}**. {r["scope"]}\n\n'+ ' · '.join(f'[Official terms {j+1}]({u})' for j,u in enumerate(r['official_terms_urls']))+'\n\n'
 (A/'licensing/ATTRIBUTION.md').write_text(attr)
 write(A/'reports/catalogue_generation.json',dict(artifacts=len(artifacts),datasets=len(ds),sources=len(sources),permitted_files=len(approved),permitted_bytes=sum(x['bytes'] for x in approved),exceptions=len(exceptions),provenance_status_counts=dict(collections.Counter(x['provenance_status'] for x in artifacts)),rights_counts=dict(collections.Counter(x['publication_decision'] for x in artifacts))))
 from archive_refine import refine
 refine(args.source_root)
 print(json.dumps(read(A/'reports/catalogue_generation.json'),indent=2))
if __name__=='__main__':main()
