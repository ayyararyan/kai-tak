#!/usr/bin/env python3
"""Bounded maintenance lanes. Reports are opt-in; accepted outputs are never rewritten."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import re

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]


def run(command, cwd=ROOT, expected=0):
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    return {'command': command, 'cwd': str(cwd.relative_to(ROOT)), 'exit_code': result.returncode,
            'expected_exit': expected, 'passed': result.returncode == expected,
            'stdout': result.stdout, 'stderr': result.stderr}


def verify_current_scientific_bindings(commit):
    """Require identical scientific inputs and an append-only published ledger."""
    mapping_path = 'publication/scientific-results-20261013/source_public_mapping.json'
    mapping_bytes = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{commit}:{mapping_path}'])
    if (ROOT / mapping_path).read_bytes() != mapping_bytes:
        raise ValueError('Scientific publication mapping changed; new review required')
    mapping = json.loads(mapping_bytes)
    checked = 0
    for row in mapping['files']:
        path = ROOT / row['public_path']
        current = path.read_bytes()
        if row['public_path'] == 'research/checkers-runway13/PROJECT_STATE.md':
            original = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{commit}:{row["public_path"]}'])
            if not current.startswith(original):
                raise ValueError('Scientific ledger no longer preserves its published prefix')
            continue
        if len(current) != row['public_bytes'] or hashlib.sha256(current).hexdigest() != row['public_sha256']:
            raise ValueError('Scientific source changed since snapshot; new review required: ' + row['public_path'])
        checked += 1
    return checked


def public_scientific_snapshot():
    """Replay the publication at its own commit, including its then-current ledger.

    Later papers append PROJECT_STATE.md; rewriting the frozen source/public
    mapping or weakening its ledger check would erase preservation evidence.
    """
    receipt = ROOT / 'publication/scientific-results-20261013/remote_verification.json'
    commit = json.loads(receipt.read_text())['artifact_commit']
    if not re.fullmatch(r'[a-f0-9]{40}', commit):
        raise ValueError('Invalid scientific snapshot commit')
    checked = verify_current_scientific_bindings(commit)
    with tempfile.TemporaryDirectory(prefix='kai-tak-scientific-snapshot-') as directory:
        destination = Path(directory)
        archive = destination / 'snapshot.tar'
        with archive.open('wb') as stream:
            subprocess.run(['git', '-C', str(ROOT), 'archive', '--format=tar', commit,
                            'research', 'publication/scientific-results-20261013'], stdout=stream, check=True)
        with tarfile.open(archive) as package:
            package.extractall(destination, filter='data')
        archive.unlink()
        command = [sys.executable, 'publication/scientific-results-20261013/run_public_tests.py']
        result = subprocess.run(command, cwd=destination, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                                text=True, capture_output=True)
        return {'command': command, 'cwd': '<disposable public scientific snapshot>', 'snapshot_commit': commit, 'current_scientific_bound_files_checked': checked, 'ledger_prefix_preserved': True,
                'exit_code': result.returncode, 'expected_exit': 0, 'passed': result.returncode == 0,
                'stdout': result.stdout, 'stderr': result.stderr,
                'scope': 'Frozen public scientific snapshot, not later mutable ledger bytes.'}


def science():
    lane = ROOT / 'research/checkers-runway13'
    commands = [([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'model', 'counterfactual'], lane, 0),
                ([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'test_explicit_reference.py'], lane / 'approximation', 0),
                ([sys.executable, 'evaluate.py'], lane / 'integrated', 2)]
    runs = [run(command, cwd, expected) for command, cwd, expected in commands]
    # Exit 2 alone cannot prove the intended refusal; require the actual gate result.
    gate = runs[2]
    try:
        payload = json.loads(gate['stdout'])
        gate['passed'] = gate['passed'] and payload['overall'] == 'INCOMPLETE' and payload['candidate_historical_clearance'] is None and payload['historical_condition_cells_certified'] == 0 and payload['frozen_files_changed'] == []
    except (ValueError, KeyError):
        gate['passed'] = False
    runs.append(public_scientific_snapshot())
    return {'runs': runs, 'errors': ['Scientific lane failed: ' + ' '.join(x['command']) for x in runs if not x['passed']],
            'scope': 'Model/counterfactual/explicit-reference regressions, public scientific snapshot checks and expected historical refusal; not full optimization or scientific completeness.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lane', choices=['fast', 'science', 'preservation', 'release', 'atlas'])
    parser.add_argument('--data-root', type=Path, help='Explicit restored original-source root (atlas) or archive root (release)')
    parser.add_argument('--scene-root', type=Path, help='Explicit restored atlas scene root; no download occurs here')
    parser.add_argument('--report', type=Path, help='New JSON file outside protected trees; refuses overwrite')
    parser.add_argument('--require-tags', action='store_true', help='Fail if any of the five baseline tags is unavailable')
    parser.add_argument('--preservation-scope', choices=['migration', 'published'], default='migration',
                        help='Migration protects every baseline file; published is for later approved active-lab revisions')
    args = parser.parse_args()
    if args.report:
        resolved = args.report.resolve()
        if resolved.exists() or resolved.is_relative_to(ROOT):
            parser.error('--report must be a new file outside the checkout')
    if args.lane == 'atlas' and (args.data_root is None or args.scene_root is None):
        parser.error('atlas requires both --data-root and --scene-root')
    if args.scene_root and args.data_root is None:
        parser.error('--scene-root requires --data-root')
    try:
        if args.lane == 'science':
            report = science()
        else:
            import repository_checks as checks
            if args.lane == 'fast':
                report = checks.fast(preservation_scope=args.preservation_scope)
                report['runs'] = [run([sys.executable, 'scripts/archive_validate.py']),
                                  run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests'])]
                report['errors'] += ['Fast subprocess failed: ' + ' '.join(x['command']) for x in report['runs'] if not x['passed']]
            elif args.lane == 'atlas':
                report = checks.atlas_dependencies(ROOT, args.data_root, args.scene_root)
            else:
                report = checks.preservation(ROOT, args.require_tags or args.lane == 'release', args.preservation_scope)
                if args.lane == 'release':
                    report['errors'] += checks.validate_status(ROOT, checks.read(ROOT, 'docs/project-status.json'))
                    command = [sys.executable, 'scripts/archive_validate.py']
                    if args.data_root:
                        command += ['--data-root', str(args.data_root.resolve())]
                    report['runs'] = [run(command)]
                    report['errors'] += ['Archive metadata/installed check failed'] if not report['runs'][0]['passed'] else []
                    report['restoration_executed'] = False
                    report['restore_note'] = 'This command checks supplied files; use fetch_data.py for actual restoration. Without --data-root only metadata is checked.'
                if args.scene_root:
                    atlas = checks.atlas_dependencies(ROOT, args.data_root, args.scene_root)
                    report['atlas'] = atlas
                    report['errors'] += atlas['errors']
        report.update(lane=args.lane, checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      status='failed' if report['errors'] else 'passed')
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        report = {'lane': args.lane, 'status': 'failed', 'errors': [str(exc)]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open('x') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    summary = {k: v for k, v in report.items() if k not in ['runs', 'links']}
    if 'links' in report:
        summary['links'] = {'checked': report['links']['checked'], 'inherited_exceptions': len(report['links']['inherited'])}
    print(json.dumps(summary, indent=2))
    return int(report['status'] != 'passed')


if __name__ == '__main__':
    raise SystemExit(main())
