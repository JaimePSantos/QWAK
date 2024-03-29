from __future__ import annotations

import warnings
import numpy as np
import json
from utils.jsonTools import json_matrix_to_complex, complex_matrix_to_json

from qwak.Operator import Operator
from qwak.State import State


warnings.filterwarnings("ignore")


class QuantumWalk:
    def __init__(self, state: State, operator: Operator) -> None:
        """This object is initialized with a user inputted initial state and
        operator.
        The dimension of the quantum walk will then be loaded from the initial
        state.
        The final state will contain the amplitudes of the time evolution of
        the initial state, as a function of the operator. This variable is initialized
        as an instance of State class.

        Parameters
        ----------
        state : State
            Initial state which will be the basis of the time dependant evolution.
        operator : Operator
            Operator which will evolve the initial state.
        """
        self._n = state.getDim()
        self._initState = state
        self._operator = operator
        self._finalState = State(self._n)

    def buildWalk(self, initState: State = None,
                  operator: Operator = None) -> None:
        """Builds the final state of the quantum walk by setting it to the matrix
        multiplication of the operator by the initial state.

        Parameters
        ----------
        initState : State, optional
            Initial state which will be the basis of the time dependant evolution, by default None.
        operator : Operator, optional
            Operator which will evolve the initial state, by default None.
        """
        if initState is not None:
            self._initState = initState
        if operator is not None:
            self._operator = operator
        self._finalState.setStateVec(
            np.matmul(
                self._operator.getOperator(),
                self._initState.getStateVec()))

    def resetWalk(self) -> None:
        """Resets the components of the QuantumWalk object."""
        self._operator.resetOperator()
        self._initState.resetState()
        self._finalState.resetState()

    def setInitState(self, newInitState: State) -> None:
        """Sets the initial state of the quantum walk to a new user inputted one.

        Parameters
        ----------
        newInitState : State
            New initial state for the quantum walk.
        """
        self._initState.setState(newInitState)

    def getInitState(self) -> State:
        """Gets the initial state of the quantum walk.

        Returns
        -------
        State
            Initial state of the quantum walk.
        """
        return self._initState

    def setDim(self, newDim: int) -> None:
        """Sets the current quantum walk dimension to a user defined one.

        Parameters
        ----------
        newDim : int
            New QuantumWalk dimension.
        """
        self._n = newDim
        self._finalState.setDim(self._n)

    def getDim(self) -> int:
        """Gets the current state dimension.

        Returns
        -------
        int
            QuantumWalk dimension.
        """
        return self._n

    def setOperator(self, newOperator: Operator) -> None:
        """Sets the current operator to a user defined one.

        Parameters
        ----------
        newOperator : Operator
            New quantum walk operator.
        """
        self._operator.setOperator(newOperator)

    def getOperator(self) -> Operator:
        """Gets the current operator.

        Returns
        -------
        Operator
            Current QuantumWalk Operator object.
        """
        return self._operator

    def setWalk(self, newWalk: QuantumWalk) -> None:
        """Sets all the parameters of the current quantum walk to user defined ones.

        Parameters
        ----------
        newWalk : QuantumWalk
            New quantum walk.
        """
        self._initState.setState(newWalk.getInitState())
        self._operator.setOperator(newWalk.getOperator())
        self._finalState.setState(newWalk.getFinalState())

    def getFinalState(self) -> State:
        """Gets the final state of the QuantumWalk.

        Returns
        -------
        State
            Final state of the QuantumWalk.
        """
        return self._finalState

    def setFinalState(self, newFinalState: State) -> None:
        """Sets the final state of the QuantumWalk.

        Parameters
        -------
        finalState: State
            Final state of the QuantumWalk.
        """
        self._finalState.setState(newFinalState)

    def getAmpVec(self) -> np.ndarray:
        """Gets the vector of the final state amplitudes of the  QuantumWalk.

        Returns
        -------
        np.ndarray
            Vector of the final state.
        """
        return self._finalState.getStateVec()

    def searchNodeAmplitude(self, searchNode: int) -> complex:
        """Searches and gets the amplitude associated with a given node.

        Parameters
        ----------
        searchNode : int
            User inputted node for the search.

        Returns
        -------
        complex
            Amplitude of the search node.
        """
        return self._finalState.getStateVec().item(searchNode)

    def transportEfficiency(self) -> float:
        """Calculates the transport efficiency of the quantum walk.

        Returns
        -------
        float
            Transport efficiency of the quantum walk.
        """
        return 1 - np.trace(self._finalState @ self._finalState.herm())

    def to_json(self) -> str:
        """Serializes the QuantumWalk object to JSON format.

        Returns
        -------
        str
            JSON string representation of the QuantumWalk object.
        """
        return json.dumps({
            "n": self._n,
            "initState": json.loads(self._initState.to_json()),
            "operator": json.loads(self._operator.to_json()),
            "finalState": json.loads(self._finalState.to_json())
        })

    @classmethod
    def from_json(cls, json_var: str) -> QuantumWalk:
        """Deserializes a JSON string to a QuantumWalk object.

        Parameters
        ----------
        json_str : str
            JSON string representation of the QuantumWalk object.

        Returns
        -------
        QuantumWalk
            Deserialized QuantumWalk object.
        """
        if isinstance(json_var, str):
            data = json.loads(json_var)
        elif isinstance(json_var, dict):
            data = json_var
        initState = State.from_json(data["initState"])
        operator = Operator.from_json(data["operator"])
        finalState = State.from_json(data["finalState"])
        walk = cls(initState, operator)
        walk.setFinalState(finalState)
        return walk

    def __str__(self) -> str:
        """String representation of the StaticQuantumwalk class.

        Returns
        -------
        str
            QuantumWalk string.
        """
        return f"{self._finalState.getStateVec()}"

    def __repr__(self) -> str:
        """Representation of the ProbabilityDistribution object.

        Returns
        -------
        str
            String of the ProbabilityDistribution object.
        """
        return f"N: {self._n}\n" \
               f"Init State:\n\t {self._initState}\n" \
               f"Operator:\n\t{self._operator}\n"\
               f"Final State:\n\t{self._finalState}"
