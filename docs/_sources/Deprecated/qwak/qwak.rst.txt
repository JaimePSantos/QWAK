__init__
========

Data access class that combines all three components required to
perform a continuous-time quantum walk, given by the multiplication of
an operator (represented by the Operator class) by an initial state
(State class).  This multiplication is achieved in the
StaticQuantumwalk class, which returns a final state (State Class)
representing the amplitudes of each state associated with a graph node.
These amplitudes can then be transformed to probability distributions
(ProbabilityDistribution class) suitable for plotting with matplotlib,
or your package of choice.

Default values for the initial state, time and transition rate are a
column vector full of 0s, 0 and 1, respectively. Methods runWalk or
buildWalk must then be used to generate the results of the quantum
walk.

Parameters
----------
graph : nx.Graph
    NetworkX graph where the walk takes place. Also used
    for defining the dimensions of the quantum walk.
time : float
    Time interval for the quantum walk, by default None.
timeList : list
    List with time intervals for multiple walks, by default None.
initStateList : list[int], optional
    List with chosen initial states for uniform superposition, by default None
customStateList : list[(int,complex)], optional
    Custom init state, by default None.
laplacian : bool, optional
    Allows the user to choose whether to use the
    Laplacian or simple adjacency matrix, by default False.
markedElements : list, optional
    List with marked elements for search, by default None.
qwakId : str, optional
    User-defined ID for the QWAK instance, by default 'userUndef'.

runWalk
=======

Builds class' attributes, runs the walk and calculates the amplitudes
and probability distributions with the given parameters. These can be
accessed with their respective get methods.

Parameters
----------
time : float, optional
    Time for which to calculate the quantum walk, by default 0.
initStateList : list[int], optional
    List with chosen initial states for uniform superposition, by default None.
customStateList : list[(int,complex)], optional
    Custom init state, by default None.

Raises
------
stOBErr
    State out of bounds exception.
nUErr
    State not unitary exception.

runExpmWalk
===========

Builds class' attributes, runs the walk and calculates the amplitudes
and probability distributions with the given parameters. These can be
accessed with their respective get methods.

Parameters
----------
time : float, optional
    Time for which to calculate the quantum walk, by default 0.
initStateList : list[int], optional
    List with chosen initial states for uniform superposition, by default None.
customStateList : list[(int,complex)], optional
    Custom init state, by default None.

Raises
------
stOBErr
    State out of bounds exception.
nUErr
    State not unitary exception.

runMultipleWalks
================

Runs the walk for multiple times and stores the probability distributions
in a list.

Parameters
----------
timeList : list, optional
    List of times for which to calculate the quantum walk, by default None.
initStateList : list, optional
    List with chosen initial states for uniform superposition, by default None.
customStateList : list, optional
    Custom init state, by default None.

Raises
------
UndefinedTimeList
    Raised when the timeList is None.

runMultipleExpmWalks
====================

Runs the walk for multiple times and stores the probability distributions
in a list.

Parameters
----------
timeList : list, optional
    List of times for which to calculate the quantum walk, by default None.
initStateList : list, optional
    List with chosen initial states for uniform superposition, by default None.
customStateList : list, optional
    Custom init state, by default None.

Raises
------
UndefinedTimeList
    Raised when the timeList is None.

resetWalk
=========

Resets the components of a walk.

setDim
======

Sets the current walk dimensions to a user defined one.
Also takes a graph string to be
evaluated and executed as a NetworkX graph generator.

Parameters
----------
newDim : int
    New dimension for the quantum walk.
graphStr : str
    Graph string to generate the graph with the new dimension.
graph : nx.Graph, optional
    Graph with the new dimension.
initStateList : list[int], optional
    Init state list with new dimension.

getDim
======

Gets the current graph dimension.

Returns
-------
int
    Dimension of graph.

setGraph
========

Sets the current graph to a user defined one.
Also recalculates the current operator and walk dimension.

Parameters
----------
newGraph : nx.Graph
    New NetworkX graph.

getGraph
========

Gets the current graph.

Returns
-------
nx.Graph
    Current graph.

setCustomGraph
==============

Sets the current graph to a user defined one.

Parameters
----------
customAdjMatrix : np.ndarray
    Adjacency matrix of the new graph.

setInitState
============

Sets the current initial state to a user defined one.

Parameters
----------
newInitState : State
    New initial state.

getInitState
============

Gets the initial state.

Returns
-------
State
    Initial State.

setTime
=======

Sets the current walk time to a user defined one.

Parameters
----------
newTime : float
    New time.

setTimeList
===========

Sets the current walk time to a user defined one.

Parameters
----------
newTimeList : list
    New time list.

getTime
=======

Gets the current walk time.

Returns
-------
float
   Current value of time.

getTimeList
===========

Gets the current walk time.

Returns
-------
float
   Current value of time.

setAdjacencyMatrix
==================

Sets the current adjacency matrix to a user defined one.

Parameters
----------
newAdjMatrix : np.ndarray
    New adjacency matrix.
initStateList : list, optional
    New initial state list, by default None.

getAdjacencyMatrix
==================

Gets the current adjacency matrix.

Returns:
    np.ndarray:
        Current adjacency matrix.

setHamiltonian
==============

Sets the current Hamiltonian to a user defined one.

Parameters
----------
newHamiltonian : np.ndarray
    New Hamiltonian.

getHamiltonian
==============

Gets the current Hamiltonian.

Returns
-------
np.ndarray
    Current Hamiltonian.

setOperator
===========

Sets the current walk operator a user defined one.

Parameters
----------
newOperator : Operator
    New operator object.

getOperator
===========

Gets the current walk operator.

Returns
-------
Operator
    Current operator object.

setWalk
=======

Sets current walk amplitudes to a user defined state.
This might not be needed and removed in the future.

Parameters
----------
newWalk : State
    New walk amplitudes.

getWalk
=======

Gets current QuantumWalk object

Returns
-------
QuantumWalk
    Current state amplitudes.

getFinalState
=============

Gets current QuantumWalk State.

Returns
-------
State
    State of the QuantumWalk.

getAmpVec
=========

Gets the array of the QuantumWalk state.

Returns
-------
np.ndarray
    Array of the QuantumWalk state.

setProbDist
===========

Sets current walk probability distribution to a user defined one.
This might not be needed and removed in the future.

Parameters
----------
newProbDist : ProbabilityDistribution
    New probability distribution.

getProbDist
===========

Gets the current probability distribution.

Returns
-------
ProbabilityDistribution
    ProbabilityDistribution object.

getProbDistList
===============

Returns a list of probability distributions in the case of multiple walks.

Returns
-------
list
    List of ProbabilityDistribution objects.

setProbDistList
===============

Sets the current probability distribution list to a user defined one.

Parameters
----------
newProbDistList : list
    New probability distribution list.

getProbVec
==========

Gets the current probability distribution vector.

Returns
-------
np.ndarray
    Probability Distribution vector.

getProbVecList
==============

Returns a list of probability distribution vectors in the case of multiple walks.

Returns
-------
list
    List of probability distribution vectors.

searchNodeAmplitude
===================

User inputted node for search

Parameters
----------
searchNode : int
    User inputted node for the search.

Returns
-------
complex
    Amplitude associated with the search node.

searchNodeProbability
=====================

Searches and gets the probability associated with a given node.

Parameters
----------
searchNode : int
    User inputted node for the search.

Returns
-------
float
    Probability associated with the search node.

getMean
=======

Gets the mean of the probability distribution.

Parameters
----------
resultRounding : int, optional
    Rounding of the result, by default None.

Returns
-------
float
    Mean of the probability distribution.

getMeanList
===========

Gets the mean of the probability distribution list.

Parameters
----------
resultRounding : int, optional
    Rounding of the results, by default None.

Returns
-------
list
    List of means of the probability distributions.

getSndMoment
============

Gets the second moment of the probability distribution.

Parameters
----------
resultRounding : int, optional
    Rounding of the result, by default None.

Returns
-------
float
    Second moment of the probability distribution.

getStDev
========

Gets the standard deviation of the probability distribution.

Parameters
----------
resultRounding : int, optional
    Rounding of the result, by default None.

Returns
-------
float
    Standard deviation of the probability distribution.

getStDevList
============

Gets the standard deviation of the probability distribution list.

Parameters
----------
resultRounding : int, optional
    Rounding of the results, by default None.

Returns
-------
list
    List of standard deviations of the probability distributions.

getInversePartRatio
===================

Gets the inverse participation ratio of the probability distribution.

Parameters
----------
resultRounding : int, optional
    Rounding of the result, by default None.

Returns
-------
float
    Inverse participation ratio of the probability distribution.

getInversePartRatioList
=======================

Gets the inverse participation ratio of the probability distribution list.

Parameters
----------
resultRounding : int, optional
    Rounding of the results, by default None.

Returns
-------
list
    List of inverse participation ratios of the probability distributions.

getSurvivalProb
===============

Gets the survival probability of the probability distribution.

Parameters
----------
fromNode : _type_
    Starting node.
toNode : _type_
    Ending node.
resultRounding : int, optional
    Rounding of the result, by default None.

Returns
-------
float
    Survival probability of the probability distribution.

Raises
------
MissingNodeInput
    Missing input node error.

getSurvivalProbList
===================

Gets the survival probability of the probability distribution list.

Parameters
----------
fromNode : _type_
    Starting node.
toNode : _type_
    Ending node.
resultRounding : int, optional
    Rounding of the results, by default None.

Returns
-------
list
    List of survival probabilities of the probability distributions.

Raises
------
MissingNodeInput
    Missing input node error.

checkPST
========

Checks if a structure allows for PST between certain nodes.

Parameters
----------
fromNode : _type_
    Starting node.
toNode : _type_
    Ending node.
Returns
-------
Union([str,bool])
    _description_

Raises
------
MissingNodeInput
    Missing input node error.

checkPST_sympy
==============

Checks if a structure allows for PST between certain nodes.

Parameters
----------
fromNode : _type_
    Starting node.
toNode : _type_
    Ending node.
Returns
-------
Union([str,bool])
    _description_

Raises
------
MissingNodeInput
    Missing input node error.

getTransportEfficiency
======================

Gets the transport efficiency of the quantum walk.

Returns
-------
float
    Transport efficiency of the quantum walk.

getMarkedElements
=================

Gets the marked elements of the quantum walk.

Returns
-------
list
    Marked elements of the quantum walk.

setMarkedElements
=================

Sets the marked elements of the quantum walk.

Parameters
----------
markedElements : list
    Marked elements of the quantum walk.

getQWAK
=======

Gets the QWAK instance.

Returns
-------
QWAK
    QWAK instance.

setQWAK
=======

Sets the QWAK instance's attributes to the ones of the given QWAK instance.

Parameters
----------
newQWAK : QWAK
    QWAK instance to copy the attributes from.

getQWAKId
=========

Gets the QWAK instance's ID.

Returns
-------
str
    QWAK instance's ID.

to_json
=======

Returns a JSON representation of the QWAK instance

Parameters
----------
isDynamic : bool, optional
    If True, the JSON will contain the timeList, probDistList and
    walkList attributes, by default False.

Returns
-------
str
    JSON representation of the QWAK instance.

from_json
=========

Returns a QWAK instance from a JSON representation.

Parameters
----------
json_var : str
    JSON representation of the QWAK instance.
isDynamic : bool, optional
    If True, the JSON will contain the timeList and probDistList attributes,
    by default False.

Returns
-------
QWAK
    QWAK instance from a JSON representation.

