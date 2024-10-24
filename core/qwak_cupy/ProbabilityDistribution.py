from __future__ import annotations
from typing import Union

import cupy as cp
from qwak_cupy.State import State
from qwak_cupy.Errors import MissingNodeInput
import json
from utils.jsonTools import json_matrix_to_complex, complex_matrix_to_json
from functools import reduce


class ProbabilityDistribution:
    def __init__(self, state: State) -> None:
        self._state = state
        self._stateVec = self._state.getStateVec()
        self._n = state.getDim()
        self._probVec = cp.zeros(self._n, dtype=float)

    def resetProbDist(self) -> None:
        self._stateVec = cp.zeros((self._n, 1), dtype=complex)
        self._probVec = cp.zeros(self._n, dtype=float)

    def buildProbDist(self, state: State = None) -> None:
        if state is not None:
            self._n = state.getDim()
            self._state.setState(state)
            self._stateVec = self._state.getStateVec()

        self._probVec = cp.array(
            [((state[0] * cp.conj(state[0])).real) for state in self._stateVec])

    def setProbDist(self, newProbDist: ProbabilityDistribution) -> None:
        self._n = newProbDist.getDim()
        self._state.setState(newProbDist.getState())
        self._stateVec = newProbDist.getStateVec()
        self._probVec = newProbDist.getProbVec()

    def getStateVec(self) -> State:
        return self._stateVec

    def getState(self) -> State:
        return self._state

    def setState(self, newState: State) -> None:
        self._state.setState(newState)

    def setDim(self, newDim: int) -> None:
        self._n = newDim
        self._probVec = cp.zeros(self._n, dtype=float)

    def getDim(self) -> int:
        return self._n

    def setProbVec(self, newProbVec: cp.ndarray) -> None:
        self._probVec = newProbVec

    def getProbVec(self) -> cp.ndarray:
        return self._probVec

    def searchNodeProbability(self, searchNode: int) -> float:
        return self._probVec.item(searchNode)

    def moment(self, k: int) -> float:
        pos = cp.arange(0, self._n)
        m = 0
        for x in range(self._n):
            m += (pos[x] ** k) * self._probVec[x]
        return float(m)

    def invPartRatio(self) -> float:
        return 1 / (cp.sum(cp.absolute(self._probVec) ** 2))

    def stDev(self) -> float:
        stDev = self.moment(2) - self.moment(1) ** 2
        return cp.sqrt(stDev) if (stDev > 0) else 0

    def survivalProb(self, fromNode, toNode) -> float:
        survProb = 0
        try:
            if fromNode == toNode:
                return self._probVec[int(fromNode)][0]
            else:
                for i in range(int(fromNode), int(toNode) + 1):
                    survProb += self._probVec[i]
            return survProb
        except ValueError:
            raise MissingNodeInput(
                f"A node number is missing: fromNode = {fromNode}; toNode={toNode}")

    def searchNodeProbability(self, searchNode: int) -> float:
        return self._probVec.item(searchNode)

    def __str__(self) -> str:
        return f"{self._probVec}"

    def __repr__(self) -> str:
        return f"N: {self._n}\n" \
               f"State:\n\t{self._stateVec}\n" \
               f"ProbDist:\n\t{self._probVec}"
