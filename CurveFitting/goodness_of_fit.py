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
    CurveFitting/goodness_of_fit.py

"""
# Python Dependencies
import warnings

import numpy as np

from typing import Callable, Optional
from inspect import getfullargspec
from scipy.optimize import curve_fit


class Goodness:
    """Goodness of Fit

    Args:
        function (Callable): function describing data
        xdata (np.ndarray): Observed X Values
        ydata (np.ndarray): Observed Y Values
        yerror (np.ndarray): Observed Error (standard deviation) in Y Values
        best_fit (np.ndarray): Best Fit parameters for the given function and data
        covariance (np.ndarray): Covariance Matrix

    Assumptions:
        The first argument of the provided function must accept xdata

    """
    def __init__(self,
                 function: Callable,
                 xdata: np.ndarray,
                 ydata: np.ndarray,
                 yerror: Optional[np.ndarray] = None,
                 best_fit: Optional[np.ndarray] = None,
                 covariance: Optional[np.ndarray] = None
                 ) -> None:
        # Instance Args
        self.function = function
        self.xdata = xdata
        self.ydata = ydata
        self.yerror = yerror

        assert xdata.shape == ydata.shape, f"X and Y Data Must Be the Same Shape."

        self.best_fit = best_fit
        self.covariance = covariance

    def fit(self, **kwargs) -> None:
        """Fits the data to a given function."""
        try:
            self.best_fit, self.covariance = curve_fit(
                f=self.function,
                xdata=self.xdata,
                ydata=self.ydata,
                sigma=self.yerror,
                **kwargs
            )

        except RuntimeError:
            warnings.warn("Data Failed to be Fit using: %s" % self.function.__name__)
            size = self.k
            self.best_fit = np.array([np.nan] * size)
            self.covariance = np.array([np.nan] * size * size).reshape((size, size))

    @property
    def parameters(self) -> np.ndarray:
        """Parameter names of a Given Function."""
        return np.asarray(getfullargspec(self.function).args[1:])

    @property
    def std(self) -> np.ndarray:
        """Standard Deviation (std) of Best Fit Parameters."""
        return np.sqrt(self.covariance.diagonal())

    @property
    def expected(self) -> np.ndarray:
        """Expected Value given best fit parameters."""
        return self.function(self.xdata, *self.best_fit)

    @property
    def residuals(self) -> np.ndarray:
        """Residual Difference between Observed and Expected."""
        return self.ydata - self.expected

    @property
    def ssr(self) -> float:
        """Sum of Squared Residuals (SSR)"""
        return np.power(self.residuals, 2).sum()

    @property
    def dfm(self) -> np.ndarray:
        """Distance from the Mean"""
        return self.ydata - self.ydata.mean()

    @property
    def sse(self) -> float:
        """Sum of Squared Error (SSE)."""
        return np.power(self.dfm, 2).sum()

    @property
    def dof(self) -> int:
        """Degrees of Freedom (DOF), n"""
        return len(self.ydata)

    @property
    def k(self) -> int:
        """Number of Parameters, k"""
        return len(self.parameters)

    @property
    def rmse(self) -> float:
        """Root Mean Squared Error (RMSE)"""
        return (self.ssr / self.dof) ** 0.5

    @property
    def syx(self) -> float:
        """Alternative Form of RMSE, modifying degrees of freedom by number of fit variables"""
        return (self.ssr / (self.dof - self.k)) ** 0.5

    @property
    def rsq(self) -> float:
        """Pearson's Correlation Coefficient, R-Squared"""
        return 1.0 - (self.ssr / self.sse)

    @property
    def rsq_adj(self) -> float:
        """Adjusted R-Squared Value"""
        return (1 - self.rsq) * (self.dof - 1.0) / (self.k - 1.0)

    def report(self) -> dict:
        """Prepares a Report of Goodness of Fit Metrics."""

        return {
            "Variables": self.parameters,
            "Fit": self.best_fit,
            "StDev": self.std,
            "SSR": self.ssr,
            "SyX": self.syx,
            "SSE": self.sse,
            "RMSE": self.rmse,
            "RSQ": self.rsq,
            "RSQ (Adjusted)": self.rsq_adj,
            "Equation": self.function.__name__,
        }
