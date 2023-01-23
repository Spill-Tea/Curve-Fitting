"""
    CurveFitting/tests/test_expressions.py

"""
import pytest
from CurveFitting import expressions as ex


@pytest.mark.parametrize("exp, variables", [
    (ex.Gaussian, [ex.x]),
    (ex.Poisson, [ex.x]),
    (ex.Parabola, [ex.x]),
    (ex.PadeApproximant, [ex.x]),
    (ex.OneSiteSpecificBinding, [ex.x]),
])
def test_variables(exp: ex.Expression, variables: list):
    assert exp.variables == variables


@pytest.mark.parametrize("exp, constants", [
    (ex.Gaussian, [ex.mu, ex.sigma]),
    (ex.Poisson, [ex.mu]),
    (ex.Parabola, [ex.a, ex.b, ex.c]),
    (ex.PadeApproximant, [ex.A0, ex.A1, ex.B1]),
    (ex.OneSiteSpecificBinding, [ex.Bmax, ex.Kd]),
])
def test_constants(exp: ex.Expression, constants: list):
    assert exp.constants == constants


@pytest.mark.parametrize("exp, args", [
    (ex.Gaussian, [ex.x, ex.mu, ex.sigma]),
    (ex.Poisson, [ex.x, ex.mu]),
    (ex.Parabola, [ex.x, ex.a, ex.b, ex.c]),
    (ex.PadeApproximant, [ex.x, ex.A0, ex.A1, ex.B1]),
    (ex.OneSiteSpecificBinding, [ex.x, ex.Bmax, ex.Kd]),
])
def test_args(exp: ex.Expression, args: list):
    assert exp.args == args


@pytest.mark.parametrize("exp, names", [
    (ex.Gaussian, ["x", "mu", "sigma"]),
    (ex.Poisson, ["x", "mu"]),
    (ex.Parabola, ["x", "a", "b", "c"]),
    (ex.PadeApproximant, ["x", "A0", "A1", "B1"]),
    (ex.OneSiteSpecificBinding, ["x", "Bmax", "Kd"]),
])
def test_names(exp: ex.Expression, names: list):
    assert exp.names == names
