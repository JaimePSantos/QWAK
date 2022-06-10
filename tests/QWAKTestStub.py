import networkx as nx
import numpy as np

from Tools.Profiler import profile
from qwak.qwak import QWAK, StochasticQWAK
from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State

import pytest


class QWAKTestStub:
    def __init__(self, testQwak=None):
        # TODO: We should pass the graph as a parameter here.
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
