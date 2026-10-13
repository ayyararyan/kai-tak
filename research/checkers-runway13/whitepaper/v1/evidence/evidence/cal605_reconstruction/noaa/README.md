# CAL605 NOAA weather decode and exploratory context

Verified 13 October 2026. **This lane is implemented, tested and run against the retained source.** It produces a reproducible weather table, not a reconstructed aircraft-local wind field, an independently verified station history, or a calibrated prediction interval.

## Main findings

The retained NOAA routine reports at **03:00 and 04:00 UTC on 4 November 1993 both contain wind from 070° true at 10.8 m/s (20.994 kt)**. This is consistent, to conversion precision, with the CAD Appendix 5 published mean wind 070°/21 kt supplied to this reconstruction. Structured gust groups report **17.5 m/s (34.02 kt) at 03:00 and 20.6 m/s (40.04 kt) at 04:00**. These are station report values, not instantaneous winds acting on CAL605 between the reports. NOAA and CAD may share the originating observations: their agreement is consistency, not independent replication.

The 10.8 m/s mean speed is higher than **8,285 of 8,360 (99.10%)** observed records in the declared like-for-like routine subset below. There are 17 ties and 58 higher values. Thus this case sits near the high-wind edge of the year's *reported routine normal-wind observations*. It is not representative calm-weather validation. This is exploratory descriptive context; it is **not** an accident probability, return period, flight-selection correction, or calibrated population percentile. Missing calendar hours and repeated correlated weather episodes prevent treating records as independent random trials.

The same-clock-hour check gives 343/348 (98.56%) below at 03:00 and 351/355 (98.87%) below at 04:00. Ties are shown separately in `verification.json`; rounding a discrete value into one exact percentile would hide that ambiguity.

There is also a useful data-quality warning: the **10:00 UTC** event-day row codes calm wind as QC=1 while temperature and visibility are missing and remarks contain forecast-like text. It is retained and flagged `partial_weather_row=True`, not repaired. The rank subset excludes this row by its normal-wind and nonpartial filters. Passing archive QC flags is not sufficient to establish meteorological truth. Another Nov 4 row's free-text remarks contain what looks like a different airport's report; none of that free text is parsed as Kai Tak current conditions.

## Reproduce

From this directory, using Python 3 (stdlib only):

```sh
python3 decode_noaa.py
python3 -m unittest -v test_decode_noaa.py
```

Outputs:

- `observations_1993.csv`: all 8,549 retained records, in source order.
- `observations_1993-11-04.csv`: all 24 event-date records; no removal of suspicious rows.
- `verification.json`: source/document hashes, types, missingness, duplicates, coverage, event comparison and precise rank denominators.
- `test_results.txt`: the recorded twelve-test run.
- `test_decode_noaa.py`: tests sentinel handling, negative temperature/scales, zero, QC rejection with preservation, not parsing gust-like text in remarks, fail-closed unknown/truncated sections, actual event fields and corrupt record lengths.

Before mutating any output, the decoder checks the **pinned acquired archive SHA256**, decodes those exact hashed bytes, and validates **every row** for USAF450070/WBAN99999, year1993, header latitude/longitude/elevation and historical call sign. Any mismatch fails explicitly; substituted station/year rows are never silently filtered into the rank. Tests demonstrate both archive substitution and metadata mismatch leave existing outputs untouched.

The decoder rejects record-length mismatches and unsupported ADD groups instead of silently skipping them. Group lengths come from the official documentation; they cover every additional identifier in this retained file. This is not claimed to be a universal ISD decoder. `REM` and `EQD` are retained as raw text and never searched for numerical gust observations. No imputation, interpolation, averaging, or UTC-to-flight-clock synchronization occurs.

### Independent-review repair

The first implementation recorded the archive hash but did not enforce it. Independent review correctly identified that a replaced station-year source could therefore enter the annual denominator. The repair adds the pinned-source and all-row identity gates above, before any output write. The original acquisition hash matches, and both regenerated CSVs are byte-identical to their pre-repair versions: **no weather values, rank denominators or conclusions changed**. Adjacent checks cover year, both station identifiers, both coordinates, elevation, call sign, empty input and preservation of old outputs on rejection. This is an input-integrity fix, not a model or sample change. It does not establish historical anemometer siting beyond the retained metadata.

## Source and provenance

Original unchanged archive: `../../weather_feasibility_2026-10-13/NOAA_450070-99999-1993.gz`, acquired earlier from [NOAA station-year archive](https://www.ncei.noaa.gov/pub/data/noaa/1993/450070-99999-1993.gz).

- SHA256: `617c7db4f19c3aaacef91ae8a688c0aab196cdfc7ddfba72857c8e70056d66e0`.
- Format documentation acquired and retained as `isd-format-document.pdf` from [official NOAA ISD format specification](https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf), SHA256 `1be604b08b5f7c2429e6aef178ff8893019c234bc7bc51bfb7ec1e16a6682f04`.
- `isd-format-document.txt` is a local `pdftotext -layout` extraction for auditable field lookup. Control/mandatory positions are printed pp. 5–12; gust OC1 is p. 111, pressure MA1 pp. 95–96. Full-source retained fields, not quoted report prose, support derived tables.

Every record identifies USAF 450070 / WBAN 99999, historical call sign VHHH, header coordinates +22.333 / +114.183, elevation 24 m. **This does not reconcile the historic station/anemometer siting or datum with HKO.** No modern VHHH metadata or Chek Lap Kok coordinates were substituted.

## Schema and quality rule

Each numerical field has its unmodified `_raw` token, `_quality` code, `_missing` flag and `_strict_qc_accepted` flag. Numeric columns contain decoded values when present even if quality is not accepted; downstream analysis must explicitly apply the acceptance flag. Empty CSV numeric cells mean missing, not zero. `raw_record` preserves the entire original line. `additional_groups_json` preserves all structured ADD fields. Time is UTC, as specified by the format; `source_line` is one-based.

**Strict analysis acceptance: present numeric value and quality 1 or 5**, meaning all checks passed in the NOAA encoding. Codes 0/4/9 are only gross-check status, 2/3/6/7 suspect/error, and manual/edited codes need separate review; none are silently accepted. This conservative explicit rule is local to this diagnostic and does not overwrite source values. Missing signed values are positive sentinels; genuine negative temperatures remain negative. Code V with missing direction denotes variable direction and is preserved separately; it is not assigned a direction. Conversion to knots uses exactly 1 kt = 1852/3600 m/s.

`gust_mps` comes exclusively from structured **OC1** (four speed digits /10, then quality); absence of OC1 does not mean zero gust. `altimeter_setting_hpa` and `station_pressure_hpa` come from distinct MA1 slots. Neither is relabelled mandatory `sea_level_pressure_hpa`, which is missing in every row here. The format defines wind direction relative to **true north**: no magnetic-runway component calculation is made.

The rank subset is fixed and exposed in `verification.json`: **FM-15 routine report, source flag 4, exact UTC hour, wind type N (normal), present speed with QC1/5, and not missing both temperature and visibility**. Both event-hour records qualify. The reporting-type and wind-type restriction avoids pooling special reports and distinct wind conventions. It also means the denominator is a selected observed subset, not the full calendar year, all weather conditions, or a population of landings.

## QC inventory

| Check | Observed |
|---|---:|
| Rows / event-date rows | 8,549 / 24 |
| Date coverage | All 365 dates, Jan 1 00:00 through Dec 31 23:00 UTC |
| FM-15 / FM-16 records | 8,543 / 6 |
| Duplicate raw records / timestamps | 0 / 0 |
| Missing calendar-hour timestamps / off-hour records | 215 / 4 |
| Missing wind speeds / strict accepted | 19 / 8,530 |
| Gust group present / absent | 519 / 8,030 |
| Missing temperature / visibility | 68 / 43 |
| Altimeter setting present | 8,438 |
| Sea-level pressure / station pressure present | 0 / 0 |
| Partial rows (temperature and visibility both absent) | 19 |

Because gust reporting is selective, no unconditional gust distribution or gust-to-mean prediction law is fitted. No altitude-varying or vertical wind is recovered. The annual diagnostic uses observations after the accident as retrospective context; it is not a forecast or pre-accident fitted policy. Aircraft parameters, terrain, solver, and project specifications were not edited.
