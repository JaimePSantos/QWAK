import numpy as np
import warnings
warnings.filterwarnings("ignore")

class ProbabilityDistribution:
    def __init__(self,state):
        self._n = state.getDim()
        self._stateVec = state.getStateVec()
        self._probVec = np.zeros((self._n, 1))

    def buildProbDist(self):
        for st in range(self._n):
            self._probVec[st] = self._stateVec[st] * np.conjugate(self._stateVec[st])

    def setProbDist(self,newProbDist):
        self._probVec = newProbDist.getProbDist()

    def getProbDist(self):
        return self._probVec