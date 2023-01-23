"""
    CurveFitting/tests/_setup.py

"""
import numpy as np

from CurveFitting.goodness_of_fit import Goodness
from CurveFitting.utils import line

good_line = Goodness(
    function=line,
    xdata=np.arange(5),
    ydata=np.arange(5) * 2 - 1,
)
good_line.fit()
