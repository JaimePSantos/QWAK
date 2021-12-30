from QuantumWalk.Operator import Operator
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.State import State


class QuantumWalkDao:
    """[summary]
    """

    def __init__(self, graph):
        """[summary]

        Args:
            graph ([type]): [description]
        """
        self._graph = graph
        self._operator = Operator(self._graph)
        self._n = len(self._graph)
        self._initState = State(self._n)
        self._time = 0
        self._gamma = 1
        self._initStateList = [1]

    def runWalk(self, time=0, gamma=1, initStateList=[1]):
        """[summary]

        Args:
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
            initStateList (list, optional): [description]. Defaults to [1].
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

    def buildWalk(self):
        """[summary]
        """
        self._initState.buildState(self._initStateList)
        self._operator.buildDiagonalOperator(self._time, self._gamma)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.buildProbDist()

    def setDim(self, newDim, graphStr):
        """[summary]

        Args:
            newDim ([type]): [description]
            graphStr ([type]): [description]
        """
        self._n = newDim
        self._graph = eval(graphStr + f"({self._n})")
        self._n = len(self._graph)
        self._initStateList = [int(self._n / 2)]
        self._initState = State(self._n)
        self._operator = Operator(self._graph)

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def setGraph(self, newGraph):
        """[summary]

        Args:
            newGraph ([type]): [description]
        """
        self._graph = newGraph
        self._operator = Operator(self._graph)
        self._n = len(self._graph)

    def getGraph(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._graph

    def setInitState(self, newInitState):
        """[summary]

        Args:
            newInitState ([type]): [description]
        """
        self._initState.setState(newInitState)
        self._initStateList = self._initState.getStateList()

    def getInitState(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._initState

    def setTime(self, newTime):
        """[summary]

        Args:
            newTime ([type]): [description]
        """
        self._time = newTime

    def getTime(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._time

    def setGamma(self, newGamma):
        """[summary]

        Args:
            newGamma ([type]): [description]
        """
        self._gamma = newGamma

    def getGamma(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._gamma

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._operator.setOperator(newOperator)

    def getOperator(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._operator

    def setWalk(self, newWalk):
        """[summary]

        Args:
            newWalk ([type]): [description]
        """
        self._quantumWalk.setWalk(newWalk)

    def getWalk(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._quantumWalk.getWalk()

    def setProbDist(self, probDist):
        """[summary]

        Args:
            probDist ([type]): [description]
        """
        self._probDist = probDist

    def getProbDist(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._probDist.getProbDist()

    def getStateAmplitude(self, state):
        """[summary]

        Args:
            state ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._quantumWalk.getStateAmplitude(state)

    def getStateProbability(self, state):
        """[summary]

        Args:
            state ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._probDist.getStateProbability(state)
