# Historical landing/weather data: feasibility findings

Checked 13 October 2026. Research-discussion evidence, not a new frozen model or a completed historical validation. Aircraft, objective, braking, solver and terrain-owner files unchanged.

## New acquired weather source

Downloaded NOAA's legacy ISD station-year file:
https://www.ncei.noaa.gov/pub/data/noaa/1993/450070-99999-1993.gz

- Local original: `NOAA_450070-99999-1993.gz`, 127,633 bytes.
- SHA256: `617c7db4f19c3aaacef91ae8a688c0aab196cdfc7ddfba72857c8e70056d66e0`.
- Gzip decompression succeeds; 8,549 fixed-width records span 1993-01-01 through 1993-12-31. There are 24 records dated 1993-11-04.
- Header location codes: latitude +22333, longitude +114183, elevation +0024; historical ICAO field VHHH. Do not replace these automatically with the modern inventory's Chek Lap Kok coordinates (+22.309,+113.915) or select a historical station from today's airport code alone.
- `verification.json` records acquisition time, checksum, counts and sample headers. Verification is of file integrity and header structure, not complete meteorological quality control or site-history reconciliation.
- The attempted Global Hourly CSV endpoint did not produce the expected CSV schema. The legacy gzip endpoint above worked. NOAA now has a successor hourly product; this retained historical source must be versioned, not silently exchanged.

NOAA documentation describes wind, visibility, temperature, pressure, cloud and other fields, but presence, missingness, duplicates, units and quality flags must be checked for each field in this file. Station identity/location history and the actual anemometer must be reconciled with HKO before scientific use. Hourly surface observations are not the three-dimensional gust field experienced in a final turn. No decoded analysis table or calibrated wind model is claimed. NOAA access is public; third-party report and airline data rights remain separate.

Source documentation:
- https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database
- https://www.ncei.noaa.gov/pub/data/noaa/isd-format-document.pdf
- https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv

## Existing flight report contains directly matching weather evidence

Primary local source: `../../../../data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf` (resolve from project/workspace roots; canonical acquisition path is workspace `data/kai-tak-2026-10-13/sources/`). CAD Report 1/95 concerns the actual 4 November 1993 Kai Tak CAL605 landing. Appendix 11 has selected DFDR plots; Appendix 12 is an acceleration-integrated track, not independent position truth. Raw recorder samples remain unavailable.

Fresh inspection of the report's searchable text found:
- Section 1.7.7: SE, mid-runway and NW anemometers; reported official winds came from SE. Two- and ten-minute means are distinguished.
- Section 1.7.11 and Appendix 7 (begins PDF page 137): printed wind-system records for 03:30–03:40 UTC. The system recorded every ten minutes in benign conditions and every thirty seconds when its shear threshold was exceeded. This is event-dependent sampling, not an uninterrupted 30-second series.
- Appendix 7 explains present-wind, two-minute, ten-minute and extreme-value fields and lists five locations including Lei Yue Mun and Yau Yat Chuen.
- Section 1.7.11 explicitly says the anemometers did not measure vertical currents and that alignment between the wind-system and ATC clocks could not be established. Do not assume exact synchronization with DFDR.
- Appendices 5 and 6 add meteorological reports and sensor locations. Appendix 22 discusses the windshear event; Appendix 24 includes runway friction analysis. Their applicability to model calibration must be assessed separately.

These are a matched historical case, not a representative successful-landing sample or an identified accident-risk distribution. Scanned traces/printouts require uncertainty-preserving digitization; OCR alone is not numeric ground truth.

## Wider sources and access status

- HKO's 1993 Summary documents airport observations at hourly or more frequent intervals: https://www.weather.gov.hk/tc/publica/smo/files/smo1993.pdf . Indexed text inspected; direct screenshot retrieval timed out, so no table values transcribed from this source.
- HKO research describes Kai Tak wind/gust observations within its 1968–2008 study: https://www.hko.gov.hk/en/publica/reprint/files/r832.pdf . This establishes historical measurement use, not public release or completeness of all underlying records.
- HKO offers surface, upper-air and warning data requests, potentially paid: https://www.weather.gov.hk/en/cis/reqform.htm . Specific station/time coverage and availability must be confirmed. No request or purchase sent.
- Holtom's authored FOQA article, mirrored at https://theairlinepilots.com/forumarchive/flightsafety/foqaflightdataanalysis.php , establishes historical BA analysis including Kai Tak. Its 1,079-approach denominator is not verified as exclusively Kai Tak; no raw series recovered. Airline, investigation and aviation-weather archive leads remain leads, not promised releases.

## Mathematical interpretation and proposed outputs

Flight records can identify observed trajectory/response relationships and calibrate parts of an aircraft-and-disturbance model when adequate states, controls, configuration and excitation are present. Position and airport weather alone generally cannot separate controls, aerodynamics and unobserved local wind. Observed pilot choices do not uniquely identify an objective or prove optimality.

Recommended direction within the existing approximate-explicit goal:
1. Reconstruct observed paths with measurement/time/registration uncertainty, retaining successful approaches, go-arounds and incidents as different outcomes where available.
2. Estimate identifiable model parameters and out-of-sample tracking/model discrepancy. Hold out whole flights/dates, not adjacent frames from one trace. A single accident cannot calibrate a population 95% prediction interval.
3. Construct dated, uncertainty-aware landing-feasibility sets using historical obstacles, aircraft constraints and specified wind sets. An inner feasible set is not the entire true feasibility boundary; solver failure outside it is not infeasibility.
4. Fit an explicit condition-to-polynomial-coefficient map to terrain-aware reference solutions, validate it on held-out conditions, and certify constraints and objective gap separately. Feedback against unknown future gusts is a further requirement, not implied by a known-wind path.
5. Compare historical/candidate paths under identical entry state, aircraft, wind information, terminal target and objective. A better feasible path establishes improvement in that model; a global upper bound is required for a global near-optimality claim.
6. Compare dated city geometries while holding aircraft, weather and objective fixed. If only obstacles are removed, feasible sets can only expand; real epochs need not be nested. Observed year differences are confounded by fleet, procedure, weather and selection changes.

Useful theoretical precedents, not novelty claims:
- Explicit piecewise-affine MPC under linear-quadratic/polyhedral assumptions: https://cse.lab.imtlucca.it/~bemporad/publications/papers/acc00-mpqp.pdf . The nonlinear landing problem does not automatically inherit this exact form.
- Inverse-control non-identifiability: https://arxiv.org/abs/2305.15332 . Inferring an objective is distinct from estimating dynamics or choosing the project's agreed objective.

Priority: digitize the already-held matched CAL605 flight/weather case as a reconstruction benchmark, and obtain routine-flight records for generalization. Preserve the planned multi-date geometry work. No new scientific result or operational landing procedure has been established by this acquisition.
