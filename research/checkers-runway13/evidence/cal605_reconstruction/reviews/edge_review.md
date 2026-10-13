[
  {
    "location": "wind/reconstruct_wind.py:103-130; wind/plot_wind.py:18",
    "trigger_condition": "A documented ? speed or direction anchor is supplied; both reproduce TypeError.",
    "guard_snippet": "difference = None if a is None or b is None else a-b; propagate nulls through summaries/plots; count missing cells",
    "potential_consequence": "Build crashes after replacing three outputs, leaving stale diagnostics alongside new null-bearing records."
  },
  {
    "location": "noaa/decode_noaa.py:117-127",
    "trigger_condition": "Retained event record with USAF 450071 or year 1994 still qualifies for annual ranks.",
    "guard_snippet": "if sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SOURCE_SHA256: raise ValueError(\"Wrong retained archive\"); validate station/year before writing",
    "potential_consequence": "Changed-source station/year contamination enters 1993 Kai Tak diagnostics; regenerated hash records, but never rejects, substitution."
  }
]
