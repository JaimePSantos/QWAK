import networkx as nx
import numpy as np
from scipy import linalg as ln
from timeit import default_timer as timer

# Assuming this is your custom import
from qwak.Operator import Operator


class OperatorBenchmark3:
    def __init__(self, graph, eigen=False) -> None:
        self._graph = graph

    def buildAdjacencyTimed(self):
        start_time = timer()
        self._adjacencyMatrix = np.asarray(
            nx.laplacian_matrix(self._graph).todense().astype(complex))
        end_time = timer()
        return end_time - start_time

    def buildEigenTimed(self):
        start_time = timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        end_time = timer()
        return end_time - start_time

    def buildDiagonalOperatorEigTimed(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> float:
        start_time = timer()
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        diag = np.diag(
            np.exp(-1j * self._eigenvalues * time)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        self._operator = np.matmul(
            self._operator, self._eigenvectors.conjugate().transpose()
        )
        end_time = timer()
        return end_time - start_time

    def buildDiagonalOperatorNoEigTimed(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> float:
        start_time = timer()
        diag = np.diag(
            np.exp(-1j * self._eigenvalues * time)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        self._operator = np.matmul(
            self._operator, self._eigenvectors.conjugate().transpose()
        )
        end_time = timer()
        return end_time - start_time

    def buildSlowDiagonalOperatorTimed(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> float:
        start_time = timer()
        self._adjacencyMatrix = np.asarray(
            nx.laplacian_matrix(graph).todense().astype(complex))
        self.slowperator = ln.expm(-1j * self._adjacencyMatrix * time)
        end_time = timer()
        return end_time - start_time

    def buildSlowDiagonalOperatorNoAdjTimed(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> float:
        start_time = timer()
        self.slowperator = ln.expm(-1j * self._adjacencyMatrix * time)
        end_time = timer()
        return end_time - start_time
