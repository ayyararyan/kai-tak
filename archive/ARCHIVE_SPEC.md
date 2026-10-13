---
title: Kai Tak Historical Research Archive v1.0.0
type: feature
created: 2026-10-13
status: implemented-local-candidate-incomplete
baseline_commit: 128f7006e8c929a878bd80bdf84521a97c45ee30
context: [archive/requirements/AUTHORIZED_REQUEST.md, archive/audit/INITIAL_AUDIT.md]
---

# Archive implementation specification

<frozen-after-approval reason="Aryan explicitly authorized the complete attached implementation request; licensing/publication remain gated">

## Intent

Implement a durable, citable, discoverable archive of the existing Kai Tak research. The full [authorized request](requirements/AUTHORIZED_REQUEST.md) is normative; this specification organizes execution and does not narrow it. Public identity: **The Kai Tak Historical Research Archive**. Subtitle: *Historical Geography, Aviation Evidence, Flight Dynamics and Mathematical Reconstructions of Hong Kong's Kai Tak Airport.* Researcher: Aryan Ayyar. The white paper remains **Checkers with Runway 13**.

## Boundaries

Audit before structural edits. Preserve original evidence, scientific meaning, original research paths, dirty local work, main branch, history and all three published tags/releases. Use an additive archive layer on a dedicated branch. No broad renames, source repairs, source normalization or duplicate deletion. Inventory tracked, untracked, ignored, large, linked and external data. Distinguish source acquisition, observation, publication and revision dates; nulls mean unknown, never inferred from filesystem times.

Implement all 15 request sections and deliverables A–G. Collection IDs 01–09 remain stable. Every item gets a stable identity, checksum where bytes exist, provenance state, scientific status, rights decision and reproducibility classification. Distinguish raw, transformed, reconstructed, simulated, certified and invalidated outputs. A missing provenance edge remains an explicit completeness blocker, not an invented relationship.

Rights are source/channel-specific. Unknown rights default to metadata-only. Prepare draft MIT/Apache-2.0, CC BY 4.0/CC0 recommendations and precise scope; grant no new license. Preserve attribution and no-endorsement statements. Inspect contributors/dependencies, exclude private operational data, and never treat public accessibility as permission.

Prepare independent deterministic v1.0.0 collection bundles, master/member manifests and checksums from verified permitted bytes. Original-work open licenses remain unapproved; any authored-material candidates must be labelled approval-required. Archive semantic versions are independent of paper/model/source epochs. Retain old releases unchanged. Do not invent DOI or publish/deposit/push without separate authorization.

## I/O and failure semantics

| Input/state | Required behavior |
|---|---|
| Metadata-only clone | Browse nine collections; schema/policy/provenance checks run without large assets |
| Selected collection or complete candidate | Verify archive and member hashes/counts before safe restore to documented unchanged paths |
| Missing source, unverified rights or scientific calibration | Explicit typed exception/report; no fabricated source, permission or claim |
| Hash mismatch, duplicate member, unsafe path, symlink or conflicting destination | Fail closed; no conflicting overwrite or valid-looking partial result |
| Interrupted transfer | Recoverable temporary bytes; only verified archives become cache entries |
| Version correction | New version with retained old bytes and correction record, never silent replacement |
| External publication or license activation | Final author review; no automatic action |

</frozen-after-approval>

## Code map and implementation tasks

- `archive/audit/` — prechange inventory, Git/release verification, duplicate/dependency and final reconciliation reports.
- `archive/catalogue/` — dataset, source, artifact and provenance registries; human-readable catalogue and CSV exports.
- `archive/collections/01` through `09` — collection landing pages and metadata.
- `archive/schemas/` — JSON Schema contracts plus reference/policy validation.
- `archive/licensing/` — official rights matrix, exact source scopes, attribution, draft grants and approval decisions.
- `archive/releases/v1.0.0/` — fixed candidate master/member manifests, release notes, checksums and explicit exceptions. Large bundles outside Git.
- `scripts/fetch_data.py` — retain legacy defaults; add archive discovery, selection, safe download/restore and integrity reporting.
- `scripts/archive_*.py` — deterministic build, metadata/data checks and bounded reproducibility workflow.
- `tests/` — metadata, rights, archive reproducibility, extraction attacks and regression coverage.
- `README.md`, `CITATION.cff`, `archive/preservation/` — homepage, citations, Zenodo-ready planning metadata without fabricated DOI or license.
- `archive/STATE.md`, `archive/TRACEABILITY.md`, `archive/PUBLICATION_READINESS.md` — one task ledger, requirement coverage and executive handoff.

## Acceptance

Given the baseline and all locally accessible source roots, inventory every relevant file without mutating originals; report inaccessible or undocumented fields. Given published releases, verify actual remote bytes and exact member sets against corresponding manifests. Given source-specific rights, bundle only allowed files and report every excluded/restricted/missing item. Given a clean checkout, metadata checks pass without data; selected collections restore with byte-level verification; one or more named derived outputs reproduce independently. Given malformed inputs, adversarial archive tests fail before corrupting destinations. Given a publication candidate, every shipped byte has a checksum, source/creator, rights decision and restoration path. Unknown historical geometry/calibration remains unresolved in the scientific description. Final handoff separately reports correctness, requirement coverage, local restore readiness and publication blockers.

## Design notes

Use JSON Schema and compact Dataset-style records; no gratuitous STAC conversion of non-georeferenced imagery. Stable dataset IDs are semantic names, artifact IDs derive from canonical paths, source IDs identify institutional products. Multiple storage copies are locations of an artifact, not different observations. Unknown lineage is recorded as unknown and blocks a claim of complete provenance. Existing snapshot manifests remain historical artifacts and are not edited to conceal discrepancies.

## Verification

Run metadata validation, integrity/security unit tests, deterministic rebuild comparison, local HTTP download into a clean checkout, full member hash/size validation, existing scientific fixture checks and isolated NOAA producer replay. Test conflicting destinations and interruption cleanup. Compare baseline evidence hashes and tag identities after work. Record machine-readable outcomes and exact incomplete requirements.

## Publication authorization — 2026-10-13

Aryan: “Let’s publish it now.” Publish the reviewed permitted-data subset and archive navigation on GitHub, preserving documented unresolved rights/lineage. This authorizes push/release, not a new license selection or Zenodo deposition. Preserve later accepted main artifacts, exclude private authorised-enquiry directories, verify the remote tree and bytes.
