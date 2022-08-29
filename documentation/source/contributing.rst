Contributing
============

Contributing as a few additional steps that may require some explanation for first-time users.
Here, we'll give you step-by-step instructions on how to setup github for contributing to this project, how to format your code changes and how to generate updated documentation.

Setting up the repo for contributing
************************************

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


#. Follow QWAK's `installation instructions <https://jaimepsantos.github.io/QWAK/installation.html>`_.




