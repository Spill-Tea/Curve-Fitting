# MIT License
#
# Copyright (c) 2022 Spill-Tea
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
    CurveFitting/utils.py

"""
# Python Dependencies
import numpy as np

from typing import Optional
from scipy.stats import norm


def line(x, m, b):
    """Simple Linear Equation"""
    return x * m + b


def ci_x(std, p: float):
    """Return the Confidence Interval at the specified percentage, p"""
    assert 0 <= p <= 1.0
    population = p + (1 - p) / 2
    return norm.ppf(population) * std


def weights(a: np.ndarray) -> np.ndarray:
    """Convert the error into a weighting paradigm"""
    alpha = np.nanmax(a) - a
    omega = 1 - np.exp(- alpha / np.max(alpha) - 1)
    return np.power(omega / omega.max(), 2)


def regression(x: np.ndarray, y: np.ndarray, z: Optional[np.ndarray] = None):
    """Linear Regression weighted by z, defaulting to equal weights."""
    if z is None:
        z = np.ones(x.shape)
    j = np.vstack((x, z)).T
    params = np.linalg.lstsq(j, y, None)[0]
    return params
