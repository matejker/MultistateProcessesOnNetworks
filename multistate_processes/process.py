import numpy as np
np.set_printoptions(suppress=True)


class MultistateProcess:
    """A continuous-time multistate dynamical processes that is represented by the rate functions F_m(i->j), where it
    denotes the rate at which a node in state i changes to state j as a function of the the number of node's neighbors
    in each of n states. For matrix notation we consider a rate matrix (F_m)ij = F_m(i->j). An object MultistateProcess
    has also transition matrix P with transition probabilities between states based on neighbor's states (m) and diagonal
    matrix R where (R - F.T) forms a true transition rate matrix.

    Object attributes:
        rates (np.array n x n): a rate matrix with given neighbor states interactions
        n (integer): number of states in the process
        tau=None (np.array n x 1)
        **kwargs: extra variables for rate matrix

    To use:
    >>> rates = np.array([['0', '({0} + {1})*alpha'], ['{0}*beta', '{0} + {1}']])
    >>> process = MultistateProcess(rates, alpha=2, beta=3)
    >>> m = np.array([10, 2])
    >>> process.F(m)
    array([[ 0., 24.], [30., 12.]])

    References:
        ..[1] Peter G. Fennell, James P. Gleeson,
        Multistate dynamical processes on networks: Analysis through degree-based approximation frameworks,
        arXiv:1709.09969 [physics.soc-ph]

        ..[2] Richard Durrett,
        Essentials of Stochastic Processes,
        Springer; 2nd ed. 2012 edition (23 May 2012)
    """

    def __init__(self, rates, tau=None, **kwargs):
        self.rates = rates
        self.kwargs = kwargs

        self.n = self.rates.shape[0]

        self.tau = tau or np.ones(self.n)

    def get_rate_matrix(self, m):
        """Generates the rate matrix from the given rate template and neighbor states of vector m.

        Args:
            m (np.array n x 1): vector of neighbor states
        Return:
            (np.array n x n): rate matrix
        """
        eval_rates = [eval(j.format(*m), self.kwargs) for i in self.rates for j in i]
        return np.array(eval_rates).astype(float).reshape(self.rates.shape)

    def F(self, m):  # noqa
        """(Shell which) generates the rate matrix from the given rate template and neighbor states of vector m.

        Args:
            m (np.array n x 1): vector of neighbor states
        Return:
            (np.array n x n): rate matrix
        """
        return self.get_rate_matrix(m)

    def R(self, m):  # noqa
        """Diagonal matrix R where (R - F.T) forms a true transition rate matrix.

        Args:
            m (np.array n x 1): vector of neighbor states
        Return:
            (np.array n x n): diagonal matrix
        """
        matrix = self.get_rate_matrix(m)
        return np.diag(matrix.sum(axis=1))

    def P(self, m):  # noqa
        """Transition matrix P with transition probabilities between states based on neighbors stats (m).

        Args:
            m (np.array n x 1): vector of neighbor states
        Return:
            (np.array n x n): Transition matrix P
        """
        matrix = self.get_rate_matrix(m)
        return np.exp(- matrix * self.tau)
