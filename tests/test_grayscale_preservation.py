"""The one authorized grayscale correction must not open frozen science to edits."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import repository_checks as checks


@pytest.fixture
def correction(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(tmp_path), *args], text=True).strip()

    git('init', '-q')
    names = [checks.V5_ROOT + name for name in
             ('scripts/figure_style.py', 'figures/01_place.svg', 'evidence/model.py', 'main.tex')]
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('original fixture\n')
    git('add', '.')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'frozen fixture')
    commit = git('rev-parse', 'HEAD')
    monkeypatch.setattr(checks, 'BASELINE_COMMIT', commit)
    monkeypatch.setattr(checks, 'V5_GRAYSCALE_PREDECESSOR', commit)
    monkeypatch.setattr(checks, 'PRESERVED_TAGS', {})
    baseline = {'commit': commit, 'tags': {}, 'files':
                [{'path': name, 'sha256': checks.sha(tmp_path / name)} for name in names]}
    baseline_path = tmp_path / 'docs/migration/baseline.json'
    baseline_path.parent.mkdir(parents=True)
    baseline_path.write_text(json.dumps(baseline))
    name = names[0]
    old_sha = checks.sha(tmp_path / name)
    (tmp_path / name).write_text('grayscale fixture\n')
    record = {'path': name, 'original_sha256': old_sha,
              'original_git_blob': git('rev-parse', f'{commit}:{name}'),
              'sha256': checks.sha(tmp_path / name), 'git_blob': git('hash-object', '--', name)}
    data = {'schema_version': 1, 'correction_id': 'v5-grayscale-20261014',
            'authorization': checks.V5_GRAYSCALE_AUTHORIZATION, 'scope': 'grayscale-presentation-only',
            'baseline_commit': commit, 'predecessor_commit': commit, 'files': [record]}
    path = tmp_path / checks.V5_GRAYSCALE_MANIFEST
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(data))
    monkeypatch.setattr(checks, 'V5_GRAYSCALE_MANIFEST_SHA256', checks.sha(path))
    return tmp_path, git, data, path, baseline, baseline_path, names


@pytest.mark.parametrize('scope', ['migration', 'published'])
def test_exact_correction_passes_and_preserves_old_git_bytes(correction, scope):
    root, git, data, _, _, _, names = correction
    result = checks.preservation(root, scope=scope)
    assert result['errors'] == []
    assert result['exact_grayscale_successors_checked'] == 1
    assert git('show', f'{data["baseline_commit"]}:{names[0]}') == 'original fixture'


def test_unlisted_grayscale_artifact_still_fails(correction):
    root, _, _, _, _, _, names = correction
    (root / names[1]).write_text('unrecorded different figure')
    result = checks.preservation(root)
    assert 'Protected bytes changed or missing: ' + names[1] in result['errors']


@pytest.mark.parametrize('kind', ['sha256', 'git_blob', 'actual_bytes', 'original_sha256',
                                  'original_git_blob', 'duplicate', 'empty', 'malformed',
                                  'authorization', 'scope', 'identity', 'missing_history'])
def test_correction_rejects_tampering_and_has_no_partial_exemption(correction, kind, monkeypatch):
    root, _, data, path, _, _, names = correction
    record = data['files'][0]
    if kind in ('sha256', 'original_sha256'):
        record[kind] = '0' * 64
    elif kind in ('git_blob', 'original_git_blob'):
        record[kind] = '0' * 40
    elif kind == 'actual_bytes':
        (root / names[0]).write_text('later unapproved update')
    elif kind == 'duplicate':
        data['files'].append(copy.deepcopy(record))
    elif kind == 'empty':
        data['files'] = []
    elif kind == 'malformed':
        data['files'].append({'path': 42})
    elif kind == 'authorization':
        data[kind] = 'An invented request'
    elif kind == 'scope':
        data[kind] = 'science-and-evidence'
    elif kind == 'identity':
        data['correction_id'] = 'future-correction'
    else:
        # Simulate a shallow clone with no retained original Git object.
        subprocess.run(['git', '-C', str(root), 'update-ref', '-d', 'refs/heads/master'], check=True)
        subprocess.run(['git', '-C', str(root), 'update-ref', '-d', 'refs/heads/main'], check=True)
        subprocess.run(['git', '-C', str(root), 'reflog', 'expire', '--expire=now', '--all'], check=True)
        subprocess.run(['git', '-C', str(root), 'gc', '--prune=now'], check=True, capture_output=True)
    path.write_text(json.dumps(data))
    # Deliberately move the pin here to exercise the independent semantic gates.
    monkeypatch.setattr(checks, 'V5_GRAYSCALE_MANIFEST_SHA256', checks.sha(path))
    result = checks.preservation(root)
    assert result['errors']
    assert result['exact_grayscale_successors_checked'] == 0
    assert 'Protected bytes changed or missing: ' + names[0] in result['errors']


@pytest.mark.parametrize('index', [2, 3])
def test_correction_cannot_authorize_evidence_or_manuscript(correction, index, monkeypatch):
    root, git, data, path, _, _, names = correction
    name = names[index]
    old_sha = checks.sha(root / name)
    (root / name).write_text('unauthorized scientific change')
    data['files'].append({'path': name, 'original_sha256': old_sha,
                          'original_git_blob': git('rev-parse', f'{data["baseline_commit"]}:{name}'),
                          'sha256': checks.sha(root / name), 'git_blob': git('hash-object', '--', name)})
    path.write_text(json.dumps(data))
    monkeypatch.setattr(checks, 'V5_GRAYSCALE_MANIFEST_SHA256', checks.sha(path))
    result = checks.preservation(root)
    assert 'Duplicate or unauthorized grayscale path: ' + name in result['errors']
    assert result['exact_grayscale_successors_checked'] == 0


def test_changed_original_sha_and_baseline_cannot_redefine_original(correction, monkeypatch):
    root, _, data, path, baseline, baseline_path, names = correction
    digest = data['files'][0]['sha256']
    baseline['files'][0]['sha256'] = digest
    data['files'][0]['original_sha256'] = digest
    baseline_path.write_text(json.dumps(baseline))
    path.write_text(json.dumps(data))
    monkeypatch.setattr(checks, 'V5_GRAYSCALE_MANIFEST_SHA256', checks.sha(path))
    result = checks.preservation(root)
    assert 'Grayscale original SHA does not match retained Git bytes: ' + names[0] in result['errors']
    assert result['exact_grayscale_successors_checked'] == 0


def test_without_correction_original_preservation_still_applies(correction):
    root, _, _, path, _, _, names = correction
    path.unlink()
    result = checks.preservation(root)
    assert 'Protected bytes changed or missing: ' + names[0] in result['errors']


def test_correction_manifest_cannot_be_a_symlink(correction):
    root, _, data, path, _, _, _ = correction
    target = root / 'alternate.json'
    target.write_text(json.dumps(data))
    path.unlink()
    path.symlink_to(target)
    assert 'Invalid grayscale correction manifest file' in checks.preservation(root)['errors']


def test_successor_and_manifest_cannot_be_jointly_rewritten(correction):
    root, git, data, path, _, _, names = correction
    (root / names[0]).write_text('a later unapproved presentation edit\n')
    data['files'][0]['sha256'] = checks.sha(root / names[0])
    data['files'][0]['git_blob'] = git('hash-object', '--', names[0])
    path.write_text(json.dumps(data))
    result = checks.preservation(root)
    assert 'Grayscale correction manifest differs from its reviewed SHA-256 pin' in result['errors']
    assert result['exact_grayscale_successors_checked'] == 0
    assert 'Protected bytes changed or missing: ' + names[0] in result['errors']
