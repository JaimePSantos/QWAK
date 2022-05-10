import networkx as nx
import numpy as np

from Tools.Profiler import profile
from qwak.qwak import QWAK, StochasticQWAK

from Tools.testVariables import (probDistUniformSuperpositionCycle,
        probDistUniformSuperpositionComplete,
        orientedGraph,
        probDistUniformSuperpositionCycleOriented,
        probDistUniformSuperpositionPath,
        stochasticProbDistSingleNodeCycleNoise,
        stochasticProbDistSingleNodeCycleNoNoise,
        )

probDistUniformSuperpositionCycle = np.asarray(probDistUniformSuperpositionCycle).flatten()
probDistUniformSuperpositionComplete= np.asarray(probDistUniformSuperpositionComplete).flatten()
probDistUniformSuperpositionCycle = np.asarray(probDistUniformSuperpositionCycle).flatten()
probDistUniformSuperpositionCycleOriented = np.asarray(probDistUniformSuperpositionCycleOriented).flatten()
probDistUniformSuperpositionPath = np.asarray(probDistUniformSuperpositionPath).flatten()

import unittest


class QWAKTest(unittest.TestCase):

    def testProbDistUniformSuperpositionCycle(self):
        n = 100
        t = 12
        qwakStub = QWAKTestStub()
        qwak = qwakStub.getQwak()
        np.testing.assert_almost_equal(qwak.getProbDistVec(),np.zeros(n),err_msg="Probability distribution before running should be 0.")
        qwak.runWalk(t)
        np.testing.assert_almost_equal(qwak.getProbDistVec(),probDistUniformSuperpositionCycle, err_msg= f"Probability Distribution does not match expected for n = {n} and t = {t}")

    def testProbDistUniformSuperpositionComplete(self):
        n = 100 
        t = 12 
        self.t = t
        graph = nx.complete_graph(n)
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedSearch = None
        qwakStub = QWAKTestStub(QWAK(graph, initStateList = initStateList, customStateList = None, laplacian = laplacian, markedSearch = markedSearch)
)
        qwak = qwakStub.getQwak()
        np.testing.assert_almost_equal(qwak.getProbDistVec(),np.zeros(n),err_msg="Probability distribution before running should be 0.")
        qwak.runWalk(t)
        np.testing.assert_almost_equal(qwak.getProbDistVec(),probDistUniformSuperpositionComplete, err_msg= f"Probability Distribution does not match expected for n = {n} and t = {t}")

    def testProbDistUniformSuperpositionCycleOriented(self):
        n = 100 
        t = 12 
        self.t = t
        graph = orientedGraph 
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedSearch = None
        qwakStub = QWAKTestStub(QWAK(graph, initStateList = initStateList, customStateList = None, laplacian = laplacian, markedSearch = markedSearch)
)
        qwak = qwakStub.getQwak()
        np.testing.assert_almost_equal(qwak.getProbDistVec(),np.zeros(n),err_msg="Probability distribution before running should be 0.")
        qwak.runWalk(t)
        np.testing.assert_almost_equal(qwak.getProbDistVec(),probDistUniformSuperpositionCycleOriented, err_msg= f"Probability Distribution does not match expected for n = {n} and t = {t}")

    def testProbDistUniformSuperpositionPath(self):
        n = 100 
        t = 12 
        self.t = t
        graph = nx.path_graph(n)
        initStateList = [n // 2, n // 2 + 1]
        laplacian = True 
        markedSearch = None
        qwakStub = QWAKTestStub(QWAK(graph, initStateList = initStateList, customStateList = None, laplacian = laplacian, markedSearch = markedSearch)
)
        qwak = qwakStub.getQwak()
        np.testing.assert_almost_equal(qwak.getProbDistVec(),np.zeros(n),err_msg="Probability distribution before running should be 0.")
        qwak.runWalk(t)
        np.testing.assert_almost_equal(qwak.getProbDistVec(),probDistUniformSuperpositionPath, err_msg= f"Probability Distribution does not match expected for n = {n} and t = {t}")


class QWAKTestStub:

    def __init__(self, testQwak = None):
        if testQwak is None:
            n = 100 
            t = 12 
            self.t = t
            graph = nx.cycle_graph(n)
            initStateList = [n // 2, n // 2 + 1]
            laplacian = False
            markedSearch = None
            self.qwak = QWAK(graph, initStateList = initStateList, customStateList = None, laplacian = laplacian, markedSearch = markedSearch)
        else:
            self.qwak = testQwak

    def buildWalk(self):
        self.qwak.runWalk(self.t)

    def getQwak(self):
        return self.qwak

class StochasticQWAKTestStub:

    def __init__(self, testQwak = None):
        if testQwak is None:
            n = 50 
            t = 6
            self.t = t
            noiseParam = 0.
            sinkNode = None 
            sinkRate = 1.0
            graph = nx.cycle_graph(n)
            initStateList = [n // 2]
            laplacian = False
            markedSearch = None
            self.qwak = StochasticQWAK(graph, initStateList = initStateList, customStateList = None, noiseParam = noiseParam, sinkNode = sinkNode, sinkRate = sinkRate)
        else:
            self.qwak = testQwak

    def buildWalk(self):
        self.qwak.runWalk(self.t)

    def getQwak(self):
        return self.qwak

if __name__ == '__main__':
    unittest.main()
