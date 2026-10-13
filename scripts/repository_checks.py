#!/usr/bin/env python3
"""Nonmutating checks for navigation, public metadata and frozen boundaries.

Network availability, historical scientific truth and browser layout are not
established by these checks. Old link defects have exact, inspectable identities.
"""
import ast
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = '125ebac16dc52a86998e2f6c4893e116bfca67d8'
PRESERVED_TAGS = {
    'snapshot-2026-10-13': 'fd0c0d85b6c514fc7f919542192f18b747f4e092',
    'update-2026-10-13': '6178eed1de49f66ac658acf5f5d26fa7e754b9ba',
    'integration-2026-10-13': '128f7006e8c929a878bd80bdf84521a97c45ee30',
    'archive-v1.0.0': '9f4f7b0cc47b2db0933bd4d20b4e3698f43a465d',
    'visual-atlas-v1': 'c39008bbdb400e5a0ca25bfb480af85f1b0e6047',
}
ATLAS_COVERAGE = {'input': 25, 'scene': 27}
MUTABLE_BASELINE = {'README.md', '.gitignore'}
# Only this sealed public proof snapshot may inherit existing historical links.
# The manifest is pinned independently of the mutable navigation metadata.
FROZEN_LINK_SNAPSHOTS = {
    'research/checkers-runway13/mathematical-note/v1/frozen-source/': {
        'manifest_sha256': '2379eab54afb7f1baa0a9f71501e558e98706148cdea6b51bbf4c960c8113a51',
        'source_commit': '78a9ce1c627f917c94306af5529d5e9ebeb743e8',
    },
}
V5_GRAYSCALE_MANIFEST = 'publication/v5-grayscale-20261014/correction-manifest.json'
# Pinning the manifest itself prevents a later joint file/hash rewrite from reusing this authorization.
V5_GRAYSCALE_MANIFEST_SHA256 = 'bae7bcc86f8346634eaeace9f70aaada01a16d0b89306eb37b7c59ae31aba408'
V5_GRAYSCALE_PREDECESSOR = 'bdcbcdb71065797d65c38a37348cb80ea6e1a4d3'
V5_GRAYSCALE_AUTHORIZATION = ('The v5 whitepaper is awesome - just one change: the same figures can be made '
                              'in grayscale and then recompile the pdf and update on Github main')
V5_ROOT = 'research/checkers-runway13/whitepaper/v5/'
V5_FIGURES = ('01_place', '02_bearings', '03_turn', '04_landing', '05_runway', '06_maps',
              '07_stereo', '08_wind', '09_certificate', '10_recorder', '11_weather',
              '12_rollout', 'A1_paths', 'A2_controls', 'A3_weather_context')
# This is one dated, explicitly authorized presentation correction, not a mutable
# V5 subtree. Each actually changed file also needs exact old/new identities.
V5_GRAYSCALE_PATHS = {V5_ROOT + name for name in (
    'scripts/figure_style.py', 'scripts/historical_figures.py', 'scripts/mechanics_figures.py',
    'scripts/evidence_figures.py', 'package_sources.py', 'README.md', 'SPEC.md', 'STATE.md',
    'VERIFICATION.md', 'REPRODUCIBILITY.md', 'VERSION_CHANGES.md', 'FIGURE_REDESIGN.md',
    'checkers-with-runway-13-white-paper-v5.pdf', 'checkers-with-runway-13-white-paper-v5-sources.zip',
    'qa/document_checks.json', 'qa/science_checks.json', 'qa/science_figure_semantics.json',
    'qa/figure_provenance.json', 'qa/package_manifest.json', 'qa/fonts.txt')}
V5_GRAYSCALE_PATHS.update(V5_ROOT + path for name in V5_FIGURES for path in (
    *(f'figures/{name}.{extension}' for extension in ('pdf', 'svg', 'png')),
    f'presentation/{name}.png', f'qa/figure-records/{name}.json'))
PRIVATE = re.compile(r'(^|/)(\.env(?:\..*)?|.*private-source-history.*|authorized_enquiries_[^/]*|REQUEST_DRAFTS\.md|.*ENQUIRY_DRAFT\.md|.*token.*\.json|id_(?:rsa|ed25519))($|/)', re.I)


def read(root, path):
    return json.loads((root / path).read_text())


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def git(root, *args, input=None):
    return subprocess.run(['git', '-C', str(root), *args], input=input,
                          text=True, capture_output=True, check=True).stdout


def public_files(root):
    """Tracked plus unignored additions: see pending work, not restored bulk files."""
    return sorted(set(git(root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').split('\0')) - {''})


def safe_reference(root, path):
    if not isinstance(path, str) or not path or '\\' in path or PRIVATE.search(path):
        return False
    p = Path(path)
    return not p.is_absolute() and '..' not in p.parts and (root / p).resolve().is_relative_to(root.resolve())


def validate_status(root, status):
    import jsonschema
    errors = [f'status schema: {e.json_path}: {e.message}' for e in
              jsonschema.Draft202012Validator(read(root, 'docs/project-status.schema.json'),
                                            format_checker=jsonschema.FormatChecker()).iter_errors(status)]
    if errors:
        return errors
    versions = [p['version'] for p in status['papers']]
    if len(set(versions)) != len(versions):
        errors.append('Duplicate paper versions')
    published = [p for p in status['papers'] if p['status'] == 'published']
    if not published or status['latest_paper'] != max(published, key=lambda p: int(p['version'][1:]))['version']:
        errors.append('Latest paper is not the highest published version')
    baseline = read(root, 'docs/migration/baseline.json')
    if status['audited_commit'] != BASELINE_COMMIT or status['tags'] != PRESERVED_TAGS or baseline['tags'] != PRESERVED_TAGS:
        errors.append('Audited commit/tag identities disagree with migration baseline')
    paths = [(p[k], p.get(h)) for p in status['papers'] for k, h in
             [('pdf', 'pdf_sha256'), ('source_package', 'source_sha256'), ('guide', '')] if p[k] is not None]
    paths += [(v, None) for k in ['entry', 'manifest'] for v in [status['archive'][k]]]
    paths += [(status['atlas'][k], None) for k in ['entry', 'gallery', 'pdf', 'scene_manifest']]
    paths += [(v, None) for v in status['receipts'].values()]
    note = status['mathematical_note']
    paths += [(note[k], note.get(h)) for k, h in
              [('pdf', 'pdf_sha256'), ('source_package', 'source_sha256'),
               ('guide', ''), ('delivery_manifest', ''), ('publication_receipt', '')]]
    for path, digest in paths:
        if not safe_reference(root, path):
            errors.append(f'Unsafe/private status path: {path}')
        elif not (root / path).is_file():
            errors.append(f'Missing status artifact: {path}')
        elif digest and sha(root / path) != digest:
            errors.append(f'Status artifact checksum mismatch: {path}')
    if errors:
        return errors
    errors.extend(validate_mathematical_note(root, note))
    for paper in status['papers']:
        version = paper['version']
        base = f'research/checkers-runway13/whitepaper/{version}'
        if paper['pdf'] != f'{base}/checkers-with-runway-13-white-paper-{version}.pdf' or paper['guide'] != f'{base}/README.md':
            errors.append('Paper version disagrees with artifact paths: ' + version)
        if paper['source_package'] and not re.fullmatch(r'checkers-with-runway-13-white-paper-' + re.escape(version) + r'-sources?\.zip', Path(paper['source_package']).name):
            errors.append('Paper version disagrees with source package: ' + version)
        qa_path = f'{base}/qa/document_checks.json'
        # v3's original QA is preserved within the v4 accepted package.
        if version == 'v3':
            qa_path = 'research/checkers-runway13/whitepaper/v4/qa/v3-baseline/document_checks.json'
        if not (root / qa_path).is_file():
            errors.append('Paper lacks versioned document QA: ' + version)
        else:
            qa = read(root, qa_path)
            if qa.get('pdf_sha256') != paper['pdf_sha256'] or qa.get('pages') != paper['pages']:
                errors.append('Paper page count/PDF identity disagrees with document QA: ' + version)
    if errors:
        return errors
    latest = next(p for p in published if p['version'] == status['latest_paper'])
    receipt = read(root, status['receipts']['paper'])
    for key, digest in [('pdf', 'pdf_sha256'), ('source_package', 'source_sha256')]:
        receipt_hash = receipt.get('artifacts', {}).get(Path(latest[key]).name, {}).get('sha256')
        readback_hash = next((row.get('sha256') for row in receipt.get('git_readback', {}).get('artifacts', []) if row.get('path') == latest[key]), None)
        if latest[digest] not in (receipt_hash, readback_hash):
            errors.append(f'Latest {key} is not pinned by its publication receipt')
    a = status['archive']
    manifest = read(root, a['manifest'])
    derived = {'version': 'v' + manifest['archive_version'], 'tag': manifest['release_tag'],
               'bundles': len(manifest['assets']), 'permitted_files': sum(x['files'] for x in manifest['assets']),
               'catalogue_artifacts': len(read(root, 'archive/catalogue/artifacts.json')['artifacts']),
               'datasets': len(read(root, 'archive/catalogue/datasets.json')['datasets']),
               'collections': len(list((root / 'archive/collections').glob('*/collection.json'))),
               'provenance_warnings': read(root, status['receipts']['archive'])['installed_validation']['warning_count']}
    for key, value in derived.items():
        if a[key] != value:
            errors.append(f'Archive {key}: status {a[key]!r} != evidence {value!r}')
    if manifest['status'] != 'published' or manifest['complete_historical_archive']:
        errors.append('Archive published-subset boundary changed')
    for asset in manifest['assets']:
        expected = 'https://github.com/ayyararyan/kai-tak/releases/download/' + a['tag'] + '/' + asset['name']
        if asset['url'] != expected:
            errors.append('Release URL/tag mismatch: ' + asset['name'])
        collection = read(root, str(Path(a['manifest']).parent / asset['manifest']))
        for member in collection['files']:
            if member['publication_decision'] != 'Redistribution permitted' or not safe_reference(root, member['path']):
                errors.append('Archive rights/private-member violation: ' + member['path'])
    atlas = status['atlas']
    if atlas['tag'] != 'visual-atlas-' + atlas['version'] or any(not atlas[k].startswith('visual-atlas/' + atlas['version'] + '/') for k in ('entry', 'gallery', 'pdf', 'scene_manifest')):
        errors.append('Atlas edition disagrees with paths/tag')
        return errors
    bundle = read(root, atlas['scene_manifest'])
    views = sum(m['path'].endswith('.blend') for m in bundle['members'])
    gallery = read(root, 'visual-atlas/' + atlas['version'] + '/metadata/gallery.json')
    if atlas['views'] != views or atlas['plates'] != len(gallery):
        errors.append('Atlas counts disagree with scene manifest/gallery')
    if atlas['tag'] != read(root, status['receipts']['atlas'])['release']['tagName']:
        errors.append('Atlas tag disagrees with receipt')
    if atlas['browser_acceptance'] == 'verified-local-chromium':
        browser = read(root, 'docs/migration/browser-acceptance.json')
        if browser.get('status') != 'passed' or len(browser.get('checks', [])) < 15 or not all(c.get('passed') is True for c in browser['checks']):
            errors.append('Local browser acceptance lacks its passing evidence')
        if browser.get('edition') != atlas['version'] or browser.get('gallery_path') != atlas['gallery'] or browser.get('gallery_sha256') != sha(root / atlas['gallery']):
            errors.append('Browser receipt does not bind the current edition/gallery bytes')
    return errors


def validate_mathematical_note(root, note):
    """Bind an independent accepted companion; do not relabel the white paper."""
    errors = []
    version = note['version']
    base = f'research/checkers-runway13/mathematical-note/{version}'
    names = {'pdf': f'certified-local-optimality-{version}.pdf',
             'source_package': f'certified-local-optimality-{version}-sources.zip',
             'guide': 'README.md', 'delivery_manifest': 'DELIVERY_MANIFEST.json'}
    if any(note[key] != f'{base}/{name}' for key, name in names.items()):
        return ['Mathematical-note version disagrees with artifact paths']
    qa_path = root / base / 'qa/document_checks.json'
    clean_path = root / base / 'qa/grayscale-clean-build.json'
    if not qa_path.is_file() or not clean_path.is_file():
        return ['Mathematical note lacks versioned document QA']
    qa = read(root, qa_path)
    clean = read(root, clean_path)
    delivery = read(root, note['delivery_manifest'])
    receipt = read(root, note['publication_receipt'])
    if (clean.get('production_pdf_sha256') != note['pdf_sha256']
            or clean.get('pages_compared') != note['pages'] or clean.get('passed') is not True
            or qa.get('pages') != note['pages'] or qa.get('failures')
            or qa.get('unresolved_references') is not False):
        errors.append('Mathematical-note page count/PDF identity disagrees with document QA')
    if any(delivery.get(key) != note[key] for key in ('title', 'pages', 'rendering_revision')) or delivery.get('version') != int(version[1:]):
        errors.append('Mathematical-note identity disagrees with delivery manifest')
    for key, digest in [('pdf', 'pdf_sha256'), ('source_package', 'source_sha256')]:
        matches = [a for a in delivery.get('assets', []) if a.get('path') == names[key]]
        if len(matches) != 1 or matches[0].get('sha256') != note[digest] or matches[0].get('bytes') != (root / note[key]).stat().st_size:
            errors.append('Mathematical-note asset is not bound by delivery manifest: ' + key)
        published = [a for a in receipt.get('assets', []) if a.get('path') == note[key]]
        if len(published) != 1 or published[0].get('sha256') != note[digest] or published[0].get('bytes') != (root / note[key]).stat().st_size or published[0].get('matches_git') is not True:
            errors.append('Mathematical-note asset is not bound by publication receipt: ' + key)
    commit = receipt.get('commit')
    if (not isinstance(commit, str) or not re.fullmatch(r'[a-f0-9]{40}', commit)
            or receipt.get('remote_commit') != commit or receipt.get('independent_bare_fetch_commit') != commit
            or receipt.get('full_tree_match') is not True):
        errors.append('Mathematical-note publication lacks matching remote verification')
    return errors


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.anchors = [], set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ['href', 'src', 'poster']:
            if key in values and values[key] and '${' not in values[key]:
                self.links.append(values[key])
        if values.get('srcset') and not values['srcset'].startswith('data:'):
            self.links.extend(item.strip().split()[0] for item in values['srcset'].split(',') if item.strip())
        if values.get('id'):
            self.anchors.add(values['id'])
        if tag == 'a' and values.get('name'):
            self.anchors.add(values['name'])


def parsed_document(text, markdown=True):
    """CommonMark reference/inline links, heading IDs, and static HTML assets."""
    parser = HTMLReferences()
    if not markdown:
        parser.feed(text)
        return parser.links, parser.anchors
    from markdown_it import MarkdownIt
    tokens = MarkdownIt('commonmark', {'html': True}).parse(text)
    links, anchors, counts = [], set(), Counter()
    for index, token in enumerate(tokens):
        if token.type == 'heading_open':
            inline = tokens[index + 1]
            title = ''.join(t.content for t in (inline.children or []) if t.type in ('text', 'code_inline', 'image'))
            slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
            count = counts[slug]
            counts[slug] += 1
            anchors.add(slug + (f'-{count}' if count else ''))
        for child in [token, *(token.children or [])]:
            if child.type == 'link_open':
                links.append(child.attrGet('href'))
            elif child.type == 'image':
                links.append(child.attrGet('src'))
            elif child.type in ('html_inline', 'html_block'):
                parser.feed(child.content)
    return links + parser.links, anchors | parser.anchors


def check_homepage_navigation(root, status):
    """Check current product routes without taking editorial ownership of README."""
    links, _ = parsed_document((root / 'README.md').read_text())
    targets = {unquote(urlsplit(link).path).removeprefix('./') for link in links}
    paper = next(p for p in status['papers'] if p['version'] == status['latest_paper'])
    required = [('paper', {paper['pdf'], 'papers/README.md'}),
                ('archive', {status['archive']['entry']}),
                ('atlas', {status['atlas']['entry'], 'visual-atlas/README.md'})]
    return ['Author-maintained README lacks current ' + label + ' route'
            for label, choices in required if not targets.intersection(choices)]


def check_links(root, paths, exceptions):
    allowed = {(x['source'], x['target'], x.get('issue', 'missing')) for x in exceptions['links']}
    records = {x['path']: x['sha256'] for x in exceptions.get('historical_records', [])}
    errors, inherited, checked, documents = [], [], 0, {}
    copied, copy_errors = frozen_copy_link_exceptions(root, paths, exceptions)
    allowed.update(copied)
    errors.extend(copy_errors)
    if records:
        errors.extend(validate_exceptions(root, {'links': [], 'historical_records': exceptions['historical_records']}, read(root, 'docs/migration/baseline.json')))
    inventory = {(root / name).resolve() for name in paths}
    directories = {parent for path in inventory for parent in path.parents if parent.is_relative_to(root.resolve())}
    for name in paths:
        p = root / name
        if p.suffix.lower() in ('.md', '.html') and p.is_file():
            documents[name] = parsed_document(p.read_text(), p.suffix.lower() == '.md')
    for source, (links, _) in list(documents.items()):
        if source in records:
            if sha(root / source) != records[source]:
                errors.append(f'Historical link-record changed: {source}')
            continue
        for target in links:
            url = urlsplit(target)
            if url.scheme == 'file':
                errors.append({'source': source, 'target': target, 'issue': 'machine-local-file-url'})
                continue
            if url.scheme or url.netloc:
                continue
            checked += 1
            decoded = unquote(url.path)
            destination = (root / decoded.lstrip('/') if decoded.startswith('/') else (root / source).parent / decoded) if decoded else root / source
            if not destination.resolve().is_relative_to(root.resolve()):
                issue = 'outside-repository'
            elif not destination.exists():
                issue = 'missing'
            elif destination.resolve() not in inventory and not (destination.is_dir() and destination.resolve() in directories):
                issue = 'not-public'
            elif re.fullmatch(r'L\d+(?:-L\d+)?', url.fragment) and destination.is_file() and destination.suffix.lower() not in ('.html', '.htm'):
                line_numbers = [int(n) for n in re.findall(r'\d+', url.fragment)]
                issue = None if 1 <= min(line_numbers) <= max(line_numbers) <= len(destination.read_bytes().splitlines()) else 'fragment'
            elif url.fragment and destination.suffix.lower() in ('.md', '.html'):
                name = destination.resolve().relative_to(root.resolve()).as_posix()
                if name not in documents:
                    documents[name] = parsed_document(destination.read_text(), destination.suffix.lower() == '.md')
                issue = 'fragment' if unquote(url.fragment) not in documents[name][1] else None
            else:
                issue = None
            if issue:
                row = {'source': source, 'target': target, 'issue': issue}
                if (source, target, issue) in allowed:
                    inherited.append(row)
                else:
                    errors.append(row)
    return {'checked': checked, 'inherited': inherited, 'errors': errors}


def frozen_copy_link_exceptions(root, paths, exceptions):
    """Inherit exact old link defects only for manifest-bound, unchanged copies."""
    inventory = set(paths)
    active = [(prefix, pin) for prefix, pin in FROZEN_LINK_SNAPSHOTS.items()
              if any(path.startswith(prefix) for path in inventory)]
    if not active:
        return set(), []
    baseline = read(root, 'docs/migration/baseline.json')
    errors = validate_exceptions(root, exceptions, baseline)
    if errors:
        return set(), errors
    original_hashes = {row['path']: row['sha256'] for row in baseline['files']}
    allowed = set()
    for prefix, pin in active:
        name = prefix + 'PUBLIC_SOURCE_MANIFEST.json'
        path = root / name
        if name not in inventory or path.is_symlink() or not safe_reference(root, name) or not path.is_file() or sha(path) != pin['manifest_sha256']:
            errors.append('Frozen link-copy manifest is missing or changed: ' + name)
            continue
        manifest = read(root, name)
        if manifest.get('source_commit') != pin['source_commit']:
            errors.append('Frozen link-copy source commit changed: ' + name)
            continue
        verified = {}
        for row in exceptions['links']:
            source, target = row['source'], row['target']
            copy = prefix + source
            if copy not in inventory:
                continue
            if copy not in verified:
                entry = manifest.get('files', {}).get(source, {})
                digest = original_hashes.get(source)
                p = root / copy
                verified[copy] = (source in inventory and safe_reference(root, copy)
                                  and not p.is_symlink() and p.is_file()
                                  and entry.get('sha256') == digest == row.get('source_sha256')
                                  and entry.get('bytes') == p.stat().st_size
                                  and sha(p) == digest)
                if not verified[copy]:
                    errors.append('Frozen historical-link copy differs from its original: ' + copy)
            if verified[copy]:
                allowed.add((copy, target, row.get('issue', 'missing')))
    return allowed, errors


def validate_exceptions(root, exceptions, baseline):
    """Exceptions cannot excuse a newly added source or a changed frozen document."""
    files = {r['path']: r['sha256'] for r in baseline['files']}
    errors = []
    cache = {}
    for row in exceptions.get('historical_records', []):
        source = row['path']
        if source not in files or source in MUTABLE_BASELINE or row.get('sha256') != files.get(source):
            errors.append('Historical record lacks frozen source identity: ' + source)
        elif not (root / source).is_file() or sha(root / source) != files[source]:
            errors.append('Historical record source bytes changed: ' + source)
    for row in exceptions['links']:
        source = row['source']
        if source not in files or source in MUTABLE_BASELINE or row.get('source_sha256') != files.get(source):
            errors.append('Exception lacks frozen source identity: ' + source)
            continue
        if not (root / source).is_file() or sha(root / source) != files[source]:
            errors.append('Exception source bytes changed: ' + source)
            continue
        if not row.get('classification') or not row.get('reason'):
            errors.append('Unclassified historical exception: ' + source)
        if source not in cache:
            cache[source] = parsed_document((root / source).read_text(), Path(source).suffix.lower() == '.md')[0]
        if row['target'] not in cache[source]:
            errors.append('Exception does not identify an actual frozen link: ' + source + ' → ' + row['target'])
    return errors


def v5_grayscale_correction(root, rows, original):
    """Validate the exact successor; keep the historical SHA/Git baseline intact.

    The manifest does not establish scientific or visual acceptance. It binds
    the separately reviewed grayscale artifacts and cannot exempt evidence,
    manuscript TeX, earlier editions, tags or arbitrary future revisions.
    """
    path = root / V5_GRAYSCALE_MANIFEST
    if not path.exists() and not path.is_symlink():
        return {}, []
    errors, replacements = [], {}
    if not safe_reference(root, V5_GRAYSCALE_MANIFEST) or path.is_symlink() or not path.is_file():
        return {}, ['Invalid grayscale correction manifest file']
    if sha(path) != V5_GRAYSCALE_MANIFEST_SHA256:
        return {}, ['Grayscale correction manifest differs from its reviewed SHA-256 pin']
    try:
        data = read(root, V5_GRAYSCALE_MANIFEST)
        fields = {'schema_version', 'correction_id', 'authorization', 'scope',
                  'baseline_commit', 'predecessor_commit', 'files'}
        if not isinstance(data, dict) or set(data) != fields or type(data['schema_version']) is not int or data['schema_version'] != 1:
            return {}, ['Invalid grayscale correction manifest schema']
        expected = {'correction_id': 'v5-grayscale-20261014',
                    'authorization': V5_GRAYSCALE_AUTHORIZATION, 'scope': 'grayscale-presentation-only',
                    'baseline_commit': BASELINE_COMMIT, 'predecessor_commit': V5_GRAYSCALE_PREDECESSOR}
        if any(data[key] != value for key, value in expected.items()):
            return {}, ['Grayscale correction identity/authorization changed']
        if not isinstance(data['files'], list) or not data['files']:
            return {}, ['Grayscale correction requires exact changed-file records']
        predecessor = {}
        for line in git(root, 'ls-tree', '-r', V5_GRAYSCALE_PREDECESSOR).splitlines():
            metadata, name = line.split('\t', 1)
            predecessor[name] = metadata.split()[2]
        seen = set()
        for record in data['files']:
            required = {'path', 'original_sha256', 'original_git_blob', 'sha256', 'git_blob'}
            if not isinstance(record, dict) or set(record) != required or not all(isinstance(v, str) for v in record.values()):
                errors.append('Malformed grayscale changed-file record')
                continue
            name = record['path']
            if name in seen or name not in V5_GRAYSCALE_PATHS or name not in rows:
                errors.append('Duplicate or unauthorized grayscale path: ' + name)
                continue
            seen.add(name)
            if not all(re.fullmatch('[a-f0-9]{64}', record[key]) for key in ('original_sha256', 'sha256')) or not all(re.fullmatch('[a-f0-9]{40}', record[key]) for key in ('original_git_blob', 'git_blob')):
                errors.append('Invalid grayscale digest: ' + name)
                continue
            if record['original_git_blob'] != original.get(name) or predecessor.get(name) != original.get(name) or record['original_sha256'] != rows[name]['sha256']:
                errors.append('Grayscale original identity disagrees with historical baseline: ' + name)
                continue
            old = subprocess.check_output(['git', '-C', str(root), 'cat-file', 'blob', original[name]])
            if hashlib.sha256(old).hexdigest() != record['original_sha256']:
                errors.append('Grayscale original SHA does not match retained Git bytes: ' + name)
                continue
            p = root / name
            if record['sha256'] == record['original_sha256'] or record['git_blob'] == record['original_git_blob']:
                errors.append('Grayscale record does not identify a changed successor: ' + name)
            elif not safe_reference(root, name) or p.is_symlink() or not p.is_file() or sha(p) != record['sha256'] or git(root, 'hash-object', '--', name).strip() != record['git_blob']:
                errors.append('Grayscale successor bytes do not match correction: ' + name)
            else:
                replacements[name] = record
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        errors.append('Grayscale correction could not verify preserved history: ' + str(exc))
    # A malformed/partly valid manifest never partially relaxes preservation.
    return ({} if errors else replacements), errors


def preservation(root, require_tags=False, scope='migration'):
    baseline = read(root, 'docs/migration/baseline.json')
    errors, checked, unavailable = [], 0, []
    if baseline['commit'] != BASELINE_COMMIT:
        errors.append('Baseline identity changed')
    rows = {x['path']: x for x in baseline['files']}
    original = {}
    try:
        for line in git(root, 'ls-tree', '-r', BASELINE_COMMIT).splitlines():
            metadata, path = line.split('\t', 1)
            original[path] = metadata.split()[2]
        if set(original) != set(rows):
            errors.append('Baseline path inventory does not match original commit')
    except subprocess.CalledProcessError:
        errors.append('Original commit unavailable: use full history (fetch-depth: 0)')
    corrections, correction_errors = v5_grayscale_correction(root, rows, original)
    errors.extend(correction_errors)
    def protected(path):
        return path not in MUTABLE_BASELINE and (scope == 'migration' or
            path.startswith(('archive/releases/v1.0.0/', 'visual-atlas/v1/', 'publication/')) or
            bool(re.match(r'research/checkers-runway13/whitepaper/(?:v[1-5]/|checkers-with-runway-13-white-paper-v[1-5])', path)))
    for path, record in rows.items():
        if not protected(path):
            continue
        p = root / path
        checked += 1
        expected_sha = corrections.get(path, record)['sha256']
        if p.is_symlink() or not p.is_file() or sha(p) != expected_sha:
            errors.append('Protected bytes changed or missing: ' + path)
    # Independent Git blob comparison prevents an edited SHA baseline concealing edits.
    live = [p for p in rows if protected(p) and (root / p).is_file()]
    if live and original:
        blobs = git(root, 'hash-object', '--stdin-paths', input='\n'.join(live) + '\n').splitlines()
        errors.extend('Original Git blob changed: ' + p for p, digest in zip(live, blobs)
                      if corrections.get(p, {}).get('git_blob', original.get(p)) != digest)
    if baseline['tags'] != PRESERVED_TAGS:
        errors.append('Baseline tag identities changed')
    for tag, expected in PRESERVED_TAGS.items():
        try:
            actual = git(root, 'rev-parse', '--verify', f'refs/tags/{tag}^{{commit}}').strip()
            if actual != expected:
                errors.append('Tag target changed: ' + tag)
        except subprocess.CalledProcessError:
            unavailable.append(tag)
            if require_tags:
                errors.append('Missing required release tag: ' + tag)
    return {'scope': scope, 'protected_files_checked': checked, 'tags_unavailable': unavailable,
            'exact_grayscale_successors_checked': len(corrections), 'errors': errors}


def check_public_boundaries(root, paths, baseline_paths):
    errors = []
    for path in paths:
        if PRIVATE.search(path):
            errors.append('Private path in publication tree: ' + path)
        if path not in baseline_paths and re.match(r'(?i)licen[sc]e(?:\.|$)', Path(path).name):
            errors.append('Unapproved blanket license: ' + path)
        if (root / path).is_symlink():
            errors.append('Symlinks are not publication substitutes: ' + path)
    return errors


def atlas_dependencies(root, data_root, scene_root):
    """Map only explicit repo-relative manifest paths; never rewrite camera/jobs."""
    errors, inputs, scenes = [], 0, 0
    for manifest, key, base, label in [('visual-atlas/v1/metadata/input_manifest.json', 'files', data_root, 'input'),
                                       ('visual-atlas/v1/metadata/scene_bundle.json', 'members', scene_root, 'scene')]:
        data = read(root, manifest)
        rows = data.get(key) if isinstance(data, dict) else None
        if not isinstance(rows, list) or len(rows) != ATLAS_COVERAGE[label]:
            errors.append(f'Atlas {label} manifest requires {ATLAS_COVERAGE[label]} members')
            continue
        seen = set()
        for row in rows:
            if not isinstance(row, dict) or not safe_reference(base, row.get('path')) or not isinstance(row.get('sha256'), str) or not re.fullmatch(r'[a-f0-9]{64}', row['sha256']) or type(row.get('bytes')) is not int or row['bytes'] < 1:
                errors.append(f'Invalid atlas {label} manifest member: {row!r}')
                continue
            name = row['path']
            if name in seen:
                errors.append(f'Duplicate atlas {label} member: {name}')
                continue
            seen.add(name)
            if row.get('available', True) is not True:
                errors.append('Recorded unavailable dependency: ' + name)
                continue
            # Source Git files can come from the checkout; restored bulk from explicit root.
            path = base / name
            if label == 'input' and not path.exists():
                path = root / name
            if not path.resolve().is_relative_to((root if path == root / name else base).resolve()) or path.is_symlink() or not path.is_file() or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
                errors.append(f'Atlas {label} missing/size/hash mismatch: {name}')
            if label == 'input':
                inputs += 1
            else:
                scenes += 1
    return {'input_files_checked': inputs, 'scene_members_checked': scenes, 'errors': errors,
            'scope': 'Source/scene byte identity only; no render or browser acceptance.'}


def fast(root=ROOT, preservation_scope='migration'):
    import yaml
    paths = public_files(root)
    errors = []
    parsed, syntax = 0, 0
    for name in paths:
        p = root / name
        if not p.is_file():
            errors.append('Missing tracked file: ' + name)
            continue
        try:
            if p.suffix == '.py':
                ast.parse(p.read_bytes(), filename=name)
                syntax += 1
            elif p.suffix == '.json':
                json.loads(p.read_text())
                parsed += 1
            elif p.suffix in ('.yml', '.yaml'):
                config = yaml.safe_load(p.read_text())
                if name.startswith('.github/workflows/') and (not isinstance(config, dict) or config.get('permissions') != {'contents': 'read'}):
                    errors.append('Workflow must retain read-only repository permissions: ' + name)
        except (ValueError, SyntaxError, UnicodeError) as exc:
            errors.append(f'{name}: {exc}')
        except yaml.YAMLError as exc:
            errors.append(f'{name}: {exc}')
    status = read(root, 'docs/project-status.json')
    status_errors = validate_status(root, status)
    errors.extend(status_errors)
    from update_navigation import update
    if not status_errors:
        errors.extend(check_homepage_navigation(root, status))
        errors.extend('Stale generated navigation: ' + p for p in update(root, check=True))
    exceptions = read(root, 'docs/migration/link-exceptions.json')
    baseline = read(root, 'docs/migration/baseline.json')
    errors.extend(validate_exceptions(root, exceptions, baseline))
    links = check_links(root, paths, exceptions)
    errors.extend(links['errors'])
    preserved = preservation(root, scope=preservation_scope)
    errors.extend(preserved['errors'])
    errors.extend(check_public_boundaries(root, paths, {x['path'] for x in read(root, 'docs/migration/baseline.json')['files']}))
    return {'python_syntax_files': syntax, 'json_files': parsed, 'links': links,
            'preservation': preserved, 'errors': errors}
