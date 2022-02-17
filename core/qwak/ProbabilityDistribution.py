import warnings

import numpy as np

from qwak.State import State

warnings.filterwarnings("ignore")


class ProbabilityDistribution:
    """
    Class containing the vector containing the probabilities associated with the
    final state of a continuous-time quantum walk.

    """

    def __init__(self, state: State) -> None:
        """
        The dimension of the probability vector will then be loaded from
        the state inputted by the user.
        The vector containing the probabilities will be initialized full of zeros
        with the dimension obtained from the state.

        Args:
            :param state: State to be converted into a probability.
            :type state: State
        """
        self._n = state.getDim()
        self._stateVec = state.getStateVec()
        self._probVec = np.zeros((self._n, 1))

    def __str__(self) -> str:
        """
        String representation of the Probability Distribution class.

        Returns:
            :return: f'{self._probVec}'
            :rtype: str
        """
        return f'{self._probVec}'

    def resetProbDist(self):
        self._stateVec.resetState()
        self._probVec = np.zeros((self._n, 1))

    def buildProbDist(self) -> None:
        """
        Builds the probability vector by multiplying the user inputted
        amplitude state by its conjugate.
        TODO: Nao devia ser pelo complexo conjugado?
        """
        for st in range(self._n):
            self._probVec[st] = self._stateVec[st] * np.conj(self._stateVec[st])

    def setProbVec(self, newProbVec: np.ndarray) -> None:
        """
        Sets the current probability vector to a user inputted one.

        Args:
            :param newProbVec: New probability vector for the distribution.
            :type newProbVec: Numpy.ndarray
        """
        self._probVec = newProbVec.getProbDist()

    def getProbVec(self) -> np.ndarray:
        """
        Gets the probability vector associated with a distribution.

        Returns:
            :return: self._probVec
            :rtype: Numpy.ndarray
        """
        return self._probVec

    def searchNodeProbability(self, searchNode: int) -> float:
        """
        Searches and gets the probability associated with a given node.

        Args:
            :param node: User inputted node for the search.
            :type state: int

        Returns:
            :return: self._probVec.item(searchNode)
            :rtype: float
        """
        return self._probVec.item(searchNode)

    def mean(self) -> float:
        """
        Gets the mean of the current probability distribution.

        Returns:
            :return: float(m)
            :rtype: float
        """
        pos = np.arange(0,self._n)
        m = 0
        for x in range(self._n):
            m += pos[x]*self._probVec[x]
        return float(m)

    def moment(self,k) -> float:
        pos = np.arange(0,self._n)
        m = 0
        for x in range(self._n):
            m += (pos[x]**k)*self._probVec[x]
        return float(m)

    def stdev(self) -> float:
        """
        Gets the standard deviation of the current probability distribution.

        Returns:
            :return: float(std)
            :rtype: float
        """
        pos = np.arange(0,self._n)
        std = 0
        for x in range(self._n):
            std += self._probVec[x]*(pos[x] - self.mean())**2
        return float(np.sqrt(std))

    def altStdev(self):
        return np.sqrt(self.moment(2) - self.moment(1)**2)

    def survivalProb(self,k0,k1):
        survProb = 0
        for i in range(k0,k1):
            survProb +=  self._probVec[i]
        return survProb

