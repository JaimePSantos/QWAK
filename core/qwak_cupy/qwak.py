from __future__ import annotations
from typing import Union

import networkx as nx
import cupy as cp
import copy
import json
from qwak.Errors import (
    StateOutOfBounds,
    NonUnitaryState,
    UndefinedTimeList,
    EmptyProbDistList,
    MissingNodeInput,
    MissingGraphInput,
)
from qwak_cupy.State import State
from qwak_cupy.Operator import Operator
from qwak_cupy.QuantumWalk import QuantumWalk
from qwak_cupy.ProbabilityDistribution import ProbabilityDistribution


class QWAK:
    def __init__(
            self,
            graph: nx.Graph,
            time: float = 0,
            timeList: list = None,
            gamma: float = 1,
            initStateList: list = None,
            customStateList: list = None,
            laplacian: bool = False,
            markedElements: list = [],
            qwakId: str = 'userUndef',
    ) -> None:
        self._graph = graph
        self._n = len(self._graph)
        if timeList is not None:
            self._timeList = cp.array([x for x in timeList])
        else:
            self._timeList = cp.array([0] * self._n)
        self._qwakId = qwakId
        self._operator = Operator(
            self._graph,
            time=time,
            gamma=gamma,
            laplacian=laplacian,
            markedElements=markedElements)
        self._initState = State(
            self._n,
            nodeList=initStateList,
            customStateList=customStateList)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._probDist = ProbabilityDistribution(
            self._quantumWalk.getFinalState())
        self._probDistList = cp.array([])

    def runWalk(
            self,
            time: float = 0,
            initStateList: list = None,
            customStateList: list = None) -> None:
        try:
            self._initState.buildState(
                nodeList=initStateList, customStateList=customStateList
            )
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildDiagonalOperator(time=time)
        self._quantumWalk.buildWalk(self._initState, self._operator)
        self._probDist.buildProbDist(self._quantumWalk.getFinalState())

    def setProbDist(self, newProbDist: ProbabilityDistribution) -> None:
        self._probDist.setProbDist(newProbDist)

    def getProbDist(self) -> ProbabilityDistribution:
        return self._probDist

    def getProbDistList(self) -> list:
        return self._probDistList

    def setProbDistList(self, newProbDistList: list) -> None:
        self._probDistList = newProbDistList

    def getProbVec(self) -> cp.ndarray:
        return self._probDist.getProbVec()

