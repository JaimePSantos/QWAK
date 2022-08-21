import networkx as nx
import numpy as np

from core.GraphicalQWAK import GraphicalQWAK
from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State

import pytest


class GraphicalQWAKTestStub:
    def __init__(self, testGQwak=None):
        staticN = 100
        dynamicN = staticN
        staticTime = 10
        initState = [staticN // 2, (staticN // 2) + 1]
        staticGraph = nx.cycle_graph(staticN)
        dynamicGraph = nx.cycle_graph(dynamicN)
        dynamicTimeList = [0, 5]
        initStateList = [[staticN // 2, (staticN // 2) + 1]]
        if testGQwak is None:
            self.GQwak = GraphicalQWAK(
                staticN=staticN,
                dynamicN=dynamicN,
                staticGraph=staticGraph,
                dynamicGraph=dynamicGraph,
                staticStateList=initState,
                dynamicStateList=initStateList,
                staticTime=staticTime,
                dynamicTimeList=dynamicTimeList,
            )
        else:
            self.GQwak = testGQwak

    def runWalk(self):
        return self.GQwak.runWalk()

    # def getProbVec(self):
    #     return self.qwak.getProbVec()
    #
    # def setInitState(self, newState):
    #     self.qwak.setInitState(newState)
    #
    # def getDim(self):
    #     return self.qwak.getDim()
    #
    # def setDim(self, newDim, graphStr, initStateList=None):
    #     self.qwak.setDim(newDim, graphStr, initStateList)
    #
    # def getAdjacencyMatrix(self):
    #     return self.qwak.getAdjacencyMatrix()
    #
    # def setAdjacencyMatrix(self, newAdjacencyMatrix, initStateList):
    #     self.qwak.setAdjacencyMatrix(newAdjacencyMatrix, initStateList)
    #
    # def getMean(self):
    #     return self.qwak.getMean()
    #
    # def getSndMoment(self):
    #     return self.qwak.getSndMoment()
    #
    # def getStDev(self):
    #     return self.qwak.getStDev()
    #
    # def getSurvivalProb(self, k0, k1):
    #     return self.qwak.getSurvivalProb(k0, k1)
    #
    # def getInversePartRatio(self):
    #     return self.qwak.getInversePartRatio()
