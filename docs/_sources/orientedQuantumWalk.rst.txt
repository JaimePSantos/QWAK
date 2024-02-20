Directed Quantum Walk
=====================

.. WARNING:: This page is under construction.

A directed graph :math:`G=(V,E)` differs from its undirected counterpart by having
ordered vertex pairs in :math:`E`. Early work established *strong
quadrangularity* and *graph reversibility* as prerequisites for coined
quantum walks (CQWs) on such graphs. Recent
studies show performance gains in centrality ranking via CTQWs, with applications like PageRank.
Other models, like *staggered quantum walks*, have also been defined in these structures.

Directed graphs exhibit distinct transport properties, requiring different
methods to characterize state transfer. Additionally,
these graphs can exhibit new phenomena, such as zero state transfer.

In the subsequent sections, we will demonstrate how to use ``QWAK`` for
simulating CTQWs on directed infinite lines and explore the *enhanced
decay rate* of the survival probability in more general
structures.

Dynamics
~~~~~~~~

To define a directed infinite line, as shown in the figure below,
we use the Hamiltonian :math:`H` given by equation

.. math::
   :label: hamiltonian

   H = \sum_{x = L}^{R}e^{i\alpha}\ket{x+1}\bra{x}+e^{-i\alpha}\ket{x-1}\bra{x},

where :math:`L` and :math:`R` are the left and right borders of
the line, respectively. We can obtain an infinite path graph by setting
:math:`R\rightarrow\infty` and :math:`L\rightarrow -\infty`.

.. |orientedLineGraph| image:: ../../Images/SoftwareUsage/DirectedQW/oriented_infinite_line.png
   :width: 60 %
   :align: middle

|orientedLineGraph|

We implement the *finite* line using the ``path_graph`` function and add direction to it using
the ``getWeightedGraph`` function available in the notebook.

.. code-block:: python
   :linenos:

   n = 100
   alpha = np.pi/2
   weight = np.exp(1j*alpha)
   baseGraph = nx.path_graph(n, create_using=nx.DiGraph)
   graph = getWeightedGraph(baseGraph, weight)

Inspired by previous work, we choose a non-localized
initial condition given by equation

.. math::
   :label: eq:survProbInitCond

   \ket{\psi(0)} = \cos(\theta)\ket{-k} + e^{i\gamma}\sin(\theta)\ket{k},

which can be easily implemented in Python.

.. code-block:: python
   :linenos:

   k = 1
   theta = np.pi/4
   l = 0
   gamma = l * np.pi

   initCond = [(n//2-k, np.cos(theta)), (n//2+k, np.exp(1j*gamma)*np.sin(theta))]

After initializing the ``QWAK`` object, we
compute the walk using the ``runWalk`` method. To specify a
non-localized initial condition, we pass the ``customStateList`` parameter
to provide both the node and its corresponding amplitude.

.. code-block:: python
   :linenos:

   t = 35

   qw = QWAK(graph)
   qw.runWalk(time = t, customStateList = initCond)

   probVec = qw.getProbVec()

The probability distribution is obtained using the ``getProbVec`` method. To
study how the evolution of the probability distribution changes with different
graph weights, the following figure displays the CTQW
for multiple values of :math:`\alpha`.

.. |orientedDynamicsPath| image:: ../../Images/SoftwareUsage/DirectedQW/orDynN512NW3Alpha0.79-1.57TMAX110.png
   :width: 50 %
   :align: middle

|orientedDynamicsPath|

Indeed, the value of :math:`\alpha` has a severe impact on the dynamics of the walk.
In the case of an undirected graph (:math:`\alpha = 0`), symmetry is expected around
the center node; however, varying values of :math:`\alpha` can alter the shape of the
distribution, presenting a method of controlling how the walker propagates
throughout the structure.

Survival Probability
~~~~~~~~~~~~~~~~~~~~
The survival probability of a quantum walk can be characterized as the mean
probability of finding the walker in a certain location after some time :math:`t`.
Considering the symmetric position range of :math:`[k_0,k_1]`, this
quantity will be

.. math::
   P_{[k_0,k_1]}(t)=\sum_{i=k_0}^{k_1} P_{i}(t).

Here, we will use ``QWAK`` to run the walk for an interval using multiple
values of :math:`\alpha`. Classically, the survival probability decays at a rate
proportionate to :math:`t^{-\frac{1}{2}}`, while a quantum walk typically decays
quadratically faster at a rate of :math:`t^{-1}`. It is known, however, that certain
initial conditions can achieve *enhanced decay rate*, scaling with :math:`t^{-3}`.

.. |decRateOriented| image:: ../../Images/SoftwareUsage/DirectedQW/decMatrix512NW3_Alpha1.05-1.57S500TMAX100.png
   :width: 50 %
   :align: middle

|decRateOriented|

Using the previously defined directed graph and the chosen initial condition, we
can analyze the impact of varying :math:`\alpha` values on the decay rate of the
survival probability:

.. code-block:: python
   :linenos:

   timeList = np.linspace(0, 100, 500)
   alphaList = [0, np.pi/3, np.pi/2]
   decayRateMatrix = []
   for alpha in alphaList:
       weight = np.exp(1j * alpha)
       graph = getWeightedGraph(baseGraph, weight)
       qw = QWAK(graph)
       qw.runMultipleWalks(timeList, customStateList=initCond)
       decayRateMatrix.append(
                     qw.getSurvivalProbList(N//2 - k, N//2 + k))

   plt.loglog()
   for decayRate in decayRateMatrix:
       plt.plot(survProbList)
   plt.show()

The code iterates through a list of :math:`\alpha` values, generating a directed
graph for each and computing the corresponding survival probabilities over
time. These are stored in a decay rate matrix for log-log plotting, as shown in the previous figure.

Directional line graphs enable more effective control of interference effects in quantum walks. This
allows for both normal and enhanced decay rates under broader initial
conditions. The figure shows that an optimal :math:`\alpha` value can be chosen to
accelerate decay, irrespective of :math:`k`'s parity.
