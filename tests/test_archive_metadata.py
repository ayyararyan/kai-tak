"""Negative metadata/replay regressions using isolated, minimal archive copies."""
import collections
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import archive_geospatial
import archive_reproduce
import archive_validate


def read(path):
    return json.loads(path.read_text())


class MetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        a = ROOT / 'archive'
        art = next(x for x in read(a / 'catalogue/artifacts.json')['artifacts'] if x['path'] == str(archive_reproduce.RAW))
        ds = next(x for x in read(a / 'catalogue/datasets.json')['datasets'] if x['id'] == art['dataset_ids'][0])
        sources = [x for x in read(a / 'catalogue/sources.json')['sources'] if x['id'] in art['source_ids']]
        rights = [x for x in read(a / 'licensing/rights_registry.json')['records'] if x['id'] in {art['rights_id']} | {s['rights_id'] for s in sources}]
        cls.seed = copy.deepcopy((art, ds, sources, rights))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.a = self.root / 'archive'
        shutil.copytree(ROOT / 'archive/schemas', self.a / 'schemas')
        art, ds, sources, rights = copy.deepcopy(self.seed)
        art.update(dataset_ids=[ds['id']], derived_from=[])
        ds.update(artifact_ids=[art['id']], derived_from=[], producer_scripts=[], file_count=1,
                  total_bytes=art['bytes'], permitted_bundle_files=1)
        self.art, self.ds = art, ds
        self.put('catalogue/artifacts.json', dict(schema_version='1.0.0', archive_version='1.0.0', artifacts=[art]))
        self.put('catalogue/datasets.json', dict(schema_version='1.0.0', archive_version='1.0.0', status='candidate', datasets=[ds]))
        self.put('catalogue/sources.json', dict(schema_version='1.0.0', sources=sources))
        self.put('licensing/rights_registry.json', dict(schema_version='1.0.0', records=rights))
        self.put('catalogue/provenance.json', dict(schema_version='1.0.0', nodes=[], activities=[], edges=[dict(id='edge-source-' + sid, relation='attributed-to-source', subject=art['id'], object=sid, evidence_level='source-and-checksum-bound') for sid in art['source_ids']]))
        self.put('catalogue/publication_usage.json', {'usages': []})
        member = {k: art[k] for k in ('path', 'bytes', 'sha256', 'rights_id', 'publication_decision')}
        member.update(artifact_id=art['id'], dataset_id=ds['id'])
        for c in range(1, 10):
            cid = f'{c:02}'
            members = [member] if cid == '05' else []
            self.put(f'releases/v1.0.0/collections/{cid}.json', dict(schema_version='1.0.0', archive_version='1.0.0', collection_id=cid, files=members))
            self.put(f'collections/{cid}/collection.json', dict(schema_version='1.0.0', id=cid, title='Fixture',
                     dataset_ids=[ds['id']] if members else [], citation='Fixture citation', file_count=len(members),
                     permitted_bundle_files=len(members), release_manifest=f'../../releases/v1.0.0/collections/{cid}.json'))
        self.asset = dict(name='kai-tak-archive-v1.0.0-collection-05.tar.gz', collection_id='05', bytes=100,
                          sha256='1' * 64, files=1, unpacked_bytes=art['bytes'], url=None, manifest='collections/05.json')
        self.put('releases/v1.0.0/manifest.json', dict(schema_version='1.0.0', archive_version='1.0.0', status='candidate', source_commit='1' * 40, complete_historical_archive=False, assets=[self.asset], exceptions=[], dependencies=[], rights_notice='Fixture rights'))
        self.put('releases/v1.0.0/checksums.json', {self.asset['name']: self.asset['sha256']})
        (self.a / 'releases/v1.0.0/SHA256SUMS').write_text(self.asset['sha256'] + '  ' + self.asset['name'] + '\n')
        self.put('preservation/zenodo-version-draft.json', {'proposed_files': [{k: self.asset[k] for k in ('name', 'bytes', 'sha256')}]})

    def put(self, name, value):
        path = self.a / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def mutate(self, name, change):
        value = read(self.a / name)
        change(value)
        self.put(name, value)

    def fails(self, label):
        report = archive_validate.validate(self.root)
        self.assertEqual(report['status'], 'failed')
        self.assertIn(label, {e['check'] for e in report['errors']}, report['errors'])

    def test_valid_metadata_fixture(self):
        report = archive_validate.validate(self.root)
        self.assertEqual(report['errors'], [])

    def test_published_release_requires_real_identity_and_urls(self):
        self.mutate('releases/v1.0.0/manifest.json', lambda x: x.update(status='published'))
        self.fails('published-release-identity')
        def publish(x):
            x.update(release_tag='archive-v1.0.0', release_url='https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0', release_date='2026-10-13', publication_authorized=True)
            x['assets'][0]['url']='https://github.com/ayyararyan/kai-tak/releases/download/archive-v1.0.0/'+x['assets'][0]['name']
        self.mutate('releases/v1.0.0/manifest.json', publish)
        self.assertEqual(archive_validate.validate(self.root)['errors'], [])
        self.mutate('releases/v1.0.0/manifest.json', lambda x: x['assets'][0].update(url='https://wrong.invalid/data'))
        self.fails('published-asset-urls')

    def test_wrong_master_manifest_path(self):
        self.mutate('releases/v1.0.0/manifest.json', lambda x: x['assets'][0].update(manifest='collections/03.json'))
        self.fails('asset-collection-binding:05')

    def test_wrong_collection_identity(self):
        self.mutate('releases/v1.0.0/collections/05.json', lambda x: x.update(collection_id='03'))
        self.fails('collection-identity:05')

    def test_wrong_dataset_binding(self):
        self.mutate('releases/v1.0.0/collections/05.json', lambda x: x['files'][0].update(dataset_id='missing-dataset'))
        self.fails('manifest-catalogue-binding:' + self.art['id'])

    def test_wrong_member_hash(self):
        self.mutate('releases/v1.0.0/collections/05.json', lambda x: x['files'][0].update(sha256='2' * 64))
        self.fails('manifest-catalogue-binding:' + self.art['id'])

    def test_wrong_asset_name(self):
        self.mutate('releases/v1.0.0/manifest.json', lambda x: x['assets'][0].update(name='wrong.tar.gz'))
        self.fails('asset-collection-binding:05')

    def test_checksum_disagreement(self):
        self.put('releases/v1.0.0/checksums.json', {self.asset['name']: '2' * 64})
        self.fails('checksums-json-binding')

    def test_sha256sums_disagreement(self):
        (self.a / 'releases/v1.0.0/SHA256SUMS').write_text('2' * 64 + '  ' + self.asset['name'] + '\n')
        self.fails('sha256sums-binding')

    def test_preservation_disagreement(self):
        self.mutate('preservation/zenodo-version-draft.json', lambda x: x['proposed_files'][0].update(bytes=1))
        self.fails('preservation-files-binding')

    def test_duplicate_virtual_nodes(self):
        self.mutate('catalogue/provenance.json', lambda x: x.update(nodes=[dict(id='v', kind='archive-member', sha256=None)] * 2))
        self.fails('unique-ids:nodes')

    def test_virtual_node_collides_with_artifact(self):
        self.mutate('catalogue/provenance.json', lambda x: x.update(nodes=[dict(id=self.art['id'], kind='archive-member', sha256=None)]))
        self.fails('unique-artifact-node-identities')

    def test_supplemental_cycle_through_virtual_nodes(self):
        def change(pv):
            pv['nodes'] = [dict(id='v', kind='archive-member', sha256=None)]
            pv['edges'] += [dict(id='cycle1', relation='derived-from', subject=self.art['id'], object='v', evidence_level='fixture'), dict(id='cycle2', relation='extracted-from', subject='v', object=self.art['id'], evidence_level='fixture')]
        self.mutate('catalogue/provenance.json', change)
        self.fails('acyclic-artifact-lineage')

    def test_missing_attribution_edge(self):
        self.mutate('catalogue/provenance.json', lambda x: x.update(edges=[]))
        self.fails('source-attribution-binding:' + self.art['id'])

    def test_revoked_rights(self):
        self.mutate('licensing/rights_registry.json', lambda x: x['records'][0].update(publication_decision='Rights unresolved'))
        self.fails('rights-decision:' + self.art['id'])

    def test_bad_schema_reports_failure_without_exception(self):
        self.mutate('catalogue/artifacts.json', lambda x: x.update(artifacts=None))
        self.fails('schema:catalogue/artifacts.json')

    def test_dataset_membership_is_bidirectional(self):
        self.mutate('catalogue/datasets.json', lambda x: x['datasets'][0].update(artifact_ids=[], file_count=0, total_bytes=0, permitted_bundle_files=0))
        self.fails('artifact-dataset-membership:' + self.art['id'])

    def test_zero_missing_height_count_does_not_disappear(self):
        counts = collections.Counter(features=10, invalid_geometry=0)
        expected = dict(features=10, invalid_geometry=0, BaseHeight_missing=4, TopHeight_missing=3)
        checks = archive_geospatial.compare_building_counts(counts, expected)
        self.assertFalse(checks['BaseHeight_missing'])
        self.assertFalse(checks['TopHeight_missing'])
        self.assertTrue(checks['features'])

    def test_failed_decoder_missing_outputs_writes_failed_report(self):
        lane = self.root / archive_reproduce.LANE
        lane.mkdir(parents=True)
        (lane / 'decode_noaa.py').write_text('raise SystemExit(7)\n')
        (lane / 'test_decode_noaa.py').write_text('')
        (lane / 'isd-format-document.pdf').write_bytes(b'fixture')
        raw = self.root / archive_reproduce.RAW
        raw.parent.mkdir(parents=True)
        raw.write_bytes(b'fixture')
        rows = [{'path': str(archive_reproduce.RAW), 'sha256': hashlib.sha256(b'fixture').hexdigest()}]
        rows += [{'path': str(archive_reproduce.LANE / n), 'sha256': 'f' * 64} for n in ('observations_1993.csv', 'observations_1993-11-04.csv')]
        self.put('catalogue/artifacts.json', {'artifacts': rows})
        report_path = self.root / 'failed-replay.json'
        with patch.object(archive_reproduce, 'ROOT', self.root), patch.object(sys, 'argv', ['replay', '--data-root', str(self.root), '--report', str(report_path)]), patch('sys.stdout', io.StringIO()):
            self.assertEqual(archive_reproduce.main(), 2)
        report = read(report_path)
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['producer_exit'], 7)
        self.assertTrue(all(x['rows'] is None and not x['byte_identical'] for x in report['outputs']))

    def test_replay_timeout_is_captured(self):
        with patch('archive_reproduce.subprocess.run', side_effect=subprocess.TimeoutExpired('decoder', 90, stderr=b'partial log')):
            result = archive_reproduce.run_step(['decoder'], self.root)
        self.assertEqual(result.returncode, 124)
        self.assertIn('partial log', result.stderr)
        self.assertIn('timed out', result.stderr)


if __name__ == '__main__':
    unittest.main()
