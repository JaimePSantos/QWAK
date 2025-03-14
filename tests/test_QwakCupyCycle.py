import networkx as nx
import numpy as np
import cupy as cp
from qwak.Errors import StateOutOfBounds, NonUnitaryState

from qwak_cupy.qwak import QWAK
from qwak_cupy.State import State
from tests.stubs.CQWAKTestStub import CQWAKTestStub as QWAKTestStub

from tests.testVariables.qwakVar import (
    probDistUniformSuperpositionCycle,
    probDistUniformSuperpositionCycleOriented,
    probDistCustomStateCycle,
    probDistCycleNewDim,
    probDistUniformSuperpositionComplete,
)

from tests.testVariables.customGraphs import orientedGraph

import pytest


class TestQWAKCupyCycle(object):
    def test_ProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk()
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.asarray(probDistUniformSuperpositionCycle),
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_ProbDistUniformSuperpositionCycleOriented(self):
        n = 100
        t = 12
        graph = orientedGraph
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedElements = None
        qwak = QWAKTestStub(
            QWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                laplacian=laplacian,
                markedElements=markedElements,
            )
        )
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk(t)
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.asarray(probDistUniformSuperpositionCycleOriented),
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_ProbDistCustomStateCycle(self):
        n = 100
        t = 12
        customStateList = [
            (n // 2, 1j * (1 / np.sqrt(2))),
            (n // 2 + 1, (1 / np.sqrt(2))),
        ]
        
        state = State(n, customStateList=customStateList)
        state.buildState()
        qwak = QWAKTestStub()
        qwak.setInitState(state)
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        qwak.buildWalk()
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.asarray(probDistCustomStateCycle),
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_SetDimCycle(self):
        newDim = 1000
        graphStr = "nx.cycle_graph"
        t = 12
        initStateList = [newDim // 2, newDim // 2 + 1]
        qwak = QWAKTestStub()
        assert qwak.getDim() == 100
        qwak.setDim(
            newDim,
            graphStr=graphStr,
            initStateList=initStateList)
        assert qwak.getDim() == 1000
        cp.testing.assert_array_almost_equal(
            qwak.getAdjacencyMatrix(),
            cp.asarray(nx.to_numpy_array(
                nx.cycle_graph(newDim),
                dtype=complex)),
            err_msg=f"Expected adjacency matrix of {graphStr} of size {newDim} but got {qwak.getAdjacencyMatrix()}",
        )
        qwak.buildWalk(t)
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.asarray(probDistCycleNewDim),
            err_msg=f"Probability Distribution does not match expected for n = {newDim} and t = {t}",
        )

    def test_SetAdjacencyMatrix(self):
        n = 100
        t = 12
        initStateList = [n // 2, n // 2 + 1]
        newAdjMatrix = cp.asarray(nx.to_numpy_array(
            nx.complete_graph(n), dtype=complex))
        qwak = QWAKTestStub()
        cp.testing.assert_array_almost_equal(
            qwak.getAdjacencyMatrix(),
            cp.asarray(nx.to_numpy_array(
                nx.cycle_graph(n),
                dtype=complex)),
            err_msg=f"Expected adjacency matrix of cycle of size {n} but got {qwak.getAdjacencyMatrix()}",
        )
        qwak.buildWalk(t)
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.asarray(probDistUniformSuperpositionCycle),
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
        qwak.setAdjacencyMatrix(newAdjMatrix, initStateList)
        qwak.buildWalk(t)
        cp.testing.assert_array_almost_equal(
            qwak.getAdjacencyMatrix(),
            newAdjMatrix,
            err_msg=f"Expected adjacency matrix of cycle of size {n} but got {qwak.getAdjacencyMatrix()}",
        )
        cp.testing.assert_array_almost_equal(
            qwak.getProbVec(),
            cp.asarray(probDistUniformSuperpositionComplete),
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_MeanCycle(self):
        n = 100
        t = 12
        qwak = QWAKTestStub()
        qwak.buildWalk()
        np.testing.assert_allclose(
            cp.asnumpy(qwak.getMean()),
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
            cp.asnumpy(qwak.getSndMoment()),
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
            cp.asnumpy(qwak.getStDev()),
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
            cp.asnumpy(qwak.getSurvivalProb(n // 2, n // 2 + 1)),
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
            cp.asnumpy(qwak.getInversePartRatio()),
            38.079796685604926,
            atol=0,
            err_msg=f"Inverse Participation Ratio for a cycle of size {n} for time {t} should be 38.07979... but got {qwak.getInversePartRatio()}",
        )
    
    def test_StateOutOfBoundsException(self):
        with pytest.raises(StateOutOfBounds):
            n = 100
            state = State(n, nodeList=[n + 1])  # Explicitly set nodeList
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