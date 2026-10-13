# Whole-aircraft integration identities and continuous checks

Prerequisite mathematics for historical integration, not the deferred full optimal-landing derivation. No source-backed global optimum or completed historical clearance is claimed.

## Reference point and physical pose
Let B be the occupied closed body set in a declared body frame. Let b_ref be the body-coordinate point whose world path r_ref(t) is specified, and R(t) its attitude transform into the declared world coordinates. Occupancy is

    A(t) = r_ref(t) + R(t)(B - b_ref).

It is not r_ref+B, and b_ref cannot be silently switched between CG, eye, and wheel contact. Given b_CG and a differentiable rigid-body attitude, in a right-handed world frame set d=R(b_CG-b_ref), dR/dt=[omega]xR. Then

    r_CG = r_ref+d
    v_CG = v_ref+omega×d
    a_CG = a_ref+alpha×d+omega×(omega×d).

Proof: differentiate twice and use d_dot=omega×d. Thus even a constant body offset changes inertial acceleration during roll/pitch/yaw; translating positions alone is not a calibrated dynamics integration. The frozen point-mass path has a lumped ground-contact reference but its airborne inverse forces use that path as the inertial mass trajectory. The integrated physical interpretation requires a genuine CG path plus gear contact, not permission to reinterpret its old certificate as a rigid747 certificate.

In forward/right/up engineering components, positive yaw turns toward right, positive pitch raises the nose, positive bank lowers the right wing. The implementation uses R=Rz(yaw) Ry(-pitch) Rx(-bank). This frame is left-handed relative to ENU; do not import an ENU angular vector/cross product without a consistent basis transformation. `reference_kinematics` is for a declared right-handed world angular-vector convention. The point-mass lift-bank and flight-path angle do not themselves provide body Euler angles, angle of attack, sideslip or deformation. In particular, setting body pitch equal to flight-path angle is not justified.

A source PAPI statement of52ft minimum eye height is not a52ft CG or wheel height. For source eye point b_eye,

    h_eye = h_ref + e_z' R(b_eye-b_ref).

The report supports the eye-height statement, not an available b_eye, flight pose or hard tracking error. Preserve50ft frozen point-reference height as a scenario; no physical equivalence inferred.

## Support function: exact obstacle-plane clearance
For any bounded body set, define h_B(q)=sup_{b in B} q·b. Above a plane with upward normal n and equation n·p=c, minimum body clearance along n is

    min_{p in A(t)} (n·p-c)
       = n·r_ref-c - h_(B-b_ref)(-R' n).

For tracking error in compact set E, subtract h_E(-n); for symmetric E this equals h_E(n). Euclidean normal clearance d requires this expression >=d||n||. Proof: linearity, inf f=-sup(-f), followed by independent Minkowski sum support. This is exact for that plane/body class. Obstacle avoidance in general is NOT equivalent to being above every obstacle's infinite supporting plane: side passage must retain the relevant spatial support/disjunction.

For a box b=center+diag(halfwidth)u, |u_i|<=1,

    h_B(q)=q·center + sum_i halfwidth_i |q_i|.

The active corner is selected by signs of q_i; regime switches occur at q_i=0. For a finite polytope, the active support vertex changes on (b_i-b_j)·q=0, subject to all comparison inequalities. These are exact clearance-expression regimes, NOT optimal-flight regimes or sufficiency proofs for the landing objective. Wing/tail effects cannot be replaced by a constant CG clearance unless that constant is proved to dominate every supported pose.

## Exact polynomial range and all-time body enclosure
For p(s)=sum c_k s^k with real-decimal coefficients and0<=a<=b<=1, put s=a+(b-a)u. Power coefficients are

    q_j = sum_(k>=j) c_k choose(k,j) a^(k-j)(b-a)^j.

Degree-n Bernstein coefficients are

    beta_i = sum_(j<=i) q_j choose(i,j)/choose(n,j).

Because the Bernstein basis is nonnegative and sums to1 on[0,1], min beta_i<=p(s)<=max beta_i. `polynomial_range` computes these bounds with exact rational arithmetic. Polynomial grid samples are verification, not the proof. Finite rational inputs are required and extrapolation rejected.

On a time cell, supply enclosing position ranges, Euler-angle ranges and reference/body vertices. Outward-rounded interval rotation encloses each transformed vertex for every joint parameter value; coordinatewise min/max bounds the convex hull. Adding a tracking box encloses its Minkowski sum. Disjoint outer boxes therefore prove disjoint supplied sets for the whole cell; overlap only means possible intersection, not a proved collision. Domain proof requires the angle boxes to enclose actual continuous attitude, not just sampled attitudes. Current code uses40-digit mpmath interval elementary arithmetic and outward float summaries; it is not a formal proof-assistant or an empirical accuracy certificate.

## Unknown coverage cannot certify free space
A source spot height does not bound intervening roofs, equipment or terrain. If a swept horizontal footprint reaches an unmeasured obstacle whose top is not bounded by the accepted evidence, an above-ground clearance bound cannot be computed from that evidence. Filling the top with0 is an unauthorized assumption. The same observation set can permit different completions with different clearance outcomes. That is a failure of identification/certification, not proof the actual historical aircraft could not land.

The inherited entire-area unknown mask remains epistemic; it is neither an occupied solid nor a free-space map. A complete list of presently known objects is not complete physical coverage. All current historical calls therefore remain blocked, even when synthetic continuous-enclosure tests pass.
