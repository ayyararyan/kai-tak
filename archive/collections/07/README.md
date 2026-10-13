# 07 — Mathematical Models and Results

Ayyar, Aryan (2026). Mathematical Models and Results. The Kai Tak Historical Research Archive, candidate v1.0.0, collection 07. **Unpublished candidate; no DOI assigned.**

433 catalogued artifacts; 0 verified-permitted files selected for the new data bundle. Other entries remain available as source references, existing Git research or explicitly restricted dependencies.

[Master catalogue](../../CATALOGUE.md) · [Rights](../../licensing/README.md) · [Collection manifest](../../releases/v1.0.0/collections/07.json)

## Declared synthetic landing model and scenario outputs

**ID:** `kt-synthetic-model`. Point-mass approach/flare/rollout with replay diagnostics

- Quantity: {"recorded_model_tests": 52, "recorded_artifact_checks": 29}; 20 catalogued files.
- Epoch: Synthetic model generated 2026-10-13, not historical observations.
- Processing: scenario/generated.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Synthetic entry/corridor and uncalibrated aircraft/braking; Historical mode must fail closed; Search failure not infeasibility proof
- Source links: [source 1](https://github.com/ayyararyan/kai-tak), [source 2](https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Restricted mathematical derivations and checks

**ID:** `kt-restricted-analytical-results`. Straight-circle-straight, finite-roll and necessary bounds

- Quantity: {}; 24 catalogued files.
- Epoch: No observational epoch.
- Processing: mathematical derivation / numerical checking.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Theorems apply only to explicit restricted domains; No unrestricted full landing optimum
- Source links: [source 1](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Calm-air continuous-family feasibility certificate

**ID:** `kt-calm-air-certificate`. Computer-assisted fixed-witness interval certificate and incomplete global search

- Quantity: {"margin_lower": 0.0397, "global_upper": 0.1559772, "accepted_closed_intervals": 2502}; 26 catalogued files.
- Epoch: Synthetic calm-air scenario.
- Processing: verified model certificate / unresolved optimization.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Not global optimum; Invalidated global bounds .10/.05/.04/.03972 must not be used; IEEE/numerical physical accuracy not implied by real-decimal certificate
- Source links: [source 1](https://github.com/ayyararyan/kai-tak)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Wind-conditioned full landing reference

**ID:** `kt-wind-counterfactual`. Fixed steady 070 true/21kt scenario plus interval certificate

- Quantity: {"touchdown_m": 302.114052038277, "stop_m": 2233.231, "reserve_m": 552.769, "certified_margin_lower": 0.1507934696816132, "global_necessary_upper": 0.21674437819006, "interval_boxes": 376, "recorded_tests": 37}; 11 catalogued files.
- Epoch: Historical mean wind used as declared steady scenario, not recovered gust history.
- Processing: scenario / model-feasibility certificate.
- Verification: recorded scoped verification; not freshly rerun in this audit.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: No causal accident-prevention or historical-clearance claim; Uniform wind not aircraft gust history; Loose optimality gap not near-optimality; Symlink-backed bundle paths require safe explicit dereference in release preparation
- Source links: [source 1](https://github.com/ayyararyan/kai-tak), [source 2](https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf), [source 3](https://www.ncei.noaa.gov/pub/data/noaa/1993/450070-99999-1993.gz)
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.

## Mathematical Models and Results — supporting and unclassified artifacts

**ID:** `kt-support-07`. Ancillary reports, scripts and outputs; consult file-level provenance gaps.

- Quantity: {}; 359 catalogued files.
- Epoch: not established.
- Processing: mixed/unclassified.
- Verification: Not independently verified.
- CRS / vertical datum: not applicable or unresolved / not applicable or unresolved.
- Limitations: Directory classification is navigational, not a verified source or transformation chain.
- Source links: Not established; see unresolved source record.
- Reuse: source-specific; consult artifact decisions. New candidate includes 0 matched permitted files.
