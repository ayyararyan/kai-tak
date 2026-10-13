import pytest
from .solve import validation_samples, sensitivity_cases, optimize
from .trajectory import load_config, validate_config


def test_dense_mesh_is_strict_refinement():
    for n in (5,121,1201,2401):
        assert validation_samples(n)>n
        assert validation_samples(n)>=10*(n-1)+1


def test_custom_crosswind_stresses_are_perturbations():
    cfg=load_config();cfg['parameters']['wind_mps']['value']=[8,3,1]
    cases=sensitivity_cases(validate_config(cfg))
    assert cases[0][2]==[8,8,1]
    assert cases[1][2]==[8,-2,1]


@pytest.mark.parametrize('n,maxiter',[(4,180),(121,0),(121,1.2),(5.2,180)])
def test_solver_rejects_invalid_discretization(n,maxiter):
    with pytest.raises(ValueError):optimize(load_config(),n,maxiter)
