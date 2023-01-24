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
    CurveFitting/core.py

"""
# Python Dependencies
import sympy as sm
from typing import List, Optional

from .expressions import Expression


class Equation:
    """Class to Handle Conversion to Derivative and Integral.

    Args:
        expression (Expression): Expression Class Interface
        backend (List[str]): Backend Modules used to evaluate the expression into a function.

    References:
        1. https://docs.sympy.org/latest/modules/utilities/lambdify.html

    """
    __slots__ = (
        "expression",
        "equation",
        "derivative_expression",
        "derivative",
        "second_derivative_expression",
        "second_derivative",
        "integral_expression",
        "integral",
    )

    def __init__(self, expression: Expression, backend: Optional[List[str]] = None):
        self.expression = expression
        self.equation = sm.lambdify(expression.args, expression.expression, backend)
        self.equation.__doc__ = sm.latex(expression.expression)

        self.derivative_expression = sm.Derivative(
            expression.expression, *expression.variables, evaluate=True
        )
        self.derivative = sm.lambdify(
            expression.args,
            self.derivative_expression,
            backend
        )
        self.derivative.__doc__ = sm.latex(self.derivative_expression)

        self.second_derivative_expression = sm.Derivative(
            self.derivative_expression, *self.expression.variables, evaluate=True
        )
        self.second_derivative = sm.lambdify(
            expression.args,
            self.second_derivative_expression,
            backend
        )
        self.second_derivative.__doc__ = sm.latex(self.second_derivative_expression)

        self.integral_expression = sm.integrate(expression.expression, expression.variables)
        self.integral = sm.lambdify(
            expression.args,
            self.integral_expression,
            backend
        )
        self.integral.__doc__ = sm.latex(self.integral_expression)
