"""
    CurveFitting/tests/test_goodness.py

"""
import pytest
import numpy as np

from CurveFitting.goodness_of_fit import Goodness


@pytest.mark.parametrize("x, y, f, expected", [
    (np.arange(5), np.arange(5) * 2 - 1, lambda x, m, b: m * x + b, np.array([2., -1])),
])
def test_fit(x, y, f, expected):
    good = Goodness(
        function=f,
        xdata=x,
        ydata=y,
    )
    good.fit()

    assert np.alltrue(np.isclose(good.best_fit, expected))
