============
Contributing
============

Contributing has a few additional steps that may require some explanation for first-time users.
Here, we'll give you step-by-step instructions on how to setup github for contributing to this project,
how to format your code changes and how to generate updated documentation.

A few extra packages are required when contributing to QWAK:

.. code-block:: shell

    pip install autopep8 pytest bumpver

`Autopep8 <https://pypi.org/project/autopep8/>`_ formats code according to the PEP 8 style.
`Pytest <https://docs.pytest.org/en/7.1.x/>`_ is responsible for unit testing the package to assure everything
working correctly after a change.
`Bumpver <https://github.com/mbarkhau/bumpver/>`_ manages package versioning.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

   genDoc
   pypi

Setting up the repo for contributing
------------------------------------

#. Install `git <https://git-scm.com/.>`_.

#. Fork the `QWAK <https://github.com/JaimePSantos/QWAK>`_ repository to your account so you can work on own copy. This will allow you to open Pull Requests later.

#. Add the upstream repository:

   .. code-block:: shell

      git remote add upstream https://github.com/JaimePSantos/QWAK.git

#. Update your fork with:

   .. code-block:: shell

      git checkout main

   Followed by:

   .. code-block:: shell

      git pull --rebase upstream main

   This should be done somewhat regularly to ensure your fork is up-to-date with the most recent QWAK version.

#. Follow QWAK's `installation instructions <https://jaimepsantos.github.io/QWAK/installation.html>`_ in case you haven't installed the package yet.

   .. code-block:: shell

      pip install -e .

   This should be used to install your package in editable mode.

Making your changes
-------------------

#. Checkout and sync your main branch with the upstream to reflect the newest version:

   .. code-block:: shell

      git checkout main
      git pull --rebase upstream main

#. Create a new branch to work on instead of main:

   .. code-block:: shell

      git checkout -b <new_branch_name> upstream/main

#. If this is the first time you're building the package:

   .. code-block:: shell

      python -m pip install --upgrade build
      python -m build

   This might not be needed, will test in the future and update the docs accordingly.

#. Make your changes.

#. Ensure your changes does not break the existing code by running the following command inside the main project folder:

   .. code-block:: shell

      pytest -v tests/

#. If all the tests are successfull, format your changed files with:

   .. code-block:: shell

      autopep8 --in-place --aggressive --aggressive --max-line-length 72 <path_to_file>

   Or, alternatively an entire folder with:

   .. code-block:: shell

      autopep8 --recursive --in-place --aggressive --aggressive --max-line-length 72 <path_to_folder>

#. In case a version bump is required:

   .. code-block:: shell

       bumpver update --patch

#. Commit your changes:

   .. code-block:: shell

      git commit -am <commit message>

   Make sure you write a short descriptive message so that the changes on the commit can be easily identified.

#. Push your changes to your fork:

   .. code-block:: shell

      git push -u origin <branch name>

#. Visit your repo on github and create a pull request to the main repo!