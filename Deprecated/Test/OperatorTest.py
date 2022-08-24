import timeit

import networkx as nx
import numpy as np
from scipy import linalg as ln


class OperatorTestV1:
    """[summary]"""

    def __init__(self, graph, time=0, gamma=1):
        """[summary]

        Args:
            graph ([type]): [description]
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
        """
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._time = time
        self._gamma = gamma
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))

        self.eighExecutionTime = 0
        self.diagExecutionTime = 0
        self.matMulExecutionTime = 0
        self.fullExecutionTime = 0

    def __mul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._operator * other

    def __rmul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return other * self._operator

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "%s" % self._operator

    def buildDiagonalOperator(self):
        """[summary]"""
        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        endTimeEigh = timeit.default_timer()
        executionTimeEigh = endTimeEigh - startTimeEigh
        self.eighExecutionTime = executionTimeEigh

        startTimeDiag = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues))
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = endTimeDiag - startTimeDiag
        self.diagExecutionTime = executionTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = self._eigenvectors @ D @ self._eigenvectors.H
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = endTimeMatMul - startTimeMatMul
        self.matMulExecutionTime = executionTimeMatMul

    def timedBuildDiagonalOperator(self):
        """[summary]"""
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = endTimeFullExec - startTimeFullExec
        self.fullExecutionTime = executionTimeFullExec

    #### ------- ####

    def setTime(self, newTime):
        """[summary]

        Args:
            newTime ([type]): [description]
        """
        self._time = newTime

    def getTime(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._time

    def setGamma(self, newGamma):
        """[summary]

        Args:
            newGamma ([type]): [description]
        """
        self._gamma = newGamma

    def getGamma(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._gamma

    def setDim(self, newDim):
        """[summary]

        Args:
            newDim ([type]): [description]
        """
        self._n = newDim

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def getAdjacencyMatrix(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self, adjacencyMatrix):
        """[summary]

        Args:
            adjacencyMatrix ([type]): [description]
        """
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        return self._operator


class OperatorTestV2:
    """[summary]"""

    def __init__(self, graph, time=0, gamma=1):
        """[summary]

        Args:
            graph ([type]): [description]
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
        """
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._time = time
        self._gamma = gamma
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))

        self.eighExecutionTime = 0
        self.diagExecutionTime = 0
        self.matMulExecutionTime = 0
        self.fullExecutionTime = 0

    def __mul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._operator * other

    def __rmul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return other * self._operator

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "%s" % self._operator

    def buildDiagonalOperator(self):
        """[summary]"""
        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        endTimeEigh = timeit.default_timer()
        executionTimeEigh = endTimeEigh - startTimeEigh
        self.eighExecutionTime = executionTimeEigh

        startTimeDiag = timeit.default_timer()
        D = np.diag(
            np.exp(-1j * self._time * self._gamma * self._eigenvalues)
        ).diagonal()
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = endTimeDiag - startTimeDiag
        self.diagExecutionTime = executionTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors, D)
        self._operator = self._operator @ self._eigenvectors.H
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = endTimeMatMul - startTimeMatMul
        self.matMulExecutionTime = executionTimeMatMul

    def timedBuildDiagonalOperator(self):
        """[summary]"""
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = endTimeFullExec - startTimeFullExec
        self.fullExecutionTime = executionTimeFullExec

    #### ------- ####

    def setTime(self, newTime):
        """[summary]

        Args:
            newTime ([type]): [description]
        """
        self._time = newTime

    def getTime(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._time

    def setGamma(self, newGamma):
        """[summary]

        Args:
            newGamma ([type]): [description]
        """
        self._gamma = newGamma

    def getGamma(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._gamma

    def setDim(self, newDim):
        """[summary]

        Args:
            newDim ([type]): [description]
        """
        self._n = newDim

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def getAdjacencyMatrix(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self, adjacencyMatrix):
        """[summary]

        Args:
            adjacencyMatrix ([type]): [description]
        """
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._operator


class OperatorTestV3:
    """[summary]"""

    def __init__(self, graph, time=0, gamma=1):
        """[summary]

        Args:
            graph ([type]): [description]
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
        """
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._time = time
        self._gamma = gamma
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))

        self.eighExecutionTime = 0
        self.diagExecutionTime = 0
        self.matMulExecutionTime = 0
        self.fullExecutionTime = 0

    def __mul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._operator * other

    def __rmul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return other * self._operator

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "%s" % self._operator

    def buildDiagonalOperator(self):
        """[summary]"""
        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = ln.eigh(
            self._adjacencyMatrix, driver="evd"
        )
        endTimeEigh = timeit.default_timer()
        executionTimeEigh = endTimeEigh - startTimeEigh
        self.eighExecutionTime = executionTimeEigh

        startTimeDiag = timeit.default_timer()
        D = np.diag(
            np.exp(-1j * self._time * self._gamma * self._eigenvalues)
        ).diagonal()
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = endTimeDiag - startTimeDiag
        self.diagExecutionTime = executionTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors, D)
        self._operator = self._operator @ self._eigenvectors.conjugate().transpose()
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = endTimeMatMul - startTimeMatMul
        self.matMulExecutionTime = executionTimeMatMul

    def timedBuildDiagonalOperator(self):
        """[summary]"""
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = endTimeFullExec - startTimeFullExec
        self.fullExecutionTime = executionTimeFullExec

    #### ------- ####

    def setTime(self, newTime):
        """[summary]

        Args:
            newTime ([type]): [description]
        """
        self._time = newTime

    def getTime(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._time

    def setGamma(self, newGamma):
        """[summary]

        Args:
            newGamma ([type]): [description]
        """
        self._gamma = newGamma

    def getGamma(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._gamma

    def setDim(self, newDim):
        """[summary]

        Args:
            newDim ([type]): [description]
        """
        self._n = newDim

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def getAdjacencyMatrix(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self, adjacencyMatrix):
        """[summary]

        Args:
            adjacencyMatrix ([type]): [description]
        """
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._operator


class OperatorTestV4:
    """[summary]"""

    def __init__(self, graph):
        """[summary]

        Args:
            graph ([type]): [description]
        """
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))

        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        endTimeEigh = timeit.default_timer()
        self.eighExecutionTime = endTimeEigh - startTimeEigh

    def __mul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._operator * other

    def __rmul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return other * self._operator

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "%s" % self._operator

    def buildDiagonalOperator(self, time, gamma):
        """[summary]

        Args:
            time ([type]): [description]
            gamma ([type]): [description]
        """
        self._time = time
        self._gamma = gamma

        startTimeDiag = timeit.default_timer()
        D = np.diag(
            np.exp(-1j * self._time * self._gamma * self._eigenvalues)
        ).diagonal()
        endTimeDiag = timeit.default_timer()
        self.diagExecutionTime = endTimeDiag - startTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors, D)
        self._operator = self._operator @ self._eigenvectors.H
        endTimeMatMul = timeit.default_timer()
        self.matMulExecutionTime = endTimeMatMul - startTimeMatMul

    def timedBuildDiagonalOperator(self, time=0, gamma=1):
        """[summary]

        Args:
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
        """
        self.diagExecutionTime = 0
        self.matMulExecutionTime = 0
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator(time, gamma)
        endTimeFullExec = timeit.default_timer()
        self.fullExecutionTime = (
            self.eighExecutionTime +
            self.diagExecutionTime +
            self.matMulExecutionTime)

    #### ------- ####

    def setTime(self, newTime):
        """[summary]

        Args:
            newTime ([type]): [description]
        """
        self._time = newTime

    def getTime(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._time

    def setGamma(self, newGamma):
        """[summary]

        Args:
            newGamma ([type]): [description]
        """
        self._gamma = newGamma

    def getGamma(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._gamma

    def setDim(self, newDim):
        """[summary]

        Args:
            newDim ([type]): [description]
        """
        self._n = newDim

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def getAdjacencyMatrix(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self, adjacencyMatrix):
        """[summary]

        Args:
            adjacencyMatrix ([type]): [description]
        """
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._operator
