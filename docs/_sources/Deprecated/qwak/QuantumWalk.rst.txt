__init__
========

This object is initialized with a user inputted initial state and
operator.
The dimension of the quantum walk will then be loaded from the initial
state.
The final state will contain the amplitudes of the time evolution of
the initial state, as a function of the operator. This variable is initialized
as an instance of State class.

Parameters
----------
state : State
    Initial state which will be the basis of the time dependant evolution.
operator : Operator
    Operator which will evolve the initial state.

buildWalk
=========

Builds the final state of the quantum walk by setting it to the matrix
multiplication of the operator by the initial state.

Parameters
----------
initState : State, optional
    Initial state which will be the basis of the time dependant evolution, by default None.
operator : Operator, optional
    Operator which will evolve the initial state, by default None.

resetWalk
=========

Resets the components of the QuantumWalk object.

setInitState
============

Sets the initial state of the quantum walk to a new user inputted one.

Parameters
----------
newInitState : State
    New initial state for the quantum walk.

getInitState
============

Gets the initial state of the quantum walk.

Returns
-------
State
    Initial state of the quantum walk.

setDim
======

Sets the current quantum walk dimension to a user defined one.

Parameters
----------
newDim : int
    New QuantumWalk dimension.

getDim
======

Gets the current state dimension.

Returns
-------
int
    QuantumWalk dimension.

setOperator
===========

Sets the current operator to a user defined one.

Parameters
----------
newOperator : Operator
    New quantum walk operator.

getOperator
===========

Gets the current operator.

Returns
-------
Operator
    Current QuantumWalk Operator object.

setWalk
=======

Sets all the parameters of the current quantum walk to user defined ones.

Parameters
----------
newWalk : QuantumWalk
    New quantum walk.

getFinalState
=============

Gets the final state of the QuantumWalk.

Returns
-------
State
    Final state of the QuantumWalk.

setFinalState
=============

Sets the final state of the QuantumWalk.

Parameters
-------
finalState: State
    Final state of the QuantumWalk.

getAmpVec
=========

Gets the vector of the final state amplitudes of the  QuantumWalk.

Returns
-------
np.ndarray
    Vector of the final state.

searchNodeAmplitude
===================

Searches and gets the amplitude associated with a given node.

Parameters
----------
searchNode : int
    User inputted node for the search.

Returns
-------
complex
    Amplitude of the search node.

transportEfficiency
===================

Calculates the transport efficiency of the quantum walk.

Returns
-------
float
    Transport efficiency of the quantum walk.

to_json
=======

Serializes the QuantumWalk object to JSON format.

Returns
-------
str
    JSON string representation of the QuantumWalk object.

from_json
=========

Deserializes a JSON string to a QuantumWalk object.

Parameters
----------
json_str : str
    JSON string representation of the QuantumWalk object.

Returns
-------
QuantumWalk
    Deserialized QuantumWalk object.

__str__
=======

String representation of the StaticQuantumwalk class.

Returns
-------
str
    QuantumWalk string.

__repr__
========

Representation of the ProbabilityDistribution object.

Returns
-------
str
    String of the ProbabilityDistribution object.

