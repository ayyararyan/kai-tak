# CAL605 published flight-trace reconstruction

**Implemented and locally verified, 13 October 2026.** This is numerical digitization of published charts, not raw DFDR data and not a physical landing prediction.

## What is included

- **123 manual pixel anchors** from CAD Report 1/95 Appendix 11 Figure 4 (PDF page 154 / printed A11-5): final-approach/rollout groundspeed, calibrated airspeed, magnetic heading and radio altitude.
- **67 manual pixel anchors** from Figures 1–2 (PDF pages 151–152 / printed A11-2–3): coarse final-turn segment around seconds 80–145 from arbitrary datum A, including groundspeed, CAS, heading, barometric altitude, radio altitude, FMC wind speed/direction and drift. The narrow drift peak at about A=135 s is explicitly sampled.
- Separate narrative event table, source-image overlays, charts, piecewise-linear final-phase representation, sensitivity envelopes and basic numerical verification.
- No edits to the frozen landing model or active terrain work.

## Reproduce

From workspace root:

```sh
research/checkers-runway13/.venv/bin/python research/checkers-runway13/evidence/cal605_reconstruction/flight/build_flight.py
research/checkers-runway13/.venv/bin/python research/checkers-runway13/evidence/cal605_reconstruction/flight/build_approach.py
research/checkers-runway13/.venv/bin/python -m unittest discover -s research/checkers-runway13/evidence/cal605_reconstruction/flight -p 'test_flight.py' -v
```

No network access is required. Scripts preserve the actual manually read raster coordinates and calibration values, and regenerate JSON/CSV/PNG outputs. Source-PDF and source-raster checksums are in `trace_anchors.json`; the Figure 1–2 raster checksums are in `approach_anchors.json`.

## Artifact semantics

| File | Meaning |
|---|---|
| `flight_anchor_readings.csv` | 123 observed-chart pixel readings transformed through calibrated axes; no pseudo-samples. |
| `flight_traces.csv` | 273 one-second **interpolated** variable rows representing the coarse anchor polyline. They are not additional observations. |
| `trace_anchors.json` | Original Figure 4 pixels, calibration, declared pixel sensitivities, source identity. |
| `approach_anchor_readings.csv`, `approach_anchors.json` | 67 Figure 1–2 anchors; only the selected final-turn segment, with no interpolation or claim to full gust extrema. |
| `flight_events.csv` | First air/ground transition from graph plus separately report-stated events; dates/clocks not fabricated. |
| `source_anchor_overlay.png`, `figure1_anchor_overlay.png`, `figure2_anchor_overlay.png` | Manual anchors drawn on source images; visually inspected after generation. |
| `final_approach_rollout.png`, `approach_wind_samples.png` | Standalone explanatory charts with uncertainty interpretation visibly stated. |
| `flight_summary.json` | Conditional temporal integral and its restricted sensitivity interpretation. |

All time axes remain as printed: **A and B are distinct arbitrary report datums**, and neither has been assigned a UTC clock. Figures 1 and 2 share printed datum A. No exact A-to-B offset is asserted. The report says DFDR and CVR were synchronized using matching events; that does not identify synchronization to ground weather-system clock.

## Uncertainty construction

Final-phase horizontal anchor readings use ±3 pixels; both time-axis calibration endpoints also vary ±3 pixels. This gives roughly ±0.42 seconds from datum B. Vertical reading allowances are ±8 pixels for GS/CAS, ±4 for heading and ±5 for radio height; vertical-axis calibration endpoints vary ±3 pixels. Final bounds evaluate all endpoint corners of the affine mapping. The approach chart has ±4-pixel horizontal reading/calibration ranges; its vertical allowances are documented variable by variable and intentionally larger near overlapping traces. These are **declared reading sensitivities**, not empirically estimated standard errors.

For each interpolated timestamp, candidate piecewise-linear segments are evaluated over independent anchor time/value boxes. Shared calibration correlations are relaxed, so this encloses the declared independent boxes. Six tests check axis transforms, a randomized affine enclosure, 2,000 random independent anchor-polyline realizations across four variables, semantics, counts and non-claims. This does not prove unobserved curve excursions lie inside the polyline envelope.

**Not covered:** source-plot transcription/calibration error, raw DFDR sensor errors, exact historical physical position, clock synchronization error, unresolved between-anchor gust peaks, or joint 95% physical uncertainty. Bounds are not confidence intervals or prediction intervals. Integrating groundspeed is derived path length, not independent ground-position truth.

## Findings and checks worth retaining

1. **Distinct rollout regimes are visible.** Groundspeed declines relatively slowly immediately after first ground indication, then much faster later. Narrative section 1.11.4 (printed pp. 32–33) separately states reverse call at +17 s, selection click half a second later and aggressive deceleration at +20 s. Constant effective braking throughout the ground roll does not represent this control history.
2. **The final turn is not a constant-wind, constant-groundspeed segment.** In coarse Figure 1 samples, GS rises from roughly 127 kt around A=110 s to 163 kt around A=145 s; heading changes from roughly 91°M to 133°M. Figure 2 samples show FMC wind speed falling from roughly 48 kt around A=110 s to about 14 kt around A=130 s, and a drift excursion around 13° at A=135 s. Reading ranges are substantial (about ±6–7 kt for these speed samples and ±2° for drift); unsampled extrema are not bounded. These are descriptive associations, not identification of a wind-only causal acceleration. CAS is not true airspeed, heading is magnetic while FMC direction is true, and their scalar difference is not a wind vector.
3. **Radio-height zero does not mark the report's touchdown event.** The Figure 4 radio-height curve crosses plotted zero before the first air-to-ground flag, and remains near −8 ft on the ground. This is a published trace convention/measurement issue left unresolved, not a claim that the aircraft travelled below the runway. Use the air/ground transition for graph-relative touchdown; do not use radio altitude as AMSL or historical clearance.
4. **Retain source/reference-event differences.** First ground indication reads B≈31.00 s, sensitivity [30.59, 31.42] s. GS at that pixel reads about155 kt with vertical sensitivity roughly ±5.4 kt, versus the narrative's stated160 kt. The narrative's figure is not an independent validation measurement. The last preterminal anchor is B≈69.93 s with GS≈28 kt, but Figure 4 alone does not label that anchor as runway end or water impact.
5. Integrating the coarse GS polyline from first ground indication to that final preterminal anchor gives **about2.08 km**, with deliberately broad declared digitization/endpoint sensitivity about **1.86–2.31 km**. This is not a reconstructed runway touchdown-to-exit distance with physical coverage. Compare it with the independently extracted Figure 5/narrative only after preserving different endpoints and chart conventions; do not force agreement.

## Remaining scope

The selected final approach/rollout variables are extracted and reproducible. Complete three-minute DFDR recovery, a georeferenced 3D flight track, raw measurement-error calibration, exact weather-clock linkage and historical landing confidence/prediction intervals remain unavailable. No accident probability, optimality gap, historical clearance certificate or exact operational procedure is produced here.
