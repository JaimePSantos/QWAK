__init__
========

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

buildStochasticOperator
=======================

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

_buildLaplacian
===============

Internal method to build the Laplacian matrix from the adjacency matrix of the graph.

_buildQuantumHamiltonian
========================

Internal method to build the quantum Hamiltonian from the graph's adjacency matrix.

_buildClassicalHamiltonian
==========================

Internal method to build the classical Hamiltonian (Lindblad operators).

getClassicalHamiltonian
=======================

Returns the classical Hamiltonian (Lindblad operators) of the system.

Returns
-------
list[Qobj]
    A list of Qobj representing the Lindblad operators.

setClassicalHamiltonian
=======================

Sets a new classical Hamiltonian for the system.

Parameters
----------
newClassicalHamiltonian : list of Qobj
    The new list of Lindblad operators to set as the classical Hamiltonian.

getQuantumHamiltonian
=====================

Returns the quantum Hamiltonian of the system.

Returns
-------
Qobj
    The quantum Hamiltonian as a QuTiP object.

setQuantumHamiltonian
=====================

Sets a new quantum Hamiltonian for the system.

Parameters
----------
newQuantumHamiltonian : Qobj
    The new quantum Hamiltonian as a QuTiP object.

setSinkNode
===========

Sets a new sink node for the system.

Parameters
----------
newSinkNode : int
    The index of the new sink node in the graph.

getSinkNode
===========

Returns the index of the current sink node in the graph.

Returns
-------
int
    The index of the sink node.

getLaplacian
============

Returns the Laplacian matrix of the graph.

Returns
-------
np.ndarray
    The Laplacian matrix.

