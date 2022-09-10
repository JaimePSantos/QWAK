import numpy as np
from qutip import Qobj


class StochasticProbabilityDistribution(object):
    """_summary_

    Parameters
    ----------
    object : _type_
        _description_
    """

    # TODO: Figure out why we need the object.
    def __init__(self, state: Qobj) -> None:
        """_summary_

        Parameters
        ----------
        state : Qobj
            Initial state which will be the basis of the time dependant evolution.
        """
        self._finalState = state.getFinalState()
        self._n = state.getDim()
        self._probVec = np.zeros((self._n, 1))

    def buildProbDist(self, state=None) -> None:
        """_summary_

        Parameters
        ----------
        state : _type_, optional
            _description_, by default None
        """
        if state is not None:
            self._finalState = state.getFinalState()
        self._probVec = np.diagonal(self._finalState)

    def getProbVec(self) -> np.ndarray:
        """_summary_

        Returns
        -------
        np.ndarray
            _description_
        """
        return self._probVec.flatten()

    def setProbVec(self, newFinalState) -> None:
        """_summary_

        Parameters
        ----------
        newFinalState : _type_
            _description_
        """
        self._finalState = newFinalState