> **Publication update 2026-10-13: [Data Release v1.0.0](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0) is the frozen public permitted-data release. Original-work license drafts remain inactive; no DOI. The preparation text below records the audited scope.**

# The Kai Tak Historical Research Archive

*Historical Geography, Aviation Evidence, Flight Dynamics and Mathematical Reconstructions of Hong Kong's Kai Tak Airport.*

An independent historical and mathematical investigation of Kai Tak's Runway 13 approach, researched by **Aryan Ayyar**. Explore dated maps and photographs, urban geography, aviation and weather evidence, three-dimensional reconstructions, mathematical models and research publications.

**[Data Release v1.0.0](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0)** contains 418 permitted files in five independently downloadable bundles. The catalogue describes 3,268 artifacts across 44 datasets. Rights and scientific limitations remain explicit; no new original-work license or DOI has been issued.

## Explore the collections

| | Collection |
|---|---|
| 01 | [Historical Maps and Aerial Photography](collections/01/README.md) |
| 02 | [Historical Buildings and Urban Geography](collections/02/README.md) |
| 03 | [Terrain and Geospatial Data](collections/03/README.md) |
| 04 | [Aviation and Flight Evidence](collections/04/README.md) |
| 05 | [Weather and Meteorological Records](collections/05/README.md) |
| 06 | [Three-Dimensional Reconstruction](collections/06/README.md) |
| 07 | [Mathematical Models and Results](collections/07/README.md) |
| 08 | [Research Figures and Visualizations](collections/08/README.md) |
| 09 | [Documentation and Research Publications](collections/09/README.md) |

[Full catalogue](CATALOGUE.md) · [Machine-readable datasets](catalogue/datasets.json) · [Sources and provenance](PROVENANCE.md)

## Read the research

**Checkers with Runway 13** retains its title. [White paper v4 (PDF)](../research/checkers-runway13/whitepaper/v4/checkers-with-runway-13-white-paper-v4.pdf) · [Sources and verification](../research/checkers-runway13/whitepaper/v4/README.md). Earlier paper versions remain unchanged. Their later publication does not change this archive release’s fixed data boundary.

## Download and reproduce

```sh
python3 scripts/fetch_data.py --list
python3 scripts/fetch_data.py --release v1.0.0 --collection 05
python3 scripts/archive_reproduce.py
```

The v1.0.0 command downloads from the versioned GitHub release. Without `--release`, the helper retains the existing five-group research-snapshot download. Both modes verify checksums and refuse conflicting overwrites.

[Download guide](DOWNLOAD.md) · [Reproduction guide](REPRODUCIBILITY.md) · [Release manifest and exceptions](releases/v1.0.0/manifest.json)

## What is established—and what is not

The holdings include **227 acquired map editions**, **48 full DAP-L0 photographs**, modern geospatial sources, historical source indexes, approximate recorder-chart readings and synthetic flight calculations. Index records are not acquired photographic frames; modern buildings are not a complete reconstruction of 1993.

Byte integrity, mathematical validity and historical accuracy are different claims. The research has not established complete historical obstacle clearance, a globally optimal historical approach or operational aviation safety. Photogrammetric surfaces remain conditional reconstructions, not survey-grade geometry. Invalidated results are retained and labelled.

[Scientific status and limitations](SCIENTIFIC_STATUS.md) · [Verification reports](reports/) · [Publication readiness](PUBLICATION_READINESS.md)

## Reuse and cite

Reuse is **source-specific**. Hong Kong open-data products retain their conditions and attribution requirements. Restricted documents and unresolved material are catalogued, not automatically repackaged. Original-work license proposals remain drafts; the [existing NOTICE](../NOTICE.md) still applies.

[Rights and attribution](licensing/README.md) · [Citation instructions](CITATION.md) · [CITATION.cff](../CITATION.cff) · [Preservation plan](preservation/README.md)

No source institution endorses this independent archive. This is research material, not flight guidance.

## Snapshot boundary

This data release is pinned to research commit `128f7006e8c929a878bd80bdf84521a97c45ee30`. Separate work advanced the original checkout during preparation; newer white-paper material is recorded in the [concurrent-work audit](audit/concurrent_work.json), not silently incorporated into these manifests. See the [publication-readiness report](PUBLICATION_READINESS.md) for tested scope and remaining blockers.
