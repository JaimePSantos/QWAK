import numpy as np
import timeit
import warnings
warnings.filterwarnings("ignore")

class ProbabilityDistributionTest:
    def __init__(self,state):
        self._n = state.getDim()
        self._stateVec = state.getStateVec()
        self._probVec = np.zeros((self._n, 1))
        self.probDistExecutionTime = 0

    def __str__(self):
        return '%s' % self._probVec

    def buildProbDist(self):
        for st in range(self._n):
            self._probVec[st] = self._stateVec[st] * np.conjugate(self._stateVec[st])

    def timedBuildProbDist(self):
        startTimeProbDist = timeit.default_timer()
        self.buildProbDist()
        endTimeProbDist = timeit.default_timer()
        self.probDistExecutionTime = (endTimeProbDist - startTimeProbDist)

    def setProbDist(self,newProbDist):
        self._probVec = newProbDist.getProbDist()

    def getProbDist(self):
        return self._probVec

    def getStateProbability(self,state):
        return self._probVec.item(state)

