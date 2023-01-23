"""
    CurveFitting/tests/test_plotting.py

"""
import pytest
import plotly.graph_objects as go

from CurveFitting.plotting import Plotting
from ._setup import good_line


plot = Plotting(good_line)


@pytest.mark.parametrize("plotting", [
    plot
])
def test_qq_plot(plotting):
    figure = plotting.qqplot()
    assert isinstance(figure, go.Figure)


@pytest.mark.parametrize("plotting", [
    plot
])
def test_fit(plotting):
    figure = plotting.fit()
    assert isinstance(figure, go.Figure)


@pytest.mark.parametrize("plotting", [
    plot
])
def test_residuals(plotting):
    figure = plotting.residuals()
    assert isinstance(figure, go.Figure)


@pytest.mark.parametrize("plotting", [
    plot
])
def test_predicted(plotting):
    figure = plotting.predicted()
    assert isinstance(figure, go.Figure)
