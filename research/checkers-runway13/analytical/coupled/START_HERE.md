# Plain-English result

We have constructed a complete landing and checked that it obeys the chosen
model's rules throughout the flight and stop, including between sample points.

We have also proved that a best path exists within the model's fixed family of
smooth curves. We have **not identified that best path** or derived its exact
closed-form formula. The feasible candidate is not a proven optimum.

The global checker initially reported much tighter limits, but a contradiction
test exposed an interval-library branch problem. Those results were withdrawn;
the feasible-candidate proof was rerun and passed. The separate conservative
upper bound remains valid.

These are results for the uncalibrated nominal model, not a historical Kai Tak
safety certification. Detailed arguments, checks and remaining gaps are in
RESULTS.md. No model settings or braking strength were changed to obtain the path.
