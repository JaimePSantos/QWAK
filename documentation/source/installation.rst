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


And then install the package via:

.. code-block:: console

  pip install .

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