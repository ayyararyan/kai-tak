import itertools
import math
import numpy as np
import pytest
from prerequisites import *

def test_dimension_semantics():
    p=wheel_plan();assert len(p)==18 and len({v['id'] for v in p})==18
    assert all(v['z_m'] is None for v in p)
    wing=[v for v in p if v['gear']=='wing']; body=[v for v in p if v['gear']=='body']
    assert np.mean([v['aft_m'] for v in wing])==pytest.approx(24.0665)
    assert np.mean([v['aft_m'] for v in body])==pytest.approx(27.1399)
    assert max(v['right_m'] for v in wing)-min(v['right_m'] for v in wing)==pytest.approx(12.1158)
    # 19-inch tyre width adds to outer centre span; agrees 41ft4in within source rounding.
    assert abs((12.1158+19*INCH)-(41*12+4)*INCH) < .001
    assert {v['aft_m'] for v in wing}=={(947.5-29)*INCH,(947.5+29)*INCH}

def test_cg_mass_moment():
    for f in [-10,0,27.1,50,100]:
        c=landing_cg_percent_mac(f)
        assert 525718*c==pytest.approx(476116*27.1+49602*f)
    assert landing_cg_percent_mac(27.1)==pytest.approx(27.1)
    assert landing_cg_percent_mac(10)-landing_cg_percent_mac(0)==pytest.approx(10*49602/525718)

def test_all_known_spoiler_commands():
    # Independent set-of-allowed-inputs oracle, exhaustive 96 state/input combinations.
    for pos in ['DN','ARM','UP']:
        for row in itertools.product([False,True],repeat=5):
            g,a,b,c,d=row
            if not g: expected='none'
            elif pos=='DN':expected='raise' if a==b==True and (c or d) else 'none'
            elif pos=='ARM':expected='raise' if a==b==True else 'none'
            else:expected='none' if a==b==True else 'lower'
            assert spoiler_command(pos,*row)==expected

def test_unknowns_are_not_false():
    assert spoiler_command('ARM',None,True,True,False,False)=='unknown'
    assert spoiler_command('ARM',False,None,None,None,None)=='none'
    assert spoiler_command('UP',True,False,None,None,None)=='lower'
    assert reverse_selection_permitted(None,True) is None
    assert reverse_selection_permitted(False,None) is False
    assert autobrake_activation_prerequisites(True,True,True,True,None,True,True) is None
    assert spoiler_command('ARM',True,True,True,False,False)=='raise'
    assert autobrake_activation_prerequisites(True,True,True,True,False,True,True) is False

def test_deforming_point_against_finite_difference():
    # Exact analytic trajectory, independent position differencing; changing strut
    # length makes the Coriolis term nonzero and a missing term fail the test.
    w=.7
    def sample(t):
        R=np.array([[math.cos(w*t),-math.sin(w*t),0],[math.sin(w*t),math.cos(w*t),0],[0,0,1]])
        b=np.array([2+t+.3*t*t,.4*t,-3+.1*t*t])
        cg=np.array([.5*t*t,2*t,5-.2*t*t])
        return cg+R@b,R,b,cg
    t=.4;h=1e-4;pos,R,b,cg=sample(t)
    p,v,a=deforming_point_kinematics(cg,[t,2,-.4*t],[1,0,-.4],R,[0,0,w],[0,0,0],b,[1+.6*t,.4,.2*t],[.6,0,.2])
    np.testing.assert_allclose(p,pos,atol=1e-12)
    np.testing.assert_allclose(v,(sample(t+h)[0]-sample(t-h)[0])/(2*h),atol=1e-7)
    np.testing.assert_allclose(a,(sample(t+h)[0]-2*pos+sample(t-h)[0])/(h*h),atol=2e-7)

def test_point_plane_contact_distinction():
    obs=plane_observation([0,0,0],[0,0,-.7],[0,0,2],0)
    assert obs==dict(gap_m=0.,normal_speed_mps=-.7) # pre-impact is not sustained contact
    assert plane_observation([0,0,-.1],[0,0,0],[0,0,1],0)['gap_m']<0

@pytest.mark.parametrize('bad',[float('nan'),float('inf')])
def test_nonfinite_refusal(bad):
    with pytest.raises(ValueError):landing_cg_percent_mac(bad)
    with pytest.raises(ValueError):plane_observation([0,0,bad],[0,0,0],[0,0,1],0)

def test_missing_reference_refusal():
    with pytest.raises(ValueError):deforming_point_kinematics([0,0,0],[0,0,0],[0,0,0],np.eye(3),[0,0,0],[0,0,0],[0,0,None],[0,0,0],[0,0,0])
    with pytest.raises(ValueError):deforming_point_kinematics([0,0,0],[0,0,0],[0,0,0],np.diag([-1,1,1]),[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0])
    with pytest.raises(ValueError):spoiler_command('ARM',1,True,True,False,False)
