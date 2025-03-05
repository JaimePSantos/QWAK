.. _conda-installation:

Installing QWAK locally with Anaconda (recommended)
***************************************************
Download and install `Anaconda <https://www.anaconda.com/>`_.

Create a conda environment using:

.. code-block:: console

  conda create -n <name_of_env>

Activate the virtual environment:

.. code-block:: console

  conda activate <name_of_env>

After the environment is setup, you will need to install the core dependencies:

.. code-block:: console

  pip install numpy scipy sympy matplotlib networkx qutip

And if you're interested in using the GUI you will also need:

.. code-block:: console

  pip install eel

After the dependencies are met, you will only need to assure you navigated to the cloned directory:

.. code-block:: console

  cd <path-to-cloned-folders>/QWAK/

And then install the package via PyPi:

.. code-block:: console

  pip install qwak-sim

Or locally through:

.. code-block:: console

  pip install .

.. note:: If you're installing the package for development purposes run

            pip install -e .

          This allows for code changes that do not require re-installation of the package.

.. WARNING:: The GUI was migrated to a fullstack web app and some changes were made to the GraphicalQWAK class.

             For this reason, the local eel GUI might be temporarily unavailable.
