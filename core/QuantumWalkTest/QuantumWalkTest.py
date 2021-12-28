import numpy as np
from QuantumWalkTest.StateTest import StateTest
import timeit
import warnings
warnings.filterwarnings("ignore")


class QuantumWalkTest:
    """[summary]
    """

    def __init__(self, state, operator):
        """[summary]

        Args:
            state ([type]): [description]
            operator ([type]): [description]
        """
        self._n = state.getDim()
        self._initState = state.getStateVec()
        self._operator = operator.getOperator()
        self._finalState = StateTest(self._n)
        self.walkExecutionTime = 0

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return '%s' % self._finalState.getStateVec()

    def buildWalk(self):
        """[summary]
        """
        self._finalState.setStateVec(
            np.matmul(self._operator, self._initState))

    def timedBuildWalk(self):
        """[summary]
        """
        startTimeWalk = timeit.default_timer()
        self.buildWalk()
        endTimeWalk = timeit.default_timer()
        self.walkExecutionTime = (endTimeWalk - startTimeWalk)

    def setInitState(self, newInitState):
        """[summary]

        Args:
            newInitState ([type]): [description]
        """
        self._initState = newInitState

    def getInitState(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._initState

    def setDim(self, newDim):
        """[summary]

        Args:
            newDim ([type]): [description]
        """
        self._n = newDim

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._operator = newOperator

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
        self._initState = newWalk.getInitState()
        self._operator = newWalk.getOperator()
        self._finalState = newWalk.getWalk()

    def getWalk(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._finalState

    def getStateAmplitude(self, state):
        """[summary]

        Args:
            state ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._finalState.getStateVec().item(state)
