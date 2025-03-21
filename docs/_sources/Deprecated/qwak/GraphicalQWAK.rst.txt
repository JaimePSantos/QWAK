__init__
========

_summary_

Parameters
----------
staticN : int
    _description_
dynamicN : int
    _description_
staticGraph : nx.Graph
    _description_
dynamicGraph : nx.Graph
    _description_
staticStateList : list
    _description_
dynamicStateList : list
    _description_
staticTime : float
    _description_
dynamicTimeList : list
    _description_
staticGamma : float
    _description_
dynamicGamma : float
    _description_

to_json
=======

_summary_

Returns
-------
str
    _description_

from_json
=========

_summary_

Parameters
----------
json_str : str
    _description_

Returns
-------
Operator
    _description_

runWalk
=======

_summary_

Returns
-------
_type_
    _description_

runMultipleWalks
================

_summary_

Returns
-------
_type_
    _description_

setStaticDim
============

_summary_

Parameters
----------
newDim : _type_
    _description_
graphStr : _type_
    _description_
initStateList : _type_, optional
    _description_, by default None

setDynamicDim
=============

_summary_

Parameters
----------
newDim : _type_
    _description_
graphStr : _type_
    _description_

getStaticDim
============

_summary_

Returns
-------
_type_
    _description_

getDynamicDim
=============

_summary_

Returns
-------
_type_
    _description_

setStaticGraph
==============

_summary_

Parameters
----------
newGraphStr : _type_
    _description_

setDynamicGraph
===============

_summary_

Parameters
----------
newGraphStr : _type_
    _description_

setStaticCustomGraph
====================

_summary_

Parameters
----------
customAdjacency : _type_
    _description_

setDynamicCustomGraph
=====================

_summary_

Parameters
----------
customAdjacency : _type_
    _description_

getStaticGraph
==============

_summary_

Returns
-------
_type_
    _description_

getDynamicGraph
===============

_summary_

Returns
-------
_type_
    _description_

getStaticGraphToJson
====================

_summary_

Returns
-------
_type_
    _description_

getDynamicGraphToJson
=====================

_summary_

Returns
-------
_type_
    _description_

getStaticAdjacencyMatrix
========================

_summary_

Returns
-------
_type_
    _description_

getDynamicAdjacencyMatrix
=========================

_summary_

Returns
-------
_type_
    _description_

setStaticTime
=============

_summary_

Parameters
----------
newTime : _type_
    _description_

getStaticTime
=============

_summary_

Returns
-------
_type_
    _description_

setDynamicTime
==============

_summary_

Parameters
----------
newTimeList : _type_
    _description_

getDynamicTime
==============

_summary_

Returns
-------
_type_
    _description_

setDynamicInitStateList
=======================

_summary_

Parameters
----------
newInitStateList : _type_
    _description_

setStaticInitState
==================

_summary_

Parameters
----------
initStateStr : _type_
    _description_

getStaticInitState
==================

_summary_

Returns
-------
_type_
    _description_

getDynamicInitStateList
=======================

_summary_

Returns
-------
_type_
    _description_

getStaticProbDist
=================

_summary_

Returns
-------
_type_
    _description_

getDynamicProbDistList
======================

_summary_

Returns
-------
_type_
    _description_

getStaticProbVec
================

_summary_

Returns
-------
_type_
    _description_

getDynamicProbVecList
=====================

_summary_

Returns
-------
_type_
    _description_

getStaticMean
=============

_summary_

Returns
-------
_type_
    _description_

getDynamicMean
==============

_summary_

Returns
-------
_type_
    _description_

getStaticSndMoment
==================

_summary_

Returns
-------
_type_
    _description_

getDynamicSndMoment
===================

_summary_

Returns
-------
_type_
    _description_

getStaticStDev
==============

_summary_

Returns
-------
_type_
    _description_

getDynamicStDev
===============

_summary_

Returns
-------
_type_
    _description_

getStaticSurvivalProb
=====================

_summary_

Parameters
----------
k0 : _type_
    _description_
k1 : _type_
    _description_

Returns
-------
_type_
    _description_

getDynamicSurvivalProb
======================

_summary_

Parameters
----------
k0 : _type_
    _description_
k1 : _type_
    _description_

Returns
-------
_type_
    _description_

getStaticInversePartRatio
=========================

_summary_

Returns
-------
_type_
    _description_

getDynamicInvPartRatio
======================

_summary_

Returns
-------
_type_
    _description_

checkPST
========

_summary_

Parameters
----------
nodeA : _type_
    _description_
nodeB : _type_
    _description_

Returns
-------
_type_
    _description_

