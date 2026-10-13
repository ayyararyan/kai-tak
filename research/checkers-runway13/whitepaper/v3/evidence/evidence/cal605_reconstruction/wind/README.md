# CAL605 wind printout reconstruction

**Status: visually transcribed and computationally verified, 13 October 2026.** This is a descriptive historical wind-evidence component, not a reconstruction of wind at the aircraft, a calibrated physical uncertainty model, or a source of independent repeated observations.

## What the printed records show

The actual printouts on CAD Report 1/95 PDF pages 138–139 (printed A7-2/A7-3) contain **15 timestamps, five sensors, and three direction/speed fields: 225 pairs / 450 numbers**. All were visually readable and retained. The explanatory sample on page 137 is not counted as an additional observation. No missing timestamps are interpolated.

The striking feature is the joint importance of **where** wind is observed and **which averaging window** is used:

- At wind-clock **03:35:30, NW A = 37 kt**, versus **B = 23 kt** and **C = 19 kt**. A exceeds the ten-minute mean by **18 kt**. A is the maximum one-second speed in a five-second window, not a contemporaneous mean or instantaneous point sample.
- At wind-clock **03:38:00**, present-field speed is **12 kt at NW** and **37 kt at Lei Yue Mun**, a **25 kt** difference. These are distinct sites; this is not measured aircraft windshear.
- The largest printed across-sensor range is **25 kt for A**, **21 kt for B**, and **16 kt for C**. The latter two fields are overlapping rolling averages, not independent observations.
- The printed preceding-ten-minute one-second extrema (E) reach **44 kt at NW**; the highest extracted A record at NW is only **37 kt**. The sparse A printouts therefore miss a higher maximum already recorded by the instrument summary. This does not locate that maximum within the flight timeline.

| Sensor | Range of A − B across printed records (kt) | Range of A − C (kt) |
|---|---:|---:|
| SE | −3 to 11 | −2 to 13 |
| NW | −5 to 14 | −8 to 18 |
| MID | −5 to 6 | −4 to 7 |
| LYM | −2 to 8 | −3 to 8 |
| YYC | −7 to 14 | −7 to 15 |

These are exact arithmetic differences of printed integers, not bounds on true wind, confidence intervals, or representative frequencies. Sparse, event-dependent printouts cannot support unbiased time averages. Report page 137 says significant windshear activates thirty-second printouts; otherwise they update every ten minutes. Preserve the actual 30/60/120-second gaps without explaining missing records as zero wind or absence of shear.

## Source anomalies deliberately not repaired

1. **LYM at 03:35:30 reads `A360/32`** on page 138. This is visually confirmed in `source_pages/wind-138-anomalies-detail.png`. Preserve 360 degrees as printed, including circular differences; do not change it to 060 to make the series smoother. Whether this is a source/system error is unknown.
2. **NW at 03:38:00 reads `C060/17`** on actual page 138, whereas the illustrative page-137 example at the same timestamp reads `C060/19`. The actual page-138 value is retained and flagged. The key 25 kt cross-sensor A difference is unaffected by that C discrepancy.

## Semantics and uncertainty

- **A:** maximum one-second wind speed and associated direction in a five-second period.
- **B/C:** preceding two-/ten-minute arithmetic mean speed. Direction uses the source's Attachment II algorithm; this extraction does not attempt to reconstruct it from the unavailable raw samples.
- **E:** minimum/maximum one-second speed in the preceding ten minutes. Extracted for SE and NW only. Maxima across overlapping windows are not separate gust events.
- Units: speed in knots; directions in printed degrees. No true/magnetic or runway-component transformation is asserted here.
- Time: printout labels UTC, but wind-system offset to ATC/DFDR remains unestablished here. Time fields explicitly use `wind_clock_time`, not joined flight time.
- Display increments: integer knots and ten-degree directions. Rounding rule and instrument accuracy are not established by these pages. Thus even a ±0.5 kt / ±5° rounding interpretation would be an assumption, not a verified physical bound.
- Null semantics: `?` in manual anchors becomes JSON/CSV null/empty; no ambiguous A/B/C cells were needed after visual inspection. Source-level anomalies remain readable values with notes.
- Surface sites do not identify wind on the complete flight path; vertical wind is not measured in these records. No probability, CI, accident causality, or optimal landing claim follows.

## Files and reproduction

- `manual_readings.txt`: manually checked A/B/C source anchors for every printed sensor/time.
- `manual_extrema.txt`: optional E extrema anchors for SE/NW.
- `wind_records.csv`: long table, one row per direction/speed pair, with page/block/row/column provenance.
- `wind_extraction.json`: source hashes, semantics, uncertainties, normalized manual lines and original machine-text aids.
- `within_sensor_differences.csv`, `across_sensor_variability.csv`, `summary.json`: reproducible descriptive calculations.
- `wind_extrema.csv`: rolling extrema without invented peak times.
- `wind_windows.png` / `.pdf`: standalone figure using dots only; no interpolation across gaps.
- `source_pages/`: PDF renderings actually inspected, including enlarged anomaly detail.
- `test_wind.py`: eleven source-semantic, arithmetic, null-propagation, plotting and failure-preservation checks.
- `manifest.json`: SHA256 identities; `verify_manifest.py` verifies them.

From workspace root:

```sh
python3 research/checkers-runway13/evidence/cal605_reconstruction/wind/reconstruct_wind.py
research/checkers-runway13/.venv/bin/python -m unittest discover -s research/checkers-runway13/evidence/cal605_reconstruction/wind -p test_wind.py -v
research/checkers-runway13/.venv/bin/python research/checkers-runway13/evidence/cal605_reconstruction/wind/plot_wind.py
python3 research/checkers-runway13/evidence/cal605_reconstruction/wind/verify_manifest.py
```

Numeric CSV/JSON reconstruction is deterministic and network-free. Figure PDF metadata can change on regeneration; this does not alter source or numerical identity. A manifest mismatch after deliberate regeneration must be inspected, not silently accepted.

**Coverage:** All requested A/B/C cells and sensor/time combinations complete. E extrema additionally retained. D, F, G and printed shear flags remain outside this transcription's optional extrema coverage and are explicitly listed in metadata. No parent model, terrain artifact or ledger modified.

## Independent-review repair: missing anchors

The initial code accepted `?` at parsing but crashed in downstream differences, extrema or plotting. Because some outputs had already been written, it could leave inconsistent new/stale files. No actual transcribed source value was affected (the real 450 cells are readable).

Repaired: numeric nulls propagate independently by variable; a missing direction does not discard a known speed, and vice versa. Within-sensor summaries use valid pairs and report their counts. Full-five-sensor ranges are null unless all five relevant readings exist; minima/maxima among available readings retain explicit valid-sensor counts. All-missing summaries return null, never zero. Plotting omits missing speeds and reports their number. E extrema also accept nulls.

All calculations and serialization now finish before staged output files replace existing files. A malformed-anchor regression confirms prior outputs are unchanged on a derivation failure. This is not a claimed atomic multi-file directory transaction against an I/O interruption during final replacement. Tests cover missing speed, missing direction, a sparse all-missing record, plotting each case, and failure preservation. Actual 225 pairs and their numerical values are unchanged.
