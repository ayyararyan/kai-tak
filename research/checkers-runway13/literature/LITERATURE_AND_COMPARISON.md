# Checkers with Runway 13: literature and comparative research design

Date: 2026-10-13. Status: sourced exploratory research package, not a frozen model, theorem, simulated result, or operational recommendation. Scope: Aryan's three aims—derive bounds, confront historical records, investigate a better admissible landing path. Working agreement and existing project brief/README loaded. This file proposes design choices; it does not silently approve aircraft parameters or an objective.

## Verdict

Yes, a mathematically defensible comparison is possible. It is not yet established that a safer historical-technology alternative exists. “The historical approach” is a procedure permitting varied flown trajectories, not an identified globally optimal curve. We must specify whether we challenge one recorded flight, one reconstructed guidance policy, or the best member of a procedure-constrained family.

For a minimization objective J and common feasible set F, one verified candidate c in F with J(c) < J(b) proves the particular baseline b suboptimal. It does not establish that c is globally optimal, that all historical approaches were inferior, or that real-world accident probability falls. Closed form is neither necessary nor sufficient for that comparison.

## What existing work already supplies

### 1. Constant-speed wind benchmark

[Wu and Chen (2024), sections 2–4](https://arxiv.org/html/2412.04797v1) uses altitude hold, constant airspeed, a known steady wind slower than airspeed, bounded turn control, and prescribed terminal position and heading. It characterizes four candidate path families; two involve quadratic roots and two transcendental equations, with a root-enumeration procedure. Thus its “closed form” is not universally an elementary expression. This is a useful relaxed horizontal minimum-time benchmark, not a descending airliner landing solution: no terrain, roll-rate state, pilot information, go-around constraint, or touchdown dynamics appears in its formulation. Full assumptions in section 2 were inspected; its proofs have not been independently audited.

### 2. Smooth curvature is not a new research topic

[Kostov and Degtiariova-Kostova (1995)](https://emis.muni.cz/journals/AMUC/_vol-64/_no_2/_kostov/kostov.html) constructs suboptimal planar paths with continuous tangent/curvature and bounded curvature derivative, with prescribed endpoint positions, headings and curvatures. The abstract states a distance-versus-derivative-bound restriction and an additive suboptimality bound. Abstract inspected, not the complete proof. [Bakolas and Tsiotras (2009)](https://sites.utexas.edu/ebakolas/publications/) is separately verified in the author's publication list as “On the Generation of Nearly Optimal, Planar Paths of Bounded Curvature and Bounded Curvature Gradient,” ACC, pp. 385–390; its full text remains to be obtained.

Our model translation—not a theorem claimed from either source: for a still-air, constant-speed coordinated level turn, curvature kappa = g tan(phi)/V², so d(kappa)/ds = g sec²(phi) dot(phi)/V³. Consequently a constant curvature-gradient limit is NOT exactly a constant roll-rate limit; their relation depends on bank. Wind further separates air-relative and ground-track curvature. Substituting clothoids without checking this mapping changes the model.

### 3. Descending Dubins-like paths already inform landing optimization

[Bakolas, Zhao and Tsiotras (2011)](https://dcsl.gatech.edu/papers/aiaa11.pdf) develops semi-analytic initial guesses: descending three-dimensional Dubins-like geometry, time parametrization respecting control limits, then numerical landing optimization. Sections II–III distinguish restricted path-family optimization from global 3D optimality. This is an especially useful precedent for our analytic-to-numerical workflow, not evidence of an airport-specific theorem. Browser-indexed full text was inspected, but direct download returned 404; no local copy is claimed.

### 4. A strong six-degree-of-freedom comparator exists

[Kim et al. (2024)](https://arxiv.org/html/2405.16680v1) formulates aircraft landing with 6-DoF RCAM dynamics, runway alignment and obstacle avoidance, solved through sequential convex programming. Section 2.1 assumes a rigid aircraft, flat non-rotating Earth, constant density/gravity and constant wind without shear. Their alignment constraint applies in the final approach phase; continuous-time constraint violations between temporal nodes are explicitly addressed. This is a relevant numerical comparator, not a Kai Tak historical reconstruction, a proof of global optimality for our problem, or a robust-gust guarantee. A reported Monte Carlo solver success rate is not an aircraft accident probability. Key assumptions and constraint discussion inspected; full algorithm not independently reproduced.

### 5. Planning geometry and tracking safety must be separated

[FaSTrack, Chen, Herbert et al. (2021)](https://arxiv.org/html/2102.07039v1) couples a simplified planner to richer tracking dynamics through an HJ-derived tracking-error bound and a safety controller. It demonstrates cars and quadrotors, not Kai Tak airliners. Section VI discusses additional recursive-safety needs when a planner cannot stop instantly; that matters for aircraft. The conclusion explicitly acknowledges perfect sensing and a representative tracking model. Its guarantee is conditional on its disturbance/model/information assumptions, not permission to label any path “safe.” Its architecture is valuable here: inflate obstacle constraints by defensible tracking uncertainty instead of checking only a centerline.

### 6. Reachability and abort-landing analysis are established

[Kirchner et al. (2020)](https://arxiv.org/html/2005.07875v1) applies backward reachable tubes to helicopter emergency landing, using a numerical trajectory-optimization approximation and specified terminal speed/height limits. Its helicopter dynamics are not transferable to a 747; pilot reaction dynamics are identified as future work. Use it as a methodological precedent, not a numerical safety certificate for Kai Tak.

[Bulirsch, Montrone and Pesch (1991)](https://doi.org/10.1007/BF00940502) treats abort landing in windshear as a minimax optimal-control problem. The institutional bibliographic record/abstract was verified; detailed theorem assumptions remain unread. This older literature is a mandatory lead before claiming a new robust go-around result. “Minimax” alone does not identify whether uncertainty is adversarial wind or a maximum-over-time performance objective; inspect the equations before borrowing a claim.

## Proposed comparison: preserve the counterfactual

Freeze a common scenario record before solving: aircraft and configuration, mass, entry state/time, runway/terrain/obstacles at the historical date, weather realization or uncertainty class, admissible observations, navigation aids, pilot/control response delays, actuator and aerodynamic envelope, landing target, missed-approach option, and horizon.

Recommended primary comparison is safety-margin improvement under historical information/operational constraints. Candidate objective for Aryan to select: maximize the magnitude of a specified disturbance class for which an admissible feedback policy can reach the landing gate while preserving a defined go-around option until a specified commitment gate. This requires specifying the uncertainty set, commitment rule and pilot/controller class; it is not a parameter-free meaning of “safest.” Report terrain clearance, stall/load margin, roll demand, terminal errors and tracking burden separately. Do not trade lower fuel/time against violated safety constraints through a convenient weighted sum.

Keep three explicit arms:

1. **Historical-condition baseline:** a procedure-consistent reconstruction and, where identifiable, measured flights. Use uncertainty bands, not an invented unique historical trajectory. Label reconstructed policy versus recorded path.
2. **Same-conditions alternative:** identical admissible information, aircraft, terminal target, obstacles and operating rules; optimize the selected criterion. A baseline path known only after the flight cannot be treated as a fully identified feedback policy under unobserved gusts.
3. **Modern-guidance counterfactual:** improved navigation/state estimation/autonomous tracking if investigated. This is a different question, not evidence that pilots should have flown this alternative with 1990s information.

First derive and reproduce reduced-model benchmarks, then compare numerical solutions in the same model; only after that test sensitivity to richer dynamics. Model stages must remain explicit and preserve all three eventual aims. Closed-form bounds can be useful even if the realistic optimum is numerical.

## Historical validation and proof discipline

The acquisition README reports CAL605 accident-recorder plots, not raw synchronized data or successful demonstrations. Do not use that accident as the historical optimal policy. Digitized curves, if later authorized and produced, need axis calibration, timing synchronization, units, uncertainty intervals and provenance. Unknown control inputs/wind cannot be filled with a convenient truth. Fit any estimated parameters separately from held-out checks; one accident cannot establish typical pilot behavior.

Use historical records first for model falsification: do documented measured states/kinematics lie within the predicted envelope after uncertainty? If a model declares a demonstrably flown segment impossible, investigate geometry, wind, timing, or restrictive assumptions. Successful passage of a segment proves neither safe full landing nor go-around availability. Conversely, an accident does not show the turn was infeasible; later events and decision choices matter.

For each result maintain evidence classes:

- Constructive feasible trajectory/policy, independently integrated and constraints checked continuously or with valid error bounds.
- Necessary-condition violation or certified outer exclusion, under stated assumptions.
- Unresolved: solver failure, incomplete global search, overlapping measurement/objective error intervals.
- Comparative improvement: strict advantage exceeding reconstruction and numerical uncertainty, on the common feasible set.
- Global optimum: separately justified exhaustive candidate characterization, lower-bound certificate, or validated global method. Multistart alone is not such a certificate.

For uncertainty, distinguish “one causal feedback policy for every disturbance in W” from “a different trajectory after learning each entire wind history.” The latter grants hindsight. Monte Carlo and adversarial search are falsification tools; their non-failure is not a universal guarantee.

## Contribution and next step

A worthwhile white paper need not invent new control theory. A reproducible, historically faithful Kai Tak benchmark with transparent analytic bounds, uncertainty-aware record confrontation and a fair candidate comparison would already satisfy a serious research-hobby purpose. A new theorem would need a precisely missing result relative to the literature, not merely a new airport coordinate substitution or the inclusion of roll/wind/obstacles.

Recommend first selecting the aircraft envelope, landing/commitment gates and safety objective, then building a source-backed geometry/state specification. No globally better path, historical suboptimality, new theorem or real-world safety improvement has yet been established.

## Search and acquisition limits

Focused searches covered bounded curvature derivative, landing trajectory optimization, HJ landing safety, and Kai Tak with optimal/optimization/trajectory terms. Kai Tak-specific searches returned largely unrelated airport resource-allocation or simulation material, not a directly usable comparative flight-path paper. This limited search is not proof of absence. Other languages, historical engineering archives, thesis citations and full reference chaining remain open.

Three primary PDFs were downloaded and SHA-256 recorded in `sources/manifest.json`; signatures checked. The two Gatech URL failures are recorded rather than passed off as downloads. Rights to redistribute any paper are not inferred. No simulator, theorem implementation, institutional outreach, publication or repository push was performed.

Verification: PDF text extraction confirms all three titles; checksums recomputed successfully. The unversioned FaSTrack PDF URL resolved to v2 (13 March 2021), while cited HTML assumptions were read in v1; no claim of a version-by-version theorem comparison is made. Wu–Chen PDF is v1.
