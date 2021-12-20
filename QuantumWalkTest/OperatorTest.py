import networkx as nx
import numpy as np
from scipy import linalg as ln
from scipy import sparse
from scipy.sparse import issparse
import timeit

class OperatorTest:
    def __init__(self,graph,time=0,gamma=1,mode='default'):
        if mode == 'default':
            self._graph = graph
            self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
            self._time = time
            self._gamma = gamma
            self._n = len(graph)
            self._operator = np.zeros((self._n,self._n))

            self.eighExecutionTime = 0
            self.eighExecutionTime2 = 0
            self.eighExecutionTime3 = 0

            self.diagExecutionTime = 0
            self.diagExecutionTime2 = 0
            self.diagExecutionTime3 = 0

            self.matMulExecutionTime = 0
            self.matMulExecutionTime2 = 0
            self.matMulExecutionTime3 = 0

            self.fullExecutionTime = 0
            self.fullExecutionTime2 = 0
            self.fullExecutionTime3 = 0

        elif mode == 'opt':
            self._graph = graph
            self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
            self._n = len(graph)
            self._operator = np.zeros((self._n,self._n))    

            startTimeEigh = timeit.default_timer()
            self._eigenvalues, self._eigenvectors = np.linalg.eigh(self._adjacencyMatrix)
            endTimeEigh = timeit.default_timer()
            executionTimeEigh = (endTimeEigh - startTimeEigh)
            self.eighExecutionTime = executionTimeEigh

            self.diagExecutionTime = 0
            self.diagExecutionTime2 = 0
            self.diagExecutionTime3 = 0

            self.matMulExecutionTime = 0
            self.matMulExecutionTime2 = 0
            self.matMulExecutionTime3 = 0

            self.fullExecutionTime = 0
            self.fullExecutionTime2 = 0
            self.fullExecutionTime3 = 0
        
        else:
            print("%s Wrong operator mode")
            return

    def __mul__(self,other):
        return self._operator*other

    def __rmul__(self,other):
        return other*self._operator

    def __str__(self):
        return '%s' % self._operator

    def buildDiagonalOperator(self):
        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(self._adjacencyMatrix)
        endTimeEigh = timeit.default_timer()
        executionTimeEigh = (endTimeEigh - startTimeEigh)
        self.eighExecutionTime = executionTimeEigh

        startTimeDiag = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues))
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = (endTimeDiag - startTimeDiag)
        self.diagExecutionTime = executionTimeDiag


        startTimeMatMul = timeit.default_timer()
        self._operator = (self._eigenvectors @ D @ self._eigenvectors.H)
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = (endTimeMatMul - startTimeMatMul)
        self.matMulExecutionTime = executionTimeMatMul


    def buildDiagonalOperator2(self):
        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(self._adjacencyMatrix)
        endTimeEigh = timeit.default_timer()
        executionTimeEigh = (endTimeEigh - startTimeEigh)
        self.eighExecutionTime2 = executionTimeEigh

        startTimeDiag = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues)).diagonal()
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = (endTimeDiag - startTimeDiag)
        self.diagExecutionTime2 = executionTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors,D)
        self._operator = self._operator @ self._eigenvectors.H
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = (endTimeMatMul - startTimeMatMul)
        self.matMulExecutionTime2 = executionTimeMatMul


    def buildDiagonalOperator3(self):
        startTimeEigh = timeit.default_timer()
        self._eigenvalues, self._eigenvectors = ln.eigh(self._adjacencyMatrix,driver='evd')
        endTimeEigh = timeit.default_timer()
        executionTimeEigh = (endTimeEigh - startTimeEigh)
        self.eighExecutionTime3 = executionTimeEigh

        startTimeDiag = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues)).diagonal()
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = (endTimeDiag - startTimeDiag)
        self.diagExecutionTime3 = executionTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = np.multiply(self._eigenvectors,D)
        self._operator = self._operator @ self._eigenvectors.conjugate().transpose()
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = (endTimeMatMul - startTimeMatMul)
        self.matMulExecutionTime3 = executionTimeMatMul
    
    def buildDiagonalOperator4(self,time = 0, gamma = 1):
        self._time = time
        self._gamma = gamma

        startTimeDiag = timeit.default_timer()
        D = np.diag(np.exp(-1j * self._time * self._gamma * self._eigenvalues))
        endTimeDiag = timeit.default_timer()
        executionTimeDiag = (endTimeDiag - startTimeDiag)
        self.diagExecutionTime = executionTimeDiag

        startTimeMatMul = timeit.default_timer()
        self._operator = (self._eigenvectors @ D @ self._eigenvectors.H)
        endTimeMatMul = timeit.default_timer()
        executionTimeMatMul = (endTimeMatMul - startTimeMatMul)
        self.matMulExecutionTime = executionTimeMatMul

    def timedBuildDiagonalOperator(self):
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = (endTimeFullExec - startTimeFullExec)
        self.fullExecutionTime = executionTimeFullExec

    def timedBuildDiagonalOperator2(self):
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator2()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = (endTimeFullExec - startTimeFullExec)
        self.fullExecutionTime2 = executionTimeFullExec

    def timedBuildDiagonalOperator3(self):
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator3()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = (endTimeFullExec - startTimeFullExec)
        self.fullExecutionTime3 = executionTimeFullExec

    def timedBuildDiagonalOperator4(self):
        startTimeFullExec = timeit.default_timer()
        self.buildDiagonalOperator4()
        endTimeFullExec = timeit.default_timer()
        executionTimeFullExec = (endTimeFullExec - startTimeFullExec)
        self.fullExecutionTime3 = executionTimeFullExec
    
    
    #### ------- ####

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

