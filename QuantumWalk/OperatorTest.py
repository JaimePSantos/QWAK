import networkx as nx
import numpy as np
from scipy import linalg as ln
from scipy import sparse
from scipy.sparse import issparse
import timeit

class OperatorTest:
    def __init__(self,graph,time=0,gamma=1):
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._time = time
        self._gamma = gamma
        self._n = len(graph)
        self._operator = np.zeros((self._n,self._n))

    def __mul__(self,other):
        return self._operator*other

    def __rmul__(self,other):
        return other*self._operator

    def __str__(self):
        return '%s' % self._operator

    def buildOperator(self):
        self._operator = ln.expm(-1j * self._gamma * self._adjacencyMatrix * self._time)

    def buildDiagonalOperator(self):
        startTimeExpm = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(self._adjacencyMatrix)
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tEigh took %s seconds." % executionTimeExpm)

        startTimeExpm = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues))
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tDiag took %s seconds." % executionTimeExpm)

        startTimeExpm = timeit.default_timer()
        self._operator = (self._eigenvectors @ D @ self._eigenvectors.H)
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tMatMul took %s seconds." % executionTimeExpm)

    def buildDiagonalOperator2(self):
        startTimeExpm = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(self._adjacencyMatrix)
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tEigh took %s seconds." % executionTimeExpm)

        startTimeExpm = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues)).diagonal()
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tDiag took %s seconds." % executionTimeExpm)

        startTimeExpm = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors,D)
        self._operator = self._operator @ self._eigenvectors.H
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tMatMul took %s seconds." % executionTimeExpm)

    def buildDiagonalOperator3(self):
        startTimeExpm = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = ln.eigh(self._adjacencyMatrix)
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tEigh took %s seconds." % executionTimeExpm)

        startTimeExpm = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues)).diagonal()
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tDiag took %s seconds." % executionTimeExpm)

        startTimeExpm = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors,D)
        self._operator = self._operator @ self._eigenvectors.conjugate().transpose()
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("\tMatMul took %s seconds." % executionTimeExpm)

    def timedBuildDiagonalOperator(self):
        startTimeExpm = timeit.default_timer()
        self.buildDiagonalOperator()
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("Diagonal operator took %s seconds.\n" % executionTimeExpm)

    def timedBuildDiagonalOperator2(self):
        startTimeExpm = timeit.default_timer()
        self.buildDiagonalOperator2()
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("Faster Diagonal operator took %s seconds.\n " % executionTimeExpm)

    def timedBuildDiagonalOperator3(self):
        startTimeExpm = timeit.default_timer()
        self.buildDiagonalOperator3()
        endTimeExpm = timeit.default_timer()
        executionTimeExpm = (endTimeExpm - startTimeExpm)
        print("Faster Diagonal operator took %s seconds.\n " % executionTimeExpm)

    def setTime(self,newTime):
        self._time = newTime

    def getTime(self):
        return self._time

    def setGamma(self, newGamma):
        self._gamma = newGamma

    def getGamma(self):
        return self._gamma

    def setDim(self,newDim):
        self._n = newDim

    def getDim(self):
        return self._n

    def getAdjacencyMatrix(self):
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self,adjacencyMatrix):
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self,newOperator):
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        return self._operator

