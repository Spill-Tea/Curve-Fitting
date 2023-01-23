"""
    CurveFitting/tests/test_expressions.py

"""
import pytest
from CurveFitting import expressions as ex


@pytest.mark.parametrize("exp, names", [
    (ex.Gaussian, ["x", "mu", "sigma"]),
    (ex.Poisson, ["x", "mu"]),
    (ex.Parabola, ["x", "a", "b", "c"]),
    (ex.PadeApproximant, ["x", "A0", "A1", "B1"]),
    (ex.OneSiteSpecificBinding, ["x", "Bmax", "Kd"]),
])
def test_names(exp: ex.Expression, names: list):
    assert exp.names == names


