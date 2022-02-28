import networkx as nx
import numpy as np

from qwak.Operator import Operator
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.QuantumWalk import QuantumWalk
from qwak.State import State


class QWAK:
    """
        Data access class that combines all three components required to perform a continuous-time quantum walk,
        given by the multiplication of an operator (represented by the Operator class) by an initial
        state (State class).
        This multiplication is achieved in the StaticQuantumwalk class, which returns a final state (State
        Class) representing the amplitudes of each state associated with a graph node.
        These amplitudes can then be transformed to probability distributions (ProbabilityDistribution class) suitable
        for plotting with matplotlib, or your package of choice.
    """

    def __init__(self, graph: nx.Graph, laplacian:bool = False,markedSearch = None) -> None:
        """
        Default values for the initial state, time and transition rate are a column vector full of 0s, 0 and 1,
        respectively. Methods runWalk or buildWalk must then be used to generate the results of the quantum walk.

        Args:
            :param laplacian: Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
            :type laplacian: bool
            :param graph: NetworkX graph where the walk takes place. Also used for defining the dimensions of the quantum walk.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        if markedSearch is not None:
            self._operator = Operator(self._graph, laplacian, markedSearch=markedSearch)
        else:
            self._operator = Operator(self._graph,laplacian)
        self._n = len(self._graph)
        self._initStateList = [0]
        self._initState = State(self._n,self._initStateList)
        self._time = 0

    def resetWalk(self):
        self._initState.resetState()
        self._operator.resetOperator()
        self._quantumWalk.resetWalk()

    def runWalk(self, time: float = 0, initStateList: list = [0]) -> None:
        """
        Builds class' attributes, runs the walk and calculates the amplitudes and probability distributions
        with the given parameters. These can be accessed with their respective get methods.

        Args:
            :param time: Time for which to calculate the quantum walk. Defaults to 0.
            :type time: (int, optional)
            :param gamma: Transition rate of the given walk. Defaults to 1.
            :type gamma: (int, optional)
            :param initStateList: List with chosen initial states. Defaults to [0].
            :type initStateList: (list, optional)
        """
        self._time = time
        self._initStateList = initStateList
        self._initState.buildState(self._initStateList)
        self._operator.buildDiagonalOperator(self._time)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.buildProbDist()

    def setDim(self, newDim: int, graphStr: str) -> None:
        """
        Sets the current walk dimensions to a user defined one.
        Also takes a graph string to be
        evaluated and executed as a NetworkX graph generator.

        Args:
            :param newDim: New dimension for the quantum walk.
            :type newDim: int
            :param graphStr: Graph string to generate the graph with the new dimension.
            :type graphStr: str
        """
        self._n = newDim
        self._graph = eval(graphStr + f"({self._n})")
        self._n = len(self._graph)
        self._initStateList = [int(self._n / 2)]
        self._initState = State(self._n,self._initStateList)
        self._operator = Operator(self._graph)

    def getDim(self) -> int:
        """
        Gets the current graph dimension.

        Returns:
            :return: self._n
            :rtype: int
        """
        return self._n

    def setAdjacencyMatrix(self,newAdjMatrix):
        self._operator.setAdjacencyMatrix(newAdjMatrix)
        self._n = len(self._operator.getAdjacencyMatrix())
        self._initStateList = [int(self._n / 2)]
        self._initState = State(self._n)
        self._initState.buildState(self._initStateList)

    def getAdjacencyMatrix(self):
        return self._operator.getAdjacencyMatrix()

    def setGraph(self, newGraph: nx.Graph) -> None:
        """
        Sets the current graph to a user defined one.
        Also recalculates the current operator and walk dimension.

        Args:
            :param newGraph: New NetworkX graph.
            :type newGraph: NetworkX.Graph
        """
        self._n = len(self._graph)
        self._graph = newGraph
        self._operator = Operator(self._graph)

    def getGraph(self) -> nx.Graph:
        """
        Gets the current graph.

        Returns:
            :return: self._graph
            :rtype: NetworkX.Graph
        """
        return self._graph

    def setInitState(self, newInitState: State) -> None:
        """
        Sets the current initial state to a user defined one.

        Args:
            :param newInitState: New initial state.
            :type newInitState: State
        """
        self._initState.setState(newInitState)
        self._initStateList = self._initState.getNodeList()

    def getInitState(self) -> State:
        """
        Gets the initial state.

        Returns:
            :return: self._initState
            :rtype: State
        """
        return self._initState

    def setTime(self, newTime: float) -> None:
        """
        Sets the current walk time to a user defined one.

        Args:
            :param newTime: New time.
            :type newTime: float
        """
        self._time = newTime

    def getTime(self) -> float:
        """
        Gets the current walk time.

        Returns:
            :return: self._time
            :rtype: float
        """
        return self._time

    def setOperator(self, newOperator: Operator) -> None:
        """
        Sets the current walk operator a user defined one.

        Args:
            :param newOperator: New operator.
            :type newOperator: Operator
        """
        self._operator.setOperator(newOperator)

    def getOperator(self):
        """
        Gets the current walk operator.

        Returns:
            :return: self._operator
            :rtype: Operator
        """
        return self._operator

    def setWalk(self, newWalk: State) -> None:
        """
        Sets current walk amplitudes to a user defined state.
        This might not be needed and removed in the future.

        Args:
            :param newWalk: New walk amplitudes.
            :type newWalk: State
        """
        self._quantumWalk.setWalk(newWalk)

    def getWalk(self) -> State:
        """
        Gets current walk amplitudes, also known as final state.

        Returns:
            :return: self._quantumWalk.getWalk()
            :rtype: State
        """
        return self._quantumWalk

    def setProbDist(self, newProbDist: object) -> None:
        """
        Sets current walk probability distribution to a user defined one.
        This might not be needed and removed in the future.

        Args:
            :param newProbDist: New probability distribution.
            :type newProbDist: ProbabilityDistribution
        """
        self._probDist = newProbDist

    def getProbDist(self) -> ProbabilityDistribution:
        """
        Gets the current probability distribution.

        Returns:
            :return: self._probDist.getProbDist()
            :rtype: ProbabilityDistribution
        """
        return self._probDist

    def searchNodeAmplitude(self, searchNode: int) -> complex:
        """
        Searches and gets the amplitude associated with a given node.

        Args:
            :param searchNode: User inputted node for the search.
            :type searchNode: int

        Returns:
            :return: self._quantumWalk.searchNodeAmplitude(searchNode)
            :rtype: complex

        """
        return self._quantumWalk.searchNodeAmplitude(searchNode)

    def searchNodeProbability(self, searchNode: int) -> float:
        """
        Searches and gets the probability associated with a given node.

        Args:
            :param searchNode: User inputted node for the search.
            :type searchNode: int

        Returns:
            :return: self._probDist.searchNodeProbability(searchNode)
            :rtype: float
        """
        return self._probDist.searchNodeProbability(searchNode)

    def checkPST(self,nodeA,nodeB):
        nodeA = int(nodeA)
        nodeB = int(nodeB)
        return self._operator.checkPST(nodeA,nodeB)

    def transportEfficiency(self):
        return self._operator.transportEfficiency(self._initState.getStateVec())

    def getMean(self):
        return self._probDist.moment(1)

    def getSndMoment(self):
        return self._probDist.moment(2)

    def getStDev(self):
        return self._probDist.stDev()

    def getSurvivalProb(self,k0,k1):
        return self._probDist.survivalProb(k0,k1)

    def getInversePartRatio(self):
        return self._quantumWalk.invPartRatio()

