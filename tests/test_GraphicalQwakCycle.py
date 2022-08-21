import networkx as nx
import numpy as np

from qwak.qwak import QWAK, StochasticQWAK
from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from QWAKTestStub import QWAKTestStub

# from testVariables import (
#
# )

import pytest


class TestGraphicalQWAKCycle(object):
    def test_ProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        pass
        # qwak = QWAKTestStub()
        # np.testing.assert_almost_equal(
        #     qwak.getProbVec(),
        #     np.zeros(n),
        #     err_msg="Probability distribution before running should be 0.",
        # )
        # qwak.buildWalk()
        # np.testing.assert_almost_equal(
        #     qwak.getProbVec(),
        #     probDistUniformSuperpositionCycle,
        #     err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        # )