from __future__ import annotations
from typing import Union

import networkx as nx
import sympy as sp
import cupyx.scipy.linalg as cpx_scipy
from sympy.abc import pi
import cupy as cp
from utils.jsonTools import json_matrix_to_complex, complex_matrix_to_json
import json

from qwak_cupy.Errors import MissingNodeInput
from utils.PerfectStateTransfer import isStrCospec, checkRoots, swapNodes, getEigenVal


class Operator:
    def __init__(
            self,
            graph: nx.Graph,
            gamma: float = 1,
            time: float = 0,
            laplacian: bool = False,
            markedElements: list = [],
    ) -> None:
        """
        Class for the quantum walk operator.

        This object is initialized with a user inputted graph, which is then used to
        generate the dimension of the operator and the adjacency matrix, which is
        the central structure required to perform walks on regular graphs. Note that this
        version of the software only supports regular undirected graphs, which will hopefully
        be generalized in the future.

        The eigenvalues and eigenvectors of the adjacency matrix are also calculated during
        initialization, which are then used to calculate the diagonal operator through spectral
        decomposition. This was the chosen method since it is computationally cheaper than calculating
        the matrix exponent directly.

        TODO: CheckPST is not defined here. Since it will probably be moved to the
        TODO: utils folder, it will be necessary to import it here.

        Parameters
        ----------
        graph : nx.Graph
            Graph where the walk will be performed.
        gamma : float
            Needs Completion.
        time: float, optional
            Time for which to calculate the operator, by default None.
        laplacian : bool, optional
            Allows the user to choose whether to use the Laplacian or simple adjacency matrix, by default False.
        markedElements : list, optional
            List with marked elements for search, by default None.
        """
        self._time = time
        self._gamma = gamma
        self._laplacian = laplacian
        self._markedElements = markedElements
        self._graph = graph
        self._n = len(graph)
        self._operator = cp.zeros((self._n, self._n), dtype=complex)

        self._hamiltonian = self._buildHamiltonian(
            self._graph, self._laplacian)
        if self._markedElements:
            self._hamiltonian = self._buildSearchHamiltonian(
                self._hamiltonian, self._markedElements)

        self._isHermitian = self._hermitianTest(self._hamiltonian)
        self._eigenvalues, self._eigenvectors = self._buildEigenValues(
            self._hamiltonian)

    def buildDiagonalOperator(self, time: float = 0) -> None:
        """Builds operator matrix from optional time and transition rate parameters, defined by user.

        The first step is to calculate the diagonal matrix that takes in time, transition rate and
        eigenvalues and convert it to a list of the diagonal entries.

        The entries are then multiplied
        by the eigenvectors, and the last step is to perform matrix multiplication with the complex
        conjugate of the eigenvectors.

        Parameters
        ----------
        time : float, optional
            Time for which to calculate the operator, by default 0.
        gamma : float, optional
            Needs completion.
        round : int, optional
        """
        self._time = time
        diag = cp.diag(
            cp.exp(-1j * self._eigenvalues * self._time)).diagonal()
        self._operator = cp.multiply(self._eigenvectors, diag)
        if self._isHermitian:
            self._operator = cp.matmul(
                self._operator, self._eigenvectors.conjugate().transpose())
        else:
            self._operator = cp.matmul(
                self._operator, cpx_scipy.inv(
                    self._eigenvectors))

    def buildExpmOperator(self, time: float = 0) -> None:
        """Builds operator matrix from optional time and transition rate parameters, defined by user.

        Uses the scipy function expm to calculate the matrix exponential of the adjacency matrix.

        Parameters
        ----------
        time : float, optional
            Time for which to calculate the operator, by default 0.
        """
        self._time = time
        self._operator = cpx_scipy.expm(-1j *
                                        self._hamiltonian * self._time)

    def _buildHamiltonian(
            self,
            graph,
            laplacian: bool,
    ) -> cp.ndarray:
        """Builds the hamiltonian of the graph, which is either the Laplacian or the simple matrix.

        Parameters
        ----------
        laplacian : bool
            Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
        markedElements : list
            List of elements for the search.
        """
        self._adjacency = cp.array(nx.to_numpy_array(
            graph, dtype=complex))
        if laplacian:
            self._adjacency = self._adjacency - \
                self._degreeDiagonalMatrix(graph)
        return -self._adjacency * self._gamma

    def _buildSearchHamiltonian(self, hamiltonian, markedElements):
        for marked in markedElements:
            hamiltonian[marked[0], marked[0]] += marked[1]
        return hamiltonian

    def _buildEigenValues(self, hamiltonian) -> None:
        """Builds the eigenvalues and eigenvectors of the adjacency matrix.

        Parameters
        ----------
        isHermitian : bool
            Checks if the adjacency matrix is Hermitian.
        """

        if self._isHermitian:
            eigenvalues, eigenvectors = cp.linalg.eigh(
                hamiltonian
            )
        else:
            eigenvalues, eigenvectors = cp.linalg.eig(
                hamiltonian)
        return eigenvalues, eigenvectors

    def _hermitianTest(self, hamiltonian) -> bool:
        """Checks if the adjacency matrix is Hermitian.

        Parameters
        ----------
        hamiltonian : cp.ndarray
            Adjacency matrix.

        Returns
        -------
        bool
            True if Hermitian, False otherwise.
        """
        return cp.allclose(hamiltonian, hamiltonian.conj().T)

    def getEigenValues(self) -> list:
        """Returns the eigenvalues of the adjacency matrix.

        Returns
        -------
        list
            List of eigenvalues.
        """
        return self._eigenvalues

    def _setEigenValues(self, eigenValues: list) -> None:
        """Sets the eigenvalues of the adjacency matrix.

        Parameters
        ----------
        eigenValues : list
            List of eigenvalues.
        """
        self._eigenvalues = eigenValues

    def getEigenVectors(self) -> list:
        """Returns the eigenvectors of the adjacency matrix.

        Returns
        -------
        list
            List of eigenvectors.
        """
        return self._eigenvectors

    def _setEigenVectors(self, eigenVectors: list) -> None:
        """Sets the eigenvectors of the adjacency matrix.

        Parameters
        ----------
        eigenVectors : list
            _description_
        """
        self._eigenvectors = eigenVectors

    def getHamiltonian(self):
        """Returns the hamiltonian of the graph, which is either the Laplacian or the simple matrix.

        Returns
        -------
        cp.ndarray
            Hamiltonian of the graph.
        """
        return self._hamiltonian

    def setHamiltonian(self, hamiltonian):
        """Sets the hamiltonian for the walk.

        Parameters
        ----------
        hamiltonian : cp.ndarray
            Hamiltonian of the graph.
        """
        self._hamiltonian = hamiltonian
        self._eigenvalues, self._eigenvectors = self._buildEigenValues(
            self._hamiltonian)

    def resetOperator(self) -> None:
        """Resets Operator object."""
        self._operator = cp.zeros((self._n, self._n), dtype=complex)

    def setDim(self, newDim: int, graph: nx.Graph) -> None:
        """Sets the current Operator objects dimension to a user defined one.

        Parameters
        ----------
        newDim : int
            New dimension for the Operator object.
        graph : nx.Graph
            New graph for the Operator object.
        """
        self._n = newDim
        self._operator = cp.zeros((self._n, self._n), dtype=complex)
        self._graph = graph
        self._hamiltonian = (
            cp.array(
                nx.adjacency_matrix(
                    self._graph).todense(),
                dtype=complex))
        self._adjacency = self._hamiltonian
        self.setAdjacencyMatrix(self._hamiltonian)

    def getDim(self) -> int:
        """Gets the current graph dimension.

        Returns
        -------
        int
            Dimension of Operator object.
        """
        return self._n

    def setTime(self, newTime: float) -> None:
        """Sets the current operator time to a user defined one.

        Parameters
        ----------
        newTime : float
            New operator time.
        """
        self._time = newTime

    def getTime(self) -> float:
        """Gets the current operator time.

        Returns
        -------
        float
            Current time of Operator object.
        """
        return self._time

    def setAdjacencyMatrix(self, adjacencyMatrix: cp.ndarray) -> None:
        """Sets the adjacency matrix of the operator to a user defined one.
        Might make more sense to not give the user control over this parameter, and make
        them instead change the graph entirely.

        Parameters
        ----------
        adjacencyMatrix : cp.ndarray
            New adjacency matrix for the Operator object.
        """
        self._hamiltonian = adjacencyMatrix.astype(complex)
        self._adjacency = self._hamiltonian
        self._n = len(self._hamiltonian)
        self.resetOperator()
        self._eigenvalues, self._eigenvectors = self._buildEigenValues(
            self._hamiltonian)

    def _setAdjacencyMatrixOnly(
            self, adjacencyMatrix: cp.ndarray) -> None:
        """Sets the adjacency matrix of the operator to a user defined one.
        Might make more sense to not give the user control over this parameter, and make
        them instead change the graph entirely.

        Parameters
        ----------
        adjacencyMatrix : cp.ndarray
            New adjacency matrix.
        """
        self._hamiltonian = adjacencyMatrix.astype(complex)
        self._n = len(self._hamiltonian)
        self.resetOperator()

    def getAdjacencyMatrix(self) -> cp.ndarray:
        """Gets the current adjacency matrix of the Operator.

        Returns
        -------
        cp.ndarray
            Adjacency matrix of the Operator.
        """
        return self._adjacency

    def _setOperatorVec(self, newOperator: cp.ndarray) -> None:
        """Sets all the parameters of the current operator to user defined ones.

        Parameters
        ----------
        newOperator : Operator
            New user inputted Operator.
        """
        self._operator = newOperator

    def setOperator(self, newOperator: Operator) -> None:
        """Sets all the parameters of the current operator to user defined ones.

        Parameters
        ----------
        newOperator : Operator
            New user inputted Operator.
        """
        self._n = newOperator.getDim()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self) -> cp.ndarray:
        """Gets the cupy ndarray associated with the current operator.

        Returns
        -------
        cp.ndarray
            Current Operator object.
        """
        return self._operator

    def getMarkedElements(self) -> list:
        """Returns the marked elements of the operator.

        Returns
        -------
        list
            List of marked elements.
        """
        return self._markedElements

    def setMarkedElements(self, markedElements: list) -> None:
        """Sets the marked elements of the operator.

        Parameters
        ----------
        markedElements : list
            List of marked elements.
        """
        self._markedElements = markedElements

    @staticmethod
    def _degreeDiagonalMatrix(G):
        degrees = cp.array(list(dict(G.degree()).values()))
        return cp.diag(degrees)

    def __mul__(self, other: cp.ndarray) -> cp.ndarray:
        return self._operator * other

    def __rmul__(self, other: cp.ndarray) -> cp.ndarray:
        return other * self._operator

    def __str__(self) -> str:
        return f"{self._operator}"

    def __repr__(self) -> str:
        """Representation of the ProbabilityDistribution object.

        Returns
        -------
        str
            String of the ProbabilityDistribution object.
        """
        return f"N: {self._n}\n" \
            f"Time: {self._time}\n" \
            f"Graph: {nx.to_dict_of_dicts(self._graph)}\n" \
            f"Operator:\n\t{self._operator}"
