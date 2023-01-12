from __future__ import annotations
from typing import Union

import numpy as np
from qwak.State import State
from qwak.Errors import MissingNodeInput
import json
from utils.jsonMethods import json_matrix_to_complex, complex_matrix_to_json
from functools import reduce


class ProbabilityDistribution:
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
        self._probVec = np.zeros(self._n, dtype=float)

    def to_json(self) -> str:
        """
            Converts the ProbabilityDistribution object to a JSON string.

        Returns
        -------
        str
            JSON string of the ProbabilityDistribution object.
        """
        return json.dumps({
            'state': json.loads(self._state.to_json()),
            'dim': self._n,
            'prob_vec': self._probVec.tolist()
        })

    @classmethod
    def from_json(cls,
                  json_var: Union[str,
                                  dict]) -> ProbabilityDistribution:
        """Converts a JSON string to a ProbabilityDistribution object.

        Parameters
        ----------
        json_var : Union[str, dict]
            JSON string or dictionary to be converted to a ProbabilityDistribution object.

        Returns
        -------
        ProbabilityDistribution
            ProbabilityDistribution object converted from JSON.
        """
        if isinstance(json_var, str):
            json_dict = json.loads(json_var)
        elif isinstance(json_var, dict):
            json_dict = json_var
        state = State.from_json(json_dict['state'])
        prob_vec = np.array(json_dict['prob_vec'])
        probDist = cls(state)
        probDist.setProbVec(prob_vec)
        return probDist

    def resetProbDist(self) -> None:
        """Resets the ProbabilityDistribution object."""
        # TODO: Rethink state attribute
        self._stateVec = np.zeros((self._n, 1), dtype=complex)
        self._probVec = np.zeros(self._n, dtype=float)

    def buildProbDist(self, state: State = None) -> None:
        """Builds the probability vector by multiplying the user inputted
        amplitude state by its conjugate.

        Parameters
        ----------
        state : State, optional
            State to be converted into a probability, by default None
        """
        if state is not None:
            self._n = state.getDim()
            self._state.setState(state)
            self._stateVec = self._state.getStateVec()
        self._probVec = np.array(
            [((state.item(0) * np.conj(state.item(0))).real) for state in self._stateVec])

    def setProbDist(self, newProbDist: ProbabilityDistribution) -> None:
        """Sets the current probability distribution to a user inputted one.

        Parameters
        ----------
        newProbDist : ProbabilityDistribution
            New probability distribution for the object.
        """
        self._n = newProbDist.getDim()
        self._state.setState(newProbDist.getState())
        self._stateVec = newProbDist.getStateVec()
        self._probVec = newProbDist.getProbVec()

    def getStateVec(self) -> State:
        """Gets the state vector associated with a distribution.

        Returns
        -------
        State
            Returns the state vector of the ProbabilityDistribution object.
        """
        return self._stateVec

    def getState(self) -> State:
        """Gets the state associated with a distribution.

        Returns
        -------
        State
            Returns the state of the ProbabilityDistribution object.
        """
        return self._state

    def setState(self, newState: State) -> None:
        """Sets the current state to a user inputted one.

        Parameters
        ----------
        newState : State
            New state for the distribution.
        """
        self._state.setState(newState)

    def setDim(self, newDim: int) -> None:
        """Sets the current dimension to a user inputted one.

        Parameters
        ----------
        newDim : int
            New dimension for the distribution.
        """
        self._n = newDim
        self._probVec = np.zeros(self._n, dtype=float)

    def getDim(self) -> int:
        """Gets the dimension associated with a distribution.

        Returns
        -------
        int
            Returns the dimension of the ProbabilityDistribution object.
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
        return self._probVec

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

    def moment(self, k: int) -> float:
        """Calculates the kth moment of the probability distribution.

        Parameters
        ----------
        k : int
            User inputted moment.

        Returns
        -------
        float
            kth moment of the probability distribution.
        """
        pos = np.arange(0, self._n)
        m = 0
        for x in range(self._n):
            m += (pos[x] ** k) * self._probVec[x]
        return float(m)

    def invPartRatio(self) -> float:
        """Calculates the inverse participation ratio of the probability distribution.

        Returns
        -------
        float
            Inverse participation ratio of the probability distribution.
        """
        return 1 / (np.sum(np.absolute(self._probVec)**2))

    def stDev(self) -> float:
        """Calculates the standard deviation of the probability distribution.

        Returns
        -------
        float
            Standard deviation of the probability distribution.
        """
        stDev = self.moment(2) - self.moment(1) ** 2
        return np.sqrt(stDev) if (stDev > 0) else 0

    def survivalProb(self, fromNode, toNode) -> float:
        """Calculates the survival probability of the probability distribution.

        Parameters
        ----------
        fromNode : _type_
            Starting Node.
        toNode : _type_
            Ending node.

        Returns
        -------
        float
            Survival probability of the probability distribution.
        """
        survProb = 0
        try:
            if fromNode == toNode:
                return self._probVec[int(k0)][0]
            else:
                for i in range(int(fromNode), int(toNode) + 1):
                    survProb += self._probVec[i]
            return survProb
        except ValueError:
            raise MissingNodeInput(
                f"A node number is missing: fromNode = {fromNode}; toNode={toNode}")

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
