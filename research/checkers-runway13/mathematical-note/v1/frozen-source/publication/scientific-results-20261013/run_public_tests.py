"""Run the 117 tests reproducible from this public Git snapshot.

No scientific tests are edited. Explicit exclusions: two original-workspace
preservation tests and five historical-source tests. Publication integrity has
its own mapping-aware checker; restricted originals are not mocked.
"""
from pathlib import Path
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'research/checkers-runway13'
EXCLUDED = [
    'test_parent_snapshot_unchanged', 'test_preserved_packages',
    'test_control_influence_not_silently_deleted',
    'test_hypothesis_remains_unaccepted',
    'test_pythagorean_residual_decomposition',
    'test_source_residual_reproduction',
]
FILES = [
    'counterfactual/test_counterfactual.py', 'integrated/test_integrated.py',
    'integrated/followup/test_diagnosis.py',
    'integrated/aircraft_followup/test_prerequisites.py',
    'integrated/assumption_solution/test_solution.py',
    'integrated/assumption_solution/refinement/test_refinement.py',
    'integrated/assumption_solution/refinement/local_certificate/test_local_certificate.py',
]
GEO = '''import unittest,sys
suite=unittest.TestSuite()
for module in ['integrated.test_frames_and_gate','integrated.test_source_geometry']:
    for cls in unittest.defaultTestLoader.loadTestsFromName(module):
        for test in cls:
            if not test.id().endswith('.test_source_observations_hashes_and_unknown_fixdatum'):
                suite.addTest(test)
assert suite.countTestCases()==15
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
'''
if __name__ == '__main__':
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    # Do not let an inherited PYTHONPATH silently substitute private research code.
    env.pop('PYTHONPATH', None)
    subprocess.run([sys.executable, str(HERE/'verify_public_snapshot.py')], check=True, env=env)
    subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *FILES,
                    '-k', ' and '.join('not '+name for name in EXCLUDED)], cwd=ROOT, env=env, check=True)
    subprocess.run([sys.executable, '-c', GEO], cwd=ROOT, env=env, check=True)
