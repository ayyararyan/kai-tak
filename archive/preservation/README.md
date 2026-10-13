# Long-term preservation and Zenodo preparation

**No Zenodo record, DOI reservation or deposition has been performed or verified.** Draft metadata are not evidence of deposit. External publication remains unauthorized.

Zenodo is a suitable candidate for immutable versioned preservation and persistent citation. Its [versioning guidance](https://zenodo.org/help/versioning) distinguishes a concept DOI for the series from version-specific DOIs. Cite an exact version for reproducibility. Metadata can be prepared before authorization, but a DOI value must come from an actual verified record, never a guessed placeholder.

## Proposed deposit

1. Review and freeze the permitted bundle set and source-specific rights notices.
2. Include its exact collection/master manifests, catalogue, schemas, checksums, methodology, correction notices and verification reports.
3. Include an exact approved source-code/metadata snapshot; do not assume GitHub source archiving has preserved every separately attached data asset. Verify each deposited file name, size and checksum explicitly.
4. Deposit only permitted source bytes and approved original outputs. CAD/AIS, Boeing, private correspondence/session data, unresolved imagery and unapproved mixed figures stay out. Their non-sensitive source records and dependency notes remain.
5. After authorization, create the version record and obtain actual identifiers. Verify all bytes in the preserved record before citing it as archived. Link version records to the archive concept and the research repository.

[Concept draft](zenodo-concept-draft.json) · [Version draft and proposed files](zenodo-version-draft.json) · [DataCite mapping](datacite-draft.json) · [schema.org datasets](schemaorg-datasets.jsonld) · [Creator/contributor record](creators.json)

These are reviewable metadata mappings, **not submission-ready API payloads**: publication date, rights declarations and identifiers are intentionally unassigned. No affiliation, ORCID, endorsement or DOI is inferred.

## Exactly what is preserved

The local candidate data bundles preserve only their enumerated member bytes. The master manifest names every excluded catalogue artifact. Original repository commit `128f7006e8c929a878bd80bdf84521a97c45ee30` supplies the inherited research code/publications; the final archive-branch commit supplies the added tooling/metadata. Local release handoff records those commits separately. Before any deposition, include or independently archive approved source bytes and verify them; a Git URL by itself is an external dependency, not proof of long-term preservation.

The existing three GitHub releases have been downloaded/hash-checked but are not shown to be Zenodo-preserved. GitHub reported no immutable-release protection. Keep them intact; do not overwrite their assets or tags. Preserve failed/invalidated results and the documented frozen-manifest discrepancies without presenting them as accepted scientific findings.

Zenodo's [GitHub metadata guide](https://help.zenodo.org/docs/github/describe-software/) supports CITATION.cff and `.zenodo.json`, with `.zenodo.json` taking precedence if both exist. No root `.zenodo.json` is installed here: mixed-rights archival data require explicit deposit review rather than accidental software-release automation.

## Local review packaging

After committing reviewed source, run `python3 scripts/archive_package_review.py --bundles /outside/git/final-bundles --output-dir /new/outside/git/review-package`. This verifies every data member, creates a deterministic metadata/tooling tar, and verifies a Git bundle of the exact branch/history. `REVIEW_PACKAGE_MANIFEST.json` outside Git records their hashes and source commit. **The mixed-rights Git bundle is private preservation only; do not upload the whole review directory.** No new license applies to support files until author approval.
