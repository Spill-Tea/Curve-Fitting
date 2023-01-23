"""
    CurveFitting/tests/test_goodness.py

"""
import pytest
import numpy as np

from CurveFitting.goodness_of_fit import Goodness
from CurveFitting.utils import line


@pytest.mark.parametrize("x, y, f, expected", [
    (np.arange(5), np.arange(5) * 2 - 1, line, np.array([2., -1])),
])
def test_dofk(x, y, f, expected):
    good = Goodness(
        function=f,
        xdata=x,
        ydata=y,
    )
    assert good.dof == len(y) == len(x)
    assert good.k == len(expected)


@pytest.mark.parametrize("x, y, f, expected", [
    (np.arange(5), np.arange(5) * 2 - 1, line, np.array([2., -1])),
])
def test_fit(x, y, f, expected):
    good = Goodness(
        function=f,
        xdata=x,
        ydata=y,
    )
    good.fit()

    assert np.alltrue(np.isclose(good.best_fit, expected))
