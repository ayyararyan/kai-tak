# Checkers with Runway 13

**[The Kai Tak Historical Research Archive](archive/README.md)** · [Data Release v1.0.0](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0) · [Nine collection catalogues](archive/CATALOGUE.md)

Historical Geography, Aviation Evidence, Flight Dynamics and Mathematical Reconstructions of Hong Kong's Kai Tak Airport.

**A lost airport. A 47° turn over Kowloon. The mathematics of getting an aircraft all the way to a stop.**

![Black-and-white illustration of a Boeing 747 approaching the former Kai Tak Airport over Kowloon](assets/kai-tak-approach-black-and-white.png)

*Cover artwork is an illustration, not a historical photograph or a reconstructed flight path.*

[**Read the white paper (v5, PDF)**](research/checkers-runway13/whitepaper/v5/checkers-with-runway-13-white-paper-v5.pdf) · [**Explore the research**](#explore-the-project) · [**Browse the data**](#historical-data-and-archive) · [**Reproduce the results**](#reproduce-the-research)

---

## An extraordinary approach, a deceptively simple question

Before it closed in 1998, Hong Kong's Kai Tak Airport was famous for an approach that brought large aircraft over densely built Kowloon. Runway 13 used an **offset Instrument Guidance System (IGS)** followed by a **visual right turn** toward the runway. The published instrument and runway directions differ by about **47°**. The final turn required visual references; it was **not** a zero-visibility landing procedure.

The view was spectacular. The engineering question is more interesting:

> **How could an aircraft turn, descend, align with Runway 13, touch down, and still have enough distance to stop?**

This independent project investigates that question through historical maps, dated aerial photographs, flight and weather evidence, three-dimensional surface reconstruction, explicit flight-dynamics models, and computer-assisted mathematical verification.

It also asks where the available evidence **stops**: a mathematically feasible path inside a simplified model is not a verified historical flight path or an aviation-safety finding.

## Latest mathematical results — assumption-conditional local certificate

[**Read the new local-optimality report**](research/checkers-runway13/integrated/assumption_solution/refinement/local_certificate/REPORT.md) · [Derivation and proof](research/checkers-runway13/integrated/assumption_solution/refinement/local_certificate/DERIVATION.md) · [Conditions and refinement](research/checkers-runway13/integrated/assumption_solution/refinement/REPORT.md) · [Reproduce this snapshot](publication/scientific-results-20261013/README.md)

A validated interval proof establishes a **strict local primary optimum in five flare variables** and a connected **non-strict local primary optimum in the 12-parameter trajectory family**. The exact implicit root is near η = 0.1523607643018617; the safe global-family bracket **[0.15236076430186170190, 0.181970215] remains unmatched**. Ten condition points have certified complete paths; this is not a complete condition-to-optimum formula or domain map.

The rounded root path touches down **302.126459 m** past the threshold, stops at **2234.377025 m**, and leaves **551.622975 m**. It is distinct from the unchanged delivered secondary path, whose primary loss is certified ≤10⁻⁴ against this proved **local** primary optimum. Global primary/secondary optimality remains open. The 5 kt tailwind and 60/65 m urban cases are unresolved, not proved infeasible; **historical certification remains false**. These conditional results use explicit geometry and aircraft assumptions.

This is a new, additive scientific layer. The frozen manuscripts, older synthetic examples, historical archive and visual atlas retain their own dates, evidence and claims.

## Start with the paper

### [Checkers with Runway 13 — Version 5](research/checkers-runway13/whitepaper/v5/checkers-with-runway-13-white-paper-v5.pdf)

**38 pages · 15 redesigned scientific illustrations · Seven-act engineering investigation · Eight technical appendices**

Why can a modest bank accumulate a 47-degree turn? Why might reaching the runway leave too little pavement to stop? The rewritten paper follows those questions from the lift vector to the ground roll, then returns to dated photographs, recovered surface geometry, wind and the CAL605 accident record. Physical calculations and historical evidence carry the narrative.

[Read the PDF](research/checkers-runway13/whitepaper/v5/checkers-with-runway-13-white-paper-v5.pdf) · [Read the abstract](research/checkers-runway13/whitepaper/v5/abstract.md) · [Download editable sources](research/checkers-runway13/whitepaper/v5/checkers-with-runway-13-white-paper-v5-sources.zip) · [Inspect claims and evidence](research/checkers-runway13/whitepaper/v5/CLAIMS_AND_EVIDENCE.csv) · [Verification report](research/checkers-runway13/whitepaper/v5/VERIFICATION.md)

![Three original aerial frames locating Kai Tak, Kowloon City, Checkerboard Hill and the bay](research/checkers-runway13/whitepaper/v5/figures/01_place.png)

*Separate Lands Department source frames, not a stitched panorama or a reconstructed flight path. The October images and the November catalogue/handwritten-date discrepancy retain their source labels. See [rights and provenance](research/checkers-runway13/whitepaper/v5/RIGHTS_AND_PROVENANCE.md).*

V5 preserves V4's RFS-based academic typography while substantially rewriting the prose and redesigning the complete figure system. All 38 pages were visually inspected; a clean source-package build matched their text and rendered pixels, and all 60 figure exports reproduced byte-for-byte. The underlying model, two separate certificates and historical evidence remain unchanged. The first-person foreword remains marked for author review; no independent human specialist review is claimed.

[Editorial assessment](research/checkers-runway13/whitepaper/v5/EDITORIAL_ASSESSMENT.md) · [Figure redesign](research/checkers-runway13/whitepaper/v5/FIGURE_REDESIGN.md) · [600 dpi presentation figures](research/checkers-runway13/whitepaper/v5/presentation/) · [Publication record](research/checkers-runway13/whitepaper/v5/PUBLICATION.md)

The [35-page Version 4](research/checkers-runway13/whitepaper/v4/checkers-with-runway-13-white-paper-v4.pdf), [33-page Version 3](research/checkers-runway13/whitepaper/v3/checkers-with-runway-13-white-paper-v3.pdf) and [30-page Version 2](research/checkers-runway13/whitepaper/v2/checkers-with-runway-13-white-paper-v2.pdf) remain unchanged and available.

## Explore the project

| Follow your curiosity | Where to go |
| --- | --- |
| **What did the airport and Kowloon look like?** | [Historical survey sheets, photographs and building chronology](research/checkers-runway13/reconstruction/chronology/REPORT.md) |
| **Can photographs reveal the old city in 3D?** | [Photogrammetric reconstruction](research/checkers-runway13/reconstruction/block_matching/REPORT.md) and [3D workbench documentation](research/checkers-runway13/reconstruction/block_matching/scene/README.md) |
| **How does a complete mathematical landing work?** | [Flight model](research/checkers-runway13/README.md), [calm-air analytical results](research/checkers-runway13/analytical/coupled/RESULTS.md), and [wind-conditioned landing](research/checkers-runway13/counterfactual/REPORT.md) |
| **What can the historical accident record tell us?** | [CAL605 flight and weather evidence](research/checkers-runway13/evidence/cal605_reconstruction/SPEC.md) |
| **What would a historical aircraft-clearance calculation still need?** | [Historical integration report](research/checkers-runway13/integrated/REPORT.md) and [archival records follow-up](research/checkers-runway13/integrated/records_followup/REPORT.md) |
| **Which questions are resolved, disputed or still open?** | [Project research ledger](research/checkers-runway13/PROJECT_STATE.md) and [literature comparison](research/checkers-runway13/literature/LITERATURE_AND_COMPARISON.md) |

### A city recovered in layers

The project brings together several kinds of evidence, rather than treating one aerial image as a complete 3D city:

| Research material | Documented scope |
| --- | --- |
| Historical survey-sheet archives | **227** acquired editions covering **93** sheet locations |
| Historical full aerial photographs | **48** acquired frames |
| November 1993 stereo-derived surface | **171,307** dense points and a **partial, non-watertight** observed-surface mesh |
| Visually reviewed historical mapped faces | **45** faces across selected 1989, 1994 and 1997 editions |
| Later source-bound integrated evidence | **88** features, including point observations, mapped faces and other evidence types |

The reconstructed stereo surface includes roofs, ground, vegetation and possibly erroneous matches; it is **not** a complete model of every building. Most dense points fall outside the local map-control hull, and their heights use a fitted **relative reference plane**, not Hong Kong Principal Datum. Historical footprints with unknown heights remain unknown. The 2026 building dataset is a **separate modern comparison**, not a substitute for the 1993 skyline.

For the existing reconstruction, begin with the [3D workbench README](research/checkers-runway13/reconstruction/block_matching/scene/README.md). Its full viewer and large geometry depend on the restored data package; a publicly hosted interactive demo is not claimed here.

### From an approach to a complete stop

![Constructed calm-air trajectory and stopping result, an explicit mathematical model rather than an actual historical flight](research/checkers-runway13/whitepaper/v3/figures/09_complete_calm.png)

*Model illustration: the calm-air constructed landing. It does not demonstrate the clearance or flyability of a historical Boeing 747.*

The research supplies **two separate synthetic landing scenarios** under stated simplified dynamics and braking assumptions:

| Model scenario | Touchdown beyond threshold | Full stop from threshold | Runway remaining |
| --- | ---: | ---: | ---: |
| Calm-air reference | 313.49 m | 2,531.32 m | **254.68 m** |
| Steady wind, 070° true / 21 kt | 302.11 m | 2,233.23 m | **552.77 m** |

Both constructed paths have computer-assisted **continuous-time feasibility certificates within their specified mathematical models**. The wind and calm cases are separately optimized scenarios: their difference is **not** an identified causal effect of wind. Neither establishes historical obstacle clearance, near-global optimality, a validated aircraft performance envelope, or operational safety.

[Read the mathematical verification](research/checkers-runway13/whitepaper/v3/VERIFICATION.md) · [Explore seven explanatory insights](research/checkers-runway13/whitepaper/v3/INSIGHTS.md)

## Historical data and archive

**[The Kai Tak Historical Research Archive](archive/README.md)** provides a versioned catalogue of 3,268 artifacts in 44 datasets across nine collections. [Data Release v1.0.0](https://github.com/ayyararyan/kai-tak/releases/tag/archive-v1.0.0) contains **418 source-permitted files in five independently restorable bundles (824.8 MB compressed)**. This is an audited subset, not a claim that every historical source is acquired or reusable.

```sh
git clone https://github.com/ayyararyan/kai-tak.git
cd kai-tak
python3 scripts/fetch_data.py --release v1.0.0
# Or fetch only weather observations:
python3 scripts/fetch_data.py --release v1.0.0 --collection 05
```

[Collections](archive/CATALOGUE.md) · [Download/verification](archive/DOWNLOAD.md) · [Source rights](archive/licensing/README.md) · [Citations](archive/CITATION.md) · [Limitations and audit](archive/PUBLICATION_READINESS.md)

The existing [dated research snapshots](publication/release_assets.json), with 1,254 restored files, remain unchanged and accessible through `python3 scripts/fetch_data.py` without `--release`. Earlier publication is not a new license grant. The new archive's historical data boundary remains research commit `128f7006e8c929a878bd80bdf84521a97c45ee30`; later paper v3/v4 packages are preserved separately in this repository. DOI registration and new original-work license grants have not occurred.

## Reproduce the research

### Rebuild the latest white paper (v5)

The [V5 build guide](research/checkers-runway13/whitepaper/v5/README.md) documents the pinned Python dependencies, XeLaTeX/BibTeX, Poppler and locally licensed fonts. The public package's two documentation-only path normalizations do not affect its build inputs.

~~~bash
cd research/checkers-runway13/whitepaper/v5
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py --figures
.venv/bin/python verify_certificates.py
~~~

[Reproducibility report](research/checkers-runway13/whitepaper/v5/REPRODUCIBILITY.md) · [Scientific checks](research/checkers-runway13/whitepaper/v5/SCIENTIFIC_VERIFICATION.md)

### Rebuild white paper v3

The portable manuscript includes its frozen numerical inputs, plots, source code and proof-checking scripts. It requires Python, Tectonic and Poppler; see the [full build guide](research/checkers-runway13/whitepaper/v3/README.md).

~~~bash
cd research/checkers-runway13/whitepaper/v3
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
.venv/bin/python verify_certificates.py
~~~

The paper's verification record reports **89 passing model/counterfactual tests**, **104 checked frozen inputs**, and a source-only clean rebuild that matched all **33 pages in extracted text and rendered pixels**. These are recorded project checks, **not independent aerospace peer review**.

### Reproduce the wider model and reconstruction

The [core flight-model README](research/checkers-runway13/README.md) covers its dedicated numerical environment and tests. Geospatial processing has [different dependencies](research/checkers-runway13/geospatial/README.md). Some source-bound historical integrations require third-party originals that are intentionally **not redistributed**; their acquisition references and expected checks are recorded, rather than bypassed.

## What remains an open research question?

**The key distinction:** showing that a continuous trajectory satisfies a reduced model's constraints is not the same as showing that a specific historical aircraft could follow it safely over 1993 Kowloon.

The project is still working toward date-specific historical obstacle geometry, reliable runway-end and vertical-datum registration, aircraft/gear/attitude calibration, and defensible treatment of uncertainty and tracking. The later integration work identifies a material runway-reference mismatch and specific archival records worth acquiring; it **does not** claim to have resolved those issues or derived the historical closed-form optimal landing.

[Read the integration findings](research/checkers-runway13/integrated/REPORT.md) · [Review the exact archival leads](research/checkers-runway13/integrated/records_followup/REPORT.md)

This is an **independent research and historical-education project**, not flight guidance, an airworthiness assessment or a validated accident-prevention analysis.

## Author, attribution and use

**Aryan Ayyar** works in financial economics and mathematics. This project grew from a longstanding fascination with the engineering of Kai Tak, and from time spent studying and living in Hong Kong. Its purpose is to make a difficult and beautiful engineering question investigable through explicit models, source material and reproducible results.

The research used **AI-assisted implementation, drafting and checking**; the manuscript does not claim independent human specialist review.

Original research and code are copyright © 2026 Aryan Ayyar. **No blanket open-source license has yet been granted.** Third-party datasets, photographs, maps and publications retain their own rights and use conditions. Hong Kong Government open-data material is attributed to its source institutions under the applicable DATA.GOV.HK/CSDI terms. Restricted report scans and scholarly PDFs are inventoried or linked, not republished where permission has not been established.

[Rights and attribution](NOTICE.md) · [Source-by-source publication scope](DATA_SOURCES.md) · [White-paper figure provenance](research/checkers-runway13/whitepaper/v5/RIGHTS_AND_PROVENANCE.md)

For scholarly reference, cite **Ayyar, A. (2026), _Checkers with Runway 13_, white paper v5**, with the [versioned PDF](research/checkers-runway13/whitepaper/v5/checkers-with-runway-13-white-paper-v5.pdf) and the specific dataset release or source record used. A persistent archive DOI is not claimed.
