#!/usr/bin/env python3
"""Export the actual interval finite objects from the accepted proof formulas.

This uses the original interval_root.py and validate.py algebra, at their
original precision. Exact decimal preconditioners and exact binary interval
endpoints accompany mpmath's directed bounds() strings. No root solve or
optimization is run. Output is additive, never an old certificate rewrite.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
source = args.source_root.resolve()
project = source / "research/checkers-runway13"
local = project / "integrated/assumption_solution/refinement/local_certificate"
output = args.output.resolve()
if local == output or local in output.parents:
    parser.error("do not write into the sealed local certificate directory")
sys.path.insert(0, str(local))
import interval_root as r
import validate as v
from mpmath import mp

t = time.monotonic()
stored = json.loads((local / "certificate.json").read_text())
center, radius = stored["root"]["center"], stored["root"]["radius"]
I, iv = r.I, r.iv
rad = I(radius)
X = [I(c) + iv.mpf([-rad.b, rad.b]) for c in center]
f, j0, *_ = r.system(center)
_, jx, margins, curvature, signs = r.system(X)
mp.dps = 55
inverse = mp.inverse(mp.matrix([[mp.mpf(r.decimal_mid(x)) for x in row] for row in j0]))
C_decimal = [[mp.nstr(inverse[i, j], 48) for j in range(9)] for i in range(9)]
C = [[I(x) for x in row] for row in C_decimal]
R = r.minus(r.eye(9), r.mm(C, jx))
correction = [-x for x in r.mv(C, f)]
deviation = r.mv(R, [iv.mpf([-rad.b, rad.b])] * 9)
K = [x + y for x, y in zip(correction, deviation)]
row_sums = [sum((abs(x) for x in row), I(0)) for row in R]
norm_upper = max(x.b for x in row_sums)
assert norm_upper < 1
assert norm_upper < I("2e-14").a
assert all(x.a > -rad.a and x.b < rad.a for x in K)
assert all(abs(x).b < I("2e-34").a for x in K)
assert [r.bounds(x) for x in K] == stored["root"]["krawczyk_offset"]

A = [[margins[j].d[k] for j in range(6)] for k in range(5)] + [[I(1)] * 6]
mp.dps = 55
Am = mp.matrix([[mp.mpf(r.decimal_mid(x)) for x in row] for row in A])
inverse_A = Am ** -1
CA_decimal = [[mp.nstr(inverse_A[i, j], 48) for j in range(6)] for i in range(6)]
CA = [[I(x) for x in row] for row in CA_decimal]
RA = r.minus(r.eye(6), r.mm(CA, A))
A_row_sums = [sum((abs(x) for x in row), I(0)) for row in RA]
A_norm_upper = max(x.b for x in A_row_sums)
b = [I(0)] * 5 + [I(1)]
approx = r.mv(CA, b)
residual = r.mv(CA, [x - y for x, y in zip(b, r.mv(A, approx))])
epsilon = max(abs(x).b for x in residual) / (1 - A_norm_upper)
weights = [x + iv.mpf([-epsilon.b, epsilon.b]) for x in approx]
assert A_norm_upper < 1 and all(x.a > 0 for x in weights)
assert A_norm_upper < I("2.5e-14").a
assert min(x.a for x in weights) > I("0.0009658").b
assert [r.bounds(x) for x in weights] == stored["simplex"]["multiplier_enclosures"]


def entry(x):
    return {"directed_bounds_strings": r.bounds(x),
            "exact_binary_endpoints": [[int(v) for v in endpoint] for endpoint in x._mpi_]}


def matrix(A):
    return [[entry(x) for x in row] for row in A]


result = {
    "source_commit": "78a9ce1c627f917c94306af5529d5e9ebeb743e8",
    "verified_utc": datetime.now(timezone.utc).isoformat(),
    "interval_precision_decimal_digits": iv.dps,
    "midpoint_inverse_precision_decimal_digits": 55,
    "preconditioner_decimal_significant_digits": 48,
    "coordinate_order": ["T_flare/5", "x_touchdown/300", "u_touchdown/75", "flare_x_bump",
                         "flare_z_bump", "eta", "s_slew", "s_load_upper", "s_thrust_lower"],
    "margin_order": ["stop", "gate_slew", "touchdown_slew", "interior_slew", "load_upper", "thrust_lower"],
    "center_exact_decimal": center,
    "radius_exact_decimal": radius,
    "box_interval_hull": [entry(x) for x in X],
    "F_center_interval": [entry(x) for x in f],
    "J_center_interval": matrix(j0),
    "J_box_interval": matrix(jx),
    "C_exact_decimal": C_decimal,
    "C_interval_hull": matrix(C),
    "R_equals_I_minus_CJ": matrix(R),
    "R_row_sum_intervals": [entry(x) for x in row_sums],
    "R_infinity_norm_upper_endpoint": entry(norm_upper),
    "negative_C_F_center_interval": [entry(x) for x in correction],
    "R_deviation_interval": [entry(x) for x in deviation],
    "Krawczyk_offset_interval": [entry(x) for x in K],
    "strict_inclusion_verified_in_interval_arithmetic": True,
    "all_J_box_matrices_nonsingular_verified": True,
    "A_augmented_gradient_interval": matrix(A),
    "CA_exact_decimal": CA_decimal,
    "CA_interval_hull": matrix(CA),
    "RA_equals_I_minus_CA_A": matrix(RA),
    "RA_row_sum_intervals": [entry(x) for x in A_row_sums],
    "RA_infinity_norm_upper_endpoint": entry(A_norm_upper),
    "simplex_approximate_solution_interval": [entry(x) for x in approx],
    "simplex_preconditioned_residual_interval": [entry(x) for x in residual],
    "simplex_solution_error_radius_interval": entry(epsilon),
    "simplex_weight_intervals": [entry(x) for x in weights],
    "simplex_nonsingularity_and_strict_positivity_verified": True,
    "matches_original_Krawczyk_offsets_and_weights_exactly": True,
    "additional_exact_decimal_inequalities_verified": {
        "R_infinity_norm_strict_upper": "2e-14",
        "Krawczyk_offset_infinity_norm_strict_upper": "2e-34",
        "RA_infinity_norm_strict_upper": "2.5e-14",
        "smallest_multiplier_strict_lower": "0.0009658"},
    "slew_signs": signs,
    "encoding": "Each exact finite binary endpoint is [sign, mantissa, exponent, bitcount], representing (-1)^sign * mantissa * 2^exponent. Directed bound strings retain original mpmath bounds() formatting; C_exact_decimal and CA_exact_decimal are the exact real-rational preconditioner inputs, not rounded display floats.",
    "source_sha256": {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [local / "interval_root.py", local / "validate.py", local / "certificate.json"]},
    "seconds": time.monotonic() - t,
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"output": str(output), "R_norm_upper": r.bounds(norm_upper),
                  "RA_norm_upper": r.bounds(A_norm_upper),
                  "matches_original": True, "seconds": result["seconds"]}, indent=2))
