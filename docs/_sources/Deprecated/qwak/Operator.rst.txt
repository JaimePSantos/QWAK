__init__
========

Class for the quantum walk operator.

This object is initialized with a user inputted graph, which is then used to
generate the dimension of the operator and the adjacency matrix, which is
the central structure required to perform walks on regular graphs. Note that this
version of the software only supports regular undirected graphs, which will hopefully
be generalized in the future.

The eigenvalues and eigenvectors of the adjacency matrix are also calculated during
initialization, which are then used to calculate the diagonal operator through spectral
decomposition. This was the chosen method since it is computationally cheaper than calculating
the matrix exponent directly.

Parameters
----------
graph : nx.Graph
    Graph where the walk will be performed.
gamma : float
    Needs Completion.
time: float, optional
    Time for which to calculate the operator, by default None.
laplacian : bool, optional
    Allows the user to choose whether to use the Laplacian or simple adjacency matrix, by default False.
markedElements : list, optional
    List with marked elements for search, by default None.

buildDiagonalOperator
=====================

Builds operator matrix from optional time and transition rate parameters, defined by user.

The first step is to calculate the diagonal matrix that takes in time, transition rate and
eigenvalues and convert it to a list of the diagonal entries.

The entries are then multiplied
by the eigenvectors, and the last step is to perform matrix multiplication with the complex
conjugate of the eigenvectors.

Parameters
----------
time : float, optional
    Time for which to calculate the operator, by default 0.
gamma : float, optional
    Needs completion.
round : int, optional

buildExpmOperator
=================

Builds operator matrix from optional time and transition rate parameters, defined by user.

Uses the scipy function expm to calculate the matrix exponential of the adjacency matrix.

Parameters
----------
time : float, optional
    Time for which to calculate the operator, by default 0.

_buildHamiltonian
=================

Builds the hamiltonian of the graph, which is either the Laplacian or the simple matrix.

Parameters
----------
laplacian : bool
    Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
markedElements : list
    List of elements for the search.

_buildEigenValues
=================

Builds the eigenvalues and eigenvectors of the adjacency matrix.

Parameters
----------
isHermitian : bool
    Checks if the adjacency matrix is Hermitian.

_hermitianTest
==============

Checks if the adjacency matrix is Hermitian.

Parameters
----------
hamiltonian : np.ndarray
    Adjacency matrix.

Returns
-------
bool
    True if Hermitian, False otherwise.

getEigenValues
==============

Returns the eigenvalues of the adjacency matrix.

Returns
-------
list
    List of eigenvalues.

_setEigenValues
===============

Sets the eigenvalues of the adjacency matrix.

Parameters
----------
eigenValues : list
    List of eigenvalues.

getEigenVectors
===============

Returns the eigenvectors of the adjacency matrix.

Returns
-------
list
    List of eigenvectors.

_setEigenVectors
================

Sets the eigenvectors of the adjacency matrix.

Parameters
----------
eigenVectors : list
    _description_

getHamiltonian
==============

Returns the hamiltonian of the graph, which is either the Laplacian or the simple matrix.

Returns
-------
np.ndarray
    Hamiltonian of the graph.

setHamiltonian
==============

Sets the hamiltonian for the walk.

Parameters
----------
hamiltonian : np.ndarray
    Hamiltonian of the graph.

resetOperator
=============

Resets Operator object.

setDim
======

Sets the current Operator objects dimension to a user defined one.

Parameters
----------
newDim : int
    New dimension for the Operator object.
graph : nx.Graph
    New graph for the Operator object.

getDim
======

Gets the current graph dimension.

Returns
-------
int
    Dimension of Operator object.

setTime
=======

Sets the current operator time to a user defined one.

Parameters
----------
newTime : float
    New operator time.

getTime
=======

Gets the current operator time.

Returns
-------
float
    Current time of Operator object.

setAdjacencyMatrix
==================

Sets the adjacency matrix of the operator to a user defined one.
Might make more sense to not give the user control over this parameter, and make
them instead change the graph entirely.

Parameters
----------
adjacencyMatrix : np.ndarray
    New adjacency matrix.

_setAdjacencyMatrixOnly
=======================

Sets the adjacency matrix of the operator to a user defined one.
Might make more sense to not give the user control over this parameter, and make
them instead change the graph entirely.

Parameters
----------
adjacencyMatrix : np.ndarray
    New adjacency matrix.

getAdjacencyMatrix
==================

Gets the current adjacency matrix of the Operator.

Returns
-------
np.ndarray
    Adjacency matrix of the Operator.

_setOperatorVec
===============

Sets all the parameters of the current operator to user defined ones.

Parameters
----------
newOperator : Operator
    New user inputted Operator.

setOperator
===========

Sets all the parameters of the current operator to user defined ones.

Parameters
----------
newOperator : Operator
    New user inputted Operator.

getOperator
===========

Gets the numpy matrix associated with the current operator.

Returns
-------
np.matrix
    Current Operator object.

checkPST
========

Algorithm to check PST based on the article https://arxiv.org/abs/1606.02264 authored by Rodrigo Chaves.
Checks if all the conditions are true and return the **VALUE** if the graph
has PST and False otherwise.

Parameters
----------
nodeA : _type_
    Input node.
nodeB : _type_
    Output node.

Returns
-------
Float/Bool
    Either returns the time value of PST or False.

getMarkedElements
=================

Returns the marked elements of the operator.

Returns
-------
list
    List of marked elements.

setMarkedElements
=================

Sets the marked elements of the operator.

Parameters
----------
markedElements : list
    List of marked elements.

to_json
=======

    Converts the operator object to a JSON string.

Returns
-------
str
    JSON string of the operator object.

from_json
=========

Converts a JSON string to an operator object.

Parameters
----------
json_var : str, dict
    JSON string of the operator object.

Returns
-------
Operator
    Operator object.

__mul__
=======

Left-side multiplication for the Operator class.

Parameters
----------
other : np.ndarray
    Another Numpy ndarray to multiply the operator by.

Returns
-------
np.ndarray
    Result of the right-side multiplication.

__rmul__
========

Right-side multiplication for the Operator class.

Parameters
----------
other : np.ndarray
    Another Numpy ndarray to multiply the operator by.

Returns
-------
np.ndarray
    Result of the left-side multiplication.

__str__
=======

String representation of the State class.

Returns
-------
str
    String representation of the Operator object.

__repr__
========

Representation of the ProbabilityDistribution object.

Returns
-------
str
    String of the ProbabilityDistribution object.

