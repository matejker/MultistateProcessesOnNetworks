from multistate_processes.process import MultistateProcess
from multistate_processes.meanfield import MeanField
from network import Network
import numpy as np

np.set_printoptions(suppress=True)


def test_mean_field():
    network = Network(3, [(0, 1), (2, 1)])
    process = MultistateProcess(np.array([['0', '1'], ['0', '0']]))
    x = np.zeros((3, 2, 2))
    x[0] = np.array([[1, 0], [0, 1]])
    calculate = MeanField(network, process, 2, x)
    iteration = iter(calculate)

    expected_degree_distribution = np.round(np.array([0.66666667, 0.33333333]), 4)
    expected_rho = np.round(np.array([[[0.66666667, 0.33333333], [0., 1.], [0., 1.]]]), 4)

    # Testing the iterative calculations
    assert (np.round(iteration.network.degree_distribution, 4) == expected_degree_distribution).all()
    assert iteration.t == 0
    assert (next(iteration) == np.array([[0., 0.], [1., 1.]])).all()

    assert iteration.t == 1
    assert (next(iteration) == np.array([[0., 0.], [1., 1.]])).all()

    assert iteration.t == 2
    assert (next(iteration) == np.array([[0., 0.], [1., 1.]])).all()

    assert iteration.t == 2  # Number of iteration is over the t_max, so t stays on t = 2

    assert (np.round(iteration.rho(x), 4) == expected_rho).all()

    # Testing Mean Field relations
    assert (calculate.omegas(0) == np.array([0.5, 0.5])).all()
    assert np.round(np.sum(calculate.omegas(0))) == 1  # Sum of omegas has to be one

    assert calculate.mult(2, [1, 1], np.array([0.5, 0.5])) == 0.5
