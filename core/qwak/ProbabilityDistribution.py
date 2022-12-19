import warnings

import numpy as np
from qwak.State import State
from qwak.Errors import MissingNodeInput
import json
# import json_tricks as json
from utils.jsonMethods import json_matrix_to_complex,complex_matrix_to_json

warnings.filterwarnings("ignore")


class ProbabilityDistribution:
    """
    Class containing the vector containing the probabilities associated with the
    final state of a continuous-time quantum walk.

    """

    def __init__(self, state: State) -> None:
        """The dimension of the probability vector will then be loaded from
        the state inputted by the user.
        The vector containing the probabilities will be initialized full of zeros
        with the dimension obtained from the state.

        Parameters
        ----------
        state : State
            State to be converted into a probability.
        """
        self._state = state
        self._stateVec = self._state.getStateVec()
        self._n = state.getDim()
        self._probVec = np.zeros((self._n, 1), dtype=float)

    def to_json(self):
        return json.dumps({
            'state': json.loads(self._state.to_json()),
            'dim': self._n,
            'prob_vec': self._probVec.tolist()
        })

    @classmethod
    def from_json(cls, json_var):
        if isinstance(json_var,str):
            json_dict = json.loads(json_var)
        elif isinstance(json_var,dict):
            json_dict = json_var
        state = State.from_json(json_dict['state'])
        # print(json_dict['state']['n'])
        dim = json_dict['dim']
        prob_vec = np.array(json_dict['prob_vec'])
        probDist = cls(state)
        probDist.setDim(dim)
        # print(state.getDim())
        probDist.setProbVec(prob_vec)
        return probDist

    def resetProbDist(self) -> None:
        """Resets the ProbabilityDistribution object."""
        # TODO: Rethink state attribute
        self._stateVec = np.zeros((self._n, 1), dtype=complex)
        self._probVec = np.zeros((self._n, 1), dtype=float)

    def buildProbDist(self, state: State = None) -> None:
        """Builds the probability vector by multiplying the user inputted
        amplitude state by its conjugate.

        Parameters
        ----------
        state : State, optional
            _description_, by default None
        """
        if state is not None:
            self._stateVec = state.getStateVec()
        for st in range(self._n):
            self._probVec[st] = (self._stateVec[st] *
                                 np.conj(self._stateVec[st])).real

    def setProbDist(self, newProbDist) -> None:
        """_summary_

        Parameters
        ----------
        newProbDist : _type_
            _description_
        """
        self._state = newProbDist.getState()
        self._stateVec = newProbDist.getStateVec()
        self._n = newProbDist.getDim()
        self._probVec = newProbDist.getProbVec()

    def getStateVec(self) -> State:
        """_summary_

        Returns
        -------
        State
            _description_
        """
        return self._stateVec

    def getState(self):
        return self._state

    def setDim(self, newDim):
        self._n = newDim
        self._probVec = np.zeros((self._n, 1), dtype=float)

    def getDim(self) -> int:
        """_summary_

        Returns
        -------
        int
            _description_
        """
        return self._n

    def setProbVec(self, newProbVec: np.ndarray) -> None:
        """Sets the current probability vector to a user inputted one.

        Parameters
        ----------
        newProbVec : np.ndarray
            New probability vector for the distribution.
        """
        self._probVec = newProbVec

    def getProbVec(self) -> np.ndarray:
        """Gets the probability vector associated with a distribution.

        Returns
        -------
        np.ndarray
            Returns the array of the ProbabilityDistribution object.
        """
        return self._probVec.flatten()

    def searchNodeProbability(self, searchNode: int) -> float:
        """Searches and gets the probability associated with a given node.

        Parameters
        ----------
        searchNode : int
            User inputted node for the search.

        Returns
        -------
        float
            Probability of the searched node.
        """
        return self._probVec.item(searchNode)

    def mean(self) -> float:
        """Gets the mean of the current probability distribution.

        Returns
        -------
        float
            Mean of the ProbabilityDistribution object.
        """
        # TODO: This function has been replaced by moment(1).
        pos = np.arange(0, self._n)
        m = 0
        for x in range(self._n):
            m += pos[x] * self._probVec[x]
        return float(m)

    def moment(self, k) -> float:
        """_summary_

        Parameters
        ----------
        k : _type_
            _description_

        Returns
        -------
        float
            _description_
        """
        pos = np.arange(0, self._n)
        m = 0
        for x in range(self._n):
            m += (pos[x] ** k) * self._probVec[x]
        return float(m)

    def stDev(self) -> float:
        """_summary_

        Returns
        -------
        float
            _description_
        """
        stDev = self.moment(2) - self.moment(1) ** 2
        if stDev <= 0:
            return 0
        return np.sqrt(stDev)

    def survivalProb(self, k0, k1) -> float:
        """_summary_

        Parameters
        ----------
        k0 : _type_
            _description_
        k1 : _type_
            _description_

        Returns
        -------
        float
            _description_
        """
        survProb = 0
        try:
            k0 = int(k0)
            k1 = int(k1)
            if k0 == k1:
                return self._probVec[int(k0)][0]
            else:
                for i in range(int(k0), int(k1) + 1):
                    survProb += self._probVec[i]
            return survProb[0]
        except ValueError:
            raise MissingNodeInput(
                f"A node number is missing: k0 = {k0}; k1={k1}")

    def __str__(self) -> str:
        """String representation of the ProbabilityDistribution object.

        Returns
        -------
        str
            String of the ProbabilityDistribution object.
        """
        return f"{self._probVec}"

    def __repr__(self) -> str:
        """Representation of the ProbabilityDistribution object.

        Returns
        -------
        str
            String of the ProbabilityDistribution object.
        """
        return f"N: {self._n}\n" \
               f"State:\n\t{self._stateVec}\n" \
               f"ProbDist:\n\t{self._probVec}"
