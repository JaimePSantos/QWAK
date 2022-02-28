from __future__ import annotations

import numpy as np


class State:
    """
    Class that represents the states that will be used in a quantum walk.
    States are represented by column vectors in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these column vectors.
    """

    def __init__(self, n: int, nodeList: list = [0]) -> None:
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
        self._nodeList = nodeList
        self._stateVec = np.zeros((self._n, 1))

    def resetState(self):
        self._stateVec = np.zeros((self._n, 1))

    def buildState(self, nodeList: list) -> None:
        """
        Builds state vector from state list, by creating a balanced superposition of all
        nodes in the nodeList.
        This will be changed in the future to make nodeList make more sense.

        Args:
            :param nodeList: List of nodes that will have an amplitude in the state vector.
            :type nodeList: list
        """
        self._nodeList = nodeList
        nodeAmp = np.sqrt(len(self._nodeList))
        for state in self._nodeList:
            self._stateVec[state] = 1 / nodeAmp

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
