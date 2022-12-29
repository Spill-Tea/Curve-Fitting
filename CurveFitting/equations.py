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
    CurveFitting/equations.py

"""
# Python Dependencies
import sympy as sm
from typing import List, Union


# Symbols
x = sm.Symbol("x", real=True)
a = sm.Symbol("a", constant=True, real=True)
b = sm.Symbol("b", constant=True, real=True)
c = sm.Symbol("c", constant=True, real=True)
mu = sm.Symbol("c", constant=True, real=True)
sigma = sm.Symbol("c", constant=True, real=True)
baseline = sm.Symbol("baseline", constant=True, real=True)
peak = sm.Symbol("peak", constant=True, real=True)
pEC50 = sm.Symbol("pEC50", constant=True, real=True)
HillSlope = sm.Symbol("HillSlope", constant=True, real=True)
Bmax = sm.Symbol("Bmax", constant=True, real=True)
Kd = sm.Symbol("Kd", constant=True, real=True)
NS = sm.Symbol("NS", constant=True, real=True)
A0 = sm.Symbol("A0", constant=True, real=True)
A1 = sm.Symbol("A1", constant=True, real=True)
B1 = sm.Symbol("B1", constant=True, real=True)
K = sm.Symbol("K", constant=True, real=True)
Y0 = sm.Symbol("Y0", constant=True, real=True)


# Equations
class Expression:
    def __init__(self,
                 expression: Union[sm.core.add.Add, sm.core.mul.Mul, sm.core.mod.Mod],
                 ):
        self.expression = expression
        self._symbols = [*self.expression.free_symbols]

    @property
    def args(self):
        return self.variables + self.constants

    @property
    def names(self) -> List[str]:
        return [j.name for j in self.args]

    @property
    def variables(self) -> List[sm.Symbol]:
        return sorted([i for i in self._symbols if not i._assumptions.get("constant", False)])

    @property
    def constants(self) -> List[sm.Symbol]:
        return sorted([i for i in self._symbols if i._assumptions.get("constant", False)])


VariableSlopeDoseResponse = Expression(
    expression=baseline + (peak - baseline) / (1 + 10 ** ((pEC50 - x) * HillSlope))
)

BoltzmanSigmoidal = Expression(
    expression=baseline + (peak - baseline) / (1 + sm.exp((pEC50 - x) / HillSlope))
)

LogisticGrowth = Expression(
    expression=baseline * peak / ((peak - baseline) * sm.exp(-K * x) + baseline)
)

GompertzGrowth = Expression(
    expression=peak * (baseline / peak) ** sm.exp(-K * x)
)

OneSiteTotalBinding = Expression(
    expression=Bmax * x / (Kd + x) + NS * x + baseline
)

OneSiteSpecificBinding = Expression(
    expression=Bmax * x / (Kd + x)
)

SlopedSpecificBinding = Expression(
    expression=(Bmax * (x ** HillSlope)) / (Kd ** HillSlope + x ** HillSlope)
)

PadeApproximant = Expression(
    expression=(A0 + A1 * x) / (1 + B1 * x)
)

DissociationKinetics = Expression(
    expression=(Y0 - NS) * sm.exp(-K * x) + NS
)

Parabola = Expression(
    expression=a * x ** 2 + b * x + c
)

Poisson = Expression(
    expression=(mu ** x) * sm.exp(-mu) / sm.gamma(x + 1)
)

Gaussian = Expression(
    expression=sm.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * sm.sqrt(2 * sm.pi))
)
