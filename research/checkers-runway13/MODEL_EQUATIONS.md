# Constrained model v1: what the optimizer is solving

13 October 2026. Research scenario, not operational flight guidance.

## 1. Fixed scientific object

The executable searches a finite-dimensional family of smooth approach and flare trajectories for the chosen Boeing 747-400 research scenario. The aircraft identity, mass and configuration are historically anchored; aerodynamic and operating envelopes are assumptions. Maximizing a numerical slack in that assumed model is not equivalent to maximizing operational safety.

Let x point along runway 13, y to its right and h up from runway elevation. No georeferencing is asserted. The documented magnetic offset is 88−135 = −47 degrees; this fixes the nominal inbound **ground track**, not air heading in arbitrary wind.

Let r(t) be a smooth position path, w a known constant wind, v = r_dot − w, V = ||v||, gamma = asin(v_h/V), and psi = atan2(v_y,v_x). Set

    eV = (cos(gamma) cos(psi), cos(gamma) sin(psi), sin(gamma))
    eg = (-sin(gamma) cos(psi), -sin(gamma) sin(psi), cos(gamma))
    ep = (-sin(psi), cos(psi), 0).

For g>0, define required non-gravitational acceleration f = r_ddot + (0,0,g). Then

    ell_g = f · eg
    ell_p = f · ep
    L = m sqrt(ell_g² + ell_p²)
    phi = atan2(ell_p,ell_g)
    CL = 2 L / (rho V² S)
    D = 0.5 rho V² S (CD0 + k CL²)
    T = m (f · eV) + D.

These equations are algebraic inversion of the coordinated point-mass dynamics, not a fit to historical flight controls. In particular, a smooth geometrical curve may require excessive bank, lift, thrust or thrust slew, and must then be rejected. The derived q=phi_dot is bank-angle rate, not body-axis roll rate.

Equivalent airspeed is V sqrt(rho/rho0). The recorded CAD reference speed is not true airspeed: approximating low-altitude CAS by EAS is explicitly an assumption. The report's 525718 lb gives 238461.67357166 kg by exact conversion; its printed 239 tonnes is rounded.

## 2. Independent forward check

Given derived histories L(t), T(t), phi(t), integrate states (x,y,h,V,gamma,psi) using

    r_dot = V eV + w
    V_dot = (T-D)/m - g sin(gamma)
    gamma_dot = (L cos(phi)/m - g cos(gamma))/V
    psi_dot = L sin(phi)/(m V cos(gamma)).

Lift histories can instead be replayed as CL commands, recomputing L from replayed V and h; that is a stronger force-consistency check. Compare the integrated state against the original curve and check constraints again. Sampling/replay agreement is numerical corroboration, not an interval proof for every instant. Aerodynamic control inversion ignores sideslip, pitch/yaw inertia and real actuator mappings; a 6-DoF validation remains absent.

For spatially/temporally changing wind, the correct velocity dynamics require the material wind acceleration dw/dt. This implementation's constant-wind restriction must not be extended by merely adding gusts to the position equation.

## 3. Landing and ground transition

The threshold is an intermediate target, not the end of landing. The flight curve continues through a flare to the declared ground-contact reference. Touchdown is a hybrid transition: the runway supplies the vertical contact force/impulse; the ground model then governs forward motion. This point-mass transition is not a landing-gear or structural-impact calculation.

With touchdown forward groundspeed U, fixed brake delay tau and fixed deceleration a_b>0, the idealized stop station is

    x_stop = x_touchdown + U tau + U²/(2 a_b).

The reserve constraint is x_stop <= LDA − 150 m, with LDA=2786 m. This is a stipulated scenario stopping law, not a wet-runway performance guarantee. LDA, not total runway length, is the correct available length in the selected threshold frame. A finite runway width is also required; touchdown sink, heading/track and bank need their own tests and must not be hidden by a stopping-distance result.

## 4. Objective and comparison class

Write every physical inequality as g_j(z,u)>=0 in its own units. Choose documented positive scales s_j and define normalized slack c_j=g_j/s_j. Equality constraints are satisfied by the path parameterization and do not receive arbitrary positive margin. Optimize

    maximize eta, subject to c_j(t)>=eta and all hard constraints,

then minimize the declared integrated squared control demand with eta no worse than eta_star−1e−4. Slack is sensitive to the chosen normalizations; it is not a unit-free natural definition of safety. Publish individual margins as well as eta. A better score in this path family establishes neither global optimality nor historical superiority.

An infeasible fixed baseline is not a fair operational comparator. If the optimizer finds a feasible curve from an infeasible numerical seed, that is construction of a scenario path, not improvement over a valid historical flight.

## 5. Uncertainty and outstanding requirements

The long-run research object remains a causal-policy disturbance bound: there exists one admissible information-constrained feedback policy that lands (and preserves the required go-around option) for every allowed wind/entry disturbance. Separate wind-conditioned inverse-dynamics trajectories swap that quantifier order and cannot solve it. Wind stresses here are falsification diagnostics only.

Historical mode needs historical obstacle/corridor geometry, calibrated aircraft dynamics/envelopes, weather and observation assumptions. Routine-flight validation needs actual records and their uncertainties. None is inferred from an optimizer success flag. The synthetic corridor, even if every point lies inside it, is not a surveyed Kai Tak terrain clearance result.
