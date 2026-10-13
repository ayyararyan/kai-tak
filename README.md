# kai-tak

![Illustration of a Cathay Pacific Boeing 747 approaching Kai Tak over Kowloon, with mountains behind the city.](assets/kai-tak-approach.png)

Historical reconstruction and mathematical study of the Kai Tak Runway 13 approach: dated Kowloon geometry, flight/weather evidence, constrained landing trajectories, and explicit approximations with verifiable bounds.

**Work in progress.** This repository is a snapshot of research assembled on 13 October 2026. It is not an operational flight procedure, a validated aircraft simulator, or a claim that the historical approach was globally optimal or suboptimal.

## What is here

| Research area | Starting point |
|---|---|
| Project decisions, chronology and unresolved requirements | [Project state](research/checkers-runway13/PROJECT_STATE.md) |
| Executable nominal landing model and reproduction instructions | [Model README](research/checkers-runway13/README.md) |
| Explicit approach, flare and stopping formulas | [Closed form and bounds](research/checkers-runway13/approximation/CLOSED_FORM_AND_BOUNDS.md) |
| Continuous-time feasibility witness and corrected optimality bounds | [Coupled analytical results](research/checkers-runway13/analytical/coupled/RESULTS.md) |
| Historical maps, aerial photographs and building chronology | [Reconstruction report](research/checkers-runway13/reconstruction/chronology/REPORT.md) |
| Registered sheets, block matching and 3D research | [Block-matching specification](research/checkers-runway13/reconstruction/block_matching/SPEC.md), [scene](research/checkers-runway13/reconstruction/block_matching/scene/README.md) |
| Actual CAL605 recorder/weather reconstruction | [Evidence specification](research/checkers-runway13/evidence/cal605_reconstruction/SPEC.md), [weather decoding](research/checkers-runway13/evidence/cal605_reconstruction/noaa/README.md) |
| Prior literature and contribution assessment | [Literature](research/checkers-runway13/literature/LITERATURE_AND_COMPARISON.md) |
| White-paper preparation in progress | [White-paper work](research/checkers-runway13/whitepaper/) |

The original `research/checkers-runway13/` and `data/kai-tak-2026-10-13/` layout is retained so relative paths in the research scripts continue to resolve.

## Current mathematical result

The synthetic nominal model has an explicit complete landing with a computer-assisted continuous-time feasibility certificate. The verified finite-family normalized-margin bracket is **[0.0397, 0.1559772)**. The earlier claimed 0.03972 upper bound was withdrawn after checker defects and must not be used.

This does **not** establish a near-global optimum, historical obstacle clearance, calibrated real-world prediction intervals, or robustness to unknown gusts. The fixed model uses scenario aircraft/braking assumptions. Source acquisition, historical geometry reconstruction and integration into the landing calculation have different completion states; the reports preserve those distinctions and invalidated runs.

## Run the core checks

Python 3.12 was used for the core publication checks. From the repository root:

```sh
cd research/checkers-runway13
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install mpmath==1.3.0
.venv/bin/python -m pytest model -q
(cd approximation && ../.venv/bin/python -m pytest test_explicit_reference.py -q)
```

The model README describes the scenario solver. Historical-mode refusal is intentional until its required calibrated inputs are supplied. Geospatial work has a separate [dependency lock](research/checkers-runway13/geospatial/requirements.lock); do not treat the numerical-model environment as the complete reconstruction environment.

## Download the larger datasets and outputs

Code, reports, source inventories and compact outputs are in Git. Bulky open-data sources, imagery, registered geometry, meshes and intermediate numerical exports are attached to the [initial research snapshot release](https://github.com/ayyararyan/kai-tak/releases/tag/snapshot-2026-10-13).

```sh
python3 scripts/fetch_data.py
```

The helper verifies archive SHA-256 values and restores the original repository-relative paths. It does not overwrite conflicting local files. See [data provenance and exclusions](DATA_SOURCES.md), [publication manifest](publication/snapshot_manifest.json), and [release asset manifest](publication/release_assets.json).

The release contains unfinished and explicitly invalidated research artifacts as historical evidence. Their inclusion is not a claim that they are accepted results. Completed source-data acquisition is not the same as a clearance-certified historical scene.

## Attribution and rights

Research by **Aryan Ayyar**, with AI-assisted implementation and review. Source data include the Lands Department and Buildings Department, Government of the Hong Kong Special Administrative Region; CSDI Portal; DATA.GOV.HK; NOAA/NCEI; and cited aviation publications. They retain their respective rights and terms. See [NOTICE](NOTICE.md).

No blanket open-source licence has been selected for the original research/code in this initial public snapshot. Public visibility does not relicense third-party material. Original aircraft accident-report scans and scholarly PDFs are linked and inventoried rather than republished where redistribution permission has not been established.
