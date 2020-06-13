import numpy as np
from copy import deepcopy
from network import Network
from multistate_processes.process import MultistateProcess


class SimulateProcess:
    """An object that simulates the dynamical process, knowing the network, transition matrix and states from the
    previous iteration.

    Object attributes:
        network (Network): the network object
        multistate_process (MultistateProcess): object of the multistate process
        t_max (integer): max number (t) of process iterations
        states (list): list of states (from 0 to n - 1)

    To use:
        >>> network = Network(3, [(0, 1), (2, 1)])
        >>> process = MultistateProcess(np.array([['0', '1'], ['0', '0']]))
        >>> simulate = SimulateProcess(network, process, 100, [0, 1, 0])
        >>> iteration = iter(simulate)
        >>> next(iteration)
        [1, 1, 0]
        >>> next(iteration)
        [1, 1, 0]
        >>> next(iteration)
        [1, 1, 1]
    """

    def get_m_for(self, node):
        """Counts the neighbor's states know as a vector m

        Args:
            node (integer): a node (from 0 to N-1)

        Returns:
            m (np.array): a vector (n x 1) neighbor's states
        """
        m = np.zeros(self.multistate_process.n)
        neighbors = self.network.edges_basket[node]

        for n in neighbors:
            i = self.states[n]
            m[i] += 1

        return m

    def __init__(self, network: Network, multistate_process: MultistateProcess, t_max, states, seed=None):
        if seed:
            np.random.seed(seed)

        self.network = network
        self.multistate_process = multistate_process
        self.t_max = t_max
        self.states = states

    def __iter__(self):
        self.t = 0
        return self

    def __next__(self):
        """Simulating the next iteration, knowing the states from the previous iteration.

        Returns:
            states (list): current node states
        """
        if self.t == self.t_max:
            return self.states

        states = deepcopy(self.states)

        for node in range(self.network.n):
            m = self.get_m_for(node)
            i = self.states[node]
            p = self.multistate_process.P(m)
            random_vector = np.random.uniform(0, 1, size=self.multistate_process.n)

            transition_vector = (p[i] < random_vector) * (p[i] < 1)

            if not transition_vector.any():
                continue

            for j, transition in enumerate(transition_vector):
                if transition:
                    states[node] = j
                    break

        self.t += 1
        self.states = states
        return states
