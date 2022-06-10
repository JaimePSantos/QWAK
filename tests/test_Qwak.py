import networkx as nx
import numpy as np

from Tools.Profiler import profile
from qwak.qwak import QWAK, StochasticQWAK
from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State

from testVariables import (
    probDistUniformSuperpositionCycle,
    probDistUniformSuperpositionComplete,
    orientedGraph,
    probDistUniformSuperpositionCycleOriented,
    probDistUniformSuperpositionPath,
    stochasticProbDistSingleNodeCycleNoise,
    stochasticProbDistSingleNodeCycleNoNoise,
    probDistCustomStateCycle,
    probDistCycleNewDim,
)

import pytest


class TestQWAK(object):
    def test_ProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk()
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistUniformSuperpositionCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_ProbDistUniformSuperpositionComplete(self):
        n = 100
        t = 12
        self.t = t
        graph = nx.complete_graph(n)
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedSearch = None
        qwak = QWAKTestStub(
            QWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                laplacian=laplacian,
                markedSearch=markedSearch,
            )
        )
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk(t)
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistUniformSuperpositionComplete,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_ProbDistUniformSuperpositionCycleOriented(self):
        n = 100
        t = 12
        self.t = t
        graph = orientedGraph
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedSearch = None
        qwak = QWAKTestStub(
            QWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                laplacian=laplacian,
                markedSearch=markedSearch,
            )
        )
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk(t)
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistUniformSuperpositionCycleOriented,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_ProbDistUniformSuperpositionPath(self):
        # TODO: Laplacian not making a difference.
        n = 100
        t = 12
        self.t = t
        graph = nx.path_graph(n)
        initStateList = [n // 2, n // 2 + 1]
        laplacian = True
        markedSearch = None
        qwak = QWAKTestStub(
            QWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                laplacian=laplacian,
                markedSearch=markedSearch,
            )
        )
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk(t)
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistUniformSuperpositionPath,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_ProbDistCustomStateCycle(self):
        n = 100
        t = 12
        state = State(
            n,
            customStateList=[
                (n // 2, 1j * (1 / np.sqrt(2))),
                (n // 2 + 1, (1 / np.sqrt(2))),
            ],
        )
        state.buildState()
        qwak = QWAKTestStub()
        qwak.setInitState(state)
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk()
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistCustomStateCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_SetDimCycle(self):
        newDim = 1000
        graphStr = "nx.cycle_graph"
        t = 12
        initStateList = [newDim // 2, newDim // 2 + 1]
        qwak = QWAKTestStub()
        assert qwak.getDim() == 100
        qwak.setDim(newDim, graphStr, initStateList)
        assert qwak.getDim() == 1000
        np.testing.assert_almost_equal(
            qwak.getAdjacencyMatrix(),
            nx.to_numpy_array(nx.cycle_graph(newDim), dtype=complex),
            err_msg=f"Expected adjacency matrix of {graphStr} of size {newDim} but got {qwak.getAdjacencyMatrix()}",
        )
        qwak.buildWalk(t)
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistCycleNewDim,
            err_msg=f"Probability Distribution does not match expected for n = {newDim} and t = {t}",
        )

    def test_SetAdjacencyMatrix(self):
        n = 100
        t = 12
        initStateList = [n // 2, n // 2 + 1]
        newAdjMatrix = nx.to_numpy_array(nx.complete_graph(n), dtype=complex)
        qwak = QWAKTestStub()
        np.testing.assert_almost_equal(
            qwak.getAdjacencyMatrix(),
            nx.to_numpy_array(nx.cycle_graph(n), dtype=complex),
            err_msg=f"Expected adjacency matrix of cycle of size {n} but got {qwak.getAdjacencyMatrix()}",
        )
        qwak.buildWalk(t)
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistUniformSuperpositionCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
        qwak.setAdjacencyMatrix(newAdjMatrix, initStateList)
        qwak.buildWalk(t)
        np.testing.assert_almost_equal(
            qwak.getAdjacencyMatrix(),
            newAdjMatrix,
            err_msg=f"Expected adjacency matrix of cycle of size {n} but got {qwak.getAdjacencyMatrix()}",
        )
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            probDistUniformSuperpositionComplete,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_MeanCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        qwak.buildWalk()
        np.testing.assert_allclose(
            qwak.getMean(),
            50.5,
            atol=0,
            err_msg=f"Mean for a cycle of size {n} for time {t} should be 50.5 but got {qwak.getMean()}",
        )

    def test_SndMomentCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        qwak.buildWalk()
        np.testing.assert_allclose(
            qwak.getSndMoment(),
            2838.5,
            atol=0,
            err_msg=f"Second moment for a cycle of size {n} for time {t} should be 2838.5 but got {qwak.getSndMoment()}",
        )

    def test_StDevCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        qwak.buildWalk()
        np.testing.assert_allclose(
            qwak.getStDev(),
            16.977926846349753,
            atol=0,
            err_msg=f"Standard deviation for a cycle of size {n} for time {t} should be 16.9779... but got {qwak.getStDev()}",
        )

    def test_SurvivalProbCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        qwak.buildWalk()
        np.testing.assert_allclose(
            qwak.getSurvivalProb(n // 2, n // 2 + 1),
            0.02688956925823824,
            atol=0,
            err_msg=f"Survival Prob for a cycle of size {n} for time {t} between {n//2} and {n//2+1} should be 0.026889... but got {qwak.getSurvivalProb(n//2,n//2+1)}",
        )

    def test_InversePartRatioCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        qwak.buildWalk()
        np.testing.assert_allclose(
            qwak.getInversePartRatio(),
            38.079796685604926,
            atol=0,
            err_msg=f"Inverse Participation Ratio for a cycle of size {n} for time {t} should be 38.07979... but got {qwak.getInversePartRatio()}",
        )
    def test_StateOutOfBoundsException(self):
        with pytest.raises(StateOutOfBounds):
            n = 100
            state = State(n, [n + 1])
            state.buildState()
            qwak = QWAKTestStub()
            qwak.setInitState(state)
            qwak.buildWalk()

    def test_NonUnitaryStateException(self):
        with pytest.raises(NonUnitaryState):
            n = 100
            state = State(
                n,
                customStateList=[
                    (n // 2, 1),
                    (n // 2 + 1, 1),
                ],
            )
            state.buildState()
            qwak = QWAKTestStub()
            qwak.setInitState(state)
            qwak.buildWalk()


class QWAKTestStub:
    def __init__(self, testQwak=None):
        n = 100
        self.t = 12
        graph = nx.cycle_graph(n)
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedSearch = None
        if testQwak is None:
            self.qwak = QWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                laplacian=laplacian,
                markedSearch=markedSearch,
            )
        else:
            self.qwak = testQwak

    def buildWalk(self, t=None):
        if t is not None:
            self.t = t
        self.qwak.runWalk(time=self.t)

    def getProbVec(self):
        return self.qwak.getProbVec()

    def setInitState(self, newState):
        self.qwak.setInitState(newState)

    def getDim(self):
        return self.qwak.getDim()

    def setDim(self, newDim, graphStr, initStateList=None):
        self.qwak.setDim(newDim, graphStr, initStateList)

    def getAdjacencyMatrix(self):
        return self.qwak.getAdjacencyMatrix()

    def setAdjacencyMatrix(self, newAdjacencyMatrix, initStateList):
        self.qwak.setAdjacencyMatrix(newAdjacencyMatrix, initStateList)

    def getMean(self):
        return self.qwak.getMean()

    def getSndMoment(self):
        return self.qwak.getSndMoment()

    def getStDev(self):
        return self.qwak.getStDev()

    def getSurvivalProb(self, k0, k1):
        return self.qwak.getSurvivalProb(k0, k1)

    def getInversePartRatio(self):
        return self.qwak.getInversePartRatio()
