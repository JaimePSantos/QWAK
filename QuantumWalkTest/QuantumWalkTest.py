import numpy as np
from QuantumWalk.State import State
import timeit
import warnings
warnings.filterwarnings("ignore")

class QuantumWalkTest:
    def __init__(self,state,operator):
        self._n = state.getDim()
        self._initState = state.getStateVec()
        self._operator = operator.getOperator()
        self._finalState = State(self._n)

    def __str__(self):
        return '%s' % self._finalState.getStateVec()

    def buildWalk(self):
        self._finalState.setStateVec(np.matmul(self._operator, self._initState))

    def timedBuildWalk(self):
        startTimeWalk = timeit.default_timer()
        self.buildWalk()
        endTimeWalk = timeit.default_timer()
        executionTimeWalk = (endTimeWalk - startTimeWalk)
        print("Walk took %s seconds." % executionTimeWalk)

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

    def getStateAmplitude(self,state):
        return self._finalState.getStateVec().item(state)