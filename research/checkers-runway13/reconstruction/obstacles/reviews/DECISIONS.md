# Obstacle evidence review decisions

13 October 2026. Three independent native review roles inspected the new-file snapshot; the acceptance auditor also inspected the original-reading images and rebuilt the exports read-only. No role certified historical aviation clearance.

| Finding | Decision | Required repair |
|---|---|---|
| Source-crop linkage can be omitted from a future accepted row | Accept, patch | Make crop bounds mandatory and check source pixels and point containment |
| Datum support and receipt review metadata can be omitted | Accept, patch | Require pinned datum image/text, reviewer/time, accepted count/IDs and inspected evidence |
| Raw manually supplied presence/accuracy fields can contradict enforced unknown fields | Accept, patch | Reject asserted presence, numerical accuracy and physical upper-bound claims in this evidence class |
| Alternate footprint path produces constant-path provenance | Accept, patch | Export the actual verified input path |
| Current 24 map readings, symbols and platform/terrain interpretations | Accepted for bounded transcription | Preserve all values and source uncertainty; no new upper surface or volume |
| Historical obstacle reconstruction remains incomplete | Unresolved scientific requirement, not waived | Retain null roof tops, full unknown coverage, epoch/datum/accuracy gates |

These repairs enforce the existing frozen specification and do not change model meaning. The review did not require revised values, geometry, source dating or new assumptions. Verified fixes and final checks are recorded in `../parent_verification.json` when complete.

## Evidence scope

Blind review: static supplied snapshot only. Edge review: read-only reachable-path probes against the builder. Acceptance audit: all24 point-image symbols, both legends, original hill context, all45 preserved footprint geometries/properties, and fresh in-memory build matching saved objects. The separate aviation-source investigator inspected the original CAD pages; the acceptance auditor did not claim a second aviation-page audit.
