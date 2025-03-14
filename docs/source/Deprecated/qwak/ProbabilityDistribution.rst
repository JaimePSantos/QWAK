__init__
========

The dimension of the probability vector will then be loaded from
the state inputted by the user.
The vector containing the probabilities will be initialized full of zeros
with the dimension obtained from the state.

Parameters
----------
state : State
    State to be converted into a probability.

resetProbDist
=============

Resets the ProbabilityDistribution object.

buildProbDist
=============

Builds the probability vector by multiplying the user inputted
amplitude state by its conjugate.

Parameters
----------
state : State, optional
    State to be converted into a probability, by default None

setProbDist
===========

Sets the current probability distribution to a user inputted one.

Parameters
----------
newProbDist : ProbabilityDistribution
    New probability distribution for the object.

getStateVec
===========

Gets the state vector associated with a distribution.

Returns
-------
State
    Returns the state vector of the ProbabilityDistribution object.

getState
========

Gets the state associated with a distribution.

Returns
-------
State
    Returns the state of the ProbabilityDistribution object.

setState
========

Sets the current state to a user inputted one.

Parameters
----------
newState : State
    New state for the distribution.

setDim
======

Sets the current dimension to a user inputted one.

Parameters
----------
newDim : int
    New dimension for the distribution.

getDim
======

Gets the dimension associated with a distribution.

Returns
-------
int
    Returns the dimension of the ProbabilityDistribution object.

setProbVec
==========

Sets the current probability vector to a user inputted one.

Parameters
----------
newProbVec : np.ndarray
    New probability vector for the distribution.

getProbVec
==========

Gets the probability vector associated with a distribution.

Returns
-------
np.ndarray
    Returns the array of the ProbabilityDistribution object.

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
    Probability of the searched node.

moment
======

Calculates the kth moment of the probability distribution.

Parameters
----------
k : int
    User inputted moment.

Returns
-------
float
    kth moment of the probability distribution.

invPartRatio
============

Calculates the inverse participation ratio of the probability distribution.

Returns
-------
float
    Inverse participation ratio of the probability distribution.

stDev
=====

Calculates the standard deviation of the probability distribution.

Returns
-------
float
    Standard deviation of the probability distribution.

survivalProb
============

Calculates the survival probability of the probability distribution.

Parameters
----------
fromNode : _type_
    Starting Node.
toNode : _type_
    Ending node.

Returns
-------
float
    Survival probability of the probability distribution.

to_json
=======

    Converts the ProbabilityDistribution object to a JSON string.

Returns
-------
str
    JSON string of the ProbabilityDistribution object.

from_json
=========

Converts a JSON string to a ProbabilityDistribution object.

Parameters
----------
json_var : Union[str, dict]
    JSON string or dictionary to be converted to a ProbabilityDistribution object.

Returns
-------
ProbabilityDistribution
    ProbabilityDistribution object converted from JSON.

__str__
=======

String representation of the ProbabilityDistribution object.

Returns
-------
str
    String of the ProbabilityDistribution object.

__repr__
========

Representation of the ProbabilityDistribution object.

Returns
-------
str
    String of the ProbabilityDistribution object.

