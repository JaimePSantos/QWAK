import timeit
import warnings

import numpy as np

warnings.filterwarnings("ignore")


class ProbabilityDistributionTest:
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
        self.probDistExecutionTime = 0

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

    def timedBuildProbDist(self):
        """[summary]
        """
        startTimeProbDist = timeit.default_timer()
        self.buildProbDist()
        endTimeProbDist = timeit.default_timer()
        self.probDistExecutionTime = (endTimeProbDist - startTimeProbDist)

    def setProbDist(self, newProbDist):
        """[summary]

        Args:
            newProbDist ([type]): [description]
        """
        self._probVec = newProbDist.getProbDist()

    def getProbDist(self):
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