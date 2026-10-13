"""Regression tests for new-error detection and preservation, not scientific claims."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import repository_checks as checks
from update_navigation import render


@pytest.fixture
def status():
    return checks.read(ROOT, 'docs/project-status.json')


@pytest.mark.parametrize('mutation', ['future', 'duplicate', 'wrong_hash', 'private', 'count', 'unknown_field'])
def test_status_rejects_unverified_or_malformed_products(status, mutation):
    if mutation == 'future':
        status['latest_paper'] = 'v99'
    elif mutation == 'duplicate':
        status['papers'].append(copy.deepcopy(status['papers'][0]))
    elif mutation == 'wrong_hash':
        status['papers'][0]['pdf_sha256'] = '0' * 64
    elif mutation == 'private':
        status['papers'][0]['guide'] = 'research/authorized_enquiries_20261013/private.md'
    elif mutation == 'count':
        status['archive']['permitted_files'] += 1
    else:
        status['made_up_doi'] = '10.fake/not-issued'
    assert checks.validate_status(ROOT, status)


def test_rights_boundary_is_independent_of_file_existence(status, monkeypatch):
    original = checks.read
    def altered(root, path):
        value = original(root, path)
        if str(path).endswith('collections/01.json'):
            value['files'][0]['publication_decision'] = 'Rights unresolved'
        return value
    monkeypatch.setattr(checks, 'read', altered)
    assert any('rights' in e for e in checks.validate_status(ROOT, status))


def test_markdown_reference_links_headings_and_html_assets(tmp_path):
    (tmp_path / 'page.md').write_text('# Repeated heading\n# Repeated heading\n<a id="custom"></a>\n')
    (tmp_path / 'picture.png').write_bytes(b'fixture')
    (tmp_path / 'README.md').write_text('[Heading][ref]\n\n[ref]: page.md#repeated-heading-1\n\n[custom](page.md#custom)\n<img src="picture.png">\n[bad](page.md#absent)\n![missing](new.png)\n')
    result = checks.check_links(tmp_path, ['README.md', 'page.md', 'picture.png'], {'links': []})
    assert [(e['target'], e['issue']) for e in result['errors']] == [('page.md#absent', 'fragment'), ('new.png', 'missing')]


def test_exact_exception_does_not_hide_new_link_or_fragment(tmp_path):
    (tmp_path / 'README.md').write_text('[old](absent.md) [new](new.md) [anchor](README.md#missing)')
    result = checks.check_links(tmp_path, ['README.md'], {'links': [{'source': 'README.md', 'target': 'absent.md', 'issue': 'missing'}]})
    assert len(result['inherited']) == 1
    assert {e['target'] for e in result['errors']} == {'new.md', 'README.md#missing'}


def test_code_examples_are_not_links_and_encoded_traversal_fails(tmp_path):
    (tmp_path / 'README.md').write_text('```md\n[fake](missing.md)\n```\n[escape](%2E%2E/outside.md)\n')
    result = checks.check_links(tmp_path, ['README.md'], {'links': []})
    assert result['checked'] == 1
    assert result['errors'][0]['issue'] == 'outside-repository'


def test_line_references_are_bounded(tmp_path):
    (tmp_path / 'README.md').write_text('[ok](code.py#L1) [bad](code.py#L99)')
    (tmp_path / 'code.py').write_text('pass\n')
    result = checks.check_links(tmp_path, ['README.md', 'code.py'], {'links': []})
    assert [e['target'] for e in result['errors']] == ['code.py#L99']


def test_private_files_blanket_licenses_and_symlinks_rejected(tmp_path):
    (tmp_path / 'target').write_text('unchanged')
    (tmp_path / 'linked').symlink_to('target')
    paths = ['.env', 'research/authorized_enquiries_20261013/letter.md', 'LICENSE', 'linked']
    assert len(checks.check_public_boundaries(tmp_path, paths, set())) == 4


def test_generator_preserves_unmarked_prose_and_fails_ambiguous_markers():
    before = 'Before\n<!-- current:start -->\nOld\n<!-- current:end -->\nAfter\n'
    actual = render(before, 'current', 'New')
    assert actual == before.replace('Old', 'New')
    assert render(actual, 'current', 'New') == actual
    with pytest.raises(ValueError):
        render(before + '<!-- current:start -->', 'current', 'New')


def test_preservation_catches_changed_original_even_if_baseline_hash_is_altered(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(tmp_path), *args], text=True).strip()
    git('init', '-q')
    original = tmp_path / 'science.py'
    original.write_text('original = 1\n')
    git('add', 'science.py')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')
    commit = git('rev-parse', 'HEAD')
    monkeypatch.setattr(checks, 'BASELINE_COMMIT', commit)
    monkeypatch.setattr(checks, 'PRESERVED_TAGS', {})
    baseline = {'commit': commit, 'tags': {}, 'files': [{'path': 'science.py', 'sha256': checks.sha(original)}]}
    directory = tmp_path / 'docs/migration'
    directory.mkdir(parents=True)
    manifest = directory / 'baseline.json'
    manifest.write_text(json.dumps(baseline))
    assert checks.preservation(tmp_path)['errors'] == []
    original.write_text('original = 2\n')
    baseline['files'][0]['sha256'] = checks.sha(original)
    manifest.write_text(json.dumps(baseline))
    assert 'Original Git blob changed: science.py' in checks.preservation(tmp_path)['errors']


def test_atlas_verification_checks_supplied_bytes_without_writing(tmp_path, monkeypatch):
    monkeypatch.setattr(checks, 'ATLAS_COVERAGE', {'input': 1, 'scene': 1})
    root, data, scenes = [tmp_path / p for p in ['repo', 'data', 'scenes']]
    directory = root / 'visual-atlas/v1/metadata'
    directory.mkdir(parents=True)
    for p in [data, scenes]:
        p.mkdir()
    (data / 'source').write_bytes(b'source')
    (scenes / 'scene').write_bytes(b'scene')
    directory.joinpath('input_manifest.json').write_text(json.dumps({'files': [{'path': 'source', 'bytes': 6, 'available': True, 'sha256': checks.sha(data / 'source')}]}))
    directory.joinpath('scene_bundle.json').write_text(json.dumps({'members': [{'path': 'scene', 'bytes': 5, 'sha256': checks.sha(scenes / 'scene')}]}))
    before = {str(p): checks.sha(p) for p in tmp_path.rglob('*') if p.is_file()}
    assert checks.atlas_dependencies(root, data, scenes)['errors'] == []
    assert before == {str(p): checks.sha(p) for p in tmp_path.rglob('*') if p.is_file()}
    (scenes / 'scene').write_bytes(b'corrupt')
    assert checks.atlas_dependencies(root, data, scenes)['errors']


def test_complete_paper_relabel_is_rejected(status):
    status['papers'][0]['version'] = status['latest_paper'] = 'v99'
    assert any('version' in e for e in checks.validate_status(ROOT, status))


def test_paper_page_count_bound_to_qa(status):
    status['papers'][0]['pages'] = 999
    assert any('page count' in e for e in checks.validate_status(ROOT, status))


def test_both_tag_baselines_cannot_redefine_preserved_tag(status, monkeypatch):
    original = checks.read
    status['tags']['archive-v1.0.0'] = '0' * 40
    def altered(root, path):
        value = original(root, path)
        if path == 'docs/migration/baseline.json':
            value['tags'] = status['tags']
        return value
    monkeypatch.setattr(checks, 'read', altered)
    assert any('identities' in e for e in checks.validate_status(ROOT, status))
    assert 'Baseline tag identities changed' in checks.preservation(ROOT)['errors']


@pytest.mark.parametrize('source', ['README.md', 'new.md'])
def test_historical_records_cannot_hide_mutable_or_new_documents(tmp_path, source):
    p = tmp_path / source
    p.write_text('[bad](missing.md)')
    baseline = {'files': [{'path': 'README.md', 'sha256': checks.sha(p)}]}
    exceptions = {'links': [], 'historical_records': [{'path': source, 'sha256': checks.sha(p)}]}
    directory = tmp_path / 'docs/migration'
    directory.mkdir(parents=True)
    (directory / 'baseline.json').write_text(json.dumps(baseline))
    assert checks.validate_exceptions(tmp_path, exceptions, baseline)
    assert checks.check_links(tmp_path, [source], exceptions)['errors']


def test_changed_frozen_source_cannot_keep_link_exception(tmp_path):
    p = tmp_path / 'old.md'
    p.write_text('[old](missing.md)')
    digest = checks.sha(p)
    baseline = {'files': [{'path': 'old.md', 'sha256': digest}]}
    exceptions = {'links': [{'source': 'old.md', 'target': 'missing.md', 'source_sha256': digest, 'classification': 'historical', 'reason': 'frozen'}]}
    assert not checks.validate_exceptions(tmp_path, exceptions, baseline)
    p.write_text(p.read_text() + '\nChanged.')
    assert any('bytes changed' in e for e in checks.validate_exceptions(tmp_path, exceptions, baseline))
    assert checks.validate_exceptions(tmp_path, {'links': [], 'historical_records': [{'path': 'old.md', 'sha256': digest}]}, baseline)


def test_ignored_targets_are_not_public_and_directories_need_public_descendants(tmp_path):
    (tmp_path / '.work').mkdir()
    (tmp_path / '.work/draft.md').write_text('private draft')
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs/public.md').write_text('public')
    (tmp_path / 'README.md').write_text('[bad](.work/draft.md) [bad directory](.work/) [ok](docs/)')
    result = checks.check_links(tmp_path, ['README.md', 'docs/public.md'], {'links': []})
    assert [(e['target'], e['issue']) for e in result['errors']] == [('.work/draft.md', 'not-public'), ('.work/', 'not-public')]


def test_html_line_like_fragment_requires_real_id(tmp_path):
    (tmp_path / 'README.md').write_text('[bad](page.html#L1) [good](page.html#L2)')
    (tmp_path / 'page.html').write_text('<p id="L2">Example</p>\n')
    result = checks.check_links(tmp_path, ['README.md', 'page.html'], {'links': []})
    assert [(e['target'], e['issue']) for e in result['errors']] == [('page.html#L1', 'fragment')]


@pytest.mark.parametrize('field,value', [('edition', 'v99'), ('gallery_path', 'wrong.html'), ('gallery_sha256', '0' * 64)])
def test_browser_receipt_requires_edition_and_gallery_identity(status, monkeypatch, field, value):
    original = checks.read
    def altered(root, path):
        data = original(root, path)
        if path == 'docs/migration/browser-acceptance.json':
            data[field] = value
        return data
    monkeypatch.setattr(checks, 'read', altered)
    assert any('Browser receipt' in e for e in checks.validate_status(ROOT, status))


@pytest.mark.parametrize('mutation', ['missing', 'empty', 'truncated', 'duplicate', 'unsafe', 'digest', 'bytes'])
def test_atlas_malformed_manifest_never_passes(tmp_path, monkeypatch, mutation):
    data = checks.read(ROOT, 'visual-atlas/v1/metadata/input_manifest.json')
    if mutation == 'missing':
        data = {}
    elif mutation == 'empty':
        data['files'] = []
    elif mutation == 'truncated':
        data['files'].pop()
    elif mutation == 'duplicate':
        data['files'][1] = data['files'][0]
    elif mutation == 'unsafe':
        data['files'][0]['path'] = '../escape'
    elif mutation == 'digest':
        data['files'][0]['sha256'] = 'bogus'
    else:
        data['files'][0]['bytes'] = '53893170'
    original = checks.read
    monkeypatch.setattr(checks, 'read', lambda root, path: data if path.endswith('input_manifest.json') else original(root, path))
    result = checks.atlas_dependencies(ROOT, tmp_path, tmp_path)
    assert any('manifest requires' in e or 'Invalid atlas' in e or 'Duplicate atlas' in e for e in result['errors'])


def test_future_navigation_uses_current_gallery_and_neutral_edition(status):
    from update_navigation import blocks
    status['atlas']['version'] = 'v2'
    status['atlas']['gallery'] = 'visual-atlas/v2/gallery/index.html'
    status['papers'][0]['version'] = status['latest_paper'] = 'v99'
    output = blocks(status)
    gallery = output['visual-atlas/README.md', 'atlas-gallery']
    assert '(v2/gallery/index.html)' in gallery
    assert 'http://127.0.0.1:8000/visual-atlas/v2/gallery/index.html' in gallery
    assert 'v1' not in gallery
    assert 'format edition' not in output['docs/PROJECT_STATUS.md', 'status-products']


def test_generator_updates_multiple_stale_blocks_in_one_file(tmp_path, monkeypatch):
    import update_navigation as navigation
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs/project-status.json').write_text('{}')
    page = tmp_path / 'atlas.md'
    page.write_text('Introduction\n<!-- first:start -->\nOld first\n<!-- first:end -->\n'
                    'Keep this prose\n<!-- second:start -->\nOld second\n<!-- second:end -->\n')
    monkeypatch.setattr(checks, 'validate_status', lambda root, status: [])
    monkeypatch.setattr(navigation, 'blocks', lambda status: {
        ('atlas.md', 'first'): 'New first', ('atlas.md', 'second'): 'New second'})
    original = page.read_bytes()
    assert navigation.update(tmp_path, check=True) == ['atlas.md']
    assert page.read_bytes() == original
    assert navigation.update(tmp_path) == ['atlas.md']
    assert 'New first' in page.read_text() and 'New second' in page.read_text()
    assert 'Keep this prose' in page.read_text()
    assert navigation.update(tmp_path, check=True) == []


def test_generator_never_rewrites_author_owned_root_readme(tmp_path, monkeypatch, status):
    import update_navigation as navigation
    assert 'README.md' not in {path for path, marker in navigation.blocks(status)}
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs/project-status.json').write_text(json.dumps(status))
    authored = b'# Author homepage\n<!-- current-products:start -->\nMy design\n<!-- current-products:end -->\n'
    (tmp_path / 'README.md').write_bytes(authored)
    for path, marker in navigation.blocks(status):
        p = tmp_path / path
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('a') as stream:
            stream.write(f'<!-- {marker}:start -->\nOld\n<!-- {marker}:end -->\n')
    monkeypatch.setattr(checks, 'validate_status', lambda root, value: [])
    assert navigation.update(tmp_path)
    assert (tmp_path / 'README.md').read_bytes() == authored
    assert navigation.update(tmp_path, check=True) == []


def test_author_homepage_routes_checked_without_rewriting(tmp_path, status):
    page = tmp_path / 'README.md'
    page.write_text('[Old paper](research/checkers-runway13/whitepaper/v4/checkers-with-runway-13-white-paper-v4.pdf)\n'
                    '[Archive](archive/README.md) [Atlas](visual-atlas/v1/README.md)')
    original = page.read_bytes()
    assert checks.check_homepage_navigation(tmp_path, status) == ['Author-maintained README lacks current paper route']
    assert page.read_bytes() == original
    page.write_text(page.read_text() + '\n[Publication index](papers/README.md)')
    assert checks.check_homepage_navigation(tmp_path, status) == []


@pytest.mark.parametrize('mutation', ['none', 'science', 'ledger', 'mapping'])
def test_scientific_snapshot_wrapper_refuses_changed_science(tmp_path, monkeypatch, mutation):
    import hashlib
    import repo
    science_path = 'research/checkers-runway13/result.py'
    ledger_path = 'research/checkers-runway13/PROJECT_STATE.md'
    originals = {science_path: b'accepted = True\n', ledger_path: b'# Published ledger\n'}
    mapping = {'files': [{'public_path': path, 'public_bytes': len(data), 'public_sha256': hashlib.sha256(data).hexdigest()} for path, data in originals.items()]}
    mapping_path = 'publication/scientific-results-20261013/source_public_mapping.json'
    original_mapping = json.dumps(mapping).encode()
    for path, data in {**originals, mapping_path: original_mapping}.items():
        p = tmp_path / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    (tmp_path / ledger_path).write_bytes(originals[ledger_path] + b'\nLater publication\n')
    if mutation == 'science':
        (tmp_path / science_path).write_bytes(b'accepted = False\n')
    elif mutation == 'ledger':
        (tmp_path / ledger_path).write_bytes(b'Rewritten history\n')
    elif mutation == 'mapping':
        (tmp_path / mapping_path).write_bytes(b'{}')
    monkeypatch.setattr(repo, 'ROOT', tmp_path)
    monkeypatch.setattr(repo.subprocess, 'check_output', lambda command: original_mapping if command[-1].endswith(mapping_path) else originals[ledger_path])
    if mutation == 'none':
        assert repo.verify_current_scientific_bindings('a' * 40) == 1
    else:
        with pytest.raises(ValueError):
            repo.verify_current_scientific_bindings('a' * 40)


@pytest.mark.parametrize('field,value', [
    ('pdf_sha256', '0' * 64), ('source_sha256', '0' * 64), ('pages', 999),
    ('version', 'v99'), ('guide', '../outside.md'),
    ('publication_receipt', 'research/authorized_enquiries_20261013/private.md'),
    ('status', 'journal-published'), ('made_up_doi', '10.fake/not-issued'),
])
def test_mathematical_note_metadata_rejects_unverified_changes(status, field, value):
    status['mathematical_note'][field] = value
    assert checks.validate_status(ROOT, status)


def test_mathematical_companion_is_independent_of_latest_white_paper(status):
    from update_navigation import blocks
    assert checks.validate_status(ROOT, status) == []
    assert status['latest_paper'] == 'v5'
    assert len(status['papers']) == 5
    output = blocks(status)
    assert 'Latest published paper: v5' in output['papers/README.md', 'paper-index']
    companion = output['papers/README.md', 'mathematical-note']
    assert 'Independent mathematical companion' in companion
    assert status['mathematical_note']['pdf'] in companion
    assert status['mathematical_note']['publication_receipt'] in companion
    products = output['docs/PROJECT_STATUS.md', 'status-products']
    assert 'Preservation baseline:' in products
    assert 'checked against GitHub main' not in products
    assert 'README.md' not in {path for path, marker in output}


@pytest.mark.parametrize('mutation', ['asset', 'commit', 'qa'])
def test_mathematical_note_requires_publication_and_qa_binding(status, monkeypatch, mutation):
    original = checks.read
    def altered(root, path):
        data = original(root, path)
        if str(path) == status['mathematical_note']['publication_receipt']:
            if mutation == 'asset':
                data['assets'][0]['sha256'] = '0' * 64
            elif mutation == 'commit':
                data['remote_commit'] = '0' * 40
        if mutation == 'qa' and str(path).endswith('mathematical-note/v1/qa/grayscale-clean-build.json'):
            data['production_pdf_sha256'] = '0' * 64
        return data
    monkeypatch.setattr(checks, 'read', altered)
    assert checks.validate_status(ROOT, status)


@pytest.fixture
def frozen_link_fixture(tmp_path, monkeypatch):
    original = 'research/report.md'
    prefix = 'snapshot/'
    source = tmp_path / original
    source.parent.mkdir()
    source.write_text('[old](missing.md)\n')
    copied = prefix + original
    copy_path = tmp_path / copied
    copy_path.parent.mkdir(parents=True)
    copy_path.write_bytes(source.read_bytes())
    digest = checks.sha(source)
    baseline = tmp_path / 'docs/migration/baseline.json'
    baseline.parent.mkdir(parents=True)
    baseline.write_text(json.dumps({'files': [{'path': original, 'sha256': digest}]}))
    name = prefix + 'PUBLIC_SOURCE_MANIFEST.json'
    manifest = tmp_path / name
    manifest.write_text(json.dumps({'source_commit': 'a' * 40,
        'files': {original: {'bytes': source.stat().st_size, 'sha256': digest}}}))
    monkeypatch.setattr(checks, 'FROZEN_LINK_SNAPSHOTS', {prefix: {
        'manifest_sha256': checks.sha(manifest), 'source_commit': 'a' * 40}})
    exceptions = {'links': [{'source': original, 'target': 'missing.md',
        'issue': 'missing', 'source_sha256': digest,
        'classification': 'historical', 'reason': 'Original absent artifact'}]}
    return {'root': tmp_path, 'original': original, 'copied': copied,
            'manifest': name, 'exceptions': exceptions,
            'paths': [original, copied, name]}


def test_only_exact_frozen_copy_inherits_existing_link_exception(frozen_link_fixture):
    f = frozen_link_fixture
    result = checks.check_links(f['root'], f['paths'], f['exceptions'])
    assert result['errors'] == []
    assert {e['source'] for e in result['inherited']} == {f['original'], f['copied']}


@pytest.mark.parametrize('mutation', ['copy', 'source_and_copy', 'manifest',
    'target', 'issue', 'new_document', 'arbitrary_copy', 'symlink', 'unlisted_original'])
def test_frozen_copy_exception_never_hides_new_or_changed_material(frozen_link_fixture, mutation):
    f = frozen_link_fixture
    root = f['root']
    if mutation in ('copy', 'source_and_copy'):
        (root / f['copied']).write_text('[old](missing.md) [new](new.md)\n')
        if mutation == 'source_and_copy':
            (root / f['original']).write_bytes((root / f['copied']).read_bytes())
    elif mutation == 'manifest':
        (root / f['manifest']).write_text('{}')
    elif mutation == 'target':
        f['exceptions']['links'][0]['target'] = 'different.md'
    elif mutation == 'issue':
        f['exceptions']['links'][0]['issue'] = 'fragment'
    elif mutation in ('new_document', 'arbitrary_copy'):
        name = 'snapshot/new.md' if mutation == 'new_document' else 'unregistered/report.md'
        p = root / name
        p.parent.mkdir(exist_ok=True)
        p.write_bytes((root / f['original']).read_bytes())
        f['paths'].append(name)
    elif mutation == 'symlink':
        (root / f['copied']).unlink()
        (root / f['copied']).symlink_to(root / f['original'])
    else:
        f['paths'].remove(f['original'])
    result = checks.check_links(root, f['paths'], f['exceptions'])
    assert result['errors']
