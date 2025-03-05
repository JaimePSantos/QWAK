Installation
============
To install QWAK, follow these steps:

1. Set up your environment:
  - You can find instructions for setting up the environment with conda :ref:`here <conda-installation>` and with venv :ref:`here <venv-installation>`.
  - You can also find all the dependencies.

2. Ensure all required :ref:`dependencies <dependencies>` are met. GPU users can refer to the `CuPy installation guide <https://docs.cupy.dev/en/stable/install.html>`_ which requires the `CUDA Toolkit <https://developer.nvidia.com/cuda-toolkit>`_.

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

The preferred way to check the installation is by running the package's unit tests via pytest:

.. code-block:: console

  pip install pytest
  pytest -v tests/

An update to the installation check script is coming soon. For now, you can also run the basic testing script:

.. code-block:: console

  python installCheck.py

If no errors are thrown and you end up with some plots opened, then the installation was successful. For more detailed testing, refer to the :doc:`installcheck <installcheck>` module documentation.
