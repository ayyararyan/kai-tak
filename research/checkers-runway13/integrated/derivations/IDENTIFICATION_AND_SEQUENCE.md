# Why the historical optimum has not yet been derived

This is a prerequisite/identification analysis, not a substitute closed-form solution and not an impossibility theorem about closed forms.

## The intended object

Let θ collect the accepted historical frame, entry/procedure set, dated terrain and occupied obstacle sets, aircraft/attitude/reference parameters, admissible controls, wind/information specification, contact/stopping law and tolerances. The requested primary value is

    η*(θ) = sup { η : an admissible complete approach/flare/contact/stop
                     satisfies the frozen normalized inequalities c_j≥η,
                     and all dated-geometry and procedure hardconstraints }.

Among primarynearoptimizers within the frozen1e-4 allowance, minimize the existing normalized integrated squared effort. No arbitrary obstacle-distance normalization has been added. Geometry restricts admissibility; it does not replace the objective. Historical θ is not established merely by source filenames or fittedimage coordinates.

## Unidentified tops obstruct a clearance value, not all mathematics

Fix a geometrical candidate and a horizontally relevant footprintF. If the available observations do not determine or upperbound its1993 roof/equipment topH, admissible completions of the evidence can have differentH. Where the occupied body's minimum height aboveF isq, choicesH<q andH>q can change the above-roof clearance outcome. This is a conditional nonidentification statement: it applies when both completions are consistent with the evidence andF is actually reached. It does not claim arbitrary tall buildings could exist at every location, nor prove that the candidate hits a historical building. Our data currently supply neither the required targetdatevolume nor hard bound.

The same reasoning applies to an unresolved height-datum offset. A point height measuredfromHKPD cannot be subtracted from a runwayrelative height until the offset/reference convention is fixed. A modern statedoffset is not a1993measurement.

## More hazards can only shrink a fixed model's feasible set

For identical dynamics, objective, entry and terminalconditions, adding a hard obstacle constraint producesF_new⊆F_old, henceη*_new≤η*_old when both suprema are defined. Proof: supremum over a subset. This does **not** transfer the old candidate's lower certificate: it must satisfy the new constraints. Nor does it automatically transfer old upperbounds when entryconditions, reference/dynamics or terminalconstraints are changed. The requested historical extension changes assumptions that old scalarbounds condition on; those bounds have not been repurposed as historical-optimality bounds.

## Wind paths are not a causal policy

Separate knownconstantwind solutions have quantifiers

    for everyw there exists a trajectoryu_w.

The required robust causal result is

    there exists one admissible causal policyπ such that for every allowed
    wind/disturbance realization the resulting landing/go-around requirement holds.

The first statement does not imply the second: trajectorychoice can depend on future information unavailable toπ. No gustprocess, observationfiltration, actuatorresponse, disturbancehardbounds or viablego-aroundset has been calibrated here. Conversely, failure to constructπ is not proof that no such policyexists. Statistical confidence/prediction intervals also need an observation/error distribution or a statedfrequentistcalibration, absent from the present evidence.

## Exact remaining analytical work

Once the historical constraint model and admitted condition domains are established, the intended next work remains the completehybrid problem: derive candidate activeobstacle/control regimes, explicit trajectories/controls or identify unavoidable implicit equations, switchingconditions and regimecoverage; then prove sufficiency/globality in the precise admissible class and solve the secondaryobjective. A supportfunction's signregimes are clearance-expressionregimes, not optimalflightregimes. NecessaryPontryagin/KKTconditions, a polynomial with fittedcoefficients, a local numericaloptimum or a single feasiblepath will not closeOPT-02/03.

**Present state:** geometry/physical integration acceptance is not established. In compliance with the required “then” sequence, no historical optimaltrajectory formula or globalproof has been claimed or substituted. No result here establishes that universal or piecewise closedforms do or do not exist.
