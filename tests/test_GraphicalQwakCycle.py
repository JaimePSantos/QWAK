import networkx as nx
import numpy as np

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from GraphicalQWAKTestStub import GraphicalQWAKTestStub

from testVariables import (
    graphicalStaticProbDistCycle,
    graphicalDynamicProbDistCycle,
)

import pytest


class TestGraphicalQWAKCycle(object):
    def test_StaticProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        gQwak = GraphicalQWAKTestStub()
        np.testing.assert_almost_equal(
            gQwak.getStaticProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0]
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_DynamicProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        gQwak = GraphicalQWAKTestStub()
        np.testing.assert_almost_equal(
            gQwak.getDynamicProbVecList(),
            [np.zeros(n)],
            err_msg="Probability distribution before running should be 0.",
        )
        probVec = gQwak.runMultipleWalks()
        assert not probVec[0]
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalDynamicProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
