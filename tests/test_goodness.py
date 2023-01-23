"""
    CurveFitting/tests/test_goodness.py

"""
import pytest
import numpy as np
from ._setup import good_line


@pytest.mark.parametrize("good, k", [
    (good_line, 2),
])
def test_dofk(good, k):
    assert good.dof == len(good.ydata) == len(good.xdata)
    assert good.k == k


@pytest.mark.parametrize("good, expected", [
    (good_line, np.array([2., -1])),
])
def test_fit(good, expected):
    good.fit()
    assert np.alltrue(np.isclose(good.best_fit, expected))
