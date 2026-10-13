[
  {
    "location": "model/trajectory.py:243-251",
    "trigger_condition": "A later operating-margin array contains NaN while earlier minima remain finite",
    "guard_snippet": "if not all(np.all(np.isfinite(v)) for v in [*m.values(), *h.values()]): raise ValueError('nonfinite margins')",
    "potential_consequence": "Summary can declare sampled feasibility, finite eta, and no violations despite an invalid margin."
  },
  {
    "location": "model/trajectory.py:291-294",
    "trigger_condition": "Allowed zero touchdown sink acquires tiny positive vertical velocity during independent numerical replay",
    "guard_snippet": "if abs(vel[-1,2]) <= replay_velocity_error_bound: return terminal_boundary_unresolved_with_refinement()",
    "potential_consequence": "Numerical sign error reports terminal failure despite replay fidelity passing and exact nominal boundary satisfaction."
  },
  {
    "location": "model/trajectory.py:61-66",
    "trigger_condition": "Custom descent limit permits threshold flight-path angles below minus ninety degrees",
    "guard_snippet": "if not -90 < p['threshold_gamma_deg'] < 0: raise ValueError('invalid air flight-path angle')",
    "potential_consequence": "Accepted minus-100-degree endpoint becomes minus-80-degree actual flight-path angle, silently changing requested boundary conditions."
  }
]
