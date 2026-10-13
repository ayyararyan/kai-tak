# The Kai Tak Historical Research Archive

*Historical Geography, Aviation Evidence, Flight Dynamics and Mathematical Reconstructions of Hong Kong's Kai Tak Airport.*

An independent historical and mathematical investigation of Kai Tak's Runway 13 approach, researched by **Aryan Ayyar**. Explore dated maps and photographs, urban geography, aviation and weather evidence, three-dimensional reconstructions, mathematical models and research publications.

**Archive v1.0.0 is an unpublished local candidate.** Existing research releases remain available. The new catalogue and permitted-data bundles are prepared for review; no new open license or DOI has been issued.

## Explore the collections

| | Collection |
|---|---|
| 01 | [Historical Maps and Aerial Photography](archive/collections/01/README.md) |
| 02 | [Historical Buildings and Urban Geography](archive/collections/02/README.md) |
| 03 | [Terrain and Geospatial Data](archive/collections/03/README.md) |
| 04 | [Aviation and Flight Evidence](archive/collections/04/README.md) |
| 05 | [Weather and Meteorological Records](archive/collections/05/README.md) |
| 06 | [Three-Dimensional Reconstruction](archive/collections/06/README.md) |
| 07 | [Mathematical Models and Results](archive/collections/07/README.md) |
| 08 | [Research Figures and Visualizations](archive/collections/08/README.md) |
| 09 | [Documentation and Research Publications](archive/collections/09/README.md) |

[Full catalogue](archive/CATALOGUE.md) · [Machine-readable datasets](archive/catalogue/datasets.json) · [Sources and provenance](archive/PROVENANCE.md)

## Read the research

**Checkers with Runway 13** retains its title. [White paper v2 (PDF)](research/checkers-runway13/whitepaper/v2/checkers-with-runway-13-white-paper-v2.pdf) · [Source and build instructions](research/checkers-runway13/whitepaper/v2/README.md). V1 is preserved; unfinished local v3 is excluded from this archive candidate.

## Download and reproduce

```sh
python3 scripts/fetch_data.py --list
python3 scripts/fetch_data.py --release v1.0.0 --collection 05 --archive-dir /path/to/candidate/bundles --offline
python3 scripts/archive_reproduce.py
```

The v1.0.0 command currently requires the locally prepared bundles; no public download URLs have been assigned. Without `--release`, the helper retains the existing five-group research-snapshot download. Both modes verify checksums and refuse conflicting overwrites.

[Download guide](archive/DOWNLOAD.md) · [Reproduction guide](archive/REPRODUCIBILITY.md) · [Release manifest and exceptions](archive/releases/v1.0.0/manifest.json)

## What is established—and what is not

The holdings include **227 acquired map editions**, **48 full DAP-L0 photographs**, modern geospatial sources, historical source indexes, approximate recorder-chart readings and synthetic flight calculations. Index records are not acquired photographic frames; modern buildings are not a complete reconstruction of 1993.

Byte integrity, mathematical validity and historical accuracy are different claims. The research has not established complete historical obstacle clearance, a globally optimal historical approach or operational aviation safety. Photogrammetric surfaces remain conditional reconstructions, not survey-grade geometry. Invalidated results are retained and labelled.

[Scientific status and limitations](archive/SCIENTIFIC_STATUS.md) · [Verification reports](archive/reports/) · [Publication readiness](archive/PUBLICATION_READINESS.md)

## Reuse and cite

Reuse is **source-specific**. Hong Kong open-data products retain their conditions and attribution requirements. Restricted documents and unresolved material are catalogued, not automatically repackaged. Original-work license proposals remain drafts; the [existing NOTICE](NOTICE.md) still applies.

[Rights and attribution](archive/licensing/README.md) · [Citation instructions](archive/CITATION.md) · [CITATION.cff](CITATION.cff) · [Preservation plan](archive/preservation/README.md)

No source institution endorses this independent archive. This is research material, not flight guidance.

## Snapshot boundary

This unpublished data candidate is pinned to research commit `128f7006e8c929a878bd80bdf84521a97c45ee30`. Separate work advanced the original checkout during preparation; newer white-paper material is recorded in the [concurrent-work audit](archive/audit/concurrent_work.json), not silently incorporated into these manifests. See the [publication-readiness report](archive/PUBLICATION_READINESS.md) for tested scope and remaining blockers.
