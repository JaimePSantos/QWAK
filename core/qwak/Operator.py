from __future__ import annotations
from typing import Union

import networkx as nx
import sympy as sp
from scipy.linalg import inv, expm
from sympy.abc import pi
import numpy as np
from utils.jsonTools import json_matrix_to_complex, complex_matrix_to_json
import json

from qwak.Errors import MissingNodeInput
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
        self._operator = np.zeros((self._n, self._n), dtype=complex)

        self._hamiltonian = self._buildHamiltonian(self._graph,self._laplacian)
        if self._markedElements:
            self._hamiltonian = self._buildSearchHamiltonian(self._hamiltonian, self._markedElements)

        self._isHermitian = self._hermitianTest(self._hamiltonian)
        self._eigenvalues, self._eigenvectors = self._buildEigenValues(self._hamiltonian)

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
        diag = np.diag(
            np.exp(-1j * self._eigenvalues * self._time)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        if self._isHermitian:
            self._operator = np.matmul(
                    self._operator, self._eigenvectors.conjugate().transpose())
        else:
            self._operator = np.matmul(
                    self._operator, inv(
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
        self._operator = expm(-1j * self._hamiltonian * self._time)

    def _buildHamiltonian(
            self,
            graph,
            laplacian: bool,
                    ) -> np.ndarray:
        """Builds the hamiltonian of the graph, which is either the Laplacian or the simple matrix.

        Parameters
        ----------
        laplacian : bool
            Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
        markedElements : list
            List of elements for the search.
        """
        self._adjacency = nx.to_numpy_array(
            graph, dtype=complex)
        if laplacian:
            self._adjacency = self._adjacency - self._degreeDiagonalMatrix(graph)
        return -self._adjacency * self._gamma

    def _buildSearchHamiltonian(self,hamiltonian,markedElements):
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
            eigenvalues, eigenvectors = np.linalg.eigh(
                hamiltonian
            )
        else:
            eigenvalues, eigenvectors  = np.linalg.eig(
                hamiltonian )
        return eigenvalues, eigenvectors

    def _hermitianTest(self, hamiltonian) -> bool:
        """Checks if the adjacency matrix is Hermitian.

        Parameters
        ----------
        hamiltonian : np.ndarray
            Adjacency matrix.

        Returns
        -------
        bool
            True if Hermitian, False otherwise.
        """
        return np.allclose(hamiltonian, hamiltonian.conj().T)

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
        np.ndarray
            Hamiltonian of the graph.
        """
        return self._hamiltonian

    def setHamiltonian(self, hamiltonian):
        """Sets the hamiltonian for the walk.

        Parameters
        ----------
        hamiltonian : np.ndarray
            Hamiltonian of the graph.
        """
        self._hamiltonian = hamiltonian
        self._eigenvalues, self._eigenvectors = self._buildEigenValues(self._hamiltonian)

    def resetOperator(self) -> None:
        """Resets Operator object."""
        self._operator = np.zeros((self._n, self._n), dtype=complex)

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
        self._operator = np.zeros((self._n, self._n), dtype=complex)
        self._graph = graph
        self._hamiltonian = (
            nx.adjacency_matrix(self._graph).todense().astype(complex)
        )
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

    def setAdjacencyMatrix(self, adjacencyMatrix: np.ndarray) -> None:
        """Sets the adjacency matrix of the operator to a user defined one.
        Might make more sense to not give the user control over this parameter, and make
        them instead change the graph entirely.

        Parameters
        ----------
        adjacencyMatrix : np.ndarray
            New adjacency matrix.
        """
        self._hamiltonian = adjacencyMatrix.astype(complex)
        self._adjacency = self._hamiltonian
        self._n = len(self._hamiltonian)
        self.resetOperator()
        self._eigenvalues, self._eigenvectors = self._buildEigenValues(self._hamiltonian)

    def _setAdjacencyMatrixOnly(
            self, adjacencyMatrix: np.ndarray) -> None:
        """Sets the adjacency matrix of the operator to a user defined one.
        Might make more sense to not give the user control over this parameter, and make
        them instead change the graph entirely.

        Parameters
        ----------
        adjacencyMatrix : np.ndarray
            New adjacency matrix.
        """
        self._hamiltonian = adjacencyMatrix.astype(complex)
        self._n = len(self._hamiltonian)
        self.resetOperator()

    def getAdjacencyMatrix(self) -> np.ndarray:
        """Gets the current adjacency matrix of the Operator.

        Returns
        -------
        np.ndarray
            Adjacency matrix of the Operator.
        """
        return self._adjacency

    def _setOperatorVec(self, newOperator: np.ndarray) -> None:
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

    def getOperator(self) -> np.matrix:
        """Gets the numpy matrix associated with the current operator.

        Returns
        -------
        np.matrix
            Current Operator object.
        """
        return self._operator

    def checkPST(self, nodeA, nodeB):
        """Algorithm to check PST based on the article https://arxiv.org/abs/1606.02264 authored by Rodrigo Chaves.
        Checks if all the conditions are true and return the **VALUE** if the graph
        has PST and False otherwise.

        Parameters
        ----------
        nodeA : _type_
            Input node.
        nodeB : _type_
            Output node.

        Returns
        -------
        Float/Bool
            Either returns the time value of PST or False.
        """
        try:
            nodeA = int(nodeA)
            nodeB = int(nodeB)
            if nodeA > nodeB:
                nodeA, nodeB = swapNodes(nodeA, nodeB)

            symAdj = sp.Matrix(self._adjacency)
            M = self._adjacency
            P = self._eigenvectors
            P_inv = np.linalg.inv(P)
            D = np.matmul(P_inv, np.matmul(M, P))
            isCospec = isStrCospec(symAdj, nodeA, nodeB)
            chRoots, g, delta = checkRoots(
                symAdj, nodeA, self._eigenvectors, self._eigenvalues
                )
            if isCospec and chRoots:
                result = pi / (g * np.sqrt(delta))
            else:
                result = -1
            return result
        except ValueError:
            raise MissingNodeInput(
                f"A node number is missing: nodeA = {nodeA}; nodeB = {nodeB}")

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

    def to_json(self) -> str:
        """
            Converts the operator object to a JSON string.

        Returns
        -------
        str
            JSON string of the operator object.
        """
        return json.dumps({
            'graph': nx.node_link_data(self._graph),
            'time': self._time,
            'laplacian': self._laplacian,
            'markedElements': self._markedElements,
            'adjacencyMatrix': complex_matrix_to_json(self._hamiltonian),
            'eigenvalues': self._eigenvalues.tolist(),
            'eigenvectors': complex_matrix_to_json(self._eigenvectors),
            'operator': complex_matrix_to_json(self._operator),
        })

    @classmethod
    def from_json(cls, json_var: Union[str, dict]) -> Operator:
        """Converts a JSON string to an operator object.

        Parameters
        ----------
        json_var : str, dict
            JSON string of the operator object.

        Returns
        -------
        Operator
            Operator object.
        """
        if isinstance(json_var, str):
            data = json.loads(json_var)
        elif isinstance(json_var, dict):
            data = json_var
        graph = nx.node_link_graph(data['graph'])
        time = data['time']
        laplacian = data['laplacian']
        markedElements = data['markedElements']
        adjacencyMatrix = np.array(
            json_matrix_to_complex(
                data['adjacencyMatrix']))
        eigenvalues = np.array(data['eigenvalues'])

        eigenvectors = np.array(
            json_matrix_to_complex(
                data['eigenvectors']))
        operator = np.array(json_matrix_to_complex(data['operator']))

        newOp = cls(graph, time, laplacian, markedElements)
        newOp._setAdjacencyMatrixOnly(adjacencyMatrix)
        newOp._setEigenValues(eigenvalues)
        newOp._setEigenVectors(eigenvectors)
        newOp._setOperatorVec(operator)
        return newOp

    @staticmethod
    def _degreeDiagonalMatrix(G):
        degrees = np.array(list(dict(G.degree()).values()))
        return np.diag(degrees)

    def __mul__(self, other: np.ndarray) -> np.ndarray:
        """Left-side multiplication for the Operator class.

        Parameters
        ----------
        other : np.ndarray
            Another Numpy ndarray to multiply the operator by.

        Returns
        -------
        np.ndarray
            Result of the right-side multiplication.
        """
        return self._operator * other

    def __rmul__(self, other: np.ndarray) -> np.ndarray:
        """Right-side multiplication for the Operator class.

        Parameters
        ----------
        other : np.ndarray
            Another Numpy ndarray to multiply the operator by.

        Returns
        -------
        np.ndarray
            Result of the left-side multiplication.
        """
        return other * self._operator

    def __str__(self) -> str:
        """String representation of the State class.

        Returns
        -------
        str
            String representation of the Operator object.
        """
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
    