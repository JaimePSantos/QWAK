__init__
========

This object is initialized with a user inputted initial state and
operator.
The dimension of the quantum walk will then be loaded from the initial
state.
The final state will contain the amplitudes of the time evolution of
the initial state, as a function of the operator. This variable is initialized
as an instance of QObj class.

Parameters
----------
state : State
    Initial state which will be the basis of the time dependant evolution.
operator : StochasticOperator
    Operator which will evolve the initial state.

buildWalk
=========

Constructs the quantum walk over a specified time frame.

Parameters
----------
time : float
    The time over which the walk is to be simulated.
observables : list, optional
    A list of observables to monitor during the walk. Defaults to an empty list.
opts : Options, optional
    QuTiP options for the simulation. Defaults to storing states and the final state.

getFinalState
=============

Returns the final quantum state after the completion of the walk.

Returns
-------

Qobj
    The final state of the quantum walk.

setFinalState
=============

Sets a new final state for the quantum walk.

Parameters
----------
newFinalState : Qobj
    The new final state to be set for the quantum walk.

getDim
======

Returns the dimension of the quantum walk's state space.

Returns
-------
int
    The dimension of the quantum walk.

