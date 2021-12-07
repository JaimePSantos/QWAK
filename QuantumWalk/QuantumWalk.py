import numpy as np
from QuantumWalk.State import State
import warnings
warnings.filterwarnings("ignore")

class QuantumWalk:
    def __init__(self,state,operator):
        self._n = state.getDim()
        self._initState = state.getStateVec()
        self._operator = operator.getOperator()
        self._finalState = State(self._n)

    def buildWalk(self):
        self._finalState.setStateVec(np.dot(self._operator, self._initState))

    def setInitState(self,newInitState):
        self._initState = newInitState

    def getInitState(self):
        return self._initState

    def setDim(self,newDim):
        self._n = newDim

    def getDim(self):
        return self._n

    def setOperator(self,newOperator):
        self._operator = newOperator

    def getOperator(self):
        return self._operator

    def setWalk(self,newWalk):
        self._initState = newWalk.getInitState()
        self._operator = newWalk.getOperator()
        self._finalState = newWalk.getWalk()

    def getWalk(self):
        return self._finalState

    def toProbability(self):
        probs = np.zeros((self._n, 1))
        for st in range(self._n):
            probs[st] = self._finalState.getStateVec()[st] * np.conjugate(self._finalState.getStateVec()[st])
        return probs