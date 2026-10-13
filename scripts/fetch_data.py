#!/usr/bin/env python3
"""Download, verify and restore research data without conflicting overwrites.

No --release/--collection retains the historical five-group snapshot selection.
Use --list to discover archive releases; --release v1.0.0 selects the new series.
Local candidates have no download URL until an explicitly authorized publication.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tarfile
import uuid
from archive_io import (ArchiveError, atomic_json, directory, obtain_bundle,
                        preflight_destination, records_by_path, restore_bundle,
                        safe_path, read_json, load_policy, validate_collection_policy)

ROOT = Path(__file__).resolve().parents[1]


def release_plan(root, release=None, selected=None):
    selected = set(selected or [])
    if not release and not selected:
        master = json.loads((root / 'publication/release_assets.json').read_text())
        snapshot = json.loads((root / 'publication/snapshot_manifest.json').read_text())
        pairs = [(a, [r for r in snapshot['included'] if r['delivery'] == a['delivery']]) for a in master['assets']]
        return 'legacy:' + master['release_tag'], pairs, snapshot.get('excluded', [])
    release = release or 'v1.0.0'
    if len(safe_path(release)) != 1:
        raise ArchiveError('Invalid release identifier')
    release_dir = root / 'archive/releases' / release
    master = read_json(release_dir / 'manifest.json')
    if release != 'v' + master['archive_version']:
        raise ArchiveError('Release identifier/version mismatch')
    if master.get('schema_version') != '1.0.0' or master.get('status') not in ('candidate', 'published'):
        raise ArchiveError('Unsupported release schema or status')
    policy = load_policy(root)
    known = {f'{i:02d}' for i in range(1, 10)}
    if selected - known:
        raise ArchiveError('Unknown collection(s): ' + ', '.join(sorted(selected - known)))
    pairs = []
    seen = set()
    for asset in master['assets']:
        cid = asset['collection_id']
        if cid not in known or cid in seen:
            raise ArchiveError('Duplicate/invalid asset collection')
        seen.add(cid)
        if selected and cid not in selected:
            continue
        parts = safe_path(asset['manifest'])
        if asset['manifest'] != 'collections/' + cid + '.json':
            raise ArchiveError('Asset must reference its numbered collection manifest')
        collection = read_json(release_dir.joinpath(*parts))
        if collection['collection_id'] != cid or collection['archive_version'] != master['archive_version'] or collection['schema_version'] != master['schema_version']:
            raise ArchiveError('Collection/master identity or schema mismatch')
        validate_collection_policy(collection, policy)
        pairs.append((asset, collection['files']))
    exceptions = [e for e in master.get('exceptions', []) if not selected or not isinstance(e, dict) or not e.get('collection_id') or e['collection_id'] in selected]
    for cid in sorted((selected or known) - seen):
        if any(x.get('included_in_v1') and x.get('collection_id') == cid for x in policy[1].values()):
            raise ArchiveError('Missing bundle for permitted catalogue members: ' + cid)
        exceptions.append({'collection_id': cid, 'category': 'no-permitted-bundle', 'detail': 'Catalogue only; no approved bundle is available for this collection.'})
    return release, pairs, exceptions


def list_releases(root):
    result = []
    for path in sorted((root / 'archive/releases').glob('*/manifest.json')):
        master = json.loads(path.read_text())
        result.append({'release': path.parent.name, 'status': master['status'],
                       'collections': [{'id': f'{i:02d}', 'bundles': [a['name'] for a in master['assets'] if a['collection_id'] == f'{i:02d}']} for i in range(1, 10)]})
    return {'legacy': 'No --release preserves publication/release_assets.json selection', 'archive_releases': result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='list releases and all nine collection IDs')
    parser.add_argument('--release', help='archive series version, for example v1.0.0')
    parser.add_argument('--collection', action='append', help='stable ID 01–09; repeat to select multiple')
    parser.add_argument('--archive-dir', type=Path, default=ROOT / '.data-downloads')
    parser.add_argument('--destination', type=Path, default=ROOT)
    parser.add_argument('--verify-only', action='store_true', help='verify archives/members without extraction or destination mutation')
    parser.add_argument('--offline', action='store_true', help='use verified local bundle cache only')
    parser.add_argument('--report', type=Path, help='write machine-readable integrity report (refuses existing files)')
    args = parser.parse_args(argv)
    if args.list:
        print(json.dumps(list_releases(ROOT), indent=2))
        return 0
    report = {'schema_version': '1.0.0', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'operation': 'verify' if args.verify_only else 'restore', 'status': 'incomplete',
              'assets': [], 'exceptions': [], 'scientific_scope': 'Byte integrity only; not historical accuracy, full research reproducibility or aviation safety.'}
    try:
        release, pairs, exceptions = release_plan(ROOT, args.release, args.collection)
        report.update(release=release, exceptions=exceptions)
        all_records = [row for _, rows in pairs for row in rows]
        records_by_path(all_records)
        # Verify every selected asset before any destination write.
        cached = [(obtain_bundle(args.archive_dir, asset, rows, args.offline), asset, rows) for asset, rows in pairs]
        if not args.verify_only:
            preflight_destination(args.destination, all_records)
        for path, asset, rows in cached:
            if not args.verify_only:
                restore_bundle(path, asset, rows, args.destination)
            report['assets'].append({'name': asset['name'], 'sha256': asset['sha256'], 'files': len(rows), 'status': 'verified' if args.verify_only else 'restored'})
            print(('Verified' if args.verify_only else 'Restored'), asset['name'], len(rows), 'files', flush=True)
        report['status'] = ('verified' if args.verify_only else 'restored') if cached else 'catalogue-only'
        report['archive_coverage'] = 'exceptions-remain' if exceptions else 'selected-bundles-complete'
        if exceptions:
            print(f'{len(exceptions)} missing/restricted/catalogue-only exceptions; inspect the integrity report or release manifest.', file=sys.stderr)
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        if not args.verify_only:
            receipt = args.destination / '.archive-receipts' / (uuid.uuid4().hex + '.json')
            atomic_json(receipt, report)
            print('Receipt:', receipt)
        if args.report:
            atomic_json(args.report, report)
        print(json.dumps(report, indent=2))
        return 0
    except (ArchiveError, OSError, ValueError, KeyError, EOFError, tarfile.TarError) as exc:
        report.update(status='failed', error=str(exc), finished_utc=datetime.now(timezone.utc).isoformat())
        if args.report:
            try:
                atomic_json(args.report, report)
            except (OSError, ArchiveError) as report_error:
                print('Could not write report:', report_error, file=sys.stderr)
        print(json.dumps(report, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
