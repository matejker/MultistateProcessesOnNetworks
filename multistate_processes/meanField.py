import numpy as np
from scipy.special import factorial
from network import Network
from multistate_processes.calculate import CalculateProcess
from multistate_processes.process import MultistateProcess

"""
n - number of states in the process
m - an (n) array of number of neighbors in each state
  - m_i = number of neighbors in state i 

t - time in [0, T], T > 0 
  - 0 = t_0 < t_1 < ... < t_w = T
  - t_{i+1} - t_i = delta_t  

x^_{k,i}(t) - fraction of nodes of degree k in state i in time t
x - (w x n x k_max) matrix where (x)_{t,k,i} = x_k^i(t) 

omega^j(t) - \sum_{k = 1}^k_{max} \frac{k*p_k}{<k>} x^j_k(t)
mult_k(t, m) - \frac{k!}{m_0!...m_{n-1}}(\omega^0(t))^m_0 * ... * (\omega^{n-1}(t))^{m_{n-1}}
"""

class MeanField(CalculateProcess):
    def __init__(self, network: Network, process: MultistateProcess, t_max, x):
        super().__init__(network, process, t_max)
        self.x = x


    def omegas(self, t):  # TODO: think about powerlaw, instead degree_distribution use alpha
        return (np.arange(1, self.network.k_max + 1) * self.network.degree_distribution) @ self.x[t].T / self.network.mean_degree


    def mult(self, k, m, omegas):
        m_factorial_product = factorial(m).prod()
        k_factorial = factorial(k)
        omegas = omegas

        omega_product = np.power(omegas, m).prod()

        return (k_factorial * omega_product) / m_factorial_product

    def __next__(self):
        if self.t > self.t_max:
            return self.x[self.t]

        for i, d in enumerate(self.network.degree_distribution):
            if d == 0:
                # Skipping degrees with no representant node
                continue

            k = i + 1
            self.x[self.t + 1].T[i] = self.x[self.t].T[i]
            omegas = self.omegas(self.t)
            omegas_no_zeros = (omegas == 0) * 1. + omegas
            ms = self.get_ms_for(k)

            for m in ms:
                rate_matrix = self.process.R(m) - self.process.F(m).T
                self.x[self.t + 1].T[i] -= rate_matrix * self.mult(k, m, omegas_no_zeros) @ self.x[self.t].T[i]

        self.t += 1
        return self.x[self.t]
