Usage
=====

.. _walks:

This section outlines the capabilities of the ``QWAK`` package through
specific use cases. Firstly, we examine PST in 4D hypercube graphs. Secondly,
we focus on the transport properties of CTQWs in directed graphs. Further, we
discuss how ``QWAK`` can be employed for quantum search algorithms on
various graph types, namely complete graphs, hypercubes, and the Erdős-Rényi
model. Lastly, we look at stochastic quantum walks for navigating perfect mazes
and examine the impact of noise. Each subsection provides hands-on examples,
demonstrating how to leverage the ``QWAK`` package for these
applications.

Note that all of the following examples can be found in the Notebook directory
of the ``GitHub`` repository
`here <https://github.com/JaimePSantos/QWAK/tree/main/Notebook>`_, and the
code examples assume the user has ``NumPy`` and ``NetworkX``
imported.

.. toctree::
   :maxdepth: 2

   perfectStateTransfer
   orientedQuantumWalk
   searchingQWAK
   stochasticQWAK
