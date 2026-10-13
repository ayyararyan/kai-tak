# Archive versions and schema

Series: **Kai Tak Historical Research Archive — Data Release v1.0.0**. Current status: unpublished candidate. Schema: 1.0.0. It is independent of paper v1/v2, model v1, historical capture dates and prior snapshot/integration tags.

- **Major:** backward-incompatible metadata/restoration-path changes or removal/redefinition of dataset identities.
- **Minor:** additional collections/datasets or source revisions, preserving prior IDs and compatible schema; material scientific corrections should be at least a minor release.
- **Patch:** compatible corrections to metadata, checksums or processing outputs with a complete change record. Any changed published data bytes require a new version, never replacement.

Before first publication freeze exact member manifests, bundle/source/metadata hashes, source and rights identities, code commit, dependencies and unresolved exceptions. Candidate rebuilds are permitted locally and remain labelled candidates; accepted release tags/assets must never be overwritten or reused. Enable supported immutable-release controls at publication; verify protection, actual asset bytes and independent preservation separately.

An upstream revised file becomes a new source revision with its own hash and acquisition time. Retain old bytes/metadata, correction notices and superseded interpretations. Incremental downloads, if introduced, must be labelled deltas and name their complete base snapshot; current collection bundles are not deltas.

[CHANGELOG](CHANGELOG.md) · [Historical release verification](audit/existing_release_verification.json)
