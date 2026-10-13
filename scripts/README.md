# Maintenance commands and script ownership

[Architecture](../docs/ARCHITECTURE.md) · [Reproduction guide](../docs/REPRODUCIBILITY.md) · [Preservation policy](../docs/VERSIONING.md)

Run commands from the repository root. The new interface consolidates command
selection, not scientific algorithms. Install `requirements-repository.txt` for
maintenance; scientific and visual work retains its own environment.

## Routine checks

```sh
python scripts/repo.py fast
python scripts/update_navigation.py --check
python scripts/repo.py preservation --require-tags
```

Fast checks parse tracked Python without generating bytecode, validate JSON and
current-status schema, inspect Markdown/reference links, heading/line anchors and
static HTML assets, check exact historical link exceptions, verify original bytes,
run archive metadata validation and bounded infrastructure tests. No data download,
scientific optimization, manuscript build or render occurs. Unignored new files are
checked before staging, so new private paths and broken links cannot hide locally.

The [exception register](../docs/migration/link-exceptions.json) records exact
source/target pairs and their source hashes: release-only assets, excluded sources,
or references preserved inside frozen evidence/checkpoint copies. Restorable bytes
are not described as broken science. A new missing target or fragment still fails.
Network availability and JavaScript-created links are separate checks.

```sh
# Validate metadata before replacing only explicitly marked navigation blocks.
python scripts/update_navigation.py

# Separate science environment; model, counterfactual and explicit-reference tests.
python scripts/repo.py science --report /new/outside-checkout/science.json

# Release check does not publish or download. Supply restored data for installed checks.
python scripts/repo.py release --data-root /absolute/archive-restored-root

# Independent source and packed-scene byte verification; no camera/job rewrite.
python scripts/repo.py atlas --data-root /absolute/legacy-restored-root \
  --scene-root /absolute/atlas-restored-root
```

`--report` accepts a new path outside the checkout and refuses overwrite. Omit it
for stdout-only checks. Atlas source dependencies use supplied restored bytes first,
then tracked source files; a mismatching supplied file never falls back silently.
Science expects the historical integration gate to return exit 2 **and** its stated
incomplete/null-clearance result. Expected refusal is not a successful historical solution.

## Preservation now and future research

The current migration default, `--preservation-scope migration`, protects all 2,967
original paths except the authorized root README and ignore rules. Both SHA256 and
the original Git blobs are checked; changing a baseline hash cannot conceal edits.
All five available historical tag targets must match; `--require-tags` also fails
when a tag is absent. CI fetches full history, and release checks require the tags.

After this migration is accepted, an explicitly approved active-laboratory revision
may switch its fast-check workflow to `--preservation-scope published`. This keeps
paper v1–v5/source packages, atlas v1, archive v1.0.0 manifests and original
publication records immutable while permitting active lab code to evolve. Review
that workflow change together with the new scientific specification and tests.
Do not rewrite the old baseline, old hashes or tags to make an edit pass. New accepted
products require additional version-specific preservation records and corresponding
validation; adding a version is not permission to replace its predecessor. The
current migration workflow intentionally retains the stronger migration scope.

## Shared-script responsibility index

| Script | Owner / purpose | Writes and precautions |
|---|---|---|
| `repo.py` | Repository maintenance: fast/science/preservation/release/atlas lanes | Optional external report; science tests use temporary fixtures |
| `repository_checks.py` | Reusable nonmutating status/link/identity/dependency checks | None |
| `update_navigation.py` | Current-publication navigation from one JSON index | Four delimited blocks in paper/atlas/status guides; never edits the author-maintained root README; `--check` never writes |
| `fetch_data.py` | Historical and archive distribution restoration | Verified cache, selected destination and receipt; refuses conflicts; `--verify-only` avoids extraction |
| `archive_io.py` | Shared archive filesystem, policy and integrity operations | Library used by restoring/building callers; not a user command |
| `archive_validate.py` | Metadata, schema, rights and optional installed-data checks | Optional report, which callers must place outside frozen reports |
| `archive_reproduce.py` | Isolated NOAA decoder replay and output comparison | Temporary tree and optional external report |
| `archive_geospatial.py` | Installed raster/building validation | Optional report; needs separate geospatial dependencies |
| `archive_source_links.py` | Source-route HTTP availability investigation | Network requests and report; availability is not permission |
| `archive_catalogue.py` | Release-authoring: catalogue/provenance regeneration | Rewrites candidate metadata; **not for published v1** |
| `archive_refine.py` | Release-authoring: evidence-bound catalogue refinement | Rewrites catalogue/lineage/report records; not routine maintenance |
| `archive_build.py` | Release-authoring: deterministic permitted-data bundles | Candidate manifests/checksums and selected output directory; published-state guard |
| `archive_prepare_metadata.py` | Release-authoring: citation and preservation exports | Rewrites generated metadata/proposed rights scope; does not grant a license |
| `archive_acceptance.py` | Release-authoring: isolated HTTP restore/replay acceptance | New work directory and report; rewrites only copied test manifests |
| `archive_preservation.py` | Original archive audit: compare source roots and historical Git state | Explicit report; no download; its older exact tag/dirty-state assumptions are a historical checkpoint, not today's migration gate |
| `archive_privacy.py` | Publication preflight: inspect selected public files | Review/report records; pattern scans do not prove absence of all secrets |
| `archive_package_review.py` | Private review/recovery packaging | Includes **private mixed-rights Git history**; never upload whole review directory |

Read `--help` and the implementation before running a release-authoring tool.
Some original scripts have fixed report locations. Execute investigations in a
disposable checkout, never over accepted release/manuscript evidence.

## Product-specific code

Scientific producers remain beside their model: `model/`, `counterfactual/`,
`approximation/`, `analytical/`, `integrated/`, `geospatial/` and `reconstruction/`
under the [laboratory](../research/checkers-runway13/README.md). Their frozen paper
copies are intentional self-contained snapshots, not helpers to deduplicate.

Atlas preparation, scene jobs, rendering, composition and gallery generation live
in [visual-atlas/v1/scripts](../visual-atlas/v1/scripts/RENDERER.md). `prepare.py`,
`make_jobs.py`, `assemble.py`, `build_gallery.py`, `verify.py` and `inventory.py`
write edition outputs/records. Rebuild in disposable space. The new `atlas` command
checks the 25 source inputs and 27 external scene members without changing those
records. It does not substitute for rendering or browser acceptance.

## CI costs and evidence

- Ordinary fast workflow: source/metadata checks and infrastructure tests only.
- Relevant-source/manual scientific workflow: the documented smoke lane.
- Manual release-integrity workflow: metadata by default; explicit `full_restore`
  downloads both original and archive distributions plus scenes into separate roots.
- Manual atlas workflow: official checksum-verified Blender 4.5.3 Linux installation,
  full source restoration, regenerated local jobs, **one selected view** in a detached
  disposable worktree. No accepted file is replaced. Linux fonts/rendering may differ
  from the original macOS run; produced pixels still require review.

These workflows have read-only repository permissions and no release/push/deployment
step. Uploads contain explicit test reports or requested representative render outputs,
not private caches. Configuration is not proof a hosted run passed; consult the
[observed validation record](../docs/migration/VALIDATION.md).
