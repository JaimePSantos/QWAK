from __future__ import annotations
from typing import Union

import networkx as nx
import cupy as cp
import copy
import json
from qwak_cupy.Errors import (
    StateOutOfBounds,
    NonUnitaryState,
    UndefinedTimeList,
    EmptyProbDistList,
    MissingNodeInput,
    MissingGraphInput,
)
from qwak_cupy.State import State
from qwak_cupy.Operator import Operator
from qwak_cupy.QuantumWalk import QuantumWalk
from qwak_cupy.ProbabilityDistribution import (
    ProbabilityDistribution,
)


class QWAK:
    def __init__(
            self,
            graph: nx.Graph,
            time: float = 0,
            timeList: list = None,
            gamma: float = 1,
            initStateList: list = None,
            customStateList: list = None,
            laplacian: bool = False,
            markedElements: list = [],
            qwakId: str = 'userUndef',
    ) -> None:
        self._graph = graph
        self._n = len(self._graph)
        if timeList is not None:
            self._timeList = [x for x in timeList]
        else:
            self._timeList = [0] * self._n
        self._qwakId = qwakId
        self._operator = Operator(
            self._graph,
            time=time,
            gamma=gamma,
            laplacian=laplacian,
            markedElements=markedElements)
        self._initState = State(
            self._n,
            nodeList=initStateList,
            customStateList=customStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())
        self._probDistList = cp.array([])

    def runWalk(
            self,
            time: float = 0,
            initStateList: list = None,
            customStateList: list = None) -> None:
        try:
            self._initState.buildState(
                nodeList=initStateList, customStateList=customStateList
            )
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildDiagonalOperator(time=time)
        self._quantumWalk.buildWalk(self._initState, self._operator)
        self._probDist.buildProbDist(self._quantumWalk.getFinalState())

    def runExpmWalk(
            self,
            time: float = 0,
            initStateList: list = None,
            customStateList: list = None) -> None:
        try:
            self._initState.buildState(
                nodeList=initStateList, customStateList=customStateList
            )
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildExpmOperator(time=time)
        self._quantumWalk.buildWalk(self._initState, self._operator)
        self._probDist.buildProbDist(self._quantumWalk.getFinalState())

    def runMultipleWalks(
            self,
            timeList: list = None,
            initStateList: list = None,
            customStateList: list = None) -> None:

        self._probDistList = []
        if timeList is not None:
            self._timeList = timeList
        elif self._timeList is None:
            raise UndefinedTimeList(f"TimeList is {self._timeList}.")
        for time in self._timeList:
            self.runWalk(
                time=time,
                initStateList=initStateList,
                customStateList=customStateList)
            self._probDistList.append(copy.deepcopy(self.getProbDist()))

    def runMultipleExpmWalks(
            self,
            timeList: list = None,
            initStateList: list = None,
            customStateList: list = None) -> None:

        self._probDistList = []
        if timeList is not None:
            self._timeList = timeList
        elif self._timeList is None:
            raise UndefinedTimeList(f"TimeList is {self._timeList}.")
        for time in self._timeList:
            self.runExpmWalk(
                time=time,
                initStateList=initStateList,
                customStateList=customStateList)
            self._probDistList.append(copy.deepcopy(self.getProbDist()))

    def setProbDist(self, newProbDist: ProbabilityDistribution) -> None:
        self._probDist.setProbDist(newProbDist)

    def getProbDist(self) -> ProbabilityDistribution:
        return self._probDist

    def getProbDistList(self) -> list:
        return self._probDistList

    def setProbDistList(self, newProbDistList: list) -> None:
        self._probDistList = newProbDistList

    def getProbVec(self) -> cp.ndarray:
        return self._probDist.getProbVec()

    def getProbVecList(self) -> list:
        return [probDist.getProbVec()
                for probDist in self._probDistList]

    def resetWalk(self) -> None:
        """Resets the components of a walk."""
        self._initState.resetState()
        self._operator.resetOperator()
        self._quantumWalk.resetWalk()
        self._probDist.resetProbDist()
        self._probDistList = []
        self._walkList = []

    def setDim(
            self,
            newDim: int,
            graphStr: str = None,
            graph: nx.Graph = None,
            initStateList: list = None) -> None:
        self._n = newDim
        if graphStr is not None:
            self._graph = eval(f"{graphStr}({self._n})")
            self._n = len(self._graph)
        elif graph is not None:
            self._graph = graph
            self._n = len(self._graph)
        else:
            raise MissingGraphInput(
                f"You tried to set QWAK dim without providing a graph with updated dimensions: {self._graph}")

        self._initState.setDim(newDim, newNodeList=initStateList)
        self._operator.setDim(newDim, self._graph)
        self._quantumWalk.setDim(newDim)
        self._probDist.setDim(newDim)

    def getGraph(self) -> nx.Graph:
        return self._graph

    def getDim(self) -> int:

        return self._n

    def setGraph(self, newGraph: nx.Graph, initStateList=None) -> None:
        self._graph = newGraph
        self._n = len(self._graph)

    def setCustomGraph(self, customAdjMatrix: cp.ndarray) -> None:
        self._graph = nx.from_numpy_array(customAdjMatrix)
        self.setGraph(newGraph=self._graph)
        self._initStateList = [self._n // 2]
        self.setDim(
            self._n,
            graph=self._graph,
            initStateList=self._initStateList)

    def setInitState(self, newInitState: State) -> None:
        self._initState.setState(newInitState)
        self._initStateList = self._initState.getNodeList()

    def setTime(self, newTime: float) -> None:
        self._operator.setTime(newTime)

    def setTimeList(self, newTimeList: list) -> None:
        timeList = cp.linspace(
            newTimeList[0], newTimeList[1], int(
                newTimeList[1]))
        self._timeList = timeList.tolist()

    def getTime(self) -> float:
        return self._operator.getTime()

    def getTimeList(self) -> float:
        return self._timeList

    def setAdjacencyMatrix(
            self, newAdjMatrix: cp.ndarray, initStateList: list = None
    ) -> None:
        newAdjMatrix = cp.array(newAdjMatrix)
        self._n = len(self._operator.getAdjacencyMatrix())
        self._operator.setAdjacencyMatrix(newAdjMatrix)
        self._initState = State(self._n, initStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())

    def getAdjacencyMatrix(self) -> cp.ndarray:
        return self._operator.getAdjacencyMatrix()

    def setHamiltonian(self, newHamiltonian: cp.ndarray) -> None:
        self._operator.setHamiltonian(newHamiltonian)

    def getHamiltonian(self) -> cp.ndarray:
        return self._operator.getHamiltonian()

    def setOperator(self, newOperator: Operator) -> None:

        self._operator.setOperator(newOperator)

    def getOperator(self) -> Operator:
        return self._operator

    def setWalk(self, newWalk: State) -> None:
        self._quantumWalk.setWalk(newWalk)

    def getWalk(self) -> QuantumWalk:
        return self._quantumWalk

    def getFinalState(self) -> State:
        return self._quantumWalk.getFinalState()

    def getAmpVec(self) -> cp.ndarray:
        return self._quantumWalk.getAmpVec()

    # def getQWAK(self) :
    #     """Gets the QWAK instance.
    #
    #     Returns
    #     -------
    #     QWAK
    #         QWAK instance.
    #     """
    #     return self._qwak

    def setQWAK(self, newQWAK: QWAK) -> None:
        """Sets the QWAK instance's attributes to the ones of the given QWAK instance.

        Parameters
        ----------
        newQWAK : QWAK
            QWAK instance to copy the attributes from.
        """
        self.setGraph(newQWAK.getGraph())
        self.setDim(newQWAK.getDim(), graph=self._graph)
        self.setInitState(newQWAK.getInitState())
        self.setOperator(newQWAK.getOperator())
        self.setWalk(newQWAK.getWalk())
        self.setProbDist(newQWAK.getProbDist())

    def searchNodeAmplitude(self, searchNode: int) -> complex:
        """User inputted node for search

        Parameters
        ----------
        searchNode : int
            User inputted node for the search.

        Returns
        -------
        complex
            Amplitude associated with the search node.
        """
        return self._quantumWalk.searchNodeAmplitude(searchNode)

    def searchNodeProbability(self, searchNode: int) -> float:
        """Searches and gets the probability associated with a given node.

        Parameters
        ----------
        searchNode : int
            User inputted node for the search.

        Returns
        -------
        float
            Probability associated with the search node.
        """
        return self._probDist.searchNodeProbability(searchNode)

    def getMean(self, resultRounding: int = None) -> float:
        """Gets the mean of the probability distribution.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the result, by default None.

        Returns
        -------
        float
            Mean of the probability distribution.
        """
        return self._probDist.moment(1) if (
                resultRounding is None) \
            else round(self._probDist.moment(1), resultRounding)

    def getMeanList(self, resultRounding: int = None) -> list:
        """Gets the mean of the probability distribution list.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the results, by default None.

        Returns
        -------
        list
            List of means of the probability distributions.
        """
        return [
            probDist.moment(1) for probDist in self._probDistList] if (
                resultRounding is None) \
            else [
            round(
                probDist.moment(1),
                resultRounding) for probDist in self._probDistList]

    def getSndMoment(self, resultRounding: int = None) -> float:
        """Gets the second moment of the probability distribution.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the result, by default None.

        Returns
        -------
        float
            Second moment of the probability distribution.
        """
        return self._probDist.moment(2) if (resultRounding is None) \
            else round(
            self._probDist.moment(2), resultRounding)

    def getStDev(self, resultRounding: int = None) -> float:
        """Gets the standard deviation of the probability distribution.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the result, by default None.

        Returns
        -------
        float
            Standard deviation of the probability distribution.
        """
        return self._probDist.stDev() if (resultRounding is None) \
            else round(
            self._probDist.stDev(),
            resultRounding)

    def getStDevList(self, resultRounding: int = None) -> list:
        """Gets the standard deviation of the probability distribution list.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the results, by default None.

        Returns
        -------
        list
            List of standard deviations of the probability distributions.
        """
        return [
            probDist.stDev() for probDist in self._probDistList] if (
                resultRounding is None) \
            else [
            round(
                probDist.stDev(),
                resultRounding) for probDist in self._probDistList]

    def getInversePartRatio(self, resultRounding: int = None) -> float:
        """Gets the inverse participation ratio of the probability distribution.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the result, by default None.

        Returns
        -------
        float
            Inverse participation ratio of the probability distribution.
        """
        return self._probDist.invPartRatio() if (
                resultRounding is None) \
            else round(
            self._probDist.invPartRatio(), resultRounding)

    def getInversePartRatioList(
            self, resultRounding: int = None) -> list:
        """Gets the inverse participation ratio of the probability distribution list.

        Parameters
        ----------
        resultRounding : int, optional
            Rounding of the results, by default None.

        Returns
        -------
        list
            List of inverse participation ratios of the probability distributions.
        """
        return [
            probDist.invPartRatio() for probDist in self._probDistList] if (
                resultRounding is None) else [
            round(
                probDist.invPartRatio(),
                resultRounding) for probDist in self._probDistList]

    def getSurvivalProb(
            self,
            fromNode,
            toNode,
            resultRounding: int = None) -> float:
        """Gets the survival probability of the probability distribution.

        Parameters
        ----------
        fromNode : _type_
            Starting node.
        toNode : _type_
            Ending node.
        resultRounding : int, optional
            Rounding of the result, by default None.

        Returns
        -------
        float
            Survival probability of the probability distribution.

        Raises
        ------
        MissingNodeInput
            Missing input node error.
        """
        try:
            return self._probDist.survivalProb(
                fromNode,
                toNode) if (
                    resultRounding is None) else round(
                self._probDist.survivalProb(
                    fromNode,
                    toNode),
                resultRounding)
        except MissingNodeInput as err:
            raise err

    def getSurvivalProbList(
            self,
            fromNode,
            toNode,
            resultRounding: int = None) -> list:
        """Gets the survival probability of the probability distribution list.

        Parameters
        ----------
        fromNode : _type_
            Starting node.
        toNode : _type_
            Ending node.
        resultRounding : int, optional
            Rounding of the results, by default None.

        Returns
        -------
        list
            List of survival probabilities of the probability distributions.

        Raises
        ------
        MissingNodeInput
            Missing input node error.
        """
        try:
            return [
                probDist.survivalProb(
                    fromNode,
                    toNode) for probDist in self._probDistList] if (
                    resultRounding is None) else [
                round(
                    probDist.survivalProb(
                        fromNode,
                        toNode),
                    resultRounding) for probDist in self._probDistList]
        except MissingNodeInput as err:
            raise err