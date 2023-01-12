from __future__ import annotations
from typing import Union

import networkx as nx
import numpy as np
import copy
import json
from qwak.Errors import (
    StateOutOfBounds,
    NonUnitaryState,
    UndefinedTimeList,
    EmptyProbDistList,
    MissingNodeInput,
    MissingGraphInput,
)
from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import (
    ProbabilityDistribution,
)


class QWAK:
    def __init__(
        self,
        graph: nx.Graph,
        time: float = None,
        timeList: list = None,
        initStateList: list = None,
        customStateList: list = None,
        laplacian: bool = False,
        markedSearch: list = None,
        qwakId: str = 'userUndef',
    ) -> None:
        """Data access class that combines all three components required to
        perform a continuous-time quantum walk, given by the multiplication of
        an operator (represented by the Operator class) by an initial state
        (State class).  This multiplication is achieved in the
        StaticQuantumwalk class, which returns a final state (State Class)
        representing the amplitudes of each state associated with a graph node.
        These amplitudes can then be transformed to probability distributions
        (ProbabilityDistribution class) suitable for plotting with matplotlib,
        or your package of choice.
        
        Default values for the initial state, time and transition rate are a
        column vector full of 0s, 0 and 1, respectively. Methods runWalk or
        buildWalk must then be used to generate the results of the quantum
        walk.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph where the walk takes place. Also used
            for defining the dimensions of the quantum walk.
        time : float
            Time interval for the quantum walk, by default None.
        timeList : list
            List with time intervals for multiple walks, by default None.
        initStateList : list[int], optional
            List with chosen initial states for uniform superposition, by default None
        customStateList : list[(int,complex)], optional
            Custom init state, by default None.
        laplacian : bool, optional
            Allows the user to choose whether to use the
            Laplacian or simple adjacency matrix, by default False.
        markedSearch : list, optional
            List with marked elements for search, by default None.
        qwakId : str, optional
            User-defined ID for the QWAK instance, by default 'userUndef'.
        """
        self._graph = graph
        self._n = len(self._graph)
        if timeList is not None:
            self._timeList = np.array(timeList)
        else:
            self._timeList = np.zeros(self._n)
        self._qwakId = qwakId
        self._operator = Operator(
            self._graph,
            time=time,
            laplacian=laplacian,
            markedSearch=markedSearch)
        self._initState = State(
            self._n,
            nodeList=initStateList,
            customStateList=customStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)

        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())

        self._probDistList = []

    def to_json(self, isDynamic=False) -> str:
        """Returns a JSON representation of the QWAK instance

        Parameters
        ----------
        isDynamic : bool, optional
            If True, the JSON will contain the timeList, probDistList and
            walkList attributes, by default False.

        Returns
        -------
        str
            JSON representation of the QWAK instance.
        """        
        if isDynamic:
            qwakJson = json.dumps({
                'dim': self._n,
                'graph': nx.node_link_data(self._graph),
                'timeList': self._timeList.tolist(),
                'initState': json.loads(self._initState.to_json()),
                'operator': json.loads(self._operator.to_json()),
                'quantumWalk': json.loads(self._quantumWalk.to_json()),
                'probDistList': [probDist.to_json() for probDist in self._probDistList],
                'qwakId': self._qwakId
            })
        else:
            qwakJson = json.dumps({
                'dim': self._n,
                'graph': nx.node_link_data(self._graph),
                'initState': json.loads(self._initState.to_json()),
                'operator': json.loads(self._operator.to_json()),
                'quantumWalk': json.loads(self._quantumWalk.to_json()),
                'probDist': json.loads(self._probDist.to_json()),
                'qwakId': self._qwakId
            })
        return qwakJson

    @classmethod
    def from_json(cls, json_var: str, isDynamic=False) -> QWAK:
        """Returns a QWAK instance from a JSON representation.

        Parameters
        ----------
        json_var : str
            JSON representation of the QWAK instance.
        isDynamic : bool, optional
            If True, the JSON will contain the timeList and probDistList attributes, 
            by default False.

        Returns
        -------
        QWAK
            QWAK instance from a JSON representation.
        """        
        if isinstance(json_var, str):
            data = json.loads(json_var)
        elif isinstance(json_var, dict):
            data = json_var
        qwakId = data['qwakId']
        graph = nx.node_link_graph(data['graph'])

        initState = State.from_json(data['initState'])
        operator = Operator.from_json(data['operator'])
        quantumWalk = QuantumWalk.from_json(data['quantumWalk'])
        if isDynamic:
            timeList = data['timeList']
            newQwak = cls(graph=graph, timeList=timeList, qwakId=qwakId)
            probDistList = [ProbabilityDistribution.from_json(
                probDist) for probDist in data['probDistList']]
            newQwak.setProbDistList(probDistList)
        else:
            probDist = ProbabilityDistribution.from_json(
                data['probDist'])
            newQwak = cls(graph=graph, qwakId=qwakId)
            newQwak.setProbDist(probDist)
        newQwak.setInitState(initState)
        newQwak.setOperator(operator)
        newQwak.setWalk(quantumWalk)
        return newQwak

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

    def runWalk(
            self,
            time: float = None,
            initStateList: list = None,
            customStateList: list = None) -> None:
        """Builds class' attributes, runs the walk and calculates the amplitudes
        and probability distributions with the given parameters. These can be
        accessed with their respective get methods.

        Parameters
        ----------
        time : float, optional
            Time for which to calculate the quantum walk, by default 0.
        initStateList : list[int], optional
            List with chosen initial states for uniform superposition, by default None.
        customStateList : list[(int,complex)], optional
            Custom init state, by default None.

        Raises
        ------
        stOBErr
            State out of bounds exception.
        nUErr
            State not unitary exception.
        """
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

    def runMultipleWalks(
            self,
            timeList: list = None,
            initStateList: list = None,
            customStateList: list = None) -> None:
        """Runs the walk for multiple times and stores the probability distributions
        in a list.

        Parameters
        ----------
        timeList : list, optional
            List of times for which to calculate the quantum walk, by default None.
        initStateList : list, optional
            List with chosen initial states for uniform superposition, by default None.
        customStateList : list, optional
            Custom init state, by default None.

        Raises
        ------
        UndefinedTimeList
            Raised when the timeList is None.
        """
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
        """Sets the current walk dimensions to a user defined one.
        Also takes a graph string to be
        evaluated and executed as a NetworkX graph generator.

        Parameters
        ----------
        newDim : int
            New dimension for the quantum walk.
        graphStr : str
            Graph string to generate the graph with the new dimension.
        graph : nx.Graph, optional
            Graph with the new dimension.
        initStateList : list[int], optional
            Init state list with new dimension.
        """
        self._n = newDim
        if graphStr is not None:
            self._graph = eval(f"{graphStr}({self._n})")
            # We need a reassignment here since certain graphs have
            # different length than the number inputted.
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

    def getDim(self) -> int:
        """Gets the current graph dimension.

        Returns
        -------
        int
            Dimension of graph.
        """
        return self._n

    def setGraph(self, newGraph: nx.Graph, initStateList=None) -> None:
        """Sets the current graph to a user defined one.
        Also recalculates the current operator and walk dimension.

        Parameters
        ----------
        newGraph : nx.Graph
            New NetworkX graph.
        """
        self._graph = newGraph
        self._n = len(self._graph)
        self.setDim(self._n, graph=self._graph)

    def getGraph(self) -> nx.Graph:
        """Gets the current graph.

        Returns
        -------
        nx.Graph
            Current graph.
        """
        return self._graph

    def setCustomGraph(self, customAdjMatrix: np.ndarray) -> None:
        """Sets the current graph to a user defined one.

        Parameters
        ----------
        customAdjMatrix : np.ndarray
            Adjacency matrix of the new graph.
        """        
        self._graph = nx.from_numpy_matrix(customAdjMatrix)
        self.setGraph(newGraph=self._graph)
        self._initStateList = [self._n // 2]
        self.setDim(
            self._n,
            graph=self._graph,
            initStateList=self._initStateList)

    def setInitState(self, newInitState: State) -> None:
        """Sets the current initial state to a user defined one.

        Parameters
        ----------
        newInitState : State
            New initial state.
        """
        self._initState.setState(newInitState)
        self._initStateList = self._initState.getNodeList()

    def getInitState(self) -> State:
        """Gets the initial state.

        Returns
        -------
        State
            Initial State.
        """
        return self._initState

    def setTime(self, newTime: float) -> None:
        """Sets the current walk time to a user defined one.

        Parameters
        ----------
        newTime : float
            New time.
        """
        self._operator.setTime(newTime)

    def setTimeList(self, newTimeList: list) -> None:
        """Sets the current walk time to a user defined one.

        Parameters
        ----------
        newTimeList : list
            New time list.
        """
        timeList = np.linspace(
            newTimeList[0], newTimeList[1], int(
                newTimeList[1]))
        self._timeList = timeList

    def getTime(self) -> float:
        """Gets the current walk time.

        Returns
        -------
        float
           Current value of time.
        """
        return self._operator.getTime()

    def getTimeList(self) -> float:
        """Gets the current walk time.

        Returns
        -------
        float
           Current value of time.
        """
        return self._timeList

    def setAdjacencyMatrix(
            self, newAdjMatrix: np.ndarray, initStateList: list = None
    ) -> None:
        """Sets the current adjacency matrix to a user defined one.

        Parameters
        ----------
        newAdjMatrix : np.ndarray
            New adjacency matrix.
        initStateList : list, optional
            New initial state list, by default None.
        """
        self._n = len(self._operator.getAdjacencyMatrix())
        self._operator.setAdjacencyMatrix(newAdjMatrix)
        self._initState = State(self._n, initStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())

    def getAdjacencyMatrix(self) -> np.ndarray:
        """Gets the current adjacency matrix.

        Returns:
            np.ndarray:
                Current adjacency matrix.
        """
        return self._operator.getAdjacencyMatrix()

    def setOperator(self, newOperator: Operator) -> None:
        """Sets the current walk operator a user defined one.

        Parameters
        ----------
        newOperator : Operator
            New operator object.
        """
        self._operator.setOperator(newOperator)

    def getOperator(self) -> Operator:
        """Gets the current walk operator.

        Returns
        -------
        Operator
            Current operator object.
        """
        return self._operator

    def setWalk(self, newWalk: State) -> None:
        """Sets current walk amplitudes to a user defined state.
        This might not be needed and removed in the future.

        Parameters
        ----------
        newWalk : State
            New walk amplitudes.
        """
        self._quantumWalk.setWalk(newWalk)

    def getWalk(self) -> QuantumWalk:
        """Gets current QuantumWalk object

        Returns
        -------
        QuantumWalk
            Current state amplitudes.
        """
        return self._quantumWalk

    def getFinalState(self) -> State:
        """Gets current QuantumWalk State.

        Returns
        -------
        State
            State of the QuantumWalk.
        """
        return self._quantumWalk.getFinalState()

    def getAmpVec(self) -> np.ndarray:
        """Gets the array of the QuantumWalk state.

        Returns
        -------
        np.ndarray
            Array of the QuantumWalk state.
        """
        return self._quantumWalk.getAmpVec()

    def setProbDist(self, newProbDist: ProbabilityDistribution) -> None:
        """Sets current walk probability distribution to a user defined one.
        This might not be needed and removed in the future.

        Parameters
        ----------
        newProbDist : ProbabilityDistribution
            New probability distribution.
        """
        self._probDist.setProbDist(newProbDist)

    def getProbDist(self) -> ProbabilityDistribution:
        """Gets the current probability distribution.

        Returns
        -------
        ProbabilityDistribution
            ProbabilityDistribution object.
        """
        return self._probDist

    def getProbDistList(self) -> list:
        """Returns a list of probability distributions in the case of multiple walks.

        Returns
        -------
        list
            List of ProbabilityDistribution objects.
        """
        if not self._probDistList:
            raise EmptyProbDistList(
                f"Prob. dist. list is {self._probDistList}. Perhaps you didnt run multiple walks?")
        return self._probDistList

    def setProbDistList(self, newProbDistList: list) -> None:
        """Sets the current probability distribution list to a user defined one.

        Parameters
        ----------
        newProbDistList : list
            New probability distribution list.
        """        
        self._probDistList = newProbDistList

    def getProbVec(self) -> np.ndarray:
        """Gets the current probability distribution vector.

        Returns
        -------
        np.ndarray
            Probability Distribution vector.
        """
        return self._probDist.getProbVec()

    def getProbVecList(self) -> list:
        """Returns a list of probability distribution vectors in the case of multiple walks.

        Returns
        -------
        list
            List of probability distribution vectors.
        """
        return [probDist.getProbVec()
                for probDist in self._probDistList]

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

    def getMeanList(self, resultRounding: int =None) -> list:
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

    def getInversePartRatioList(self, resultRounding: int = None) -> list:
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

    def getSurvivalProb(self, fromNode, toNode, resultRounding: int = None) -> float:
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
            return self._probDist.survivalProb(fromNode, toNode) if(resultRounding is None) else round(self._probDist.survivalProb(fromNode, toNode),resultRounding)
        except MissingNodeInput as err:
            raise err

    def getSurvivalProbList(self, fromNode, toNode, resultRounding: int = None) -> list:
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

    def checkPST(self, fromNode, toNode) -> Union([str,bool]):
        """Checks if a structure allows for PST between certain nodes.

        Parameters
        ----------
        fromNode : _type_
            Starting node.
        toNode : _type_
            Ending node.
        Returns
        -------
        Union([str,bool])
            _description_

        Raises
        ------
        MissingNodeInput
            Missing input node error.
            
        """        
        try:
            return self._operator.checkPST(nodeA, nodeB)
        except MissingNodeInput as err:
            raise err

    def getTransportEfficiency(self)->float:
        """Gets the transport efficiency of the quantum walk.

        Returns
        -------
        float
            Transport efficiency of the quantum walk.
        """
        return self._quantumWalk.transportEfficiency()
