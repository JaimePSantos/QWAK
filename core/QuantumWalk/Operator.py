from __future__ import annotations

import networkx as nx
import numpy as np
from Tools.PerfectStateTransfer import isStrCospec, checkRoots
from sympy import Matrix, gcd, div, Poly, Float, pprint
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

class Operator:
    """
    Class that represents the operators that will be used in a quantum walk.
    States are represented by matrices in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these matrices.
    """

    def __init__(self, graph: nx.Graph,laplacian:bool=False) -> None:
        """
        This object is initialized with a user inputted graph, which is then used to
        generate the dimension of the operator and the adjacency matrix, which is
        the central structure required to perform walks on regular graphs. Note that this
        version of the software only supports regular undirected graphs, which will hopefully
        be generalized in the future.

        The eigenvalues and eigenvectors of the adjacency matrix are also calculated during
        initialization, which are then used to calculate the diagonal operator through spectral
        decomposition. This was the chosen method since it is computationally cheaper than calculating
        the matrix exponent directly.

        TODO: Verificar se a matriz ponderada e hermitiana ou nao.
        TODO: Funcao para fazermos um loading screen na criacao do operador.

        Args:
            :param laplacian: Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
            :type laplacian: bool
            :param graph: Graph where the walk will be performed.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        if laplacian:
            self._adjacencyMatrix = nx.laplacian_matrix(graph).todense()
        else:
            self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        self._time = 0
        self._gamma = 1

    def __mul__(self, other):
        """
        Left-side multiplication for the Operator class.

        Args:
            :param other: Another Numpy ndarray to multiply the operator by.
            :type other: Numpy.ndarray

        Returns:
            :return: self._operator * other
            :rtype: Numpy.ndarray
        """
        return self._operator * other

    def __rmul__(self, other):
        """
        Right-side multiplication for the Operator class.

        Args:
            :param other: Another Numpy ndarray to multiply the operator by.
            :type other: Numpy.ndarray

        Returns:
            :return: self._operator * other
            :rtype: Numpy.ndarray
        """
        return other * self._operator

    def __str__(self) -> str:
        """
        String representation of the State class.

        Returns:
            :return: f"{self._stateVec}"
            :rtype: str
        """
        return f"{self._operator}"

    def resetOperator(self):
        self._operator = np.zeros((self._n, self._n))

    def buildDiagonalOperator(self, time: float = 0, gamma: float = 1) -> None:
        """
        Builds operator matrix from optional time and transition rate parameters, defined by user.
        The first step is to calculate the diagonal matrix that takes in time, transition rate and
        eigenvalues and convert it to a list of the diagonal entries. The entries are then multiplied
        by the eigenvectors, and the last step is to perform matrix multiplication with the complex
        conjugate of the eigenvectors.

        Args:
            :param time: Time for which to calculate the operator. Defaults to 0.
            :type time: (int, optional)
            :param gamma: Transition rate of the given operator. Defaults to 1.
            :type gamma: (int, optional)
        """
        self._time = time
        self._gamma = gamma
        D = np.diag(np.exp(-1j * self._time * self._gamma *
                           self._eigenvalues)).diagonal()
        self._operator = np.multiply(self._eigenvectors, D)
        self._operator = self._operator @ self._eigenvectors.H

    def setDim(self, newDim: int) -> None:
        """
        Sets the current operator dimensions to a user defined one.

        Args:
            newDim ([type]): [description]
            :param newDim:
            :type newDim:
        """
        self._n = newDim

    def getDim(self) -> int:
        """
        Gets the current graph dimension.

        Returns:
            :return: self._n
            :rtype: int
        """
        return self._n

    def setTime(self, newTime: float) -> None:
        """
        Sets the current operator time to a user defined one.

        Args:
            :param newTime: New operator time.
            :type newTime: float
        """
        self._time = newTime

    def getTime(self) -> float:
        """
        Gets the current operator time.

        Returns:
            :return: self._time
            :rtype: float
        """
        return self._time

    def setGamma(self, newGamma: float) -> None:
        """
        Sets the current operator transition rate to a user defined one.

        Args:
            :param newGamma: New transition rate.
            :type newGamma: float
        """
        self._gamma = newGamma

    def getGamma(self) -> float:
        """
        Gets the current walk transition rate.

        Returns:
            :return: self._gamma
            :rtype: float
        """
        return self._gamma

    def setAdjacencyMatrix(self, adjacencyMatrix: np.ndarray) -> None:
        """
        Sets the adjacency matrix of the operator to a user defined one.
        Might make more sense to not give the user control over this parameter, and make
        them instead change the graph entirely.

        Args:
            :param adjacencyMatrix: New Numpy.ndarray adjacency matrix.
            :type adjacencyMatrix: Numpy.ndarray
        """
        self._adjacencyMatrix = adjacencyMatrix

    def getAdjacencyMatrix(self) -> np.ndarray:
        """
        Gets the current adjacency matrix of the operator.

        Returns:
            :return: self._adjacencyMatrix
            :rtype: Numpy.ndarray
        """
        return self._adjacencyMatrix

    def setOperator(self, newOperator: Operator) -> None:
        """
        Sets all the parameters of the current operator to user defined ones.

        Args:
            :param newOperator: New operator.
            :type newOperator: Operator
        """
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self) -> np.matrix:
        """
        Gets the numpy matrix associated with the current operator.

        Returns:
            :return: self._operator
            :rtype: Numpy.matrix
        """
        return self._operator

    def checkPST(self,nodeA, nodeB):
        """
         Checks if all the conditions are true and return the **VALUE** if the graph
         has PST and False otherwise.

        :param nodeA: Input node.
        :type nodeA: int
        :param nodeB: Output node.
        :type nodeB: int

        Returns:
            :return: pi / (g * np.sqrt(delta)) or False
            :rtype: **Value** or Bool
        """
        if nodeA > nodeB:
            temp = nodeA
            nodeA = nodeB
            nodeB = temp
        symAdj = sp.Matrix(self._adjacencyMatrix.tolist())
        (eigenvec, D) = A.diagonalize()
        eigenval = []

        ## Notice that I was having rouding problems because Python was not considering 6x10^-50 to be zero, so I made a loop
        # to garantee that it is zero.
        for i in range(len(D.col(0))):
            temp = D.col(i)[i]
            if abs(temp) < 0.0000001:
                temp = 0
            eigenval.append(temp)

        result, g, delta = checkRoots(symAdj, nodeA, eigenvec, eigenval)
        if isStrCospec(symAdj, nodeA, nodeB) and result:
            return pi / (g * np.sqrt(delta))
        else:
            return False
