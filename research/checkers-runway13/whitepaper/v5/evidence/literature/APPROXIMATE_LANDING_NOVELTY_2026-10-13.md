# Approximate landing with guarantees: preliminary novelty assessment

Date: 13 October 2026. Bounded primary-source literature screening, not an exhaustive systematic review.

## Verdict

Optimized landing/descent, robust control under weather uncertainty, touchdown dispersion, and mathematically certified safety are established research areas. A broad claim that approximate optimal landing with uncertainty is new is not supportable. No directly matching published Kai Tak approach-to-stop procedure with dated obstacles, calibrated outcome uncertainty and a certified near-optimality gap was located in this screening. This is not evidence of absence.

The strongest prospective contribution is a reusable explicit approximation with a demonstrable accuracy/computation advantage, continuous-path safety conditional on a documented uncertainty domain, and a quantified performance gap, validated against strong existing methods. Kai Tak would be a demanding case study; its name alone does not establish methodological novelty. A careful historical reconstruction could separately contribute a dataset or benchmark.

## Primary precedents and boundaries

1. **Kamo et al., 2022, Fundamental Framework to Plan 4D Robust Descent Trajectories for Uncertainties in Weather Prediction.** Weather-ensemble robust optimal control, expected operational costs and scenario feasibility; numerical application to Leipzig/Halle Airport. This directly establishes airport-specific uncertainty-aware descent optimization, not the complete approach–flare–ground-stop certificate requested here. Publisher indexed abstract/conclusion inspected; direct full-page access failed. DOI: https://doi.org/10.3390/aerospace9020109 ; https://www.mdpi.com/2226-4310/9/2/109

2. **Kim et al., 2024, Six-Degree-of-Freedom Aircraft Landing Trajectory Planning with Runway Alignment.** Six-degree-of-freedom RCAM dynamics, obstacle avoidance and runway alignment via sequential convex programming. Full HTML inspected. Assumes constant wind without wind shear. Do not infer calibrated probability coverage or global optimality from its numerical trajectory solutions. https://arxiv.org/html/2405.16680v1

3. **NASA, 1980, Development and flight evaluation of automatic flare laws with improved touchdown dispersion.** Adaptive sink-rate and specified-trajectory flare control evaluated in simulation and flight on the TCV B-737, improving longitudinal touchdown dispersion against an earlier flare law. This establishes long-standing outcome-dispersion work, not full-route global optimization. Official abstract inspected. https://ntrs.nasa.gov/citations/19800061375

4. **Zhao, Efficient and robust aircraft landing trajectory optimization, Georgia Tech repository (2012).** Hierarchical geometric construction, smoothing/tracking and numerical optimal control for constrained fixed-wing landing, with historical-accident simulations. Repository abstract inspected, not a complete independent proof audit. https://repository.gatech.edu/items/a720d925-4535-4bbc-8aee-bf004b7f2c2d

5. **Ariadne: A common-sense thread for enabling provable safety in air mobility systems with unreliable components.** Indexed institutional manuscript mentions Kai Tak in an illustration and discusses complete fallback trajectories through landing. The located passage does not present the requested Kai Tak optimizer. Full manuscript was not successfully opened; do not claim an exhaustive negative finding from the passage. https://repository.kaust.edu.sa/bitstreams/45258999-3dfb-4782-9d39-8e6e028088e4/download ; conference DOI https://doi.org/10.2514/6.2022-0057

## Three different guarantees

- **Optimality gap:** conditional on model, objective and admissible path family, how much better the unknown best path could be.
- **Outcome uncertainty:** possible/probable variation in path, touchdown and stopping under weather, geometry, aircraft and tracking errors. Deterministic envelopes and probabilistic prediction intervals are different products.
- **Statistical confidence:** uncertainty in estimated parameters or in an empirically established coverage statement; requires data and a defined inferential procedure.

The surviving nominal bracket 0.0397 <= eta* < 0.1559772 is a model/family performance bracket, not a real-world confidence interval and not a tight near-optimality result. Withdrawn 0.03972 and other defective-checker exclusions remain invalid. Our model score is not a calibrated accident probability.

## Search scope and next comparison

Queries combined aircraft landing trajectory optimization, robust autoland, weather uncertainty, touchdown dispersion, optimality bounds, and Kai Tak with trajectory/optimal control/landing optimization; misleading typhoon, airport scheduling and redevelopment hits were excluded. This was a web-indexed primary-source screening, not a complete Scopus/Web of Science/patent/manufacturer-internal survey. It establishes related work exists, but neither universal airport coverage nor absence of an exact match.

Before claiming novelty, compare explicit-rule evaluation cost and approximation error against numerical optimization and trajectory-tracking baselines, using the same aircraft, admissible controls, hazards, objective and uncertainty domain. Validate uncertainty coverage separately from optimization accuracy. Demonstrate what the proposed theorem or method adds beyond applying existing algorithms at a new airport.

Ownership: this note is the literature lane. Approximation/specification and terrain reconstruction remain with their existing sessions; no simulator, aircraft, braking rule or scene input was changed here.
