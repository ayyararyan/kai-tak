# Physical calibration audit

The Boeing manual and CAD report support specific statements, not a calibrated six-degree-of-freedom 747-409B landing model. The frozen baseline remains unchanged. See the 28 hash-bound observations in `source_observations.json` and the complete parameter audit in `physical_parameters.json`.

## What is now source-backed

- CAD Report1/95 printed p11 gives fourPW4056 engines, estimated525718lb landing mass, and **zero-fuel** CG27.1%MAC. The latter is not landingCG. The mass conversion is238461.67357166kg; decimal precision does not remove source estimation uncertainty.
- Printed pp25–28 and Appendix1 give the IGS/visual/missed procedure, runway dimensions and **pilot-eye** PAPI convention. The published GP-inoperative15NM fix is2219.12N11356.05E; the historical horizontal datum is not established in this chart.
- Printed pp49–50 give the operator's steady crosswind limits:25kt dry,22kt wet withoutstandingwater,10kt standingwater/slush. Passing this necessary operator condition is not landing feasibility, a gust bound or an optimality result. It does not identify allowable tailwind or a fullwind envelope.
- Boeing's generic747400 planning manual gives dimensions and static loading/ground-clearance ranges. Its current2024 revision and1998timestamped CAD drawing do not establish the exact1993 flaps30 in-flight occupied set. The website's “should be accurate within +/-6inches” is planning guidance, not a hard bound on wing deformation.
- The manufacturer supplies rated **takeoff** thrust56750lbf perPW4056. It does not supply the needed net approach thrust map or a100kN/s totalthrust slew calibration. The existing700kN cap is neither replaced nor validated by the takeoff rating.

## Missing force/attitude/actuator identification

The frozen inverse point-mass equations calculate required lift, bank and thrust from a path under an assumed polar. They do not identify body pitch, yaw, sideslip, angular inertia, control-surface deflections or actuator-rate feasibility. Lift-bank rate is not body-axis roll rate. The state used for force inversion must be the CG, whereas ground contact belongs to the main wheels. A translated gear path has different acceleration during rotation. `derivations/CLEARANCE_AND_REFERENCE.md` proves the required correction.

No accepted empirical calibration was obtained for CD0=.08, inducedfactor=.045, CLmax2.8, bank25deg, bank-rate5deg/s, load .5–1.4g, thrust700kN or slew100kN/s. Recorded flight responses alone do not identify these maxima or the polar without a stated observation/error model and sufficient excitation. CAD printed p44 explicitly says thrustleverangles were not recorded; Boeing inferred them by matching an engine model. That model's identification data/parameters are not supplied here. A trace labelledN2 is not itself a thrust control law.

The source airspeed is CAS; the frozen model approximates CAS byEAS. The assumed atmospheric density and541.2m² wingarea remain scenario inputs in the frozen configuration. No automatic source promotion has been performed. Gear flex, suspension and compression, CG/eye/gear body offsets, angleofattack/sideslip, inflight flex and tracking/attitude errors remain necessary for physical clearance and contact.

## Ground model: preserved, not calibrated

The frozen law is2s delay then constant1.4709975m/s² deceleration,150m reserve. CAD printed p14 instead describes wheelspin/ground/throttle activation logic and possible autobrake disarming. Printed p79 reports AFM rollout examples at160kt:2350m(setting2),2100m(setting3),1720m(setting4), with additional source assumptions. Boeing's current airportmanual3-36 gives **FAR airportplanning** landinglength curves underzero wind, pressurealtitude andweight, with a note toconsulttheairline. These are distinct objects, not interchangeable calibration points for the stipulated law.

At160kt the frozen delay-plus-brake law gives about2467.52m of groundtravel. That comparison is a model diagnostic, not a statement that the historical aircraft could not stop or that its actual touchdown caused the accident. The report says the actual touchdown was controllable; stronger braking was available. We have not silently changed deceleration, reserve or delayed activation to improve feasibility.

## Contact and rollout are still separate unsatisfied requirements

The continuousenclosure routines certify only supplied geometrical sets. Real gear-to-runway contact is permitted contact, while fuselage/wing/engine contact is not. A boundingbox overlapping the runway at touchdown is therefore neither a collisionproof nor an adequate contactmodel. Groundroll lateral friction, tyre load, crosswind steering, reverse-thrust and speedbrake state are not supplied by the scalar stoppinglaw. No wholeaircraft hybrid stopcertificate follows from the new boxchecks.

## Evidence that would close these specific gaps

A loading/CG and gear/eye geometry record for the configuration; a justified rigid/deformable occupied envelope with pose/tracking bounds; aircraft-specific aerodynamic/control-response and braking data with applicability/uncertainty; and an explicit contact/ground model consistent with the preserved objective and frozen-law comparison. Acquiring licensed/proprietary data or contacting an operator/manufacturer has not been authorized or performed. This does not assert that such data cannot be obtained.
