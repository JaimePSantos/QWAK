Installation
============

To install QWAK you require python 3.10 or newer.

1. Set up your environment:
   - Instructions for setting up the environment with conda can be found :ref:`here <conda-setup>`.
   - Instructions for setting up the environment with venv can be found :ref:`here <venv-setup>`.

2. Ensure all required :ref:`dependencies <dependencies>` are met. GPU users can refer to the `CuPy installation guide <https://docs.cupy.dev/en/stable/install.html>`_, which requires the `CUDA Toolkit <https://developer.nvidia.com/cuda-toolkit>`_.

3. Install the package via PyPi:

.. code-block:: console

  pip install qwak-sim

Local Installation
******************
To install QWAK locally, follow these steps:

1. Clone the repository:

.. code-block:: console

  git clone https://github.com/JaimePSantos/QWAK.git

2. Navigate to the cloned repository:

.. code-block:: console

  cd QWAK

3. Install the package:

.. code-block:: console

  pip install .

.. note::

  If you want to contribute to the development of QWAK, you can install it in edit mode by using the following command:

  .. code-block:: console

    pip install -e .

.. _testing-installation:

Testing the installation
************************

The preferred way to check the installation is by running the `installcheck.py` script. This script provides several options for running different sets of tests.

To use the script, run the following command:

.. code-block:: console

  python installcheck.py [option]

Available options are:
- `full`: Runs all tests.
- `cupy`: Runs tests related to CuPy.
- `Stochastic`: Runs stochastic tests.
- `qwakpath`: Runs QWAK path tests.
- `stochasticQwak`: Runs stochastic QWAK tests.
- `cycle`: Runs cycle tests.
- `complete`: Runs complete tests.

For example, to run all tests, use:

.. code-block:: console

  python installcheck.py full

If no errors are thrown and you end up with some plots opened, then the installation was successful. For more detailed testing, refer to the :doc:`installcheck <installcheck>` module documentation.

.. toctree::
   :maxdepth: 1

   conda-setup
   venv-setup
   dependencies
   localGUI
