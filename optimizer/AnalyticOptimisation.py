import numpy as np
import pandas as pd
from .PortfolioOptimisation import PortfolioOptimisation

class AnalyticOptimisation(PortfolioOptimisation):
    '''Portfolio Optimizer solving mean variance optimization'''
    def __init__(self):
        super().__init__()
        self._name = 'AnalyticOptimizer'  

    def set_objective(self, alpha, cov, gamma):
        super().set_objective(alpha, cov, gamma)
        self._Vinv = (0.5/self._gamma) * np.linalg.inv(self._cov)  

    def set_constraints(self, constraints):
        super().set_constraints(constraints)
        A=[]
        b=[]
        for constraint_type in constraints.keys():
            constraint_value = constraints[constraint_type]
            if constraint_type == 'min_weight':
                self._lb = constraint_value 
            elif constraint_type == 'max_weight':
                self._ub = constraint_value 
            elif constraint_type == 'sum_weights':
                A.append(np.ones(shape=(1, self._nassets)))
                b.append(np.array([[constraint_value]]))
            elif constraint_type == 'factor_constraint':
                A.append(constraint_value[0])
                b.append(constraint_value[1])
        self._constraints = [ np.concatenate(A, axis=0),
                              np.concatenate(b, axis=0)]

    def __solve(self, A, b):
        P = np.linalg.inv(A @ self._Vinv @ A.T) @ (A @ self._Vinv @ self._alpha - b)
        w =  (self._Vinv @ (self._alpha - A.T @ P))
        return w


    def solve(self, maxiter=15):
        self._weights = self.__solve(self._constraints[0], self._constraints[1])
        w = self._weights.reshape(1,-1)[0]
        # print('w ', w)
        _lb_idx = np.argwhere(w < self._lb).reshape(1,-1)[0]
        _ub_idx = np.argwhere(w > self._ub).reshape(1,-1)[0]
        # print('lower bounds', _lb_idx)
        # print('upper bounds', _ub_idx)
        n_iter = 1
        while ( ( len(_lb_idx) > 0 ) or (len(_ub_idx) > 0) ):
            # print('iteration ', n_iter)
            A = [self._constraints[0]]
            b = [self._constraints[1]]
            if len(_lb_idx) > 0:
                for idx in _lb_idx:
                    _A = np.zeros(shape=(1, self._nassets))
                    _A[0,idx] = 1.0
                    A.append(_A)
                    b.append(np.array([[self._lb]]))
            if len(_ub_idx) > 0:
                for idx in _ub_idx:
                    _A = np.zeros(shape=(1, self._nassets))
                    _A[0,idx] = 1.0
                    A.append(_A)
                    b.append(np.array([[self._ub]]))
            A = np.concatenate(A, axis=0)
            b = np.concatenate(b, axis=0)
            # print('new A', A)
            # print('new b', b)
            w = self.__solve(A, b)
            # print('new w', w)
            _lb_idx = np.argwhere(w < self._lb).reshape(1,-1)[0]
            _ub_idx = np.argwhere(w > self._ub).reshape(1,-1)[0]
            # print('new lower bounds', len(_lb_idx) )
            # print('new upper bounds', len(_ub_idx) )         
            n_iter += 1
            if (n_iter >= maxiter):
                break
        self._weights = np.clip(w, self._lb, self._ub)