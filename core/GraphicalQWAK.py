import os

import eel
import networkx as nx
import numpy as np
import copy

from qwak.Errors import StateOutOfBounds
from qwak.State import State
from qwak.qwak import QWAK

class GraphicalQWAK:
    def __init__(
        self,
        n,
        graph: nx.Graph,
        staticStateList: list,
        dynamicStateList: list,
        staticTime: float,
        dynamicTimeList: list,
    ) -> None:
        self._n = n
        # TODO: Redo how graph is implemented because right now this attribute is useless.
        self._graph = graph
        self._staticStateList = staticStateList
        self._dynamicStateList = dynamicStateList
        self._staticTime = staticTime
        self._dynamicTimeList = dynamicTimeList
        self._staticQWAK = QWAK(graph)
        self._staticQWAK.runWalk(time = self._staticTime, initStateList = self._staticStateList)
        self._dynamicQWAK = QWAK(graph)
        self._staticQWAK.runWalk(time = self._dynamicTimeList[0], initStateList = self._dynamicStateList[0])
        self._dynamicProbDistList = []
        self._dynamicAmpList = []

    def runWalk(self):
        try:
            self._staticQWAK.resetWalk()
            self._staticQWAK.runWalk(self._staticTime, self._staticStateList)
        except StateOutOfBounds as err:
            return [True, str(err)]
        qwProbabilities = self._staticQWAK.getProbDist()
        qwProbVec = qwProbabilities.getProbVec()
        probLists = qwProbVec.tolist()
        return [False, probLists]

    def runMultipleWalks(self):
        qwProbVecList = []
        self._dynamicQWAK.resetWalk()
        self._dynamicProbDistList = []
        self._dynamicAmpList = []
        # TODO: Adicionar um metodo ao QWAK para multiple walks.
        timeRange = np.linspace(self._dynamicTimeList[0], self._dynamicTimeList[1], int(self._dynamicTimeList[1]))
        for t in timeRange:
            self._dynamicQWAK.runWalk(time=t, initStateList=self._dynamicStateList[0])
            # TODO: Check if we can remove copy now that we're using a class.
            qwProbabilities = copy.copy(self._dynamicQWAK.getProbDist())
            self._dynamicAmpList.append(copy.deepcopy(self._dynamicQWAK.getWalk()))
            self._dynamicProbDistList.append(copy.deepcopy(qwProbabilities))
            qwProbVecList.append(qwProbabilities.getProbVec().tolist())
        return qwProbVecList

    def setDim(self,newDim, graphStr):
        self._staticQWAK.setDim(newDim, graphStr)
        self._dynamicQWAK.setDim(newDim, graphStr)

    def getDim(self):
        return self._staticQWAK.getDim()

    def setGraph(self,newGraph):
        newStaticGraph = eval(newGraph + f"({self._staticQWAK.getDim()})")
        newDynamicGraph = eval(newGraph + f"({self._dynamicQWAK.getDim()})")
        self._staticQWAK.setGraph(newStaticGraph)
        self._dynamicQWAK.setGraph(newDynamicGraph)

    def getGraph(self):
        # TODO: Different graphs for dynamic and static.
        return self._staticQWAK.getGraph()

    def getGraphToJson(self):
        # TODO: This will also need to change with new graph implementation.
        return nx.cytoscape_data(self._staticQWAK.getGraph())

    def setStaticTime(self,newTime):
        self._staticTime = eval(newTime)
        self._staticQWAK.setTime(self._staticTime)

    def getStaticTime(self):
        return self._staticTime

    def setDynamicTime(self,newTimeList):
        self._dynamicTimeList = list(map(float, newTimeList.split(",")))
        # self._dynamicQWAK.setTime(self._staticTime)

    def getDynamicTime(self):
        return self._dynamicTimeList

    def setDynamicInitStateList(self,newInitStateList):
        parsedInitState = newInitStateList.split(";")
        self._dynamicStateList = []
        for initState in parsedInitState:
            self._dynamicStateList.append(list(map(int, initState.split(","))))

    def setStaticInitState(self,initStateStr):
        self._staticStateList = []
        self._staticStateList = list(map(int, initStateStr.split(",")))
        newState = State(self._staticQWAK.getDim())
        newState.buildState(self._staticStateList)
        self._staticQWAK.setInitState(newState)

    def getStaticInitState(self):
        return self._staticStateList

    def getStaticMean(self):
        return self._staticQWAK.getMean()

    def getDynamicMean(self):
        # TODO: We might need to reset the walk somewhere for the plot to work properly.
        meanList = []
        for probDist in self._dynamicProbDistList:
            meanList.append(probDist.mean())
        return meanList

    def getStaticSndMoment(self):
        return self._staticQWAK.getSndMoment()

    def getStaticStDev(self):
        return self._staticQWAK.getStDev()

    def getDynamicStDev(self):
        stDevList = []
        for probDist in self._dynamicProbDistList:
            stDevList.append(probDist.stDev())
        return stDevList

    def getStaticSurvivalProb(self,k0, k1):
        # TODO: Make JS throw an error if k0 or k1 are not defined.
        return self._staticQWAK.getSurvivalProb(k0, k1)

    def getDynamicSurvivalProb(self,k0, k1):
        # TODO: Make JS throw an error if k0 or k1 are not defined.
        survProbList = []
        for probDist in self._dynamicProbDistList:
            survProbList.append(probDist.survivalProb(k0, k1))
        return survProbList

    def getStaticInversePartRatio(self):
        return self._staticQWAK.getInversePartRatio()

    def getDynamicInvPartRatio(self):
        invPartRatioList = []
        for amps in self._dynamicAmpList:
            invPartRatioList.append(amps.invPartRatio())
        return invPartRatioList

    def checkPST(self,nodeA, nodeB):
        # TODO: Make JS throw an error if k0 or k1 are not defined.
        return str(self._staticQWAK.checkPST(nodeA, nodeB))

    def customGraphWalk(self,customAdjacency):
        # TODO: Running the custom graph set graph button throws an error if the field on the prob dist side is not with correct dimension. check out how to fix this.
        self._staticQWAK.setAdjacencyMatrix(customAdjacency)
        initState = State(self._staticQWAK.getDim())
        initState.buildState([self._staticQWAK.getDim() // 2])
        self._staticQWAK.setInitState(initState)
        self._dynamicQWAK.setInitState(initState)
        self._staticQWAK.runWalk(self._staticTime)
        self._dynamicQWAK.setAdjacencyMatrix(customAdjacency)
        self._dynamicQWAK.runWalk(self._staticTime)
