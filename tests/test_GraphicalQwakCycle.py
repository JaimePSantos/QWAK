import networkx as nx
import numpy as np

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from GraphicalQWAKTestStub import GraphicalQWAKTestStub

from testVariables import (
    graphicalStaticProbDistCycle,
)

import pytest


class TestGraphicalQWAKCycle(object):
    def test_StaticProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        gqwak = GraphicalQWAKTestStub()

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
