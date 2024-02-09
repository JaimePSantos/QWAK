Searching With QWAK
===================

.. WARNING:: This page is under construction.

Here, we will go over the searching algorithm using QWAK for several different structures.

Complete Graph - Single Element
-------------------------------

To use QWAK for searching, we need to define a graph for the search space, and
the targets are marked elements, specified as a list of weighted node indices.
For a complete graph, the optimal transition rate is :math:`\gamma = \frac{1}{n}`,
resulting in a search time of :math:`\mathcal{O}(\sqrt{N})`, comparable to Grover's
algorithm.

.. code-block:: python
   :linenos:

   n = 200
   t = (np.pi/2) * np.sqrt(n)
   gamma = 1/n
   init = list(range(0,n))
   graph = nx.complete_graph(n)
   qw = QWAK(graph, gamma=gamma, markedElements=[(n//2, -1)],
             laplacian=False)
   qw.runWalk(t, initStateList=init)

Firstly, we initialize ``QWAK`` with the desired simulation parameters,
so that we can calculate the search problem via the ``runWalk`` method.
Because we created the object with a list of marked elements, the Hamiltonian
of the method will be described as:

.. math::
   H^\prime = -\gamma A - \sum_{x \in M} \ket{x}\bra{x}

.. |completeGraphSearching| image:: ../../Images/SoftwareUsage/Searching/completePlot_N512_NWALKS3_S200.png
   :width: 50 %
   :align: middle

|completeGraphSearching|

The optimal time for the search problem also depends on the number of solutions,
and the previous figurepresents the evolution of the sum probability of all the
marked elements. The utility functions needed to plot thisfigure are available
in the package.

Multiple Elements
^^^^^^^^^^^^^^^^^

.. code-block:: python
   :linenos:

   markedElements = [(n//2,-1),(n//2+1,-1)]
   t = (np.pi/2) * np.sqrt(n/len(markedElements))

To search for multiple elements, we simply extend the ``markedElements``
list and fine-tune the optimal evolution time. The aforementioned figure
demonstrates that as the number of marked elements increases, the time required
to reach maximum probability decreases. Specifically, when we mark
:math:`\frac{1}{4}` of the total elements, the walk evolves optimally in time :math:`\pi`.
This scenario is analogous to the *single-shot Grover algorithm*, where
the highest probability for finding the solution is achieved in just one step.

