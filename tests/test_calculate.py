from multistate_processes.process import MultistateProcess
from multistate_processes.calculate import CalculateProcess
from network import Network
import numpy as np

np.set_printoptions(suppress=True)


def test_calculate():
    network = Network(3, [(0, 1), (2, 1)])
    process = MultistateProcess(np.array([['0', '1'], ['0', '0']]))
    calculate = CalculateProcess(network, process, 2)
    iteration = iter(calculate)

    expected_degree_distribution = np.round(np.array([0.66666667, 0.33333333]), 4)
    expected_rho = np.round(np.array([[[0.66666667, 0.33333333], [0.66666667, 0.33333333]]]), 4)
    x = np.array([[[1, 0], [0, 1]], [[1, 0], [0, 1]]])

    assert (np.round(iteration.network.degree_distribution, 4) == expected_degree_distribution).all()
    assert iteration.t == 0
    assert next(iteration).t == 1
    assert next(iteration).t == 1  # Number of iteration is over the t_max, so t stays on t = 1

    assert iteration.get_ms_for(3) == [[0, 3], [1, 2], [2, 1], [3, 0]]
    assert (np.round(iteration.rho(x), 4) == expected_rho).all()
