import numpy as np
from multistate_processes.exceptions import BarabasiAlbertModelIncorrectInput
from itertools import combinations
from multistate_processes.network import Network


class BarabasiAlbert(Network):

    @classmethod
    def random_choice(cls, a, size=2):  # TODO: think about seed and if it is inherited from barabasi_albert_model()
        rc = np.random.choice(a, size).tolist()

        if len(set(rc)) == len(rc):
            return rc
        else:
            return cls.random_choice(a, size)

    @classmethod
    def model(cls, n, m, m0=None, seed=None):
        if seed:
            np.random.seed(seed)

        m0 = m0 or m

        if m0 < m:
            raise BarabasiAlbertModelIncorrectInput(f'Inserted values are not correct, m <= m0, m={m} and 0={m0}')

        if n < m0:
            raise BarabasiAlbertModelIncorrectInput(f'Inserted values are not correct, n => m0, m0={m0} and n={n}')

        # Initial complete graph
        edges = list(combinations(list(range(m0)), 2))
        nodes_basket = list(range(m0)) * (m0 - 1)

        r = m0
        while r < n:
            connections = cls.random_choice(nodes_basket, m)
            rm = [r] * m

            new_edges = list(zip(rm, connections))

            edges.extend(new_edges)
            nodes_basket.extend(rm + connections)

            r += 1

        return edges

    def __init__(self, n, m, m0=None, seed=None):
        edges = self.model(n, m, m0, seed)
        super().__init__(n, edges)
