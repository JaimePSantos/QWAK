from __future__ import annotations

import networkx as nx
import numpy as np
from qutip import Qobj, basis


class StochasticOperator(object):

    def __init__(
            self,
            graph: nx.Graph,
            noiseParam: float =None,
            sinkNode: int = None,
            sinkRate: float = None) -> None:
        """
        Stochastic quantum walker on QuTip.
        Class containing an open quantum system described by a Lindblad equation obtained from the adjacency matrix.

        Theoretical model:
        Whitfield, J. D. et al.
        Quantum stochastic walks: A generalization of classical random walks and quantum walks.

        @author: Lorenzo Buffoni

        Parameters
        ----------
        graph : networkx.Graph
            The graph representing the quantum walk space.
        noiseParam : float, optional
            The noise parameter controlling the quantum-classical mix (default is 0 for a fully quantum system).
        sinkNode : int, optional
            The index of the sink node in the graph (default is None, indicating no sink node).
        sinkRate : float, optional
            The rate at which probability is transferred to the sink node (default is 1).
        """
        self._graph = graph
        self.n = len(self._graph)
        self._adjacencyMatrix = (
            nx.adjacency_matrix(self._graph).todense().astype(complex)
        )
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

    def buildStochasticOperator(
            self,
            noiseParam: float = None,
            sinkNode: int = None,
            sinkRate: float = None) -> None:
        """
        Creates the Hamiltonian and the Lindblad operators for the walker given an adjacency matrix
        and other parameters.

        Parameters
        ----------
        noiseParam : float, optional
            The noise parameter controlling the quantum-classical mix (default is 0 for a fully quantum system).
        sinkNode : int, optional
            The index of the sink node in the graph (default is None, indicating no sink node).
        sinkRate : float, optional
            The rate at which probability is transferred to the sink node (default is 1).
        """
        if noiseParam is not None:
            self._p = noiseParam
        if sinkRate is not None:
            self._sinkRate = sinkRate
        if sinkNode is not None:
            self._sinkNode = sinkNode
        self._buildQuantumHamiltonian()
        self._buildClassicalHamiltonian()

    def _buildLaplacian(self) -> None:
        """
        Internal method to build the Laplacian matrix from the adjacency matrix of the graph.
        """
        degree = np.sum(self._adjacencyMatrix, axis=0).flat
        degree = list(map(lambda x: 1 / x if x > 0 else 0, degree))
        self._laplacian = np.multiply(self._adjacencyMatrix, degree)

    def _buildQuantumHamiltonian(self) -> None:
        """
        Internal method to build the quantum Hamiltonian from the graph's adjacency matrix.
        """
        if self._sinkNode is not None:
            H = Qobj(
                (1 - self._p)
                * np.pad(self._adjacencyMatrix, [(0, 1), (0, 1)], "constant")
            )
        else:
            H = Qobj((1 - self._p) * self._adjacencyMatrix)
        self._quantumHamiltonian = H

    def _buildClassicalHamiltonian(self) -> None:
        """
        Internal method to build the classical Hamiltonian (Lindblad operators).
        """
        print('_buildClassicalHamiltonian Temporarily unavailable')
        return
        # if self._sinkNode is not None:
        #     L = [
        #         np.sqrt(self._p * self._laplacian[i, j])
        #         * (basis(self.n + 1, i) * basis(self.n + 1, j).dag())
        #         for i in range(self.n)
        #         for j in range(self.n)
        #         if self._laplacian[i, j] > 0
        #     ]
        #     S = np.zeros([self.n + 1, self.n + 1])
        #     S[self.n, self._sinkNode] = np.sqrt(2 * self._sinkRate)
        #     L.append(Qobj(S))
        # else:
        #     L = [
        #         np.sqrt(self._p * self._laplacian[i, j])
        #         * (basis(self.n, i) * basis(self.n, j).dag())
        #         for i in range(self.n)
        #         for j in range(self.n)
        #         if self._laplacian[i, j] > 0
        #     ]
        # self._classicalHamiltonian = L

    def getClassicalHamiltonian(self) -> list:
        """
        Returns the classical Hamiltonian (Lindblad operators) of the system.

        Returns
        -------
        list[Qobj]
            A list of Qobj representing the Lindblad operators.
        """
        print('getClassicalHamiltonian Temporarily unavailable')
        return None
       # return self._classicalHamiltonian

    def setClassicalHamiltonian(self, newClassicalHamiltonian) -> None:
        """
        Sets a new classical Hamiltonian for the system.

        Parameters
        ----------
        newClassicalHamiltonian : list of Qobj
            The new list of Lindblad operators to set as the classical Hamiltonian.
        """
        self._classicalHamiltonian = newClassicalHamiltonian

    def getQuantumHamiltonian(self) -> Qobj:
        """
        Returns the quantum Hamiltonian of the system.

        Returns
        -------
        Qobj
            The quantum Hamiltonian as a QuTiP object.
        """
        return self._quantumHamiltonian

    def setQuantumHamiltonian(self, newQuantumHamiltonian) -> None:
        """
        Sets a new quantum Hamiltonian for the system.

        Parameters
        ----------
        newQuantumHamiltonian : Qobj
            The new quantum Hamiltonian as a QuTiP object.
        """
        self._quantumHamiltonian = newQuantumHamiltonian

    def setSinkNode(self, newSinkNode) -> None:
        """
        Sets a new sink node for the system.

        Parameters
        ----------
        newSinkNode : int
            The index of the new sink node in the graph.
        """
        self._sinkNode = newSinkNode

    def getSinkNode(self) -> int:
        """
        Returns the index of the current sink node in the graph.

        Returns
        -------
        int
            The index of the sink node.
        """
        return self._sinkNode

    def getLaplacian(self) -> np.ndarray:
        """
        Returns the Laplacian matrix of the graph.

        Returns
        -------
        np.ndarray
            The Laplacian matrix.
        """
        return self._laplacian