import networkx as nx
import numpy as np
import copy

from qwak.Errors import StateOutOfBounds, NonUnitaryState, UndefinedTimeList, EmptyProbDistList,MissingNodeInput
from qwak.State import State
from qwak.Operator import Operator, StochasticOperator
from qwak.QuantumWalk import QuantumWalk, StochasticQuantumWalk
from qwak.ProbabilityDistribution import (
    ProbabilityDistribution,
    StochasticProbabilityDistribution,
)

from qutip import Qobj, basis, mesolve, Options


class QWAK:
    """Data access class that combines all three components required to
    perform a continuous-time quantum walk, given by the multiplication of
    an operator (represented by the Operator class) by an initial state
    (State class).  This multiplication is achieved in the
    StaticQuantumwalk class, which returns a final state (State Class)
    representing the amplitudes of each state associated with a graph node.
    These amplitudes can then be transformed to probability distributions
    (ProbabilityDistribution class) suitable for plotting with matplotlib,
    or your package of choice.
    """

    def __init__(
        self,
        graph: nx.Graph,
        time: float = None,
        timeList: list = None,
        initStateList: list = None,
        customStateList: list = None,
        laplacian: bool = False,
        markedSearch: list = None,
    ) -> None:
        """Default values for the initial state, time and transition rate are a
        column vector full of 0s, 0 and 1, respectively. Methods runWalk or
        buildWalk must then be used to generate the results of the quantum
        walk.

        Parameters
        ----------
        graph : nx.Graph
            NetworkX graph where the walk takes place. Also used
            for defining the dimensions of the quantum walk.
        time : float
            __ Needs completion __
        timeList : list
            __ Needs completion __
        initStateList : list[int], optional
            List with chosen initial states for uniform superposition, by default None
        customStateList : list[(int,complex)], optional
            Custom init state, by default None.
        laplacian : bool, optional
            Allows the user to choose whether to use the
            Laplacian or simple adjacency matrix, by default False.
        markedSearch : list, optional
            List with marked elements for search, by default None.
        """
        if timeList is not None:
            self._timeList = timeList
        else:
            self._timeList = None
        self._graph = graph
        self._n = len(self._graph)
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
        self._probDistList = [ProbabilityDistribution(
            self._quantumWalk.getFinalState())]
        self._walkList = []

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
            _description_
        nUErr
            _description_
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
        """_summary_

        Parameters
        ----------
        timeList : list, optional
            _description_, by default None
        initStateList : list, optional
            _description_, by default None
        customStateList : list, optional
            _description_, by default None

        Raises
        ------
        UndefinedTimeList
            _description_
        """
        # TODO: Decide if we should reset walk here.
        # self.resetWalk()
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
            self._walkList.append(copy.deepcopy(self.getWalk()))

    def resetWalk(self) -> None:
        """Resets the components of a walk."""
        self._initState.resetState()
        self._operator.resetOperator()
        self._quantumWalk.resetWalk()
        self._probDist.resetProbDist()
        self._probDistList = []
        self._walkList = []

    def setDim(self, newDim: int, graphStr: str,
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
        initStateList : list[int], optional
            Init state list with new dimension.
        """
        # TODO: We should probably remove the graphStr as user input and just
        # make it a class attribute. There isnt a way to get the name of the
        # graph generator though.
        self._n = newDim
        self._graph = eval(graphStr + f"({self._n})")
        self._n = len(self._graph)
        self._initState = State(self._n, initStateList)
        self._operator = Operator(self._graph)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())

    def getDim(self) -> int:
        """Gets the current graph dimension.
        Returns
        -------
        int
            Dimension of graph.
        """
        return self._n

    def setGraph(self, newGraph: nx.Graph) -> None:
        """Sets the current graph to a user defined one.
        Also recalculates the current operator and walk dimension.

        Parameters
        ----------
        newGraph : nx.Graph
            New NetworkX graph.
        """
        self._n = len(self._graph)
        self._graph = newGraph
        self._operator = Operator(self._graph)

    def getGraph(self) -> nx.Graph:
        """Gets the current graph.

        Returns
        -------
        nx.Graph
            Current graph.
        """
        return self._graph

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
        """_summary_

        Parameters
        ----------
        newTime : list
            _description_
        """
        self._timeList = newTimeList

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
        """_summary_

        Parameters
        ----------
        newAdjMatrix : np.ndarray
            _description_
        initStateList : list, optional
            _description_, by default None
        """
        self._n = len(self._operator.getAdjacencyMatrix())
        self._operator.setAdjacencyMatrix(newAdjMatrix)
        self._initState = State(self._n, initStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())

    def getAdjacencyMatrix(self) -> np.ndarray:
        """_summary_

        Returns:
            np.ndarray: _description_
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

    def getWalkList(self) -> list:
        """_summary_

        Returns
        -------
        list
            _description_
        """
        return self._walkList

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

    def getAmpVecList(self) -> list:
        """_summary_

        Returns
        -------
        list
            _description_
        """
        return list(map(lambda x: x.getAmpVec(), self._walkList))

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
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        if not self._probDistList:
            raise EmptyProbDistList(
                f"Prob. dist. list is {self._probDistList}. Perhaps you didnt run multiple walks?")
        return self._probDistList

    def getProbVec(self) -> np.ndarray:
        """Gets the current probability distribution vector.

        Returns
        -------
        np.ndarray
            Probability Distribution vector.
        """
        return self._probDist.getProbVec()

    def getProbVecList(self) -> list:
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return list(
            map(lambda probDist: probDist.getProbVec(), self._probDistList))

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
        nodeA = int(nodeA)
        nodeB = int(nodeB)
        return self._operator.checkPST(nodeA, nodeB)

    def getMean(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._probDist.moment(1)

    def getSndMoment(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._probDist.moment(2)

    def getStDev(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._probDist.stDev()

    def getSurvivalProb(self, k0, k1):
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
            return self._probDist.survivalProb(k0, k1)
        except MissingNodeInput as err:
            raise err

    def getInversePartRatio(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._quantumWalk.invPartRatio()

    def getTransportEfficiency(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._quantumWalk.transportEfficiency()


class StochasticQWAK:
    """_summary_"""

    def __init__(
        self,
        graph: nx.Graph,
        initStateList=None,
        customStateList=None,
        noiseParam=None,
        sinkNode=None,
        sinkRate=None,
    ) -> None:
        """_summary_

        Parameters
        ----------
        graph : nx.Graph
            _description_
        initStateList : _type_, optional
            _description_, by default None
        customStateList : _type_, optional
            _description_, by default None
        noiseParam : _type_, optional
            _description_, by default None
        sinkNode : _type_, optional
            _description_, by default None
        sinkRate : _type_, optional
            _description_, by default None
        """
        self._graph = graph
        self._n = len(self._graph)
        self._operator = StochasticOperator(
            self._graph,
            noiseParam=noiseParam,
            sinkNode=sinkNode,
            sinkRate=sinkRate,
        )
        self._initState = State(
            self._n,
            nodeList=initStateList,
            customStateList=customStateList)
        self._quantumWalk = StochasticQuantumWalk(
            self._initState, self._operator)
        self._probDist = StochasticProbabilityDistribution(
            self._quantumWalk)

    def runWalk(
        self,
        time: float = 0,
        initStateList: list = None,
        customStateList=None,
        noiseParam=None,
        sinkNode=None,
        sinkRate=None,
        observables=[],
        opts=Options(store_states=True, store_final_state=True),
    ) -> None:
        """_summary_

        Parameters
        ----------
        time : float, optional
            _description_, by default 0
        initStateList : list, optional
            _description_, by default None
        customStateList : _type_, optional
            _description_, by default None
        noiseParam : _type_, optional
            _description_, by default None
        sinkNode : _type_, optional
            _description_, by default None
        sinkRate : _type_, optional
            _description_, by default None
        observables : list, optional
            _description_, by default []
        opts : _type_, optional
            _description_, by default Options(store_states=True, store_final_state=True)

        Raises
        ------
        stOBErr
            _description_
        nUErr
            _description_
        """
        # TODO: Move the constructors to the constructor method.
        try:
            self._initState.buildState(
                nodeList=initStateList, customStateList=customStateList
            )
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildStochasticOperator(
            noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate
        )
        self._quantumWalk = StochasticQuantumWalk(
            self._initState, self._operator)
        self._quantumWalk.buildWalk(time, observables, opts)
        self._probDist = StochasticProbabilityDistribution(
            self._quantumWalk)
        self._probDist.buildProbDist()

    def setProbDist(self, newProbDist: object) -> None:
        """_summary_

        Parameters
        ----------
        newProbDist : object
            _description_
        """
        self._probDist = newProbDist

    def getProbDist(self) -> ProbabilityDistribution:
        """_summary_

        Returns
        -------
        ProbabilityDistribution
            _description_
        """
        return self._probDist

    def getProbVec(self) -> ProbabilityDistribution:
        """_summary_

        Returns
        -------
        ProbabilityDistribution
            _description_
        """
        return self._probDist.getProbVec()

    def getQuantumHamiltonian(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._operator.getQuantumHamiltonian()

    def getClassicalHamiltonian(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._operator.getClassicalHamiltonian()

    def getLaplacian(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._operator.getLaplacian()
