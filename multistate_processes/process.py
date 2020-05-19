import numpy as np
np.set_printoptions(suppress=True)

'''
n - number of states in the whole state
m - an (n) array of number of neighbors in each state
  - m_i = number of neighbors in state i 
F_m - a transition rate (n x n) matrix for the stochastic process with m neighbors
    - (F_m)ij = F_m(i->j) - rate of i -> j with m neighbors
R_m - a diagonal (n x n) matrix 
    - (R_m)ii = \sum_{j=1}^n F_m(i->j)
    
Transition rate matrix F_m defines a whole stochastic process on a network. While a parameter m is unique for each node 
and defines each node. Knowing transition rates and parameter m for each node means to be able to do both - simulate and
count the multistate dynamical process on network.

Example: 
rates = np.array([['0', '({0} + {1})*alpha'], ['{0}*beta', '{0} + {1}']])
F = MultistateProcess(rates, alpha=2, beta=3)
m = np.array([10, 2])
F(m)

>> array([[ 0., 24.],
       [30., 12.]])
'''


class MultistateProcess:
    def __init__(self, rates, **kwargs):
        self.rates = rates
        self.kwargs = kwargs

    def get_transition_rate_matrix(self, m):
        eval_rates = [eval(j.format(*m), self.kwargs) for i in self.rates for j in i]  # TODO: think about lambda
        return np.array(eval_rates).astype(float).reshape(self.rates.shape)

    def __call__(self, m):
        return self.get_transition_rate_matrix(m)

    def R(self, m):
        matrix = self.get_transition_rate_matrix(m)
        return np.diag(matrix.sum(axis=1))
