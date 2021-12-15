import timeit

import numpy as np


class State:
    def __init__(self, n, stateList=None):
        self._n = n
        self._stateList = stateList
        self._stateVec = np.zeros((self._n, 1))

    def __mul__(self, other):
        return self._stateVec * other

    def __rmul__(self, other):
        return other * self._stateVec

    def __str__(self):
        return '%s' % self._stateVec

    def buildState(self):
        if self._stateList is not None:
            for state in self._stateList:
                self._stateVec[state] = 1 / np.sqrt(len(self._stateList))

    def setDim(self,newN):
        self._n = newN

    def getDim(self):
        return self._n

    #TODO: This might not be needed.
    def setStateList(self,newState):
        self._stateList = newState

    def getStateList(self):
        return self._stateList

    def setStateVec(self,newVec):
        self._stateVec = newVec

    def getStateVec(self):
        return self._stateVec

    def setState(self, newState):
        self._n = newState.getDim()
        self._stateList = newState.getStateList()
        self._stateVec = newState.getState()
