import numpy as np
from qutip import Qobj


class StochasticProbabilityDistribution(object):

    def __init__(self, state: Qobj) -> None:
        """ A class to represent the probability distribution of a quantum state in a stochastic system.

        Initializes the probability distribution with a given quantum state.

        Parameters
        ----------
        state : Qobj
            Initial state which will be the basis of the time dependant evolution.
        """
        self._finalState = state.getFinalState()
        self._n = state.getDim()
        self._probVec = np.zeros((self._n, 1))

    def buildProbDist(self, state: Qobj = None) -> None:
        """ Builds or updates the probability distribution of the system based on the given quantum state.

        Parameters
        ----------
        state : Qobj, optional
            The quantum state to be used for updating the probability distribution.
            If None, the existing final state is used. Default is None.
        """
        if state is not None:
            self._finalState = state.getFinalState()
        self._probVec = np.diagonal(self._finalState)

    def getProbVec(self) -> np.ndarray:
        """Returns the probability vector representing the distribution of the current state.

         Returns
         -------
         np.ndarray
             The probability vector of the current state, flattened.
         """
        return self._probVec.flatten()

    def setProbVec(self, newFinalState: np.ndarray) -> None:
        """Sets a new final state for the probability distribution.

         Parameters
         ----------
         newFinalState : np.ndarray
             The new final state to be set for the probability distribution.
         """
        self._finalState = newFinalState
