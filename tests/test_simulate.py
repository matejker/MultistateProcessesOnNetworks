from multistate_processes.process import MultistateProcess
from multistate_processes.simulate import SimulateProcess
from network import Network
import numpy as np


np.set_printoptions(suppress=True)


def test_simulate():
    network = Network(3, [(0, 1), (2, 1)])
    process = MultistateProcess(np.array([['0', '1'], ['0', '0']]))
    simulate = SimulateProcess(network, process, 3, [0, 1, 0], seed=42)
    iteration = iter(simulate)

    # Testing the simulation iterations
    assert iteration.t == 0
    assert (iteration.get_m_for(0) == np.array([0, 1])).all()
    assert (iteration.get_m_for(1) == np.array([2, 0])).all()
    assert (iteration.get_m_for(2) == np.array([0, 1])).all()

    assert next(iteration) == [1, 1, 0]
    assert iteration.t == 1
    assert (iteration.get_m_for(0) == np.array([0, 1])).all()
    assert (iteration.get_m_for(1) == np.array([1, 1])).all()
    assert (iteration.get_m_for(2) == np.array([0, 1])).all()

    assert next(iteration) == [1, 1, 1]
    assert iteration.t == 2
    assert (iteration.get_m_for(0) == np.array([0, 1])).all()
    assert (iteration.get_m_for(1) == np.array([0, 2])).all()
    assert (iteration.get_m_for(2) == np.array([0, 1])).all()

    assert next(iteration) == [1, 1, 1]
    assert iteration.t == 3
    assert (iteration.get_m_for(0) == np.array([0, 1])).all()
    assert (iteration.get_m_for(1) == np.array([0, 2])).all()
    assert (iteration.get_m_for(2) == np.array([0, 1])).all()
