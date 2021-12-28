from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest

from QuantumWalkTest.Operator.OperatorTestV4 import OperatorTestV4


class QuantumWalkDaoTestV4:
    """[summary]
    """

    def __init__(self, graph, time=0, gamma=1, initStateList=[0], version=None):
        """[summary]

        Args:
            graph ([type]): [description]
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
            initStateList (list, optional): [description]. Defaults to [0].
            version ([type], optional): [description]. Defaults to None.
        """
        self._graph = graph
        self._n = len(self._graph)

        self._operator = OperatorTestV4(self._graph)
        self.resetTimes()
        self.eighExecutionTime = self._operator.eighExecutionTime
        self.tempEigh = self.eighExecutionTime

    def resetTimes(self):
        """[summary]
        """
        self.initStateExecutionTime = 0
        self.eighExecutionTime = 0
        self.diagExecutionTime = 0
        self.matMulExecutionTime = 0
        self.fullOperatorExecutionTime = 0
        self.walkExecutionTime = 0
        self.probDistExecutionTime = 0

    def initTimes(self):
        """[summary]
        """
        self.initStateExecutionTime = self._initState.stateExecutionTime
        self.diagExecutionTime = self._operator.diagExecutionTime
        self.matMulExecutionTime = self._operator.matMulExecutionTime
        self.fullOperatorExecutionTime = self._operator.fullExecutionTime
        self.walkExecutionTime = self._quantumWalk.walkExecutionTime
        self.probDistExecutionTime = self._probDist.probDistExecutionTime

    def optRunWalk(self, time, gamma, initStateList):
        """[summary]

        Args:
            time ([type]): [description]
            gamma ([type]): [description]
            initStateList ([type]): [description]
        """
        print(
            "######### Running Optimized: np.Eig * [D] @ np.EigH ##########\n")
        self._operator.timedBuildDiagonalOperator(time, gamma)
        print(
            "######### Completed Optimized: ln.Eig * [D] @ ln.EigH ########\n")

        self._initState = StateTest(self._n, initStateList)
        self._initState.timedBuildState()

        self._quantumWalk = QuantumWalkTest(self._initState, self._operator)
        self._quantumWalk.timedBuildWalk()

        self._probDist = ProbabilityDistributionTest(
            self._quantumWalk.getWalk())
        self._probDist.timedBuildProbDist()

        self.initTimes()
        self.daoExecutionTime = self.initStateExecutionTime + self.tempEigh + self.diagExecutionTime + \
            self.matMulExecutionTime + self.walkExecutionTime + self.probDistExecutionTime
        self.tempEigh = 0  # So eigh execution time is only added once.

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