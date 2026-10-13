# Project: Checkers with Runway 13 — Complete Repository Architecture and Reorganization

**Repository:** https://github.com/ayyararyan/kai-tak

**Author:** Aryan Ayyar

**Task:** Conduct a comprehensive, non-destructive architectural reorganization of the entire research repository.

## 1. Mission

The repository has grown substantially.

What began as an independent mathematical investigation of Hong Kong's Kai Tak Airport now contains several sophisticated, interconnected research outputs:

- Versioned research white papers.
- Mathematical derivations, optimization models and verification programs.
- Historical aerial photographs, survey maps and geographic reconstruction.
- Historical building and obstacle investigations.
- Photogrammetry and three-dimensional reconstruction.
- Weather and aviation evidence.
- A formal versioned research-data archive.
- A published visual atlas with high-resolution imagery and Blender scenes.
- Extensive scientific documentation, source inventories, intermediate outputs and verification reports.

The project has reached the point where further growth without deliberate organization will make it increasingly difficult to understand, maintain, reproduce and extend.

**Your job is to transform this repository into an exceptionally well-organized, beautiful, professional and sustainable research environment.**

This is a complete repository-architecture assignment.

It is not merely a README redesign.

It is not simply renaming directories.

It is not deleting files to make the repository appear cleaner.

And it is not an opportunity to rewrite the underlying scientific findings.

The objective is to create a coherent research system with excellent navigation, clearly defined responsibilities, disciplined versioning, documented provenance and robust reproducibility.

The finished repository should be understandable to a visiting professor, an aerospace engineer, a research assistant, a historian or a curious member of the public.

It must remain fully usable by the original researcher.

---

# 2. Begin by understanding the entire project

Before implementing changes, conduct a comprehensive inspection of the latest GitHub repository and its actual directory tree.

Do not work from an earlier snapshot or assume that the current README is authoritative.

Inspect:

- The default branch and active branches.
- Recent Git history.
- All published releases and tags.
- White-paper versions and their reproducibility packages.
- The complete historical research archive.
- The visual atlas and gallery.
- Research subprojects and their dependencies.
- Data acquisition and processing pipelines.
- Source manifests and scientific evidence ledgers.
- Shared and project-specific scripts.
- Test suites, dependency locks and validation procedures.
- Large generated outputs.
- Duplicated files and source snapshots.
- Existing documentation.
- Licensing and redistribution conditions.
- Untracked local files, where available.

### Important existing components

Pay particular attention to:

`research/checkers-runway13/`

`research/checkers-runway13/whitepaper/`

`research/checkers-runway13/reconstruction/`

`research/checkers-runway13/analytical/`

`research/checkers-runway13/integrated/`

`research/checkers-runway13/evidence/`

`research/checkers-runway13/geospatial/`

`archive/`

`visual-atlas/v1/`

`publication/`

`scripts/`

`tests/`

`data/kai-tak-2026-10-13/`

`CITATION.cff`

`DATA_SOURCES.md`

`NOTICE.md`

`README.md`

The currently published archive release is `archive-v1.0.0`, with nine catalogued collections and 418 permitted-data files distributed through five collection bundles.

The visual atlas has a published `visual-atlas-v1` release, twelve 4K image plates, seventeen Blender views, a gallery and independently packaged editable scenes.

The repository also contains historical snapshot, update and integration releases.

Inspect every one of these before designing the new organization.

Determine the actual latest completed white-paper version from the repository. Do not assume that a requested future version has already been published.

### First deliverable: a repository architecture audit

Create a report identifying:

1. All current top-level directories and their purposes.
2. Every major scientific or publication subsystem.
3. Canonical source files versus generated derivatives.
4. Current release and preservation boundaries.
5. Duplicate and overlapping documentation.
6. Duplicate data and repeated evidence snapshots.
7. Fragile relative paths and hardcoded absolute paths.
8. Hidden dependencies between research workstreams.
9. Broken links, missing files and stale documentation.
10. Areas where the project structure has become unnecessarily complicated.

Distinguish genuinely redundant material from historical evidence intentionally retained for reproducibility.

Do not delete or move anything during the audit.

---

# 3. Establish four clearly separated parts of the project

Organize the repository around four conceptual pillars.

## Pillar A — Research Papers

**Checkers with Runway 13**

This area contains the formal research manuscripts and their scientific publication packages.

It should be immediately obvious:

- What the latest paper is.
- How to read it.
- How to build it.
- Which results it reports.
- Which data and scientific snapshot support it.
- Where older versions are preserved.
- What changed between versions.

Avoid presenting working drafts, generated TeX intermediates, superseded manuscript fragments and accepted papers as though they have equal publication status.

Create a proper publication index.

Preserve all previously published manuscript versions, PDFs and accepted source packages.

## Pillar B — Historical Research Archive

**The Kai Tak Historical Research Archive**

This is the versioned evidence and data-distribution system.

It contains the public dataset catalogue, source provenance, rights records, manifests, collection descriptions and data-release tooling.

It must remain independent of the paper's publication schedule.

Preserve the existing published archive v1.0.0 exactly.

Do not rewrite its release assets, source hashes, immutable manifests, tags or attribution conditions.

Maintain a clear distinction between the catalogue's total research inventory and the subset legally redistributable in the public archive.

## Pillar C — Visual Atlas

**The Kai Tak Visual Atlas**

This is the visual reconstruction and public-communication project.

It includes:

- Storyboards.
- Historical visualizations.
- 3D scenes.
- Blender rendering pipelines.
- Annotated and unannotated image plates.
- Gallery assets.
- Figure provenance.
- Render verification.
- Camera metadata.
- Versioned visual releases.

Treat it as a serious, independent product.

Do not bury its finished figures beneath technical reconstruction scripts.

Preserve the published atlas v1, its camera definitions, original source hashes and external scene-bundle restoration requirements.

## Pillar D — Scientific Research Laboratory

**Historical Reconstruction and Flight Mathematics**

This is the active scientific workspace.

It contains mathematical models, exploratory derivations, source investigations, photogrammetry, historical registration, numerical optimization, experimental outputs and scientific verification.

Organize it for active research rather than public presentation.

Distinguish:

- Accepted scientific reference models.
- Active experiments.
- Incomplete research.
- Rejected hypotheses.
- Invalidated calculations.
- Frozen verification evidence.

Research can remain unfinished without making the repository structurally unfinished.

The public-facing products should consume documented results from this research foundation.

They should not require readers to navigate the entire experimental workspace.

---

# 4. Design a beautiful top-level architecture

Develop the simplest structure that gives the four pillars clear identities.

Use this conceptual organization as a starting point:

```text
kai-tak/
│
├── README.md
├── CITATION.cff
├── NOTICE.md
│
├── docs/
│   ├── START_HERE.md
│   ├── RESEARCH_MAP.md
│   ├── PROJECT_STATUS.md
│   ├── ARCHITECTURE.md
│   ├── REPRODUCIBILITY.md
│   ├── VERSIONING.md
│   └── CHANGELOG.md
│
├── papers/
│   └── README.md
│
├── archive/
│   ├── README.md
│   ├── CATALOGUE.md
│   ├── collections/
│   ├── catalogue/
│   ├── licensing/
│   ├── releases/
│   ├── reports/
│   └── ...
│
├── visual-atlas/
│   ├── README.md
│   ├── v1/
│   └── ...
│
├── research/
│   └── checkers-runway13/
│       ├── README.md
│       ├── whitepaper/
│       ├── foundations/
│       ├── analytical/
│       ├── approximation/
│       ├── model/
│       ├── counterfactual/
│       ├── reconstruction/
│       ├── geospatial/
│       ├── integrated/
│       ├── evidence/
│       ├── literature/
│       └── ...
│
├── scripts/
│
├── tests/
│
├── publication/
│
├── assets/
│
└── .github/
    └── workflows/
```

**This is a conceptual architecture, not an instruction to forcibly move every existing directory.**

Prefer preserving established canonical paths where moving them would invalidate frozen manifests, published source packages, archive restoration, scientific hashes or historical reproducibility.

For example, `papers/` may initially serve as the polished public publication index while accepted manuscript bytes retain their current immutable locations.

Future active work can adopt cleaner locations only when migrations have been fully tested.

If a different arrangement is demonstrably simpler and safer, propose and implement it.

Every top-level directory must have a distinct purpose.

Avoid creating empty architectural layers, repeated folder names or unnecessary abstraction.

---

# 5. Separate public presentation from technical infrastructure

The repository should offer different entry points for different readers.

### For the general public

Create a welcoming route to:

- The story of Kai Tak.
- The latest white paper.
- The most impressive historical images.
- The visual atlas.
- The research-data catalogue.

A reader should not be confronted immediately with thousands of JSON files, complicated source manifests or unfinished proof attempts.

### For researchers

Provide direct access to:

- Mathematical derivations.
- Scientific assumptions.
- Reproducible experiments.
- Model configurations.
- Data provenance.
- Historical source records.
- Verification and evidence reports.

### For developers and future research assistants

Provide a clear technical architecture explaining:

- Which modules are maintained.
- What each major script does.
- How dependencies are installed.
- Which outputs are generated.
- Which files are immutable.
- How to run tests.
- How new experiments should be created.
- How new releases should be prepared.

These audiences should navigate the same repository without needing identical documentation.

---

# 6. Rebuild the root README as an elegant project homepage

The README should not become a repository inventory.

Make it visually appealing, concise and memorable.

It should introduce the engineering question, explain the project in natural prose and guide readers toward the three major public outputs.

### Recommended reading experience

Open with:

**Checkers with Runway 13**

A short, compelling description of the historic Kai Tak approach.

Use one excellent existing image, preferably a verified historical visualization or an appropriate visual-atlas plate.

Immediately provide links to:

**Read the Paper**

**Explore the Historical Archive**

**View the 3D Atlas**

Then introduce the mathematical question, provide a short research overview, and show readers how to explore or reproduce the work.

Move detailed numerical tables, extensive caveats, long lists of reports and technical environment commands to their appropriate documentation pages.

Keep essential scientific scope clear without repeatedly interrupting the narrative.

Do not create fake badges, decorative counters, invented endorsements or promotional language.

Do not add generative artwork when suitable project assets already exist.

The README should feel like the homepage of a carefully curated independent research institute project.

---

# 7. Create a real research map

One of the most valuable improvements will be a document explaining how the various research areas connect.

Create:

`docs/RESEARCH_MAP.md`

It should describe the flow from historical observations to derived research.

For example:

**Historical source discovery**

→ **Acquisition and provenance**

→ **Geospatial registration and photogrammetry**

→ **Historical reconstruction**

→ **Mathematical modelling**

→ **Numerical calculations and verification**

→ **White-paper figures, visual atlas and published datasets**

Use an elegant diagram if it genuinely helps.

For each connection, identify the actual files, scripts, data identifiers or manifests that establish the dependency.

Do not imply that the unresolved historical obstacle reconstruction has already been integrated into a validated flight solution.

Readers should understand the project in a few minutes instead of reconstructing its architecture from thousands of files.

---

# 8. Establish disciplined ownership of data and code

One problem in rapidly expanding research repositories is that the same evidence gets copied into multiple experiments and manuscripts.

Audit such duplication carefully.

Identify each file as one of:

- Original source evidence.
- Immutable archival data.
- Canonical processed data.
- Scientific model source.
- Derived output.
- Publication snapshot.
- Verification receipt.
- Temporary working artifact.
- Superseded or invalidated artifact.

Define where the canonical instance of each **new mutable work product** belongs.

Avoid unnecessary copies in future research.

However, preserve intentional immutable source snapshots inside published manuscripts and releases.

A publication's frozen copy of evidence is not automatically redundant merely because identical bytes exist in the live research tree.

Do not deduplicate across preservation boundaries if doing so would harm self-contained reproduction.

Where possible, use stable identifiers, manifests and documented dependencies instead of untracked copies.

Never use symlinks to bypass archive security assumptions or to create fragile publication packages.

---

# 9. Preserve versioning and historical integrity

This is non-negotiable.

The project already has multiple independent version histories.

Maintain separate versioning for:

**White papers:** v2, v3, v4 and later accepted versions.

**Research-data archive:** v1.0.0 and future data releases.

**Visual atlas:** v1 and future atlas editions.

**Scientific models:** Explicit model configurations and accepted result snapshots.

These version numbers describe different things.

Do not synchronize them artificially.

Maintain exact historical release references, including:

- `snapshot-2026-10-13`
- `update-2026-10-13`
- `integration-2026-10-13`
- `archive-v1.0.0`
- `visual-atlas-v1`

Verify actual tag identities and preserve every published release.

Do not move accepted artifacts if source packages, release manifests or external references require their current paths.

Keep a documented migration map for every relocated file.

Do not rewrite Git history.

Do not delete or replace old release assets.

Do not regenerate frozen source hashes merely to suppress failed validation.

---

# 10. Organize research status properly

The existing repository includes substantial chronological project ledgers and many individual verification reports.

Preserve them as historical records.

But create a short, authoritative current-status document:

`docs/PROJECT_STATUS.md`

It should identify:

- Latest published white paper.
- Latest archive release.
- Latest visual-atlas release.
- Current major scientific achievements.
- Active research directions.
- Known unresolved evidence dependencies.
- Immediate next milestones.

Avoid making users read an enormous historical ledger to discover the current state.

Historical project ledgers should remain accessible as append-only research records.

Where possible, maintain one machine-readable current-status index that drives public navigation and release links.

Do not erase older decisions or retroactively edit accepted verification reports when status changes.

Clearly distinguish historical checkpoint statements from current project status.

---

# 11. Introduce a proper documentation system

Create or improve concise documentation for:

### Start here

How a first-time visitor can explore the project in five minutes.

### Architecture

What the major components are, who uses them, and how they depend on each other.

### Reproducibility

How to rebuild the white paper, validate the research, restore the data and reproduce the visual atlas.

### Versioning

How scientific models, papers, data releases and visual editions are versioned separately.

### Source and rights

Where original data came from and what permissions apply.

### Research status

What is established and what remains under investigation.

### Contributing or extending the project

How another researcher can submit a correction, reproduce a calculation, add historical evidence or propose a new reconstruction.

Do not create duplicate documentation that must be maintained in several places.

Use authoritative source documents and links.

Where several pages need the same changing version number or release URL, generate those references from maintained metadata where practical.

---

# 12. Make the repository operationally maintainable

Introduce appropriate automation without making the project unnecessarily complicated.

### Fast validation

Run on ordinary changes:

- Documentation link checks.
- Manifest and schema validation.
- Python syntax checks.
- Lightweight unit tests.
- Metadata consistency.
- File-path and asset-reference checks.
- Current-version navigation checks.
- License-boundary checks.

### Deeper research verification

Run separately, when explicitly requested or when relevant source files change:

- Numerical-model tests.
- Mathematical certificate verification.
- Geospatial reconstruction checks.
- Historical archive integrity checks.
- White-paper clean builds.
- Figure regeneration.
- Visual-atlas scene tests.

### Release verification

Require:

- Source and asset hash checks.
- Version consistency.
- Rights and provenance verification.
- Preservation of frozen references.
- Published-artifact existence.
- Reproducibility checks appropriate to the release.

Do not download gigabytes of historical data or rerender seventeen Blender scenes on every README change.

Use separate workflows for fast repository checks, scientific verification and expensive rendering.

Document dependencies and supported platforms honestly.

Never claim that a CI check has passed unless it was actually executed and observed.

---

# 13. Protect rights, provenance and sensitive files

The repository contains extensive material obtained through official public data portals, published documents and other source investigations.

Respect the current source-specific license structure.

The public archive v1.0.0 is a permitted-data subset, not an unrestricted publication of all catalogued material.

Preserve the existing distinctions between:

- Redistributable third-party data.
- Original authored content.
- Restricted external material.
- Rights-unresolved material.
- Metadata-only source records.
- Publication snapshots.

Do not introduce a blanket open-source license.

Do not silently relicense original or third-party work.

Do not inadvertently publish private correspondence, unpublished enquiry drafts, credentials, temporary download sessions, locally retained third-party scans or private source backups.

Keep audit and verification reports, including unresolved provenance warnings, accessible in appropriate technical locations.

The reorganization must not make historical evidence appear more complete or accurate than the scientific reports establish.

---

# 14. Implement the migration incrementally

Do not attempt one enormous directory move.

Use a controlled sequence.

## Phase A — Audit and blueprint

Inspect the repository and document the existing architecture.

Identify the proposed target structure.

Create an explicit migration table showing:

- Current path.
- Proposed path or retained canonical location.
- Reason for the decision.
- Dependency impact.
- Required compatibility changes.
- Validation procedure.
- Whether the file is immutable.

## Phase B — Build the navigation layer

Create the polished README, project map, publication index, visual-atlas entry point, documentation homepage and current-status index.

Do this without disturbing existing scientific paths.

## Phase C — Normalize actively maintained code

Where safe, consolidate duplicated helpers and clarify script responsibilities.

Improve naming and interfaces.

Preserve scientific algorithms and outputs.

Avoid refactoring mathematically sensitive code solely for aesthetic reasons.

Move active, nonfrozen components only after their dependencies are identified.

## Phase D — Improve archival and generated-output boundaries

Separate generated caches and temporary research files from maintained source.

Use `.gitignore` carefully.

Retain all published scientific evidence, accepted outputs and release data.

Identify opportunities to reduce unnecessary duplication without deleting frozen research history.

## Phase E — Implement automated validation

Run documentation, integrity, compatibility and scientific smoke tests.

Verify old and new navigation paths.

Test existing archive restoration and representative research-build workflows.

## Phase F — Final acceptance

Inspect the repository as an unfamiliar visitor.

Ask whether the project is now easy to explore, reproduce and extend.

Fix confusing navigation, stale links, misclassified files and redundant documentation.

Prepare a clean, reviewed migration branch or pull request.

Do not merge, force-push, alter published releases, or make irreversible public changes without explicit authorization.

---

# 15. Protect reproducibility with a before-and-after comparison

Before modifying paths or scripts, establish a baseline.

Record:

- The exact starting commit.
- Relevant release tags.
- Selected source hashes.
- Accepted PDF hashes.
- Archive manifest hashes.
- Visual-atlas scene-bundle references.
- Representative test outcomes.
- The existing data-restoration commands.
- Existing documentation links.

After the migration, rerun the corresponding checks.

For files that must remain immutable, require identical bytes.

For scripts that are intentionally refactored, require documented behavioral equivalence within their tested domain.

Verify that both historical restoration modes still work:

- The original dated research-snapshot restoration.
- The separate versioned archive v1.0.0 restoration.

Check that the visual atlas can still recover its externally packaged Blender scenes and their source dependencies.

If a migration breaks an established workflow, repair it before declaring completion.

Do not substitute a passing metadata check for an unperformed scientific computation.

---

# 16. Deliver an exceptionally clear research experience

Create a simple reader journey.

Someone arriving at the repository should be able to choose between three natural paths.

### Discover

Explore the story, white paper, visualizations and historical context.

### Investigate

Browse the historical archive, inspect research data and trace the evidence.

### Reproduce

Run mathematical models, rebuild figures, inspect algorithms and verify reported results.

The distinction should be visible in navigation, not explained through a long technical paragraph.

A new researcher should be able to find the relevant scientific subsystem quickly.

A general reader should not need to understand the repository's internal research history.

The appearance should be professional and restrained.

Use excellent Markdown hierarchy, appropriate imagery, consistent terminology and clear documentation links.

Avoid excessive icons, badges, decorative formatting, artificial enthusiasm and AI-generated promotional wording.

---

# 17. Required deliverables

Produce the following as actual repository artifacts.

### Architecture

- Repository audit report.
- Proposed and implemented architecture.
- Old-to-new file mapping.
- Dependency and ownership documentation.
- Research-system diagram.

### Navigation and documentation

- Redesigned root README.
- Start-here guide.
- Current project-status index.
- Publication index.
- Archive entry point.
- Visual-atlas entry point.
- Technical architecture document.
- Consolidated reproducibility guide.
- Versioning and preservation policy.

### Repository implementation

- Safely organized active project directories.
- Clarified script responsibilities.
- Appropriate generated-file exclusions.
- Updated imports and relative references where required.
- Compatibility mappings for migrated paths.
- Updated documentation and internal links.

### Validation

- Link and metadata validation tools.
- Lightweight automated checks.
- Relevant scientific smoke-test results.
- Archive restoration test results.
- Visual-atlas dependency verification.
- Before-and-after preservation report.

### Final handoff

Create a concise report explaining:

1. What was reorganized.
2. What was intentionally left unchanged.
3. Which duplicated materials were consolidated and why.
4. Which immutable versions and releases remain protected.
5. Which workflows were successfully retested.
6. Which validations were not run.
7. Any remaining structural or reproducibility problems.
8. What future contributors should know.
9. What the researcher must approve before merging.

Do not report success merely because the folder tree looks tidy.

---

# 18. Completion standard

The redesigned repository should satisfy five tests.

**Discoverability:** An unfamiliar reader can understand the project and find its most important outputs within one minute.

**Scientific integrity:** Models, evidence, claims and historical limitations retain their exact meaning.

**Reproducibility:** Established research and publication workflows continue to work.

**Preservation:** No published release, frozen artifact, verification record or source identity is silently changed.

**Sustainability:** Future papers, datasets, visualizations and research workstreams can be added without creating another disorganized collection of files.

The final result should feel like the carefully designed research repository of a serious, long-term independent scientific project.

It should reflect the standards of a strong academic research group while remaining accessible to the wider public.

The repository must be organized for the future, not merely cleaned up for today.

**Do the actual architectural work, preserve the science, validate the migration and produce a coherent, beautiful research environment.**

The project title remains:

**Checkers with Runway 13**

The final repository should make the intellectual ambition of the project visible through its organization, clarity and craftsmanship.