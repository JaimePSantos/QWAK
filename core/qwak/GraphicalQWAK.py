import os

import networkx as nx
import numpy as np
import copy
from numpy import pi
from typing import Union
import json

from qwak.Errors import StateOutOfBounds, UndefinedTimeList, EmptyProbDistList, MissingNodeInput
from qwak.State import State
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import (
    ProbabilityDistribution,
)
from qwak.qwak import QWAK


class GraphicalQWAK:
    def __init__(
        self,
        staticN: int,
        dynamicN: int,
        staticGraph: nx.Graph,
        dynamicGraph: nx.Graph,
        staticStateList: list,
        dynamicStateList: list,
        staticTime: float,
        dynamicTimeList: list,
        qwakId: str = 'undefinedUser',
    ) -> None:
        """_summary_

        Parameters
        ----------
        staticN : int
            _description_
        dynamicN : int
            _description_
        staticGraph : nx.Graph
            _description_
        dynamicGraph : nx.Graph
            _description_
        staticStateList : list
            _description_
        dynamicStateList : list
            _description_
        staticTime : float
            _description_
        dynamicTimeList : list
            _description_
        """
        self._staticN = staticN
        self._dynamicN = dynamicN
        self._staticGraph = staticGraph
        self._dynamicGraph = dynamicGraph
        self._staticStateList = staticStateList
        self._dynamicStateList = dynamicStateList
        self._staticTime = staticTime
        self._dynamicTime = dynamicTimeList
        self._dynamicTimeList = np.linspace(
            self._dynamicTime[0], self._dynamicTime[1], int(
                self._dynamicTime[1]))
        self._staticQWAK = QWAK(self._staticGraph)
        # self._staticProbDist = self._staticQWAK.getProbDist()
        # self._dynamicQWAK = QWAK(self._dynamicGraph)
        # self._dynamicProbDistList = self._dynamicQWAK.getProbDistList()
        # self._dynamicAmpList = self._dynamicQWAK.getWalkList()
        self._qwakId = qwakId

    def to_json(self):
        """_summary_

        Returns
        -------
        str
            _description_
        """
        return json.dumps({
            'staticN': self._staticN,
            'dynamicN': self._dynamicN,
            'staticGraph': nx.node_link_data(self._staticGraph),
            'dynamicGraph': nx.node_link_data(self._dynamicGraph),
            'staticStateList': self._staticStateList,
            'dynamicStateList': self._dynamicStateList,
            'staticTime': self._staticTime,
            'dynamicTime': self._dynamicTime,
            'staticQWAK': json.loads(self._staticQWAK.to_json()),
            # 'dynamicQWAK': json.loads(self._dynamicQWAK.to_json()),
            # 'staticProbDist': self._staticProbDist.to_json(),
            # 'dynamicProbDistList':  list(map(lambda prob: prob.to_json(),self._dynamicProbDistList)),
            # 'dynamicAmpList': self._dynamicAmpList,
            'qwakId': self._qwakId
        })

    @classmethod
    def from_json(cls, json_var: Union[str, dict]):
        """_summary_

        Parameters
        ----------
        json_str : str
            _description_

        Returns
        -------
        Operator
            _description_
        """
        if isinstance(json_var, str):
            data = json.loads(json_var)
        elif isinstance(json_var, dict):
            data = json_var
        staticN = data['staticN']
        dynamicN = data['dynamicN']
        staticGraph = nx.node_link_graph(data['staticGraph'])
        dynamicGraph = nx.node_link_graph(data['dynamicGraph'])
        staticStateList = data['staticStateList']
        dynamicStateList = data['dynamicStateList']
        staticTime = data['staticTime']
        dynamicTime = data['dynamicTime']
        staticQWAK = QWAK.from_json(data['staticQWAK'])
        # dynamicQWAK = QWAK.from_json(data['dynamicQWAK'])
        # staticProbDist = ProbabilityDistribution.from_json(
        #     data['staticProbDist'])
        # dynamicProbDistList =  data['dynamicProbDistList']
        # dynamicAmpList =  data['dynamicAmpList']
        qwakId = data['qwakId']
        # print(staticQWAK.getProbDist().getDim())
        # print(f"Dict\t GQWAK {data['staticQWAK']['probDist']['state']['n']}")
        # print(f"Obj\t GQWAK {staticQWAK.getProbDist().getState().getDim()}")
        # print(staticN)
        # print(staticQWAK.getWalk().getFinalState())
        newGQwak = cls(
            staticN=staticN,
            dynamicN=dynamicN,
            staticGraph=staticGraph,
            dynamicGraph=dynamicGraph,
            staticStateList=staticStateList,
            dynamicStateList=dynamicStateList,
            staticTime=staticTime,
            dynamicTimeList=dynamicTime,
            qwakId=qwakId)
        # print(f"BEFORE SET {newGQwak.getStaticProbDist().getDim()}")
        # newGQwak.setDynamicTimeList(dynamicTimeList)
        newGQwak.setStaticQWAK(staticQWAK)
        # print(f"AFTER SET {newGQwak.getStaticProbDist().getDim()}")
        # newGQwak.setDynamicQWAK(dynamicQWAK)
        # newGQwak.setStaticProbDist(staticProbDist)
        # newGQwak.setDynamicProbDistList(dynamicProbDistList)
        # newGQwak.setDynamicWalkList(dynamicAmpList)

        # return ("nothing")
        return staticQWAK

    def getQwakId(self):
        return self._qwakId

    def setQwakId(self, newId):
        self._qwakId = newId

    def setStaticQWAK(self, newStaticQWAK):
        self._staticQWAK.setQWAK(newStaticQWAK)

    def getStaticQWAK(self):
        return self._staticQWAK

    def setDynamicQWAK(self, newDynamicQWAK):
        self._dynamicQWAK.setQWAK(newDynamicQWAK)

    def setDynamicTimeList(self, newTimeList):
        self._dynamicQWAK.setTimeList(newTimeList)
        self._dynamicTimeList = self._dynamicQWAK.getTimeList()

    def getStaticWalk(self):
        return self._staticQWAK.getWalk()

    def runWalk(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        try:
            # self._staticQWAK.resetWalk()
            self._staticQWAK.runWalk(
                self._staticTime, self._staticStateList)
            self._staticProbDist = self._staticQWAK.getProbDist()
            qwProbVec = self._staticProbDist.getProbVec().tolist()
            return [False, qwProbVec]
        except StateOutOfBounds as err:
            return [True, str(err)]

    def runMultipleWalks(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        try:
            self._dynamicQWAK.resetWalk()
            self._dynamicQWAK.runMultipleWalks(
                timeList=self._dynamicTimeList,
                initStateList=self._dynamicStateList[0])
            self._dynamicAmpList = self._dynamicQWAK.getWalkList()
            self._dynamicProbDistList = self._dynamicQWAK.getProbDistList()
            qwProbVecList = list(
                map(lambda probVec: probVec.tolist(), self._dynamicQWAK.getProbVecList()))
            return [False, qwProbVecList]
        except (StateOutOfBounds, UndefinedTimeList, EmptyProbDistList) as err:
            return [True, str(err)]

    def setStaticDim(self, newDim, graphStr, initStateList=None):
        """_summary_

        Parameters
        ----------
        newDim : _type_
            _description_
        graphStr : _type_
            _description_
        initStateList : _type_, optional
            _description_, by default None
        """
        self._staticN = newDim
        self._staticQWAK.setDim(
            self._staticN,
            graphStr=graphStr,
            initStateList=initStateList)
        self._staticGraph = self._staticQWAK.getGraph()

    def setDynamicDim(self, newDim, graphStr):
        """_summary_

        Parameters
        ----------
        newDim : _type_
            _description_
        graphStr : _type_
            _description_
        """
        self._dynamicN = newDim
        self._dynamicQWAK.setDim(self._dynamicN, graphStr)
        self._dynamicGraph = self._dynamicQWAK.getGraph()

    def getStaticDim(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticN

    def getDynamicDim(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._dynamicN

    def setStaticGraph(self, newGraphStr):
        """_summary_

        Parameters
        ----------
        newGraphStr : _type_
            _description_
        """
        self._staticGraph = eval(newGraphStr + f"({self._staticN})")
        self._staticN = len(self._staticGraph)
        self._staticQWAK.setGraph(self._staticGraph)

    def setDynamicGraph(self, newGraphStr):
        """_summary_

        Parameters
        ----------
        newGraphStr : _type_
            _description_
        """
        self._dynamicGraph = eval(newGraphStr + f"({self._dynamicN})")
        self._dynamicN = len(self._dynamicGraph)
        self._dynamicQWAK.setGraph(self._dynamicGraph)

    def setStaticCustomGraph(self, customAdjacency):
        """_summary_

        Parameters
        ----------
        customAdjacency : _type_
            _description_
        """
        self._staticGraph = nx.from_numpy_matrix(customAdjacency)
        self._staticQWAK.setGraph(self._staticGraph)
        self._staticN = len(self._staticGraph)
        self._staticStateList = [self._staticN // 2]
        self._staticQWAK.setDim(
            self._staticN,
            graph=self._staticGraph,
            initStateList=self._staticStateList)

    def setDynamicCustomGraph(self, customAdjacency):
        """_summary_

        Parameters
        ----------
        customAdjacency : _type_
            _description_
        """
        self._dynamicGraph = nx.from_numpy_matrix(customAdjacency)
        self._dynamicQWAK.setGraph(self._dynamicGraph)
        self._dynamicN = len(self._dynamicGraph)
        self._dynamicStateList = [[self._dynamicN // 2]]
        self._dynamicQWAK.setDim(
            self._dynamicN,
            graph=self._dynamicGraph,
            initStateList=self._dynamicStateList)

    def getStaticGraph(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticGraph

    def getDynamicGraph(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._dynamicGraph

    def getStaticGraphToJson(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return nx.cytoscape_data(self._staticGraph)

    def getDynamicGraphToJson(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return nx.cytoscape_data(self._dynamicGraph)

    def getStaticAdjacencyMatrix(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticQWAK.getAdjacencyMatrix()

    def getDynamicAdjacencyMatrix(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._dynamicQWAK.getAdjacencyMatrix()

    def setStaticTime(self, newTime):
        """_summary_

        Parameters
        ----------
        newTime : _type_
            _description_
        """
        self._staticTime = eval(newTime)
        self._staticQWAK.setTime(self._staticTime)

    def getStaticTime(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticTime

    def setDynamicTime(self, newTimeList):
        """_summary_

        Parameters
        ----------
        newTimeList : _type_
            _description_
        """
        parsedTime = list(map(float, newTimeList.split(",")))
        self._dynamicTimeList = np.linspace(
            parsedTime[0], parsedTime[1], int(
                parsedTime[1]))
        self._dynamicQWAK.setTimeList(self._dynamicTimeList)

    def getDynamicTime(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._dynamicTimeList

    def setDynamicInitStateList(self, newInitStateList):
        """_summary_

        Parameters
        ----------
        newInitStateList : _type_
            _description_
        """
        parsedInitState = newInitStateList.split(";")
        self._dynamicStateList = []
        for initState in parsedInitState:
            self._dynamicStateList.append(
                list(map(int, initState.split(","))))

    def setStaticInitState(self, initStateStr):
        """_summary_

        Parameters
        ----------
        initStateStr : _type_
            _description_
        """
        self._staticStateList = []
        self._staticStateList = list(map(int, initStateStr.split(",")))
        newState = State(self._staticQWAK.getDim())
        newState.buildState(self._staticStateList)
        self._staticQWAK.setInitState(newState)

    def getStaticInitState(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticStateList

    def getDynamicInitStateList(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._dynamicStateList

    def getStaticProbDist(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticProbDist

    def setStaticProbDist(self, newStaticProbDist):
        self._staticProbDist.setProbDist(newStaticProbDist)

    def getDynamicProbDistList(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._dynamicProbDistList

    def setDynamicProbDistList(self, newDynamicProbDistList):
        self._dynamicProbDistList = newDynamicProbDistList
        self._dynamicQWAK.setProbDistList(self._dynamicProbDistList)

    def getDynamicWalkList(self):
        return self._dynamicAmpList

    def setDynamicWalkList(self, newWalkList):
        self._dynamicAmpList = newWalkList
        self._dynamicQWAK.setWalkList(self._dynamicAmpList)

    def getStaticProbVec(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticProbDist.getProbVec()

    def getDynamicProbVecList(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return list(map(lambda probVec: probVec.tolist(),
                        self._dynamicQWAK.getProbVecList()))

    def getStaticMean(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticQWAK.getMean()

    def getDynamicMean(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        meanList = []
        for probDist in self._dynamicProbDistList:
            meanList.append(probDist.mean())
        return meanList

    def getStaticSndMoment(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        # TODO: This not used in the GUI.
        return self._staticQWAK.getSndMoment()

    def getDynamicSndMoment(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        # TODO: This not used in the GUI.
        sndMomentList = []
        for probDist in self._dynamicProbDistList:
            sndMomentList.append(probDist.getSndMoment())
        return sndMomentList

    def getStaticStDev(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticQWAK.getStDev()

    def getDynamicStDev(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        stDevList = []
        for probDist in self._dynamicProbDistList:
            stDevList.append(probDist.stDev())
        return stDevList

    def getStaticSurvivalProb(self, k0, k1):
        """_summary_

        Parameters
        ----------
        k0 : _type_
            _description_
        k1 : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        try:
            return [False, self._staticQWAK.getSurvivalProb(k0, k1)]
        except MissingNodeInput as err:
            return [True, str(err)]

    def getDynamicSurvivalProb(self, k0, k1):
        """_summary_

        Parameters
        ----------
        k0 : _type_
            _description_
        k1 : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        try:
            survProbList = []
            for probDist in self._dynamicProbDistList:
                survProbList.append(probDist.survivalProb(k0, k1))
            return [False, survProbList]
        except MissingNodeInput as err:
            return [True, str(err)]

    def getStaticInversePartRatio(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._staticQWAK.getInversePartRatio()

    def getDynamicInvPartRatio(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        invPartRatioList = []
        for amps in self._dynamicAmpList:
            invPartRatioList.append(amps.invPartRatio())
        return invPartRatioList

    def checkPST(self, nodeA, nodeB):
        """_summary_

        Parameters
        ----------
        nodeA : _type_
            _description_
        nodeB : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        try:
            return [False, str(self._staticQWAK.checkPST(nodeA, nodeB))]
        except MissingNodeInput as err:
            return [True, str(err)]
