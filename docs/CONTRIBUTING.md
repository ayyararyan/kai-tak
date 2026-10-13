# Extending the project

[Project guide](README.md) · [Ownership](OWNERSHIP.md) · [Versioning](VERSIONING.md)

## A correction or new historical source

Identify the affected claim, artifact or source ID and give the evidence for the
correction. For a new record, include institution/product, acquisition route,
observation date, retrieval date, original URL, checksum where bytes are available,
rights and any uncertainty. An index entry is not proof that an image was acquired.
Do not attach restricted originals, private correspondence or credentials to an issue.

Use a branch and pull request for review. Source visibility does not itself grant a
licence; preserve all existing notices. A contribution must not imply independent
specialist review or a historical/operational claim that has not been established.

## A reproducible experiment

1. Locate its scientific subsystem through the [laboratory index](../research/README.md).
2. Read the canonical specification, latest ledger and validation record.
3. State the object, assumptions, identified/unidentified inputs and acceptance test.
4. Record exact input identities; keep temporary runs outside accepted artifacts.
5. Run relevant tests and an independent replay/check appropriate to the claim.
6. Record results, failure states and limitations. Retain rejected or invalidated
   evidence with its disposition instead of quietly deleting it.

Changes to model meaning, sample, assumptions, objective or validation require
the researcher's explicit decision. Engineering refactors require behavioral
equivalence evidence and must not change the scientific object to simplify code.

## A paper, archive or atlas edition

Follow the independent [versioning policy](VERSIONING.md). Do not edit a frozen
edition in place. Reuse canonical inputs by identity, or deliberately freeze copies
inside a self-contained publication package with a manifest. Include source rights,
change records, output hashes, clean reproduction and actual visual inspection.

Update [current-status metadata](project-status.json) only when acceptance and
publication evidence support the new status. Regenerate navigation and run the
[repository checks](REPRODUCIBILITY.md#fast-repository-checks). External publishing,
merging and licence grants remain explicit author decisions.

## Review checklist

- Can a new reader find the result from the relevant pillar entrance?
- Is each result observed, derived, estimated, scenario-based, proxy or unidentified?
- Are inputs, dependencies, producer and rights identifiable?
- Are frozen packages and historical tags unchanged?
- Did the actual relevant workflow run, and are unperformed checks named?
- Does the change keep private/restricted material out of Git and public assets?
