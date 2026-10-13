#!/usr/bin/env python3
"""Extract a public test/proof closure from a pinned Git commit, never private files.

The bulk of this 34 MB subset exists to verify old seals and the 610-path public
disposition table. No restricted scan, account information or cache is copied.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

PIN = "78a9ce1c627f917c94306af5529d5e9ebeb743e8"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repository", type=Path, required=True)
parser.add_argument("--destination", type=Path, required=True)
parser.add_argument("--manifest-copy", type=Path)
parser.add_argument("--extend", action="store_true", help="verify and extend a draft subset without changing any copied source file")
args = parser.parse_args()
repo, target = args.repository.resolve(), args.destination.resolve()
if target.exists() and not args.extend:
    parser.error("destination already exists; choose a new directory")
if target.exists():
    old = json.loads((target / "PUBLIC_SOURCE_MANIFEST.json").read_text())
    assert old["source_commit"] == PIN
    for name, record in old["files"].items():
        data = (target / name).read_bytes()
        assert len(data) == record["bytes"] and hashlib.sha256(data).hexdigest() == record["sha256"]


def git_json(path):
    return json.loads(subprocess.check_output(["git", "show", PIN + ":" + path], cwd=repo))


publication = "publication/scientific-results-20261013/"
project = "research/checkers-runway13/"
mapping = git_json(publication + "source_public_mapping.json")
preserved = git_json(publication + "preserved_path_disposition.json")
paths = {row["public_path"] for row in mapping["files"]}
paths |= {project + row["path"] for row in preserved["paths"] if row["status"] != "not_in_git"}
paths |= {project + name for name in git_json(project + "integrated/source_manifest.json")["files"]}
paths |= {project + name for name in git_json(project + "counterfactual/inputs.json")["source_sha256"]}
paths |= {publication + name for name in ["README.md", "run_public_tests.py", "requirements.txt",
                                        "verify_public_snapshot.py", "source_public_mapping.json",
                                        "preserved_path_disposition.json", "verification.json"]}
paths |= {project + "requirements.lock", project + "analytical/verify_full_landing_analysis.py",
          project + "analytical/coupled/existence_and_bounds.py", "NOTICE.md"}
tar_bytes = subprocess.check_output(["git", "archive", "--format=tar", PIN, *sorted(paths)], cwd=repo)
target.mkdir(parents=True, exist_ok=True)
records = {}
with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as archive:
    for member in archive:
        if not member.isfile():
            continue
        assert member.name in paths and ".." not in Path(member.name).parts
        data = archive.extractfile(member).read()
        path = target / member.name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_bytes() == data, "existing snapshot file differs: " + member.name
        else:
            path.write_bytes(data)
        records[member.name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert set(records) == paths
manifest = {"source_repository": "https://github.com/ayyararyan/kai-tak", "source_commit": PIN,
            "purpose": "public mathematical proof/test and original seal verification closure",
            "restricted_inputs_included": False, "files": records,
            "file_count": len(records), "total_bytes": sum(r["bytes"] for r in records.values())}
encoded = json.dumps(manifest, indent=2) + "\n"
(target / "PUBLIC_SOURCE_MANIFEST.json").write_text(encoded)
if args.manifest_copy:
    args.manifest_copy.write_text(encoded)
print(json.dumps({k: v for k, v in manifest.items() if k != "files"}, indent=2))
