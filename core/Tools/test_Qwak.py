import networkx as nx
import numpy as np

from Tools.Profiler import profile
from qwak.qwak import QWAK, StochasticQWAK
from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State

from Tools.testVariables import (
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
        #TODO: Laplacian not making a difference.
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
        initStateList = [newDim//2, newDim//2 + 1]
        qwak = QWAKTestStub()
        assert qwak.getDim() == 100
        qwak.setDim(newDim, graphStr,initStateList)
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
        initStateList = [n//2, n//2 + 1]
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
        qwak.setAdjacencyMatrix(newAdjMatrix,initStateList)
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

    def test_stateOutOfBoundsException(self):
        with pytest.raises(StateOutOfBounds):
            n = 100
            state = State(n, [n + 1])
            state.buildState()
            qwak = QWAKTestStub()
            qwak.setInitState(state)
            qwak.buildWalk()

    def test_nonUnitaryStateException(self):
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

    def setDim(self, newDim, graphStr,initStateList = None):
        self.qwak.setDim(newDim, graphStr, initStateList)

    def getAdjacencyMatrix(self):
        return self.qwak.getAdjacencyMatrix()

    def setAdjacencyMatrix(self, newAdjacencyMatrix,initStateList):
        self.qwak.setAdjacencyMatrix(newAdjacencyMatrix,initStateList)
