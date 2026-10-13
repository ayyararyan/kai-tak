#!/usr/bin/env python3
"""Validate metadata, release identity, lineage and optional installed bytes."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from archive_io import ArchiveError, digest, records_by_path, safe_path

ROOT = Path(__file__).resolve().parents[1]
LINEAGE_RELATIONS = {'derived-from', 'extracted-from', 'generated-by',
                     'frozen-snapshot-of', 'depends-on-exact-version'}


def load(path):
    return json.loads(path.read_text())


def acyclic(graph):
    """Kahn's algorithm also covers virtual nodes, without recursion limits."""
    degrees = {node: 0 for node in graph}
    for parents in graph.values():
        for parent in parents:
            degrees[parent] = degrees.get(parent, 0) + 1
    ready = collections.deque(n for n, degree in degrees.items() if degree == 0)
    visited = 0
    while ready:
        node = ready.popleft()
        visited += 1
        for parent in graph.get(node, ()):
            degrees[parent] -= 1
            if degrees[parent] == 0:
                ready.append(parent)
    return visited == len(degrees)


def validate(root=ROOT, data_root=None):
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        raise SystemExit('Install archive/requirements-archive.txt for metadata validation')
    root = Path(root)
    a = root / 'archive'
    errors, warnings, checks = [], [], []

    def check(ok, label, detail=None):
        checks.append({'check': label, 'passed': bool(ok)})
        if not ok:
            errors.append({'category': 'archive-integrity', 'check': label, 'detail': detail})

    def result():
        return dict(schema_version='1.0.0', status='failed' if errors else 'passed',
                    mode='installed-permitted-data' if data_root else 'metadata-only',
                    checks=len(checks), checks_passed=sum(c['passed'] for c in checks),
                    errors=errors, warnings=warnings, warning_count=len(warnings),
                    full_provenance_complete=not warnings and not errors,
                    scientific_validation='Not established by archive-integrity checks',
                    publication_ready=False)

    files = {'catalogue/artifacts.json': 'artifacts', 'catalogue/datasets.json': 'datasets',
             'catalogue/sources.json': 'sources', 'licensing/rights_registry.json': 'rights',
             'catalogue/provenance.json': 'provenance', 'releases/v1.0.0/manifest.json': 'release'}
    for c in range(1, 10):
        files[f'collections/{c:02}/collection.json'] = 'collection'
        files[f'releases/v1.0.0/collections/{c:02}.json'] = 'collection-manifest'
    documents = {}
    for path, name in files.items():
        try:
            schema = load(a / f'schemas/{name}.schema.json')
            Draft202012Validator.check_schema(schema)
            documents[path] = load(a / path)
            failures = list(Draft202012Validator(schema).iter_errors(documents[path]))
            check(not failures, 'schema:' + path, [e.message for e in failures[:5]])
        except (ValueError, OSError) as exc:
            check(False, 'schema:' + path, str(exc))
    # Do not dereference malformed documents after recording a schema failure.
    if errors:
        return result()
    arts = documents['catalogue/artifacts.json']['artifacts']
    ds = documents['catalogue/datasets.json']['datasets']
    ss = documents['catalogue/sources.json']['sources']
    rr = documents['licensing/rights_registry.json']['records']
    pv = documents['catalogue/provenance.json']
    master = documents['releases/v1.0.0/manifest.json']
    indexes = []
    for label, rows in [('artifacts', arts), ('datasets', ds), ('sources', ss), ('rights', rr),
                        ('edges', pv['edges']), ('activities', pv['activities']), ('nodes', pv.get('nodes', []))]:
        check(len(rows) == len({r['id'] for r in rows}), 'unique-ids:' + label)
        indexes.append({r['id']: r for r in rows})
    am, dm, sm, rm, em, tm, nodes = indexes
    check(not (set(am) & set(nodes)), 'unique-artifact-node-identities')
    try:
        # Unavailable catalogue artifacts can have unknown hashes; check path collisions separately.
        records_by_path([{'path': x['path'], 'bytes': 0, 'sha256': '0' * 64} for x in arts])
        check(True, 'catalogue-path-safety')
    except ArchiveError as exc:
        check(False, 'catalogue-path-safety', str(exc))
    bundled = []
    for x in arts:
        label = x['id']
        check(all(d in dm for d in x['dataset_ids']), 'dataset-ref:' + label)
        check(all(s in sm for s in x['source_ids']), 'source-ref:' + label)
        check(x['rights_id'] in rm, 'rights-ref:' + label)
        check(all(p in am or p in nodes for p in x['derived_from']), 'parent-ref:' + label)
        check(all(label in dm[d]['artifact_ids'] for d in x['dataset_ids'] if d in dm), 'artifact-dataset-membership:' + label)
        if x['rights_id'] in rm:
            check(x['publication_decision'] == rm[x['rights_id']]['publication_decision'], 'rights-decision:' + label)
        if x['included_in_v1']:
            bundled.append(x)
            check(x['publication_decision'] == 'Redistribution permitted' and x['sha256'] and
                  x['provenance_status'] in ('source-and-checksum-bound', 'pinned-source-and-output-hashes', 'producer-reassembly-byte-identical') and not x['symlink'], 'inclusion-policy:' + label)
            check(not re.search(r'(?i)(queue_state|enquiry_draft|request_drafts|\.venv|__pycache__|/v3/|session|token)', x['path']), 'private-path-policy:' + label)
            check(bool(x.get('source_url') or x['derived_from'] or x.get('acquisition_id')), 'permitted-source-chain:' + label)
        elif x['provenance_status'] in ('dataset-level-only', 'authorship-proposed-exact-upstream-review-pending'):
            warnings.append({'category': 'provenance', 'artifact_id': label, 'status': x['provenance_status']})
    for d in ds:
        check(len(d['artifact_ids']) == len(set(d['artifact_ids'])) and all(x in am for x in d['artifact_ids']), 'dataset-artifacts:' + d['id'])
        check(all(x in dm for x in d['derived_from']), 'dataset-lineage:' + d['id'])
        check(all(x in rm for x in d['rights_ids']), 'dataset-rights:' + d['id'])
        members = [am[x] for x in d['artifact_ids'] if x in am]
        check(all(d['id'] in x['dataset_ids'] for x in members), 'dataset-artifact-membership:' + d['id'])
        check(d['file_count'] == len(members), 'dataset-count:' + d['id'])
        check(d['total_bytes'] == sum(x['bytes'] for x in members), 'dataset-bytes:' + d['id'])
        check(d['permitted_bundle_files'] == sum(x['included_in_v1'] for x in members), 'dataset-permitted-count:' + d['id'])
        for script in d['producer_scripts']:
            check((root / script).is_file(), 'producer-script:' + script)
        if any(word in d['id'] for word in ['modern-buildings', 'dtm5']):
            check('1993' not in (d.get('represented_epoch') or '') or bool(d['limitations']), 'historical-modern-distinction:' + d['id'])
        if d['id'] in ('kt-modern-buildings', 'kt-dtm5-original', 'kt-stereo-points', 'kt-stereo-mesh'):
            check(bool(d['horizontal_crs']) and bool(d['vertical_datum']), 'geospatial-frame:' + d['id'])
    for s in ss:
        check(s['rights_id'] in rm and bool(s['required_attribution']), 'source-rights:' + s['id'])
        if s['rights_id'] in rm:
            check(s['rights_status'] == rm[s['rights_id']]['publication_decision'], 'source-rights-decision:' + s['id'])
    graph = {identifier: set() for identifier in set(am) | set(nodes)}
    attributed = set()
    for e in pv['edges']:
        subject, obj = e['subject'], e['object']
        check(subject in graph and (obj in sm if e['relation'] == 'attributed-to-source' else obj in graph), 'edge-ref:' + e['id'])
        if e['relation'] == 'attributed-to-source':
            attributed.add((subject, obj))
        elif e['relation'] in LINEAGE_RELATIONS:
            graph.setdefault(subject, set()).add(obj)
    for x in arts:
        graph[x['id']].update(x['derived_from'])
        check({s for subject, s in attributed if subject == x['id']} == set(x['source_ids']), 'source-attribution-binding:' + x['id'])
    check(acyclic(graph), 'acyclic-artifact-lineage')
    check(acyclic({d['id']: set(d['derived_from']) for d in ds}), 'acyclic-dataset-lineage')
    for t in pv['activities']:
        check(t['output_dataset'] in dm and all(x in dm for x in t['input_datasets']) and all(x in sm for x in t['source_ids']), 'activity-ref:' + t['id'])
    rows = []
    version = master['archive_version']
    check(len(master['assets']) == len({x['name'] for x in master['assets']}), 'unique-asset-names')
    check(len(master['assets']) == len({x['collection_id'] for x in master['assets']}), 'unique-asset-collections')
    for c in range(1, 10):
        cid = f'{c:02}'
        cm = documents[f'releases/v1.0.0/collections/{cid}.json']
        meta = documents[f'collections/{cid}/collection.json']
        rows.extend(cm['files'])
        check(cm['collection_id'] == cid and cm['archive_version'] == version and cm['schema_version'] == master['schema_version'], 'collection-identity:' + cid)
        check(meta['id'] == cid and meta['release_manifest'] == f'../../releases/v1.0.0/collections/{cid}.json', 'collection-catalogue-identity:' + cid)
        check(len(meta['dataset_ids']) == len(set(meta['dataset_ids'])) and set(meta['dataset_ids']) == {d['id'] for d in ds if d['collection_id'] == cid}, 'collection-datasets:' + cid)
        check(meta['file_count'] == sum(x['collection_id'] == cid for x in arts) and meta['permitted_bundle_files'] == len(cm['files']), 'collection-catalogue-counts:' + cid)
        for f in cm['files']:
            x = am.get(f['artifact_id'])
            check(x is not None and x['included_in_v1'] and x['collection_id'] == cid and
                  all(f[k] == x[k] for k in ('path', 'bytes', 'sha256', 'rights_id', 'publication_decision')) and
                  bool(x['dataset_ids']) and f['dataset_id'] == x['dataset_ids'][0] and f['dataset_id'] in dm and
                  dm[f['dataset_id']]['collection_id'] == cid, 'manifest-catalogue-binding:' + f['artifact_id'])
        matching = [x for x in master['assets'] if x['collection_id'] == cid]
        check(len(matching) == int(bool(cm['files'])), 'collection-asset-count:' + cid)
        for asset in matching:
            check(asset['manifest'] == f'collections/{cid}.json' and asset['name'] == f'kai-tak-archive-v{version}-collection-{cid}.tar.gz', 'asset-collection-binding:' + cid)
            check(asset['files'] == len(cm['files']) and asset['unpacked_bytes'] == sum(f['bytes'] for f in cm['files']), 'asset-member-totals:' + cid)
            check(asset['bytes'] > 0 and asset['sha256'] != '0' * 64, 'asset-built:' + cid)
    try:
        records_by_path(rows)
        check(True, 'release-path-safety')
    except ArchiveError as exc:
        check(False, 'release-path-safety', str(exc))
    check(len(rows) == len(bundled) and {x['artifact_id'] for x in rows} == {x['id'] for x in bundled}, 'release-complete-member-set')
    check(len(master['exceptions']) == len({e['artifact_id'] for e in master['exceptions']}) and {e['artifact_id'] for e in master['exceptions']} == {x['id'] for x in arts if not x['included_in_v1']}, 'explicit-exceptions-complete')
    for e in master['exceptions']:
        x = am.get(e['artifact_id'])
        check(x is not None and all(e[k] == x[k] for k in ('path', 'collection_id')) and e['decision'] == x['publication_decision'] and e['reproducibility_required'] == x['required_for_reproducibility'], 'exception-catalogue-binding:' + e['artifact_id'])
    expected_checksums = {x['name']: x['sha256'] for x in master['assets']}
    try:
        check(load(a / 'releases/v1.0.0/checksums.json') == expected_checksums, 'checksums-json-binding')
        sums = {}
        for line in (a / 'releases/v1.0.0/SHA256SUMS').read_text().splitlines():
            match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
            if not match or match[2] in sums:
                raise ValueError('Malformed or duplicate SHA256SUMS record')
            sums[match[2]] = match[1]
        check(sums == expected_checksums, 'sha256sums-binding')
        proposed = load(a / 'preservation/zenodo-version-draft.json')['proposed_files']
        check(len(proposed) == len(expected_checksums) and {x['name']: (x['sha256'], x['bytes']) for x in proposed} == {x['name']: (x['sha256'], x['bytes']) for x in master['assets']}, 'preservation-files-binding')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        check(False, 'release-dependent-metadata', str(exc))
    check(master['status'] == 'candidate' and master.get('doi') is None and master.get('concept_doi') is None, 'unpublished-no-fabricated-doi')
    try:
        for u in load(a / 'catalogue/publication_usage.json')['usages']:
            p = root / u['text_path']
            check(u['dataset_id'] in dm and p.is_file(), 'publication-use:' + u['dataset_id'])
            if p.is_file():
                check(u['latex_section_label'] in p.read_text(), 'publication-label:' + u['latex_section_label'])
    except (OSError, ValueError, KeyError) as exc:
        check(False, 'publication-usage', str(exc))
    if data_root:
        for x in bundled:
            try:
                p = Path(data_root) / x['path']
                ok = digest(p) == x['sha256'] and p.stat().st_size == x['bytes']
            except (ArchiveError, OSError):
                ok = False
            check(ok, 'installed-byte-integrity:' + x['id'])
    return result()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = validate(data_root=args.data_root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'warnings'}, indent=2))
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
