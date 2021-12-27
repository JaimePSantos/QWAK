import networkx as nx
import numpy as np
from scipy import linalg as ln
from scipy import sparse
from scipy.sparse import issparse
import timeit


class OperatorTestV4:
    def __init__(self, graph):
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))

        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        endTimeEigh = timeit.default_timer()
        self.eighExecutionTime = (endTimeEigh - startTimeEigh)

    def __mul__(self, other):
        return self._operator*other

    def __rmul__(self, other):
        return other*self._operator

    def __str__(self):
        return '%s' % self._operator

    def buildDiagonalOperator(self, time, gamma):
        self._time = time
        self._gamma = gamma

        startTimeDiag = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues)).diagonal()
        endTimeDiag = timeit.default_timer()
        self.diagExecutionTime = endTimeDiag - startTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors,D)
        self._operator = self._operator @ self._eigenvectors.H
        endTimeMatMul = timeit.default_timer()
        self.matMulExecutionTime = endTimeMatMul - startTimeMatMul

    def timedBuildDiagonalOperator(self, time=0, gamma=1):
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator(time, gamma)
        endTimeFullExec = timeit.default_timer()
        self.fullExecutionTime = endTimeFullExec - startTimeFullExec

    #### ------- ####

    def setTime(self, newTime):
        self._time = newTime

    def getTime(self):
        return self._time

    def setGamma(self, newGamma):
        self._gamma = newGamma

    def getGamma(self):
        return self._gamma

    def setDim(self, newDim):
        self._n = newDim

    def getDim(self):
        return self._n

    def getAdjacencyMatrix(self):
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self, adjacencyMatrix):
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self, newOperator):
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        return self._operator
