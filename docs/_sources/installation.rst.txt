Installation
============

QWAK is not yet hosted on PiPy, so you will need to install it locally preferably with a virtual environment.
The first step will be to clone the repository:

.. code-block:: console

  git clone https://github.com/JaimePSantos/QWAK.git

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

.. _venv-installation:

Installing QWAK locally with Venv
*********************************

After navigating to the cloned repository, create a python virtual environment:

.. code-block:: console

  python3 -m venv <name_of_env>

Optionally, create a shortcut for the activation executable. If you're on linux simply:

.. code-block:: console

    ln -s /qwakEnv/bin/activate <name_of_env>

And activate the environment with:

.. code-block:: console

    source <name_of_env>

Then you will need to install the dependencies and the package itself using pip as described above.

.. _testing-installation:

Testing the installation
************************

The basic testing script can be run by:

.. code-block:: console

    python installCheck.py

If no errors are thrown and you end up with some plots opened, then the installation was successful.

However, we recommend running the package's unit tests via pytest:

.. code-block:: console

    pip install pytest
    pytest -v tests/
