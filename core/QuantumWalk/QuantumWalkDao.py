import networkx as nx

from QuantumWalk.Operator import Operator
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.State import State


class QuantumWalkDao:
    """
        Data access class that combines all three components required to perform a continuous-time quantum walk,
        given by the multiplication of an operator (represented by the Operator class) by an initial
        state (State class).
        This multiplication is achieved in the QuantumWalk class, which returns a final state (State
        Class) representing the amplitudes of each state associated with a graph node.
        These amplitudes can then be transformed to probability distributions (ProbabilityDistribution class) suitable
        for plotting with matplotlib, or your package of choice.
    """

    def __init__(self, graph: nx.Graph) -> (()):
        """
        Default values for the initial state, time and transition rate are a column vector full of 0s, 0 and 1,
        respectively. Methods runWalk or buildWalk must then be used to generate the results of the quantum walk.

        Args:
            :param graph: NetworkX graph where the walk takes place. Also used for defining the dimensions of the quantum walk.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        self._operator = Operator(self._graph)
        self._n = len(self._graph)
        self._initState = State(self._n)
        self._time = 0
        self._gamma = 1
        self._initStateList = [0]

    def runWalk(self, time: float = 0, gamma: float = 1, initStateList: list = [0]) -> ():
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
        self._gamma = gamma
        self._initStateList = initStateList
        self._initState.buildState(self._initStateList)
        self._operator.buildDiagonalOperator(self._time, self._gamma)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.buildProbDist()

    def buildWalk(self) -> ():
        """
        Given the current values of the class' attributes, runs the walk and calculates the amplitudes and probability
        distributions.
        """
        self._initState.buildState(self._initStateList)
        self._operator.buildDiagonalOperator(self._time, self._gamma)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.buildProbDist()

    def setDim(self, newDim: int, graphStr: str) -> ():
        """
        Changes the current walk dimensions to a user defined one.
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
        self._initState = State(self._n)
        self._operator = Operator(self._graph)

    def getDim(self) -> int:
        """
        Gets the current graph dimension.

        Returns:
            :return: self._n
            :rtype: int
        """
        return self._n

    def setGraph(self, newGraph: nx.Graph) -> ():
        """
        Changes the current graph to a user defined one.
        Also recalculates the current operator and walk dimension.

        Args:
            :param newGraph: New NetworkX graph.
            :type newGraph: NetworkX.Graph
        """
        self._graph = newGraph
        self._operator = Operator(self._graph)
        self._n = len(self._graph)

    def getGraph(self) -> nx.Graph:
        """
        Gets the current graph.

        Returns:
            :return: self._graph
            :rtype: NetworkX.Graph
        """
        return self._graph

    def setInitState(self, newInitState: State) -> ():
        """
        Changes the current initial state to a user defined one.

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

    def setTime(self, newTime: float) -> ():
        """
        Changes the current walk time to a user defined one.

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

    def setGamma(self, newGamma: float) -> ():
        """
        Changes the current walk transition rate to a user defined one.

        Args:
            :param newGamma: New transition rate.
            :type newGamma: float
        """
        self._gamma = newGamma

    def getGamma(self) -> float:
        """
        Gets the current walk transition rate.

        Returns:
            :return: self._gamma
            :rtype: float
        """
        return self._gamma

    def setOperator(self, newOperator: Operator) -> ():
        """
        Changes the current walk operator a user defined one.

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

    def setWalk(self, newWalk: State) -> ():
        """
        Changes current walk amplitudes to a user defined state.
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
        return self._quantumWalk.getWalk()

    def setProbDist(self, newProbDist: object) -> ():
        """
        Changes current walk probability distribution to a user defined one.
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
        return self._probDist.getProbDist()

    def getNodeAmplitude(self, searchNode: int) -> complex:
        """
        Searches and gets the amplitude associated with a given node.

        Args:
            :param searchNode: User inputted node for the search.
            :type searchNode: int

        Returns:
            :return: self._quantumWalk.getStateAmplitude(searchNode)
            :rtype: complex

        """
        return self._quantumWalk.getStateAmplitude(searchNode)

    def getNodeProbability(self, searchNode: int) -> float:
        """
        Searches and gets the probability associated with a given node.

        Args:
            :param searchNode: User inputted node for the search.
            :type searchNode: int

        Returns:
            :return: self._probDist.getStateProbability(searchNode)
            :rtype: float
        """
        return self._probDist.getStateProbability(searchNode)
