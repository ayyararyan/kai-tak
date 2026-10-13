# Integrated requirement audit — specification v1

Overall **INCOMPLETE**. 16 requirements:1Implemented,10Partiallyimplemented,5Blocked. These are full requirement statuses, not a claim that all components of a partial row exist. No unapproved exclusion, proxy substitution, objective change or downstream sequencing waiver.

| ID | Status | Implementation/evidence | Verification | Remaining requirement |
|---|---|---|---|---|
| INT-01 | Implemented | SPEC, frozen source manifest, canonical ledger append |13frozenhashes;37inheritedartifacthashes | Preserve on further work |
| GEO-01 | Partially implemented | North/south affine and projective diagnostics; thresholdpicks; frames.py |Printedgridcheck; officialnumericcheckpoint; independentnorth/southcrosscheck | Accepted historical threshold/bearing and defensible ground uncertainty; originalcrosscheck81.5m/mapped77.6m; followup diagnoses endpointsemanticlink; conditional61mextension leaves17.88m, NOTaccepted |
| GEO-02 | Blocked | CAD15ftAMSL; currentAIP/HKPDdefinitions; Appendix14 explicitHKPDsurveycontrol with missingnumericalschedule |Unknown datumrefusal test |1993aviation-toHKPD realization/offset and error |
| GEO-03 | Partially implemented | SourceIGS/MM/missed rules; explicitKL15NMcoordinate;3entryarms |ActualAppendix1 inspected; observationhashes | Historicalfixframe, complete registered entrysets; replace synthetic corridor without assuming terrainclearance |
| GEO-04 | Partially implemented |21sheetoverview; partial1993SEseawall; inherited24surfaceobservations;8newgroundspots and2partialcontours |Originalsourcepicks, worldfilecheck, geometryvalidity | Continuousdatedterrain/coastcoverage, targetdaypresence/errorbounds |
| GEO-05 | Blocked |45datedfaces plusunknownmask;4newlightpoints withnulltops |Unknown-top/epochrefusal | Historicalrooftop/equipmentvolumes;changed/demolishedidentities; defensibletopbounds |
| GEO-06 | Partially implemented |88features retain sourcehashes/dates/unknownstatus |Inheritedcounts, validgeometry andsourcehashchecks | Acceptedcomplete relevant scene, physicallysupported uncertainty/coverage |
| AIR-01 | Partially implemented |Boeingstaticdrawing/manual envelope; exactreferenceidentities |CADextentcheck; rotation/reference tests; rejectedtighterhullpreserved | Inflightshape/configuration,CG/gear/eye,pose/tracking bounds |
| AIR-02 | Partially implemented |Intervalrigidbody + exactBernstein continuouscells; feature/timereporting |Wing/tail/betweenendpointcases; unknowncoverage refuses | Actualflight/flare/contact/stop join; limitinghistoricalhazard with supportedbound |
| AIR-03 | Partially implemented |28primaryobservations; completefrozenparameteraudit; PHYSICAL_CALIBRATION |Sourcepages inspected; frozenlawunchanged | Aerodynamic/actuator/braking applicabilityanduncertainty calibration |
| OPT-01 | Blocked |Objective preserved; threecondition/entryarms catalogued |Necessarycrosswind boundaries tested | Establishedhistoricalconstraintmodel followedbycompletecondition-dependenthybridproblem |
| OPT-02 | Blocked |No replacement toy/singlecandidateformula |Sequencegate explicitly refuses | Fullclosedform trajectories/controls, switching/regime domains |
| OPT-03 | Blocked |No historicalglobalityclaim |Oldlowercertificate nottransferred | Primary/secondarysufficiency and exactclassglobalproof |
| UNC-01 | Partially implemented |Explicitunknowns; quantifier/disturbance/go-around obstruction recorded |NoRMS-tohardbound promotion; causalflagfalse | Calibrateduncertainty, onecausalpolicy, viability/go-around and physicalCI/PI |
| VAL-01 | Partially implemented |36priorunit/property/integrationtests;7newfollowupdiagnostictests; artifactverification |verification.json; followup/verification.json; sourcehashes; diagraminspection | Realintegratedhistoricalendtoendacceptance and derivedcontrolreplay unavailable |
| OUT-01 | Partially implemented |REPORT,README,evaluator,proofnotes,conditiontable, exportedfigures |Artifactmanifest and structuredblockedgate | Requestedclosedform/proof/limitinghazarddeliverables remainmissing |

No requirement is classified as “unidentified by design”: missing data remain unsatisfied work, not an approved exclusion. One failed registration or missing parameter has not been hidden behind a successful unit test. There is no historically certified conditioncell.

## Additive follow-up

See [endpoint/datum investigation](followup/REPORT.md) and [new diagnostic receipt](followup/verification.json). All16statuses remain unchanged. The source-backed61moffset is a hypothesis, not accepted registration. Publicsurveyindex no-match is bounded to that layer; no source-exhaustion claim. Original145-file checkpoint manifest is preserved under followup/prior_checkpoint/.
