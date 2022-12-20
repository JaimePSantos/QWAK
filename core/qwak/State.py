from __future__ import annotations

import numpy as np
from scipy.linalg import inv
import json

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from utils.jsonMethods import json_matrix_to_complex,complex_matrix_to_json


class State:
    """
    Class that represents the states that will be used in a quantum walk.
    States are represented by column vectors in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these column vectors.
    """

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

    def to_json(self):
        """In contrast, the to_json method is not marked with the @classmethod decorator because it is a method that is called on an instance of the Operator class. This means that it can access the attributes of the instance on which it is called, and it uses these attributes to generate the JSON string representation of the Operator instance. Since it requires access to the attributes of a specific Operator instance, it cannot be called on the Operator class itself.

        Returns
        -------
        _type_
            _description_
        """
        state_dict = {
            "n": self._n,
            "node_list": self._nodeList,
            "custom_state_list": self._customStateList,
            "state_vec": complex_matrix_to_json(self._stateVec.tolist()),
        }
        return json.dumps(state_dict)

    @classmethod
    def from_json(cls, json_var):
        """The from_json method is marked with the @classmethod decorator because it is a method that is called on the class itself, rather than on an instance of the class. This is necessary because it is used to create a new instance of the Operator class from a JSON string, and it does not require an instance of the Operator class to do so.

        Parameters
        ----------
        json_str : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if isinstance(json_var,str):
            state_dict = json.loads(json_var)
        elif isinstance(json_var,dict):
            state_dict = json_var
        n = state_dict["n"]
        node_list = state_dict["node_list"]
        custom_state_list = state_dict["custom_state_list"]
        state_vec = np.array(json_matrix_to_complex(state_dict["state_vec"]), dtype=complex)
        state = cls(n, node_list, custom_state_list)
        state.setStateVec(state_vec)
        return state

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
        # TODO: We can probably find a better way to build this
        # function.\
        # self.resetState()
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

    def _checkStateOutOfBounds(self, node) -> None:
        """_summary_

        Parameters
        ----------
        node : _type_
            _description_

        Raises
        ------
        StateOutOfBounds
            _description_
        """
        if node >= self._n:
            raise StateOutOfBounds(
                f"State {node} is out of bounds for system of size {self._n} ([0-{self._n - 1}])."
            )

    def _checkUnitaryStateList(self, customStateList) -> None:
        """_summary_

        Parameters
        ----------
        customStateList : _type_
            _description_

        Raises
        ------
        NonUnitaryState
            _description_
        """
        unitaryState = 0
        for state in customStateList:
            unitaryState += np.abs(state[1]) ** 2
        unitaryState = round(unitaryState, 5)
        if unitaryState != float(1):
            raise NonUnitaryState(
                f"The sum of the square of the amplitudes is -- {unitaryState} -- instead of 1."
            )

    def herm(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._stateVec.H

    def inv(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return inv(self._stateVec)

    def resetState(self):
        """Resets the components of the State."""
        self._stateVec = np.zeros((self._n, 1), dtype=complex)

    def setDim(self, newDim: int, newNodeList: list = None) -> None:
        """Sets the current state dimension to a user defined one.

        Parameters
        ----------
        newDim : int
            New state dimension.
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
        # TODO: Do we need this?
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

    def __matmul__(self, other):
        """_summary_

        Parameters
        ----------
        other : _type_
            _description_

        Returns
        -------
        _type_
            _description_
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
        """Representation of the ProbabilityDistribution object.

        Returns
        -------
        str
            String of the ProbabilityDistribution object.
        """
        return f"N: {self._n}\n" \
               f"Node list: {self._nodeList}\n" \
               f"Custom Node list: {self._customStateList}\n" \
               f"State:\n\t{self._stateVec}"
