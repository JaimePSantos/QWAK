import numpy as np


class State:
    """[summary]
    """

    def __init__(self, n, stateList=None):
        """[summary]

        Args:
            n ([type]): [description]
            stateList ([type], optional): [description]. Defaults to None.
        """
        self._n = n
        self._stateList = stateList
        self._stateVec = np.zeros((self._n, 1))

    def __mul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._stateVec * other

    def __rmul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return other * self._stateVec

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return '%s' % self._stateVec

    def buildState(self, stateList):
        """[summary]

        Args:
            stateList ([type]): [description]
        """
        self._stateList = stateList
        if self._stateList is not None:
            for state in self._stateList:
                self._stateVec[state] = 1 / np.sqrt(len(self._stateList))

    def setDim(self, newN):
        """[summary]

        Args:
            newN ([type]): [description]
        """
        self._n = newN

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    # TODO: This might not be needed.
    def setStateList(self, newState):
        """[summary]

        Args:
            newState ([type]): [description]
        """
        self._stateList = newState

    def getStateList(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._stateList

    def setStateVec(self, newVec):
        """[summary]

        Args:
            newVec ([type]): [description]
        """
        self._stateVec = newVec

    def getStateVec(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._stateVec

    def setState(self, newState):
        """[summary]

        Args:
            newState ([type]): [description]
        """
        self._n = newState.getDim()
        self._stateList = newState.getStateList()
        self._stateVec = newState.getStateVec()
