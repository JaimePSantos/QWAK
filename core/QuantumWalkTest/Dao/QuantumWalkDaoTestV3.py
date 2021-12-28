from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest

from QuantumWalkTest.Operator.OperatorTestV3 import OperatorTestV3

import timeit


class QuantumWalkDaoTestV3:
    """[summary]
    """

    def __init__(self, graph, time=0, gamma=1, initStateList=[0]):
        """[summary]

        Args:
            graph ([type]): [description]
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
            initStateList (list, optional): [description]. Defaults to [0].
        """
        startTimeDao = timeit.default_timer()

        self._graph = graph
        self._n = len(self._graph)
        self._initState = StateTest(self._n, initStateList)
        self._initState.timedBuildState()

        self._operator = OperatorTestV3(self._graph, time, gamma)
        print(
            "######### Running: ln.Eig * [D] @ ln.EigH #####################\n")
        self._operator.timedBuildDiagonalOperator()
        print(
            "######### Completed: np.Eig * [D] @ ln.EigH ###################\n")
        self._quantumWalk = QuantumWalkTest(
            self._initState, self._operator)
        self._quantumWalk.timedBuildWalk()
        self._probDist = ProbabilityDistributionTest(
            self._quantumWalk.getWalk())
        self._probDist.timedBuildProbDist()
        self.initTimes()

        endTimeDao = timeit.default_timer()

        self.daoExecutionTime = endTimeDao - startTimeDao

    def initTimes(self):
        """[summary]
        """
        self.initStateExecutionTime = self._initState.stateExecutionTime
        self.eighExecutionTime = self._operator.eighExecutionTime
        self.diagExecutionTime = self._operator.diagExecutionTime
        self.matMulExecutionTime = self._operator.matMulExecutionTime
        self.fullExecutionTime = self._operator.fullExecutionTime
        self.walkExecutionTime = self._quantumWalk.walkExecutionTime
        self.probDistExecutionTime = self._probDist.probDistExecutionTime

    def timedRunWalk(self):
        """[summary]
        """
        self._initState.timedBuildState()
        self._operator.timedBuildDiagonalOperator()
        self._quantumWalk.timedBuildWalk()
        self._probDist.timedBuildProbDist()

    def setInitState(self, newInitState):
        """[summary]

        Args:
            newInitState ([type]): [description]
        """
        self._initState.setState(newInitState)

    def getInitState(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._initState

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