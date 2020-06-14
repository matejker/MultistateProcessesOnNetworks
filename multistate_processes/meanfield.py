import numpy as np
from scipy.special import factorial
from network import Network
from multistate_processes.calculate import CalculateProcess
from multistate_processes.process import MultistateProcess


class MeanField(CalculateProcess):
    """Mean Field is the most relaxed, therefore, the most rough estimate of the dynamical process within the three
    approximation frameworks. Where we assume that the states of each node in the network are independent.

    Object attributes:
        children of object CalculateProcess
        x (np.array): a matrix (t_max x n x k_max) where x[t][i][k] is the expected fraction of k-degree nodes in state i
        at time t

    To use:
        >>> network = Network(3, [(0, 1), (2, 1)])
        >>> process = MultistateProcess(np.array([['0', '1'], ['0', '0']]))
        >>> x = np.zeros((10, 2, 2))
        >>> x[0] = np.array([[1, 0], [0, 1]])
        >>> calculate = MeanField(network, process, 10, x)
        >>> iteration = iter(calculate)
        >>> next(iteration)
        array([[0., 0.], [1., 1.]])
    """
    def __init__(self, network: Network, process: MultistateProcess, t_max, x):
        super().__init__(network, process, t_max)
        self.x = x


    def omegas(self, t):  # TODO: think about powerlaw, instead degree_distribution use alpha
        """Probability that the neighbor of a node is in state j at time t.
        \omega^j(t)=\sum_{k=0}^{\infty}\frac{kp_k}{<k>}x^j_k(t)

        Args:
            t (integer): a time step

        Returns:
            (np.array): omega for each state at time t
        """
        return (np.arange(1, self.network.k_max + 1) * self.network.degree_distribution) @ self.x[t].T / self.network.mean_degree


    def mult(self, k, m, omegas):
        """Probability that a k-degree node has m-neighbor in various states at time t.
        Mult_k(m,t)=\frac{k!}{m_0!...m_{n-1}!}(\omega^0(t))^{m_0}...(\omega^{n-1}(t))^{m_{n-1}}

        Args:
            k (integer): degree (1, k_max)
            m (list): neighbor's states
            omegas (np.array): a vector (n x 1) of omegas at time t

        Returns:
            mult (float): probability that a k-degree node has m-neighbor in various states at time t
        """
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

            # However, it doesn't make sense to consider nodes with degree 0 (they don't have any effect on the process)
            # Therefore, k_min = 1 which is index as 0
            k = i + 1
            self.x[self.t + 1].T[i] = self.x[self.t].T[i]
            omegas = self.omegas(self.t)

            # If omega is 0 (the probability is 0), it would mean that Mult would be zero as well
            # Therefore, using (0)^n := 1, for all integers
            omegas_no_zeros = (omegas == 0) * 1. + omegas
            ms = self.get_ms_for(k)

            for m in ms:
                rate_matrix = self.process.R(m) - self.process.F(m).T
                self.x[self.t + 1].T[i] -= rate_matrix * self.mult(k, m, omegas_no_zeros) @ self.x[self.t].T[i]

        self.t += 1
        return self.x[self.t]
