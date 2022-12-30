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
    return x * m + b


def ci_x(std, x: float):
    """Return the Confidence Interval at X Percent"""
    assert 0 <= x <= 1.0
    population = x + (1 - x) / 2
    return norm.ppf(population) * std


def linalg(x: np.ndarray, y: np.ndarray, z: Optional[np.ndarray] = None):
    if z is None:
        z = np.ones(x.shape)
    j = np.vstack((x, z)).T
    params = np.linalg.lstsq(j, y, None)[0]
    return params
