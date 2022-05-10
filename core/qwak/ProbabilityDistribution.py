import warnings

import numpy as np

from qwak.State import State
from qutip import Qobj, basis, mesolve, Options


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
        self._state = state.getStateVec()
        self._n = state.getDim()
        self._probVec = np.zeros((self._n, 1))

    def resetProbDist(self):
        self._state.resetState()
        self._probVec = np.zeros((self._n, 1))

    def buildProbDist(self,state=None) -> None:
        """
        Builds the probability vector by multiplying the user inputted
        amplitude state by its conjugate.
        TODO: Nao devia ser pelo complexo conjugado?
        """
        if state is not None:
            self._state = state.getStateVec()
        for st in range(self._n):
            self._probVec[st] = self._state[st] * np.conj(self._state[st])

    def setProbDist(self,newProbDist):
        self._state = newProbDist.getState()
        self._n = newProbDist.getDim()
        self._probVec = newProbDist.getProbVec()

    def getState(self):
        return self._state

    def getDim(self):
        return self._n

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
        return self._probVec.flatten()

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
        pos = np.arange(0, self._n)
        m = 0
        for x in range(self._n):
            m += pos[x] * self._probVec[x]
        return float(m)

    def moment(self, k) -> float:
        pos = np.arange(0, self._n)
        m = 0
        for x in range(self._n):
            m += (pos[x] ** k) * self._probVec[x]
        return float(m)

    def stDev(self):
        stDev = self.moment(2) - self.moment(1) ** 2
        if stDev <= 0:
            return 0
        return np.sqrt(stDev)

    def survivalProb(self, k0, k1):
        survProb = 0
        if k0 == k1:
            return self._probVec[int(k0)][0]
        else:
            for i in range(int(k0), int(k1) + 1):
                survProb += self._probVec[i]
        return survProb[0]

    def __str__(self) -> str:
        """
        String representation of the Probability Distribution class.

        Returns:
            :return: f'{self._probVec}'
            :rtype: str
        """
        return f"{self._probVec}"


class StochasticProbabilityDistribution(object):
    """ """

    def __init__(self, state: Qobj) -> None:
        """
        Args:
            :param state: Initial state which will be the basis of the time dependant evolution.
            :type state: State
        """
        self._finalState = state.getFinalState()
        self._n = len(self._finalState.final_state.diag())
        self._probVec = np.zeros((self._n, 1))

    def buildProbDist(self):
        """
        Builds the final state of the quantum walk by setting it to the matrix
        multiplication of the operator by the initial state.
        """
        self._probVec = self._finalState.final_state.diag()

    def getProbVec(self):
        return self._probVec

    def setProbVec(self, newFinalState):
        self._finalState = newFinalState
