"""Adversarial, deterministic-build and legacy-selection regression tests."""
import gzip
from contextlib import contextmanager
import hashlib
import http.server
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from archive_build import build_bundle
import archive_build
import archive_io
from archive_io import (ArchiveError, atomic_json, digest, obtain_bundle,
                        records_by_path, restore_bundle, safe_path, verify_bundle)
import fetch_data


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        # macOS /var is a symlink; tests explicitly choose its physical directory.
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'source'
        self.source.mkdir()
        self.cache = self.root / 'cache'
        self.cache.mkdir()
        self.dest = self.root / 'restored'
        self.rows = [self.row('research/a.txt', b'alpha'), self.row('data/b.txt', b'beta')]
        for row, body in zip(self.rows, [b'alpha', b'beta']):
            path = self.source / row['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)

    def tearDown(self):
        self.temp.cleanup()

    def row(self, path, body):
        return {'path': path, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                'artifact_id': 'artifact:' + path, 'dataset_id': 'dataset:test', 'rights_id': 'rights:test',
                'publication_decision': 'Redistribution permitted'}

    def good(self):
        asset = build_bundle(self.source, self.cache, 'test.tar.gz', self.rows)
        return self.cache / asset['name'], asset

    def policy(self, root, groups):
        artifacts, datasets, rights = [], {}, {}
        for cid, rows in groups.items():
            for row in rows:
                artifacts.append({**row, 'id': row['artifact_id'], 'dataset_ids': [row['dataset_id']],
                                  'collection_id': cid, 'included_in_v1': True, 'symlink': False,
                                  'provenance_status': 'source-and-checksum-bound'})
                datasets[row['dataset_id']] = {'id': row['dataset_id']}
                rights[row['rights_id']] = {'id': row['rights_id'], 'publication_decision': 'Redistribution permitted'}
        for relative, obj in [('catalogue/artifacts.json', {'archive_version': '1.0.0', 'artifacts': artifacts}),
                              ('catalogue/datasets.json', {'datasets': list(datasets.values())}),
                              ('licensing/rights_registry.json', {'records': list(rights.values())})]:
            path = root / 'archive' / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(obj))

    def build_fixture(self):
        root = self.root / 'repo'
        release = root / 'archive/releases/v1.0.0'
        (release / 'collections').mkdir(parents=True)
        groups = {'01': self.rows[:1], '02': self.rows[1:]}
        for number in range(1, 10):
            cid = f'{number:02}'
            (release / f'collections/{cid}.json').write_text(json.dumps({
                'schema_version': '1.0.0', 'archive_version': '1.0.0',
                'collection_id': cid, 'files': groups.get(cid, [])}))
        (release / 'manifest.json').write_text(json.dumps({
            'schema_version': '1.0.0', 'archive_version': '1.0.0', 'status': 'candidate', 'assets': []}))
        self.policy(root, groups)
        return root, release, ['--source-root', str(self.source), '--output-dir', str(self.cache)]

    def change_build_sources(self, root, release):
        for number, old in enumerate(self.rows, 1):
            body = f'new content {number}'.encode()
            (self.source / old['path']).write_bytes(body)
            self.rows[number - 1] = self.row(old['path'], body)
            path = release / f'collections/{number:02}.json'
            cm = json.loads(path.read_text())
            cm['files'] = [self.rows[number - 1]]
            path.write_text(json.dumps(cm))
        self.policy(root, {'01': self.rows[:1], '02': self.rows[1:]})

    def malicious(self, entries, rows=None):
        path = self.cache / 'bad.tar.gz'
        with tarfile.open(path, 'w:gz') as bundle:
            for name, body, kind in entries:
                member = tarfile.TarInfo(name)
                member.type = kind
                member.size = len(body) if kind == tarfile.REGTYPE else 0
                member.linkname = '../../outside'
                bundle.addfile(member, io.BytesIO(body))
        rows = rows or self.rows[:1]
        return path, {'name': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path),
                      'files': len(rows), 'unpacked_bytes': sum(r['bytes'] for r in rows)}, rows

    def assert_rejects(self, path, asset, rows):
        with self.assertRaises((ArchiveError, OSError, tarfile.TarError)):
            restore_bundle(path, asset, rows, self.dest)
        self.assertFalse((self.dest / self.rows[0]['path']).exists())

    def test_deterministic_build_and_restore(self):
        path, asset = self.good()
        second = self.root / 'second'
        other = build_bundle(self.source, second, asset['name'], list(reversed(self.rows)))
        self.assertEqual(asset, other)
        self.assertEqual(restore_bundle(path, asset, self.rows, self.dest), 2)
        self.assertEqual(restore_bundle(path, asset, self.rows, self.dest), 2)
        for row in self.rows:
            self.assertEqual(digest(self.dest / row['path']), row['sha256'])
        with tarfile.open(path) as tar:
            for member in tar:
                self.assertEqual((member.uid, member.gid, member.mtime, member.mode), (0, 0, 0, 0o644))

    def test_bad_member_hash_no_early_write(self):
        path, asset, rows = self.malicious([('research/a.txt', b'alpha', tarfile.REGTYPE), ('data/b.txt', b'evil', tarfile.REGTYPE)], self.rows)
        self.assert_rejects(path, asset, rows)

    def test_missing_member_no_early_write(self):
        self.assert_rejects(*self.malicious([('research/a.txt', b'alpha', tarfile.REGTYPE)], self.rows))

    def test_duplicate_member_rejected(self):
        self.assert_rejects(*self.malicious([('research/a.txt', b'alpha', tarfile.REGTYPE)] * 2))

    def test_symlink_hardlink_special_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE, tarfile.CHRTYPE, tarfile.DIRTYPE):
            with self.subTest(kind=kind):
                self.assert_rejects(*self.malicious([('research/a.txt', b'', kind)]))

    def test_unsafe_names(self):
        for name in ('../x', '/x', 'C:/x', 'x\\y', 'x//y', 'x/./y', 'x\n.txt', 'CON.txt', 'a./b', 'a /b', 'a\x00', '.git/config', '.archive-receipts/a.json'):
            with self.subTest(name=name), self.assertRaises(ArchiveError):
                safe_path(name)

    def test_path_casefold_unicode_and_prefix_collisions(self):
        for paths in [('a', 'A'), ('caf\u00e9', 'cafe\u0301'), ('a', 'a/b'), ('A/b', 'a')]:
            with self.subTest(paths=paths), self.assertRaises(ArchiveError):
                records_by_path([self.row(p, b'x') for p in paths])

    def test_conflicting_destination_preflight(self):
        path, asset = self.good()
        target = self.dest / self.rows[1]['path']
        target.parent.mkdir(parents=True)
        target.write_text('local work')
        self.assert_rejects(path, asset, self.rows)
        self.assertEqual(target.read_text(), 'local work')

    def test_symlink_destination_ancestor_rejected(self):
        path, asset = self.good()
        self.dest.mkdir()
        (self.dest / 'research').symlink_to(self.source / 'research', target_is_directory=True)
        with self.assertRaises(OSError):
            restore_bundle(path, asset, self.rows, self.dest)
        self.assertEqual((self.source / 'research/a.txt').read_bytes(), b'alpha')

    def test_symlink_destination_file_rejected(self):
        path, asset = self.good()
        (self.dest / 'research').mkdir(parents=True)
        (self.dest / 'research/a.txt').symlink_to(self.source / 'research/a.txt')
        with self.assertRaises(OSError):
            restore_bundle(path, asset, self.rows, self.dest)

    def test_symlink_cache_and_cache_ancestor_rejected(self):
        path, asset = self.good()
        alias = self.root / 'alias'
        alias.symlink_to(self.cache, target_is_directory=True)
        with self.assertRaises(OSError):
            obtain_bundle(alias, asset, self.rows, True)
        path.rename(self.cache / 'real')
        path.symlink_to(self.cache / 'real')
        with self.assertRaises(OSError):
            obtain_bundle(self.cache, asset, self.rows, True)

    def test_source_symlink_and_rights_rejected(self):
        source = self.source / self.rows[0]['path']
        source.rename(source.with_suffix('.original'))
        source.symlink_to(source.with_suffix('.original'))
        with self.assertRaises(OSError):
            self.good()
        source.unlink()
        source.with_suffix('.original').rename(source)
        self.rows[0]['publication_decision'] = 'Rights unresolved'
        with self.assertRaises(ArchiveError):
            self.good()

    def test_asset_counts_hash_and_size_mismatch(self):
        path, asset = self.good()
        for key, value in [('files', 3), ('unpacked_bytes', 300), ('bytes', 2), ('sha256', '0' * 64)]:
            with self.subTest(key=key), path.open('rb') as stream, self.assertRaises(ArchiveError):
                verify_bundle(stream, {**asset, key: value}, self.rows)

    def test_offline_missing(self):
        _, asset = self.good()
        with self.assertRaises(ArchiveError):
            obtain_bundle(self.root / 'empty', asset, self.rows, offline=True)

    def test_no_replace_reports_and_symlink_report(self):
        report = self.root / 'report.json'
        atomic_json(report, {'a': 1})
        with self.assertRaises(FileExistsError):
            atomic_json(report, {'a': 2})
        alias = self.root / 'report-alias.json'
        alias.symlink_to(report)
        with self.assertRaises(ArchiveError):
            atomic_json(alias, {}, replace=True)
        self.assertEqual(json.loads(report.read_text()), {'a': 1})

    def test_existing_candidate_refuses_different_bytes(self):
        path, asset = self.good()
        (self.source / self.rows[0]['path']).write_bytes(b'new')
        self.rows[0] = self.row(self.rows[0]['path'], b'new')
        with self.assertRaises(ArchiveError):
            self.good()
        self.assertEqual(digest(path), asset['sha256'])
        changed = build_bundle(self.source, self.cache, asset['name'], self.rows, rebuild=True)
        self.assertNotEqual(changed['sha256'], asset['sha256'])

    def test_generation_late_source_failure_preserves_prior_bundles_and_metadata(self):
        root, release, args = self.build_fixture()
        with patch.object(archive_build, 'ROOT', root), patch('sys.stdout', io.StringIO()):
            archive_build.main(args)
            old = {p: p.read_bytes() for p in [*self.cache.glob('*.tar.gz'), release / 'manifest.json', release / 'checksums.json']}
            self.change_build_sources(root, release)
            (self.source / self.rows[1]['path']).unlink()
            with self.assertRaises(FileNotFoundError):
                archive_build.main(args + ['--rebuild-candidate'])
        self.assertTrue(all(p.read_bytes() == data for p, data in old.items()))
        self.assertFalse(list(self.cache.glob('.archive-*')))
        self.assertFalse(list(release.glob('.archive-*')))

    def test_generation_commit_errors_roll_back_bundles_and_metadata(self):
        root, release, args = self.build_fixture()
        with patch.object(archive_build, 'ROOT', root), patch('sys.stdout', io.StringIO()):
            archive_build.main(args)
            old = {p: p.read_bytes() for p in [*self.cache.glob('*.tar.gz'), release / 'manifest.json', release / 'checksums.json']}
            self.change_build_sources(root, release)
            original = archive_build.os.replace
            for fail_target in ('kai-tak-archive-v1.0.0-collection-02.tar.gz', 'manifest.json'):
                failed = False
                def fail_once(src, dst, **kwargs):
                    nonlocal failed
                    if dst == fail_target and not failed:
                        failed = True
                        raise OSError('simulated commit failure')
                    return original(src, dst, **kwargs)
                with self.subTest(target=fail_target), patch('archive_build.os.replace', side_effect=fail_once), self.assertRaises(OSError):
                    archive_build.main(args + ['--rebuild-candidate'])
                self.assertTrue(failed)
                self.assertTrue(all(p.read_bytes() == data for p, data in old.items()))
                self.assertFalse(list(self.cache.glob('.archive-*')))
                self.assertFalse(list(release.glob('.archive-*')))
            archive_build.main(args + ['--rebuild-candidate'])
            current = json.loads((release / 'manifest.json').read_text())
            checksums = json.loads((release / 'checksums.json').read_text())
            for asset in current['assets']:
                self.assertEqual(digest(self.cache / asset['name']), asset['sha256'])
                self.assertEqual(checksums[asset['name']], asset['sha256'])

    def test_generation_first_commit_failure_removes_only_new_targets(self):
        root, release, args = self.build_fixture()
        old_master = (release / 'manifest.json').read_bytes()
        original = archive_build.os.replace
        def fail_manifest(src, dst, **kwargs):
            if dst == 'manifest.json':
                raise OSError('simulated metadata failure')
            return original(src, dst, **kwargs)
        with patch.object(archive_build, 'ROOT', root), patch('archive_build.os.replace', side_effect=fail_manifest), self.assertRaises(OSError):
            archive_build.main(args)
        self.assertEqual(list(self.cache.iterdir()), [])
        self.assertEqual((release / 'manifest.json').read_bytes(), old_master)
        self.assertFalse((release / 'checksums.json').exists())
        self.assertFalse((release / 'SHA256SUMS').exists())
        self.assertFalse(list(release.glob('.archive-*')))

    def test_generation_preservation_and_text_checksums_refresh_and_roll_back(self):
        root, release, args = self.build_fixture()
        draft_path = root / 'archive/preservation/zenodo-version-draft.json'
        draft_path.parent.mkdir(parents=True)
        draft = {'status': 'DRAFT-NOT-SUBMITTED', 'metadata': {'version': '1.0.0', 'title': 'Preserve title'},
                 'doi': None, 'author_approval_required': True, 'proposed_files': [{'name': 'stale.tar.gz'}],
                 'additional_files_requiring_review': ['Preserve this independent review requirement']}
        draft_path.write_text(json.dumps(draft))
        (release / 'SHA256SUMS').write_text('stale checksum list\n')
        with patch.object(archive_build, 'ROOT', root), patch('sys.stdout', io.StringIO()):
            archive_build.main(args)
            first_draft = json.loads(draft_path.read_text())
            for key in draft.keys() - {'proposed_files'}:
                self.assertEqual(first_draft[key], draft[key])
            old = {p: p.read_bytes() for p in [*self.cache.glob('*.tar.gz'), draft_path,
                    release / 'manifest.json', release / 'checksums.json', release / 'SHA256SUMS']}
            self.change_build_sources(root, release)
            original = archive_build.os.replace
            def fail_manifest_once(src, dst, **kwargs):
                if dst == 'manifest.json' and not src.startswith('.archive-rollback-'):
                    raise OSError('simulated final manifest commit failure')
                return original(src, dst, **kwargs)
            with patch('archive_build.os.replace', side_effect=fail_manifest_once), self.assertRaises(OSError):
                archive_build.main(args + ['--rebuild-candidate'])
            self.assertTrue(all(p.read_bytes() == body for p, body in old.items()))
            archive_build.main(args + ['--rebuild-candidate'])
        assets = json.loads((release / 'manifest.json').read_text())['assets']
        self.assertEqual((release / 'SHA256SUMS').read_text(), ''.join(f"{a['sha256']}  {a['name']}\n" for a in assets))
        self.assertEqual(json.loads(draft_path.read_text())['proposed_files'], [
            dict(name=a['name'], sha256=a['sha256'], bytes=a['bytes'],
                 treatment='eligible-source-data; attach full source-specific conditions') for a in assets])
        self.assertNotEqual(draft_path.read_bytes(), old[draft_path])
        self.assertFalse(list(draft_path.parent.glob('.archive-*')))

    def test_list_remains_metadata_only_without_policy_or_bundles(self):
        root, release, _ = self.build_fixture()
        # Discovery needs only release manifests, not policy validation or cache access.
        (root / 'archive/catalogue/artifacts.json').unlink()
        output = io.StringIO()
        with patch.object(fetch_data, 'ROOT', root), patch('sys.stdout', output), \
                patch.object(fetch_data, 'load_policy', side_effect=AssertionError('list accessed policy')), \
                patch.object(fetch_data, 'obtain_bundle', side_effect=AssertionError('list accessed bundles')):
            self.assertEqual(fetch_data.main(['--list']), 0)
        found = json.loads(output.getvalue())['archive_releases']
        self.assertEqual(found[0]['release'], 'v1.0.0')
        self.assertEqual([c['id'] for c in found[0]['collections']], [f'{n:02}' for n in range(1, 10)])
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_builder_rejects_output_dotdot_inside_repository(self):
        root, _, args = self.build_fixture()
        args[-1] = str(root.parent / 'outside/../repo/bundles')
        with patch.object(archive_build, 'ROOT', root), patch('sys.stderr', io.StringIO()), self.assertRaises(SystemExit):
            archive_build.main(args)
        self.assertFalse((root / 'bundles').exists())

    def test_builder_registry_permission_is_required_before_writing(self):
        root, _, args = self.build_fixture()
        registry = root / 'archive/licensing/rights_registry.json'
        obj = json.loads(registry.read_text())
        obj['records'][0]['publication_decision'] = 'Rights unresolved'
        registry.write_text(json.dumps(obj))
        with patch.object(archive_build, 'ROOT', root), self.assertRaises(ArchiveError):
            archive_build.main(args)
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_restore_rejects_in_place_second_pass_member_changes(self):
        path, asset = self.good()
        original_bytes = path.read_bytes()
        original_stream = archive_io.tar_stream
        good = [(r['path'], body, tarfile.REGTYPE) for r, body in zip(self.rows, [b'alpha', b'beta'])]
        variations = [good[:1], good + good[:1],
                      [(self.rows[0]['path'], b'', tarfile.SYMTYPE), good[1]],
                      good + [('unexpected.txt', b'x', tarfile.REGTYPE)]]
        for entries in variations:
            path.write_bytes(original_bytes)
            malicious, _, _ = self.malicious(entries)
            changed = malicious.read_bytes()
            calls = 0
            @contextmanager
            def mutate_on_second_pass(stream, expected):
                nonlocal calls
                calls += 1
                if calls == 2:
                    path.write_bytes(changed)
                with original_stream(stream, expected) as bundle:
                    yield bundle
            with self.subTest(entries=[x[0] for x in entries]), patch('archive_io.tar_stream', mutate_on_second_pass), self.assertRaises((ArchiveError, tarfile.TarError, EOFError, OSError)):
                restore_bundle(path, asset, self.rows, self.dest)
            self.assertFalse((self.dest / self.rows[0]['path']).exists())
            self.assertFalse((self.dest / self.rows[1]['path']).exists())
            self.assertFalse(list(self.dest.glob('.archive-stage-*')))

    def test_decompression_bomb_after_tar_end_rejected(self):
        path, asset = self.good()
        with path.open('ab') as out:
            out.write(gzip.compress(b'\x00' * 2000000))
        asset.update(bytes=path.stat().st_size, sha256=digest(path))
        self.assert_rejects(path, asset, self.rows)

    def test_http_download_atomic_and_verify(self):
        path, asset = self.good()
        body = path.read_bytes()
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body)
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            asset['url'] = f'http://127.0.0.1:{server.server_port}/bundle'
            destination = self.root / 'download'
            found = obtain_bundle(destination, asset, self.rows)
            self.assertEqual(found.read_bytes(), body)
            self.assertEqual(sorted(p.name for p in destination.iterdir()), [asset['name']])
            asset['bytes'] -= 1
            bad_cache = self.root / 'bad-download'
            with self.assertRaises(ArchiveError):
                obtain_bundle(bad_cache, asset, self.rows)
            self.assertEqual(list(bad_cache.iterdir()), [])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_interrupted_download_not_promoted(self):
        _, asset = self.good()
        asset['url'] = 'https://example.test/bundle'
        class BrokenResponse:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def geturl(self):
                return asset['url']
            def read(self, size):
                raise OSError('simulated interruption')
        target = self.root / 'interrupted'
        with patch('urllib.request.urlopen', return_value=BrokenResponse()), self.assertRaises(OSError):
            obtain_bundle(target, asset, self.rows)
        self.assertEqual(list(target.iterdir()), [])

    def test_unexpected_member_and_traversal_rejected(self):
        for name in ('unexpected.txt', '../escape', '/absolute'):
            with self.subTest(name=name):
                self.assert_rejects(*self.malicious([(name, b'alpha', tarfile.REGTYPE)]))

    def test_restore_race_does_not_clobber(self):
        path, asset = self.good()
        import archive_io
        original = archive_io.os.link
        conflict = self.dest / self.rows[0]['path']
        def race(src, dst, **kwargs):
            if dst == 'a.txt':
                conflict.write_bytes(b'concurrent local work')
            return original(src, dst, **kwargs)
        with patch('archive_io.os.link', side_effect=race), self.assertRaises(ArchiveError):
            restore_bundle(path, asset, self.rows, self.dest)
        self.assertEqual(conflict.read_bytes(), b'concurrent local work')
        self.assertEqual(list(self.dest.glob('.archive-stage-*')), [])

    def test_legacy_selection_unchanged(self):
        release, pairs, exceptions = fetch_data.release_plan(fetch_data.ROOT)
        self.assertTrue(release.startswith('legacy:'))
        self.assertEqual(len(pairs), 5)
        self.assertEqual(sum(len(rows) for _, rows in pairs), 1254)
        for asset, rows in pairs:
            self.assertEqual(asset['files'], len(rows))

    def test_cli_candidate_offline_restore_and_receipt(self):
        _, asset = self.good()
        release = self.root / 'archive/releases/v1.0.0'
        (release / 'collections').mkdir(parents=True)
        asset.update(collection_id='05', manifest='collections/05.json')
        master = {'schema_version': '1.0.0', 'archive_version': '1.0.0', 'status': 'candidate', 'assets': [asset], 'exceptions': [{'collection_id': '05', 'category': 'rights-unresolved'}]}
        (release / 'manifest.json').write_text(json.dumps(master))
        (release / 'collections/05.json').write_text(json.dumps({'schema_version': '1.0.0', 'archive_version': '1.0.0', 'collection_id': '05', 'files': self.rows}))
        self.policy(self.root, {'05': self.rows})
        report = self.root / 'report.json'
        with patch.object(fetch_data, 'ROOT', self.root), patch('sys.stdout', io.StringIO()), patch('sys.stderr', io.StringIO()):
            result = fetch_data.main(['--release', 'v1.0.0', '--collection', '05', '--offline', '--archive-dir', str(self.cache), '--destination', str(self.dest), '--report', str(report)])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(report.read_text())['archive_coverage'], 'exceptions-remain')
        self.assertEqual(len(list((self.dest / '.archive-receipts').iterdir())), 1)

    def test_fetch_rejects_forged_policy_and_missing_members(self):
        _, asset = self.good()
        release = self.root / 'archive/releases/v1.0.0'
        (release / 'collections').mkdir(parents=True)
        asset.update(collection_id='05', manifest='collections/05.json')
        master = {'schema_version': '1.0.0', 'archive_version': '1.0.0', 'status': 'candidate', 'assets': [asset], 'exceptions': []}
        (release / 'manifest.json').write_text(json.dumps(master))
        manifest_path = release / 'collections/05.json'
        for corruption in ('rights', 'dataset', 'artifact', 'bytes', 'omission', 'registry', 'catalogue-exclusion', 'missing-bundle'):
            self.policy(self.root, {'05': self.rows})
            cm = {'schema_version': '1.0.0', 'archive_version': '1.0.0', 'collection_id': '05', 'files': [dict(r) for r in self.rows]}
            (release / 'manifest.json').write_text(json.dumps(master))
            if corruption in ('rights', 'dataset', 'artifact'):
                cm['files'][0][corruption + '_id'] = 'forged'
            elif corruption == 'bytes':
                cm['files'][0]['bytes'] += 1
            elif corruption == 'omission':
                cm['files'].pop()
            elif corruption == 'registry':
                p = self.root / 'archive/licensing/rights_registry.json'
                obj = json.loads(p.read_text());obj['records'][0]['publication_decision'] = 'Rights unresolved';p.write_text(json.dumps(obj))
            elif corruption == 'catalogue-exclusion':
                p = self.root / 'archive/catalogue/artifacts.json'
                obj = json.loads(p.read_text());obj['artifacts'][0]['included_in_v1'] = False;p.write_text(json.dumps(obj))
            else:
                (release / 'manifest.json').write_text(json.dumps({**master, 'assets': []}))
            manifest_path.write_text(json.dumps(cm))
            with self.subTest(corruption=corruption), self.assertRaises(ArchiveError):
                fetch_data.release_plan(self.root, 'v1.0.0', ['05'])

    def test_cli_verify_only_no_destination_mutation(self):
        _, asset = self.good()
        with patch.object(fetch_data, 'release_plan', return_value=('test', [(asset, self.rows)], [])), patch('sys.stdout', io.StringIO()):
            result = fetch_data.main(['--offline', '--verify-only', '--archive-dir', str(self.cache), '--destination', str(self.dest)])
        self.assertEqual(result, 0)
        self.assertFalse(self.dest.exists())


if __name__ == '__main__':
    unittest.main()
