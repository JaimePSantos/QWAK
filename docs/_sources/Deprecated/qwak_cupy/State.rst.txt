__init__
========

Object is initialized with a mandatory user inputted dimension, an optional
stateList parameter which will be used to create the amplitudes for each node in the state
and an internal stateVec which will be a CuPy ndarray representing the column vector.

Parameters
----------
n : int
    Desired dimension of the state.
nodeList : list, optional
    List containing what nodes will have uniform superposition in the state, by default None.
customStateList : list, optional
    Custom amplitudes for the state, by default None.

buildState
==========

Builds state vector from state list, by creating a balanced superposition of all
nodes in the nodeList.

Parameters
----------
nodeList : list, optional
    List containing what nodes will have uniform superposition in the state, by default None.
customStateList : list, optional
    Custom amplitudes for the state, by default None.

_checkStateOutOfBounds
======================

Checks if the state is out of bounds for the system.

Parameters
----------
node : int
    Node to check.

Raises
------
StateOutOfBounds
    Out of bounds exception.

_checkUnitaryStateList
======================

Checks if the sum of the square of the amplitudes is 1.

Parameters
----------
customStateList : list
    Custom state list.

Raises
------
NonUnitaryState
    Non unitary state exception.

herm
====

Returns the Hermitian conjugate of the state vector.

Returns
-------
cp.ndarray
    Hermitian conjugate of the state vector.

inv
===

Returns the inverse of the state vector.

Returns
-------
cp.ndarray
    Inverse of the state vector.

resetState
==========

Resets the components of the State.

setDim
======

Sets the current state dimension to a user defined one.

Parameters
----------
newDim : int
    New state dimension.
newNodeList : list, optional
    List containing the new nodes, by default None.

getDim
======

Gets the current state dimension.

Returns
-------
int
    State dimension.

setNodeList
===========

Sets current node list to a user inputted one.

Parameters
----------
newNodeList : list
    List containing the new nodes.

getNodeList
===========

Gets the current list of nodes.

Returns
-------
list
    Current list of nodes.

setStateVec
===========

Sets the column vector associated with the state to a user defined one.

Parameters
----------
newVec : cp.ndarray
    New column vector for the state.

getStateVec
===========

Gets the column vector associated with the state.

Returns
-------
cp.ndarray
    Vector of the State.

setState
========

Sets all the parameters of the current state to user defined ones.

Parameters
----------
newState : State
    New state.

to_json
=======

In contrast, the to_json method is not marked with the @classmethod decorator because
it is a method that is called on an instance of the State class.

This means that it can access the attributes of the instance on which it is called, and it
uses these attributes to generate the JSON string representation of the State instance.

Since it requires access to the attributes of a specific State instance, it cannot be
called on the State class itself.

Returns
-------
str
    JSON string representation of the State instance.

from_json
=========

The from_json method is marked with the @classmethod decorator because it is a method that is called on the class itself,
rather than on an instance of the class.

This is necessary because it is used to create a new instance of the State class from a JSON string,
and it does not require an instance of the State class to do so.

Parameters
----------
json_var : Union([str, dict])
    JSON string or dictionary representation of the State instance.

Returns
-------
State
    State instance from JSON string or dictionary representation.

__mul__
=======

Left-side multiplication for the State class.

Parameters
----------
other : cp.ndarray
    Another CuPy ndarray to multiply the state by.

Returns
-------
cp.ndarray
    Array of the multiplication.

__rmul__
========

Right-side multiplication for the State class.

Parameters
----------
other : cp.ndarray
    Another CuPy ndarray to multiply the state by.

Returns
-------
cp.ndarray
    Array of the multiplication.

__matmul__
==========

Matrix multiplication for the State class.

Parameters
----------
other : cp.ndarray
    Another CuPy ndarray to multiply the state by.

Returns
-------
cp.ndarray
    Array of the multiplication.

__str__
=======

String representation of the State class.

Returns
-------
str
    State string.

__repr__
========

String representation of the State class.

Returns
-------
str
    State string.

