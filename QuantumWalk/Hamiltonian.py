import numpy as np


class Hamiltonian:
    def __init__(self,n,graph=None):
        self._n = n
        self._ham = np.zeros((self._n,self._n))
        self._graph = None
        if graph is not None:
            self._graph = graph

    def __mul__(self,other):
        return self._ham*other

    def __rmul__(self,other):
        return other*self._ham

    def buildHam(self):
        if self._graph is not None:
            self._ham = self._graph.adjacency_matrix()

    def setDim(self, newN):
        self._n = newN

    def getDim(self):
        return self._n

    def setGraph(self,newGraph):
        self._graph = newGraph

    def getGraph(self):
        return self._graph

    def setHam(self,newHam):
        self._n = newHam.getDim()
        self._graph = newHam.getGraph()
        self._ham = newHam.getHam()

    def getHam(self):
        return self._ham
