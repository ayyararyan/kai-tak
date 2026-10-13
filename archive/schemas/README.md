# Metadata contracts, schema 1.0.0

Run `scripts/archive_validate.py` with the pinned archive requirements. JSON Schema validates the artifact, dataset, source, provenance, collection, rights and release records. The validator additionally checks cross-record identities, safe paths, inclusion policy, checksums and the directed lineage graph. Explicit unknown values do not constitute verified provenance.

Stable `kt-*` dataset IDs identify a research object; `src-*` identifies a source product; `rights.*` identifies a channel-specific rights decision. `artifact-*` is a hash-derived identifier for a canonical path, not a content hash. SHA-256 identifies the exact version of its bytes. Distinct paths can contain identical content and remain distinct records. `source-version-*` and ZIP-member nodes describe versioned or embedded objects, not fabricated standalone files.

A `derived-from` edge records inputs; `generated-by` names a producer; `extracted-from` binds ZIP members; `frozen-snapshot-of` preserves paper evidence; `depends-on-exact-version` captures a pinned dependency. Source-attribution edges do not imply transformation or authorship. Unknown inputs are not inferred from folder membership.

Archive version, schema version, source revision, observation epoch, acquisition date and paper version are independent. Null means unknown/not assigned. Historical month precision is retained; verification timestamps are not acquisition dates. Schema-breaking changes require a major archive/schema revision and migration notes; published manifests must not be regenerated in place.
