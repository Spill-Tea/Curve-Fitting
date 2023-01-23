"""
    CurveFitting/tests/test_expressions.py

"""
import pytest

from CurveFitting.core import Equation
from CurveFitting import expressions as ex


@pytest.mark.parametrize("expression", [
    ex.Gaussian,
    ex.PadeApproximant,
    ex.VariableSlopeDoseResponse,
    ex.Poisson,
])
def test_equation(expression):
    eq = Equation(expression)

    assert callable(eq.equation)
    assert callable(eq.derivative)
    assert callable(eq.second_derivative)
    assert callable(eq.integral)
