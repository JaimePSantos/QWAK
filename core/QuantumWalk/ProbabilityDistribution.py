import warnings

import numpy as np

warnings.filterwarnings("ignore")


class ProbabilityDistribution:
    """[summary]
    """

    def __init__(self, state):
        """[summary]

        Args:
            state ([type]): [description]
        """
        self._n = state.getDim()
        self._stateVec = state.getStateVec()
        self._probVec = np.zeros((self._n, 1))

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return '%s' % self._probVec

    def buildProbDist(self):
        """[summary]
        """
        for st in range(self._n):
            self._probVec[st] = self._stateVec[st] * \
                                np.conjugate(self._stateVec[st])

    def setProbVec(self, newProbDist):
        """[summary]

        Args:
            newProbDist ([type]): [description]
        """
        self._probVec = newProbDist.getProbDist()

    def getProbVec(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._probVec

    def getStateProbability(self, state):
        """[summary]

        Args:
            state ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._probVec.item(state)

    def mean(self):
        pos = np.arange(0,self._n)
        m = 0
        for x in range(self._n):
            m += pos[x]*self._probVec[x]
        return m

    def std(self):
        pos = np.arange(0,self._n)
        std = 0
        mean = self.mean()
        for x in range(self._n):
            std += self._probVec[x]*(pos[x] - mean)**2
        return std