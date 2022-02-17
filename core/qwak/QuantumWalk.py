from __future__ import annotations

import warnings

import numpy as np

from qwak.State import State
from qwak.Operator import Operator

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
        as an instance of State class.

        Args:
            :param state: Initial state which will be the basis of the time dependant evolution.
            :type state: State
            :param operator: Operator which will evolve the initial state.
            :type operator: Operator.
        """
        self._n = state.getDim()
        self._initState = state
        self._operator = operator
        self._finalState = State(self._n)

    def __str__(self) -> str:
        """
        String representation of the StaticQuantumwalk class.

        Returns:
            :return: f'{self._finalState.getStateVec()}'
            :rtype: str
        """
        return f'{self._finalState.getStateVec()}'

    def resetWalk(self):
        self._operator.resetOperator()
        self._initState.resetState()
        self._finalState.resetState()

    def buildWalk(self) -> None:
        """
        Builds the final state of the quantum walk by setting it to the matrix
        multiplication of the operator by the initial state.
        """
        self._finalState.setStateVec(
            np.matmul(self._operator.getOperator(), self._initState.getStateVec()))

    def setInitState(self, newInitState: State) -> None:
        """
        Sets the initial state of the quantum walk to a new user inputted one.

        Args:
            :param newInitState: New initial state for the quantum walk.
            :type newInitState: State
        """
        self._initState.setState(newInitState)

    def getInitState(self) -> State:
        """
        Gets the initial state of the quantum walk.

        Returns:
            :return: self._initState
            :rtype: State
        """
        return self._initState

    def setDim(self, newDim: int) -> None:
        """
        Sets the current quantum walk dimension to a user defined one.

        Args:
            :param newDim: New quantum walk dimension.
            :type newDim: int
        """
        self._n = newDim

    def getDim(self) -> int:
        """
        Gets the current state dimension.

        Returns:
            :return: self._n
            :rtype: int
        """
        return self._n

    def setOperator(self, newOperator: Operator) -> None:
        """
        Sets the current operator to a user defined one.

        Args:
            :param newOperator: New quantum walk operator.
            :type newOperator: Operator
        """
        self._operator.setOperator(newOperator)

    def getOperator(self) -> Operator:
        """
        Gets the current operator.

        Returns:
            :return: self._operator
            :rtype: Operator
        """
        return self._operator

    def setWalk(self, newWalk: QuantumWalk) -> None:
        """
        Sets all the parameters of the current quantum walk to user defined ones.

        Args:
            :param newWalk: New quantum walk.
            :type newWalk: QuantumWalk
        """
        self._initState.setState(newWalk.getInitState())
        self._operator.setOperator(newWalk.getOperator())
        self._finalState.setState(newWalk.getWalk())

    def getWalk(self) -> State:
        """
        Gets the final state associated with the walk.

        Returns:
            :return: self._finalState
            :rtype: State
        """
        return self._finalState

    def searchNodeAmplitude(self, searchNode):
        """
        Searches and gets the amplitude associated with a given node.

        Args:
            :param searchNode: User inputted node for the search.
            :type searchNode: int

        Returns:
            :return: self._finalState.getStateVec().item(searchNode)
            :rtype: complex
        """
        return self._finalState.getStateVec().item(searchNode)

    def invPartRatio(self):
        amplitudes = 0
        for amp in self._finalState.getStateVec():
            amplitudes += np.absolute(amp)**4
        return 1/amplitudes
