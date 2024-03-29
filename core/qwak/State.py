from __future__ import annotations
from typing import Union

import numpy as np
from scipy.linalg import inv
import json

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from utils.jsonTools import json_matrix_to_complex, complex_matrix_to_json


class State:
    def __init__(self, n: int, nodeList: list = None,
                 customStateList: list = None) -> None:
        """Object is initialized with a mandatory user inputted dimension, an optional
        stateList parameter which will be used to create the amplitudes for each node in the state
        and an internal stateVec which will be a Numpy ndarray representing the column vector.

        Parameters
        ----------
        n : int
            Desired dimension of the state.
        nodeList : list, optional
            List containing what nodes will have uniform superposition in the state, by default None.
        customStateList : list, optional
            Custom amplitudes for the state, by default None.
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

    def buildState(
            self,
            nodeList: list = None,
            customStateList: list = None) -> None:
        """Builds state vector from state list, by creating a balanced superposition of all
        nodes in the nodeList.
        This will be changed in the future to make nodeList make more sense.

        Parameters
        ----------
        nodeList : list, optional
            List containing what nodes will have uniform superposition in the state, by default None.
        customStateList : list, optional
            Custom amplitudes for the state, by default None.
        """
        if nodeList is not None:
            self.resetState()
            self._nodeList = nodeList
        if customStateList is not None:
            self.resetState()
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

    def _checkStateOutOfBounds(self, node: int) -> None:
        """Checks if the state is out of bounds for the system.

        Parameters
        ----------
        node : int
            Node to check.

        Raises
        ------
        StateOutOfBounds
            Out of bounds exception.
        """
        if node >= self._n:
            raise StateOutOfBounds(
                f"State {node} is out of bounds for system of size {self._n} ([0-{self._n - 1}])."
            )

    def _checkUnitaryStateList(self, customStateList) -> None:
        """Checks if the sum of the square of the amplitudes is 1.

        Parameters
        ----------
        customStateList : list
            Custom state list.

        Raises
        ------
        NonUnitaryState
            Non unitary state exception.
        """
        unitaryState = 0
        for state in customStateList:
            unitaryState += np.abs(state[1]) ** 2
        unitaryState = round(unitaryState, 5)
        if unitaryState != float(1):
            raise NonUnitaryState(
                f"The sum of the square of the amplitudes is -- {unitaryState} -- instead of 1."
            )

    def herm(self) -> np.ndarray:
        """Returns the Hermitian conjugate of the state vector.

        Returns
        -------
        np.ndarray
            Hermitian conjugate of the state vector.
        """
        return self._stateVec.H

    def inv(self) -> np.ndarray:
        """Returns the inverse of the state vector.

        Returns
        -------
        np.ndarray
            Inverse of the state vector.
        """
        return inv(self._stateVec)

    def resetState(self) -> None:
        """Resets the components of the State."""
        self._stateVec = np.zeros((self._n, 1), dtype=complex)

    def setDim(self, newDim: int, newNodeList: list = None) -> None:
        """Sets the current state dimension to a user defined one.

        Parameters
        ----------
        newDim : int
            New state dimension.
        newNodeList : list, optional
            List containing the new nodes, by default None.
        """
        self._n = newDim
        self._stateVec = np.zeros((self._n, 1), dtype=complex)
        if newNodeList is not None:
            self._nodeList = newNodeList

    def getDim(self) -> int:
        """Gets the current state dimension.

        Returns
        -------
        int
            State dimension.
        """
        return self._n

    def setNodeList(self, newNodeList: list) -> None:
        """Sets current node list to a user inputted one.

        Parameters
        ----------
        newNodeList : list
            List containing the new nodes.
        """
        self._nodeList = newNodeList

    def getNodeList(self) -> list:
        """Gets the current list of nodes.

        Returns
        -------
        list
            Current list of nodes.
        """
        return self._nodeList

    def setStateVec(self, newVec: np.ndarray) -> None:
        """Sets the column vector associated with the state to a user defined one.

        Parameters
        ----------
        newVec : np.ndarray
            New column vector for the state.
        """
        self._stateVec = newVec

    def getStateVec(self) -> np.ndarray:
        """Gets the column vector associated with the state.

        Returns
        -------
        np.ndarray
            Vector of the State.
        """
        return self._stateVec

    def setState(self, newState: State) -> None:
        """Sets all the parameters of the current state to user defined ones.

        Parameters
        ----------
        newState : State
            New state.
        """
        self._n = newState.getDim()
        self._nodeList = newState.getNodeList()
        self._stateVec = newState.getStateVec()

    def to_json(self) -> str:
        """In contrast, the to_json method is not marked with the @classmethod decorator because
        it is a method that is called on an instance of the Operator class.

        This means that it can access the attributes of the instance on which it is called, and it
        uses these attributes to generate the JSON string representation of the Operator instance.

        Since it requires access to the attributes of a specific Operator instance, it cannot be
        called on the Operator class itself.

        Returns
        -------
        str
            JSON string representation of the Operator instance.
        """
        state_dict = {
            "n": self._n,
            "node_list": self._nodeList,
            "custom_state_list": self._customStateList,
            "state_vec": complex_matrix_to_json(
                self._stateVec.tolist()),
        }
        return json.dumps(state_dict)

    @classmethod
    def from_json(cls, json_var: Union[str, dict]):
        """The from_json method is marked with the @classmethod decorator because it is a method that is called on the class itself,
        rather than on an instance of the class.

        This is necessary because it is used to create a new instance of the Operator class from a JSON string,
        and it does not require an instance of the Operator class to do so.

        Parameters
        ----------
        json_var : Union([str, dict])
            JSON string or dictionary representation of the Operator instance.

        Returns
        -------
        Operator
            Operator instance from JSON string or dictionary representation.
        """
        if isinstance(json_var, str):
            state_dict = json.loads(json_var)
        elif isinstance(json_var, dict):
            state_dict = json_var
        n = state_dict["n"]
        node_list = state_dict["node_list"]
        custom_state_list = state_dict["custom_state_list"]
        state_vec = np.array(
            json_matrix_to_complex(
                state_dict["state_vec"]),
            dtype=complex)
        state = cls(n, node_list, custom_state_list)
        state.setStateVec(state_vec)
        return state

    def __mul__(self, other: np.ndarray) -> np.ndarray:
        """Left-side multiplication for the State class.

        Parameters
        ----------
        other : np.ndarray
            Another Numpy ndarray to multiply the state by.

        Returns
        -------
        np.ndarray
            Array of the multiplication
        """
        return self._stateVec * other

    def __rmul__(self, other: np.ndarray) -> np.ndarray:
        """Left-side multiplication for the State class.

        Parameters
        ----------
        other : np.ndarray
            Another Numpy ndarray to multiply the state by.

        Returns
        -------
        np.ndarray
            Array of the multiplication.
        """
        return other * self._stateVec

    def __matmul__(self, other: np.ndarray) -> np.ndarray:
        """Matrix multiplication for the State class.

        Parameters
        ----------
        other : np.ndarray
            Another Numpy ndarray to multiply the state by.

        Returns
        -------
        np.ndarray
            Array of the multiplication.
        """
        return self._stateVec @ other

    def __str__(self) -> str:
        """String representation of the State class.

        Returns
        -------
        str
            State string.
        """
        return f"{self._stateVec}"

    def __repr__(self) -> str:
        """String representation of the State class.

        Returns
        -------
        str
            State string.
        """
        return f"N: {self._n}\n" \
               f"Node list: {self._nodeList}\n" \
               f"Custom Node list: {self._customStateList}\n" \
               f"State:\n\t{self._stateVec}"
