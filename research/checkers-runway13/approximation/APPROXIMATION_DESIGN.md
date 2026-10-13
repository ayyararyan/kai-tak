# Explicit approximate landing rule: what the revised request means

13 October 2026. Research design under Aryan's latest instruction. This replaces exact symbolic global optimality as the required representation; it does not declare the landing problem solved.

## One rule, conditional on a stated domain

The target is

    theta, scene/date -> explicit procedure -> trajectory and outcome ranges.

Here theta contains the stated entry state and aircraft/environment parameters: speed, mass/configuration, wind information, braking delay/deceleration and any documented tracking/error conditions. These inputs may be fixed or vary only within a declared validated domain. Aircraft controls are decisions; braking capability is an exogenous condition, not a variable the optimizer can improve to fit the runway. Scene/date is categorical or interval-evidenced, not an interpolated year number.

A closed-form approximation may be piecewise. For example, in a validated condition cell C_j,

    q_hat(theta) = A_j Phi_j(normalize(theta)),

where Phi_j is a published low-degree polynomial basis and A_j is a fitted, published coefficient matrix. The phase boundary states are then imposed analytically, rather than merely approximately fitted. The output must name its cell and refuse unsupported extrapolation. Changes of binding obstacles may require different cells or route families; do not smooth a path through a hill to avoid a discontinuity. This is the proposed representation, not an already fitted coefficient map.

The underlying terrain-aware solver constructs comparison paths offline. The explicit rule is evaluated without rerunning that optimizer. Held-out tests and rigorous domain bounds determine whether the approximation is good enough. An equation containing an unevaluated argmax is not the deliverable.

## Explicit path representation

For one phase with duration T and normalized time s=t/T, endpoint positions p0,p1, velocities v0,v1 and accelerations a0,a1, use

    c0=p0, c1=T*v0, c2=T^2*a0/2,
    A=p1-c0-c1-c2, B=T*v1-c1-2*c2, C=T^2*a1-2*c2,
    c3=10A-4B+C/2, c4=-15A+7B-C, c5=6A-3B+C/2,
    r(s)=sum(k=0..5, c_k*s^k) + b0*64*s^3*(1-s)^3
                                 + b1*(2s-1)*64*s^3*(1-s)^3.

Position, velocity and acceleration match the specified endpoints exactly in the mathematical model. The b terms change the interior path without disturbing them. The current family uses one approach segment and one flare segment (the final easing of descent before touchdown). Analytic differentiation and inverse dynamics give corresponding speed, tilt, lift and thrust demands. These are a reference schedule, not a feedback law robust to disturbances.

For actual following of the reference, a causal tracking controller/procedure and justified error tube are additional requirements. A separate optimized path for each perfectly known wind is not such a controller. Neither uncertain-future wind nor observed future errors may enter a causal procedure.

## Runway and time outcomes

Let x_TD be distance from the usable landing threshold to touchdown, u_TD the forward ground speed at touchdown, tau the model's delay before braking, a>0 the constant braking deceleration, and L the usable landing distance. Under the existing ground model:

    delay_distance = u_TD * tau
    braking_distance = u_TD^2 / (2*a)
    ground_roll = delay_distance + braking_distance
    runway_consumed = x_TD + ground_roll
    runway_remaining = L - runway_consumed
    flight_time = T_approach + T_flare
    time_to_full_stop = flight_time + tau + u_TD/a.

Report touchdown distance, ground roll, threshold-to-stop distance, remaining runway and time separately. 'Runway used' must not silently switch between ground roll and total threshold-to-stop distance. Time zero is the declared entry state, not airport departure or threshold crossing. The fixed nominal delay/deceleration remain 2 seconds and 0.15g; varying them for sensitivity does not certify that the airborne candidate remains feasible.

For declared independent scalar intervals with nonnegative speed/delay and positive deceleration, monotonicity gives conservative algebraic ranges. For example:

    stop_low  = x_low  + u_low*tau_low   + u_low^2 /(2*a_high)
    stop_high = x_high + u_high*tau_high + u_high^2/(2*a_low)
    remaining = [L_low-stop_high, L_high-stop_low].

Analogous time bounds use u_low/a_high and u_high/a_low. A rectangle of inputs may ignore correlation and overbound the physically feasible combinations. These are conditional parameter-box envelopes, not confidence or prediction intervals. No particular input ranges are invented here.

## Three different uncertainty statements

1. **Mathematical/approximation bound:** errors introduced by the explicit approximation and numerical evaluation, within a specified model/domain.
2. **Conditional model prediction interval:** variability in an individual simulated landing under a documented probabilistic input/model-error law. Requires a sampling/calibration design, coverage level and hold-out checks. A confidence interval for mean stopping distance is not a prediction interval for an individual stop.
3. **Real-world predictive validity:** calibration of aircraft, braking, wind, terrain/registration and tracking discrepancies against evidence relevant to the conditions. Narrow numerical uncertainty is not a substitute.

Pointwise trajectory bands do not imply simultaneous coverage of the full flight. The delivery must specify whether coverage is marginal per output, joint across outcomes, or simultaneous over time. Near-ground clearance requires whole-path reasoning, not the confidence interval of average height. Statistical coverage and physical feasibility are reported separately.

Requested confidence levels and meaningful accuracy tolerances remain unselected; report achieved errors and mark real-world intervals unavailable until evidence supports choosing/calibrating them. Use metres/seconds appropriate to the evidence, not centimetre-looking output precision as an accuracy claim.

## Near-optimality

Preserve the nominal minimum-normalized-margin objective and secondary control effort. For the same scene/conditions/admissible family, a valid upper bound U(theta) and certified achieved lower bound L(theta) give regret at most U-L. A comparison only with numerical solver outputs is benchmark regret, not a global bound. A feasible path may be useful without being shown near-optimal; never conflate them.

The previously reported upper limit 0.03972 was invalidated by a branch-cut error. The surviving nominal synthetic-family bracket is [0.0397,0.1559772). It does not establish close optimality. Terrain changes require fresh feasibility and bound checks. Certificate reconstruction alone was insufficient to discover the earlier bug; adversarial/regression checks must include retaining known feasible witnesses through every global-exclusion ancestor.

## Delivery and current blocker

Final delivery must publish formulas/coefficient tables, conditions, scene identity/date, reference/control interpretation, output ranges, accuracy/coverage validation, explicit infeasible/unknown outcomes and optimality scope. Realistic historical scene integration, a solved condition domain, a condition-to-coefficient approximation and calibrated prediction intervals remain unfulfilled. Current independent work exports the existing synthetic reference and conditional stopping algebra only. It is preparatory work, not the requested final solution.
