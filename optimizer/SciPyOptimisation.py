from scipy.optimize import minimize, Bounds, LinearConstraint
import numpy as np
import pandas as pd
from .PortfolioOptimisation import PortfolioOptimisation


class SciPyOptimisation(PortfolioOptimisation):
    '''Portfolio Optimizer solving mean variance optimization'''
    def __init__(self):
        super().__init__()
        self._name = 'SciPyOptimizer'
        

    def set_objective(self, alpha, cov, gamma):
        super().set_objective(alpha, cov, gamma)
        self._objective = lambda w:  - (np.dot(np.transpose(w), self._alpha) - self._gamma * np.dot(np.dot(np.transpose(w), self._cov), w))
    
    def set_constraints(self, constraints):
        super().set_constraints(constraints)
        for constraint_type in constraints.keys():
            constraint_value = constraints[constraint_type]
            if constraint_type == 'min_weight':
                self._lb = constraint_value 
            elif constraint_type == 'max_weight':
                self._ub = constraint_value 
            elif constraint_type == 'sum_weights':
                constr = LinearConstraint(np.ones(shape=(1,self._nassets)), lb=[constraint_value], ub=[constraint_value])
                self._constraints.append(constr)
            elif constraint_type == 'factor_constraint':
                constr = LinearConstraint(constraint_value[0], lb=[constraint_value[1]], ub=[constraint_value[2]])
                self._constraints.append(constr)
        if self._lb is None:
            self._lb = -np.inf
        if self._ub is None:
            self._ub = np.inf
        self._bounds = Bounds(lb=self._lb, ub=self._ub)

    def solve(self):
        initial_guess = self._weights
        self._res = minimize(self._objective, initial_guess, method='SLSQP', 
                             bounds=self._bounds, constraints=self._constraints, options={'maxiter':5000, 'disp': False})
        self._weights = self._res.x