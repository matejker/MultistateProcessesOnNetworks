from multistate_processes.process import MultistateProcess
import numpy as np

np.set_printoptions(suppress=True)


def test_process():
    rates = np.array([['0', '({0} + {1})*alpha'], ['{0}*beta', '{0} + {1}']])
    m = np.array([10, 2])

    expected_F_m = np.array([[0., 24.], [30., 12.]])  # noqa
    expected_R_m = np.array([[24., 0.], [0., 42.]])  # noqa

    test_process = MultistateProcess(rates, alpha=2, beta=3)  # noqa

    assert (test_process.F(m) == expected_F_m).all()
    assert (test_process.R(m) == expected_R_m).all()
