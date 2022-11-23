import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from tests.stubs.GraphicalQWAKTestStub import GraphicalQWAKTestStub

from tests.testVariables.graphicalQwakVar import (
    graphicalStaticProbDistCycle,
    graphicalDynamicProbDistCycle,
    graphicalStaticProbDistCycleNewDim,
    graphicalStaticProbDistCycleNewInitState,
    graphicalDynamicProbDistCycleNewInitState,
    graphicalDynamicProbDistCycleNewDim,
    graphicalStaticSetGraphCycleComplete,
    graphicalDynamicSetGraphCycleComplete,
    graphicalStaticSetTimeCycle,
    graphicalDynamicSetTimeCycle,
    graphicalDynamicGetMeanCycle,
    graphicalDynamicGetStDevCycle,
    graphicalDynamicGetSurvivalProbCycle,
    graphicalDynamicGetInvPartRatio,
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
        assert not probVec[0], "runWalk should not have thrown an error."
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_DynamicProbDistUniformSuperpositionCycle(self):
        n = 100
        t = [0, 12]
        gQwak = GraphicalQWAKTestStub()
        # np.testing.assert_almost_equal(
        #     gQwak.getDynamicProbVecList(),
        #     [np.zeros(n)],
        #     err_msg="Probability distribution before running should be 0.",
        # )
        assert not len(gQwak.getDynamicProbVecList()), "Probability distribution before running should be 0."
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_StaticProbDistCustomStateCycle(self):
        # TODO: Introduce custom state walks to GUI first.
        pass

    def test_DynamicProbDistCustomStateCycle(self):
        # TODO: Introduce custom state walks to GUI first.
        pass

    def test_StaticSetInitStateCycle(self):
        n = 100
        t = 12
        gQwak = GraphicalQWAKTestStub()
        newInitState = str(n // 4) + ',' + str(n // 4 + 1)
        np.testing.assert_almost_equal(
            gQwak.getStaticProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        np.testing.assert_almost_equal(
            gQwak.getStaticInitState(),
            [n // 2, n // 2 + 1],
            err_msg=f"Init state of gQwak {gQwak.getStaticInitState()} does not match expected init state {[n//2,n//2+1]}",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0], "runWalk should not have thrown an error."
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
        gQwak.setStaticInitState(newInitState)
        np.testing.assert_almost_equal(
            gQwak.getStaticInitState(),
            [n // 4, n // 4 + 1],
            err_msg=f"Init state of gQwak {gQwak.getStaticInitState()} does not match expected new init state {[n//4,n//4+1]}",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0]
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticProbDistCycleNewInitState,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_DynamicSetInitStateCycle(self):
        n = 100
        t = [0, 12]
        gQwak = GraphicalQWAKTestStub()
        newInitStateList = str(n // 4) + ',' + str(n // 4 + 1)
        # np.testing.assert_almost_equal(
        #     gQwak.getDynamicProbVecList(),
        #     [np.zeros(n)],
        #     err_msg="Probability distribution before running should be 0.",
        # )
        assert not len(gQwak.getDynamicProbVecList()), "Probability distribution before running should be 0."
        np.testing.assert_almost_equal(
            gQwak.getDynamicInitStateList(),
            [[n // 2, n // 2 + 1]],
            err_msg=f"Init state of gQwak {gQwak.getStaticInitState()} does not match expected init state {[n//2,n//2+1]}",
        )
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
        gQwak.setDynamicInitStateList(newInitStateList)
        np.testing.assert_almost_equal(
            gQwak.getDynamicInitStateList(),
            [[n // 4, n // 4 + 1]],
            err_msg=f"Init state of gQwak {gQwak.getStaticInitState()} does not match expected new init state {[n//4,n//4+1]}",
        )
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicProbDistCycleNewInitState,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_StaticSetDimCycle(self):
        newDim = 1000
        graphStr = "nx.cycle_graph"
        t = 12
        initStateList = [newDim // 2, newDim // 2 + 1]
        gQwak = GraphicalQWAKTestStub()
        assert gQwak.getStaticDim() == 100, "Dimension should be 100."
        gQwak.setStaticDim(
            newDim,
            graphStr=graphStr,
            initStateList=initStateList)
        assert gQwak.getStaticDim() == 1000, "Dimension should be 1000."
        gQwak.setStaticInitState(
            str(newDim // 2) + ',' + str(newDim // 2 + 1))
        np.testing.assert_almost_equal(
            gQwak.getStaticInitState(),
            [newDim // 2, newDim // 2 + 1],
            err_msg=f"Init state of gQwak {gQwak.getStaticInitState()} does not match expected new init state {[newDim//2,newDim//2+1]}",
        )
        np.testing.assert_almost_equal(
            gQwak.getStaticAdjacencyMatrix(),
            nx.to_numpy_array(
                nx.cycle_graph(newDim),
                dtype=complex),
            err_msg=f"Expected adjacency matrix of {graphStr} of size {newDim} but got {len(gQwak.getStaticAdjacencyMatrix())}",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0], "runWalk should not have thrown an error."
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticProbDistCycleNewDim,
            err_msg=f"Probability Distribution does not match expected for n = {newDim} and t = {t}",
        )

    def test_DynamicSetDimCycle(self):
        newDim = 1000
        graphStr = "nx.cycle_graph"
        t = [0, 12]
        initStateList = [[newDim // 2, newDim // 2 + 1]]
        gQwak = GraphicalQWAKTestStub()
        assert gQwak.getDynamicDim() == 100, "Dimension should be 100."
        gQwak.setDynamicDim(newDim, graphStr)
        assert gQwak.getDynamicDim() == 1000, "Dimension should be 1000."
        gQwak.setDynamicInitStateList(
            str(newDim // 2) + ',' + str(newDim // 2 + 1))
        np.testing.assert_almost_equal(
            gQwak.getDynamicInitStateList(),
            [[newDim // 2, newDim // 2 + 1]],
            err_msg=f"Init state of gQwak {gQwak.getDynamicInitStateList()} does not match expected new init state list {[[newDim//2,newDim//2+1]]}",
        )
        np.testing.assert_almost_equal(
            gQwak.getDynamicAdjacencyMatrix(),
            nx.to_numpy_array(
                nx.cycle_graph(newDim),
                dtype=complex),
            err_msg=f"Expected adjacency matrix of {graphStr} of size {newDim} but got {gQwak.getStaticAdjacencyMatrix()}",
        )
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicProbDistCycleNewDim,
            err_msg=f"Probability Distribution does not match expected for n = {newDim} and t = {t}",
        )

    def test_StaticSetGraphCycleComplete(self):
        n = 100
        newGraphStr = "nx.complete_graph"
        t = 12
        gQwak = GraphicalQWAKTestStub()
        assert nx.is_isomorphic(gQwak.getStaticGraph(), nx.cycle_graph(
            n)), "GQwak graph should be isomorphic to a cycle graph"
        gQwak.setStaticGraph(newGraphStr)
        assert nx.is_isomorphic(gQwak.getStaticGraph(), nx.complete_graph(
            n)), "GQwak graph should be isomorphic to a complete graph"
        np.testing.assert_almost_equal(
            gQwak.getStaticProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0], "runWalk should not have thrown an error."
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticSetGraphCycleComplete,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_StaticSetGraphCycleLadder(self):
        n = 100
        newGraphStr = "nx.circular_ladder_graph"
        t = 12
        gQwak = GraphicalQWAKTestStub()
        assert nx.is_isomorphic(gQwak.getStaticGraph(), nx.cycle_graph(
            n)), "GQwak graph should be isomorphic to a cycle graph"
        gQwak.setStaticGraph(newGraphStr)
        assert nx.is_isomorphic(gQwak.getStaticGraph(), nx.circular_ladder_graph(
            n)), "GQwak graph should be isomorphic to a ladder graph"
        np.testing.assert_almost_equal(
            gQwak.getStaticProbVec(),
            np.zeros(2 * n),
            err_msg="Probability distribution before running should be 0.",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0], "runWalk should not have thrown an error."
        # np.testing.assert_almost_equal(
        #     probVec[1],
        #     graphicalStaticSetGraphCycleComplete,
        #     err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        # )

    def test_DynamicSetGraphCycleComplete(self):
        n = 100
        newGraphStr = "nx.complete_graph"
        t = [0, 12]
        gQwak = GraphicalQWAKTestStub()
        assert nx.is_isomorphic(gQwak.getDynamicGraph(), nx.cycle_graph(
            n)), "GQwak graph should be isomorphic to a cycle graph"
        gQwak.setDynamicGraph(newGraphStr)
        assert nx.is_isomorphic(gQwak.getDynamicGraph(), nx.complete_graph(
            n)), "GQwak graph should be isomorphic to a complete graph"
        # np.testing.assert_almost_equal(
        #     gQwak.getDynamicProbVecList(),
        #     [np.zeros(n)],
        #     err_msg="Probability distribution before running should be 0.",
        # )
        assert not len(gQwak.getDynamicProbVecList()), "Probability distribution before running should be 0."
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicSetGraphCycleComplete,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_StaticSetTimeCycle(self):
        n = 100
        t = 12
        # Time is given as a string since the GUI can give values such
        # as 2*pi for python to eval().
        newTime = "10*np.pi"
        gQwak = GraphicalQWAKTestStub()
        np.testing.assert_almost_equal(
            gQwak.getStaticProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        probVec = gQwak.runWalk()
        assert not probVec[0], "runWalk should not have thrown an error."
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
        assert gQwak.getStaticTime() == 12, "Time should be 12."
        gQwak.setStaticTime(newTime)
        assert gQwak.getStaticTime() == 10 * np.pi, "Time should be 10*pi."
        probVec = gQwak.runWalk()
        assert not probVec[0], "runWalk should not have thrown an error."
        np.testing.assert_almost_equal(
            probVec[1],
            graphicalStaticSetTimeCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_DynamicSetTimeCycle(self):
        n = 100
        t = [0, 12]
        # Time is given as a string since the GUI can give values such
        # as 2*pi for python to eval().
        newTimeList = '0' + ',' + str(10 * np.pi)
        gQwak = GraphicalQWAKTestStub()
        # np.testing.assert_almost_equal(
        #     gQwak.getDynamicProbVecList(),
        #     [np.zeros(n)],
        #     err_msg="Probability distribution before running should be 0.",
        # )
        assert not len(gQwak.getDynamicProbVecList()), "Probability distribution before running should be 0."
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicProbDistCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )
        assert gQwak.getDynamicTime().all() == np.linspace(
            0, 12, 12).all(), "Time list should be [0-12]."
        gQwak.setDynamicTime(newTimeList)
        assert gQwak.getDynamicTime().all() == np.linspace(
            0, 10 * np.pi, int(10 * np.pi)).all(), f"Time should be [0-10*pi]."
        probVecList = gQwak.runMultipleWalks()
        assert not probVecList[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_almost_equal(
            probVecList[1],
            graphicalDynamicSetTimeCycle,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

    def test_StaticGetMeanCycle(self):
        n = 100
        t = 12
        gQwak = GraphicalQWAKTestStub()
        runWalk = gQwak.runWalk()
        assert not runWalk[0], "runWalk should not have thrown an error."
        np.testing.assert_allclose(
            gQwak.getStaticMean(),
            50.5,
            atol=0,
            err_msg=f"Mean for a cycle of size {n} for time {t} should be 50.5 but got {gQwak.getStaticMean()}",
        )

    def test_DynamicGetMeanCycle(self):
        n = 100
        t = [0, 12]
        gQwak = GraphicalQWAKTestStub()
        runMultipleWalks = gQwak.runMultipleWalks()
        assert not runMultipleWalks[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_allclose(
            gQwak.getDynamicMean(),
            graphicalDynamicGetMeanCycle,
            atol=0,
            err_msg=f"Mean for a cycle of size {n} for time {t}: {gQwak.getDynamicStDev()} is wrong.",
        )

    def test_StaticGetStDev(self):
        n = 100
        t = 12
        gQwak = GraphicalQWAKTestStub()
        runWalk = gQwak.runWalk()
        assert not runWalk[0], "runWalk should not have thrown an error."
        np.testing.assert_allclose(
            gQwak.getStaticStDev(),
            16.977926846349753,
            atol=0,
            err_msg=f"Standard deviation for a cycle of size {n} for time {t} should be 16.9779... but got {gQwak.getStaticStDev()}",
        )

    def test_DynamicGetStDev(self):
        n = 100
        t = [0, 12]
        gQwak = GraphicalQWAKTestStub()
        runMultipleWalks = gQwak.runMultipleWalks()
        assert not runMultipleWalks[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_allclose(
            gQwak.getDynamicStDev(),
            graphicalDynamicGetStDevCycle,
            atol=0,
            err_msg=f"Standard deviation for a cycle of size {n} for time {t}: {gQwak.getDynamicStDev()} is wrong.",
        )

    def test_StaticGetSurvivalProb(self):
        n = 100
        t = 12
        k0 = 45
        k1 = 55
        gQwak = GraphicalQWAKTestStub()
        runWalk = gQwak.runWalk()
        assert not runWalk[0], "runWalk should not have thrown an error."
        survivalProb = gQwak.getStaticSurvivalProb(k0, k1)
        assert not survivalProb[0], "survivalProb should not have thrown an error."
        np.testing.assert_allclose(
            survivalProb[1],
            0.14801154492037774,
            atol=0,
            err_msg=f"SurvivalProb for a cycle of size {n} for time {t} between {k0} and {k1} should be 0.148011... but got {survivalProb}",
        )

    def test_DynamicGetSurvivalProb(self):
        n = 100
        t = [0, 12]
        k0 = 45
        k1 = 55
        gQwak = GraphicalQWAKTestStub()
        runMultipleWalks = gQwak.runMultipleWalks()
        assert not runMultipleWalks[0], "runMultipleWalks should not have thrown an error."
        survivalProbList = gQwak.getDynamicSurvivalProb(k0, k1)
        assert not survivalProbList[0], "survivalProbList should not have thrown an error."
        np.testing.assert_allclose(
            survivalProbList[1],
            graphicalDynamicGetSurvivalProbCycle,
            atol=0,
            err_msg=f"Standard deviation for a cycle of size {n} for time {t}: {gQwak.getDynamicStDev()} is wrong.",
        )

    def test_StaticGetInversePartRatio(self):
        n = 100
        t = 12
        gQwak = GraphicalQWAKTestStub()
        runWalk = gQwak.runWalk()
        assert not runWalk[0], "runWalk should not have thrown an error."
        np.testing.assert_allclose(
            gQwak.getStaticInversePartRatio(),
            38.07979668560495,
            atol=0,
            err_msg=f"Inv part ratio for a cycle of size {n} for time {t} should be 38.07979... but got {gQwak.getStaticStDev()}",
        )

    def test_DynamicGetInversePartRatio(self):
        n = 100
        t = [0, 12]
        gQwak = GraphicalQWAKTestStub()
        runMultipleWalks = gQwak.runMultipleWalks()
        assert not runMultipleWalks[0], "runMultipleWalks should not have thrown an error."
        np.testing.assert_allclose(
            gQwak.getDynamicInvPartRatio(),
            graphicalDynamicGetInvPartRatio,
            atol=0,
            err_msg=f"Inv part ratio for a cycle of size {n} for time {t}: {gQwak.getDynamicInvPartRatio()} is wrong.",
        )
