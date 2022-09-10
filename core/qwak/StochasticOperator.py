from __future__ import annotations

import networkx as nx
import numpy as np
from qutip import Qobj, basis


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

    def __init__(
            self,
            graph,
            noiseParam=None,
            sinkNode=None,
            sinkRate=None) -> None:
        """_summary_

        Parameters
        ----------
        graph : _type_
            _description_
        noiseParam : _type_, optional
            _description_, by default None
        sinkNode : _type_, optional
            _description_, by default None
        sinkRate : _type_, optional
            _description_, by default None
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
        """Creates the Hamiltonian and the Lindblad operators for the walker given an adjacency matrix
        and other parameters.

        Parameters
        ----------
        noiseParam : float, optional
            Parameter controlling the 'quantumness' of the system (0 is fully quantum, 1 is fully classical), by default None.
        sinkNode : int, optional
            _description_, by default None
        sinkRate : float, optional
            If a sink is present the trasfer rate from the sink_node to the sink , by default None.
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
        """_summary_"""
        degree = np.sum(self._adjacencyMatrix, axis=0).flat
        degree = list(map(lambda x: 1 / x if x > 0 else 0, degree))
        self._laplacian = np.multiply(self._adjacencyMatrix, degree)

    def _buildQuantumHamiltonian(self) -> None:
        """_summary_"""
        if self._sinkNode is not None:
            H = Qobj(
                (1 - self._p)
                * np.pad(self._adjacencyMatrix, [(0, 1), (0, 1)], "constant")
            )
        else:
            H = Qobj((1 - self._p) * self._adjacencyMatrix)
        self._quantumHamiltonian = H

    def _buildClassicalHamiltonian(self) -> None:
        """_summary_"""
        if self._sinkNode is not None:
            L = [
                np.sqrt(self._p * self._laplacian[i, j])
                * (basis(self.n + 1, i) * basis(self.n + 1, j).dag())
                for i in range(self.n)
                for j in range(self.n)
                if self._laplacian[i, j] > 0
            ]
            # transition matrix to the sink
            S = np.zeros([self.n + 1, self.n + 1])
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

    def getClassicalHamiltonian(self) -> list:
        """_summary_

        Returns
        -------
        list
            _description_
        """
        return self._classicalHamiltonian

    def setClassicalHamiltonian(self, newClassicalHamiltonian) -> None:
        """_summary_

        Parameters
        ----------
        newClassicalHamiltonian : _type_
            _description_
        """
        self._classicalHamiltonian = newClassicalHamiltonian

    def getQuantumHamiltonian(self) -> Qobj:
        """_summary_

        Returns
        -------
        Qobj
            _description_
        """
        return self._quantumHamiltonian

    def setQuantumHamiltonian(self, newQuantumHamiltonian) -> None:
        """_summary_

        Parameters
        ----------
        newQuantumHamiltonian : _type_
            _description_
        """
        self._quantumHamiltonian = newQuantumHamiltonian

    def setSinkNode(self, newSinkNode) -> None:
        """_summary_

        Parameters
        ----------
        newSinkNode : _type_
            _description_
        """
        self._sinkNode = newSinkNode

    def getSinkNode(self) -> int:
        """_summary_

        Returns
        -------
        int
            _description_
        """
        return self._sinkNode

    def getLaplacian(self) -> np.ndarray:
        """_summary_

        Returns
        -------
        np.ndarray
            _description_
        """
        return self._laplacian