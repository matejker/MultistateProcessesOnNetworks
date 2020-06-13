from itertools import product
from network import Network
from multistate_processes.process import MultistateProcess

class CalculateProcess:
    """A generic object for calculating multistate dynamical process which is then inherited by one of the generalized
    approximation framework.

    Object attributes:
        network (Network): the network object
        multistate_process (MultistateProcess): object of the multistate process
        t_max (integer): max number (t) of process iterations

    To use:
        >>> network = Network(3, [(0, 1), (2, 1)])
        >>> process = MultistateProcess(np.array([['0', '1'], ['0', '0']]))
        >>> calculate = CalculateProcess(network, process, 100)
        >>> iteration = iter(calculate)
        >>> next(iteration)
        <multistate_processes.calculate.CalculateProcess at 0x1116c2518>
    """

    def __init__(self, network: Network, process: MultistateProcess, t_max):
        self.network = network
        self.process = process
        self.t_max = t_max

    def __iter__(self):
        self.network.get_degree_distribution()
        self.t = 0
        return self

    def __next__(self):
        self.t += 1
        return self

    def get_ms_for(self, k):
        """Gets all possible combinations of m for given degree k.

        Args:
            k (integer): degree k
        Return:
            (list): all possible combinations of m for given degree k
        """
        return [list(h) for h in list(product(range(k + 1), repeat=self.process.n)) if sum(h) == k]

    def rho(self, x):
        """Expected fraction of nodes in each state.
        \Rho^i(t) = <\sum_{|m|=k}x^i_k(t)>_k,
        where < • >_k = \sum_{k=0}^{\inf} p_k •

        Args:
            x (np.array): A matrix (t_max x n x k_max) where x[t][i][k] fraction of nodes of degree k in state i
            at time t
        Return:
            (list): all possible combinations of m for given degree k
        """
        return x @ self.network.degree_distribution
