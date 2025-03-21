import networkx as nx
import cupy as np

from qwak_cupy.qwak import QWAK
from qwak_cupy.Errors import StateOutOfBounds, NonUnitaryState
from qwak_cupy.State import State

import pytest


class CQWAKTestStub:
    def __init__(self, testQwak=None):
        # TODO: We should pass the graph as a parameter here.
        n = 100
        self.t = 12
        graph = nx.cycle_graph(n)
        initStateList = [n // 2, n // 2 + 1]
        laplacian = False
        markedElements = None
        if testQwak is None:
            self.qwak = QWAK(
                graph,
                initStateList=initStateList,
                customStateList=None,
                laplacian=laplacian,
                markedElements=markedElements,
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

    def getInitState(self):
        return self.qwak.getInitState()

    def getDim(self):
        return self.qwak.getDim()

    def setDim(
            self,
            newDim,
            graphStr=None,
            graph=None,
            initStateList=None):
        self.qwak.setDim(
            newDim,
            graphStr=graphStr,
            graph=graph,
            initStateList=initStateList)

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
