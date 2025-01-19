import numpy as np
import pandas as pd
from .PortfolioOptimisation import PortfolioOptimisation
import cvxpy as cp

class CVXOptimisation(PortfolioOptimisation):
    '''Portfolio Optimizer solving mean variance optimization'''
    def __init__(self):
        super().__init__()
        self._name = 'CVXOptimizer'
        self._verbose = False

    def set_verbosity(self, val):
        self._  

    def set_objective(self, alpha, cov, gamma):
        super().set_objective(alpha, cov, gamma)
        self._w = cp.Variable((self._nassets,1))
        gamma = cp.Parameter(nonneg=True)
        gamma.value = self._gamma
        self._ret = self._alpha.T @ self._w
        self._risk = cp.quad_form(self._w, self._cov)
        self._objective = cp.Maximize(self._ret - gamma * self._risk)

    def set_constraints(self, constraints):
        super().set_constraints(constraints)
        for constraint_type in constraints.keys():
            constraint_value = constraints[constraint_type]
            if constraint_type == 'min_weight':
                self._lb = constraint_value 
                self._constraints.append(self._w >= self._lb)
            elif constraint_type == 'max_weight':
                self._ub = constraint_value 
                self._constraints.append(self._w <= self._ub)
            elif constraint_type == 'sum_weights':
                self._constraints.append(cp.sum(self._w) == constraint_value)
            elif constraint_type == 'factor_constraint':
                A  = constraint_value[0]
                lb = constraint_value[1]
                ub = constraint_value[2]
                if np.all(lb == ub):
                    self._constraints.append(A @ self._w == ub)
                else:
                    self._constraints.append(A @ self._w <= ub)
                    self._constraints.append(lb <= A @ self._w)

    def solve(self):
        self._problem = cp.Problem(self._objective, self._constraints)
        self._problem.solve(solver=cp.SCS, verbose=self._verbose)
        self._weights = self._w.value