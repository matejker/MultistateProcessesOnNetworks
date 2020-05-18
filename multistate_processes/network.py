import numpy as np


class Network:

    @staticmethod
    def get_edge_basket(n, edges, edge_basket=None):
        edges_basket = edge_basket or [[] for _ in range(n)]

        for e in edges:
            i = e[0]
            j = e[1]

            edges_basket[i].append(j)
            edges_basket[j].append(i)

        return edges_basket

    def __init__(self, n, edges, edge_basket=None):
        self.n = n
        self.edges = edges

        self.edges_basket = edge_basket or self.get_edge_basket(n, edges)

        self.degrees_list = [len(_) for _ in self.edges_basket]

        self.mean_degree = np.mean(self.degrees_list)  # TODO: think about powerlaw

    def degree_distribution(self, log=False, density=True):  # TODO: think about powerlaw
        min_d = min(self.degrees_list) * 1.
        max_d = max(self.degrees_list) * 1.

        m_log = np.round(np.log10(max_d), 0)

        bins = np.logspace(np.log10(min_d), np.log10(10. ** m_log), m_log * 5.) if log else np.arange(min_d, max_d)

        return np.histogram(degrees_list, bins=bins, density=density)
