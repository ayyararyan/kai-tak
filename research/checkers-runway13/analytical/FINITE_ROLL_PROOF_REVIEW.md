# Independent finite-roll proof review

2026-10-13. Audited `FINITE_ROLL_POSITION.md` and `verify_finite_roll_position.py`; fresh numerical run completed at 11:26:24 UTC. The working agreement was reloaded. Frozen-model boundary/objective requirements from the prior audit remain the comparison standard. Only this review file was written; the verifier's output JSON and frozen simulator were not modified.

## Verdict

No fatal mathematical error found. The finite-roll displacement, position matching, strictly decreasing chord W, strictly increasing matched total length D, feasible interval and fixed-altitude uniqueness theorem are correct for the explicitly restricted family. Its optimum is generally an implicit monotone scalar root, not an elementary closed form. The text accurately preserves that distinction and does not claim the requested full optimal landing has been solved.

## Proof checks

- Constant U and gamma yield `k=g cos(gamma)/U=g/V`; integrating maximum-rate bank entry gives `q=(k/p) log(sec b)`. The triangular cap follows from `2q=delta`.
- Reflection of heading and the complex displacement formula are consistent, including the hold term's phase and sign. Substitution `u=sin² z` transforms the entry integrand to `u^(−1/2) (1−u)^((−1−ia)/2)/(2p)`, hence exactly the stated incomplete beta parameters. On the real integration interval both bases are positive, so real logarithms define an unambiguous branch.
- Solving the endpoint equations with the reflected turn chord gives the stated s, ell and D. These preserve fixed speed, descent angle and zero boundary bank; they do not silently impose an altitude match.
- The heading-domain bank envelope is correct. Near either endpoint, bank is proportional to the square root of heading progress, making the time singularity integrable. Positive chord weight and increasing bank imply strict decrease of W. The negative interior weight in the matched-length integral reverses that sign and makes D strictly increase.

An independent differential calculation makes the signs and triangular conditioning explicit. Put `c=delta/2`, `v=c−q(b)`. Cancellation of moving ramp/hold join terms gives, below the triangular endpoint,

    W'(b) = −2U sin(v)/(k sin² b),
    D'(b) = 2U [sin(v)/cos(c)−v]/(k sin² b).

Here `0<v<c<pi/2`, so W'<0. Since `sin(v)/v >= sin(c)/c > cos(c)`, D'>0. Both derivatives approach zero when v approaches zero at the triangular endpoint. A zero endpoint derivative does not invalidate strict monotonicity or root uniqueness; it does explain poor inverse-root conditioning there.

## Feasibility and boundary cases

As b approaches zero, W diverges; W at the maximum admissible bank is its attained minimum. Thus the stated Wlim comparison gives an empty interval, a singleton, or `[bgeo,bmax]`, respectively. A finite Wlim always gives a strictly positive geometric lower bank when feasible. At bgeo at least one straight vanishes. If strictly positive straights are demanded, a singleton case becomes empty; in a nondegenerate case the lower endpoint is excluded and its objective value is only an infimum.

Fixed negative gamma converts exact altitude loss into a required horizontal length. Continuity and strict increase of D give the claimed necessary-and-sufficient interval condition and unique peak. At gamma zero, altitude loss must be zero and does not select a peak. A prescribed time in that level case should be expressed directly as `D(b)=U Tfixed`, since `H/(−tan gamma)` is undefined there; this is only a notation clarification to the paragraph, not a defect in the theorem.

The frozen-scenario obstruction is valid: required constant-slope length 2303.6274 m is shorter than the 2692.5824 m endpoint chord. The exact deficit is 388.9550 m. Equal endpoint EAS with unequal density also conflicts with constant TAS under the stipulated density model. These exclude the restricted family, not the variable-gamma/TAS frozen landing problem.

## Fresh numerical evidence and limits

- All 30 supplied constructed cases and five explicit rejection cases passed through `runpy`/`run()`, without running the JSON-writing main block.
- Worst independent RK4 turn-position discrepancy: `1.4445e-10 m`; heading discrepancy: `3.4493e-14 rad`; altitude recovery bank discrepancy: `6.8950e-8 rad`.
- Additional central finite differences agreed with both independent analytic derivative formulas at four interior peaks, including a peak at 99% of triangular bank.
- Additional zero-straight triangular construction verified a singleton feasible endpoint and infeasible straight lengths immediately below it.
- Incomplete-beta equivalence was checked algebraically. A separate high-precision library comparison was not run because mpmath was unavailable; no such numerical validation is claimed.

The verification helper's fixed lower bisection bound `bmax*1e-4` is suitable for its constructed sample cases, not a general existence-aware bracket for arbitrary large Wlim. Reuse as a general solver would require adaptive bracketing plus explicit feasibility checks. Floating-point tolerances near triangular bank are not interval certification. Ordinary-domain tests do not establish extreme-parameter stability or full aircraft force feasibility.

**Correctness:** restricted proofs independently checked and synthetic verification passed. **Specification completeness:** full analytical landing remains incomplete. **End-to-end readiness:** no historical/operational feasibility or frozen-objective global certificate established.
