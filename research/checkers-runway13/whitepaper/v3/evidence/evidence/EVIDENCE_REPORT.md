# Checkers with Runway 13 — historical evidence acquisition

Checked 13 October 2026. Evidence lane; exploratory acquisition, not a frozen aircraft model or operational procedure.

## Verdict

A useful historical geometry/flight-recorder case is available now: Hong Kong CAD Report 1/95, CAL605, Boeing 747-409B B-165, 4 November 1993. The complete report was previously downloaded; this lane inspected its primary chart and extracted geometry and recorder metadata. **No normal-flight, machine-readable Kai Tak trajectory collection or BA raw QAR archive has been acquired.** The three project aims remain intact; historical validation is currently limited to an accident-case reconstruction and published aggregates.

## Files and authority

- Primary report: `../../../data/kai-tak-2026-10-13/sources/CAD_1-95_CAL605_wayback.pdf` (226 pages). Original document Hong Kong CAD; recovered from [archived HKU copy](https://web.archive.org/web/20180517095657id_/http://ebook.lib.hku.hk/HKG/B35838838.pdf).
- `assets/CAD_1993_IGS_chart_page-131.pdf`, original Appendix 1 extracted without reconstruction. `assets/CAD_1993_IGS_chart.png` is a rendering visually inspected in this lane.
- Existing Appendix 11–13 extracts and plots remain in the acquisition directory; they were not overwritten.
- `assets/VHHX-v4D_simulation_chart_reproduction.pdf`: NEW 12-page, 5,805,378-byte download from [IVAO](https://xe.ivao.aero/download/charts/VHHX-v4D.pdf). **Secondary simulation redraw, not a certified historical chart.** Pages 1 and 9 visually inspected; explicit “Simulation Use Only” markings. PDF has no searchable text: the 12-byte TXT contains only page separators, NOT OCR. Two rendered previews included. Do not promote this file to historical authority.
- `assets/NCAR_LANTEX_project.html`: NEW snapshot of [NCAR's LANTEX project description](https://www.eol.ucar.edu/field_projects/lantex). Describes 15 April–23 August 1994 ISS atmospheric measurements at the **new Chek Lap Kok airport**, not Kai Tak landing demonstrations. Excluded from trajectory validation.
- `geometry_and_case_metadata.csv`: transcribed primary-report values with evidence class and limitations, NOT a frozen model parameter file.
- `recorder_parameter_key.csv`: Appendix 11 labels and sign conventions, not sampled time series.
- `evidence_inventory.csv`: provenance, SHA-256, role and content/schema checks for each listed artifact. No raw series fabricated or digitized.

## Historical geometry that is genuinely supported

Primary CAD report §1.8.1 (PDF32–33; printed25–26): IGS localiser088° magnetic, glidepath3.1°, instrument segment ends at middle marker1.7NM from touchdown. If visual flight not achieved, missed approach is mandatory; climb to4,500ft amsl. §1.10 (PDF33–34) gives runway135° magnetic, elevation15ft amsl, zero slope, length3331.5m, width61m, landing distance available2786m. Consequently the report's47° offset is internally consistent.

Appendix1, PDF131 (visually inspected), marks bearings magnetic and variation1°50′W (1990); chart shows geographical graticule and terrain heights but not a machine-readable terrain surface. Its warning says the missed-approach right turn must occur at the middle marker; early OR late turn loses terrain clearance. Flight-path indications after that marker must be ignored. This warning concerns the specified **missed approach**, not a universal rule that all landing turns begin at one point. The chart's missed-approach calculation assumptions (15° bank,1.5°/s,180kt average) must not become landing-turn limits.

**Source conflict:** IVAO's redraw says runway136° and48° localiser offset, marks variation3W and “Change: Variation/Spec update,” and includes modern navigation content. It cannot silently replace the primary1993 geometry. Its displayed displaced-threshold coordinates are N22°19.3′ E114°11.8′ (RWY13), but these are coarse secondary values, not surveyed coordinates approved for model use. Choose one historical date and magnetic/true-north reference before georeferencing. A47° track offset is not necessarily a47° change of aircraft heading in wind.

## Recorder content and its limitations

CAD §1.11.1 (PDF36/printed29) states Fairchild F1000 DFDR, more than24h recorded,269 parameters:89 variable and180 discrete; AAIB UK obtained satisfactory replay with very few corrupted areas. This does not mean all269 parameters are published. The published plots are a small selected subset.

Appendix11 PDF150 contains the parameter key. Figures1–2 (PDF151–152) cover approximately3min from1700ft; Figures3–4 (PDF153–154) cover72s synchronized with selected CVR annotations. Included controls are control-wheel roll angle, control-column pitch input and rudder-pedal position. These are **cockpit control positions**, not automatically aerodynamic surface deflections. Other variables include CAS, barometric/radio altitude, heading, pitch, roll, angle of attack, drift, acceleration, wind estimates and selected engine/system indicators. Thrust-lever angle explicitly was NOT recorded (§1.11.5). Engine spool/pressure indicators cannot be labelled directly observed throttle input. The scan does not by itself identify each variable's original sampling interval, accuracy, lag or digital quantization.

**Important independence issue:** §1.11.6 (PDF41/printed34) says Appendix12's flight path was reconstructed by integrating longitudinal and lateral accelerations. It is not independently measured GNSS trajectory truth. Comparing the path to the same acceleration traces is a consistency check, not independent validation. Figure6 is the preceding Taipei landing, not another Kai Tak case.

**Important causal issue:** §2.6.5 (PDF92–93/printed85–86) describes a controllable touchdown, approximately480m beyond displaced threshold at160kt groundspeed; the report explicitly says touchdown parameters were NOT a causal factor in this accident and the aircraft could/should have stopped safely. Do not turn the runway overrun into evidence that the historical checkerboard geometry was inherently unsafe or that an alternative turn would have prevented this accident.

Case metadata in §1.6: aircraft747-409B, engines fourPW4056, flaps30 on finals, estimated landing weight525,718lb with report parenthetical239.0tonnes. Preserve the published pairing; metric value is approximate, not an exact unit conversion. This case does not select the project aircraft without Aryan's model decision.

## BA collection and other acquisition results

The earlier acquisition report established Holtom's abridged article and aggregate sample; no new BA raw flight data obtained here. The1079-flight sample must NOT be called1079 Kai Tak flights: stated high-bank-angle observations are associated with Kai Tak, not conclusively the entire denominator. No missing histogram reconstructed. No full1999 proceedings obtained in this lane.

Search limitations are real: native web search failed with403 model-owner verification; alternate search connector returned isError. Direct Google returned JS interstitial, DuckDuckGo a challenge, and Bing RSS often returned irrelevant first-term results; these attempts do NOT justify a claim of comprehensive absence. The VHHX search did return the successfully downloaded IVAO file. NCAR direct retrieval succeeded. A fresh direct Holtom article download failed; no empty article file is represented as successful. No paywall/authentication bypass, outreach, publication or spending performed.

Public availability does not establish an open redistribution or machine-learning license. CAD/HKU archive, IVAO redraw and NCAR page retain their own rights; record citation/provenance and clarify permission before public redistribution. Local research inspection is the scope here.

## Defensible validation plan — proposed, not silently implemented

1. **Historical case reconstruction:** digitize Appendix11 independently twice, calibrating both axes and retaining pixel/line-width/time-alignment intervals, original page/figure, units and sign. Report the reconstructed samples as approximate digitized measurements, never raw DFDR. Do not interpolate high-frequency control actions from coarse plots without declaring the estimation.
2. **Coordinate discipline:** establish1993 geometry from original chart/graticule and historical surveyed references. Separate true/magnetic heading, ground track, CAS/TAS, barometric/radio/terrain-relative altitude. Current terrain/building data cannot stand in for1993 obstacle geometry.
3. **Internal consistency only where appropriate:** verify heading/roll/speed/descent relationships conditional on model approximation and wind uncertainty. Propagate uncertainties. Do not treat the acceleration-derived map and original acceleration as independent replications. Do not fit the model to the entire trace then describe the same trace as held-out validation.
4. **Bound confrontation:** a recovered flight interval inside a sufficient feasible set supports model-consistency for that interval; an apparent crossing outside a necessary bound triggers uncertainty/model/input audit, not a declaration that the pilot violated physics. Classify feasible/infeasible/unresolved using interval uncertainty; solver failure is not infeasibility.
5. **Historical optimality comparison:** fix aircraft/configuration, entry state, terminal target, historical obstacles, wind/information available and objective. A certified feasible strict improvement disproves baseline optimality only for that objective and model. Do not cherry-pick the accident to generalize about all historical pilots or compare perfect-future-wind optimization against a pilot without that information.
6. **Normal-flight validation remains blocked:** obtain decoded routine-flight QAR/DFDR export from archive custodians; recover parameter dictionaries, calibrations, sample rates, flight identifiers, aircraft/load/configuration and rights. Existing unsent request drafts are concrete acquisition next steps, not authorization to send.

## Readiness

Source inspection and inventory: verified. Raw normal-flight dataset: unavailable. Numeric plot digitization: not started. Historical geometry georeferencing: not completed. Full obstacle/aircraft model: not identified. Analytical-bound validation and claims of safer/optimal landing: not established.
