import networkx as nx
from scipy import linalg as ln
import numpy as np

from qwak.Operator import Operator


class OperatorBenchmark2:
    def __init__(
        self,
        graph,
        eigen=False,
    ) -> None:
        """_summary_

        Parameters
        ----------
        graph : nx.Graph
            _description_
        laplacian : bool, optional
            _description_, by default False
        markedSearch : _type_, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_
        """
        self._adjacencyMatrix = np.asarray(
            nx.laplacian_matrix(graph).todense().astype(complex))
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix
        )

    def buildDiagonalOperatorEig(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> None:
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        diag = np.diag(
            np.exp(-1j * self._eigenvalues * time)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        self._operator = np.matmul(
            self._operator, self._eigenvectors.conjugate().transpose()
        )

    def buildDiagonalOperatorNoEig(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> None:
        diag = np.diag(
            np.exp(-1j * self._eigenvalues * time)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        self._operator = np.matmul(
            self._operator, self._eigenvectors.conjugate().transpose()
        )

    def buildSlowDiagonalOperator(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> None:
        self._adjacencyMatrix = np.asarray(
            nx.laplacian_matrix(graph).todense().astype(complex))
        self.slowperator = ln.expm(-1j * self._adjacencyMatrix * time)

    def buildSlowDiagonalOperatorNoAdj(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None,
            time: float = 0) -> None:
        self.slowperator = ln.expm(-1j * self._adjacencyMatrix * time)
