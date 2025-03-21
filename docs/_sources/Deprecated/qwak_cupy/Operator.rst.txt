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

TODO: CheckPST is not defined here. Since it will probably be moved to the
TODO: utils folder, it will be necessary to import it here.

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
hamiltonian : cp.ndarray
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
cp.ndarray
    Hamiltonian of the graph.

setHamiltonian
==============

Sets the hamiltonian for the walk.

Parameters
----------
hamiltonian : cp.ndarray
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
adjacencyMatrix : cp.ndarray
    New adjacency matrix for the Operator object.

_setAdjacencyMatrixOnly
=======================

Sets the adjacency matrix of the operator to a user defined one.
Might make more sense to not give the user control over this parameter, and make
them instead change the graph entirely.

Parameters
----------
adjacencyMatrix : cp.ndarray
    New adjacency matrix.

getAdjacencyMatrix
==================

Gets the current adjacency matrix of the Operator.

Returns
-------
cp.ndarray
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

Gets the cupy ndarray associated with the current operator.

Returns
-------
cp.ndarray
    Current Operator object.

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

__repr__
========

Representation of the ProbabilityDistribution object.

Returns
-------
str
    String of the ProbabilityDistribution object.

