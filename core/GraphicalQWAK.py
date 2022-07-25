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

    # def setTime(self,newTime):
    #     global staticQuantumWalk, t
    #     t = eval(newTime)
    #     staticQuantumWalk.setTime(t)
    #
    # def getTime(self):
    #     return staticQuantumWalk.getTime()
    #
    # def setTimeList(self,newTimeList):
    #     global timeList
    #     timeList = list(map(float, newTimeList.split(",")))
    #
    # def setInitStateList(self,newInitStateList):
    #     global initStateList
    #     initStateList = []
    #     parsedInitState = newInitStateList.split(";")
    #     for initState in parsedInitState:
    #         initStateList.append(list(map(int, initState.split(","))))
    #
    # def setInitState(self,initStateStr):
    #     global initState
    #     initState = list(map(int, initStateStr.split(",")))
    #     newState = State(staticQuantumWalk.getDim())
    #     newState.buildState(initState)
    #     staticQuantumWalk.setInitState(newState)
    #
    # def getInitState(self):
    #     return staticQuantumWalk.getInitState()

