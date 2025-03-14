__init__
========

This class integrates the components of a stochastic quantum walk including
the graph, initial state, stochastic operator, quantum walk dynamics, and
probability distribution.
Initializes a StochasticQWAK instance with a graph and optional parameters.

Parameters
----------

graph : nx.Graph
    The graph over which the quantum walk is performed.
initStateList : list, optional
    List of nodes to initialize the quantum state.
customStateList : list, optional
    Custom states for the quantum walk.
noiseParam : float, optional
    Parameter controlling noise in the stochastic operator.
sinkNode : int, optional
    Node acting as a sink in the quantum walk.
sinkRate : float, optional
    Rate of transfer to the sink node.

runWalk
=======

Executes the stochastic quantum walk.

Parameters
----------

time : float, optional
    Duration of the quantum walk.
initStateList : list, optional
    Initial state list for the quantum walk.
customStateList : list, optional
    Custom state list for the quantum walk.
noiseParam : float, optional
    Noise parameter for the operator.
sinkNode : int, optional
    Sink node index in the graph.
sinkRate : float, optional
    Rate of transfer to the sink node.
observables : list, optional
    List of observables to monitor during the walk.
opts : Options, optional
    QuTiP options for the simulation.

setProbDist
===========

Sets a new probability distribution for the quantum walk.

Parameters
----------
newProbDist : StochasticProbabilityDistribution
    The new probability distribution to set.

getProbDist
===========

Returns the current probability distribution of the quantum walk.

Returns
-------
StochasticProbabilityDistribution
    The current probability distribution.

getProbVec
==========

Returns the probability vector of the current quantum state.

Returns
-------
np.ndarray
    The probability vector.

getQuantumHamiltonian
=====================

Retrieves the quantum Hamiltonian of the stochastic operator.

Returns
-------
Qobj
    The quantum Hamiltonian governing the evolution of the quantum walk.

getClassicalHamiltonian
=======================

Retrieves the classical Hamiltonian (Lindblad operators) of the stochastic operator.

Returns
-------
list[Qobj]
    A list of Lindblad operators representing the classical component of the quantum walk.

getLaplacian
============

Retrieves the Laplacian matrix of the graph associated with the stochastic operator.

Returns
-------
np.ndarray
    The Laplacian matrix of the graph.

