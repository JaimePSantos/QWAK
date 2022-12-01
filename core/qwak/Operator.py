from __future__ import annotations

import networkx as nx
import sympy as sp
from scipy.linalg import inv
from sympy.abc import pi
import numpy as np

from qwak.Errors import MissingNodeInput
from utils.PerfectStateTransfer import isStrCospec, checkRoots, swapNodes, getEigenVal


class Operator:
    """
    Class that represents the operators that will be used in a quantum walk.
    States are represented by matrices in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these matrices.
    """

    def __init__(
            self,
            graph: nx.Graph,
            time: float = None,
            gamma: float = None,
            laplacian: bool = False,
            markedSearch: list = None,
    ) -> None:
        """This object is initialized with a user inputted graph, which is then used to
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
        time : float
            Needs Completion.
        gamma : float
            Needs Completion.
        laplacian : bool, optional
            Allows the user to choose whether to use the Laplacian or simple adjacency matrix, by default False.
        markedSearch : list, optional
            List with marked elements for search, by default None.
        """
        if time is not None:
            self._time = time
        else:
            self._time = 0
        if gamma is not None:
            self._gamma = gamma
        else:
            self._gamma = 1
        self._graph = graph
        self._buildAdjacency(laplacian, markedSearch)
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))
        self._isHermitian = np.allclose(
            self._adjacencyMatrix,
            self._adjacencyMatrix.conjugate().transpose())
        self._buildEigenValues(self._isHermitian)

    def buildDiagonalOperator(self, time: float = None, gamma: float = None) -> None:
        """Builds operator matrix from optional time and transition rate parameters, defined by user.
        The first step is to calculate the diagonal matrix that takes in time, transition rate and
        eigenvalues and convert it to a list of the diagonal entries. The entries are then multiplied
        by the eigenvectors, and the last step is to perform matrix multiplication with the complex
        conjugate of the eigenvectors.

        Parameters
        ----------
        time : float, optional
            Time for which to calculate the operator, by default 0.
        gamma : float, optional
            Needs completion.
        """
        if time is not None:
            self._time = time
        else:
            self._time = 0
        if gamma is not None:
            self._gamma = gamma
        else:
            self._gamma = 1
        diag = np.diag(
            np.exp(-1j * self._eigenvalues * self._time * self._gamma)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        if self._isHermitian:
            self._operator = np.matmul(
                self._operator,
                self._eigenvectors.conjugate().transpose())
        else:
            self._operator = np.matmul(
                self._operator, inv(
                    self._eigenvectors))

    def _buildAdjacency(self, laplacian, markedSearch):
        """_summary_

        Parameters
        ----------
        laplacian : _type_
            _description_
        markedSearch : _type_
            _description_
        """
        if laplacian:
            self._adjacencyMatrix = np.asarray(
                nx.laplacian_matrix(
                    self._graph).todense().astype(complex))
        else:
            self._adjacencyMatrix = nx.to_numpy_array(
                self._graph, dtype=complex)
        if markedSearch is not None:
            for marked in markedSearch:
                self._adjacencyMatrix[marked[0], marked[0]] += marked[1]

    def _buildEigenValues(self, isHermitian):
        """_summary_

        Parameters
        ----------
        isHermitian : bool
            _description_
        """
        if isHermitian:
            self._eigenvalues, self._eigenvectors = np.linalg.eigh(
                self._adjacencyMatrix
            )
        else:
            self._eigenvalues, self._eigenvectors = np.linalg.eig(
                self._adjacencyMatrix)

    def resetOperator(self):
        """Resets Operator object."""
        self._operator = np.zeros((self._n, self._n))

    def setDim(self, newDim: int, graph) -> None:
        """Sets the current Operator objects dimension to a user defined one.

        Parameters
        ----------
        newDim : int
            New dimension for the Operator object.
        """
        self._n = newDim
        self._operator = np.zeros((self._n, self._n))
        self._graph = graph
        self._adjacencyMatrix = (
            nx.adjacency_matrix(self._graph).todense().astype(complex)
        )
        self.setAdjacencyMatrix(self._adjacencyMatrix)

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
        self._adjacencyMatrix = adjacencyMatrix.astype(complex)
        self._n = len(self._adjacencyMatrix)
        self.resetOperator()
        self._buildEigenValues(self._isHermitian)

    def getAdjacencyMatrix(self) -> np.ndarray:
        """Gets the current adjacency matrix of the Operator.

        Returns
        -------
        np.ndarray
            Adjacency matrix of the Operator.
        """
        return self._adjacencyMatrix

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
        # TODO: Check if numpy is faster for eigenvecs and vals.
        try:
            nodeA = int(nodeA)
            nodeB = int(nodeB)
            if nodeA > nodeB:
                nodeA, nodeB = swapNodes(nodeA, nodeB)

            symAdj = sp.Matrix(self._adjacencyMatrix.tolist())
            # Isto já foi calculado.
            eigenVec, D = symAdj.diagonalize()
            eigenVal = getEigenVal(D)
            isCospec = isStrCospec(symAdj, nodeA, nodeB)
            chRoots, g, delta = checkRoots(
                symAdj, nodeA, eigenVec, eigenVal)
            if isCospec and chRoots:
                result = pi / (g * np.sqrt(delta))
            else:
                result = -1
            return result
        except ValueError:
            raise MissingNodeInput(
                f"A node number is missing: nodeA = {nodeA}; nodeB = {nodeB}")

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

    # def transportEfficiency(self,initState):
    #     """
    #     Under Construction.
    #     @param initState:
    #     @return:
    #     """
    #     ef = 0
    #     print(f"init: {initState}")
    #     print(f"Eigenvectors {self._eigenvectors}")
    #     for i in range(len(self._eigenvectors)):
    #         eigenVec = np.transpose(self._eigenvectors[:,i]).conjugate()
    #         ef += np.absolute(np.matmul(eigenVec,initState))**2
    #         print(f"eigenVec: {eigenVec}\t\t eigenVec norm: {np.linalg.norm(eigenVec)}\t\tef : {ef}\n")
    #     return ef
