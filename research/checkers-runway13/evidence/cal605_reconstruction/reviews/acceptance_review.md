# CAL605 reconstruction acceptance audit

**Reviewed:** 2026-10-13 13:33 UTC. Independent acceptance-auditor lane.

**Verdict: no blocking findings in the reviewed selected reconstruction and exploratory-comparison scope.** This verdict does not certify a full historical trajectory, aircraft-local wind reconstruction, physical uncertainty coverage, optimal landing, or operational aviation model.

## Authority and scope

Read the entire workspace `WORKING_AGREEMENT.md`, the frozen scope in `SPEC.md`, `REPORT.md`, component methods, current extraction/diagnostic code and tests. The snapshot was treated as review context, not as authority over repaired current code. No source, model, extraction, or report file was edited by this lane. The parent is separately finalizing the unified verification manifest; its in-progress state is not counted as a completed defect here.

The approved object is matched evidence for **selected** published flight traces, ground-weather records and conditional diagnostics, followed by exploratory findings. It is not full optimal-landing implementation. The report preserves that boundary.

## Evidence checked

- **SRC-01:** Reconstruction source manifest passed the existing hash test. Independently recomputed the PDF/raster hashes in the flight metadata and approach raster hashes; all matched the retained inputs. The frozen comparator configuration and trajectory identities passed the manifest check.
- **FLT-01:** Visually inspected Figure 1, Figure 2, Figure 4 and Figure 5 anchor overlays. Selected speed, heading, altitude, wind and drift readings are consistent with the shown traces at their declared coarse precision. Inspected the first air/ground transition, radio-height offset, and sampled final-turn wind/drift change. Metadata preserves 123 final-phase anchors, 67 approach anchors, and 35 speed–distance anchors; interpolated rows are explicitly not additional observations. This inspection is not a guarantee that every between-anchor excursion has been captured.
- **WX-01:** Inspected the primary page-138 printout against the consequential 03:35:30 NW 37/23/19 kt readings, 03:38:00 NW 12 versus LYM 37 kt, NW 44 kt rolling maximum, and retained LYM 360-degree anomaly. The report correctly distinguishes A maxima from rolling B/C means and ground-sensor variation from aircraft-experienced shear. Component tests check complete 225-pair coverage and sparse/missing cases.
- **WX-02:** Current NOAA source-pinning/metadata and missing-field tests pass. The reported routine-subset statistic is explicitly selected-record retrospective context, not a landing population percentile or accident probability. Gust missingness, report quality and possible shared originating observations remain visible. This lane did not independently validate historical sensor siting.
- **COMP-01:** The stopping formula gives 254.679, 88.171, 4.986 and -161.522 m remaining for the four cases. The report's rounded 255/88/5/-162 m values and 167/250 m decomposition are supported. CAD narrative checks support 1365 m/139 kt, 1080 m/133 kt, 880 m/129 kt and strong braking near 750 m. Appendix 13's image supports the separate +20 s, 800 m, 127 kt checkpoint. The resulting 65% distance-used and 63% constant-mass energy-remaining summaries are correctly conditional and rounded.
- **OUT-01:** The report's historical-versus-synthetic comparison is explicitly unmatched in controls/environment. It does not infer wind-only causality, use CAS minus ground speed as wind, promote radio height to AMSL, or claim calibrated physical/prediction intervals. Narrative/chart discrepancies are retained rather than tuned away.
- **VAL-01:** Fresh tests and additional independent numerical checks below support the reviewed calculations. Completion of the parent's final manifest remains a separate handoff step, not an aircraft/model validation claim.

## Fresh verification

Ran with the project's Python environment and `-B`:

| Suite | Observed result |
|---|---:|
| `test_reconstruction.py` | 10 passed |
| `flight/test_flight.py` | 6 passed |
| `noaa/test_decode_noaa.py` | 12 passed |
| `wind/test_wind.py` | 11 passed |

These **39 passing tests** include meaningful independent quadrature, uncertain-axis perturbations, interpolated-envelope perturbations, missingness/null preservation, source-substitution rejection before output mutation, and source discrepancy preservation. Count/schema assertions alone are not the acceptance basis.

Additional read-only calculations verified continuity of coordinates, speed and elapsed time across all **34 explicit rollout segments**, and that each nominal duration falls within its declared coordinate/speed-box bounds. The analytical inversion is correct for positive piecewise-linear speed in runway coordinate; the first-anchor time origin, retained-span endpoint, and runway-parallel assumption are stated rather than presented as observed timing/late-turn dynamics.

Independently sampled **10,000** full anchor-time/value perturbations for the Figure 4 touchdown-flag-to-final-anchor distance integral. All sampled values were inside the declared 1856.31–2309.78 m range; sampled extrema were 1998.72–2166.27 m. This is an additional numerical diagnostic, not a proof of physical coverage or a replacement for the explicit scope restrictions. The nominal 2083.04 m calculation matches the report. The interpolation-envelope suite separately exercises 2,000 realizations over the four variables.

No complete regeneration was run by this read-only review lane. Current retained outputs, source identities, numerical consistency and tests were checked. End-to-end regeneration evidence belongs in the parent's final verification record.

## Nonblocking wording correction

`REPORT.md` currently describes the ground-weather clock as **“explicitly unsynchronized with ATC.”** The primary report's text says the wind system used its own internal clock and it was not possible to determine whether a significant time difference existed (local primary text lines 1123–1126). Unknown synchronization is not proof of a nonzero offset. Prefer: **“The wind system used a separate internal clock; its synchronization and offset to ATC are not established.”**

The surrounding report correctly says the offset is unknown and performs no synchronized join, so this wording does not invalidate the numerical results or require a model change.

## Acceptance boundary

Correctness of the checked extraction/diagnostics is supported by the evidence above. The selected benchmark's specification coverage is supported, subject to the parent's final verification-manifest handoff. Historical 3D completeness, physical error calibration, exact cross-clock registration, routine-flight generalization and historical optimality remain explicitly unestablished. Passing this review must not be described as validation of those wider objects.
