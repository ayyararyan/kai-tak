[
  {
    "location": "aerial_registration/dense_stereo.py:32-36",
    "trigger_condition": "Bilinear right-disparity interpolation mixes invalid sentinel with valid disparities: 69 current correspondences, six exported.",
    "guard_snippet": "right_ok = all_nonzero_weight_remap_contributors_valid(d2, xr, yr); valid &= right_ok",
    "potential_consequence": "Invalid right matches pass consistency gating and enter the exported dense point cloud."
  },
  {
    "location": "scene/build_scene.py:46-50",
    "trigger_condition": "A regenerated sparse CSV contains finite points rejected by its diagnostic or positive-depth flags.",
    "guard_snippet": "if r[\"passes_diagnostic_5px_filter\"] != \"True\" or r[\"positive_depth_both_views\"] != \"True\": continue",
    "potential_consequence": "Rejected points regain accepted display status; named rejected roofs appear as measured relative heights."
  },
  {
    "location": "scene/build_scene.py:36; scene/template.html:13",
    "trigger_condition": "A modern polygon contains interior rings; current component 3810921432T20050430:0 has one.",
    "guard_snippet": "rings_local = [local_ring(r.coords) for r in [q.exterior, *q.interiors]]; render_all_ring_walls(rings_local)",
    "potential_consequence": "The delivered comparison omits real courtyard walls and inner roof boundaries."
  }
]
