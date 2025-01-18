import numpy as np
import pandas as pd

class PortfolioOptimisation:
    def __init__(self):
        self._name = 'PortfolioOptimizer'
        self._constraints = []
        self._lb = None
        self._ub = None
        self._weights = None

    def set_objective(self, alpha, cov, gamma):
        if isinstance(alpha, pd.DataFrame) or isinstance(alpha, pd.Series):
            self._alpha = alpha.to_numpy()
        elif isinstance(alpha, np.ndarray):
            self._alpha = alpha
        
        if self._alpha.shape[1] != 1:
            raise Exception('need alpha as a nx1 column')           
        self._nassets = self._alpha.shape[0]
        
        if isinstance(cov, pd.DataFrame):
            self._cov = cov.to_numpy()
        elif isinstance(cov, np.ndarray):
            self._cov = cov
        if self._cov.shape != (self._nassets, self._nassets):
            raise Exception('need Covariance as a nxn matrix') 
        self._gamma = gamma
        self.__eye = np.ones(shape=(self._nassets,))

    def set_constraints(self, constraints):
        if not isinstance(constraints, dict):
            raise Exception('constraints need to be a python dictionary') 
        constraint_types = ['min_weight', 'max_weight', 'sum_weights', 'factor_constraint']
        for constraint_type in constraints.keys():
            if constraint_type not in constraint_types:
                raise Exception('constraints {:s} not recognized'.format(constraint_type))
            
    def set_weights(self, w):
        self._weights = w    
    def get_weights(self):
        return self._weights