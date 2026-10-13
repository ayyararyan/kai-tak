import math, unittest
import numpy as np
from diagnose_threshold import build, residual, unit_bearing

class DiagnosisTests(unittest.TestCase):
    def test_reverse_triangle_bound_attained(self):
        # Independent synthetic geometry; bearing-free bound attained along endpoints.
        n=np.array([10.,40.]);s=np.array([310.,-360.]);L=430.
        beta=math.degrees(math.atan2(*(s-n)))
        self.assertAlmostEqual(residual(n,s,beta,L)['norm_m'],70.,places=10)
        for b in np.linspace(-360,360,401):
            self.assertGreaterEqual(residual(n,s,b,L)['norm_m']+1e-10,70.)
    def test_offset_sign_and_lateral_invariance(self):
        a=residual([10,20],[500,-400],131,600)
        b=residual([10,20],[500,-400],131,600,61)
        self.assertAlmostEqual(b['along_m']-a['along_m'],61.)
        self.assertAlmostEqual(b['right_m'],a['right_m'])
    def test_coordinate_rotation_covariance(self):
        n=np.array([4.,5.]);s=np.array([70.,-30.]);angle=.23
        Q=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
        a=residual(n,s,130,73)
        b=residual(Q@n,Q@s,130-math.degrees(angle),73)
        np.testing.assert_allclose([a['along_m'],a['right_m']],[b['along_m'],b['right_m']],atol=1e-12)
    def test_source_residual_reproduction(self):
        r=build()
        self.assertAlmostEqual(r['uncorrected_mapped_axis']['norm_m'],77.6229012827399,places=7)
        self.assertAlmostEqual(r['fitted_endpoint_distance_m'],2863.2762183390105,places=7)
    def test_hypothesis_remains_unaccepted(self):
        r=build()
        self.assertEqual(r['lda_m'],2786)
        self.assertIsNone(r['accepted_threshold_EN_m'])
        self.assertIsNone(r['aviation_to_HKPD_offset_m'])
        self.assertFalse(r['historical_clearance_ready'])
        for name in ['mapped_axis_result','short_axis_result']:
            self.assertFalse(r['concrete_extension_hypothesis'][name]['accepted_historical_registration'])
            self.assertIsNone(r['concrete_extension_hypothesis'][name]['physical_error_bound_m'])
    def test_pythagorean_residual_decomposition(self):
        r=build()
        for v in [r['uncorrected_mapped_axis'],r['concrete_extension_hypothesis']['mapped_axis_result']]:
            self.assertAlmostEqual(v['along_m']**2+v['right_m']**2,v['norm_m']**2,places=7)
    def test_control_influence_not_silently_deleted(self):
        r=build();rows=r['north_fit_leave_one_out']
        self.assertEqual(len(rows),5)
        v=next(x for x in rows if x['omitted']=='seawall_corner')
        self.assertGreater(v['heldout_RMS_m'],100)
        self.assertGreater(v['mismatch_with_uncorrected_south_m'],200)

if __name__=='__main__':unittest.main()
