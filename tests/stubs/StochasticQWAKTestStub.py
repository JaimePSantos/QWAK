import networkx as nx
import numpy as np

from qwak.qwak import StochasticQWAK


class StochasticQWAKTestStub:
    def __init__(self, testQwak=None):
        if testQwak is None:
            n = 50
            t = 6
            self.t = t
            noiseParam = 0.0
            sinkNode = None
            sinkRate = 1.0
            graph = nx.cycle_graph(n)
            initStateList = [n // 2]
            laplacian = False
            markedSearch = None
            self.qwak = StochasticQWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                noiseParam=noiseParam,
                sinkNode=sinkNode,
                sinkRate=sinkRate,
            )
        else:
            self.qwak = testQwak

    def buildWalk(
            self,
            t,
            noiseParam=None,
            sinkNode=None,
            sinkRate=None):
        if t is not None:
            self.t = t
        self.qwak.runWalk(self.t)

    def getProbVec(self):
        return self.qwak.getProbVec()
