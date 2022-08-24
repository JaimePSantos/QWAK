import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from tests.stubs.GraphicalQWAKTestStub import GraphicalQWAKTestStub

from tests.testVariables.graphicalQwakVar import (
    graphicalStaticProbDistCycle,
    graphicalDynamicProbDistCycle,
    graphicalStaticProbDistCycleNewDim,
)


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
        t = [0,12]
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

    def test_StaticProbDistUniformSuperpositionCycleOriented(self):
        # TODO: Introduce oriented walks to GUI first.
        pass

    def test_ProbDistCustomStateCycle(self):
        # TODO: Introduce custom state walks to GUI first.
        pass

    def test_StaticSetDimCycle(self):
        newDim = 1000
        graphStr = "nx.cycle_graph"
        t = 12
        initStateList = [newDim // 2, newDim // 2 + 1]
        gQwak = GraphicalQWAKTestStub()
        assert gQwak.getStaticDim() == 100
        gQwak.setStaticDim(newDim, graphStr)
        gQwak.setStaticInitState(str(newDim // 2)+','+str(newDim // 2 + 1))
        assert gQwak.getStaticDim() == 1000
        np.testing.assert_almost_equal(
            gQwak.getStaticAdjacencyMatrix(),
            nx.to_numpy_array(
                nx.cycle_graph(newDim),
                dtype=complex),
            err_msg=f"Expected adjacency matrix of {graphStr} of size {newDim} but got {gQwak.getStaticAdjacencyMatrix()}",
        )
        plt.plot(gQwak.runWalk()[1])
        plt.show()
        np.testing.assert_almost_equal(
            gQwak.runWalk()[1],
            graphicalStaticProbDistCycleNewDim,
            err_msg=f"Probability Distribution does not match expected for n = {newDim} and t = {t}",
        )
