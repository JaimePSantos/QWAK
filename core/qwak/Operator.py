from __future__ import annotations

import networkx as nx
import numpy as np
import sympy as sp
from scipy.linalg import inv
from sympy.abc import pi
import numpy as np
from qutip import Qobj, basis, mesolve, Options

from Tools.PerfectStateTransfer import isStrCospec, checkRoots, swapNodes, getEigenVal


class Operator:
    """
    Class that represents the operators that will be used in a quantum walk.
    States are represented by matrices in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these matrices.
    """

    def __init__(
        self,
        graph: nx.Graph,
        laplacian: bool = False,
        adjacencyMatrix=None,
        markedSearch=None,
    ) -> None:
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

        Args:
            :param laplacian: Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
            :type laplacian: bool
            :param graph: Graph where the walk will be performed.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        self._buildAdjacency(laplacian, markedSearch)
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))
        self._isHermitian = np.allclose(self._adjacencyMatrix, self._adjacencyMatrix.H)
        self._time = 0
        self._buildEigenValues(self._isHermitian)

    def buildDiagonalOperator(self, time: float = 0) -> None:
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
        diag = np.diag(np.exp(-1j * self._eigenvalues * self._time)).diagonal()
        self._operator = np.multiply(self._eigenvectors, diag)
        if self._isHermitian:
            self._operator = np.matmul(self._operator, self._eigenvectors.H)
        else:
            self._operator = np.matmul(self._operator, inv(self._eigenvectors))

    def _buildAdjacency(self, laplacian, markedSearch):
        if laplacian:
            self._adjacencyMatrix = (
                nx.laplacian_matrix(self._graph).todense().astype(complex)
            )
        else:
            self._adjacencyMatrix = (
                nx.adjacency_matrix(self._graph).todense().astype(complex)
            )
        if markedSearch is not None:
            for marked in markedSearch:
                self._adjacencyMatrix[marked[0], marked[0]] += marked[1]

    def _buildEigenValues(self, isHermitian):
        if isHermitian:
            self._eigenvalues, self._eigenvectors = np.linalg.eigh(
                self._adjacencyMatrix
            )
        else:
            self._eigenvalues, self._eigenvectors = np.linalg.eig(self._adjacencyMatrix)

    def resetOperator(self):
        self._operator = np.zeros((self._n, self._n))

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

    def setAdjacencyMatrix(self, adjacencyMatrix: np.ndarray) -> None:
        """
        Sets the adjacency matrix of the operator to a user defined one.
        Might make more sense to not give the user control over this parameter, and make
        them instead change the graph entirely.

        Args:
            :param adjacencyMatrix: New Numpy.ndarray adjacency matrix.
            :type adjacencyMatrix: Numpy.ndarray
        """
        self._adjacencyMatrix = adjacencyMatrix.astype(complex)
        self._n = len(self._adjacencyMatrix)
        self.resetOperator()
        self._buildEigenValues(self._isHermitian)

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

    def checkPST(self, nodeA, nodeB):
        """
         Checks if all the conditions are true and return the **VALUE** if the graph
         has PST and False otherwise.
         TODO: Check if numpy is faster for eigenvecs and vals.

         Args:
            :param nodeA: Input node.
            :type nodeA: int
            :param nodeB: Output node.
            :type nodeB: int

        Returns:
            :return: pi / (g * np.sqrt(delta)) or False
            :rtype: **Value** or Bool
        """
        if nodeA > nodeB:
            nodeA, nodeB = swapNodes(nodeA, nodeB)

        symAdj = sp.Matrix(self._adjacencyMatrix.tolist())
        # Isto já foi calculado.
        eigenVec, D = symAdj.diagonalize()
        eigenVal = getEigenVal(D)
        isCospec = isStrCospec(symAdj, nodeA, nodeB)
        chRoots, g, delta = checkRoots(symAdj, nodeA, eigenVec, eigenVal)
        if isCospec and chRoots:
            result = pi / (g * np.sqrt(delta))
        else:
            result = -1
        return result

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


class StochasticOperator(object):
    """
    Stochastic quantum walker on QuTip.
    Class containing an open quantum system described by a Lindblad equation obtained from the adjacency matrix.

    Theoretical model:
    Whitfield, J. D., Rodríguez-Rosario, C. A., & Aspuru-Guzik, A. (2010).
    Quantum stochastic walks: A generalization of classical random walks and quantum walks.
    Physical Review A, 81(2), 022323.

    @author: Lorenzo Buffoni
    """

    def __init__(self, graph, noiseParam=None, sinkNode=None, sinkRate=None):
        self._graph = graph
        self.n = len(self._graph) 
        self._adjacencyMatrix = (
            nx.adjacency_matrix(self._graph).todense().astype(complex)
        )
        # TODO: Why cant we use the normal laplacian?
        # self._laplacian = np.matrix(
        #    nx.laplacian_matrix(self._graph).todense().astype(complex)
        # )
        # normalized laplacian of the classical random walk
        self._buildLaplacian()
        if noiseParam is None:
            self._p = 0.0
        else:
            self._p = noiseParam
        if sinkRate is None:
            self._sinkRate = 1.0
        else:
            self._sinkRate = sinkRate
        self._sinkNode = sinkNode
        self._quantumHamiltonian = Qobj()
        self._classicalHamiltonian = []

    def buildStochasticOperator(self, noiseParam=None, sinkNode=None, sinkRate=None):
        """Creates the Hamiltonian and the Lindblad operators for the walker given an adjacency matrix
        and other parameters.

        Parameters
        ----------
        noise_param : float between 0 and 1
            parameter controlling the 'quantumness' of the system (0 is fully quantum, 1 is fully classical)
        sinkRate : float between 0 and 1
            if a sink is present the trasfer rate from the sink_node to the sink (defaults to 1.)
        """
        if noiseParam is not None:
            self._p = noiseParam
        if sinkRate is not None:
            self._sinkRate = sinkRate
        if sinkNode is not None:
            self._sinkNode = sinkNode
        self._buildQuantumHamiltonian()
        self._buildClassicalHamiltonian()

    def _buildLaplacian(self):
        degree = np.sum(self._adjacencyMatrix, axis=0).flat
        degree = list(map(lambda x : 1/x if x>0 else 0, degree))
        self._laplacian = np.multiply(self._adjacencyMatrix,degree)
        
    def _buildQuantumHamiltonian(self):
        if self._sinkNode is not None:
            H = Qobj(
                (1 - self._p)
                * np.pad(self._adjacencyMatrix, [(0, 1), (0, 1)], "constant")
            )
        else:
            H = Qobj((1 - self._p) * self._adjacencyMatrix)
        self._quantumHamiltonian = H

    def _buildClassicalHamiltonian(self):
        if self._sinkNode is not None:
            L = [
                np.sqrt(self._p * self._laplacian[i, j])
                * (basis(self.n + 1, i) * basis(self.n + 1, j).dag())
                for i in range(self.n)
                for j in range(self.n)
                if self._laplacian[i, j] > 0
            ]
            S = np.zeros([self.n + 1, self.n + 1])  # transition matrix to the sink
            S[self.n, self._sinkNode] = np.sqrt(2 * self._sinkRate)
            L.append(Qobj(S))
        else:
            L = [
                np.sqrt(self._p * self._laplacian[i, j])
                * (basis(self.n, i) * basis(self.n, j).dag())
                for i in range(self.n)
                for j in range(self.n)
                if self._laplacian[i, j] > 0
            ]
        self._classicalHamiltonian = L

    def getClassicalHamiltonian(self):
        return self._classicalHamiltonian

    def setClassicalHamiltonian(self, newClassicalHamiltonian):
        self._classicalHamiltonian = newClassicalHamiltonian

    def getQuantumHamiltonian(self):
        return self._quantumHamiltonian

    def setQuantumHamiltonian(self, newQuantumHamiltonian):
        self._quantumHamiltonian = newQuantumHamiltonian

    def setSinkNode(self, newSinkNode):
        self._sinkNode = newSinkNode

    def getSinkNode(self):
        return self._sinkNode

    def getLaplacian(self):
        return self._laplacian
