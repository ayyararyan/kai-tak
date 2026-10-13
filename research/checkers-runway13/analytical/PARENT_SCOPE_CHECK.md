# Parent mathematical scope check

13 October 2026. Internal review of the analytical lane's stated problem, not a claim of full landing optimality.

- Direct integration of a right circular turn from heading −δ to0 gives displacement (R sinδ,R(cosδ−1)). Solving the two endpoint equations gives the stated straight lengths. D=C−BR and B=2tan(δ/2)−δ>0, so minimum distance at the largest geometrically feasible radius follows within this family.
- For descending coordinated flight at fixed horizontal speed U, use tan(phi)=U²/(gR cos(gamma)), not the level-flight formula. This distinction is explicitly preserved.
- With fixed altitude loss H and freely chosen constant slope, gamma=-atan(H/D). Differentiating log(sqrt(1+H²/D²)/R) yields the single stationary condition D³+2H²D−CH²=0. Its derivative 3D²+2H² is positive; clipping the stationary radius gives the interval optimum.
- The free-slope altitude variant changes vertical entry/exit velocity across radii. It must not be represented as a comparison at the numerical model's fixed seven-state initial condition. At fixed gamma and H, D and generally R are fixed instead.
- A theorem minimizing bank/time in a restricted family is neither a proof for the existing nominal-margin objective nor a global lower bound for the full unrestricted trajectory problem. The family restriction and instantaneous-bank relaxation work in different directions, so no unproved bound transfer is allowed.
- Historical terrain is needed to identify a relevant feasible set. Mathematical optimality does not remove uncertainty in measured terrain, navigation or aircraft performance.

Primary literature rechecked directly by parent: https://arxiv.org/abs/2412.04797 and https://arxiv.org/html/2412.04797v1. The primary author listing names Fanchen Wu and Zheng Chen. The paper explicitly separates quadratic-root and nonlinear-transcendental candidate solutions for its constant-speed, altitude-hold, steady-wind setting. Its title's use of closed form must not be imported as a claim that every candidate uses only elementary evaluation.
