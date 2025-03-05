import networkx as nx
import numpy as np

from qwak.StochasticQwak import StochasticQWAK
from stubs.StochasticQWAKTestStub import StochasticQWAKTestStub

from testVariables.stochasticQwakVar import (
    stochasticProbDistSingleNodeCycleNoise,
    stochasticProbDistSingleNodeCycleNoNoise,
)


class TestStochasticQWAK(object):
    def test_StochasticProbDistSingleNodeCycleNoNoise(self):
        n = 50
        t = 6
        qwak = StochasticQWAKTestStub()
        np.testing.assert_almost_equal(
            qwak.getProbVec(),
            np.zeros(n),
            err_msg="Probability distribution before running should be 0.",
        )
        print("Before calling buildWalk")
        qwak.buildWalk(t)
        print("After calling buildWalk")


    def test_StochasticProbDistSingleNodeCycleNoise(self):
        n = 50
        t = 1
        self.t = t
        noiseParam = 0.15
        sinkNode = 10
        sinkRate = 1.0
        graph = nx.cycle_graph(n)
        initStateList = [n // 2]
        qwak = StochasticQWAKTestStub(
            StochasticQWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                noiseParam=noiseParam,
                sinkNode=sinkNode,
                sinkRate=sinkRate,
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
            stochasticProbDistSingleNodeCycleNoise,
            err_msg=f"Probability Distribution does not match expected for n = {n} and t = {t}",
        )

bench = TestStochasticQWAK()
bench.test_StochasticProbDistSingleNodeCycleNoNoise()
# bench.test_StochasticProbDistSingleNodeCycleNoise()