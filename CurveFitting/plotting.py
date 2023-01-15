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
    CurveFitting/plotting.py

"""
# Python Dependencies
import numpy as np

from typing import List, Optional

from plotly import express as px
from plotly import graph_objects as go

from . import utils
from .core import Equation
from .goodness_of_fit import Goodness


class Plotting:
    def __init__(self, good: Goodness):
        self.good = good

    def qqplot(self, color: Optional[str] = None) -> go.Figure:
        return qqplot(self.good, color)

    def fit(self, color: Optional[str] = None, name: str = "f(p)") -> go.Figure:
        return plot_fit(self.good, color, name)

    def residuals(self, color: Optional[str] = None) -> go.Figure:
        return plot_residuals(self.good, color)

    def predicted(self, color: Optional[str] = None) -> go.Figure:
        return plot_predicted(self.good, color)

    def fit_all(self, equation: Equation, colors: Optional[List[str]] = None) -> go.Figure:
        if colors is None:
            colors = px.colors.qualitative.Prism[:]
        assert len(colors) >= 4, "Must provide at least four colors."
        figure = self.fit(colors[0], "f(p)")
        setup = zip(
            [equation.derivative, equation.second_derivative, equation.integral],
            [u"&#8706;f(p)", u"&#8706;&#8706;f(p)", u"&#x222b; f(p)"]
        )
        previous = self.good.function

        for n, (eq, name) in enumerate(setup, 1):
            self.good.function = eq
            _trace_fit(figure, self.good, colors[n], name)
            _plot_error(figure, self.good, colors[n], name)

        # Reset
        self.good.function = previous

        return figure


def qqplot(good: Goodness, color: str = "#579677"):
    """Renders a Quantile-Quantile (QQ) Plot as a diagnostic QC tool for underlying fit."""
    # Preparation
    observed_rsd = good.dfm / good.ydata.std()
    expect = good.expected
    predicted_rsd = (expect - expect.mean()) / expect.std()
    figure = go.Figure()

    figure.add_trace(go.Scatter(
        name="Quantile-Quantile",
        x=observed_rsd,
        y=predicted_rsd,
        mode="markers",
        marker=dict(
            color=color,
            size=4.5,
        )
    ))

    figure.add_trace(go.Scatter(
        name="fit",
        mode="lines",
        x=observed_rsd,
        y=utils.line(observed_rsd, *utils.regression(observed_rsd, predicted_rsd)),
        line=dict(
            color=color,
            shape="spline",
            dash="dot",
            width=1.25,
        ),
    ))

    figure.update_layout(
        title="Quantile-Quantile (QQ) Plot",
        xaxis_title="Observed RSD",
        yaxis_title="Expected RSD",
        font=dict(
            family="times",
            size=12
        )
    )

    return figure


def _trace_fit(figure: go.Figure, good: Goodness, color: str, name: str):
    # For presentation purposes (due to the nature of splining), use more p values
    x = np.linspace(
        np.nanmin(good.xdata),
        np.nanmax(good.xdata),
        1_000
    )

    figure.add_trace(go.Scatter(
        name=f"{name} - Fit",
        mode="lines",
        x=x,
        y=good.expect(x),
        line=dict(
            color=color,
            shape="spline",
            dash="dot"
        ),
    ))


def _plot_error(figure: go.Figure, good: Goodness, color: str, name: str):
    x = np.linspace(
        np.nanmin(good.xdata),
        np.nanmax(good.xdata),
        1_000
    )
    error_95ci = utils.ci_x(good.std, 0.95)

    figure.add_trace(go.Scatter(
        name=f"{name} - Error",
        mode="lines",
        x=np.concatenate((x, x[::-1])),
        y=np.concatenate((
            good.function(x, *(good.best_fit + error_95ci)),
            good.function(x[::-1], *(good.best_fit - error_95ci)),
        )),
        line=dict(
            color=color,
            dash="dot",
            width=0.5,
        ),
        fill="toself",
        opacity=0.5,
    ))


def plot_fit(good: Goodness, color: str = "rgb(29, 105, 150)", name: str = "f(p)"):
    figure = go.Figure()

    figure.add_trace(go.Scatter(
        name="Data",
        mode="markers",
        x=good.xdata,
        y=good.ydata,
        error_y=dict(
            type="data",
            array=good.yerror,
            color=color,
            thickness=1.0,
            width=1.75,
        ),
        marker=dict(
            color=color
        ),
    ))

    _trace_fit(figure, good, color, name)
    _plot_error(figure, good, color, name)

    figure.update_layout(
        xaxis=dict(title="X"),
        yaxis=dict(title="Y"),
        font=dict(
            family="Times",
            size=12,
        )
    )

    return figure


def plot_residuals(good: Goodness, color: str = "rgb(56, 166, 165)"):
    """Plots the Residuals of a Curve Fit Best Parameters."""
    figure = go.Figure()
    x, y = good.xdata, good.residuals

    figure.add_trace(go.Scatter(
        name="data",
        mode="markers",
        x=x,
        y=y,
        error_y=dict(
            type="data",
            array=good.yerror,
            color=color,
            thickness=1.0,
            width=1.75,
        ),
        marker=dict(
            color=color,
            size=4.5,
        ),
    ))

    if good.yerror is not None:
        z = utils.weights(good.yerror)
    else:
        z = None

    figure.add_trace(go.Scatter(
        name="fit",
        mode="lines",
        x=x,
        y=utils.line(x, *utils.regression(x, y, z)),
        line=dict(
            color=color,
            shape="spline",
            dash="dot",
            width=1.25,
        ),
    ))

    figure.update_layout(
        xaxis=dict(title="X"),
        yaxis=dict(title="Residuals"),
        font=dict(
            family="Times",
            size=12,
        )
    )

    return figure


def plot_predicted(good: Goodness, color: str = "rgb(56, 166, 165)"):
    """Plots Predicted"""
    figure = go.Figure()

    x, y = good.ydata, good.expected

    figure.add_trace(go.Scatter(
        name="data",
        mode="markers",
        x=x,
        y=y,
        error_x=dict(
            type="data",
            array=good.yerror,
            color=color,
            thickness=1.0,
            width=1.75,
        ),
        marker=dict(
            color=color,
            size=4.0,
        ),
    ))

    figure.add_trace(go.Scatter(
        name="fit",
        mode="lines",
        x=x,
        y=utils.line(x, *utils.regression(x, y)),
        line=dict(
            color=color,
            shape="spline",
            dash="dot",
            width=0.5
        ),
    ))

    figure.update_layout(
        xaxis=dict(title="Observed Values"),
        yaxis=dict(title="Anticipated Values"),
        font=dict(
            family="Times",
            size=12,
        )
    )

    return figure
