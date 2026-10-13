# Original aviation-source obstacle audit

Verified 2026-10-13. This lane inspected the original CAD CAL605 report, not flight-simulator charts. Output is 14 source-linked numerical context observations, **zero new accepted individual obstacle heights and zero georeferenced elevation points**. Do not count these rows as added obstacles.

## Useful verified facts

- PDF pp33–34 (printed26–27): runway elevation15ft AMSL (=4.572m in that same unresolved AMSL realization); source says no slope; runway135° magnetic,3331.5m long,61m wide,LDA2786m. Promontory242.3m wide and parallel taxiway separation111m. Full original pages were visually checked. These constrain later runway registration and datum consistency, but do not themselves supply surveyed threshold coordinates or a shoreline polygon.
- PDF p131 / Appendix1 A1-1 visually inspected: actual chart scale1:400,000; all altitude/height/elevation figures in feet; heights related to aerodrome elevation15ft; bearings magnetic; variation1°50′W(1990). Chart regional labels were not interpreted as point obstacles because their symbol semantics were not established. The chart is far too coarse for building reconstruction.
- PDF p143 / Appendix9 A9-1 visually inspected: airport plan depicts terminal, runway/taxiway, checkerboard and approach lights. The small annotation beside Checker Board remains ambiguous in the original150ppi one-bit image even after enlargement and orientation correction. It is retained as a rejected extraction candidate, not guessed.
- Official Lands Department datum explanatory notes PDF pp7–8 / A4–A5: mean sea level approximately1.23m above HKPD for North Point1965–1983; approximately1.30m for Quarry Bay1997–2015; chart datum0.15m below HKPD. Text independently reread. Neither mean defines the report’s aviation AMSL realization; no automatic conversion was applied.

## Source precision and support

`source_observations.json` preserves values, units, exact pages, classification, source hashes, null horizontal geometry, null hard uncertainty bounds and `clearance_eligible:false`. Exact international-foot unit conversion does not make a rounded source height exact. Neither source states an obstacle inventory complete for the approach. Datum offsets describe specific observation epochs, not a proven1993 aviation registration.

The source report was already available: this is a newly inspected/hash-bound structured evidence package, **not newly acquired historical geometry**. Original sources unchanged; only this folder was written. No aircraft/model edit, publication, or source redistribution performed.

## Next evidence action

Prioritize already-georeferenced contemporary large-scale survey sheets for explicitly identified spot levels/contours, building outlines and object-associated roof elevations. Retain terrain point observations separately from roof tops; a spot elevation does not upper-bound an entire obstacle. CAD runway facts can serve as an independent cross-source check only once the two vertical datums and runway geometry are reconciled.
