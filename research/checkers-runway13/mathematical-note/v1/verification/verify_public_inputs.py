#!/usr/bin/env python3
"""Verify the frozen public scientific snapshot with an append-only ledger check.

The original 2026-10-13 checker remains unmodified. Its exact-file PROJECT_STATE
binding predates the V5 ledger appends on current main. This additive check
requires the *entire original prefix* to retain the old hash, and binds the
entire current file to the accepted 78a9ce1 source commit. No scientific input
receives an exception and no private-source test is reported as passing.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path

PINNED_LEDGER_BYTES = 106014
PINNED_LEDGER_SHA256 = "63d7fc3a93962ae9a488afc9d8b8f5da83479f0dbd52ffbf670c5823015ba378"


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check(repo):
    root = repo / "research/checkers-runway13"
    publication = repo / "publication/scientific-results-20261013"
    mapping = json.loads((publication / "source_public_mapping.json").read_text())
    by_source = {r["source_path"]: r for r in mapping["files"]}
    require(len(by_source) == len(mapping["files"]), "duplicate mapping path")
    exceptions = []
    for row in mapping["files"]:
        path = repo / row["public_path"]
        data = path.read_bytes()
        if row["source_path"] == "PROJECT_STATE.md":
            require(digest(data[:row["public_bytes"]]) == row["public_sha256"], "historical ledger prefix changed")
            require(len(data) == PINNED_LEDGER_BYTES and digest(data) == PINNED_LEDGER_SHA256,
                    "current full ledger differs from pinned accepted main")
            exceptions.append({"path": row["public_path"], "historical_prefix_bytes": row["public_bytes"],
                               "historical_prefix_sha256": row["public_sha256"],
                               "pinned_full_bytes": len(data), "pinned_full_sha256": digest(data),
                               "appended_bytes": len(data) - row["public_bytes"],
                               "reason": "subsequent V5 publication ledger entries; exact old prefix preserved"})
        else:
            require(len(data) == row["public_bytes"] and digest(data) == row["public_sha256"],
                    "scientific/public mapping changed: " + row["public_path"])
    for row in mapping["exclusions"]:
        require(not (root / row["path"]).exists(), "excluded file present: " + row["path"])
    base = root / "integrated/assumption_solution"
    seals = 0
    for relative in ["artifact_manifest.json", "refinement/artifact_manifest.json",
                     "refinement/local_certificate/artifact_manifest.json"]:
        path = base / relative
        own = by_source[str(path.relative_to(root))]
        require(own["source_sha256"] == own["public_sha256"], "original seal transformed")
        for name, record in json.loads(path.read_text())["files"].items():
            row = by_source[str((path.parent / name).relative_to(root))]
            require(record["sha256"] == row["source_sha256"] and record["bytes"] == row["source_bytes"],
                    "sealed source binding differs: " + name)
            seals += 1
    preserved = json.loads((base / "refinement/local_certificate/preserved_snapshot.json").read_text())
    disposition = json.loads((publication / "preserved_path_disposition.json").read_text())["paths"]
    require(len(disposition) == len(preserved) == 610, "preservation count mismatch")
    require({r["path"] for r in disposition} == set(preserved), "preservation membership mismatch")
    for row in disposition:
        original = preserved[row["path"]]
        require((row["source_sha256"], row["source_bytes"]) == (original["sha256"], original["bytes"]),
                "preservation source binding differs")
        path = root / row["path"]
        if row["status"] == "not_in_git":
            require(bool(row["reason"]) and not path.exists(), "missing disposition no longer applies")
        else:
            data = path.read_bytes()
            require(len(data) == row["public_bytes"] and digest(data) == row["public_sha256"],
                    "preserved public mismatch: " + row["path"])
            if row["status"] == "normalized_git":
                original_mapping = by_source[row["path"]]
                require(bool(original_mapping["transformations"]) and
                        original_mapping["public_sha256"] == row["public_sha256"], "undocumented normalization")
            else:
                require(row["public_sha256"] == row["source_sha256"], "identical claim mismatch")
    require(seals == 224, "sealed entry count differs")
    return {"status": "PASS", "mapped_public_files": len(mapping["files"]),
            "scientific_byte_exceptions": 0, "append_only_ledger_binding": exceptions,
            "sealed_source_bindings": seals, "original_sealed_manifests": 3,
            "preservation_dispositions": dict(collections.Counter(r["status"] for r in disposition)),
            "scope": "public input integrity; no private-source reproduction claim"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.source.resolve()), indent=2))
