# Project: The Kai Tak Historical Research Archive

## Mission

Work inside my existing GitHub repository:

**https://github.com/ayyararyan/kai-tak**

Researcher: **Aryan Ayyar**

Associated research white paper: **Checkers with Runway 13**

Your assignment is to audit, organize, document, license appropriately, and prepare a fully versioned public research archive of the historical, geospatial, meteorological, aviation, mathematical, and computational data already collected for this project.

**Do not merely propose a repository structure. Implement the organization, generate the catalogues and documentation, write the necessary scripts, run the integrity checks, and prepare a complete archival release.**

The intended result is a professional open-research resource that could be shared with:

- Independent researchers and students.
- Aviation historians and enthusiasts.
- Aerospace engineers and mathematicians.
- Hong Kong historical and geospatial researchers.
- Universities, museums and research libraries.
- Relevant civil aviation and public institutions.

The archive must be reproducible, discoverable, properly attributed, citable and understandable without requiring personal knowledge of the original research workflow.

The existing white paper retains its title, **Checkers with Runway 13**.

The data archive should have the public identity:

**The Kai Tak Historical Research Archive**

Subtitle:

*Historical Geography, Aviation Evidence, Flight Dynamics and Mathematical Reconstructions of Hong Kong's Kai Tak Airport.*

Preserve the existing GitHub repository and historical research artifacts.

---

# 1. Begin with a comprehensive repository audit

Before reorganizing anything, inspect the entire repository, including its Git history, existing GitHub releases, associated release assets, manifests, research directories, documentation, and file dependencies.

Do not assume that the latest README describes every file.

Inspect the following existing components at minimum:

- `README.md`
- `DATA_SOURCES.md`
- `NOTICE.md`
- `publication/snapshot_manifest.json`
- `publication/release_assets.json`
- `publication/integration_source_inventory.json`
- `publication/INTEGRATION_UPDATE.md`
- `scripts/fetch_data.py`
- `data/kai-tak-2026-10-13/`
- `research/checkers-runway13/`
- `research/checkers-runway13/reconstruction/`
- `research/checkers-runway13/geospatial/`
- `research/checkers-runway13/evidence/`
- `research/checkers-runway13/analytical/`
- `research/checkers-runway13/counterfactual/`
- `research/checkers-runway13/whitepaper/`

Also inspect all existing release tags, including the initial snapshot, subsequent research update and integrated-data release.

Determine their actual remote availability and current contents.

Do not infer that an archive exists simply because a manifest contains a URL.

Audit both tracked and untracked local files where available. Identify files excluded through `.gitignore`, external data bundles, symlinks, large files, caches, temporary data and existing reproducibility dependencies.

Produce an initial machine-readable inventory showing:

1. Relative file path.
2. File name and extension.
3. File size.
4. SHA-256 checksum.
5. Research category.
6. Original source or creator.
7. Acquisition or generation date, where known.
8. Date or historical epoch represented by the content.
9. Current storage location.
10. Existing release and version.
11. Whether the file is original, downloaded, transformed, derived or generated.
12. Redistribution and licensing status.
13. Scientific verification status.
14. Relationship to other files and scripts.
15. Whether it is required for reproducibility.

Identify missing files, broken references, duplicated data, inconsistent manifests, untracked dependencies and unverifiable archival claims.

**Do not delete, overwrite, move or normalize original evidence during this audit.**

Produce an audit report before implementing any structural changes.

---

# 2. Design a professional archival structure

The existing repository has accumulated substantial research material from multiple parallel workstreams.

Organize it so that a new researcher can immediately understand what exists and how to access it.

Prefer a non-destructive archive layer over a large-scale relocation of the original research workspace.

Consider this logical structure, adapting it to the existing repository:

## Archive collections

**01 — Historical Maps and Aerial Photography**

Historical survey maps, dated aerial imagery, source indexes, registration records and geographic coverage.

**02 — Historical Buildings and Urban Geography**

Building inventories, construction chronology, source-linked structure evidence, historical reconstruction, vanished-building uncertainties and date-specific geometry.

**03 — Terrain and Geospatial Data**

Digital terrain models, elevation information, coordinate systems, datums, source vintages, GIS processing and spatial derivatives.

**04 — Aviation and Flight Evidence**

Historical approach charts, runway geometry, publicly redistributable flight observations, reconstructed recorder traces, accident-report source references and annotated research outputs.

**05 — Weather and Meteorological Records**

NOAA observations, historical airport weather, wind records, decoded tables, source observations and quality-control reports.

**06 — Three-Dimensional Reconstruction**

Photogrammetry, point clouds, reconstructed surfaces, mesh data, camera assumptions, registration controls and reconstruction uncertainty.

**07 — Mathematical Models and Results**

Flight-trajectory models, numerical experiments, explicit equations, simulation outputs, certificates, analytical bounds and reproducibility data.

**08 — Research Figures and Visualizations**

Original scientific diagrams, maps, reconstructed views, plot inputs and scripts.

**09 — Documentation and Research Publications**

White papers, explanatory reports, technical appendices, bibliographies and methodological notes.

Keep collection identifiers stable across versions.

Existing internal research directories may remain in their current locations. The public archive can expose a curated collection view through metadata, manifests, links and immutable release packages.

Avoid duplicating large files unnecessarily.

Every collection should have a human-readable landing page and an associated machine-readable metadata record.

---

# 3. Establish a rigorous data-provenance system

This is one of the most important requirements.

Much of the research material has been assembled through extensive open-source investigation, including official government portals, open datasets, published aviation literature, archival records and downloaded historical material.

Every archived item must have a traceable provenance chain.

For each source, capture:

- Original title and creator or issuing organization.
- Source landing-page URL.
- Direct download URL, where appropriate.
- Source dataset identifier, archival reference or document number.
- Original publication date, if available.
- Actual observation, survey or capture date.
- Download or acquisition date.
- Original format, size and checksum.
- Source version and revision information.
- Original coordinate reference system and vertical datum where applicable.
- Known data-quality limitations.
- Rights holder and licensing terms.
- Transformation or processing steps.
- Resulting derived outputs and their checksums.
- Research reports or white-paper figures using that source.

Preserve the distinction between an event date, a source publication date, a dataset revision date and an acquisition date.

For example, modern Hong Kong building data must not be labelled as a complete reconstruction of 1993.

Similarly, a historical aerial-photo index must not be described as a collection of acquired full photographic frames.

Represent all important transformations as reproducible provenance chains:

**Original source → Downloaded artifact → Validated source → Transformation → Derived dataset → Scientific result → Figure or white-paper claim**

Maintain source-to-derivative relationships using stable identifiers rather than relying only on filenames.

Use a well-defined schema that can be validated automatically.

---

# 4. Conduct a formal licensing and redistribution audit

The objective is to make as much of the research publicly reusable as legally appropriate.

However, do not assume that material found through an open-source web search is automatically open-licensed or redistributable.

Treat copyright ownership, access conditions, redistribution permission and scientific reliability as separate questions.

### Review source-specific rights

Inspect the current official terms applicable to:

- DATA.GOV.HK.
- Hong Kong Common Spatial Data Infrastructure (CSDI).
- Hong Kong Lands Department datasets.
- Hong Kong historical survey-sheet datasets.
- Hong Kong Digital Aerial Photo open-data releases.
- Hong Kong Buildings Department data.
- NOAA/NCEI data.
- Civil Aviation Department publications.
- Third-party maps, diagrams, aircraft manuals and scholarly publications.
- Any additional external material included in the local research collection.

Do not generalize permission from one government dataset to an entire government archive.

Check the actual terms of the specific dataset and distribution channel.

### Classify each artifact

Assign one of the following publication decisions:

**Redistribution permitted:** Verified rights allow the material to be included, subject to recorded conditions.

**Original authored material:** The researcher owns the relevant rights and may choose an open license.

**Link-only:** The public catalogue may identify and link to the source, but the original file will not be redistributed.

**Permission required:** Redistribution depends on obtaining additional authorization.

**Rights unresolved:** Available evidence is insufficient to confirm redistribution permission.

**Excluded:** The material must not enter the public archive for legal, privacy, security or other documented reasons.

A successful download or public URL must never be treated as permission by itself.

For ambiguous cases, default to metadata and source links rather than republishing the files.

### Create a rights and licensing register

Produce:

- A source-by-source rights matrix.
- A list of applicable licenses and official terms.
- Required attribution statements.
- Redistribution restrictions.
- Notes on derivative works.
- Links to authoritative licensing pages.
- Verification dates.
- Outstanding permission questions.
- Explicit inclusion or exclusion decisions.

Where appropriate, preserve the source institution's required disclaimers and acknowledgment of intellectual-property ownership.

Do not imply endorsement by the Government of Hong Kong, the Civil Aviation Department, the Indian Navy or any other institution.

---

# 5. Introduce clear licenses for original research

The repository currently has no blanket open-source license for its original code and research.

Recommend a practical licensing structure for review and approval.

My preferred options to evaluate are:

| Original material | Candidate license |
|---|---|
| Original software, scripts and computational tools | MIT or Apache-2.0 |
| Original explanatory documentation and authored figures | CC BY 4.0 |
| Original research datasets and derived factual tables | CC BY 4.0 or CC0, where the researcher has sufficient rights |
| Third-party material | Original source-specific rights and conditions |

These are candidate licenses, not preapproved selections.

Check the actual authorship, dependencies, contributions and source restrictions before recommending a license.

Do not place an unrestricted repository-wide license over mixed-rights material.

Use clear directory-scoped license notices or other unambiguous file-level declarations where necessary.

Distinguish:

- Copyright ownership.
- Research attribution.
- Dataset citation.
- Redistribution permission.
- Software license.
- Data license.
- Scholarly publication license.

Prepare the recommended licenses and associated notices for author approval.

Do not finalize any new licensing grant, relicense third-party content or publish license changes without explicit authorization.

Make the eventual rights structure easy for an external researcher to understand.

---

# 6. Create versioned, immutable research-data releases

Establish a formal data archive series beginning with:

**Kai Tak Historical Research Archive — Data Release v1.0.0**

Use semantic versioning for the archive itself.

Keep this version series separate from:

- White-paper version numbers.
- Simulation-model versions.
- Historical data observation dates.
- Existing GitHub snapshot and integration tags.

Document the meaning of major, minor and patch releases.

### Versioning principles

A published data release must be immutable.

Never silently replace files in an accepted archival version.

Every release must have a fixed file manifest, checksums, a documented schema, clear provenance and source identities.

A researcher downloading Version 1.0.0 two years later should be able to reconstruct exactly the research artifact represented by that release.

If a correction changes published data, issue a new version and retain the original release and its correction notice.

If source data have been updated by an official provider, preserve the earlier version and record the new source revision separately.

Create an archive change log that identifies:

- Added data.
- Removed data.
- Corrected data.
- Changed processing procedures.
- Updated licensing decisions.
- Superseded scientific claims.
- Backward-incompatible schema changes.
- Known unresolved problems.

Preserve the historical GitHub releases already published. Do not rewrite their contents or reuse their tags.

### Release organization

Prepare appropriately sized, independently downloadable collection bundles.

Use deterministic archive construction where practical.

Include a machine-readable master release manifest describing which bundles constitute the complete release.

Record SHA-256 checksums, file counts, archive sizes, schema versions and required dependencies.

Avoid placing huge binary datasets directly into the Git source history.

Retain compact catalogues, scripts, documentation and manifests in Git.

Use release assets or suitable archival storage for large dataset files.

If incremental downloads are supported, ensure they are clearly distinguished from independently restorable complete snapshots.

---

# 7. Create an excellent public data catalogue

The archive must be navigable by someone who has never seen the research project.

Create a public catalogue with separate entries for each collection and significant dataset.

For each entry, show:

- Dataset name.
- Short description.
- Scientific purpose.
- Source or creator.
- Historical period.
- Geographic coverage.
- Coordinate system, where relevant.
- File formats.
- Number of records, photographs, sheets or features.
- Processing level.
- Verification status.
- Rights and reuse status.
- Download location or source link.
- Required attribution.
- Citation instructions.
- Known limitations.
- Relevant research publications.

Make clear distinctions between raw observations, cleaned data, reconstructed quantities, simulated outputs and mathematical certificates.

Where useful, support both human-readable Markdown catalogues and machine-readable JSON/CSV metadata.

Consider standards such as DataCite, schema.org/Dataset, STAC for geospatial imagery, and standard geospatial metadata conventions when they fit naturally.

Do not add elaborate standards merely for appearance.

The goal is practical interoperability and clarity.

---

# 8. Build a reliable archive download and verification workflow

Improve the existing `scripts/fetch_data.py` system rather than replacing a working solution without justification.

A new researcher should be able to:

1. Clone the GitHub repository.
2. Browse the archive catalogue.
3. Select one collection or a complete release.
4. Download the appropriate data.
5. Verify the downloaded archives.
6. Restore files to documented locations.
7. Reproduce selected derived outputs.
8. Check that all necessary source dependencies are available.

Support options such as:

- Listing available collections and releases.
- Downloading selected collections.
- Downloading an entire release.
- Verifying checksums without extraction.
- Reporting missing or externally restricted sources.
- Refusing conflicting overwrites.
- Producing a local integrity report.

Provide a simple, well-documented command-line interface.

Preserve backward compatibility with existing research scripts wherever possible.

Avoid requiring users to download the entire collection merely to reproduce one figure or analysis.

Downloads and extraction must be resistant to unsafe archive paths, malicious filenames, symlink escapes and inconsistent manifests.

Use atomic or recoverable operations so interrupted downloads do not leave corrupted datasets presented as valid.

---

# 9. Preserve the integrity of the scientific research

The archive must not make unsupported scientific claims.

For every research output, distinguish:

- Verified mathematical results.
- Validated numerical calculations.
- Synthetic model scenarios.
- Historical observations.
- Approximate source digitizations.
- Partially reconstructed surfaces.
- Unvalidated interpretations.
- Superseded or invalidated results.

The archive contains important research on Kai Tak's Runway 13, but the existing synthetic flight models have not established complete historical obstacle clearance, global optimality or operational aviation safety.

Document these distinctions clearly.

Historical photogrammetric outputs should not be labelled as survey-grade geometry without validation.

Keep original evidence and its derivatives separable.

Preserve known data inconsistencies instead of silently correcting them.

Include relevant verification reports and point to the white paper sections where each research output is used.

Do not remove historical research failures that are useful for understanding the development of the project. Place them in clearly identified provenance or superseded-results records, without presenting them as accepted findings.

---

# 10. Add reproducibility, citation and preservation support

Make the archive suitable for scholarly citation.

Prepare:

- `CITATION.cff`
- Dataset citation records.
- A structured version history.
- Recommended citations for individual collections.
- Creator and contributor metadata.
- Source attribution records.
- Metadata compatible with a long-term research repository.

Evaluate Zenodo as a long-term archival destination.

Prepare the metadata for both:

1. A concept-level archive identifier covering the archive series.
2. Version-specific identifiers for individual immutable releases.

Do not invent DOI values.

Do not imply that a GitHub release has been archived by Zenodo unless the actual files, metadata and persistent record have been verified.

Where third-party source material cannot be redistributed, deposit only permitted archival outputs and link to the source records.

Document precisely which bytes are preserved in the long-term archive versus which data require retrieval from external providers.

Prepare the first release for DOI registration, but do not perform external publication or deposition without authorization.

---

# 11. Create a professional archive homepage

The repository's landing page should be welcoming to a general reader while remaining technically useful.

A visitor should understand within one minute:

**What is this project?**

A historical and mathematical investigation of Kai Tak Airport's famous Runway 13 approach.

**What is available?**

Historical source catalogues, geospatial data, flight and weather evidence, reconstructions, mathematical models, figures, and research papers.

**How can I explore it?**

Through a clearly organized collection catalogue.

**How can I download it?**

Through versioned archives and documented download tools.

**Can I reuse it?**

Through source-specific rights and licensing information.

**How do I cite it?**

Through citation records and persistent identifiers once registered.

**What has actually been verified?**

Through an explicit account of source coverage, scientific methods, verification and limitations.

Make the white paper easily discoverable without allowing the research-publication directory to overwhelm the archive catalogue.

The README should be polished, concise, visually organized and free from promotional or exaggerated claims.

---

# 12. Add data-quality and archive-integrity tests

Create automated validation covering:

- Manifest schema correctness.
- Unique stable dataset identifiers.
- File hashes and sizes.
- Archive member counts.
- Duplicate content and path collisions.
- Source reference integrity.
- License metadata completeness.
- Inclusion/exclusion policy compliance.
- Dataset-to-source provenance links.
- Version consistency.
- Download and extraction safety.
- Backward-compatible paths.
- Required scientific metadata.
- Archive reproducibility.
- Broken source references.
- Missing dependencies.
- Unexpected generated or private files.

Include geospatial-specific checks where appropriate:

- Coordinate reference systems.
- Vertical datum documentation.
- Geographic coverage.
- Observation dates.
- Missing values.
- Invalid geometries.
- Historical versus modern data classifications.

Do not silently repair source data.

Document whether a failure concerns data integrity, historical accuracy, reproducibility or rights.

Provide tests that can run on a metadata-only checkout as well as additional checks that run when the large data archives are installed.

---

# 13. Implement safely and preserve the existing project

Create a dedicated development branch for the archive reorganization.

Preserve the existing main branch, research history, published white papers, original files, and immutable release tags.

Use a staged migration with a clear old-path-to-new-catalogue mapping.

Avoid broad renames unless they have a documented purpose.

If scripts currently depend on original research paths, preserve compatibility through explicit mappings or tested adapters.

Do not delete existing data simply because a duplicate is detected.

Report duplicates and propose safe consolidation.

Remove credentials, tokens, personal correspondence, private download-session information, confidential notes and unnecessary machine-specific metadata from any proposed public artifact.

Inspect the effects of all generated archive files before publication.

Do not automatically push to the public branch, create public releases, upload to Zenodo, select licenses, or contact external institutions without explicit permission.

Local implementation and testing are authorized. Public-release actions require a separate review.

---

# 14. Required final deliverables

Produce actual files and working implementations, not merely descriptions.

### A. Audit and migration

- Complete repository audit report.
- Master source inventory.
- Duplicate and dependency report.
- Rights and licensing audit.
- Existing-release verification.
- Old-to-new archive mapping.

### B. Public archive structure

- Archive homepage.
- Collection-specific READMEs.
- Human-readable data catalogue.
- Machine-readable dataset catalogue.
- Stable identifiers and metadata schemas.
- Provenance and attribution records.

### C. Licensing

- Source-specific license matrix.
- Recommended original-work licenses.
- Draft license and attribution files.
- List of restricted or unresolved items.
- Explicit author-approval decisions required.

### D. Version 1.0.0 archival package

- Complete archival release manifest.
- Collection-level manifests.
- Checksums.
- Schema and version documentation.
- Release notes.
- Downloadable release bundles, prepared where source bytes are available and redistribution has been verified.
- Explicit exceptions for missing or nonredistributable material.

### E. Software and verification

- Improved archive download tooling.
- Archive verification scripts.
- Automated integrity tests.
- Reproducibility instructions.
- Machine-readable verification reports.

### F. Publication preparation

- `CITATION.cff`.
- Long-term archival metadata.
- Proposed Zenodo deposition structure.
- Dataset citation examples.
- Public release checklist.
- Final archive publication summary.

### G. Executive handoff

Provide a concise final report with:

1. What was reorganized.
2. What data exist and in what quantity.
3. What has been verified.
4. What can legally be redistributed.
5. What remains restricted or unresolved.
6. Which existing releases have been preserved.
7. What new files and tools were created.
8. Whether the archive can be downloaded and restored from a clean environment.
9. What is ready for publication.
10. What requires author approval.

Include working links to files, local paths or proposed pull requests as applicable.

Do not declare the archive fully complete if critical source files cannot be accessed or essential rights have not been verified.

---

# 15. Acceptance criteria

The task is complete when an independent researcher can:

**Discover:** Understand which historical, aviation, geospatial and mathematical datasets exist.

**Verify:** Trace every substantive dataset to an original source, checksum and processing history.

**Download:** Obtain every publicly redistributable collection in a documented way.

**Reproduce:** Recreate specified derived research outputs from available source data.

**Cite:** Identify an exact dataset version and appropriate attribution.

**Reuse:** Understand the licenses, permissions and limitations applying to each artifact.

**Trust appropriately:** Distinguish established findings from assumptions, uncertain historical reconstructions and unfinished research.

**Preserve:** Recover an immutable archive version even after future research changes.

The project should ultimately be suitable for presentation as an independent public research resource to universities, aviation societies, museums, government research institutions and the wider Hong Kong community.

The ultimate objective is not to create an impressive-looking GitHub repository.

It is to create a **serious, durable, reusable and historically responsible open-research archive**, one that other researchers can build upon long after the original Kai Tak study has been completed.

**Implement the archive, validate the results, prepare Version 1.0.0, and provide a publication-readiness report. Preserve all existing scientific evidence and await authorization before making irreversible public changes.**
