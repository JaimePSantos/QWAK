__init__
========

A class to represent the probability distribution of a quantum state in a stochastic system.

Initializes the probability distribution with a given quantum state.

Parameters
----------
state : Qobj
    Initial state which will be the basis of the time dependant evolution.

buildProbDist
=============

Builds or updates the probability distribution of the system based on the given quantum state.

Parameters
----------
state : Qobj, optional
    The quantum state to be used for updating the probability distribution.
    If None, the existing final state is used. Default is None.

getProbVec
==========

Returns the probability vector representing the distribution of the current state.

Returns
-------
np.ndarray
    The probability vector of the current state, flattened.

setProbVec
==========

Sets a new final state for the probability distribution.

Parameters
----------
newFinalState : np.ndarray
    The new final state to be set for the probability distribution.

