import warnings

import numpy as np

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator

warnings.filterwarnings("ignore")


class QuantumWalk:
    """
    Class that represents the final state containing the amplitudes of a
    continuous-time quantum walk.

    """

    def __init__(self, state: State, operator: Operator) -> None:
        """
        This object is initialized with a user inputted initial state and
        operator.
        The dimension of the quantum walk will then be loaded from the initial
        state.
        The final state will contain the amplitudes of the time evolution of
        the initial state, as a function of the operator. This variable is initialized
        as a state class.

        Args:
            :param state: Initial state which will be the basis of the time dependant evolution.
            :type state: State
            :param operator: Operator which will evolve the initial state.
            :type operator: Operator.
        """
        self._n = state.getDim()
        self._initState = state.getStateVec()
        self._operator = operator.getOperator()
        self._finalState = State(self._n)

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
