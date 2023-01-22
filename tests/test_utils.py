"""
    CurveFitting/tests/test_utils.py

"""
import pytest
import numpy as np
from CurveFitting import utils


@pytest.mark.parametrize("std, p, expected", [
    (1.0, 0.95, 1.95996),
    (1.0, 0.90, 1.64485),
    (1.0, 0.99, 2.575829),
    (1.0, 0.999, 3.290526),
])
def test_ci(std, p, expected):
    result = utils.ci_x(std, p)
    assert np.isclose(result, expected, rtol=1e-5)


@pytest.mark.parametrize("x, m, b, expected", [
    (1, 1, 5, 6),
    (np.arange(3), 1, 5, np.array([5, 6, 7])),
])
def test_line(x, m, b, expected):
    result = utils.line(x, m, b)
    assert np.array_equal(result, expected)


@pytest.mark.parametrize("x, y, expected", [
    (np.arange(3), np.arange(3), np.array([1, 0])),
    (np.arange(5, 9), np.arange(4), np.array([1, -5])),
    (np.arange(3, 7), np.linspace(0.5, 2.0, 4, True), np.array([0.5, -1])),
])
def test_linalg(x, y, expected):
    result = utils.regression(x, y)
    assert np.alltrue(np.isclose(result, expected))
