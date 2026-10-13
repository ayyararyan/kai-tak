# Kai Tak historical integration

**Overall: INCOMPLETE. The requested closed-form optimal landing has not been derived.** Historical geometry and physical integration remain unaccepted. The required geometry-first sequence is preserved; no numerical candidate or simplified formula has been substituted for the requested solution.

## What changed

The accepted scope is formalized in [SPEC.md](SPEC.md), with all 16 requirements retained in [TRACEABILITY.md](TRACEABILITY.md). Frozen numerical baselines and invalidated evidence are unchanged. New local work includes:

- Boeing’s official 747-400 planning manual and three-view CAD drawing; current Hong Kong AIP datum definitions; direct inspection of the primary accident report, approach chart, historical maps and aerial photographs.
- Explicit coordinate transformations, independent printed-grid checks, and northern/southern runway registration experiments. The corrected threshold cross-check **fails by 81.5 metres**. Neither fit is accepted as historical registration.
- Two partial, labelled 60 m and 80 m terrain contours on the November 1989 hill map, eight additional readable ground-height observations, and one explicitly unreadable spot. Also: a partial August 1993 southeastern seawall and four mapped approach-light symbols. These additions have source pixels and hashes, not invented heights or uncertainty bounds.
- A conditional whole-aircraft envelope and continuous occupied-volume evaluator. It includes wings and tail, checks time intervals rather than endpoints alone, and reports features and time intervals for supplied-scene clearance. Unknown heights, dates or coverage prevent a clearance result.
- Twenty-eight primary procedure, aircraft and datum observations; a complete audit of the frozen physical parameters; three surface-condition limits and three distinct approach-entry arms.

## Registration: evidence, not an accepted frame

| Check | Result | Interpretation |
|---|---:|---|
| Official ITRF96 → HK80 numerical checkpoint | About 2.8 mm residual | Formula/sign/unit check with a stated zero ellipsoidal-height assumption; not historical ground accuracy |
| Printed grid versus map worldfile | Maximum 0.593 m disagreement | Independent raster-coordinate check; manual picking and cartographic accuracy remain distinct |
| Northern affine fit / held-out RMS | 3.82 m / 12.95 m | Five fitted and four held-out interpreted features; no hard bound |
| Southern affine fit / held-out RMS | 8.32 m / 8.53 m | Five fitted and three held-out seawall controls; no hard bound |
| Northern threshold versus southern end + LDA | **81.54 m disagreement** | Independent diagnostic fails; no averaged threshold adopted |
| Aviation height → HKPD | **Unresolved** | Reported 15 ft AMSL is not converted using a guessed 1.23 m or 1.30 m offset |

One initially considered road control had changed between map and photograph. It was rejected and the earlier result preserved. Projective fits did not resolve held-out errors. The southern direction uses a short baseline extrapolated over 2,786 m, which amplifies angular error. Image perspective and edge semantics remain unresolved. RMS residuals are not deterministic bounds or confidence intervals.

A separate long-edge extraction from near-contemporary maps gives a roughly 134.02° grid direction and approximately 61.0 m opposing-edge separation, consistent with the reported width. This supports the mapped line identities, not centimetre survey accuracy. Replacing the short photographic direction with that mapped direction still leaves a **77.62 m threshold discrepancy**. The frame remains unaccepted. Appendix 9’s variation annotation was enlarged and read as 1°50′W, consistent with Appendix 1; no supposed conflicting variation was adopted.

The primary chart explicitly gives the GP-inoperative KL 15 NM fix as **2219.12N 11356.05E**. Its historical horizontal datum remains unidentified. The chart gives 088° magnetic for the IGS localizer, 135° magnetic for the runway, and 1°50′W variation for 1990. The earlier 133°10′ true bearing remains a labelled scenario, not a 1993 survey or grid bearing. The MM’s reported 1.7 NM is “from touchdown,” not an exact threshold radial. Missed approach is mandatory at the MM without visual reference; that published procedure does not certify the subsequent visual landing path.

## Terrain, structures and aircraft occupancy

[The integrated scene](geometry/integrated_evidence.geojson) contains **88 features**:

- 24 inherited approximate surface observations;
- 45 dated mapped faces and one unknown-coverage mask;
- eight additional readable ground spots, one unreadable spot, and two partial contours;
- one partial seawall, four light-symbol points, and two mapped runway-edge segments.

The new readable spots span 31.4–73.5 m HKPD in the November 1989 source. The contour traces are approximately 52.7 m and 59.0 m long. No intervening surface is interpolated as a certified terrain bound. The southeastern seawall/lights concern the Runway 31/end-of-runway area, not the Runway 13 visual turn.

**New complete historical obstacle volumes: zero. New hard height bounds: zero.** Target-day presence, roofs, equipment tops and relevant continuous coverage remain unresolved. The relative stereo surface has not been relabelled HKPD, and modern buildings have not been substituted for 1993 structures.

The tighter CAD projection-intersection shape failed a dimensional check: its height was below the manufacturer’s 19.51 m static maximum. That rejected result is preserved. The primary conditional box is about 70.98 × 65.36 × 19.82 m including explicitly conditional planning/chord inflation. It is **not** a calibrated in-flight envelope. Landing CG, gear/eye offsets, pitch, sideslip, flaps-30 geometry, deformation and tracking remain unresolved.

The existing point-mass candidate cannot simply be relabelled a CG path or have a 747 attached to it. [The prerequisite derivations](derivations/CLEARANCE_AND_REFERENCE.md) give the reference-point acceleration correction, exact support-function clearance expression and continuous enclosure proof. These are not optimal-flight regimes. Box overlap means possible intersection, not collision; permitted wheel contact needs its own contact model.

## Supported conditions and missing calibration

| Source-supported arm | Necessary restriction | Historical optimum |
|---|---|---|
| Dry runway | Steady crosswind ≤ 25 kt | Not derived |
| Wet, no standing water | Steady crosswind ≤ 22 kt | Not derived |
| Standing water or slush | Steady crosswind ≤ 10 kt | Not derived |
| Published IGS visual transition | MM/visual/missed-approach rules | Not derived |
| IGS glidepath inoperative | Published acquisition/descent conditions | Not derived |
| Explicit conditional visual entry | Full supplied state and admissible entry set | No historical domain inferred |

These wind limits are operator/aircraft-specific historical evidence. Under the old chart-bearing scenario, 070° true / 21 kt gives 18.74 kt crosswind: it passes the first two necessary limits, not the third. Passing is not full landing feasibility. No tailwind domain, mass/configuration range or causal gust policy is inferred.

Boeing takeoff thrust ratings and airport-planning landing curves do not calibrate approach thrust response, control rates or the frozen braking law. The two-second delay, 0.15 g deceleration and 150 m reserve remain unchanged. [The physical audit](PHYSICAL_CALIBRATION.md) records the exact missing calibration and why pilot-eye, CG and gear references cannot be conflated.

## Verification versus completion

- **Correctness:** 36 targeted tests pass. Coverage includes exact rational Bernstein bounds, frame signs/inverses, wing/tail effects, between-endpoint obstacles, rigid-reference acceleration, positional phase joins, feature/time reporting, condition boundaries, and refusal of unknown heights/coverage.
- **Completeness:** 16 requirements: one implemented, ten partially implemented, five blocked. No unapproved exclusions or proxy substitutions.
- **End-to-end:** the historical evaluator correctly emits a structured blocked result and exit code 2. That refusal path is verified. The desired historical clearance and optimum pipeline is not implemented or accepted.

See [verification.json](verification.json) for artifact/source checks and [evidence_gates.pdf](evidence_gates.pdf) for the exported diagnostic comparison. Tests do not replace data, historical acceptance or sufficiency proofs.

## Exact remaining dependencies

1. Jointly controlled runway/procedure registration and a documented 1993 aviation-to-HKPD reference tie.
2. Relevant dated terrain, roof and equipment volumes or defensible bounds, including changed/demolished identities and coverage.
3. Applicable aircraft reference, pose, deformation, tracking, force/control and contact/braking calibration.
4. Then: the complete hybrid derivation, explicit trajectory/control regimes, switching domains, global primary and secondary proofs, independent control replay and continuous validation.

[The identification note](derivations/IDENTIFICATION_AND_SEQUENCE.md) explains the obstruction without claiming that closed forms cannot exist. Missing requirements remain open, not reclassified as an approved smaller task. No permission to continue existing scope is being requested. No outreach, spending, publication or peer sync occurred. Configured web search is unavailable; direct primary-source retrieval worked, but no exhaustive search claim is made. The sole project ledger remains `../PROJECT_STATE.md`.
