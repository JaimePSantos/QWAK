Usage
=====

.. _installation:

Installation
------------

To use QWAK, first install it using pip:

.. code-block:: console

   (.venv) $ pip install .

.. _walks:

Creating Walks
----------------

To retrieve a list of random ingredients,
you can use the ``QWAK`` class:

.. py:class:: QWAK(graph: nx.Graph, laplacian: bool = False, markedSearch=None)

        Default values for the initial state, time and transition rate are a column vector full of 0s, 0 and 1,
        respectively. Methods runWalk or buildWalk must then be used to generate the results of the quantum walk.

        Args:
            :param laplacian: Allows the user to choose whether to use the Laplacian or simple adjacency matrix.
            :type laplacian: bool
            :param graph: NetworkX graph where the walk takes place. Also used for defining the dimensions of the quantum walk.
            :type graph: NetworkX.Graph

