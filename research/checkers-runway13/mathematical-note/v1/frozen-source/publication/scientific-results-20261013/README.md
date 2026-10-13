# Scientific-results snapshot — 13 October 2026

This additive publication follows the settled 18:13 UTC scientific audit. It does not replace the historical archive, visual atlas, manuscripts or their frozen evidence. No release assets are changed and no new license is granted.

## Read the results

- [Latest local certificate](../../research/checkers-runway13/integrated/assumption_solution/refinement/local_certificate/REPORT.md) and [derivation](../../research/checkers-runway13/integrated/assumption_solution/refinement/local_certificate/DERIVATION.md).
- [Refinement and condition domains](../../research/checkers-runway13/integrated/assumption_solution/refinement/REPORT.md), including unsuccessful enclosure attempts.
- [Original conditional solution](../../research/checkers-runway13/integrated/assumption_solution/REPORT.md), [assumptions](../../research/checkers-runway13/integrated/assumption_solution/ASSUMPTIONS.md), [condition table](../../research/checkers-runway13/integrated/assumption_solution/conditions.csv), and [aircraft prerequisites](../../research/checkers-runway13/integrated/aircraft_followup/REPORT.md).

The new theorem is a **strict local primary optimum in five flare variables**, connected to a **non-strict local primary optimum in the 12-parameter family**. The exact implicit root is near η = 0.1523607643018617; the global-family bracket **[0.15236076430186170190, 0.181970215] is unmatched**. The rounded root path has touchdown 302.126459 m, stop 2234.377025 m, and 551.622975 m remaining. These are not the unchanged delivered secondary path's coordinates. That secondary path retains the primary objective within 10⁻⁴ of the proved **local** primary optimum; no global secondary proof follows.

Ten condition points are certified, not a full domain map or closed-form global optimizer. Tailwind 5 kt / urban 60 m / urban 65 m remain unresolved, not proved infeasible. A-04 and A-05 remain partial; historical certification remains false. Older sealed reports retain their historical proof status. The exact local root is defined by its certified decimal box, not by rounded display coordinates.

## Publication scope and provenance

[Source/public mapping](source_public_mapping.json) binds **235 files**: all 136 original, 69 refinement and 19 local-certificate entries, their three unchanged manifests, six aircraft-followup authored/derived files, assumption authorization, and a scientific-only ledger append. Seven mapped files differ from their canonical counterparts: six have private absolute-path prefixes normalized; the ledger preserves the previous public edition and appends only settled scientific entries. All source SHA-256 values remain available; no original scientific hash or sealed manifest is rewritten to make normalized bytes appear original.

The [610-path availability table](preserved_path_disposition.json) separates source preservation from public availability: 438 identical Git files, five normalized Git files, and 167 inherited omissions. Those omissions include source scans, cached acquisition bodies, private drafts and old runtime logs/caches. The originals were checked locally; omission is not public reproduction. Original manifest hashes of omitted files are provenance, not disclosure of their contents.

All new authored source code, evaluators, coefficients, trajectories, plots, sensitivity outputs, certificates, proof derivations and selected failed/invalidated scientific cases are included. The pre-exit-repair urban55 candidate and failed domain-enclosure experiments remain labelled; search failure is not infeasibility. The earlier environment/diagnostic error logs are retained as sealed provenance, not reported as current failures.

Excluded: ten third-party aircraft-source images, runtime caches, **all** `integrated/authorized_enquiries_20261013/`, both `*_ENQUIRY_DRAFT.md` files, private account/login/session records, and restricted third-party bodies. The exact scoped exclusions are in the mapping. Source permission is separate from permission to publish research. Raw canonical ledger sections containing private operational details are not copied. Existing release assets and their restoration manifests are untouched.

## Reproduce the public checks

From the repository root, with Python 3.12:

```sh
python3.12 -m venv .venv-scientific
.venv-scientific/bin/python -m pip install -r publication/scientific-results-20261013/requirements.txt
.venv-scientific/bin/python publication/scientific-results-20261013/run_public_tests.py
```

Fresh-environment verification passed **102 numerical/core/proof tests and 15 geometry tests (117 total)**. The root, positive multiplier simplex, stationary/endpoint extrema and complete-path certificate are freshly reproduced by these tests. The runner names its exclusions explicitly; it does not edit scientific tests, fake source files or count deselections as passes.

Five historical-source tests need restricted originals: four in `integrated/followup/test_diagnosis.py` and `test_source_observations_hashes_and_unknown_fixdatum`. They passed separately with seven local source inputs supplied to an isolated private fixture, but are **not** claimed as publicly reproducible from Git alone. Acquisition references remain in the existing source inventory. Two original-workspace tests (`test_parent_snapshot_unchanged`, `test_preserved_packages`) require unnormalized bytes and the entire original workspace, including intentionally excluded material. Their publication counterpart is:

```sh
python3 publication/scientific-results-20261013/verify_public_snapshot.py
```

This checks every mapped public hash, all 224 source-manifest bindings, three unchanged seals, and explicit disposition of all 610 preservation paths. It is an integrity check, not a substitute mathematical theorem. The original strict verifiers remain unmodified and will correctly refuse incomplete/normalized public trees. The parent's earlier **124 tests** refer to the original-source audit; they are not relabelled as 124 public-copy passes.

A separate fresh public-copy calculation reproduced the baseline secondary retention certificate over **4,020 processed time cells** and the numerical-root-center independent replay; see [publication verification](verification.json). No new search, model change or certificate regeneration was performed. Existing sealed proof outputs remain unchanged.

The two shipped evaluators can be called from `research/checkers-runway13` using your environment's Python:

```sh
python integrated/assumption_solution/evaluate.py mean 20
python integrated/assumption_solution/refinement/export_refinement.py --case urban58 --time 45 --side right
```

These evaluate named accepted paths; they do not extrapolate unsupported conditions or return a globally optimal flight procedure. Do not run producer scripts against sealed packages without first making a separate copy: they can invalidate recorded manifests. No historical-clearance, flight-guidance or overall scientific-completion claim accompanies publication.
