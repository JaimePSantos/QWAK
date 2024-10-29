from __future__ import annotations

import warnings
import cupy as cp
import json
from utils.jsonTools import json_matrix_to_complex, complex_matrix_to_json

from qwak_cupy.Operator import Operator
from qwak_cupy.State import State


warnings.filterwarnings("ignore")


class QuantumWalk:
    def __init__(self, state: State, operator: Operator) -> None:
        self._n = state.getDim()
        self._initState = state
        self._operator = operator
        self._finalState = State(self._n)

    def buildWalk(self, initState: State = None,
                  operator: Operator = None) -> None:
        if initState is not None:
            self._initState = initState
        if operator is not None:
            self._operator = operator
        self._finalState.setStateVec(
            cp.matmul(
                self._operator.getOperator(),
                self._initState.getStateVec()))

    def resetWalk(self) -> None:
        self._operator.resetOperator()
        self._initState.resetState()
        self._finalState.resetState()

    def setInitState(self, newInitState: State) -> None:
        self._initState.setState(newInitState)

    def getInitState(self) -> State:
        return self._initState

    def setDim(self, newDim: int) -> None:
        self._n = newDim
        self._finalState.setDim(self._n)

    def getDim(self) -> int:
        return self._n

    def setOperator(self, newOperator: Operator) -> None:
        self._operator.setOperator(newOperator)

    def getOperator(self) -> Operator:
        return self._operator

    def setWalk(self, newWalk: QuantumWalk) -> None:
        self._initState.setState(newWalk.getInitState())
        self._operator.setOperator(newWalk.getOperator())
        self._finalState.setState(newWalk.getFinalState())

    def xz(self) -> State:
        return self._finalState

    def setFinalState(self, newFinalState: State) -> None:
        self._finalState.setState(newFinalState)

    def getAmpVec(self) -> cp.ndarray:
        return self._finalState.getStateVec()

    def searchNodeAmplitude(self, searchNode: int) -> complex:
        return self._finalState.getStateVec().item(searchNode)

    def transportEfficiency(self) -> float:
        return 1 - cp.trace(self._finalState @ self._finalState.herm())

    def __str__(self) -> str:
        return f"{self._finalState.getStateVec()}"

    def __repr__(self) -> str:
        return f"N: {self._n}\n" \
               f"Init State:\n\t {self._initState}\n" \
               f"Operator:\n\t{self._operator}\n"\
               f"Final State:\n\t{self._finalState}"
