from __future__ import annotations

import numpy as np
from scipy.linalg import inv

from qwak.Errors import StateOutOfBounds, NonUnitaryState


class State:
    """
    Class that represents the states that will be used in a quantum walk.
    States are represented by column vectors in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these column vectors.
    """

    def __init__(self, n: int, nodeList: list = None, customStateList=None) -> None:
        """
        Object is initialized with a mandatory user inputted dimension, an optional
        stateList parameter which will be used to create the amplitudes for each node in the state
        and an internal stateVec which will be a Numpy ndarray representing the column vector.

        Args:
            :param n: Desired dimension of the state.
            :type n: int
            :param nodeList: List containing what nodes will have amplitudes in the state.
            :type nodeList: (list,optional)
        """
        self._n = n
        if nodeList is None:
            self._nodeList = []
        else:
            self._nodeList = nodeList
        if customStateList is None:
            self._customStateList = []
        else:
            self._customStateList = customStateList
        self._stateVec = np.zeros((self._n, 1), dtype=complex)

    def buildState(self, nodeList: list = None, customStateList=None) -> None:
        """
        Builds state vector from state list, by creating a balanced superposition of all
        nodes in the nodeList.
        This will be changed in the future to make nodeList make more sense.

        Args:
            :param nodeList: List of nodes that will have an amplitude in the state vector.
            :type nodeList: list
        """
        # TODO: We can probably find a better way to build this function.
        if nodeList is not None:
            self._nodeList = nodeList
        if customStateList is not None:
            self._customStateList = customStateList
        if self._customStateList:
            self._checkUnitaryStateList(self._customStateList)
            for customState in self._customStateList:
                self._checkStateOutOfBounds(customState[0])
                self._stateVec[customState[0]] = customState[1]
        else:
            nodeAmp = np.sqrt(len(self._nodeList))
            for state in self._nodeList:
                self._checkStateOutOfBounds(state)
                self._stateVec[state] = 1 / nodeAmp

    def _checkStateOutOfBounds(self, node):
        if node >= self._n:
            raise StateOutOfBounds(
                f"State {node} is out of bounds for system of size {self._n} ([0-{self._n - 1}])."
            )

    def _checkUnitaryStateList(self, customStateList):
        unitaryState = 0
        for state in customStateList:
            unitaryState += np.abs(state[1]) ** 2
        unitaryState = round(unitaryState, 5)
        if unitaryState != float(1):
            raise NonUnitaryState(
                f"The sum of the square of the amplitudes is -- {unitaryState} -- instead of 1."
            )

    def herm(self):
        return self._stateVec.H

    def inv(self):
        return inv(self._stateVec)

    def resetState(self):
        self._stateVec = np.zeros((self._n, 1))

    def setDim(self, newDim: int) -> None:
        """
        Sets the current state dimension to a user defined one.

        Args:
            :param newDim: New state dimension.
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

    def setNodeList(self, newNodeList: list) -> None:
        """
        Sets current node list to a user inputted one.
        This might not be needed and removed in the future.

        Args:
            :param newNodeList: List containing the new nodes.
            :type newNodeList: list
        """
        self._nodeList = newNodeList

    def getNodeList(self) -> list:
        """
        Gets the current list of nodes.

        Returns:
            :return: self._nodeList
            :rtype: list
        """
        return self._nodeList

    def setStateVec(self, newVec: np.ndarray) -> None:
        """
        Sets the column vector associated with the state to a user defined one.

        Args:
            :param newVec: New column vector for the state
            :type newVec: Numpy.ndarray
        """
        self._stateVec = newVec

    def getStateVec(self) -> np.ndarray:
        """
        Gets the column vector associated with the state.

        Returns:
            :return: self._stateVec
            :rtype: Numpy.ndarray
        """
        return self._stateVec

    def setState(self, newState: State) -> None:
        """[summary]
        Sets all the parameters of the current state to user defined ones.

        Args:
            :param newState: New state.
            :type newState: State
        """
        self._n = newState.getDim()
        self._nodeList = newState.getNodeList()
        self._stateVec = newState.getStateVec()

    def __mul__(self, other: np.ndarray) -> np.ndarray:
        """
        Left-side multiplication for the State class.

        Args:
            :param other: Another Numpy ndarray to multiply the state by.
            :type other: Numpy.ndarray

        Returns:
            :return: self._stateVec * other
            :rtype: Numpy.ndarray
        """
        return self._stateVec * other

    def __rmul__(self, other: np.ndarray) -> np.ndarray:
        """
        Right-side multiplication for the State class.

        Args:
            :param other: Another Numpy ndarray to multiply the state by.
            :type other: Numpy.ndarray

        Returns:
            :return: self._stateVec * other
            :rtype: Numpy.ndarray
        """
        return other * self._stateVec

    def __str__(self) -> str:
        """
        String representation of the State class.

        Returns:
            :return: f"{self._stateVec}"
            :rtype: str
        """
        return f"{self._stateVec}"

    def __matmul__(self, other):
        return self._stateVec @ other
