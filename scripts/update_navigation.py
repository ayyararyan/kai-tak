#!/usr/bin/env python3
"""Render only delimited current-product navigation; --check never writes."""
import argparse
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def blocks(status):
    paper = next(p for p in status['papers'] if p['version'] == status['latest_paper'])
    archive, atlas = status['archive'], status['atlas']
    release = 'https://github.com/ayyararyan/kai-tak/releases/tag/'
    rows = []
    for p in status['papers']:
        label = 'Published' if p['status'] == 'published' else 'Historical working draft'
        rows.append(f"| {p['version']} | {label} · {p['pages']} pages | [PDF](../{p['pdf']}) | [Guide](../{p['guide']}) |")
    date = datetime.date.fromisoformat(status['as_of']).strftime('%d %B %Y').lstrip('0')
    return {
        ('papers/README.md', 'paper-index'): '\n'.join([
            f"## Latest published paper: {paper['version']}", '',
            f"[Read the {paper['pages']}-page PDF](../{paper['pdf']}) · [Editable source package](../{paper['source_package']}) · [Build guide](../{paper['guide']})", '',
            '| Version | Status | Read | Reproduction |', '|---|---|---|---|', *rows]),
        ('visual-atlas/README.md', 'atlas-current'): '\n'.join([
            f"**Published edition: {atlas['version']}.** {atlas['plates']} principal 4K plates, {atlas['views']} Blender views.", '',
            f"[Read the atlas PDF]({atlas['pdf'].removeprefix('visual-atlas/')}) · [Plate and methods guide]({atlas['entry'].removeprefix('visual-atlas/')}) · [Download editable scenes]({release}{atlas['tag']})"]),
        ('visual-atlas/README.md', 'atlas-gallery'): '\n'.join([
            '## Open the gallery', '',
            f"GitHub displays the [gallery HTML source]({atlas['gallery'].removeprefix('visual-atlas/')}); it does not host",
            'this directory as a live exhibition. After cloning, open that file in a browser,',
            'or serve the checkout locally:', '', '```sh',
            'python3 -m http.server 8000 --bind 127.0.0.1',
            f"# Open http://127.0.0.1:8000/{atlas['gallery']}", '```']),
        ('docs/PROJECT_STATUS.md', 'status-products'): '\n'.join([
            f"As of **{date}**, checked against GitHub main at `{status['audited_commit']}`.", '',
            '| Product | Current public version | Authority |', '|---|---|---|',
            f"| Checkers with Runway 13 | **{paper['version']}**, {paper['pages']}-page edition | [Paper index](../papers/README.md), [publication receipt](../{status['receipts']['paper']}) |",
            f"| Historical Research Archive | **{archive['version']}**, {archive['permitted_files']} permitted files in {archive['bundles']} bundles | [Archive](../{archive['entry']}), [release receipt](../{status['receipts']['archive']}) |",
            f"| Visual Atlas | **{atlas['version']}**, {atlas['plates']} principal plates / {atlas['views']} views | [Atlas](../visual-atlas/README.md), [delivery receipt](../{status['receipts']['atlas']}) |"]),
    }


def render(text, marker, content):
    start, end = f'<!-- {marker}:start -->', f'<!-- {marker}:end -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f'Expected exactly one marker pair: {marker}')
    before, tail = text.split(start)
    _, after = tail.split(end)
    return before + start + '\n' + content + '\n' + end + after


def update(root=ROOT, check=False):
    status = json.loads((root / 'docs/project-status.json').read_text())
    # Validate before writing any block, so invalid versions cannot become navigation.
    from repository_checks import validate_status
    errors = validate_status(root, status)
    if errors:
        raise ValueError('; '.join(errors))
    originals, rendered = {}, {}
    for (path, marker), content in blocks(status).items():
        p = root / path
        if p not in originals:
            originals[p] = p.read_text()
            rendered[p] = originals[p]
        rendered[p] = render(rendered[p], marker, content)
    changes = [(p, new) for p, new in rendered.items() if new != originals[p]]
    if not check:
        for p, new in changes:
            p.write_text(new)
    return [str(p.relative_to(root)) for p, _ in changes]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        changed = update(check=args.check)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'{exc}\n')
    print(('Stale' if args.check else 'Updated') + ' navigation: ' + (', '.join(changed) or 'none'))
    return int(args.check and bool(changed))


if __name__ == '__main__':
    raise SystemExit(main())
