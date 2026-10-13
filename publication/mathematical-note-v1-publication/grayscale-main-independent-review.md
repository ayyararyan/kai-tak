# Independent main-integration review

Reviewed at **2026-10-13T19:44:17Z**. Working integration HEAD: `4da2546e9a10c8e1f3e0e5485df2ba2fd75cb857`.
Main baseline: `96c19132c7b44329addfa47cab77d0afcb52bc88`.
Accepted grayscale artifact: `0146dba2f69759ee97739ab931db50df639e0e50`.

**Verdict: no actionable defect found in the reviewed integration diff.**
The review covered the checker, status schema/metadata, generated navigation,
reproducibility documentation, and the three publication-only note updates.
No code or scientific artifact was edited by this reviewer.

## Independently observed checks

- `pytest tests/test_repository_checks.py -q -p no:cacheprovider`: **63 passed**.
  The new negative cases reject changed copies, changed originals and copies,
  altered manifests, different target/issue pairs, new documents, arbitrary
  copies, symlinks and unlisted originals. Note tests reject invalid identities,
  hashes, page counts, unsafe paths, publication claims, receipt and QA binding.
- `scripts/update_navigation.py --check`: **no stale navigation**.
- Direct status validation: **zero errors**.
- Direct repository link check: **1,946 links checked; zero errors**.
- Frozen-copy inheritance: **exactly 17 allowed triples and 17 observed inherited
  copy links**, all matching their registered source/target/issue identities.
- `git diff --check`: **passed**.

The exception implementation does not skip a subtree. It requires the independently
pinned public-source manifest hash and scientific commit; an original exception
validated against the baseline and current original bytes; a public, safe,
nonsymlink copy whose digest and byte count match the manifest; and the exact
link target and issue. A failed identity check emits errors and does not add the
copy exception. The manifest contains 487 source records and its SHA-256 is
`2379eab54afb7f1baa0a9f71501e558e98706148cdea6b51bbf4c960c8113a51`.

## Preservation and publication meaning

The author-maintained root README is byte-identical to the main baseline
(SHA-256 `49635abe18071f5223075afd0c6f8217a962559253c15886a2492df35bf238a1`).
The navigation generator still excludes it. V5 remains the latest white paper;
the mathematical note has a separate repository-publication entry and does not
claim journal acceptance or a tagged release.

A complete tracked-note comparison against the accepted grayscale artifact found
only `README.md`, `STATE.md` and `DELIVERY_MANIFEST.json` changed. These explicitly
record subsequent publication activity and distinguish the immutable source-ZIP
snapshot from later live documentation. The manuscript, figures, scientific
inputs and frozen proof closure are unchanged.

The PDF, source ZIP and package manifest match the accepted artifact byte-for-byte:

| Artifact | SHA-256 |
|---|---|
| PDF | `10ac658ffa41e7fad5cd7da3a4be5e2ad013a0b9b27ac2d37100a45171d6c98f` |
| Source ZIP | `a0d84f7e12525f986c41e9a06545020cf0258e8f1fd0a4329a5341fdba62b84c` |
| Package manifest | `26ae68cc6c0cd250c3d318a7d0614d0c8f5d4e8a04be3a8eeb0e0ef23797844a` |

This is an independent maintenance/integration review, not a new scientific-proof
replay. The broader fast/preservation runs belong to the production lane. Hosted
CI and the eventual main push were not yet observed by this reviewer; this verdict
covers the local reviewed integration, not those subsequent operations.
