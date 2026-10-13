"""Regression tests for evidence semantics and immutable/idempotent catalogue updates."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import archive_catalogue as catalogue
import archive_refine as refinement


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.archive = self.root / 'archive'
        self.source = self.root / 'source'
        self.source.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def put(self, path, value):
        p = self.archive / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value) + '\n')
        return p

    def snapshot(self):
        return {str(p.relative_to(self.archive)): p.read_bytes()
                for p in self.archive.rglob('*') if p.is_file()}

    def test_published_generation_and_refinement_refuse_before_any_write(self):
        self.put('releases/v1.0.0/manifest.json', {'status': 'published'})
        self.put('sentinel.json', {'original': True})
        before = self.snapshot()
        with patch.object(catalogue, 'A', self.archive), patch.object(
                sys, 'argv', ['archive_catalogue.py', '--source-root', str(self.source)]):
            with self.assertRaisesRegex(ValueError, 'unpublished candidate'):
                catalogue.main()
        with patch.object(refinement, 'A', self.archive):
            with self.assertRaisesRegex(ValueError, 'unpublished candidate'):
                refinement.refine(self.source)
        self.assertEqual(before, self.snapshot())

    def test_geospatial_verification_is_not_acquisition_or_generation(self):
        for raw in (True, False):
            dates = catalogue.geospatial_dates('2026-10-13T12:20:57Z', raw)
            self.assertIsNone(dates['acquisition_date'])
            self.assertIsNone(dates['generation_date'])
            self.assertEqual(dates['verification_date'], '2026-10-13T12:20:57Z')
            self.assertEqual(dates['acquisition_no_later_than'],
                             dates['verification_date'] if raw else None)
            self.assertEqual(dates['generation_no_later_than'],
                             None if raw else dates['verification_date'])

    def test_all_seven_withdrawn_results_and_branch_safe_status(self):
        names = ['global_exclusion_10000', 'global_exclusion_attempt',
                 'global_exclusion_corrected', 'global_exclusion_endpoint_exact',
                 'global_upper_003972', 'global_upper_004', 'global_upper_005']
        prefix = 'research/checkers-runway13/analytical/coupled/'
        for name in names + ['global_upper_branch_safe_01']:
            path = prefix + name + '.json'
            item = {'path': path, 'sha256': catalogue.digest(catalogue.ROOT / path),
                    'scientific_verification_status': 'recorded verification'}
            catalogue.scientific_status_from_evidence(item, [catalogue.ROOT])
            expected = 'unresolved;' if name.endswith('branch_safe_01') else 'invalidated;'
            self.assertTrue(item['scientific_verification_status'].startswith(expected), name)
            self.assertEqual(item['scientific_status_evidence']['sha256'], item['sha256'])

    def test_frozen_evidence_uses_own_hash_and_status(self):
        path = 'whitepaper/v1/evidence/frozen-result.json'
        p = self.source / path
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps({'invalidated': True, 'invalidation_reason': 'withdrawn'}))
        item = {'path': path, 'sha256': '0' * 64,
                'scientific_verification_status': 'unknown'}
        catalogue.scientific_status_from_evidence(item, [self.source])
        self.assertEqual(item['scientific_verification_status'], 'unknown')
        item['sha256'] = catalogue.digest(p)
        catalogue.scientific_status_from_evidence(item, [self.source])
        self.assertTrue(item['scientific_verification_status'].startswith('invalidated;'))
        self.assertEqual(item['scientific_status_evidence']['reason'], 'withdrawn')

    def fixture(self, path='sample.json'):
        (self.source / path).parent.mkdir(parents=True, exist_ok=True)
        body = b'{"invalidated": true, "result": "invalidated_do_not_use"}'
        (self.source / path).write_bytes(body)
        aid = catalogue.aid(path)
        item = dict(id=aid, path=path, sha256=hashlib.sha256(body).hexdigest(), bytes=len(body),
                    creator=['Government source'], dataset_ids=['kt-frozen-evidence'],
                    source_ids=['src-old'], processing_level='transformed', publication_date=None,
                    publication_decision='Redistribution permitted', rights_id='rights-test',
                    provenance_status='pinned-source-and-output-hashes', included_in_v1=True,
                    derived_from=[], collection_id='01', required_for_reproducibility=True,
                    scientific_verification_status='recorded verification')
        dataset = dict(id='kt-frozen-evidence', producer_scripts=['build.py'], limitations=[],
                       derived_from=['old-dataset'], artifact_ids=[aid], collection_id='01')
        self.put('catalogue/artifacts.json', {'artifacts': [item]})
        self.put('catalogue/datasets.json', {'datasets': [dataset]})
        old_edge = dict(id='old-attribution', relation='attributed-to-source', subject=aid,
                        object='src-old', evidence_level='old')
        self.put('catalogue/provenance.json', {'edges': [old_edge], 'activities': []})
        self.put('catalogue/catalogue_corrections.json', {
            'dataset_and_global_corrections': [dict(dataset_id=dataset['id'],
                remove_derived_from=['old-dataset'], add_relation={'relation': 'selected-using-index',
                                                                  'object': 'old-dataset'})],
            'artifact_updates': [dict(artifact_id=aid, path=path,
                                      fields={'source_ids': ['src-new'],
                                              'creator': ['Transformation author']})]})
        edge = dict(id='derived-test', relation='generated-by', subject=aid, object='node-1')
        self.put('catalogue/lineage_edges.json', {'additional_nodes': [{'id': 'node-1'}],
                                                'edges': [edge]})
        self.put('catalogue/sources.json', {'sources': [{'id': 'src-new'}]})
        assets = []
        for i in range(1, 10):
            cid = f'{i:02}'
            files = [dict(path=path, bytes=item['bytes'], sha256=item['sha256'], artifact_id=aid,
                          dataset_id=dataset['id'], rights_id=item['rights_id'],
                          publication_decision=item['publication_decision'])] if i == 1 else []
            self.put(f'releases/v1.0.0/collections/{cid}.json', dict(schema_version='1.0.0',
                      archive_version='1.0.0', collection_id=cid, files=files))
            self.put(f'collections/{cid}/collection.json', {'permitted_bundle_files': len(files)})
            (self.archive / f'collections/{cid}/README.md').write_text('1 verified-permitted files\n')
        assets.append(dict(collection_id='01', name='built.tar.gz', bytes=321, sha256='a' * 64,
                           files=1, unpacked_bytes=len(body), manifest='collections/01.json', url=None))
        self.put('releases/v1.0.0/manifest.json', {'status': 'candidate', 'assets': assets})
        (self.archive / 'CATALOGUE.md').write_text('# Catalogue\n')
        return aid, assets

    def test_refinement_repairs_legacy_geospatial_dates_in_artifact(self):
        path = catalogue.P + 'geospatial/raw/example.json'
        self.fixture(path)
        artifact_file = self.archive / 'catalogue/artifacts.json'
        artifacts = catalogue.read(artifact_file)
        artifacts['artifacts'][0]['acquisition_date'] = 'verification-misused-as-acquisition'
        catalogue.write(artifact_file, artifacts)
        geo = self.root / (catalogue.P + 'geospatial/manifest.json')
        catalogue.write(geo, {'verified_at_utc': '2026-10-13T12:20:57Z',
                             'files': [{'path': 'raw/example.json',
                                        'sha256': artifacts['artifacts'][0]['sha256']}]})
        with patch.object(refinement, 'A', self.archive), patch.object(refinement, 'ROOT', self.root):
            refinement.refine(self.source)
        result = catalogue.read(artifact_file)['artifacts'][0]
        self.assertIsNone(result['acquisition_date'])
        self.assertIsNone(result['generation_date'])
        self.assertEqual(result['verification_date'], '2026-10-13T12:20:57Z')
        self.assertEqual(result['acquisition_no_later_than'], result['verification_date'])

    def test_refinement_twice_is_byte_stable_and_restores_source_edges(self):
        aid, assets = self.fixture()
        with patch.object(refinement, 'A', self.archive), patch.object(refinement, 'ROOT', self.root):
            refinement.refine(self.source)
            first = self.snapshot()
            refinement.refine(self.source)
            self.assertEqual(first, self.snapshot())
        artifact = catalogue.read(self.archive / 'catalogue/artifacts.json')['artifacts'][0]
        self.assertEqual(artifact['source_attribution'], ['Government source'])
        self.assertEqual(artifact['creator'], ['Transformation author'])
        self.assertTrue(artifact['scientific_verification_status'].startswith('invalidated;'))
        dataset = catalogue.read(self.archive / 'catalogue/datasets.json')['datasets'][0]
        self.assertEqual(dataset['consumer_scripts'], ['build.py'])
        self.assertEqual(len(dataset['limitations']), 1)
        self.assertEqual(len(dataset['related_datasets']), 1)
        edges = catalogue.read(self.archive / 'catalogue/provenance.json')['edges']
        self.assertEqual(len(edges), 2)
        self.assertEqual([(e['subject'], e['object']) for e in edges
                          if e['relation'] == 'attributed-to-source'], [(aid, 'src-new')])
        self.assertEqual(catalogue.read(self.archive / 'releases/v1.0.0/manifest.json')['assets'], assets)


if __name__ == '__main__':
    unittest.main()
