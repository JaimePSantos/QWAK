import networkx as nx
import numpy as np

from Tools.Profiler import profile
from qwak.qwak import StochasticQWAK
from Tools.testVariables import (
        stochasticProbDistSingleNodeCycleNoise,
        stochasticProbDistSingleNodeCycleNoNoise,
        )


import pytest

class TestStochasticQWAK(object):

    def test_StochasticProbDistSingleNodeCycleNoise(self):
        n = 50
        t = 6
        qwak = StochasticQWAKTestStub()
        np.testing.assert_almost_equal(qwak.getProbVec(),np.zeros(n),err_msg="Probability distribution before running should be 0.")
        qwak.buildWalk()
        np.testing.assert_almost_equal(qwak.getProbVec(),stochasticProbDistSingleNodeCycleNoNoise, err_msg= f"Probability Distribution does not match expected for n = {n} and t = {t}")



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

    def getProbVec(self):
        return self.qwak.getProbVec()
