.. _venv-setup:

Setting up QWAK with Venv
*************************

After navigating to the cloned repository, create a Python virtual environment:

.. code-block:: console

  python3 -m venv <name_of_env>

Optionally, create a shortcut for the activation executable. If you're on Linux, simply:

.. code-block:: console

    ln -s /qwakEnv/bin/activate <name_of_env>

Activate the environment with:

.. code-block:: console

    source <name_of_env>

Then you will need to install the dependencies and the package itself using pip as described above.
