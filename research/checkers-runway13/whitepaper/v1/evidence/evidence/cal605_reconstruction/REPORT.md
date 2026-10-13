# CAL605: what the reconstructed evidence changes

13 October 2026. **A reproducible, exploratory flight/weather benchmark is built.** It covers selected final-turn and rollout traces, the complete five-sensor A/B/C wind printout, the 1993 weather archive, and conditional stopping diagnostics. It is not a recovered raw DFDR tape, a georeferenced full 3D trajectory, a historical optimal landing, or a calibrated prediction interval.

The strongest result is a distinction: **speed can be falling while the braking needed to stop on the remaining runway is rising.** The stopping-aid state and time to effective deceleration matter alongside touchdown location and speed. Meanwhile, a single airport mean wind misses material differences both across sensors and across averaging windows.

## 1. The earlier 255 m runway margin does not survive historical touchdown inputs

Hold the existing model's usable runway (2786 m), two-second delay and 0.15g constant deceleration fixed. Evaluate its equation at different touchdown inputs:

| Conditional calculation | Touchdown beyond threshold | Ground speed | Runway remaining at calculated stop |
|---|---:|---:|---:|
| Existing synthetic reference | 313 m | 151.4 kt | **255 m** |
| Change touchdown position only | 480 m | 151.4 kt | **88 m** |
| Change speed only | 313 m | 160 kt | **5 m** |
| Both report-stated touchdown inputs | 480 m | 160 kt | **−162 m** |

The report-stated inputs are rounded historical evidence, not precise calibrated measurements. The 150 m reserve is the research model's requirement, not an inferred historic operating rule. A negative result means the formula's stop lies beyond the runway; it is **not** an actual reconstruction of the final turn into the water.

The decomposition is exact within this formula: the later touchdown uses another **167 m**, and the extra speed uses another **250 m**, of which the braking term dominates. This is a sensitivity calculation under common braking assumptions, not evidence that the synthetic approach could actually have been flown in CAL605's weather.

![Conditional runway and speed-distance findings](findings.png)

[PDF figure](findings.pdf) · [machine-readable calculations](analysis.json) · [scenario table](conditional_stopping_cases.csv).

## 2. Decelerating did not mean regaining a comfortable stopping margin

For remaining runway \(R\), current ground speed \(v\), assumed response delay \(\tau\) and subsequent constant deceleration \(a>0\), the simplified stopping condition is

\[
R\ge v\tau+\frac{v^2}{2a}.
\]

It is equivalent, when \(R>v\tau\), to

\[
a_{\rm required}=\frac{v^2}{2(R-v\tau)}.
\]

Using report narrative landmarks, **without any additional delay**, gives:

| Report landmark | Runway remaining | Ground speed | Required constant deceleration to stop at end |
|---|---:|---:|---:|
| Touchdown | ~2300 m | 160 kt | ~0.150g |
| Roll excursions ended | ~1365 m | 139 kt | ~0.191g |
| Autobrake warning call | ~1080 m | 133 kt | ~0.221g |
| Reverse selected | ~880 m | 129 kt | ~0.255g |

At the last state, introducing a two-second delay raises the conditional requirement to approximately **0.300g**. Equivalently, assuming a sustained 0.3g gives only about **two seconds of delay allowance** in this idealized equation. These rounded observations cannot identify an exact physical deadline; 0.3g is an illustrative sustained braking scenario, not an established maximum capability.

Appendix 13's approximate +20 s checkpoint lists 800 m remaining and 127 kt. Relative to the narrative's ~2300 m touchdown remaining distance, about **65% of the runway had been used while 63% of touchdown kinetic energy remained** (constant mass). The narrative places strong braking at about 750 m rather than exactly 800 m. Both source statements are retained; no forced reconciliation is used.

The report already explains the sequence: forward-thrust advancement after touchdown disarmed autobrakes and retracted spoilers; strong deceleration followed much later. Our contribution here is a reproducible numerical description and connection to the explicit stopping equation, not a new discovery of the accident's cause. A constant-deceleration fit alone would suppress these discrete system states.

Sources: CAD Report 1/95 §§1.11.4, 2.2.5–2.2.7; physical PDF pages 39–40, 63–65 and Appendix 13/page 159. [Source-stated event table](flight_events.csv), [digitized Figure 5](source_pages/rollout_overlay.png), [35 speed-distance anchors](rollout_trace.csv).

## 3. The final turn had changing speed, wind readings and drift

Selected Figures 1–2 readings show ground speed rising roughly **127 to 163 kt** between report-datum A≈110 and 145 s, while heading changes roughly **91°M to 133°M**. FMC wind-speed readings fall from about **48 kt at A≈110 s to 14 kt at A≈130 s**; the sampled drift excursion reaches about **13° around A≈135 s**.

These are coarse readings with substantial declared raster sensitivities, roughly ±6–7 kt for these speed samples and ±2° for drift. Unsampled peaks are not bounded. The observations do not identify a wind-only cause for the ground-speed change: the aircraft is turning, its controls are changing and the wind vector's projection changes. CAS is not TAS, and CAS minus ground speed is not a recovered wind vector. Magnetic heading and true FMC wind direction are not subtracted without a common bearing frame.

![Approach samples](flight/approach_wind_samples.png)

The final-phase extraction also reveals an important measurement issue: the plotted radio-height trace crosses zero before the first ground flag and sits near −8 ft on the ground. It must not be interpreted as negative aircraft clearance or converted directly into historical terrain elevation.

The first ground flag reads B≈31.0 s. Integrating the coarse speed polyline to the last preterminal speed anchor yields about 2.08 km; a deliberately conservative declared pixel/anchor sensitivity calculation gives 1.86–2.31 km. The final anchor is **not explicitly identified as runway exit**, and these are not physical error bounds. We do not tune the curve to force the narrative's ~2300 m distance.

[Flight methods and limitations](flight/README.md), [final-phase figure](flight/final_approach_rollout.png), [original Figure 4 anchors](flight/trace_anchors.json), [Figure 1–2 anchors](flight/approach_anchors.json).

## 4. “The airport wind” is not one number

All actual printed A/B/C fields were transcribed: **15 irregular timestamps × five sensors × three fields = 225 direction–speed pairs**. Thirty printed rolling-extrema pairs were additionally retained.

- **Same sensor, different time window:** at wind-system 03:35:30, NW's present-field speed is **37 kt**, its two-minute mean **23 kt**, and its ten-minute mean **19 kt**. The 18 kt difference is exact arithmetic of printed numbers, not a calibrated error bound on true wind.
- **Same timestamp, different locations:** at 03:38:00, NW records **12 kt** while Lei Yue Mun records **37 kt**, a **25 kt** difference. This is spatial variation across ground sensors, not measured shear encountered by the aircraft.
- **Sparse samples miss peaks:** NW's preceding-ten-minute maximum reaches **44 kt**, but the largest retained NW present-field reading is only **37 kt**. We know the sparse printout does not contain all instrument-recorded maxima; we cannot locate the missing peak on the flight timeline.

“A” means the maximum one-second speed in a five-second window, not an instantaneous mean. “B/C” are overlapping two-/ten-minute averages. The printer was event-triggered, so the rows are neither uniformly spaced nor independent observations. No interpolation fills the gaps.

![Wind-window comparison](wind/wind_windows.png)

The NOAA 03:00 and 04:00 UTC observations both give 070°/about21 kt, consistent with the report's weather table. Their gust fields give about34 and40 kt. Shared originating observations are possible, so this is a cross-format consistency check, not independent replication. In the declared comparable routine-report subset, 8285/8360 observations (**99.10%**) have lower mean wind speed. This is retrospective selected-record context, not a population percentile with a CI, a forecast or accident probability. Gusts are missing from most records, so no unconditional gust distribution is estimated.

[Wind extraction and source anomalies](wind/README.md) · [NOAA decoder/QC](noaa/README.md).

## 5. What is explicit, and what remains unidentified

The reconstructed ground speed is linear in runway coordinate between each of the 35 Figure 5 anchors. Within segment i, let \(v_i>0\) be its initial speed, \(x_i\) its coordinate and \(m_i=(v_{i+1}-v_i)/(x_{i+1}-x_i)\). Under runway-parallel motion,

\[
v(t)=v_i e^{m_i(t-t_i)},\qquad
x(t)=x_i+\frac{v_i}{m_i}\left(e^{m_i(t-t_i)}-1\right).
\]

For \(m_i=0\), use \(x=x_i+v_i(t-t_i)\). Segment duration is \(\log(v_{i+1}/v_i)/m_i\). All **34 numerical segments** are in [explicit_rollout.json](explicit_rollout.json). This is an explicit reconstruction under stated interpolation, **not** an optimal landing formula. Its time origin is the first retained anchor before touchdown, not report datum A, B or UTC. It ends at the last source anchor, not at a modeled stop. The final yaw means its runway-parallel assumption is not a complete physical replay.

| Object | Status / meaning |
|---|---|
| Source-stated flight events | Transcribed; rounded source values and discrepancies retained. |
| Selected flight traces | Digitized: 190 approach/final-phase anchors plus 35 speed-distance anchors. |
| Explicit rollout interpolation | Derived conditional on the polyline and runway-parallel motion; no extrapolation. |
| Ground weather printout | Complete A/B/C transcription for five sensors and all printed timestamps. |
| NOAA archive | All8549 records decoded with raw fields and quality flags;24 on event date. |
| Pixel-reading ranges | Declared deterministic sensitivity boxes; no statistical coverage. |
| Actual physical tracking/model-error distribution | Not identified from these sources. |
| Exact flight/wind clock offset | Unknown; no synchronized join or lag correlation performed. |
| Complete georeferenced 3D flight path | Not delivered; terrain registration and raw-state evidence still needed. |
| Population95% landing prediction interval | Not available from a single accident. |
| Historical feasibility/near-optimality | Not established by this reconstruction. |

The ground-weather system uses a separate internal clock; its synchronization/offset to ATC could not be established in the primary report. The report gives the aircraft warning at about03:35:15 on the ATC clock and about32 seconds before touchdown, implying an approximate touchdown anchor near03:35:47 on that clock. Its timing accuracy is not quantified. This does not identify the ground-weather clock offset. Report-datum A/B are retained separately here; the approximate anchor is recorded in [the clock ledger](clock_alignment.json), not used to force synchronized samples. No guessed clock offset is used to claim that a particular ground gust caused a flight excursion.

Source inconsistencies are data, not inconveniences: touchdown is about2300 m remaining in the narrative,2250 m in Appendix13, and about2210 m at Figure5's plotted ground-flag transition. These may refer to different timing/position conventions or rounded reconstruction; this benchmark cannot resolve them. The LYM direction printed as360° and the actual-versus-illustrative NW mean discrepancy are also preserved.

## Verification and reproduction

[Verification record](verification.json) records final test results, artifact counts, source identities and review dispositions. Source images with anchor overlays were visually inspected. Tests check units, axis transformations and sensitivity enclosures, missingness, parser source identity, published-value consistency, analytical reconstruction against independent quadrature, and frozen-model identity. They do not validate raw aircraft or meteorological measurement accuracy.

From the workspace root:

```sh
research/checkers-runway13/.venv/bin/python research/checkers-runway13/evidence/cal605_reconstruction/reconstruct.py
research/checkers-runway13/.venv/bin/python research/checkers-runway13/evidence/cal605_reconstruction/flight/build_flight.py
research/checkers-runway13/.venv/bin/python research/checkers-runway13/evidence/cal605_reconstruction/flight/build_approach.py
python3 research/checkers-runway13/evidence/cal605_reconstruction/noaa/decode_noaa.py
python3 research/checkers-runway13/evidence/cal605_reconstruction/wind/reconstruct_wind.py
```

No source aircraft configuration, nominal optimizer, braking assumption or terrain-owner artifact was changed. No publication, purchase, outreach or operational aviation action occurred.

**Implication for the next model discussion:** a useful condition-to-landing rule must make stopping-aid state/activation history and the available disturbance information explicit. More geometric precision alone will not fix a two-second/constant-braking assumption applied to this event. That is a supported model-design lesson, not permission to silently change the frozen model. Routine landings and go-arounds are still needed for generalization.
