import os

import eel
import networkx as nx
import numpy as np
import copy

from qwak.Errors import StateOutOfBounds, UndefinedTimeList, EmptyProbDistList
from qwak.State import State
from qwak.qwak import QWAK


class GraphicalQWAK:
    def __init__(
        self,
        staticN,
        dynamicN,
        staticGraph: nx.Graph,
        dynamicGraph: nx.Graph,
        staticStateList: list,
        dynamicStateList: list,
        staticTime: float,
        dynamicTimeList: list,
    ) -> None:
        self._staticN = staticN
        self._dynamicN = dynamicN
        self._staticGraph = staticGraph
        self._dynamicGraph = dynamicGraph
        self._staticStateList = staticStateList
        self._dynamicStateList = dynamicStateList
        self._staticTime = staticTime
        self._dynamicTimeList = np.linspace(
                dynamicTimeList[0], dynamicTimeList[1], int(
                    dynamicTimeList[1]))
        self._staticQWAK = QWAK(self._staticGraph)
        self._staticQWAK.runWalk(
            time=self._staticTime,
            initStateList=self._staticStateList)
        self._dynamicQWAK = QWAK(self._dynamicGraph)
        self._staticQWAK.runWalk(
            time=self._dynamicTimeList[0],
            initStateList=self._dynamicStateList[0])
        self._dynamicProbDistList = []
        self._dynamicAmpList = []

    def runWalk(self):
        try:
            self._staticQWAK.resetWalk()
            self._staticQWAK.runWalk(
                self._staticTime, self._staticStateList)
        except StateOutOfBounds as err:
            return [True, str(err)]
        qwProbabilities = self._staticQWAK.getProbDist()
        qwProbVec = qwProbabilities.getProbVec()
        probLists = qwProbVec.tolist()
        return [False, probLists]

    def runMultipleWalks(self):
        try:
            self._dynamicQWAK.resetWalk()
            self._dynamicQWAK.runMultipleWalks(timeList=self._dynamicTimeList,initStateList=self._dynamicStateList[0])
            self._dynamicAmpList = self._dynamicQWAK.getWalkList()
            self._dynamicProbDistList = self._dynamicQWAK.getProbDistList()
            qwProbVecList = list(map(lambda probVec: probVec.tolist(), self._dynamicQWAK.getProbVecList()))
        except (StateOutOfBounds,UndefinedTimeList,EmptyProbDistList) as err:
            return [True, str(err)]
        return [False, qwProbVecList]

    def setStaticDim(self, newDim, graphStr):
        self._staticN = newDim
        self._staticQWAK.setDim(self._staticN, graphStr)
        self._staticGraph = self._staticQWAK.getGraph()

    def setDynamicDim(self, newDim, graphStr):
        self._dynamicN = newDim
        self._dynamicQWAK.setDim(self._dynamicN, graphStr)
        self._dynamicGraph = self._dynamicQWAK.getGraph()

    def getStaticDim(self):
        return self._staticN

    def getDynamicDin(self):
        return self._dynamicN

    def setStaticGraph(self, newGraphStr):
        self._staticGraph = eval(newGraphStr + f"({self._staticN})")
        self._staticQWAK.setGraph(self._staticGraph)

    def setDynamicGraph(self, newGraphStr):
        self._dynamicGraph = eval(newGraphStr + f"({self._dynamicN})")
        self._dynamicQWAK.setGraph(self._dynamicGraph)

    def getStaticGraph(self):
        return self._staticGraph

    def getDynamicGraph(self):
        return self._dynamicGraph

    def getStaticGraphToJson(self):
        return nx.cytoscape_data(self._staticGraph)

    def getDynamicGraphToJson(self):
        return nx.cytoscape_data(self._dynamicGraph)

    def setStaticTime(self, newTime):
        self._staticTime = eval(newTime)
        self._staticQWAK.setTime(self._staticTime)

    def getStaticTime(self):
        return self._staticTime

    def setDynamicTime(self, newTimeList):
        parsedTime = list(map(float, newTimeList.split(",")))
        self._dynamicTimeList = np.linspace(
                parsedTime[0], parsedTime[1], int(
                    parsedTime[1]))
        self._dynamicQWAK.setTimeList(self._dynamicTimeList)

    def getDynamicTime(self):
        return self._dynamicTimeList

    def setDynamicInitStateList(self, newInitStateList):
        parsedInitState = newInitStateList.split(";")
        self._dynamicStateList = []
        for initState in parsedInitState:
            self._dynamicStateList.append(
                list(map(int, initState.split(","))))

    def setStaticInitState(self, initStateStr):
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

    def getStaticSurvivalProb(self, k0, k1):
        # TODO: Make JS throw an error if k0 or k1 are not defined.
        return self._staticQWAK.getSurvivalProb(k0, k1)

    def getDynamicSurvivalProb(self, k0, k1):
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

    def checkPST(self, nodeA, nodeB):
        # TODO: Make JS throw an error if k0 or k1 are not defined.
        return str(self._staticQWAK.checkPST(nodeA, nodeB))

    def customGraphWalk(self, customAdjacency):
        # TODO: Running the custom graph set graph button throws an
        # error if the field on the prob dist side is not with correct
        # dimension. check out how to fix this.
        # TODO: This function needs rework
        self._staticQWAK.setAdjacencyMatrix(customAdjacency)
        initState = State(self._staticQWAK.getDim())
        initState.buildState([self._staticQWAK.getDim() // 2])
        self._staticQWAK.setInitState(initState)
        self._dynamicQWAK.setInitState(initState)
        self._staticQWAK.runWalk(self._staticTime)
        self._dynamicQWAK.setAdjacencyMatrix(customAdjacency)
        self._dynamicQWAK.runWalk(self._staticTime)
