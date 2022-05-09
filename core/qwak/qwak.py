import networkx as nx

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from qwak.Operator import Operator, StochasticOperator
from qwak.QuantumWalk import QuantumWalk, StochasticQuantumWalk
from qwak.ProbabilityDistribution import (
        ProbabilityDistribution,
        StochasticProbabilityDistribution,
        )

from qutip import Qobj, basis, mesolve, Options

class QWAK:
    """
    Data access class that combines all three components required to
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
            initStateList=None,
            customStateList=None,
            laplacian: bool = False,
            markedSearch=None,
            ) -> None:
        """
        Default values for the initial state, time and transition rate are a
        column vector full of 0s, 0 and 1, respectively. Methods runWalk or
        buildWalk must then be used to generate the results of the quantum
        walk.

        Args:
            :param laplacian: Allows the user to choose whether to use the
            Laplacian or simple adjacency matrix.
            :type laplacian: bool
            :param graph: NetworkX graph where the walk takes place. Also used
            for defining the dimensions of the quantum walk.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        self._n = len(self._graph)
        self._operator = Operator(self._graph, laplacian=laplacian, markedSearch=markedSearch)
        self._initState = State(self._n, nodeList=initStateList, customStateList=customStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(self._quantumWalk.getFinalState())

    def runWalk(
            self, time: float = 0, initStateList: list = None, customStateList=None
            ) -> None:
        """
        Builds class' attributes, runs the walk and calculates the amplitudes
        and probability distributions with the given parameters. These can be
        accessed with their respective get methods.

        Args:
            :param time: Time for which to calculate the quantum walk. Defaults to 0.
            :type time: (int, optional)
            :param gamma: Transition rate of the given walk. Defaults to 1.
            :type gamma: (int, optional)
            :param initStateList: List with chosen initial states. Defaults to [0].
            :type initStateList: (list, optional)
        """
        try:
            self._initState.buildState(nodeList = initStateList, customStateList=customStateList)
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildDiagonalOperator(time=time)
        self._quantumWalk.buildWalk(self._initState,self._operator)
        self._probDist.buildProbDist(self._quantumWalk.getFinalState())

    def resetWalk(self):
        self._initState.resetState()
        self._operator.resetOperator()
        self._quantumWalk.resetWalk()

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
        self._initState = State(self._n, self._initStateList)
        self._operator = Operator(self._graph)

    def getDim(self) -> int:
        """
        Gets the current graph dimension.

        Returns:
            :return: self._n
            :rtype: int
        """
        return self._n

    def setAdjacencyMatrix(self, newAdjMatrix):
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
        self._operator.setTime(newTime)

    def getTime(self) -> float:
        """
        Gets the current walk time.

        Returns:
            :return: self._time
            :rtype: float
        """
        return self._operator.getTime()

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

    def getFinalState(self) -> State:
        """
        Gets current walk amplitudes, also known as final state.

        Returns:
            :return: self._quantumWalk.getWalk()
            :rtype: State
        """
        return self._quantumWalk.getFinalState()

    def getAmpVec(self) -> State:
        """
        Gets current walk amplitudes, also known as final state.

        Returns:
            :return: self._quantumWalk.getWalk()
            :rtype: State
        """
        return self._quantumWalk.getAmpVec()

    def setProbDist(self, newProbDist: object) -> None:
        """
        Sets current walk probability distribution to a user defined one.
        This might not be needed and removed in the future.

        Args:
            :param newProbDist: New probability distribution.
            :type newProbDist: ProbabilityDistribution
        """
        self._probDist.setProbDist(newProbDist)

    def getProbDist(self) -> ProbabilityDistribution:
        """
        Gets the current probability distribution.

        Returns:
            :return: self._probDist.getProbDist()
            :rtype: ProbabilityDistribution
        """
        return self._probDist

    def getProbDistVec(self) -> ProbabilityDistribution:
        """
        Gets the current probability distribution.

        Returns:
            :return: self._probDist.getProbDist()
            :rtype: ProbabilityDistribution
        """
        return self._probDist.getProbVec()

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

    def checkPST(self, nodeA, nodeB):
        nodeA = int(nodeA)
        nodeB = int(nodeB)
        return self._operator.checkPST(nodeA, nodeB)

    def getMean(self):
        return self._probDist.moment(1)

    def getSndMoment(self):
        return self._probDist.moment(2)

    def getStDev(self):
        return self._probDist.stDev()

    def getSurvivalProb(self, k0, k1):
        return self._probDist.survivalProb(k0, k1)

    def getInversePartRatio(self):
        return self._quantumWalk.invPartRatio()

    def getTransportEfficiency(self):
        return self._quantumWalk.transportEfficiency()


class StochasticQWAK:
    """
    Data access class that combines all three components required to
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
            initStateList=None,
            customStateList=None,
            noiseParam=None,
            sinkNode=None,
            sinkRate=None,
            ) -> None:
        """
        Default values for the initial state, time and transition rate are a
        column vector full of 0s, 0 and 1, respectively. Methods runWalk or
        buildWalk must then be used to generate the results of the quantum
        walk.

        Args:
            :param laplacian: Allows the user to choose whether to use the
            Laplacian or simple adjacency matrix.
            :type laplacian: bool
            :param graph: NetworkX graph where the walk takes place. Also used
            for defining the dimensions of the quantum walk.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        self._n = len(self._graph)
        self._operator = StochasticOperator(
                graph,
                noiseParam=noiseParam,
                sinkNode=sinkNode,
                sinkRate=sinkRate,
                )
        self._initState = State(self._n, nodeList = initStateList, customStateList = customStateList)

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
        """
        Builds class' attributes, runs the walk and calculates the amplitudes
        and probability distributions with the given parameters. These can be
        accessed with their respective get methods.

        Args:
            :param time: Time for which to calculate the quantum walk. Defaults to 0.
            :type time: (int, optional)
            :param gamma: Transition rate of the given walk. Defaults to 1.
            :type gamma: (int, optional)
            :param initStateList: List with chosen initial states. Defaults to [0].
            :type initStateList: (list, optional)
        """
        try:
            self._initState.buildState(nodeList = initStateList, customStateList = customStateList) 
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildStochasticOperator(noiseParam = noiseParam, sinkNode = sinkNode, sinkRate = sinkRate)
        self._quantumWalk = StochasticQuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk(time,observables,opts)
        self._probDist = StochasticProbabilityDistribution(self._quantumWalk)
        self._probDist.buildProbDist()

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

    def getProbVec(self) -> ProbabilityDistribution:
        """
        Gets the current probability distribution.

        Returns:
            :return: self._probDist.getProbDist()
            :rtype: ProbabilityDistribution
        """
        return self._probDist.getProbVec()

    def getQuantumHamiltonian(self):
        return self._operator.getQuantumHamiltonian()

    def getClassicalHamiltonian(self):
        return self._operator.getClassicalHamiltonian()

    def getLaplacian(self):
        return self._operator.getLaplacian()
